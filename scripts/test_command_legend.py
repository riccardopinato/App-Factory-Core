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
        for phrase in ("Legenda", "Audit tutte le app", "Capability priorità",
                       "Capability Notes-Ecosistema", "Procedi", "Mock-up interattivi"):
            self.assertIn(phrase, rendered)
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
