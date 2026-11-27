"""Fail-closed evaluation of selective source-only Spec Lite adoption decision."""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "spec_lite" / "ADOPTION_DECISION_2026-11-27.json"
SHA = re.compile(r"^[0-9a-f]{40}$")


def check_decision(doc):
    errors = []
    if doc.get("schema_version") != 1 or doc.get("record_id") != "FSL-ADOPTION-20261127":
        errors.append("DECISION_SCHEMA")
    if doc.get("status") != "LIMITED_OPT_IN_SOURCE_ONLY":
        errors.append("PREMATURE_GLOBAL_ADOPTION")
    stages = doc.get("stage_gates", {})
    if set(stages) != {"step1", "step2", "step3", "step4"}:
        errors.append("MISSING_STAGE_GATES")
    elif any(stages[k].get("status") != "PASS_SOURCE_CI" for k in stages):
        errors.append("STAGE_NOT_VERIFIED")
    base = doc.get("source_of_truth", {})
    if not SHA.fullmatch(str(base.get("factory_baseline_sha", ""))):
        errors.append("FACTORY_SHA_DRIFT")
    if str(base.get("master_version")) != "27" or base.get("golden_index") != 31:
        errors.append("MASTER_PRECEDENCE_DRIFT")
    if base.get("external_research_status") != "E1_RESEARCH_ONLY":
        errors.append("FALSE_OSS_ADMISSION")
    m = doc.get("metrics", {})
    if m.get("pilot_acceptance_criteria_linked") != 11 or m.get("pilot_regression_tests_added") != 11:
        errors.append("PILOT_COVERAGE_UNPROVEN")
    if m.get("agent_adapter_offline_tests") != 19 or m.get("applab_adapter_offline_tests") != 22:
        errors.append("ADAPTER_TEST_COVERAGE_UNPROVEN")
    if m.get("review_findings_repaired_in_applab") != 4:
        errors.append("REVIEW_FINDINGS_UNVERIFIED")
    if any(m.get(x) != "NOT_MEASURED" for x in
           ("development_time_saved", "token_savings", "device_performance_improvement")):
        errors.append("UNPROVEN_EFFICIENCY_CLAIM")
    restrictions = doc.get("restrictions", {})
    must_deny = (
        "new_cap_id", "new_golden", "new_scheduler", "new_verifier",
        "install_spec_kit_cli", "auto_execute_jobs", "auto_approve_requirements",
        "auto_merge", "auto_release", "new_product_policy_authority",
        "bulk_story_or_recipe_spec_per_record"
    )
    if any(restrictions.get(k) is not False for k in must_deny):
        errors.append("UNSAFE_PROMOTION_OR_NEW_AUTHORITY")
    bounds = doc.get("status_boundaries", {})
    if bounds.get("actual_agent_windows_runtime") != "NOT_VERIFIED" or (
        bounds.get("actual_production_applab_workflow") != "NOT_VERIFIED"
    ):
        errors.append("RUNTIME_FALSE_PASS")
    modes = doc.get("mode_rules", {})
    if (modes.get("FAST", {}).get("adoption") != "OPTIONAL_SINGLE_COMPACT_CONTRACT"
        or modes.get("FAST", {}).get("mandatory_documents") != 1
        or modes.get("STANDARD", {}).get("adoption") != "OPT_IN_FOR_BOUNDED_FEATURES_BUGS"
        or modes.get("CONTROLLED", {}).get("human_gate_required") is not True):
        errors.append("UNSAFE_ROUTER_ADOPTION")
    scope = doc.get("rollout", {})
    if len(scope.get("already_piloted", [])) != 3 or scope.get("other_repositories") != "NOT_BULK_ADOPTED":
        errors.append("PREMATURE_BULK_ROLLOUT")
    gate = stages.get("step4", {})
    if any(not SHA.fullmatch(str(gate.get(k, ""))) for k in ("agent_core_sha", "applab_sha")):
        errors.append("ADAPTER_SHA_MISSING")
    if not all(str(gate.get(k, "")).startswith("https://github.com/")
               for k in ("app_lab_main_ci", "app_lab_main_android", "agent_main_ci")):
        errors.append("MAIN_CI_RECEIPT_MISSING")
    return sorted(set(errors))


class FactorySpecLiteAdoptionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DECISION.read_text(encoding="utf-8"))

    def test_selective_decision_has_no_unproven_promotion(self):
        self.assertEqual(check_decision(self.data), [])

    def test_claiming_full_global_adoption_is_denied(self):
        d = copy.deepcopy(self.data)
        d["status"] = "CERTIFIED_AUTONOMOUS_GLOBAL"
        self.assertIn("PREMATURE_GLOBAL_ADOPTION", check_decision(d))

    def test_master_or_golden_promotion_is_denied(self):
        d = copy.deepcopy(self.data)
        d["restrictions"]["new_golden"] = True
        self.assertIn("UNSAFE_PROMOTION_OR_NEW_AUTHORITY", check_decision(d))

    def test_runtime_claim_without_real_proof_denied(self):
        d = copy.deepcopy(self.data)
        d["status_boundaries"]["actual_agent_windows_runtime"] = "CERTIFIED"
        self.assertIn("RUNTIME_FALSE_PASS", check_decision(d))

    def test_unmeasured_token_speedups_cannot_be_claimed(self):
        d = copy.deepcopy(self.data)
        d["metrics"]["token_savings"] = "20%"
        self.assertIn("UNPROVEN_EFFICIENCY_CLAIM", check_decision(d))

    def test_missing_ci_evidence_blocks_adoption(self):
        d = copy.deepcopy(self.data)
        d["stage_gates"]["step4"]["app_lab_main_android"] = None
        self.assertIn("MAIN_CI_RECEIPT_MISSING", check_decision(d))

    def test_controlled_without_human_gate_denied(self):
        d = copy.deepcopy(self.data)
        d["mode_rules"]["CONTROLLED"]["human_gate_required"] = False
        self.assertIn("UNSAFE_ROUTER_ADOPTION", check_decision(d))

    def test_bulk_rollout_denied(self):
        d = copy.deepcopy(self.data)
        d["rollout"]["other_repositories"] = "AUTO_DEPLOY_ALL"
        self.assertIn("PREMATURE_BULK_ROLLOUT", check_decision(d))


if __name__ == "__main__":
    unittest.main()
