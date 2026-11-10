"""Contract and negative test vectors; does not simulate app installation."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_template_engine_v1.py"
spec = importlib.util.spec_from_file_location("template_validator", SCRIPT)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
NOTE = json.loads((ROOT / "contracts" / "template_engine_v1" / "examples" / "notes_reading_library.json").read_text(encoding="utf-8"))
ANNA = json.loads((ROOT / "contracts" / "template_engine_v1" / "examples" / "anna_morning_ritual.json").read_text(encoding="utf-8"))


class TemplateEngineV1ContractTests(unittest.TestCase):
    def test_valid_two_consumer_examples(self):
        self.assertEqual([], mod.validate_examples())
        self.assertEqual([], mod.validate_manifest(NOTE))
        self.assertEqual([], mod.validate_manifest(ANNA))

    def reject(self, source, update, marker):
        manifest = copy.deepcopy(source)
        update(manifest)
        self.assertTrue(any(marker in e for e in mod.validate_manifest(manifest)),
                        f"Expected {marker}, got {mod.validate_manifest(manifest)}")

    def test_four_original_pack_manifests_remain_research_only(self):
        candidates = {
            "notes_project_launch_studio_research.json": (
                "riccardopinato/Notes-Ecosistema",
                "it.riccardopinato.notes.project_launch_studio",
            ),
            "notes_study_sprint_studio_research.json": (
                "riccardopinato/Notes-Ecosistema",
                "it.riccardopinato.notes.study_sprint_studio",
            ),
            "anna_memory_atlas_research.json": (
                "riccardopinato/Agenda-per-Anna",
                "it.riccardopinato.anna.memory_chapters",
            ),
            "anna_twelve_week_reflection_research.json": (
                "riccardopinato/Agenda-per-Anna",
                "it.riccardopinato.anna.twelve_week_reflection",
            ),
        }
        for filename, (app_id, template_id) in candidates.items():
            with self.subTest(filename=filename):
                candidate = json.loads(
                    (ROOT / "contracts" / "template_engine_v1" / "examples" / filename)
                    .read_text(encoding="utf-8")
                )
                self.assertEqual([], mod.validate_manifest(candidate))
                self.assertEqual(candidate["app_id"], app_id)
                self.assertEqual(candidate["template_id"], template_id)
                self.assertEqual(candidate["catalog_status"], "research_candidate")
                self.assertEqual(candidate["access"]["tier"], "paid_once")
                self.assertIn("entitlement_key", candidate["access"])
                self.assertEqual(candidate["installation"]["scope"], "private")
                self.assertTrue(candidate["installation"]["confirmation_required"])
                self.assertEqual(
                    candidate["installation"]["removal_policy"],
                    "detach_keep_user_data",
                )
                self.assertFalse(candidate["provenance"]["external_assets_embedded"])
                self.assertEqual(
                    candidate["provenance"]["rights_status"],
                    "first_party_pending_review",
                )

    def test_invalid_contract_and_identity(self):
        self.reject(NOTE, lambda x: x.update(contract_version=2), "contract_version")
        self.reject(NOTE, lambda x: x.update(template_id="../../example"), "template_id")
        self.reject(NOTE, lambda x: x.update(template_version="1.latest"), "template_version")
        self.reject(NOTE, lambda x: x.update(app_id="other/account"), "app_id")

    def test_cross_app_locales_are_exhaustive(self):
        self.reject(NOTE, lambda x: x["localization"]["translations"].pop("de"), "translations must match")
        self.reject(NOTE, lambda x: x["localization"].update(default_locale="nl"), "missing from translations")

    def test_incompatible_build_range(self):
        self.reject(NOTE, lambda x: x["compatibility"].update(max_app_build=0), "max_app_build")
        self.reject(NOTE, lambda x: x["compatibility"].update(max_app_build=0), "below min_app_build")

    def test_no_untrusted_preview_assets_or_remote_paths(self):
        self.reject(NOTE, lambda x: x["preview"].update(asset_path="https://example.com/img.png"), "preview")
        self.reject(NOTE, lambda x: x["preview"].update(kind="bundled_original", asset_path="../secret.png", sha256="b"*64), "safe relative")
        self.reject(NOTE, lambda x: x["preview"].update(kind="bundled_original", asset_path="assets/original.png"), "sha256")
        self.reject(NOTE, lambda x: x["preview"].update(kind="bundled_original", asset_path="C:\\secret.png", sha256="a"*64), "safe relative")

    def test_no_executable_payload_or_external_assets(self):
        self.reject(NOTE, lambda x: x.update(script="rm -rf"), "script")
        self.reject(NOTE, lambda x: x["provenance"].update(external_assets_embedded=True), "external_assets_embedded")
        self.reject(NOTE, lambda x: x["installation"].update(strategy="execute_sql"), "strategy")
        self.reject(NOTE, lambda x: x["installation"].update(removal_policy="purge_user_data"), "removal_policy")

    def test_payment_gate_requires_logical_entitlement(self):
        self.reject(ANNA, lambda x: x["access"].pop("entitlement_key"), "entitlement_key")
        self.reject(NOTE, lambda x: x["access"].update(entitlement_key="notes.some.paid"), "free template")

    def test_configuration_is_bounded(self):
        self.reject(NOTE, lambda x: x["configuration"]["fields"].append(copy.deepcopy(x["configuration"]["fields"][0])), "duplicate keys")
        self.reject(NOTE, lambda x: x["configuration"]["fields"][1].update(default="unknown"), "choice default")
        self.reject(ANNA, lambda x: x["configuration"]["fields"][1].update(default=12), "default outside bounds")
        self.reject(ANNA, lambda x: x["configuration"]["fields"][0].update(default="true"), "boolean default")
        self.reject(ANNA, lambda x: x["configuration"]["fields"][1].update(min=9), "min greater than max")

    def test_shared_install_is_explicit_and_confirmed(self):
        self.reject(ANNA, lambda x: x["installation"].update(scope="shared_automatic"), "scope")
        self.reject(ANNA, lambda x: x["installation"].update(confirmation_required=False), "confirmation_required")
        self.reject(ANNA, lambda x: x["installation"].update(replay_policy="repeat_every_time"), "replay_policy")

    def test_unapproved_status_cannot_claim_store_ready(self):
        self.reject(NOTE, lambda x: x.update(catalog_status="store_ready"), "catalog_status")
        self.reject(NOTE, lambda x: x["access"].update(price_eur=3.99), "price_eur")


if __name__ == "__main__":
    unittest.main()
