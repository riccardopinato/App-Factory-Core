#!/usr/bin/env python3
"""Offline regression test for portfolio command routing."""
import json
import unittest
from pathlib import Path
import resolve_v27_candidate as router
ROOT=Path(__file__).resolve().parents[1]
REG=json.loads((ROOT/"commands/REGISTRY.json").read_text(encoding="utf-8"))
class PortfolioTests(unittest.TestCase):
    def test_all_22_stay_isolated(self):
        new=[x for x in REG["commands"] if x.get("contract_version")==1]
        self.assertEqual(len(new),22)
        for x in new:
            with self.subTest(name=x["trigger"]):
                r=router.resolve(x["trigger"],"Legenda Audit Capability")
                self.assertEqual(r["selection"],"MODULES",r)
                self.assertEqual(r["route_rules"],[x["route_id"]])
    def test_legenda_never_dispatches_listed_commands(self):
        for name in ("Test","APK","Ripara","Nuova app","CI"):
            self.assertEqual(router.resolve("Legenda "+name)["route_rules"],["legend"])
if __name__=="__main__":
    unittest.main(verbosity=2)
