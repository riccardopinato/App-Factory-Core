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


    def test_safe_numerical_normalizations_and_real_mismatch(self):
        good = module.numeric_difference(
            "Cuoci 4 uova a 74 °C.", "Cook four eggs to 74 °C (165 °F).", "it", "en")
        self.assertEqual(good, (False, True, False))
        self.assertEqual(module.numeric_difference(
            "Cuoci a 74 °C.", "Cook to 165 °F.", "it", "en")[0], False)
        self.assertTrue(module.numeric_difference(
            "Cuoci a 74 °C.", "Cook to 70 °C (165 °F).", "it", "en")[0])
        self.assertTrue(module.numeric_difference(
            "Gira di 90°.", "Turn a quarter of a turn.", "it", "en")[0])

    def test_units_need_review_even_when_cardinal_values_match(self):
        self.assertEqual(module.numeric_difference(
            "Cuoci 4 minuti.", "Cook for 4 hours.", "it", "en"), (False, False, True))
        self.assertEqual(module.numeric_difference(
            "Cuoci 4 minuti.", "Cook for 4 minutes.", "it", "en"), (False, False, False))
        self.assertEqual(module.numeric_difference(
            "Taglia 4–5 mm.", "Slice 4–5 mm.", "it", "en"), (False, False, False))

    def test_stale_draft_and_stale_semantic_evidence_rejected(self):
        data = sample()
        draft = sample()
        draft["records"][0]["source"]["steps"]["first"] = "Wrong original."
        with self.assertRaisesRegex(ValueError, "Stale draft"):
            module.run(data, drafts=draft)
        rows = [
            {"id": "recipe_000080", "locale": lang, "state": "OFFLINE_REVIEW_REQUIRED",
             "reviewType": "OFFLINE_ONLY"} for lang in ("en", "fr")
        ]
        report = {"adapter": "cooking_anime", "sourceLocale": "it",
                  "targetLocales": ["en", "fr"], "recordCount": 1,
                  "comparisonCount": 2, "certification": "NOT_CERTIFIED",
                  "inputFingerprint": module.stable_hash(data), "results": rows}
        self.assertEqual(module.run(data, semantic_report=report)["comparisons"], 2)
        report["results"] = rows[:1]
        with self.assertRaises(ValueError):
            module.run(data, semantic_report=report)
        report["results"] = rows + rows[:1]
        with self.assertRaises(ValueError):
            module.run(data, semantic_report=report)
        report["results"] = rows
        data["records"][0]["source"]["steps"]["first"] = "Changed canonical!"
        with self.assertRaisesRegex(ValueError, "Stale/unbound"):
            module.run(data, semantic_report=report)

    def test_compound_units_and_frequency_idioms(self):
        self.assertEqual(module.numeric_difference(
            "Giralo una o due volte e lascia 4–6 minuti.",
            "Turn once or twice and allow 4–6 minutes.", "it", "en"),
            (False, True, False))
        self.assertEqual(module.unit_anchors(
            "Fodera uno stampo da 18 cm e monta per 8–10 minuti.", "it"),
            module.unit_anchors(
                "Prepare an 18-cm pan and beat for 8–10 minutes.", "en"))
        self.assertEqual(module.unit_anchors(
            "Cuoci in una teglia da 28 cm", "it"),
            module.unit_anchors(
                "Bake in a 28-cm-Form", "de"))

    def test_numeric_findings_include_priority_and_source_evidence(self):
        data = sample()
        data["records"][0]["source"]["ingredients"] = {"flour": {"name": "Farina 00"}}
        data["records"][0]["translations"]["en"]["ingredients"] = {
            "flour": {"name": "Plain flour"}}
        data["records"][0]["translations"]["fr"]["ingredients"] = {
            "flour": {"name": "Farine ordinaire"}}
        result = module.run(data)
        en = next(r for r in result["results"] if r["locale"] == "en")
        grade = next(i for i in en["issues"] if i["code"] == "INGREDIENT_CLASSIFICATION_REVIEW")
        self.assertEqual(grade["priority"], "P2")
        self.assertEqual(grade["sourceEvidence"], "Farina 00")
        self.assertTrue(result["triageIssuePriorities"].get("P2", 0) >= 1)
        self.assertEqual(result["certification"], "NOT_CERTIFIED")

if __name__ == "__main__":
    unittest.main()
