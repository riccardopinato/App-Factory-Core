#!/usr/bin/env python3
"""Static contract regression gate for the App Factory Audit operator.

This checks documented instructions, sealed command routing, and 14 contract
scenarios. It does NOT evaluate an LLM, Android runtime, or product correctness.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "audit/MASTER_AUDIT_360_APP_FACTORY_v1.txt"
ACTION_PATH = ROOT / "audit/AUDIT_OPERATOR_EFFICIENCY_ACTION_PACK_v1.txt"
REGISTRY_PATH = ROOT / "commands/REGISTRY.json"

# Contract coverage, not behavioral claims. Three archetypes are grounded in
# repository snapshots referenced in the Action Pack.
CONTRACT_SCENARIOS = {
    "T01_green_pr_unmerged": ("Non confondere un'idea, una PR", "AUDIT_ONLY"),
    "T02_readme_vs_runtime": ("runtime", "Un PASS su un livello non promuove gli altri"),
    "T03_static_false_positive": ("Sospetto != bug", "falsi positivi"),
    "T04_unconfirmed_high_risk": ("P0", "rischi residui"),
    "T05_personal_noncommercial_app": ("Business N/A", "non fare"),
    "T06_duplicate_issue": ("issue duplicate", "anti-duplicazione"),
    "T07_anna_sync_and_vault": ("sync", "privacy", "lifecycle"),
    "T08_omni_media_delete": ("DELETE & ENTITY LIFECYCLE", "cancellazione"),
    "T09_unavailable_repository": ("Se una fonte non è disponibile", "non verificati"),
    "T10_head_moved": ("invalidation triggers", "ri-verificare"),
    "T11_apk_not_certified": ("Un PASS su un livello non promuove gli altri", "release"),
    "T12_untrusted_repository_instructions": ("TRUST BOUNDARY DELLE FONTI", "DATI DA ISPEZIONARE"),
    "T13_draft_golden_not_certified": ("Draft solo come reference", "CERTIFICATI e pertinenti"),
    "T14_repeatability_fixed_sha": ("riproducibilita", "SHA", "stabilità"),
}

class AuditOperatorContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = SPEC_PATH.read_bytes()
        cls.spec = cls.raw.decode("utf-8")
        cls.action = ACTION_PATH.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        cls.all_text = cls.spec + "\n" + cls.action

    def test_canonical_safety_and_read_only(self):
        audit = next((x for x in self.registry["commands"] if x["id"] == "audit"), None)
        self.assertIsNotNone(audit)
        self.assertEqual(audit["trigger"], "Audit")
        self.assertEqual(audit["effect"], "SOLA LETTURA")
        self.assertEqual(audit["entrypoint"], "audit/MASTER_AUDIT_360_APP_FACTORY_v1.txt")
        self.assertEqual(audit["route_id"], "audit")
        git_blob = hashlib.sha1(b"blob " + str(len(self.raw)).encode() + b"\0" + self.raw).hexdigest()
        self.assertEqual(audit["spec_blob_sha"], git_blob, "SHA seal must bind the exact new Audit spec")
        for marker in ("AUDIT_ONLY", "SOLA LETTURA", "Solo comando di implementazione separato"):
            self.assertIn(marker.casefold(), self.spec.casefold())
        self.assertNotIn("auto-eseguire in modalita' Audit", self.spec.casefold())  # forbidden behavior is only mentioned in Action Pack

    def test_legacy_sections_and_reporting_not_lost(self):
        for n in range(24):
            with self.subTest(section=n):
                self.assertRegex(self.spec, rf"(?m)^## {n}\\. ")
        self.assertIn("## 19-bis.", self.spec)
        for letter in "ABCDEFGHIJKLMNOPQR":
            with self.subTest(report=letter):
                self.assertRegex(self.spec, rf"(?m)^{letter}\\. \\*\\*")

    def test_efficiency_handoff_and_boundary(self):
        for marker in (
            "audit differenziale", "Pass 0", "Pass 6", "Execution Pack",
            "invalidation triggers", "NON FARE", "FIX MINIMO",
            "TRUST BOUNDARY DELLE FONTI", "Nessuna nuova API/cloud/AI onerosa",
            "Un PASS su un livello non promuove gli altri",
            "REPORT", "SOLA LETTURA",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker.casefold(), self.all_text.casefold())

    def test_no_artificial_fixed_five_steps(self):
        self.assertNotIn("le priorità e i 5 maxi-step", self.spec)
        self.assertNotIn("e i 5 maxi-step", self.spec)
        self.assertNotIn("Genera 5–15 opportunità", self.spec)
        self.assertIn("fino a 5 maxi-step", self.spec)

    def test_14_contract_scenarios(self):
        for case_id, markers in CONTRACT_SCENARIOS.items():
            with self.subTest(case=case_id):
                for marker in markers:
                    self.assertIn(marker.casefold(), self.all_text.casefold(), f"{case_id}: {marker}")

    def test_pilot_provenance_and_limitations(self):
        for marker in (
            "Anna\'s Diary", "Android Omni Cleaner", "World Days",
            "7f6a60ff883b664574e3b7404aea12295d5a392b",
            "e2959f4680e1c3c6c40720d72d1c1262287c1925",
            "6820b1d1ff1bf8268c41e2b43f124c952a9ecb42",
            "nessun runtime", "NON rivendicata", "STATIC CONTRACT TESTS",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker.casefold(), self.action.casefold())

if __name__ == "__main__":
    unittest.main(verbosity=2)
