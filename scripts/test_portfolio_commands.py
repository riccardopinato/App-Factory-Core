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
    def test_generic_roadmap_not_a_public_command(self):
        r=router.resolve("Procedi con la roadmap","redesign Flutter")
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertNotIn("portfolio-commands",r["modules"])
        self.assertIn("audit-roadmap",r["modules"])

    def test_tampered_command_spec_blocks(self):
        import tempfile, shutil
        m=json.loads((ROOT/"v27/candidate/MODULE_MAP.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            needed=["CURRENT.yaml","v27/candidate/MODULE_MAP.json",
                    m["core"]["path"],m["living_fallback"]["path"],
                    "commands/REGISTRY.json","commands/specs/APK.md"]
            needed += [x["path"] for x in m["modules"]]
            needed += [x["path"] for x in m.get("policy_updates",[])]
            for path in needed:
                dst=root/path
                dst.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/path,dst)
            dst=root/"commands/specs/APK.md"
            dst.write_text(dst.read_text(encoding="utf-8")+"\\nDRIFT",encoding="utf-8")
            r=router.resolve("APK AnnaDiary",root=root)
            self.assertEqual(r["selection"],"BLOCKED_COMMAND_SPEC_UNAVAILABLE",r)
    def test_legenda_never_dispatches_listed_commands(self):
        for name in ("Test","APK","Ripara","Nuova app","CI"):
            self.assertEqual(router.resolve("Legenda "+name)["route_rules"],["legend"])
if __name__=="__main__":
    unittest.main(verbosity=2)
