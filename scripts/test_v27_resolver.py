#!/usr/bin/env python3
"""v27C resolver safety and synchronization checks, no external services."""
from __future__ import annotations
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import resolve_v27_candidate as resolver
import build_v27_fallback as builder

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((ROOT/"v27/candidate/MODULE_MAP.json").read_text(encoding="utf-8"))

class RouterTests(unittest.TestCase):
    def test_modular_ui_and_roadmap(self):
        r=resolver.resolve("Procedi con la roadmap", "redesign delle schermate Flutter")
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("experience",r["modules"])
        self.assertIn("audit-roadmap",r["modules"])
        self.assertNotIn("monetization-ai",r["modules"])
        self.assertLess(r["loaded_bytes"], (ROOT/MANIFEST["living_fallback"]["path"]).stat().st_size)

    def test_continuation_always_loads_full_parallel_authority(self):
        r=resolver.resolve("Procedi con la roadmap",
                           "redesign schermate Oggi Calendario Ricordi")
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("authority-execution",r["modules"])
        self.assertIn("experience",r["modules"])
        self.assertIn("audit-roadmap",r["modules"])

    def test_repository_name_alone_is_not_a_task(self):
        r=resolver.resolve("AppLab")
        self.assertEqual(r["selection"],"FALLBACK_BASELINE_USED",r)

    def test_master_update_routes_to_policy(self):
        r=resolver.resolve("aggiorna App Factory Core","regole del Master Prompt")
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("factory-policy-sync",r["modules"])

    def test_unknown_intent_uses_verified_operational_fallback(self):
        r=resolver.resolve("Procedi")
        self.assertEqual(r["selection"],"FALLBACK_BASELINE_USED",r)
        self.assertEqual(r["fallback_path"],MANIFEST["living_fallback"]["path"])

    def test_golden_selection_uses_registry(self):
        r=resolver.resolve("redesign schermate",load_golden=True)
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("app_shell_responsive_visual_qa",[g["id"] for g in r["goldens"]])

    def test_stale_session_pin_blocks(self):
        r=resolver.resolve("redesign schermate",expected_sha="0"*40)
        self.assertEqual(r["selection"],"BLOCKED",r)

    def test_preference_audit_is_read_only_semantically(self):
        r=resolver.resolve("audit del codice")
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("audit-roadmap",r["modules"])
        self.assertNotIn("factory-policy-sync",r["modules"])
        # Router only returns documents; it never grants a mutation authority.
        self.assertFalse(r["active"])

    def test_selected_module_corruption_fallback_and_bad_fallback_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            paths=["CURRENT.yaml","v27/candidate/MODULE_MAP.json",
                   MANIFEST["core"]["path"],
                   MANIFEST["living_fallback"]["path"],
                   *[x["path"] for x in MANIFEST["modules"]],
                   *[x["path"] for x in MANIFEST.get("policy_updates",[])]]
            for path in paths:
                target=root/path
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/path,target)
            selected=root/"v27/candidate/modules/40-experience.txt"
            selected.write_bytes(selected.read_bytes()+b"\nDRIFT")
            r=resolver.resolve("redesign schermate",root=root)
            self.assertEqual(r["selection"],"FALLBACK_BASELINE_USED",r)
            fallback=root/MANIFEST["living_fallback"]["path"]
            fallback.write_bytes(fallback.read_bytes()+b"\nDRIFT")
            r=resolver.resolve("redesign schermate",root=root)
            self.assertEqual(r["selection"],"BLOCKED_FACTORY_BASELINE_UNVERIFIED",r)

    def test_generator_exact_and_drift_sensitive(self):
        self.assertEqual(
            builder.render(MANIFEST),
            (ROOT/MANIFEST["living_fallback"]["path"]).read_text(encoding="utf-8")
        )
        self.assertEqual(builder.hash_bytes(builder.render(MANIFEST).encode()),
                         MANIFEST["living_fallback"]["git_blob_sha"])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            paths=[MANIFEST["core"]["path"],
                   *[x["path"] for x in MANIFEST["modules"]],
                   *[x["path"] for x in MANIFEST.get("policy_updates",[])]]
            for path in paths:
                target=root/path
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/path,target)
            old=builder.ROOT
            try:
                builder.ROOT=root
                policy=root/"v27/candidate/modules/80-factory-policy-sync.txt"
                policy.write_text(policy.read_text(encoding="utf-8")+"\nFuture rule",encoding="utf-8")
                self.assertNotEqual(builder.render(MANIFEST),
                                    (ROOT/MANIFEST["living_fallback"]["path"]).read_text())
            finally:
                builder.ROOT=old

if __name__=="__main__":
    unittest.main(verbosity=2)
