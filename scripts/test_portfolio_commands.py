#!/usr/bin/env python3
"""Offline regression test for portfolio command routing."""
import json
import unittest
from pathlib import Path
import resolve_v27_candidate as router
ROOT=Path(__file__).resolve().parents[1]
REG=json.loads((ROOT/"commands/REGISTRY.json").read_text(encoding="utf-8"))
class PortfolioTests(unittest.TestCase):
    def test_all_26_stay_isolated(self):
        new=[x for x in REG["commands"] if x.get("contract_version")==1]
        self.assertEqual(len(new),26)
        for x in new:
            with self.subTest(name=x["trigger"]):
                r=router.resolve(x["trigger"],"Legenda Audit Capability")
                self.assertEqual(r["selection"],"MODULES",r)
                self.assertEqual(r["route_rules"],[x["route_id"]])
    def test_avanti_and_avanti_roadmap_longest_prefix(self):
        for task, route, spec in (
            ("Avanti", "cmd_avanti", "commands/specs/AVANTI.md"),
            ("Avanti AnnaDiary", "cmd_avanti", "commands/specs/AVANTI.md"),
            ("Avanti roadmap", "cmd_avanti_roadmap", "commands/specs/AVANTI_ROADMAP.md"),
            ("Avanti roadmap AnnaDiary", "cmd_avanti_roadmap", "commands/specs/AVANTI_ROADMAP.md"),
        ):
            with self.subTest(task=task):
                r=router.resolve(task, "Prossimo Audit Riprendi Avanti roadmap")
                self.assertEqual(r["selection"], "MODULES", r)
                self.assertEqual(r["route_rules"], [route], r)
                self.assertIn(spec, r["document_paths"])
                self.assertIn("authority-execution", r["modules"])
        for consult in ("Legenda Avanti", "Legenda Avanti roadmap",
                        "Prossimo", "Riprendi"):
            with self.subTest(consult=consult):
                r=router.resolve(consult, "Avanti roadmap AnnaDiary")
                self.assertNotIn("cmd_avanti", r["route_rules"], r)
                self.assertNotIn("cmd_avanti_roadmap", r["route_rules"], r)

    def test_web_deploy_routes_explicitly_and_not_to_apk(self):
        for task in ("Deploy", "Deploy Anna's Diary", "Deploy anteprima Anna's Diary",
                     "Deploy produzione Anna's Diary"):
            with self.subTest(task=task):
                result=router.resolve(task,"APK CI Play Store")
                self.assertEqual(result["selection"],"MODULES",result)
                self.assertEqual(result["route_rules"],["cmd_deploy"],result)
                self.assertIn("commands/specs/DEPLOY.md",result["document_paths"])
                self.assertNotIn("cmd_apk",result["route_rules"])

    def test_corrupt_deploy_contract_is_blocked(self):
        import tempfile, shutil
        m=json.loads((ROOT/"v27/candidate/MODULE_MAP.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            paths=["CURRENT.yaml","v27/candidate/MODULE_MAP.json",
                   m["core"]["path"],m["living_fallback"]["path"],
                   "commands/REGISTRY.json","commands/specs/DEPLOY.md"]
            paths += [x["path"] for x in m["modules"]]
            paths += [x["path"] for x in m["policy_updates"]]
            for path in paths:
                dst=root/path
                dst.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/path,dst)
            target=root/"commands/specs/DEPLOY.md"
            target.write_text(target.read_text(encoding="utf-8")+"\\nTAMPER",encoding="utf-8")
            r=router.resolve("Deploy produzione AnnaDiary",root=root)
            self.assertEqual(r["selection"],"BLOCKED_COMMAND_SPEC_UNAVAILABLE",r)

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
        for name in ("Test","APK","Deploy","Ripara","Nuova app","CI"):
            self.assertEqual(router.resolve("Legenda "+name)["route_rules"],["legend"])
if __name__=="__main__":
    unittest.main(verbosity=2)
