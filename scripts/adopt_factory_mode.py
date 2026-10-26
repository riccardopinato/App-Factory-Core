#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

CORE_ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = CORE_ROOT / "adoption/FACTORY_MODE_PROFILE_v1.yaml"
TEMPLATE_PATH = CORE_ROOT / "adoption/APP_FACTORY_ADOPTION.yaml"
VALIDATOR_PATH = CORE_ROOT / "scripts/validate_factory_adoption.py"
MANIFEST_NAME = "APP_FACTORY_ADOPTION.yaml"
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return payload


def workflow_files(repo_root: Path) -> list[str]:
    root = repo_root / ".github" / "workflows"
    if not root.is_dir():
        return []
    return sorted(
        path.relative_to(repo_root).as_posix()
        for path in root.iterdir()
        if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}
    )


def desired_manifest(repository: str, existing: dict[str, Any]) -> dict[str, Any]:
    template = load_yaml(TEMPLATE_PATH)
    desired = dict(existing)
    desired["schema_version"] = 1
    desired["repository"] = repository
    desired["factory"] = dict(template["factory"])
    desired["workflow_integration"] = dict(template["workflow_integration"])
    desired["applab"] = dict(existing.get("applab") or template["applab"])
    desired["applab"]["mode"] = "CENTRAL"
    desired.setdefault("app_overrides", {})
    if not isinstance(desired["app_overrides"], dict):
        raise ValueError("app_overrides must be an object")
    return desired


def dump_yaml(payload: dict[str, Any]) -> str:
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Adopt the central App Factory mode in an app repository.")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    repository = args.repository.strip()
    if not repo_root.is_dir():
        parser.error("--repo-root must be an existing directory")
    if repository == "REPLACE_ME/REPLACE_ME" or not REPOSITORY_RE.fullmatch(repository):
        parser.error("--repository must be owner/repository")

    manifest_path = repo_root / MANIFEST_NAME
    existing = load_yaml(manifest_path)
    before = manifest_path.read_text(encoding="utf-8") if manifest_path.is_file() else ""
    desired = desired_manifest(repository, existing)
    rendered = dump_yaml(desired)
    workflows = workflow_files(repo_root)

    plan = {
        "schema_version": 1,
        "repository": repository,
        "mode": "ROADMAP_FAST_PLUS_CONTINUOUS_MAINTENANCE",
        "manifest_path": str(manifest_path),
        "manifest_exists": manifest_path.is_file(),
        "manifest_change_required": before != rendered,
        "existing_workflows": workflows,
        "workflow_action": (
            "PRESERVE_EXISTING_AND_INTEGRATE"
            if workflows
            else "NO_EXISTING_WORKFLOW_ADD_ONLY_IF_REQUIRED"
        ),
        "workflow_files_modified_by_adopter": [],
        "dry_run": not args.apply,
    }

    if args.apply and before != rendered:
        manifest_path.write_text(rendered, encoding="utf-8")

    if args.apply:
        validation = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--repo-root", str(repo_root), "--json"],
            cwd=CORE_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if validation.returncode != 0:
            print(validation.stdout)
            print(validation.stderr, file=sys.stderr)
            return validation.returncode
        plan["validation"] = json.loads(validation.stdout)
        plan["manifest_change_required_after_apply"] = False

    if args.json:
        print(json.dumps(plan, indent=2, sort_keys=True))
    else:
        print("APP FACTORY ADOPTION PLAN")
        print(f"Repository: {repository}")
        print(f"Manifest change required: {plan['manifest_change_required']}")
        print(f"Workflow action: {plan['workflow_action']}")
        if not args.apply:
            print("Dry run only. Use --apply to write the manifest.")
        else:
            print("Adoption manifest aligned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
