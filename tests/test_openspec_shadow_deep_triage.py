#!/usr/bin/env python3
"""Offline adversarial tests of pinned optional Shadow Mode deep triage."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from openspec_shadow_mode import IncompleteSnapshot  # noqa: E402
from openspec_shadow_deep_triage import (  # noqa: E402
    MAX_DEEP_PAIRS, _compare, _tree_blobs, deep_review, deep_markdown, parse_pairs,
)

REPO = "riccardopinato/Android-Omni-Cleaner"
A, B, C = "a" * 40, "b" * 40, "c" * 40
H1, H2, H3, H4 = "1" * 40, "2" * 40, "3" * 40, "4" * 40


def snap_and_report():
    snap = {
        "repository": REPO,
        "prs": [
            {"number": 39, "head_sha": C, "changed_paths": ["lib/main.kt"]},
            {"number": 75, "head_sha": A, "changed_paths": ["lib/main.kt", "lib/same.kt"]},
            {"number": 77, "head_sha": B, "changed_paths": [
                "lib/main.kt", "lib/same.kt", "lib/new.kt",
            ]},
        ],
    }
    report = {"overlap_pairs": [
        {"prs": [39, 75], "count": 1},
        {"prs": [39, 77], "count": 1},
        {"prs": [75, 77], "count": 2},
    ]}
    return snap, report


def tree(paths):
    return {"truncated": False, "tree": [
        {"type": "blob", "path": name, "sha": sha} for name, sha in paths.items()
    ]}


class FakeDeepAPI:
    def __init__(self):
        self.payload = {
            f"/repos/{REPO}/git/trees/{A}?recursive=1":
                tree({"lib/main.kt": H1, "lib/same.kt": H3}),
            f"/repos/{REPO}/git/trees/{B}?recursive=1":
                tree({"lib/main.kt": H2, "lib/same.kt": H3, "lib/new.kt": H4}),
            f"/repos/{REPO}/git/trees/{C}?recursive=1":
                tree({"lib/main.kt": H1}),
            f"/repos/{REPO}/compare/{A}...{B}": {
                "status": "ahead", "ahead_by": 4, "behind_by": 0,
                "base_commit": {"sha": A}, "commits": [{"sha": B}],
            },
            f"/repos/{REPO}/compare/{C}...{B}": {
                "status": "diverged", "ahead_by": 6, "behind_by": 2,
                "base_commit": {"sha": C}, "commits": [{"sha": B}],
            },
            f"/repos/{REPO}/compare/{A}...{C}": {
                "status": "behind", "ahead_by": 0, "behind_by": 1,
                "base_commit": {"sha": A}, "commits": [],
            },
            f"/repos/{REPO}/commits/{C}": {"sha": C},
        }
        self.calls = []

    def get(self, path):
        self.calls.append(path)
        if path not in self.payload:
            raise AssertionError("Unexpected GitHub GET " + path)
        return copy.deepcopy(self.payload[path])


class DeepTriageTests(unittest.TestCase):
    def assertBlocked(self, callable_, expected):
        with self.assertRaisesRegex(IncompleteSnapshot, expected):
            callable_()

    def test_strict_opt_in_two_pairs_and_order_canonicalization(self):
        self.assertEqual(parse_pairs("77:75,39:77"), [(75, 77), (39, 77)])

    def test_invalid_or_unbounded_pair_selection_fails_closed(self):
        for raw in ("", "75:77,77:75", "75:75", "0:77", "75:-77",
                    "75:77;cat", "1:2,2:3,3:4,4:5,5:6",
                    "1:2, 2:3", "1000000000:77"):
            with self.subTest(raw=raw):
                self.assertBlocked(lambda: parse_pairs(raw), "DEEP_PAIR")

    def test_maximum_four_pairs(self):
        self.assertEqual(len(parse_pairs("1:2,2:3,3:4,4:5")), MAX_DEEP_PAIRS)

    def test_deep_ancestry_and_blob_differences_are_evidence_not_pass(self):
        api = FakeDeepAPI()
        snap, base = snap_and_report()
        result = deep_review(api, snap, base, parse_pairs("75:77,39:77"))
        self.assertEqual(result["status"], "REVIEW_ONLY_NOT_CERTIFIED")
        self.assertEqual(result["selected_pairs"], 2)
        self.assertEqual(result["unreviewed_overlapping_pairs"], 1)
        first, second = result["pairs"]
        self.assertEqual(first["history"]["relation"], "A_ANCESTOR_OF_B")
        self.assertEqual((first["shared_changed_paths"], first["byte_identical_blob_count"],
                          first["different_blob_count"], first["missing_or_nonblob_count"]),
                         (2, 1, 1, 0))
        self.assertEqual(first["different_file_sample"], ["lib/main.kt"])
        self.assertEqual(second["history"]["relation"], "DIVERGED_HISTORY")
        self.assertEqual(second["byte_identical_blob_count"], 0)
        self.assertEqual(second["different_blob_count"], 1)
        self.assertEqual(len(api.calls), 5, "Three immutable trees reused across two comparisons")
        self.assertFalse(result["product_conflict_certified"])
        self.assertFalse(result["complete_repository_semantic_coverage"])
        self.assertFalse(result["writes_performed"])
        self.assertIn("byte-identical 1", deep_markdown({"deep_triage": result}))

    def test_pair_that_is_not_open_is_rejected(self):
        api = FakeDeepAPI()
        snap, report = snap_and_report()
        self.assertBlocked(lambda: deep_review(api, snap, report, [(75, 99)]),
                           "DEEP_PAIR_PR_NOT_OPEN")
        self.assertEqual(api.calls, [])

    def test_pair_without_path_overlap_is_rejected(self):
        api = FakeDeepAPI()
        snap, report = snap_and_report()
        report["overlap_pairs"] = []
        self.assertBlocked(lambda: deep_review(api, snap, report, [(75, 77)]),
                           "DEEP_PAIR_NO_SHARED_CHANGED_FILES")
        self.assertEqual(api.calls, [])

    def test_overlap_count_mismatch_not_accepted(self):
        api = FakeDeepAPI()
        snap, report = snap_and_report()
        report["overlap_pairs"][-1]["count"] = 3
        self.assertBlocked(lambda: deep_review(api, snap, report, [(75, 77)]),
                           "DEEP_CHANGED_PATH_INVENTORY_MISMATCH")

    def test_compare_spoofed_base_rejected(self):
        api = FakeDeepAPI()
        key = f"/repos/{REPO}/compare/{A}...{B}"
        api.payload[key]["base_commit"]["sha"] = C
        self.assertBlocked(lambda: _compare(api, REPO, A, B),
                           "DEEP_COMPARE_BASE_IDENTITY_MISMATCH")

    def test_compare_spoofed_head_rejected(self):
        api = FakeDeepAPI()
        key = f"/repos/{REPO}/compare/{A}...{B}"
        api.payload[key]["commits"][-1]["sha"] = C
        self.assertBlocked(lambda: _compare(api, REPO, A, B),
                           "DEEP_COMPARE_TARGET_NOT_VERIFIED")

    def test_compare_inconsistent_direction_rejected(self):
        api = FakeDeepAPI()
        key = f"/repos/{REPO}/compare/{A}...{B}"
        api.payload[key]["behind_by"] = 1
        self.assertBlocked(lambda: _compare(api, REPO, A, B),
                           "DEEP_COMPARE_DIRECTION_INCONSISTENT")

    def test_behind_compares_exact_target_by_pinned_commit_lookup(self):
        api = FakeDeepAPI()
        result = _compare(api, REPO, A, C)
        self.assertEqual(result["relation"], "B_ANCESTOR_OF_A")
        self.assertIn(f"/repos/{REPO}/commits/{C}", api.calls)

    def test_truncated_tree_must_fail_not_mark_all_identical(self):
        api = FakeDeepAPI()
        api.payload[f"/repos/{REPO}/git/trees/{A}?recursive=1"]["truncated"] = True
        self.assertBlocked(lambda: _tree_blobs(api, REPO, A),
                           "DEEP_GIT_TREE_INCOMPLETE")

    def test_tree_duplicate_path_rejected(self):
        api = FakeDeepAPI()
        key = f"/repos/{REPO}/git/trees/{A}?recursive=1"
        api.payload[key]["tree"] += [copy.deepcopy(api.payload[key]["tree"][0])]
        self.assertBlocked(lambda: _tree_blobs(api, REPO, A),
                           "DEEP_GIT_TREE_ENTRY_INVALID")

    def test_tree_record_budget_rejected(self):
        api = FakeDeepAPI()
        key = f"/repos/{REPO}/git/trees/{A}?recursive=1"
        api.payload[key]["tree"] = [
            {"path": f"file/{i}.kt", "type": "blob", "sha": H1}
            for i in range(6001)
        ]
        self.assertBlocked(lambda: _tree_blobs(api, REPO, A),
                           "DEEP_TREE_RECORD_BUDGET_EXCEEDED")

    def test_missing_blob_not_mistaken_for_equal_file(self):
        api = FakeDeepAPI()
        key = f"/repos/{REPO}/git/trees/{A}?recursive=1"
        api.payload[key]["tree"] = api.payload[key]["tree"][:1]
        snap, report = snap_and_report()
        x = deep_review(api, snap, report, [(75, 77)])["pairs"][0]
        self.assertEqual(x["byte_identical_blob_count"], 0)
        self.assertEqual(x["different_blob_count"], 1)
        self.assertEqual(x["missing_or_nonblob_count"], 1)
        self.assertEqual(x["missing_file_sample"], ["lib/same.kt"])

    def test_same_commit_is_not_claimed_semantic_identical(self):
        self.assertEqual(_compare(FakeDeepAPI(), REPO, A, A)["relation"],
                         "IDENTICAL_HEAD_SHA")


if __name__ == "__main__":
    unittest.main()
