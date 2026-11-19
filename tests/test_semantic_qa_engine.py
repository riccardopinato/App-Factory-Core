#!/usr/bin/env python3
"""Offline test vectors: never use API, network, secrets or mutable app data."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "reference_engines/semantic_qa/semantic_qa.py"
spec = importlib.util.spec_from_file_location("semantic_qa_engine", PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)

def fixture():
    return {
        "schemaVersion": 1, "adapter": "cooking_anime", "privacy": "PUBLIC_EDITORIAL",
        "sourceLocale": "it", "targetLocales": ["en", "es"],
        "domainRubric": "Do not reverse safety and cooking instructions.",
        "records": [
            {"id": "recipe_000059", "protectedTerms": ["Sake"],
             "source": {"title": "Vongole al sake",
                        "steps": {"one": "Cuoci 4 minuti con 100 ml di sake."}},
             "translations": {
                "en": {"title": "Sake clams",
                       "steps": {"one": "Cook for 4 minutes with 100 ml sake."}},
                "es": {"title": "Almejas al sake",
                       "steps": {"one": "Cocina 4 minutos con 100 ml de sake."}}}},
            {"id": "recipe_000153", "protectedTerms": [],
             "source": {"title": "Polpette di pollo",
                        "steps": {"one": "Raggiungi 74 °C al cuore."}},
             "translations": {
                 "en": {"title": "Chicken meatballs",
                        "steps": {"one": "Reach 70 °C in the center."}},
                 "es": {"title": "Albóndigas de pollo",
                        "steps": {"one": "Alcanza 74 °C en el centro."}},
             }},
        ],
    }

class OfflineSemanticTests(unittest.TestCase):
    def test_coverage_and_determinism(self):
        sample = fixture()
        a = mod.audit(sample, workers=1)
        b = mod.audit(sample, workers=4, batch_size=1)
        self.assertEqual(a["comparisonCount"], 4)
        self.assertEqual([(x["id"], x["locale"], x["state"]) for x in a["results"]],
                         [(x["id"], x["locale"], x["state"]) for x in b["results"]])
        self.assertEqual(a["semanticModelActuallyUsed"], False)
        self.assertEqual(a["certification"], "NOT_CERTIFIED")
        self.assertTrue(all("OFFLINE" in x["reviewType"] for x in a["results"]))

    def test_numeric_semantic_drift_is_review_not_false_certification(self):
        a = mod.audit(fixture())
        row = next(x for x in a["results"] if x["id"] == "recipe_000153"
                   and x["locale"] == "en")
        self.assertTrue(any(i["code"] == "NUMERIC_ANCHOR_DRIFT"
                            for i in row["findings"]))
        self.assertEqual(row["state"], "OFFLINE_REVIEW_REQUIRED")

    def test_missing_locale_is_hold(self):
        data = fixture()
        del data["records"][0]["translations"]["es"]
        row = mod.audit(data)["results"][1]
        self.assertEqual(row["state"], "HOLD")

    def test_changed_source_and_target_invalidates_cache(self):
        data = fixture()
        cache = {}
        first = mod.audit(data, cache=cache)
        self.assertEqual(first["cachedComparisons"], 0)
        second = mod.audit(data, cache=cache)
        self.assertEqual(second["cachedComparisons"], 4)
        data["records"][0]["source"]["steps"]["one"] += " Mantieni caldo."
        third = mod.audit(data, cache=cache)
        self.assertEqual(third["cachedComparisons"], 2)
        data["records"][1]["translations"]["en"]["title"] += " grilled"
        fourth = mod.audit(data, cache=cache)
        self.assertEqual(fourth["cachedComparisons"], 3)

    def test_no_external_without_approval(self):
        data = fixture()
        for allow in (False, True):
            with patch.dict("os.environ", {"OPENAI_API_KEY": ""}):
                with self.assertRaises(ValueError):
                    mod.audit(data, provider="openai", model="review-model",
                              allow_external=allow)
        private = fixture()
        private["privacy"] = "PRIVATE"
        with patch.dict("os.environ", {"OPENAI_API_KEY": "fake"}):
            with self.assertRaises(ValueError):
                mod.audit(private, provider="openai", model="review-model",
                          allow_external=True)

    def test_opt_in_model_verdict_and_second_independent_pass(self):
        data = fixture()
        with patch.dict("os.environ", {"OPENAI_API_KEY": "fake"}):
            with patch.object(mod, "openai_review", side_effect=[
                    {"verdict": "PASS", "issues": []},
                    {"verdict": "HOLD", "issues": []},
                    {"verdict": "PASS", "issues": []},
                    {"verdict": "PASS", "issues": []},
                    {"verdict": "PASS", "issues": []},
                    {"verdict": "PASS", "issues": []},
                    {"verdict": "PASS", "issues": []},
                    {"verdict": "PASS", "issues": []},
                 ]) as review:
                out = mod.audit(data, provider="openai", model="fake",
                                allow_external=True, second_pass=True, workers=1)
                self.assertEqual(review.call_count, 8)
                self.assertEqual(out["comparisonCount"], 4)
                self.assertTrue(any(x["state"] == "AI_REVIEW_HOLD" for x in out["results"]))

    def test_invalid_ids_no_silent_dedup(self):
        data = fixture()
        data["records"][1]["id"] = data["records"][0]["id"]
        with self.assertRaises(ValueError):
            mod.audit(data)

    def test_cli_report_cache_no_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            incoming, result, cache = (folder / n for n in
                                        ("in.json", "out.json", "cache.json"))
            incoming.write_text(json.dumps(fixture()), encoding="utf-8")
            import subprocess, sys
            for run in range(2):
                subprocess.run([sys.executable, str(PATH), "--input", str(incoming),
                                "--report", str(result), "--cache", str(cache),
                                "--workers", "3"], check=True, capture_output=True)
                recorded = json.loads(result.read_text(encoding="utf-8"))
                self.assertEqual(recorded["cachedComparisons"], 0 if run == 0 else 4)


if __name__ == "__main__":
    unittest.main()
