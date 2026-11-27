#!/usr/bin/env python3
"""Offline adversarial vectors for live GitHub Shadow Mode; no real API calls."""
import base64
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from openspec_shadow_mode import IncompleteSnapshot, assess, markdown, snapshot, paged

REPO = "riccardopinato/Android-Omni-Cleaner"
HEAD = "a" * 40


def pr(number, files, source=HEAD):
    return {"number": number, "head": {"sha": hex(number)[2:].rjust(40, "b")[-40:]},
            "base": {"sha": source, "ref": "main"}, "state": "open",
            "changed_files": len(files), "draft": True}


class FakeAPI:
    def __init__(self, pr_files=None, manifest=None):
        self.pr_files = pr_files if pr_files is not None else {
            77: ["app/src/main/Gallery.kt", "docs/new.md"],
            75: ["app/src/main/Gallery.kt", "app/src/main/Scan.kt"],
            74: ["docs/README.md"]}
        self.prs = [pr(n, files) for n, files in sorted(self.pr_files.items())]
        self.manifest = manifest
        self.head_reads = 0
        self.list_reads = 0
        self.token = "synthetic-token-never-exposed"
        self.mutate_head = self.mutate_pr_list = self.missing_file = False
        self.file_duplicate = self.detail_mismatch = False

    def get(self, path):
        if path == f"/repos/{REPO}":
            return {"full_name": REPO, "default_branch": "main"}
        if path == f"/repos/{REPO}/commits/main":
            self.head_reads += 1
            return {"sha": ("c" * 40 if self.mutate_head and self.head_reads > 1 else HEAD)}
        if "/pulls?state=open&per_page=100&page=" in path:
            page = int(path.rsplit("=", 1)[-1])
            if page == 1:
                self.list_reads += 1
            found = copy.deepcopy(self.prs[(page-1)*100:page*100])
            if self.mutate_pr_list and self.list_reads > 1 and page == 1 and found:
                found[0]["head"]["sha"] = "9" * 40
            return found
        if "/pulls/" in path and "/files?" in path:
            n = int(path.split("/pulls/")[1].split("/")[0])
            page = int(path.rsplit("=", 1)[-1])
            files = list(self.pr_files[n])
            if self.missing_file and n == 77:
                files = files[:1]
            if self.file_duplicate and n == 77:
                files = [files[0], files[0]]
            return [{"filename": name, "status": "modified"}
                    for name in files[(page-1)*100:page*100]]
        if "/pulls/" in path and "/files?" not in path:
            n = int(path.rsplit("/", 1)[-1])
            found = copy.deepcopy(next(x for x in self.prs if x["number"] == n))
            if self.detail_mismatch and n == 77:
                found["head"]["sha"] = "1" * 40
            return found
        if "/contents/" in path and self.manifest is not None:
            return {"encoding": "base64",
                    "content": base64.b64encode(json.dumps(self.manifest).encode()).decode()}
        raise AssertionError("Unexpected fake GET " + path)


