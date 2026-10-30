#!/usr/bin/env python3
"""No-network tests; synthetic PRs are test fixtures, never real measurements."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import summarize_v27_delivery as m

LEDGER = Path(__file__).resolve().parents[1] / "evidence/v27-observability/DELIVERY_LEDGER.json"
PIN = "477de1e3cb3788ac828311cb1f04c8bbcfb97be7"


class DeliveryMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_cumulative_source_is_consistent_without_causal_attribution(self):
        summary = m.summarize(self.source)
        self.assertGreaterEqual(summary["cohorts"]["pre_v27"]["n"], 30)
        self.assertEqual(summary["total_observations"], len(self.source["records"]))
        self.assertEqual(summary["causal_attribution"], "NOT_VERIFIED")
        self.assertEqual(summary["actual_active_development_time"], "NOT_MEASURED")
        # As new evidence arrives, v27_confirmed may legitimately become >0.
        # A descriptive comparison is allowed only with matched independent samples.
        self.assertTrue(all(r["descriptive_relative_change_pct"] is None or
                            r["sufficient_matched_samples"]
                            for r in summary["comparable_groups"]))

    def test_optional_final_head_ci_evidence_is_scoped(self):
        for row in self.source["records"]:
            ids = row.get("ci_observed_run_ids")
            if ids is None:
                continue
            self.assertTrue(ids)
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(all(isinstance(x, int) and x > 0 for x in ids))
            sha = row["ci_observed_final_head_sha"]
            self.assertEqual(len(sha), 40)
            self.assertTrue(all(ch in "0123456789abcdef" for ch in sha))
            self.assertGreaterEqual(row["ci_observed_final_head_rerun_attempts"], 0)
            self.assertLessEqual(m.parse_time(row["ci_observed_last_success_at"]),
                                 m.parse_time(row["merged_at"]))
            # Final-head run_attempt=1 does not prove the entire PR had no retries.
            self.assertIsNone(row["ci_retries"])

    def test_anna_parallel_prs_are_not_counted_as_independent_work_time(self):
        summary = m.summarize(self.source)
        anna = next(x for x in summary["per_repo"]
                    if x["repo"] == "riccardopinato/Agenda-per-Anna")
        self.assertEqual(anna["pre_v27_n"], 8)
        self.assertEqual(anna["pre_v27_overlapping_pr_windows_n"], 6)
        self.assertGreater(anna["pre_v27_raw_pr_elapsed_median_minutes_not_active_time"], 580)
        self.assertFalse(anna["can_infer_active_development_time"])
        feature = next(x for x in summary["comparable_groups"]
                       if x["repo"] == "riccardopinato/Agenda-per-Anna"
                       and x["category"] == "feature")
        self.assertEqual(feature["pre_v27_n"], 7)
        self.assertEqual(feature["pre_v27_nonoverlap_in_sample_n"], 1)
        self.assertFalse(feature["sufficient_matched_samples"])
        self.assertIsNone(feature["descriptive_relative_change_pct"])

    def test_same_pr_cannot_be_double_counted(self):
        altered = copy.deepcopy(self.source)
        altered["records"].append(copy.deepcopy(altered["records"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            m.summarize(altered)

    def test_activation_crossing_cannot_be_labeled_old(self):
        altered = copy.deepcopy(self.source)
        row = next(x for x in altered["records"]
                   if x["cohort"] == "transition_excluded")
        row["cohort"] = "pre_v27"
        with self.assertRaisesRegex(ValueError, "overlaps"):
            m.summarize(altered)

    def test_date_alone_never_certifies_v27(self):
        altered = copy.deepcopy(self.source)
        row = copy.deepcopy(altered["records"][0])
        row.update(pr_number=99998, opened_at="2026-11-01T10:00:00Z",
                   merged_at="2026-11-01T10:20:00Z", cohort="v27_confirmed",
                   factory_baseline_sha=None,
                   url="https://github.com/"+row["repo"]+"/pull/99998")
        altered["records"].append(row)
        with self.assertRaisesRegex(ValueError, "pinned Factory SHA"):
            m.summarize(altered)

    def test_future_evidence_produces_descriptive_comparison_not_causal_proof(self):
        altered = copy.deepcopy(self.source)
        old = next(x for x in altered["records"]
                   if x["repo"] == "riccardopinato/Agenda-per-Anna"
                   and x["category"] == "feature" and x["cohort"] == "pre_v27")
        # Add independent historical fixtures on non-overlapping days.
        # The real Anna feature PRs are mostly a single overlapping open-window episode.
        for i in range(2):
            old_row = copy.deepcopy(old)
            old_row.update(
                pr_number=98001+i,
                opened_at=f"2026-10-{20+i}T10:00:00Z",
                merged_at=f"2026-10-{20+i}T10:30:00Z",
                url=f"https://github.com/{old['repo']}/pull/{98001+i}")
            altered["records"].append(old_row)
        for i in range(3):
            row = copy.deepcopy(old)
            row.update(
                pr_number=99001+i, cohort="v27_confirmed",
                opened_at=f"2026-11-0{i+1}T10:00:00Z",
                merged_at=f"2026-11-0{i+1}T10:20:00Z",
                factory_baseline_sha=PIN,
                baseline_evidence_uri="https://github.com/riccardopinato/App-Factory-Core/blob/main/CURRENT.yaml",
                url=f"https://github.com/{old['repo']}/pull/{99001+i}")
            altered["records"].append(row)
        summary = m.summarize(altered)
        cmp = next(x for x in summary["comparable_groups"] if
                   x["repo"] == old["repo"] and x["category"] == "feature")
        self.assertTrue(cmp["sufficient_matched_samples"])
        self.assertLess(cmp["descriptive_relative_change_pct"], 0)
        self.assertEqual(summary["causal_attribution"], "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
