#!/usr/bin/env python3
"""OpenSpec Shadow Mode: bounded live GitHub PR snapshot and read-only review hints.

No merges, comments, approvals, code changes, data download outside GitHub API,
new verification authority or success claims. Input PR files/manifests are untrusted.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-f]{40}$")
SPEC_MANIFEST = re.compile(r"(?:^|/)spec_lite/[^/]+/manifest\.json$")
MAX_PRS = 300
MAX_FILES = 3000
MAX_BYTES = 10 * 1024 * 1024


class IncompleteSnapshot(RuntimeError):
    """No complete and stable read-only GitHub evidence can be asserted."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise IncompleteSnapshot(code)


def parse_repo(value: str) -> str:
    require(isinstance(value, str) and bool(REPO.fullmatch(value)), "INVALID_REPOSITORY")
    require(all(x not in (".", "..") for x in value.split("/")), "INVALID_REPOSITORY")
    return value


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise IncompleteSnapshot("GITHUB_API_REDIRECT_DENIED")


class GitHubAPI:
    """Read-only GitHub REST JSON; never follow redirects that could leak credentials."""

    def __init__(self, token: str | None = None):
        self.token = token or ""
        self.opener = urllib.request.build_opener(_NoRedirect)

    def get(self, path: str) -> Any:
        require(path.startswith("/repos/") and not path.startswith("//")
                and "\n" not in path, "INVALID_GITHUB_PATH")
        headers = {"Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2022-11-28",
                   "User-Agent": "AppFactory-OpenSpec-Shadow"}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        req = urllib.request.Request("https://api.github.com" + path, headers=headers,
                                     method="GET")
        try:
            with self.opener.open(req, timeout=20) as response:
                raw = response.read(MAX_BYTES + 1)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
            raise IncompleteSnapshot("GITHUB_API_REQUEST_FAILED") from None
        require(len(raw) <= MAX_BYTES, "GITHUB_RESPONSE_TOO_LARGE")
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeError, ValueError):
            raise IncompleteSnapshot("GITHUB_JSON_INVALID") from None


def paged(get: Callable[[str], Any], prefix: str, *, max_records: int) -> list:
    """Page until a short page; fail closed at 100-per-page and bounded hard caps."""
    out: list[Any] = []
    for page in range(1, max_records // 100 + 2):
        chunk = get(prefix + ("&" if "?" in prefix else "?") + f"per_page=100&page={page}")
        require(isinstance(chunk, list), "PAGINATION_RESPONSE_INVALID")
        require(len(chunk) <= 100, "PAGINATION_PAGE_OVERSIZED")
        require(len(out) + len(chunk) <= max_records, "PAGINATION_TRUNCATED")
        out.extend(chunk)
        if len(chunk) < 100:
            return out
    raise IncompleteSnapshot("PAGINATION_UNTERMINATED")


def _sha(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA.fullmatch(value))


def _identity(pr: dict) -> tuple:
    try:
        return (pr["number"], pr["head"]["sha"], pr["base"]["sha"], pr["base"]["ref"])
    except (KeyError, TypeError):
        raise IncompleteSnapshot("PR_IDENTITY_MISSING") from None


def _list_prs(api: Any, repo: str) -> list[dict]:
    prs = paged(api.get, f"/repos/{repo}/pulls?state=open", max_records=MAX_PRS)
    require(all(isinstance(x, dict) for x in prs), "PR_RECORD_INVALID")
    ids = [_identity(x) for x in prs]
    require(all(type(x[0]) is int and x[0] > 0 and _sha(x[1])
                and _sha(x[2]) and isinstance(x[3], str) for x in ids),
            "PR_IDENTITY_INVALID")
    require(len({x[0] for x in ids}) == len(ids), "DUPLICATE_PR_IDENTITY")
    return prs


def _read_manifest(api: Any, repo: str, pr_sha: str, filename: str) -> dict:
    encoded = urllib.parse.quote(filename, safe="/")
    response = api.get(f"/repos/{repo}/contents/{encoded}?ref={pr_sha}")
    require(isinstance(response, dict) and response.get("encoding") == "base64"
            and isinstance(response.get("content"), str), "MANIFEST_NOT_PINNED_READABLE")
    try:
        raw = base64.b64decode(response["content"], validate=False)
        require(len(raw) <= 512_000, "MANIFEST_TOO_LARGE")
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError, TypeError):
        raise IncompleteSnapshot("MANIFEST_JSON_INVALID") from None
    require(isinstance(data, dict) and isinstance(data.get("spec_id"), str)
            and isinstance(data.get("requirements"), list)
            and isinstance(data.get("target"), dict)
            and data["target"].get("repository") == repo, "MANIFEST_IDENTITY_INVALID")
    require(0 < len(data["requirements"]) <= 200, "MANIFEST_REQUIREMENTS_INVALID")
    return data