class ShadowModeTests(unittest.TestCase):
    def test_complete_source_is_review_only(self):
        api = FakeAPI()
        result = assess(snapshot(api, REPO))
        self.assertEqual(result["status"], "REVIEW_NEEDED_NOT_CERTIFIED")
        self.assertEqual(result["pr_count"], 3)
        self.assertEqual(result["overlap_pair_count"], 1)
        self.assertEqual(result["overlap_pairs"][0]["prs"], [75, 77])
        self.assertEqual(result["unmapped_requirement_prs"], [74, 75, 77])
        self.assertFalse(result["side_effects"])
        self.assertFalse(result["semantic_absence_certified"])
        self.assertNotIn(api.token, markdown(result))
        self.assertEqual((api.head_reads, api.list_reads), (2, 2))

    def test_empty_pr_inventory_never_certifies_runtime(self):
        result = assess(snapshot(FakeAPI({}), REPO))
        self.assertEqual(result["status"], "EMPTY_PR_INVENTORY_NOT_CERTIFIED")
        self.assertFalse(result["runtime_certified"])

    def test_changed_files_incomplete_is_blocked(self):
        api = FakeAPI()
        api.missing_file = True
        with self.assertRaisesRegex(IncompleteSnapshot, "PR_FILES_INCOMPLETE"):
            snapshot(api, REPO)

    def test_duplicate_files_are_blocked(self):
        api = FakeAPI()
        api.file_duplicate = True
        with self.assertRaisesRegex(IncompleteSnapshot, "PR_FILE_DUPLICATE"):
            snapshot(api, REPO)

    def test_head_changed_during_collection_is_blocked(self):
        api = FakeAPI()
        api.mutate_head = True
        with self.assertRaisesRegex(IncompleteSnapshot, "DEFAULT_HEAD_CHANGED_DURING_SCAN"):
            snapshot(api, REPO)

    def test_open_pr_inventory_changed_is_blocked(self):
        api = FakeAPI()
        api.mutate_pr_list = True
        with self.assertRaisesRegex(IncompleteSnapshot, "PR_INVENTORY_CHANGED_DURING_SCAN"):
            snapshot(api, REPO)

    def test_pr_detail_changed_is_blocked(self):
        api = FakeAPI()
        api.detail_mismatch = True
        with self.assertRaisesRegex(IncompleteSnapshot, "PR_CHANGED_DURING_READ"):
            snapshot(api, REPO)

    def test_paginated_pr_inventory_not_truncated(self):
        api = FakeAPI({i: [f"lib/{i}.dart"] for i in range(1, 103)})
        result = assess(snapshot(api, REPO))
        self.assertEqual(result["pr_count"], 102)
        self.assertEqual(result["file_records_read"], 102)
        self.assertEqual(result["overlap_pairs"], [])

    def test_over_limit_inventory_fails_closed(self):
        with self.assertRaisesRegex(IncompleteSnapshot, "PAGINATION_TRUNCATED"):
            snapshot(FakeAPI({i: [f"lib/{i}.dart"] for i in range(1, 302)}), REPO)

    def test_target_focus_retains_global_overlaps_without_false_zero(self):
        result = assess(snapshot(FakeAPI(), REPO), 74)
        self.assertEqual(result["pr_count"], 3)
        self.assertEqual(result["overlap_pair_count"], 1)
        self.assertEqual(result["overlap_pairs"][0]["prs"], [75, 77])
        self.assertEqual(result["focused_overlap_pair_count"], 0)
        self.assertEqual(result["focused_overlap_pairs"], [])
        self.assertIn("repository-wide findings remain visible", markdown(result))
        self.assertIn("PR #75 / #77", markdown(result))
        self.assertEqual(result["unmapped_requirement_prs"], [74, 75, 77])

    def test_target_focus_shows_global_and_targeted_pair_counts(self):
        result = assess(snapshot(FakeAPI(), REPO), 75)
        self.assertEqual(result["overlap_pair_count"], 1)
        self.assertEqual(result["focused_overlap_pair_count"], 1)
        self.assertEqual(result["focused_overlap_pairs"][0]["prs"], [75, 77])
        self.assertIn("Focused PR #75: **1**", markdown(result))

    def test_target_pr_unknown_fails_closed(self):
        with self.assertRaisesRegex(IncompleteSnapshot, "TARGET_PR_NOT_IN_OPEN_INVENTORY"):
            assess(snapshot(FakeAPI(), REPO), 999)

    def test_old_base_sha_is_not_called_a_semantic_conflict(self):
        api = FakeAPI()
        api.prs[0]["base"]["sha"] = "1" * 40
        result = assess(snapshot(api, REPO))
        self.assertEqual(result["base_sha_differs_from_current_default"], [74])
        self.assertFalse(result["semantic_absence_certified"])

    def test_same_declared_previous_requirement_only_requires_review(self):
        manifest = {"spec_id": "FSL-20261127-DELTAPILOT",
                    "target": {"repository": REPO},
                    "requirements": [{"id": "FR-001", "delta": {
                        "operation": "MODIFIED", "previous": {
                            "spec_id": "FSL-20261127-BASEPILOT",
                            "requirement_id": "FR-002", "source_sha": "f" * 40}}}]}
        api = FakeAPI({77: ["docs/spec_lite/gallery/manifest.json"],
                       75: ["docs/spec_lite/cleaning/manifest.json"]}, manifest)
        result = assess(snapshot(api, REPO))
        self.assertEqual(result["competing_requirement_deltas"][0]["prs"], [75, 77])
        self.assertFalse(result["competing_requirement_deltas"][0]["verified_product_conflict"])

    def test_github_merge_conflict_state_is_factual_not_product_verdict(self):
        api = FakeAPI()
        api.prs[0]["mergeable"] = False
        api.prs[0]["mergeable_state"] = "dirty"
        result = assess(snapshot(api, REPO))
        self.assertEqual(result["github_merge_conflict_prs"], [74])
        self.assertFalse(result["semantic_absence_certified"])

    def test_complete_file_scope_containment_is_not_claimed_code_equivalence(self):
        api = FakeAPI({75: ["lib/gallery.dart"], 77: ["lib/gallery.dart", "lib/other.dart"]})
        result = assess(snapshot(api, REPO))
        self.assertEqual(result["overlap_pairs"][0]["full_file_scope_containment"], [75])
        self.assertIn("not code equivalence", markdown(result))

    def test_bad_declared_prior_never_clears(self):
        manifest = {"spec_id": "FSL-20261127-X", "target": {"repository": REPO},
                    "requirements": [{"id": "FR-001", "delta": {
                        "operation": "MODIFIED", "previous": None}}]}
        api = FakeAPI({77: ["docs/spec_lite/gallery/manifest.json"]}, manifest)
        with self.assertRaisesRegex(IncompleteSnapshot, "MANIFEST_PRIOR_INCOMPLETE"):
            snapshot(api, REPO)

    def test_unmapped_pr_does_not_infer_no_conflict(self):
        result = assess(snapshot(FakeAPI({75: ["lib/gallery.dart"]}), REPO))
        self.assertEqual(result["unmapped_requirement_prs"], [75])
        self.assertEqual(result["competing_requirement_deltas"], [])

    def test_wrong_repository_rejected_before_io(self):
        with self.assertRaisesRegex(IncompleteSnapshot, "INVALID_REPOSITORY"):
            snapshot(FakeAPI(), "https://evil.example/x")

    def test_paged_get_rejects_nonlist(self):
        with self.assertRaisesRegex(IncompleteSnapshot, "PAGINATION_RESPONSE_INVALID"):
            paged(lambda _: {"untrusted": True}, "/repos/a/b/pulls?state=open",
                  max_records=300)


if __name__ == "__main__":
    unittest.main()
