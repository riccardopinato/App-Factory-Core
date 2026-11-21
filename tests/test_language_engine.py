"""Deterministic tests: no network, no model, no source mutation."""
from __future__ import annotations
import importlib.util
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "language_engine_v1", ROOT / "reference_engines/language_engine/language_engine.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sample():
    return {
        "schemaVersion": 1, "adapter": "cooking_anime", "privacy": "PUBLIC_EDITORIAL",
        "sourceLocale": "it", "targetLocales": ["en", "fr"],
        "records": [{
            "id": "recipe_000080",
            "source": {"steps": {"first": "Cuoci per 74 °C con {ingredient}.",
                                 "second": "Mescola il miso."}},
            "translations": {
                "en": {"steps": {"first": "Cook to 74 °C with {ingredient}."}},
                "fr": {"steps": {"first": "Cuire à 74 °C avec {ingredient}.",
                                 "second": "Mélangez le miso."}},
            },
        }],
    }


class LanguageEngineTests(unittest.TestCase):
    def test_holds_missing_translation_and_prepares_only_drafts(self):
        data = sample()
        drafts = sample()
        drafts["records"][0]["translations"]["en"]["steps"]["second"] = "Mix the miso."
        report = module.run(data, drafts=drafts)
        self.assertEqual(report["comparisons"], 2)
        self.assertEqual(report["states"]["HOLD"], 1)
        row = next(x for x in report["results"] if x["locale"] == "en")
        self.assertEqual(row["proposals"][0]["origin"], "MACHINE_DRAFT")
        self.assertEqual(row["proposals"][0]["status"], "REVIEW_REQUIRED")
        self.assertFalse(report["publicationAuthorized"])
        self.assertEqual(report["providerCalls"], 0)

    def test_approved_memory_source_fingerprint_required(self):
        data = sample()
        original = data["records"][0]["source"]["steps"]["second"]
        mem = {"entries": [{
            "status": "approved", "sourceText": original, "targetText": "Mix the miso.",
            "sourceSha256": module.fingerprint(original),
            "domain": "cooking_anime", "sourceLocale": "it", "targetLocale": "en",
        }]}
        row = module.run(data, memory=mem)["results"][0]
        self.assertEqual(row["proposals"][0]["origin"], "APPROVED_MEMORY")
        mem["entries"][0]["sourceSha256"] = "wrong"
        with self.assertRaises(ValueError):
            module.run(data, memory=mem)

    def test_placeholder_mismatch_holds_and_number_difference_review(self):
        data = sample()
        data["records"][0]["translations"]["en"]["steps"]["first"] = "Cook to 70 °C with the ingredient."
        result = module.run(data)
        codes = {i["code"] for i in result["results"][0]["issues"]}
        self.assertIn("PLACEHOLDER_DRIFT", codes)
        self.assertIn("NUMBER_ANCHOR_REVIEW", codes)

    def test_glossary_review_scoped_by_domain(self):
        data = sample()
        terms = {"entries": [{
            "domain": "cooking_anime", "source": "miso",
            "targets": {"fr": "miso spécial"},
        }]}
        out = module.run(data, glossary=terms)
        fr = next(x for x in out["results"] if x["locale"] == "fr")
        self.assertIn("GLOSSARY_TERM_REVIEW", {i["code"] for i in fr["issues"]})

    def test_rejects_mismatched_drafts_and_duplicate_ids(self):
        data = sample()
        wrong = sample()
        wrong["targetLocales"] = ["de"]
        with self.assertRaises(ValueError):
            module.run(data, drafts=wrong)
        data["records"].append(data["records"][0])
        with self.assertRaises(ValueError):
            module.run(data)

    def test_batch_lane_identity_preserved(self):
        data = sample()
        original = data["records"][0]
        data["records"] = [{**original, "id": f"r-{i}"} for i in range(201)]
        out = module.run(data, max_records_per_lane=100)
        self.assertEqual(out["laneCount"], 3)
        self.assertEqual({r["lane"] for r in out["results"]}, {0, 1, 2})
        self.assertEqual(out["sourceRecords"], 201)
        self.assertEqual(out["comparisons"], 402)


if __name__ == "__main__":
    unittest.main()
