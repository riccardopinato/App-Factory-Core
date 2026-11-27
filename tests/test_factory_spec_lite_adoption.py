"""Selective Factory Spec Lite adoption decision: fail closed on false promotion.

The ledger is a previously CI-verified evidence record. These offline tests
check internal consistency and governance constraints, not external runtime.
"""
from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADOPTION = ROOT / "spec_lite/adoption/2026-11-27.json"
PILOTS = ROOT / "spec_lite/pilots/2026-11-27.json"
SHA = re.compile(r"^[0-9a-f]{40}$")
CI_URL = re.compile(r"^https://github\.com/riccardopinato/[^/]+/actions/runs/[0-9]+$")


def validate_adoption(d: dict, ledger: dict) -> list[str]:
    errors: list[str] = []
    baseline = d.get("baseline", {})
    ev = d.get("evidence", {})
    g = d.get("guardrails", {})
    measurements = d.get("measurements", {})
    decision = d.get("decision", {})
    promotion = d.get("promotion", {})
    mode = d.get("mode_routing", {})
    rollout = d.get("rollout", {})

    if d.get("schema_version") != 1 or d.get("status") != "SELECTIVE_SOURCE_CI_ADOPTION":
        errors.append("ADOPTION_STATUS_INVALID")
    if baseline.get("factory_repo") != "riccardopinato/App-Factory-Core" or baseline.get("master_version") != "27" or baseline.get("golden_index_version") != 31:
        errors.append("FACTORY_AUTHORITY_DRIFT")
    if baseline.get("factory_main_before_pr") != "8b3d9263ad1a72f3b8a43273550fe43646780d78" or baseline.get("step3_ledger") != "spec_lite/pilots/2026-11-27.json":
        errors.append("FACTORY_BASELINE_DRIFT")
    step3 = ev.get("step3_pilots", {})
    if (ledger.get("status") != "STEP3_SOURCE_PILOTS_COMPLETE"
        or ledger.get("gate_to_maxi_step4", {}).get("status") != "ACCEPTED"
        or ledger.get("gate_to_maxi_step4", {}).get("all_pilot_main_ci_green") is not True
        or step3.get("main_sha") != baseline.get("factory_main_before_pr")
        or len(ledger.get("pilots", [])) != 3):
        errors.append("STEP3_SOURCE_GATES_NOT_PROVEN")
    ac_count = sum(len(p.get("acceptance_criteria", [])) for p in ledger.get("pilots", []))
    test_count = sum(p.get("tests_added", 0) for p in ledger.get("pilots", []))
    if (measurements.get("acceptance_criteria_linked") != ac_count
        or measurements.get("tests_added_ac") != test_count
        or step3.get("approved_ac_mappings") != ac_count
        or step3.get("regression_tests_added") != test_count
        or ac_count != 11 or test_count != 11):
        errors.append("MEASURED_AC_TEST_COVERAGE_DRIFT")
    stats = ledger.get("metrics", {})
    src_tests = stats.get("production_source_lines_added", 0) + stats.get("test_lines_added", 0)
    docs = stats.get("documentation_lines_added")
    if (measurements.get("pilot_doc_lines_added") != docs
        or measurements.get("pilot_source_test_lines_added") != src_tests
        or measurements.get("doc_to_source_test_ratio") != (docs / src_tests if src_tests else None)):
        errors.append("ACTUAL_COST_MEASUREMENT_DRIFT")
    for section in ("gallery", "omni"):
        val = measurements.get(section, {})
        if val.get("historical_ci_seconds", 0) <= 0 or val.get("success_pilot_ci_seconds", 0) <= 0 or val.get("postmerge_seconds", 0) <= 0:
            errors.append("CI_METRICS_INCOMPLETE:" + section)
    if (measurements.get("development_time_saved") != "NOT_MEASURED"
        or measurements.get("tokens_saved") != "NOT_MEASURED"
        or measurements.get("device_performance_gain") != "NOT_MEASURED"
        or measurements.get("speedup_proven") is not False):
        errors.append("UNPROVEN_EFFICIENCY_CLAIM")
    if measurements.get("traceability_gain_observed") is None or not isinstance(measurements["traceability_gain_observed"], str):
        errors.append("UNSUPPORTED_TRACEABILITY_CLAIM")

    bridges = ev.get("step4_bridges", [])
    expected = {
        "riccardopinato/App-Factory-Agent-Core": ("117b56b20dff1e63012c314ef32a2aa80fc558ab", 19),
        "riccardopinato/AppLab": ("0b498ef04458d56a17318823efa9e77f31cd8e4a", 22),
    }
    if len(bridges) != 2 or {x.get("owner") for x in bridges} != set(expected):
        errors.append("STEP4_BRIDGE_OWNERS_INCOMPLETE")
    for b in bridges:
        owner = b.get("owner")
        if owner not in expected:
            continue
        sha, count = expected[owner]
        if b.get("main_sha") != sha or b.get("test_methods") != count:
            errors.append("STEP4_EXACT_COMMIT_TEST_DRIFT:" + owner)
        for key in ("postmerge_ci",):
            if not isinstance(b.get(key), str) or not CI_URL.fullmatch(b[key]):
                errors.append("STEP4_MISSING_POSTMERGE_EVIDENCE:" + owner)
        if owner.endswith("AppLab") and (not CI_URL.fullmatch(b.get("android_postmerge_ci", ""))
                                         or not CI_URL.fullmatch(b.get("canary_postmerge_ci", ""))):
            errors.append("STEP4_APPLAB_RUNTIME_CI_EVIDENCE_MISSING")
    if not all(g.get(k) is True for k in (
        "master_router_precedence","product_bible_roadmap_approval_required",
        "golden_and_agents_precedence_preserved","no_missing_test_silently_green",
        "source_sha_exact","no_duplicate_scheduler","no_duplicate_verifier",
        "no_self_issued_approval","no_unverified_runtime_pass",
        "no_unreviewed_production_merge","no_automatic_store_release",
        "no_unapproved_cloud_or_billing","no_factory_golden_registry_update",
        "no_upstream_cli_install","no_mass_app_rollout"
    )):
        errors.append("SECURITY_OR_QUALITY_GATE_REDUCED")
    if (promotion.get("core_process") != "OPTIONAL_SOURCE_CI_TRACED"
        or promotion.get("golden_registry") != "UNCHANGED"
        or promotion.get("master") != "UNCHANGED"
        or promotion.get("application_migration") != "NONE"):
        errors.append("UNSUPPORTED_PROCESS_GOLDEN_OR_MASTER_PROMOTION")
    positive = decision.get("reuse", [])
    negative = decision.get("not_adopted", [])
    if (len(positive) != 4 or len(negative) != 5
        or len({x.get("id") for x in positive+negative}) != 9):
        errors.append("ADOPTION_DEDUP_MATRIX_INCOMPLETE")
    if any(x.get("status") not in {"ADOPT_OPTIONAL","ADOPT_AS_OPTIONAL_ADAPTER"} for x in positive):
        errors.append("MANDATORY_OR_UNVERIFIED_ADOPTION")
    if set(mode) != {"FAST", "STANDARD", "CONTROLLED"}:
        errors.append("ROUTER_MODE_REDUCTION")
    elif (mode["FAST"].get("extra_document_requirement") != "NONE"
          or mode["FAST"].get("risk_flags_must_all_be_false") is not True
          or mode["STANDARD"].get("requires_regression_mapping") is not True
          or mode["CONTROLLED"].get("requires_manual_gate_and_rollback") is not True
          or not all("UNCHANGED" in mode[m].get("existing_test_gates", "") for m in mode)):
        errors.append("ROUTER_OR_CONTROLLED_GATE_BYPASS")
    if (rollout.get("policy") != "OPT_IN_ONLY_ON_NEXT_APPROVED_SCOPED_CHANGE; NO BATCH REPO EDIT"
        or set(rollout.get("already_piloted", [])) != {
            "riccardopinato/GalleryDrift",
            "riccardopinato/Android-Omni-Cleaner",
            "riccardopinato/App-Factory-Agent-Core",
        } or set(rollout.get("not_per_record", [])) != {
            "riccardopinato/World-Days","riccardopinato/CookingAnime"
        }):
        errors.append("UNAUTHORIZED_MASS_APP_ROLLOUT")
    if not any("real" in str(x).lower() or "live" in str(x).lower() for x in d.get("not_proven", [])):
        errors.append("MISSING_REAL_RUNTIME_CAVEAT")
    return sorted(set(errors))


