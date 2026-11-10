#!/usr/bin/env python3
"""Real active-v27 routing fixtures; offline tests, NO model/API calls."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import resolve_v27_candidate as router

ROOT=Path(__file__).resolve().parents[1]
CORE=json.loads((ROOT/"v27/candidate/MODULE_MAP.json").read_text(encoding="utf-8"))


class ActiveCommandTests(unittest.TestCase):
    def test_current_v27_is_active(self):
        r=router.resolve("Avanti roadmap Anna's Diary", "approved current roadmap")
        self.assertTrue(r["active"])
        self.assertEqual(r["selection"],"MODULES")
        self.assertEqual(r["route_rules"],["cmd_avanti_roadmap"])
        self.assertIn("commands/specs/AVANTI_ROADMAP.md",r["document_paths"])

    def test_audit_capability_contracts_are_loaded(self):
        for task, route, source in (
            ("Audit Anna's Diary","audit","audit/MASTER_AUDIT_360_APP_FACTORY_v1.txt"),
            ("Capability Notes-Ecosistema","capability_sync","capability/MASTER_CAPABILITY_SYNC_v1.txt"),
            ("Legenda Test","legend","commands/specs/LEGENDA.md"),
            ("Mock-up interattivi","mockup_interactive","v27/candidate/modules/81-interactive-mockup-review.txt"),
            ("Integra i mock-up","mockup_integration","v27/candidate/modules/81-interactive-mockup-review.txt"),
        ):
            with self.subTest(task=task):
                r=router.resolve(task,"Avanti Roadmap Capability")
                self.assertEqual(r["selection"],"MODULES",r)
                self.assertEqual(r["route_rules"],[route],r)
                self.assertIn(source,r["document_paths"])

    def test_corrupted_legacy_spec_is_blocked(self):
        import tempfile, shutil
        manifest=CORE
        for task, source in (
            ("Audit", "audit/MASTER_AUDIT_360_APP_FACTORY_v1.txt"),
            ("Capability", "capability/MASTER_CAPABILITY_SYNC_v1.txt"),
            ("Legenda", "commands/specs/LEGENDA.md"),
        ):
            with self.subTest(task=task), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp)
                paths=["CURRENT.yaml","v27/candidate/MODULE_MAP.json",
                       manifest["core"]["path"], manifest["living_fallback"]["path"],
                       "commands/REGISTRY.json", source]
                paths += [m["path"] for m in manifest["modules"]]
                paths += [m["path"] for m in manifest["policy_updates"]]
                for p in paths:
                    d=root/p
                    d.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copyfile(ROOT/p,d)
                damaged=root/source
                damaged.write_bytes(damaged.read_bytes()+b"\\nTAMPER")
                result=router.resolve(task,root=root)
                self.assertEqual(result["selection"],"BLOCKED_COMMAND_SPEC_UNAVAILABLE",result)

    def test_integration_never_inherits_readonly_mockup_lane(self):
        r=router.resolve("Integra i mock-up","APPROVED designs")
        self.assertEqual(r["route_rules"],["mockup_integration"])
        self.assertIn("authority-execution",r["modules"])

    def test_context_does_not_dispatch_other_shortcuts(self):
        r=router.resolve("Audit","Avanti roadmap, Capability, Integra i mock-up")
        self.assertEqual(r["route_rules"],["audit"])
        r=router.resolve("Legenda Audit","Avanti roadmap")
        self.assertEqual(r["route_rules"],["legend"])

    def test_bare_procedi_still_uses_verified_fallback(self):
        self.assertEqual(router.resolve("Procedi")["selection"],"FALLBACK_BASELINE_USED")

    def test_ambiguous_source_errors_never_promote(self):
        self.assertNotIn("cmd_avanti_roadmap",router.resolve("Prossimo","Avanti roadmap")["route_rules"])


if __name__=="__main__":
    unittest.main(verbosity=2)
