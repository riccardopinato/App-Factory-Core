#!/usr/bin/env python3
"""Adversarial read-only delta, drift and postmerge closeout tests."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_spec_lite import validate_manifest  # noqa: E402
from check_spec_lite_drift import review  # noqa: E402
from spec_lite_closeout import reconcile  # noqa: E402


def sample(mode="FAST"):
    return json.loads((ROOT / "spec_lite" / "examples" / f"{mode}.json").read_text(encoding="utf-8"))


def errors(doc):
    return validate_manifest(doc, expected_factory_sha=doc["factory"]["sha"],
                             expected_source_sha=doc["target"]["source_sha"])


def delta(doc, operation="ADDED", previous=None):
    doc["requirements"][0]["delta"] = {
        "operation": operation, "previous": previous,
        "reason": "Reconcile the behavior without changing unapproved product scope.",
    }
    return doc


def prior(doc):
    return {"spec_id": doc["spec_id"], "requirement_id": "FR-001", "source_sha": "1" * 40}


class DeltaContractTests(unittest.TestCase):
    def assertHas(self, doc, prefix):
        self.assertTrue(any(prefix in e for e in errors(doc)), errors(doc))

    def test_existing_fixtures_unchanged(self):
        for mode in ("FAST", "STANDARD", "CONTROLLED"):
            self.assertEqual(errors(sample(mode)), [])

    def test_added_delta_valid_without_previous(self):
        self.assertEqual(errors(delta(sample())), [])

    def test_modified_previous_pinned_valid(self):
        d = sample("STANDARD")
        self.assertEqual(errors(delta(d, "MODIFIED", prior(d))), [])

    def test_added_with_previous_rejected(self):
        d = sample()
        self.assertHas(delta(d, "ADDED", prior(d)), "DELTA_ADDED_MUST_NOT_HAVE_PREVIOUS")

    def test_modified_without_previous_rejected(self):
        self.assertHas(delta(sample(), "MODIFIED"), "DELTA_PREVIOUS_REQUIRED")

    def test_removed_in_fast_rejected(self):
        d = sample()
        self.assertHas(delta(d, "REMOVED", prior(d)), "DELTA_REMOVAL_NOT_FAST")

    def test_previous_cannot_be_current_unmodified_sha(self):
        d = sample()
        prev = prior(d)
        prev["source_sha"] = d["target"]["source_sha"]
        self.assertHas(delta(d, "MODIFIED", prev), "DELTA_PREVIOUS_NOT_PINNED_TO_PRIOR_STATE")

    def test_invalid_operation_rejected_by_schema(self):
        d = sample()
        delta(d, "AUTO_MERGE")
        self.assertHas(d, "SCHEMA:")

    def test_previous_invalid_sha_rejected_by_schema(self):
        d = sample("STANDARD")
        prev = prior(d)
        prev["source_sha"] = "0"
        self.assertHas(delta(d, "MODIFIED", prev), "SCHEMA:")


class DriftTests(unittest.TestCase):
    def setUp(self):
        self.d = delta(sample())
        self.repo = self.d["target"]["repository"]
        self.heads = {self.repo: self.d["target"]["source_sha"]}

    def check(self, docs=None, heads=None, prs=None, canonical=None):
        return review(docs if docs is not None else [self.d],
                      heads=self.heads if heads is None else heads,
                      open_prs=[] if prs is None else prs,
                      canonical={} if canonical is None else canonical)

    def test_complete_source_snapshot_is_review_not_certification(self):
        v = self.check()
        self.assertEqual(v["status"], "REVIEW_ONLY_NOT_CERTIFIED")
        self.assertFalse(v["writes_performed"])
        self.assertEqual(v["snapshot_authenticity"], "NOT_ATTESTED")

    def test_missing_snapshots_block(self):
        r = review([self.d], heads=None, open_prs=None, canonical=None)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertIn("OPEN_PR_SNAPSHOT_REQUIRED", r["errors"])


    def test_open_pr_with_incomplete_requirement_id_is_blocked(self):
        v = self.check(prs=[{"repository": self.repo, "number": 12,
            "requirements": [{}], "changed_paths": []}])
        self.assertIn(f"PR_REQUIREMENT_IDENTITY_MISSING:{self.repo}:12", v["errors"])

    def test_intersecting_globs_are_reviewed(self):
        first = copy.deepcopy(self.d)
        second = copy.deepcopy(self.d)
        second["spec_id"] += "-ALT"
        second["requirements"][0]["id"] = "FR-002"
        second["requirements"][0]["acceptance"][0]["id"] = "AC-002"
        first["scope"]["allowed_paths"] = ["lib/*/foo.dart"]
        second["scope"]["allowed_paths"] = ["lib/widgets/*.dart"]
        v = self.check(docs=[first, second])
        self.assertTrue(any("PATH_OVERLAP_REVIEW" in x for x in v["warnings"]))

    def test_stale_source_blocks(self):
        self.assertTrue(any("STALE_TARGET_HEAD" in x
                            for x in self.check(heads={self.repo: "a" * 40})["errors"]))

    def test_same_previous_requirement_changed_twice_blocks(self):
        first = delta(sample("STANDARD"), "MODIFIED", prior(sample("STANDARD")))
        other = copy.deepcopy(first)
        other["spec_id"] += "-ALT"
        repo = first["target"]["repository"]
        ref = first["requirements"][0]["delta"]["previous"]
        key = f"{repo}@{ref['source_sha']}:{ref['spec_id']}:{ref['requirement_id']}"
        result = review([first, other], heads={repo: first["target"]["source_sha"]},
                        open_prs=[], canonical={key: {"status": "CURRENT"}})
        self.assertTrue(any("OVERLAPPING_REQUIREMENT_CHANGE" in x
                            for x in result["errors"]))

    def test_previous_requirement_must_exist_in_pinned_snapshot(self):
        d = delta(sample("STANDARD"), "MODIFIED", prior(sample("STANDARD")))
        repo = d["target"]["repository"]
        v = review([d], heads={repo: d["target"]["source_sha"]},
                   open_prs=[], canonical={})
        self.assertTrue(any("PREVIOUS_REQUIREMENT_NOT_VERIFIED" in x for x in v["errors"]))

    def test_previous_requirement_current_passes_with_matching_key(self):
        d = delta(sample("STANDARD"), "MODIFIED", prior(sample("STANDARD")))
        repo = d["target"]["repository"]
        key = f"{repo}@{'1'*40}:{d['spec_id']}:FR-001"
        v = review([d], heads={repo: d["target"]["source_sha"]},
                   open_prs=[], canonical={key: {"status": "CURRENT"}})
        self.assertEqual(v["errors"], [])

    def test_pr_missing_requirement_inventory_is_blocked(self):
        v = self.check(prs=[{"repository": self.repo, "number": 12, "changed_paths": []}])
        self.assertTrue(any("PR_REQUIREMENT_COVERAGE_UNKNOWN" in x for x in v["errors"]))

    def test_open_pr_same_requirement_blocks(self):
        v = self.check(prs=[{"repository": self.repo, "number": 12,
            "requirements": [{"spec_id": self.d["spec_id"], "requirement_id": "FR-001"}],
            "changed_paths": []}])
        self.assertTrue(any("OPEN_PR_REQUIREMENT_CONFLICT" in x for x in v["errors"]))

    def test_open_pr_shared_path_is_review_not_automatic_block(self):
        v = self.check(prs=[{"repository": self.repo, "number": 12,
            "requirements": [], "changed_paths": ["lib/gallery.dart"]}])
        self.assertTrue(any("OPEN_PR_PATH_OVERLAP_REVIEW" in x for x in v["warnings"]))
        self.assertEqual(v["status"], "REVIEW_ONLY_NOT_CERTIFIED")


class CloseoutTests(unittest.TestCase):
    def setUp(self):
        self.doc = delta(sample())
        self.doc["approval"]["status"] = "APPROVED"
        self.doc["approval"]["decision_ref"] = "https://github.com/example/repo/issues/1"
        self.doc["requirements"][0]["status"] = "APPROVED"
        self.repo = self.doc["target"]["repository"]
        ref = {"repository": self.repo, "sha": self.doc["target"]["source_sha"]}
        # Synthetic approved product refs for preview tests only; no real Gallery
        # Product Bible is fabricated or written in any consumer repository.
        self.doc["canonical_refs"]["product_bible"] = {**ref, "path": "PRODUCT_BIBLE.md"}
        self.doc["canonical_refs"]["roadmap"] = {**ref, "path": "ROADMAP.md"}
        self.receipts = {
            "merged": True, "merge_sha": "9"*40, "ci_conclusion": "success",
            "ci_head_sha": "9"*40, "pr_url": "https://github.com/example/repo/pull/2",
            "checks": {"SOURCE_TEST": "https://github.com/example/repo/actions/runs/3"},
            "factory_sha": self.doc["factory"]["sha"],
            "source_sha": self.doc["target"]["source_sha"],
        }

    def test_valid_added_change_is_preview_only(self):
        r = reconcile(self.doc, {}, self.receipts)
        self.assertEqual(r["status"], "PREVIEW_REQUIRES_TRUSTED_REVIEW")
        self.assertFalse(r["writes_performed"])
        self.assertFalse(r["product_bible_written"])
        self.assertIn(f"{self.repo}:{self.doc['spec_id']}:FR-001", r["proposed_canonical"])


    def test_rename_cannot_overwrite_current_destination(self):
        prev = prior(self.doc)
        self.doc["requirements"][0]["id"] = "FR-002"
        self.doc["requirements"][0]["acceptance"][0]["id"] = "AC-002"
        delta(self.doc, "RENAMED", prev)
        oldkey = f"{self.repo}:{prev['spec_id']}:FR-001"
        newkey = f"{self.repo}:{self.doc['spec_id']}:FR-002"
        canonical = {
            oldkey: {"status": "CURRENT", "source_sha": prev["source_sha"], "text": "old"},
            newkey: {"status": "CURRENT", "source_sha": "8"*40, "text": "unrelated"},
        }
        result = reconcile(self.doc, canonical, self.receipts)
        self.assertIn("RENAMED_DESTINATION_ALREADY_EXISTS:FR-002", result["errors"])
        self.assertIsNone(result["proposed_canonical"])

    def test_approved_manifest_with_proposed_requirement_denied(self):
        self.doc["requirements"][0]["status"] = "PROPOSED"
        result = reconcile(self.doc, {}, self.receipts)
        self.assertTrue(any("PROPOSED_REQUIREMENT_CANNOT_SHIP" in x
                            for x in result["errors"]))

    def test_standard_security_risk_without_controlled_denied(self):
        self.doc["mode"] = "STANDARD"
        self.doc["risk"]["security"] = True
        result = reconcile(self.doc, {}, self.receipts)
        self.assertTrue(any("HIGH_RISK_REQUIRES_CONTROLLED" in x
                            for x in result["errors"]))

    def test_sha_supplied_independently_must_match(self):
        receipts = dict(self.receipts, source_sha="a"*40)
        result = reconcile(self.doc, {}, receipts)
        self.assertTrue(any("SOURCE_SHA_MISMATCH" in x for x in result["errors"]))

    def test_missing_merge_rejected(self):
        r = dict(self.receipts, merged=False)
        self.assertIn("MERGED_PR_REQUIRED", reconcile(self.doc, {}, r)["errors"])

    def test_ci_must_match_merge_sha(self):
        r = dict(self.receipts, ci_head_sha="b"*40)
        self.assertIn("POSTMERGE_CI_SHA_MISMATCH", reconcile(self.doc, {}, r)["errors"])

    def test_missing_required_test_receipt(self):
        r = dict(self.receipts, checks={})
        self.assertTrue(any("MISSING_REQUIRED_CHECK_EVIDENCE" in x for x in
                            reconcile(self.doc, {}, r)["errors"]))

    def test_proposal_not_approved_cannot_close(self):
        self.doc["approval"]["status"] = "PROPOSED"
        self.assertIn("PRODUCT_APPROVAL_REQUIRED",
                      reconcile(self.doc, {}, self.receipts)["errors"])

    def test_modify_existing_requirement_not_new(self):
        prev = prior(self.doc)
        delta(self.doc, "MODIFIED", prev)
        key = f"{self.repo}:{prev['spec_id']}:FR-001"
        existing = {key: {"status": "CURRENT", "source_sha": prev["source_sha"], "text": "old"}}
        r = reconcile(self.doc, existing, self.receipts)
        self.assertEqual(r["status"], "PREVIEW_REQUIRES_TRUSTED_REVIEW")
        self.assertEqual(r["proposed_canonical"][key]["source_sha"], "9"*40)
        self.assertEqual(r["proposed_canonical"][key]["history"][0]["source_sha"], prev["source_sha"])
        self.assertEqual(r["proposed_canonical"][key]["history"][0]["text"], "old")

    def test_missing_prior_snapshot_blocks(self):
        delta(self.doc, "MODIFIED", prior(self.doc))
        r = reconcile(self.doc, {}, self.receipts)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertIsNone(r["proposed_canonical"])

    def test_human_gate_required_for_controlled(self):
        self.doc["mode"] = "CONTROLLED"
        self.assertIn("CONTROLLED_HUMAN_GATE_EVIDENCE_REQUIRED",
                      reconcile(self.doc, {}, self.receipts)["errors"])


if __name__ == "__main__":
    unittest.main()
