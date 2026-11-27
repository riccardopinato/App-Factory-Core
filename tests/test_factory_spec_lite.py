#!/usr/bin/env python3
"""Adversarial offline vectors for Factory Spec Lite v1. No user app is modified."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_spec_lite import validate_manifest, main  # noqa: E402


def example(mode: str = "FAST") -> dict:
    return json.loads((ROOT / "spec_lite" / "examples" / f"{mode}.json").read_text(encoding="utf-8"))


def errors(doc: dict, factory=None, source=None) -> list[str]:
    return validate_manifest(
        doc,
        expected_factory_sha=factory or doc["factory"]["sha"],
        expected_source_sha=source or doc["target"]["source_sha"],
    )


class FactorySpecLiteTest(unittest.TestCase):
    def assertError(self, d: dict, expected: str) -> None:
        found = errors(d)
        self.assertTrue(any(expected in x for x in found), f"missing {expected}, got {found}")

    def test_three_modes_validate_as_proposed(self):
        for mode in ("FAST", "STANDARD", "CONTROLLED"):
            with self.subTest(mode=mode):
                d = example(mode)
                self.assertEqual(errors(d), [])
                self.assertEqual(d["approval"]["status"], "PROPOSED")
                self.assertEqual(d["verification"]["status"], "NOT_VERIFIED")

    def test_templates_cover_spec_plan_tasks_and_mode(self):
        for mode in ("FAST", "STANDARD", "CONTROLLED"):
            with self.subTest(mode=mode):
                text = (ROOT / "spec_lite" / "templates" / f"{mode}.md").read_text(encoding="utf-8")
                for required in ("Specification", "Plan", "Tasks", "FR-", "AC-", mode):
                    self.assertIn(required, text)

    def test_missing_requirements_rejected(self):
        d = example()
        d["requirements"] = []
        self.assertError(d, "SCHEMA:requirements:")

    def test_missing_acceptance_rejected(self):
        d = example()
        d["requirements"][0]["acceptance"] = []
        self.assertError(d, "SCHEMA:requirements.0.acceptance:")

    def test_duplicate_requirement_id_rejected(self):
        d = example()
        d["requirements"].append(copy.deepcopy(d["requirements"][0]))
        self.assertError(d, "DUPLICATE_REQUIREMENT_ID:FR-001")

    def test_duplicate_acceptance_id_rejected(self):
        d = example()
        copy_req = copy.deepcopy(d["requirements"][0])
        copy_req["id"] = "FR-002"
        d["requirements"].append(copy_req)
        self.assertError(d, "DUPLICATE_ACCEPTANCE_ID:AC-001")

    def test_unresolved_requirement_conflict_rejected(self):
        d = example()
        d["requirements"][0]["conflicts_with"] = ["FR-002"]
        self.assertError(d, "UNRESOLVED_REQUIREMENT_CONFLICT")

    def test_path_scope_conflict_rejected(self):
        d = example()
        d["scope"]["forbidden_paths"] = ["lib/**"]
        self.assertError(d, "CONFLICTING_PATH_SCOPE")

    def test_traversal_and_unsafe_paths_rejected(self):
        d = example()
        d["scope"]["allowed_paths"] = ["../outside"]
        self.assertError(d, "INVALID_SCOPE_PATH")

    def test_wrong_target_source_sha_rejected(self):
        d = example()
        found = errors(d, source="a" * 40)
        self.assertIn("SOURCE_SHA_MISMATCH", found)

    def test_wrong_factory_sha_rejected(self):
        d = example()
        found = errors(d, factory="a" * 40)
        self.assertIn("FACTORY_SHA_MISMATCH", found)

    def test_wrong_ref_sha_rejected(self):
        d = example("STANDARD")
        d["canonical_refs"]["product_bible"]["sha"] = "a" * 40
        self.assertError(d, "CANONICAL_REF_DRIFT:product_bible")

    def test_missing_product_approval_rejected(self):
        d = example("STANDARD")
        d["approval"]["status"] = "APPROVED"
        self.assertError(d, "APPROVAL_EVIDENCE_REQUIRED")

    def test_proposed_requirement_cannot_ship(self):
        d = example("STANDARD")
        d["approval"] = {"status": "APPROVED", "decision_ref": "https://github.com/riccardopinato/Android-Omni-Cleaner/issues/1"}
        self.assertError(d, "PROPOSED_REQUIREMENT_CANNOT_SHIP")

    def test_proposal_cannot_claim_approved_req(self):
        d = example()
        d["requirements"][0]["status"] = "APPROVED"
        self.assertError(d, "UNAUTHORIZED_REQUIREMENT_APPROVAL")

    def test_unapproved_product_ref_cannot_ship(self):
        d = example()
        d["approval"] = {"status": "APPROVED", "decision_ref": "https://github.com/riccardopinato/GalleryDrift/issues/1"}
        d["requirements"][0]["status"] = "APPROVED"
        self.assertError(d, "APPROVED_SCOPE_REQUIRES_PRODUCT_BIBLE_AND_ROADMAP")

    def test_fast_with_data_loss_risk_rejected(self):
        d = example()
        d["risk"]["data_loss"] = True
        self.assertError(d, "HIGH_RISK_REQUIRES_CONTROLLED")

    def test_controlled_without_rollback_rejected(self):
        d = example("CONTROLLED")
        d["validation"]["rollback_plan"] = None
        self.assertError(d, "CONTROLLED_REQUIRES_ROLLBACK_PLAN")

    def test_controlled_without_gate_rejected(self):
        d = example("CONTROLLED")
        d["validation"]["manual_gate"] = False
        self.assertError(d, "CONTROLLED_REQUIRES_MANUAL_GATE")

    def test_missing_ac_test_mapping_rejected(self):
        d = example("STANDARD")
        d["validation"]["required_checks"] = ["INTEGRATION_TEST"]
        self.assertError(d, "ACCEPTANCE_TEST_GAP:AC-001")

    def test_unmapped_required_kind_is_rejected(self):
        d = example("STANDARD")
        d["validation"]["required_checks"].append("DEVICE_TEST")
        self.assertError(d, "REQUIRED_CHECK_UNMAPPED:DEVICE_TEST")

    def test_controlled_required_device_kind_cannot_be_unmapped(self):
        d = example("CONTROLLED")
        d["requirements"][0]["acceptance"] = [
            ac for ac in d["requirements"][0]["acceptance"]
            if ac["evidence_type"] != "DEVICE_TEST"
        ]
        self.assertError(d, "REQUIRED_CHECK_UNMAPPED:DEVICE_TEST")

    def test_all_proposed_modes_map_each_mandatory_check(self):
        for mode in ("FAST", "STANDARD", "CONTROLLED"):
            d = example(mode)
            mapped = {
                ac["evidence_type"]
                for req in d["requirements"] for ac in req["acceptance"]
            }
            self.assertEqual(set(d["validation"]["required_checks"]), mapped)

    def test_claim_without_evidence_rejected(self):
        d = example()
        d["verification"]["status"] = "RUNTIME_VERIFIED"
        self.assertError(d, "UNPROVEN_VERIFICATION_CLAIM")

    def test_untrusted_sha_parameter_rejected(self):
        d = example()
        self.assertIn("TRUSTED_SOURCE_SHA_MISSING_OR_INVALID", errors(d, source="wrong-sha"))

    def test_examples_cli_pass_but_not_runtime(self):
        self.assertEqual(main(["--examples"]), 0)


if __name__ == "__main__":
    unittest.main()
