#!/usr/bin/env python3
"""Prepare a deterministic post-merge delta reconciliation PREVIEW; never write product truth."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from validate_spec_lite import validate_manifest

_SHA = re.compile(r"^[0-9a-f]{40}$")


def reconcile(manifest: dict[str, Any], canonical: dict[str, dict[str, Any]],
              receipts: dict[str, Any]) -> dict[str, Any]:
    errors: set[str] = set()
    result = dict(canonical)   # Preserve unrelated canonical entries.
    spec = manifest.get("spec_id", "")
    target = manifest.get("target", {})
    repo = target.get("repository", "")
    checks = manifest.get("validation", {}).get("required_checks", [])
    # Validate complete schema/semantic contract before considering receipts.
    # Trusted expected SHA values must be supplied separately from the manifest.
    admission_errors = validate_manifest(
        manifest, expected_factory_sha=receipts.get("factory_sha", ""),
        expected_source_sha=receipts.get("source_sha", ""),
    )
    errors.update(f"INVALID_MANIFEST:{error}" for error in admission_errors)
    if receipts.get("merged") is not True:
        errors.add("MERGED_PR_REQUIRED")
    if not _SHA.fullmatch(str(receipts.get("merge_sha", ""))):
        errors.add("INVALID_MERGE_SHA")
    if receipts.get("ci_conclusion") != "success":
        errors.add("GREEN_POSTMERGE_CI_REQUIRED")
    if receipts.get("ci_head_sha") != receipts.get("merge_sha"):
        errors.add("POSTMERGE_CI_SHA_MISMATCH")
    if not str(receipts.get("pr_url", "")).startswith("https://github.com/"):
        errors.add("PR_RECEIPT_REQUIRED")
    evidence = receipts.get("checks", {})
    if not isinstance(evidence, dict):
        evidence = {}
    for kind in checks:
        if not str(evidence.get(kind, "")).startswith("https://github.com/"):
            errors.add(f"MISSING_REQUIRED_CHECK_EVIDENCE:{kind}")
    if manifest.get("approval", {}).get("status") != "APPROVED":
        errors.add("PRODUCT_APPROVAL_REQUIRED")
    if manifest.get("mode") == "CONTROLLED" and not str(
        receipts.get("human_gate_evidence", "")).startswith("https://github.com/"):
        errors.add("CONTROLLED_HUMAN_GATE_EVIDENCE_REQUIRED")
    for req in manifest.get("requirements", []):
        rid = req.get("id")
        delta = req.get("delta") or {"operation": "ADDED", "previous": None}
        action = delta.get("operation")
        previous = delta.get("previous")
        key = f"{repo}:{spec}:{rid}"
        prior_history = []
        if action in ("MODIFIED", "REMOVED", "RENAMED"):
            if not isinstance(previous, dict):
                errors.add(f"PREVIOUS_REFERENCE_REQUIRED:{rid}")
                continue
            previous_key = f"{repo}:{previous.get('spec_id')}:{previous.get('requirement_id')}"
            found = result.get(previous_key)
            if not isinstance(found, dict) or found.get("source_sha") != previous.get("source_sha"):
                errors.add(f"PREVIOUS_REQUIREMENT_SNAPSHOT_MISMATCH:{rid}")
                continue
            if found.get("status") != "CURRENT":
                errors.add(f"PREVIOUS_REQUIREMENT_NOT_CURRENT:{rid}")
                continue
            if action == "MODIFIED" and key != previous_key:
                errors.add(f"MODIFIED_MUST_KEEP_REQUIREMENT_ID:{rid}")
                continue
            if action == "MODIFIED":
                prior_history = list(found.get("history", []))
                prior_history.append({
                    "source_sha": found.get("source_sha"),
                    "text": found.get("text"),
                    "acceptance": found.get("acceptance", []),
                    "superseded_by_sha": receipts.get("merge_sha"),
                })
            if action == "RENAMED" and key == previous_key:
                errors.add(f"RENAMED_REQUIRES_NEW_ID:{rid}")
                continue
            if (action == "RENAMED" and key in result
                and result[key].get("status") == "CURRENT"):
                errors.add(f"RENAMED_DESTINATION_ALREADY_EXISTS:{rid}")
                continue
            result[previous_key] = {**found, "status": "SUPERSEDED",
                                    "superseded_by": key if action != "REMOVED" else None}
        if action != "REMOVED":
            if key in result and result[key].get("status") == "CURRENT" and action == "ADDED":
                errors.add(f"ADDED_REQUIREMENT_ALREADY_EXISTS:{rid}")
            else:
                result[key] = {"status": "CURRENT", "source_sha": receipts.get("merge_sha"),
                               "text": req.get("text"), "acceptance": req.get("acceptance", []),
                               **({"history": prior_history} if prior_history else {})}
        if action == "REMOVED" and key == previous_key:
            # previous requirement is marked superseded, never silently deleted.
            pass
    return {
        "status": "BLOCKED" if errors else "PREVIEW_REQUIRES_TRUSTED_REVIEW",
        "errors": sorted(errors),
        "proposed_canonical": result if not errors else None,
        "change_id": spec, "receipts": receipts,
        "snapshot_authenticity": "UNTRUSTED_INPUT_NEEDS_APP_LAB_GITHUB_REVIEW",
        "product_bible_written": False, "writes_performed": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--canonical", type=Path, required=True)
    p.add_argument("--receipts", type=Path, required=True)
    a = p.parse_args()
    try:
        doc = json.loads(a.manifest.read_text(encoding="utf-8"))
        current = json.loads(a.canonical.read_text(encoding="utf-8"))
        receipts = json.loads(a.receipts.read_text(encoding="utf-8"))
        report = reconcile(doc, current, receipts)
    except (OSError, UnicodeError, ValueError, TypeError) as e:
        report = {"status": "BLOCKED", "errors": [f"INPUT_ERROR:{type(e).__name__}"],
                  "writes_performed": False}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PREVIEW_REQUIRES_TRUSTED_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
