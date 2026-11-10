#!/usr/bin/env python3
"""Offline negative and positive controls for the command legend registry."""
from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path
import build_command_legend as legend

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "commands/REGISTRY.json").read_text(encoding="utf-8"))
M = json.loads((ROOT / "v27/candidate/MODULE_MAP.json").read_text(encoding="utf-8"))

class LegendTests(unittest.TestCase):
    def test_generated_view_and_route_coverage(self):
        self.assertTrue(legend.validate(R, M))
        rendered = legend.render(R, M)
        self.assertEqual(rendered, (ROOT / "commands/LEGGENDA.md").read_text(encoding="utf-8"))
        for phrase in ("Legenda", "Audit tutte le app", "Capability priorità", "Stelle 95",
                       "Capability Notes-Ecosistema", "Procedi", "Mock-up interattivi",
                       "Avanti", "Avanti roadmap"):
            self.assertIn(phrase, rendered)
    def test_22_approved_commands_and_pins(self):
        approved=("Stato","Prossimo","Allinea","Roadmap","Backlog","Riprendi",
                  "Golden","Donor","Factory","Adotta Factory","Nuova app",
                  "CI","Test","Ripara","APK","Store","Peso","Sicurezza",
                  "UX","Monetizzazione","Mercato","Idee","Deploy",
                  "Avanti","Avanti roadmap")
        self.assertEqual(len(R["commands"]),32)
        for name in approved:
            with self.subTest(name=name):
                item=next(x for x in R["commands"] if x["trigger"]==name)
                self.assertEqual(item["contract_version"],1)
                self.assertEqual(len(item["spec_blob_sha"]),40)

    def test_apk_and_deploy_share_section_but_not_contract(self):
        apk=next(x for x in R["commands"] if x["id"]=="apk")
        deploy=next(x for x in R["commands"] if x["id"]=="deploy")
        self.assertEqual(apk["group"], "APK e Deploy")
        self.assertEqual(deploy["group"], "APK e Deploy")
        self.assertNotEqual(apk["entrypoint"], deploy["entrypoint"])
        self.assertNotEqual(apk["route_id"], deploy["route_id"])
        self.assertIn("### APK e Deploy", legend.render(R, M))
        self.assertIn("Deploy produzione Anna's Diary", legend.render(R, M))

    def test_corrupt_contract_hash_rejected(self):
        broken=copy.deepcopy(R)
        item=next(x for x in broken["commands"] if x["id"]=="apk")
        item["spec_blob_sha"]="0"*40
        with self.assertRaises(ValueError):
            legend.validate(broken,M)

    def test_duplicate_public_command_rejected(self):
        bad = copy.deepcopy(R)
        bad["commands"].append(copy.deepcopy(bad["commands"][0]))
        with self.assertRaises(ValueError):
            legend.validate(bad, M)
    def test_unlisted_future_public_route_rejected(self):
        bad = copy.deepcopy(M)
        bad["task_routes"].append({"id":"future_public","terms":["future public"],
                                   "modules":["command-legend"],"public_command":True})
        with self.assertRaises(ValueError):
            legend.validate(R, bad)
    def test_missing_entrypoint_rejected(self):
        bad = copy.deepcopy(R)
        bad["commands"][0]["entrypoint"] = "commands/DOES_NOT_EXIST.md"
        with self.assertRaises(ValueError):
            legend.validate(bad, M)
    def test_nonpublic_router_rejected(self):
        bad = copy.deepcopy(R)
        bad["commands"][0]["route_id"] = "roadmap"
        with self.assertRaises(ValueError):
            legend.validate(bad, M)

if __name__ == "__main__":
    unittest.main(verbosity=2)
