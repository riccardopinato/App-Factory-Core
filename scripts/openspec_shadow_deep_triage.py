#!/usr/bin/env python3
"""Opt-in OpenSpec Shadow deep triage of explicitly selected live PR pairs.

Uses the existing stable/complete GitHub PR snapshot. Adds only pinned GitHub
GET compare/tree reads for <=4 selected overlapping pairs. A source comparison
is NEVER a semantic product verdict, merge permission, QA or certification.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

from openspec_shadow_mode import (
    GitHubAPI, IncompleteSnapshot, _sha, assess, markdown, require, snapshot,
)

MAX_DEEP_PAIRS = 4
MAX_TREE_RECORDS = 6000
_PAIR = re.compile(r"[1-9][0-9]{0,7}:[1-9][0-9]{0,7}")


def parse_pairs(raw: str) -> list[tuple[int, int]]:
    require(isinstance(raw, str) and 0 < len(raw) <= 100,
            "DEEP_PAIRS_SELECTION_REQUIRED_OR_TOO_LARGE")
    entries = raw.split(",")
    require(1 <= len(entries) <= MAX_DEEP_PAIRS, "DEEP_PAIR_BUDGET_EXCEEDED")
    found: list[tuple[int, int]] = []
    for item in entries:
        require(bool(_PAIR.fullmatch(item)), "DEEP_PAIR_FORMAT_INVALID")
        a, b = map(int, item.split(":"))
        require(a != b, "DEEP_PAIR_SELF_COMPARE_FORBIDDEN")
        pair = tuple(sorted((a, b)))
        require(pair not in found, "DEEP_PAIR_DUPLICATE")
        found.append(pair)
    return found


def _tree_blobs(api: Any, repo: str, commit_sha: str) -> dict[str, str]:
    require(_sha(commit_sha), "DEEP_PINNED_COMMIT_REQUIRED")
    obj = api.get(f"/repos/{repo}/git/trees/{commit_sha}?recursive=1")
    require(isinstance(obj, dict)
            and obj.get("truncated") is False
            and isinstance(obj.get("tree"), list),
            "DEEP_GIT_TREE_INCOMPLETE")
    entries = obj["tree"]
    require(len(entries) <= MAX_TREE_RECORDS, "DEEP_TREE_RECORD_BUDGET_EXCEEDED")
    found: dict[str, str] = {}
    seen: set[str] = set()
    for entry in entries:
        require(isinstance(entry, dict)
                and isinstance(entry.get("path"), str)
                and bool(entry["path"])
                and not entry["path"].startswith("/")
                and ".." not in entry["path"].split("/")
                and entry["path"] not in seen,
                "DEEP_GIT_TREE_ENTRY_INVALID")
        seen.add(entry["path"])
        if entry.get("type") == "blob":
            require(_sha(entry.get("sha")), "DEEP_GIT_BLOB_SHA_INVALID")
            found[entry["path"]] = entry["sha"]
    return found


def _compare(api: Any, repo: str, sha_a: str, sha_b: str) -> dict[str, Any]:
    require(_sha(sha_a) and _sha(sha_b), "DEEP_COMPARE_SHA_INVALID")
    if sha_a == sha_b:
        return {"relation": "IDENTICAL_HEAD_SHA", "status": "identical",
                "ahead_by": 0, "behind_by": 0, "head_checked": True}
    obj = api.get(f"/repos/{repo}/compare/{sha_a}...{sha_b}")
    require(isinstance(obj, dict)
            and isinstance(obj.get("base_commit"), dict)
            and obj["base_commit"].get("sha") == sha_a,
            "DEEP_COMPARE_BASE_IDENTITY_MISMATCH")
    status = obj.get("status")
    ahead, behind = obj.get("ahead_by"), obj.get("behind_by")
    require(status in ("ahead", "behind", "diverged")
            and type(ahead) is int and type(behind) is int
            and ahead >= 0 and behind >= 0, "DEEP_COMPARE_RESPONSE_INVALID")
    if status == "ahead":
        require(ahead > 0 and behind == 0, "DEEP_COMPARE_DIRECTION_INCONSISTENT")
        relation = "A_ANCESTOR_OF_B"
    elif status == "behind":
        require(ahead == 0 and behind > 0, "DEEP_COMPARE_DIRECTION_INCONSISTENT")
        relation = "B_ANCESTOR_OF_A"
    else:
        require(ahead > 0 and behind > 0, "DEEP_COMPARE_DIRECTION_INCONSISTENT")
        relation = "DIVERGED_HISTORY"
    # GitHub compare response has no head_commit field. On ahead/diverged,
    # the last listed commit must be the exact requested target SHA. For
    # behind, the commits list can legitimately be empty: explicitly GET
    # the pinned target commit to assert its identity.
    if ahead:
        commits = obj.get("commits")
        require(isinstance(commits, list) and bool(commits)
                and isinstance(commits[-1], dict)
                and commits[-1].get("sha") == sha_b,
                "DEEP_COMPARE_TARGET_NOT_VERIFIED")
    else:
        target = api.get(f"/repos/{repo}/commits/{sha_b}")
        require(isinstance(target, dict) and target.get("sha") == sha_b,
                "DEEP_COMPARE_TARGET_NOT_VERIFIED")
    return {"relation": relation, "status": status, "ahead_by": ahead,
            "behind_by": behind, "head_checked": True}


def deep_review(api: Any, snap: dict[str, Any], report: dict[str, Any],
                pairs: list[tuple[int, int]]) -> dict[str, Any]:
    """Fail closed if any selected pair or immutable evidence cannot be verified."""
    repo = snap["repository"]
    prs = {p["number"]: p for p in snap["prs"]}
    collisions = {tuple(p["prs"]): p for p in report["overlap_pairs"]}
    cache: dict[str, dict[str, str]] = {}
    details = []
    for pair in pairs:
        require(pair[0] in prs and pair[1] in prs, "DEEP_PAIR_PR_NOT_OPEN")
        require(pair in collisions, "DEEP_PAIR_NO_SHARED_CHANGED_FILES")
        a, b = (prs[n] for n in pair)
        exact_a, exact_b = a["head_sha"], b["head_sha"]
        relation = _compare(api, repo, exact_a, exact_b)
        for sha in (exact_a, exact_b):
            if sha not in cache:
                cache[sha] = _tree_blobs(api, repo, sha)
        blobs_a, blobs_b = cache[exact_a], cache[exact_b]
        common = sorted(set(a["changed_paths"]) & set(b["changed_paths"]))
        require(bool(common) and len(common) == collisions[pair]["count"],
                "DEEP_CHANGED_PATH_INVENTORY_MISMATCH")
        identical = [p for p in common if blobs_a.get(p) and blobs_a[p] == blobs_b.get(p)]
        different = [p for p in common if blobs_a.get(p) and blobs_b.get(p)
                     and blobs_a[p] != blobs_b[p]]
        missing = [p for p in common if p not in blobs_a or p not in blobs_b]
        require(len(identical) + len(different) + len(missing) == len(common),
                "DEEP_BLOB_ACCOUNTING_MISMATCH")
        details.append({
            "prs": list(pair), "sha_a": exact_a, "sha_b": exact_b,
            "history": relation,
            "shared_changed_paths": len(common),
            "byte_identical_blob_count": len(identical),
            "different_blob_count": len(different),
            "missing_or_nonblob_count": len(missing),
            "different_file_sample": different[:15],
            "missing_file_sample": missing[:15],
            "interpretation": "BYTE_IDENTITY_AND_COMMIT_ANCESTRY_ONLY_NOT_FUNCTIONAL_EQUIVALENCE",
            "source": "GITHUB_PINNED_COMPARE_AND_UNTRUNCATED_GIT_TREES",
        })
    return {
        "mode": "SELECTED_PAIR_DEEP_TRIAGE",
        "status": "REVIEW_ONLY_NOT_CERTIFIED",
        "selected_pairs": len(details),
        "unreviewed_overlapping_pairs": len(report["overlap_pairs"]) - len(details),
        "pairs": details,
        "complete_repository_semantic_coverage": False,
        "product_conflict_certified": False,
        "device_or_runtime_certified": False,
        "writes_performed": False,
    }


def deep_markdown(report: dict[str, Any]) -> str:
    deep = report["deep_triage"]
    out = ["", "### Optional pinned commit + blob triage",
           f"- Selected pairs: {deep['selected_pairs']}; "
           f"other overlapping pairs not deeply examined: {deep['unreviewed_overlapping_pairs']}"]
    for p in deep["pairs"]:
        out.append(f"- PR #{p['prs'][0]} / #{p['prs'][1]}: "
                   f"{p['history']['relation']}; shared paths {p['shared_changed_paths']}, "
                   f"byte-identical {p['byte_identical_blob_count']}, "
                   f"different {p['different_blob_count']}, "
                   f"missing/nonblob {p['missing_or_nonblob_count']}")
        if p["different_file_sample"]:
            out.append("  - Different-file examples: " + ", ".join(
                f"`{s}`" for s in p["different_file_sample"][:5]))
    out += ["- The relationship and blob hashes do not authorize any merge, "
            "certify functional equivalence or replace manual reconciliation.", ""]
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", required=True)
    p.add_argument("--target-pr", type=int, default=0)
    p.add_argument("--deep-pairs", required=True,
                   help="1–4 exact open PR pair numbers, e.g. 75:77,39:77")
    p.add_argument("--json-out", type=Path)
    p.add_argument("--md-out", type=Path)
    args = p.parse_args()
    api = GitHubAPI(os.environ.get("GITHUB_TOKEN"))
    started = time.monotonic()
    try:
        require(args.target_pr >= 0, "INVALID_TARGET_PR")
        selected = parse_pairs(args.deep_pairs)
        snap = snapshot(api, args.repo)
        report = assess(snap, args.target_pr)
        report["deep_triage"] = deep_review(api, snap, report, selected)
        status = 0
    except IncompleteSnapshot as exc:
        report = {
            "record_type": "OPENSPEC_SHADOW_GITHUB_REVIEW",
            "status": "INCOMPLETE_NO_CLEARANCE",
            "error_code": str(exc),
            "repository": args.repo,
            "semantic_absence_certified": False,
            "deep_triage_completed": False,
            "side_effects": False,
        }
        status = 2
    report["github_api_requests"] = api.request_count
    report["github_api_response_bytes"] = api.payload_bytes
    report["wall_seconds"] = round(time.monotonic() - started, 3)
    report["token_savings"] = "NOT_MEASURED"
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
    if status == 0:
        body = markdown(report) + deep_markdown(report)
        body += (f"\nDeep scanner cost observation: {api.request_count} GitHub REST GET(s), "
                 f"{api.payload_bytes} response bytes, {report['wall_seconds']} wall seconds. "
                 "No proven time/token savings.\n")
    else:
        body = ("## OpenSpec Shadow Deep Mode — INCOMPLETE, not a PASS\n\n"
                f"Evidence error: `{report['error_code']}`.\n")
    if args.md_out:
        args.md_out.write_text(body, encoding="utf-8")
    print(body)
    return status


if __name__ == "__main__":
    sys.exit(main())
