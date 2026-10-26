#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

CORE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = CORE_ROOT / "adoption/FACTORY_MODE_PROFILE_v1.yaml"
MANIFEST_NAME = "APP_FACTORY_ADOPTION.yaml"
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML {path}: {exc}") from exc


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def workflow_files(repo_root: Path) -> list[str]:
    root = repo_root / ".github" / "workflows"
    if not root.is_dir():
        return []
    return sorted(
        path.relative_to(repo_root).as_posix()
        for path in root.iterdir()
        if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}
    )


def validate(repo_root: Path, profile_path: Path = DEFAULT_PROFILE) -> dict[str, Any]:
    errors: list[str] = []
    manifest_path = repo_root / MANIFEST_NAME
    if not manifest_path.is_file():
        return {
            "aligned": False,
            "errors": [f"missing {MANIFEST_NAME}"],
            "repository": "",
            "existing_workflows": workflow_files(repo_root),
            "workflow_action": "NOT_EVALUATED",
        }

    manifest = load_yaml(manifest_path)
    profile = load_yaml(profile_path)
    schema = load_json(CORE_ROOT / "schemas" / "factory_adoption.schema.json")

    if not isinstance(manifest, dict):
        errors.append("adoption manifest must be an object")
        manifest = {}
    if not isinstance(profile, dict):
        errors.append("Factory mode profile must be an object")
        profile = {}

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in sorted(validator.iter_errors(manifest), key=lambda x: list(x.path)):
        location = ".".join(str(x) for x in err.path) or "<root>"
        errors.append(f"manifest schema violation at {location}: {err.message}")

    repository = str(manifest.get("repository", ""))
    if repository == "REPLACE_ME/REPLACE_ME" or not REPOSITORY_RE.fullmatch(repository):
        errors.append("repository must be the real owner/repository")

    factory = manifest.get("factory") if isinstance(manifest.get("factory"), dict) else {}
    if factory.get("profile_version") != profile.get("profile_version"):
        errors.append("manifest profile_version does not match canonical profile")
    if factory.get("profile_path") != "adoption/FACTORY_MODE_PROFILE_v1.yaml":
        errors.append("manifest must point to the canonical Factory mode profile")

    workflow = manifest.get("workflow_integration") if isinstance(manifest.get("workflow_integration"), dict) else {}
    profile_workflow = profile.get("workflow_integration") if isinstance(profile.get("workflow_integration"), dict) else {}
    if workflow.get("strategy") != profile_workflow.get("strategy"):
        errors.append("workflow integration strategy drift")
    if workflow.get("overwrite_existing") is not False:
        errors.append("existing workflows must never be overwritten by adoption")
    if profile_workflow.get("overwrite_existing_workflows") is not False:
        errors.append("canonical profile illegally permits workflow overwrite")

    workflows = workflow_files(repo_root)
    action = (
        "PRESERVE_EXISTING_AND_INTEGRATE"
        if workflows
        else "NO_EXISTING_WORKFLOW_ADD_ONLY_IF_REQUIRED"
    )

    return {
        "aligned": not errors,
        "errors": errors,
        "repository": repository,
        "profile_id": profile.get("profile_id"),
        "profile_version": profile.get("profile_version"),
        "mode": profile.get("mode"),
        "existing_workflows": workflows,
        "workflow_action": action,
        "workflow_overwrite_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate per-app App Factory adoption.")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate(Path(args.repo_root).resolve(), Path(args.profile).resolve())
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("APP FACTORY ADOPTION: " + ("PASS" if report["aligned"] else "FAIL"))
        print(f"Workflow action: {report['workflow_action']}")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["aligned"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