def _requirement_keys(doc: dict) -> list[tuple[str, str, str, str]]:
    """Self-declared proposal only; never accept APPROVED or verified claims."""
    keys = []
    for req in doc["requirements"]:
        require(isinstance(req, dict)
                and isinstance(req.get("id"), str)
                and re.fullmatch(r"FR-[0-9]{3}", req["id"]), "MANIFEST_REQUIREMENT_ID_INVALID")
        delta = req.get("delta")
        if delta is not None:
            require(isinstance(delta, dict), "MANIFEST_DELTA_INVALID")
        delta = delta or {}
        operation = delta.get("operation", "UNSPECIFIED")
        require(operation in ("UNSPECIFIED", "ADDED", "MODIFIED", "REMOVED", "RENAMED"),
                "MANIFEST_DELTA_INVALID")
        previous = delta.get("previous")
        if operation in ("MODIFIED", "REMOVED", "RENAMED"):
            require(isinstance(previous, dict)
                    and isinstance(previous.get("spec_id"), str)
                    and isinstance(previous.get("requirement_id"), str)
                    and _sha(previous.get("source_sha")), "MANIFEST_PRIOR_INCOMPLETE")
            key = (previous["spec_id"], previous["requirement_id"],
                   previous["source_sha"], operation)
        else:
            key = (doc["spec_id"], req["id"], "ADDED_OR_UNSPECIFIED", operation)
        keys.append(key)
    require(len({x[:3] for x in keys}) == len(keys), "MANIFEST_DUPLICATE_REQUIREMENT")
    return keys


def snapshot(api: Any, repository: str) -> dict[str, Any]:
    repo = parse_repo(repository)
    info = api.get(f"/repos/{repo}")
    require(isinstance(info, dict)
            and str(info.get("full_name", "")).casefold() == repo.casefold(),
            "GITHUB_REPOSITORY_IDENTITY_MISMATCH")
    branch = info.get("default_branch")
    require(isinstance(branch, str) and bool(branch)
            and re.fullmatch(r"[A-Za-z0-9_./-]{1,120}", branch)
            and ".." not in branch, "DEFAULT_BRANCH_INVALID")
    basepath = f"/repos/{repo}"
    def read_head() -> str:
        value = api.get(basepath + "/commits/" + urllib.parse.quote(branch, safe=""))
        sha = value.get("sha") if isinstance(value, dict) else None
        require(_sha(sha), "HEAD_SHA_UNVERIFIED")
        return sha

    head_before = read_head()
    before = _list_prs(api, repo)
    prs = []
    total_files = 0
    for p in before:
        number = p["number"]
        detail = api.get(basepath + f"/pulls/{number}")
        require(isinstance(detail, dict) and _identity(detail) == _identity(p)
                and detail.get("state") == "open", "PR_CHANGED_DURING_READ")
        expected = detail.get("changed_files")
        require(type(expected) is int and 0 <= expected < MAX_FILES,
                "PR_FILE_COUNT_UNVERIFIABLE_OR_CAPPED")
        files = paged(api.get, basepath + f"/pulls/{number}/files",
                      max_records=MAX_FILES)
        require(len(files) == expected, "PR_FILES_INCOMPLETE")
        paths = []
        manifest_paths = []
        for f in files:
            require(isinstance(f, dict) and isinstance(f.get("filename"), str)
                    and f["filename"] and not f["filename"].startswith("/")
                    and ".." not in f["filename"].split("/"), "PR_FILE_PATH_INVALID")
            name = f["filename"]
            paths.append(name)
            if SPEC_MANIFEST.search(name) and f.get("status") != "removed":
                manifest_paths.append(name)
        require(len(set(paths)) == len(paths), "PR_FILE_DUPLICATE")
        requirements = []
        for filename in manifest_paths:
            doc = _read_manifest(api, repo, p["head"]["sha"], filename)
            requirements += _requirement_keys(doc)
        prs.append({
            "number": number, "head_sha": p["head"]["sha"],
            "base_sha": p["base"]["sha"], "base_ref": p["base"]["ref"],
            "draft": bool(detail.get("draft", False)),
            "mergeable": detail.get("mergeable") if type(detail.get("mergeable")) is bool else None,
            "mergeable_state": detail.get("mergeable_state", "unknown"),
            "changed_files": expected, "changed_paths": sorted(paths),
            "requirement_keys": requirements,
            "requirement_coverage": "DECLARED_UNTRUSTED" if manifest_paths else "UNMAPPED",
            "manifest_paths": manifest_paths,
        })
        total_files += len(files)
    head_after = read_head()
    after = _list_prs(api, repo)
    require(head_before == head_after, "DEFAULT_HEAD_CHANGED_DURING_SCAN")
    require(sorted(map(_identity, before)) == sorted(map(_identity, after)),
            "PR_INVENTORY_CHANGED_DURING_SCAN")
    return {
        "repository": repo, "default_branch": branch, "head_sha": head_after,
        "pr_count": len(prs), "file_records_read": total_files, "prs": prs,
        "api_pagination_complete": True, "head_rechecked": True,
        "pr_inventory_rechecked": True,
        "provider": "GITHUB_REST_READ_ONLY",
        "token_present": bool(getattr(api, "token", "")),
        "side_effects": False,
    }


