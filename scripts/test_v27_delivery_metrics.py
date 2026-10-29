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

    def test_real_historical_source_is_consistent_and_not_attributed_to_v27(self):
        summary = m.summarize(self.source)
        self.assertGreaterEqual(summary["cohorts"]["pre_v27"]["n"], 30)
        self.assertEqual(summary["cohorts"]["v27_confirmed"]["n"] if
                         "v27_confirmed" in summary["cohorts"] else 0, 0)
        self.assertEqual(summary["causal_attribution"], "NOT_VERIFIED")
        self.assertTrue(all(not r["sufficient_matched_samples"] for r in
                            summary["comparable_groups"]))

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