class FactorySpecLiteAdoptionTests(unittest.TestCase):
    def setUp(self):
        self.adoption = json.loads(ADOPTION.read_text(encoding="utf-8"))
        self.ledger = json.loads(PILOTS.read_text(encoding="utf-8"))

    def assertDenied(self, trial, code):
        found = validate_adoption(trial, self.ledger)
        self.assertIn(code, found, found)

    def test_selective_process_decision_is_internally_consistent(self):
        self.assertEqual(validate_adoption(self.adoption, self.ledger), [])

    def test_missing_bridge_ci_fails_closed(self):
        d = copy.deepcopy(self.adoption)
        d["evidence"]["step4_bridges"][1]["android_postmerge_ci"] = None
        self.assertDenied(d, "STEP4_APPLAB_RUNTIME_CI_EVIDENCE_MISSING")

    def test_wrong_applab_merge_sha_refused(self):
        d = copy.deepcopy(self.adoption)
        d["evidence"]["step4_bridges"][1]["main_sha"] = "f"*40
        self.assertDenied(d, "STEP4_EXACT_COMMIT_TEST_DRIFT:riccardopinato/AppLab")

    def test_unmeasured_token_speedups_refused(self):
        d = copy.deepcopy(self.adoption)
        d["measurements"]["speedup_proven"] = True
        d["measurements"]["tokens_saved"] = "40%"
        self.assertDenied(d, "UNPROVEN_EFFICIENCY_CLAIM")

    def test_false_golden_promotion_denied(self):
        d = copy.deepcopy(self.adoption)
        d["promotion"]["golden_registry"] = "CERTIFIED"
        self.assertDenied(d, "UNSUPPORTED_PROCESS_GOLDEN_OR_MASTER_PROMOTION")

    def test_new_global_rollout_denied(self):
        d = copy.deepcopy(self.adoption)
        d["rollout"]["policy"] = "MASS UPDATE ALL APPS"
        self.assertDenied(d, "UNAUTHORIZED_MASS_APP_ROLLOUT")

    def test_extra_mandatory_fast_documents_denied(self):
        d = copy.deepcopy(self.adoption)
        d["mode_routing"]["FAST"]["extra_document_requirement"] = "5 DOCS"
        self.assertDenied(d, "ROUTER_OR_CONTROLLED_GATE_BYPASS")

    def test_manual_gate_cannot_be_waived(self):
        d = copy.deepcopy(self.adoption)
        d["mode_routing"]["CONTROLLED"]["requires_manual_gate_and_rollback"] = False
        self.assertDenied(d, "ROUTER_OR_CONTROLLED_GATE_BYPASS")

    def test_incomplete_pilot_gate_blocks_adoption(self):
        ledger = copy.deepcopy(self.ledger)
        ledger["gate_to_maxi_step4"]["all_pilot_main_ci_green"] = False
        self.assertIn("STEP3_SOURCE_GATES_NOT_PROVEN", validate_adoption(self.adoption, ledger))

    def test_requirement_test_mapping_must_match_verified_ledger(self):
        d = copy.deepcopy(self.adoption)
        d["measurements"]["acceptance_criteria_linked"] += 1
        self.assertDenied(d, "MEASURED_AC_TEST_COVERAGE_DRIFT")

    def test_second_scheduler_or_verifier_refused(self):
        d = copy.deepcopy(self.adoption)
        d["guardrails"]["no_duplicate_scheduler"] = False
        self.assertDenied(d, "SECURITY_OR_QUALITY_GATE_REDUCED")


if __name__ == "__main__":
    unittest.main()
