"""Fail-closed, offline proof that Step 3 ledger cannot self-certify pending checks."""
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "spec_lite" / "pilots" / "2026-11-27.json"


def verify_ledger(data: dict) -> list[str]:
    errors: list[str] = []
    items = data.get("pilots", [])
    if len(items) != 3 or data.get("pilot_count") != 3:
        errors.append("REQUIRES_EXACTLY_THREE_PILOTS")
    if len({x.get("id") for x in items}) != len(items):
        errors.append("DUPLICATE_PILOT_ID")
    if data.get("factory_source_sha") != "f8b9f550c544735237f19cdd723bd2df667ceee6":
        errors.append("FACTORY_BASELINE_DRIFT")
    if data.get("no_runtime_certification_claim") is not True:
        errors.append("RUNTIME_FALSE_PASS_RISK")
    if data.get("no_golden_promotion") is not True:
        errors.append("GOLDEN_PREMATURE_PROMOTION")
    total_ac = 0
    total_tests = 0
    all_complete = True
    for p in items:
        total_ac += len(p.get("acceptance_criteria", []))
        total_tests += p.get("tests_added", 0)
        expected = f"{len(p.get('acceptance_criteria', []))}/{len(p.get('acceptance_criteria', []))} source-level mapped"
        if p.get("requirement_coverage") != expected or not p.get("acceptance_criteria"):
            errors.append("COVERAGE_MISMATCH:" + p.get("id", "?"))
        if p.get("tests_added") != len(p.get("acceptance_criteria", [])):
            errors.append("TEST_COUNT_MISMATCH:" + p.get("id", "?"))
        for key in ("source_sha", "pr_head_sha", "merged_main_sha"):
            if not isinstance(p.get(key), str) or len(p[key]) != 40:
                errors.append("MISSING_SOURCE_SHA:" + p.get("id", "?") + ":" + key)
        if p.get("pr_ci", {}).get("status") != "SUCCESS" or not p.get("pr_ci", {}).get("run_url"):
            errors.append("PR_CI_NOT_PROVEN:" + p.get("id", "?"))
        if p.get("evidence_grade") != "SOURCE_AND_CI_ONLY":
            errors.append("SCOPE_OF_PROOF_INVALID:" + p.get("id", "?"))
        if p.get("physical_qa") != "NOT_VERIFIED" or p.get("effectiveness_gain") != "NOT_MEASURED":
            errors.append("OVERCLAIMED_PROOF:" + p.get("id", "?"))
        if p.get("main_ci", {}).get("status") != "SUCCESS" or not p.get("main_ci", {}).get("run_url"):
            all_complete = False
    if data.get("acceptance_criteria_mapped") != total_ac or data.get("tests_added") != total_tests:
        errors.append("TOTAL_MISMATCH")
    gate = data.get("gate_to_maxi_step4", {})
    if all_complete:
        if gate.get("status") != "ACCEPTED" or gate.get("all_pilot_main_ci_green") is not True:
            errors.append("STEP3_GATES_NOT_RECORDED")
        if gate.get("quantitative_evaluation_complete") is not True:
            errors.append("QUANTITATIVE_EVALUATION_REQUIRED")
        metrics = data.get("metrics", {})
        if (not isinstance(metrics, dict) or metrics.get("acceptance_criteria_linked") != total_ac
            or metrics.get("tests_added") != total_tests
            or not isinstance(metrics.get("measured_ci_job_seconds"), dict)
            or not metrics["measured_ci_job_seconds"]):
            errors.append("QUANTITATIVE_METRICS_MISSING_OR_INCONSISTENT")
        if data.get("status") != "STEP3_SOURCE_PILOTS_COMPLETE":
            errors.append("COMPLETE_STATUS_MISMATCH")
    else:
        if gate.get("status") != "BLOCKED" or gate.get("all_pilot_main_ci_green") is not False:
            errors.append("FALSE_STEP4_APPROVAL")
        if data.get("status") != "IN_PROGRESS_POSTMERGE_CI":
            errors.append("FALSE_STEP3_COMPLETION")
    return errors


class PilotEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FILE.read_text(encoding="utf-8"))

    def test_record_is_internally_consistent(self):
        self.assertEqual(verify_ledger(self.data), [])

    def test_unverified_main_cannot_authorize_step4(self):
        trial = copy.deepcopy(self.data)
        trial["pilots"][0]["main_ci"] = {"status": "PENDING", "run_url": None}
        trial["status"] = "STEP3_SOURCE_PILOTS_COMPLETE"
        trial["gate_to_maxi_step4"] = {"status": "ACCEPTED", "all_pilot_main_ci_green": True}
        found = verify_ledger(trial)
        self.assertIn("FALSE_STEP4_APPROVAL", found)

    def test_corrupted_sha_or_claim_blocks(self):
        trial = copy.deepcopy(self.data)
        trial["pilots"][0]["source_sha"] = "BAD"
        trial["pilots"][1]["evidence_grade"] = "DEVICE_CERTIFIED"
        errors = verify_ledger(trial)
        self.assertTrue(any("MISSING_SOURCE_SHA" in x for x in errors))
        self.assertTrue(any("SCOPE_OF_PROOF_INVALID" in x for x in errors))

    def test_missing_criterion_or_test_breaks_coverage(self):
        trial = copy.deepcopy(self.data)
        trial["pilots"][2]["tests_added"] = 2
        found = verify_ledger(trial)
        self.assertTrue(any("TEST_COUNT_MISMATCH" in x for x in found))

    def test_completed_main_ci_does_not_bypass_quantitative_gate(self):
        trial = copy.deepcopy(self.data)
        self.assertTrue(all(x["main_ci"]["status"] == "SUCCESS" for x in trial["pilots"]))
        trial["gate_to_maxi_step4"]["quantitative_evaluation_complete"] = False
        found = verify_ledger(trial)
        self.assertIn("QUANTITATIVE_EVALUATION_REQUIRED", found)

    def test_missing_quantitative_observation_blocks_step4(self):
        trial = copy.deepcopy(self.data)
        del trial["metrics"]["measured_ci_job_seconds"]
        found = verify_ledger(trial)
        self.assertIn("QUANTITATIVE_METRICS_MISSING_OR_INCONSISTENT", found)
