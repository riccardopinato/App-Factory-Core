#!/usr/bin/env python3
"""Read-only Spec Lite change/PR drift check. Not a GitHub/API verifier or CI authority."""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
from pathlib import Path
from typing import Any

from validate_spec_lite import validate_manifest


def _overlap(a: str, b: str) -> bool:
    """Conservative path collision check; ambiguous patterns are reported, not auto-merged."""
    if a == b:
        return True
    for x, y in ((a, b), (b, a)):
        if x.endswith("/**") and (y == x[:-3] or y.startswith(x[:-3] + "/")):
            return True
        if fnmatch.fnmatchcase(y, x):
            return True
    # Two glob expressions can intersect without either matching the other's
    # literal pattern (lib/*/foo.dart and lib/widgets/*.dart, for example).
    # Fail conservative as REVIEW, not automatic conflict or auto-merge.
    if "*" in a and "*" in b:
        def fixed_root(pattern: str) -> str:
            parts = []
            for part in pattern.split("/"):
                if any(c in part for c in "*?["):
                    break
                parts.append(part)
            return "/".join(parts)
        ra, rb = fixed_root(a), fixed_root(b)
        if not ra or not rb or ra == rb or ra.startswith(rb + "/") or rb.startswith(ra + "/"):
            return True
    return False


def review(docs: list[dict[str, Any]], *, heads: dict[str, str] | None,
           open_prs: list[dict[str, Any]] | None,
           canonical: dict[str, dict[str, Any]] | None) -> dict[str, Any]:
    """Caller-supplied snapshots are UNTRUSTED unless independently authenticated."""
    errors: set[str] = set()
    warnings: set[str] = set()
    checked: list[str] = []
    if not isinstance(heads, dict):
        errors.add("HEAD_SNAPSHOT_REQUIRED")
    if not isinstance(open_prs, list):
        errors.add("OPEN_PR_SNAPSHOT_REQUIRED")
    if not isinstance(canonical, dict):
        errors.add("CANONICAL_REQUIREMENT_SNAPSHOT_REQUIRED")
    keys: dict[tuple[str, str, str], str] = {}
    groups: dict[str, list[tuple[str, set[str]]]] = {}
    for d in docs:
        if not isinstance(d, dict):
            errors.add("INVALID_MANIFEST")
            continue
        spec_id = d.get("spec_id", "<missing>")
        repo = d.get("target", {}).get("repository")
        source_sha = d.get("target", {}).get("source_sha")
        if not isinstance(repo, str) or not isinstance(source_sha, str):
            errors.add(f"INVALID_TARGET:{spec_id}")
            continue
        checked.append(spec_id)
        if isinstance(heads, dict) and heads.get(repo) != source_sha:
            errors.add(f"STALE_TARGET_HEAD:{spec_id}")
        # Complete structural admission is still mandatory.
        issues = validate_manifest(d, expected_factory_sha=d.get("factory", {}).get("sha", ""),
                                   expected_source_sha=source_sha)
        errors.update(f"INVALID_MANIFEST:{spec_id}:{x}" for x in issues)
        paths = d.get("scope", {}).get("allowed_paths", [])
        groups.setdefault(repo, []).append((spec_id, set(paths) if isinstance(paths, list) else set()))
        for req in d.get("requirements", []):
            rid = req.get("id")
            delta = req.get("delta") or {}
            previous = delta.get("previous")
            key = (repo, str(previous.get("spec_id", spec_id)) if isinstance(previous, dict) else spec_id,
                   str(previous.get("requirement_id", rid)) if isinstance(previous, dict) else rid)
            if key in keys:
                errors.add(f"OVERLAPPING_REQUIREMENT_CHANGE:{keys[key]}:{spec_id}:{key[2]}")
            keys[key] = spec_id
            if delta.get("operation") in ("MODIFIED", "REMOVED", "RENAMED"):
                if isinstance(previous, dict):
                    lookup = f"{repo}@{previous.get('source_sha')}:{previous.get('spec_id')}:{previous.get('requirement_id')}"
                    if not isinstance(canonical, dict) or lookup not in canonical:
                        errors.add(f"PREVIOUS_REQUIREMENT_NOT_VERIFIED:{spec_id}:{rid}")
                    elif canonical[lookup].get("status") != "CURRENT":
                        errors.add(f"PREVIOUS_REQUIREMENT_NOT_CURRENT:{spec_id}:{rid}")
                else:
                    errors.add(f"PREVIOUS_REQUIREMENT_MISSING:{spec_id}:{rid}")

    for repo, entries in groups.items():
        for i, (name, paths) in enumerate(entries):
            for other, opaths in entries[i+1:]:
                if any(_overlap(a, b) for a in paths for b in opaths):
                    warnings.add(f"PATH_OVERLAP_REVIEW:{repo}:{name}:{other}")

    for pr in open_prs if isinstance(open_prs, list) else []:
        if not isinstance(pr, dict) or not isinstance(pr.get("repository"), str):
            errors.add("INVALID_PR_SNAPSHOT_RECORD")
            continue
        repo, number = pr["repository"], pr.get("number", "unknown")
        affected = pr.get("requirements")
        if affected is None or not isinstance(affected, list):
            errors.add(f"PR_REQUIREMENT_COVERAGE_UNKNOWN:{repo}:{number}")
            continue
        for reqkey in affected:
            if (not isinstance(reqkey, dict)
                or not isinstance(reqkey.get("spec_id"), str)
                or not re.fullmatch(r"FSL-[A-Z0-9][A-Z0-9-]{5,63}", reqkey["spec_id"])
                or not isinstance(reqkey.get("requirement_id"), str)
                or not re.fullmatch(r"FR-[0-9]{3}", reqkey["requirement_id"])):
                errors.add(f"PR_REQUIREMENT_IDENTITY_MISSING:{repo}:{number}")
                continue
            key = (repo, reqkey["spec_id"], reqkey["requirement_id"])
            if key in keys:
                errors.add(f"OPEN_PR_REQUIREMENT_CONFLICT:{repo}:{number}:{keys[key]}:{key[2]}")
        changed = pr.get("changed_paths")
        if not isinstance(changed, list):
            warnings.add(f"PR_PATH_COVERAGE_UNKNOWN:{repo}:{number}")
        else:
            for name, paths in groups.get(repo, []):
                if any(_overlap(a, b) for a in paths for b in changed if isinstance(b, str)):
                    warnings.add(f"OPEN_PR_PATH_OVERLAP_REVIEW:{repo}:{number}:{name}")

    return {
        "status": "BLOCKED" if errors else "REVIEW_ONLY_NOT_CERTIFIED",
        "checked_specs": sorted(checked), "errors": sorted(errors),
        "warnings": sorted(warnings), "snapshot_authenticity": "NOT_ATTESTED",
        "writes_performed": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifests", nargs="+", required=True, type=Path)
    p.add_argument("--heads", type=Path, required=True)
    p.add_argument("--open-prs", type=Path, required=True)
    p.add_argument("--canonical", type=Path, required=True)
    args = p.parse_args()
    try:
        docs = [json.loads(p.read_text(encoding="utf-8")) for p in args.manifests]
        heads = json.loads(args.heads.read_text(encoding="utf-8"))
        prs = json.loads(args.open_prs.read_text(encoding="utf-8"))
        canonical = json.loads(args.canonical.read_text(encoding="utf-8"))
        result = review(docs, heads=heads, open_prs=prs, canonical=canonical)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        result = {"status": "BLOCKED", "errors": [f"INPUT_ERROR:{type(exc).__name__}"],
                  "writes_performed": False}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "REVIEW_ONLY_NOT_CERTIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