def assess(snap: dict[str, Any], target_pr: int = 0) -> dict[str, Any]:
    prs = snap["prs"]
    ids = {x["number"] for x in prs}
    require(target_pr == 0 or target_pr in ids, "TARGET_PR_NOT_IN_OPEN_INVENTORY")
    pairs = []
    by_file = defaultdict(list)
    by_req = defaultdict(list)
    for p in prs:
        for path in p["changed_paths"]:
            by_file[path].append(p["number"])
        for spec, rid, oldsha, operation in p["requirement_keys"]:
            by_req[(spec, rid, oldsha)].append((p["number"], operation))
    file_pair_paths = defaultdict(list)
    for path, numbers in by_file.items():
        for i, a in enumerate(numbers):
            for b in numbers[i+1:]:
                file_pair_paths[tuple(sorted((a, b)))].append(path)
    for (a, b), paths in sorted(file_pair_paths.items()):
        pa = next(p for p in prs if p["number"] == a)
        pb = next(p for p in prs if p["number"] == b)
        pairs.append({
            "prs": [a, b], "kind": "FILE_OVERLAP_REVIEW", "count": len(paths),
            "sample_paths": sorted(paths)[:12],
            "different_base_branch": pa["base_ref"] != pb["base_ref"],
            "meaning": "COMMON_CHANGED_PATHS_NOT_PROVEN_SEMANTIC_CONFLICT",
            "full_file_scope_containment": sorted([
                x["number"] for x, y in ((pa, pb), (pb, pa))
                if set(x["changed_paths"]).issubset(set(y["changed_paths"]))
            ]),
        })
    competing = []
    for (spec, req, oldsha), edits in by_req.items():
        diff_prs = sorted({x[0] for x in edits})
        if len(diff_prs) > 1:
            competing.append({
                "prs": diff_prs, "spec_id": spec, "requirement_id": req,
                "prior_source_sha": oldsha,
                "operations": sorted({x[1] for x in edits}),
                "kind": "COMPETING_SELF_DECLARED_REQUIREMENT_DELTAS_REVIEW",
                "verified_product_conflict": False,
            })
    unmapped = sorted(p["number"] for p in prs if p["requirement_coverage"] == "UNMAPPED")
    base_drift = sorted(p["number"] for p in prs if
                        p["base_ref"] == snap["default_branch"]
                        and p["base_sha"] != snap["head_sha"])
    github_merge_conflicts = sorted(p["number"] for p in prs
                                    if p["mergeable"] is False
                                    or p["mergeable_state"] == "dirty")
    mergeability_unverified = sorted(p["number"] for p in prs
                                    if p["mergeable"] is None
                                    and p["mergeable_state"] != "dirty")
    return {
        "schema_version": 1, "record_type": "OPENSPEC_SHADOW_GITHUB_REVIEW",
        "status": "REVIEW_NEEDED_NOT_CERTIFIED" if prs else "EMPTY_PR_INVENTORY_NOT_CERTIFIED",
        "repository": snap["repository"], "head_sha": snap["head_sha"],
        "default_branch": snap["default_branch"], "target_pr": target_pr,
        "pr_count": len(prs), "file_records_read": snap["file_records_read"],
        "overlap_pairs": pairs, "overlap_pair_count": len(pairs),
        "focused_overlap_pairs": [p for p in pairs if target_pr and target_pr in p["prs"]],
        "focused_overlap_pair_count": sum(1 for p in pairs if target_pr and target_pr in p["prs"]),
        "competing_requirement_deltas": competing,
        "focused_competing_requirement_deltas": [
            item for item in competing if target_pr and target_pr in item["prs"]],
        "unmapped_requirement_prs": unmapped,
        "base_sha_differs_from_current_default": base_drift,
        "github_merge_conflict_prs": github_merge_conflicts,
        "github_mergeability_unknown_prs": mergeability_unverified,
        "snapshot_checks": {
            "paginated": snap["api_pagination_complete"],
            "head_stable": snap["head_rechecked"],
            "pr_list_stable": snap["pr_inventory_rechecked"],
        },
        "source": snap["provider"],
        "auth_mode": "WORKFLOW_TOKEN" if snap["token_present"] else "PUBLIC_READ_ONLY",
        "semantic_absence_certified": False, "runtime_certified": False,
        "side_effects": False, "pr_comments_created": False,
    }


def markdown(report: dict[str, Any]) -> str:
    out = ["## OpenSpec Shadow Mode — read-only PR review",
           f"- Repository: \`{report['repository']}\` at \`{report['head_sha']}\`",
           f"- Status: **{report['status']}** — never a merge/QA/physical PASS",
           f"- Open PRs: **{report['pr_count']}**; complete changed-path records: "
           f"**{report['file_records_read']}**; overlapping pairs: **{report['overlap_pair_count']}**",
           *( [f"- Focused PR #{report['target_pr']}: **{report['focused_overlap_pair_count']}** "
                "overlap pair(s); repository-wide findings remain visible"] if report["target_pr"] else [] ),
           f"- Requirements without structured mapping: **{len(report['unmapped_requirement_prs'])}** "
           "(their absence of conflicts cannot be certified)",
           f"- Default-base SHA differs from observed HEAD in "
           f"**{len(report['base_sha_differs_from_current_default'])}** PR(s) "
           "(informational; not proof of stale implementation)",
           f"- GitHub currently reports **{len(report['github_merge_conflict_prs'])}** "
           "PR(s) with merge conflict state; no product semantic verdict",
           f"- Mergeability unavailable/unknown for "
           f"**{len(report['github_mergeability_unknown_prs'])}** PR(s)"]
    ordered_pairs = sorted(report["overlap_pairs"],
                           key=lambda x: (0 if report["target_pr"] in x["prs"] else 1,
                                          -x["count"], x["prs"]))
    for item in ordered_pairs[:20]:
        out.append(f"- PR #{item['prs'][0]} / #{item['prs'][1]}: "
                   f"{item['count']} shared file(s); e.g. "
                   + ", ".join(item["sample_paths"][:3])
                   + (f"; complete file-path containment for PR(s): "
                      f"{item['full_file_scope_containment']} (not code equivalence)"
                      if item["full_file_scope_containment"] else ""))
    for item in report["competing_requirement_deltas"][:10]:
        out.append("- Requirement change proposals " + "/".join("#" + str(x) for x in item["prs"]) +
                   f": \`{item['spec_id']}:{item['requirement_id']}\` — untrusted proposal, human review")
    if len(report["overlap_pairs"]) > 20:
        out.append(f"- Additional overlap pairs omitted from summary: {len(report['overlap_pairs'])-20}; inspect JSON")
    out += ["", "No automatic merge, PR comment, product decision, AppLab verification or device claim."]
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", required=True)
    p.add_argument("--target-pr", type=int, default=0)
    p.add_argument("--json-out", type=Path)
    p.add_argument("--md-out", type=Path)
    args = p.parse_args()
    try:
        require(args.target_pr >= 0, "INVALID_TARGET_PR")
        snap = snapshot(GitHubAPI(os.environ.get("GITHUB_TOKEN")), args.repo)
        report = assess(snap, args.target_pr)
        status = 0
    except IncompleteSnapshot as exc:
        report = {
            "record_type": "OPENSPEC_SHADOW_GITHUB_REVIEW",
            "status": "INCOMPLETE_NO_CLEARANCE", "error_code": str(exc),
            "repository": args.repo, "semantic_absence_certified": False,
            "side_effects": False,
        }
        status = 2
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if status == 0:
        body = markdown(report)
    else:
        body = f"## OpenSpec Shadow Mode — INCOMPLETE, not a PASS\n\nEvidence error: \`{report['error_code']}\`.\n"
    if args.md_out:
        args.md_out.write_text(body, encoding="utf-8")
    print(body)
    return status


if __name__ == "__main__":
    sys.exit(main())
