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

    def test_capability_global_command_routes_to_catalog_sync(self):
        r=resolver.resolve("Capability",load_golden=True)
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("capability-sync",r["modules"])
        self.assertIn("authority-execution",r["modules"])
        self.assertIn("audit-roadmap",r["modules"])
        self.assertIn("single_donor_capability_admission",
                      [g["id"] for g in r["goldens"]])
        self.assertNotIn("factory-policy-sync",r["modules"])

    def test_capability_scoped_and_audit_stay_separate(self):
        scoped=resolver.resolve("Capability Anna's Diary")
        audit=resolver.resolve("Audit")
        self.assertEqual(scoped["selection"],"MODULES",scoped)
        self.assertIn("capability-sync",scoped["modules"])
        self.assertEqual(audit["selection"],"MODULES",audit)
        self.assertNotIn("capability-sync",audit["modules"])

    def test_legend_is_read_only_even_with_capability_context(self):
        r=resolver.resolve("Legenda", "Audit Capability Notes-Ecosistema")
        self.assertEqual(r["selection"], "MODULES", r)
        self.assertIn("command-legend", r["modules"])
        self.assertNotIn("capability-sync", r["modules"])
        self.assertNotIn("audit-roadmap", r["modules"])
        self.assertEqual(r["route_rules"], ["legend"])

    def test_legend_filter_never_dispatches_mentioned_command(self):
        r=resolver.resolve("Legenda Capability", "integra i mock-up")
        self.assertEqual(r["selection"], "MODULES", r)
        self.assertIn("command-legend", r["modules"])
        self.assertNotIn("capability-sync", r["modules"])

    def test_exact_audit_capability_commands_ignore_unsafe_context(self):
        audit=resolver.resolve("Audit", "Capability")
        cap=resolver.resolve("Capability Notes-Ecosistema", "Audit di app")
        self.assertEqual(audit["route_rules"], ["audit"])
        self.assertEqual(cap["route_rules"], ["capability_sync"])

    def test_23_shortcuts_route_one_contract(self):
        reg=json.loads((ROOT/"commands/REGISTRY.json").read_text(encoding="utf-8"))
        new=[c for c in reg["commands"] if c.get("contract_version")==1]
        self.assertEqual(len(new),24)
        for item in new:
            with self.subTest(trigger=item["trigger"]):
                r=resolver.resolve(item["trigger"]+" AnnaDiary","Legenda Capability Audit")
                self.assertEqual(r["selection"],"MODULES",r)
                self.assertEqual(r["route_rules"],[item["route_id"]],r)
                self.assertIn(item["entrypoint"],r["document_paths"])
                if item["route_id"]=="cmd_stelle":
                    self.assertIn("capability-sync",r["modules"])
                else:
                    self.assertNotIn("capability-sync",r["modules"])

    def test_multiword_shortcuts_and_legacy_isolation(self):
        pairs=[("Adotta Factory AnnaDiary","cmd_adotta_factory"),
               ("Deploy AnnaDiary","cmd_deploy"),
               ("Deploy produzione AnnaDiary","cmd_deploy"),
               ("Factory Golden","cmd_factory"),
               ("Nuova app Test","cmd_nuova_app"),
               ("Roadmap Notes","cmd_roadmap"),
               ("Legenda APK","legend"),
               ("Audit Test","audit"),
               ("Capability Test","capability_sync"),
               ("Stelle 95","cmd_stelle"),
               ("Legenda Stelle","legend"),
               ("Mock-up interattivi","mockup_interactive"),
               ("Integra i mock-up","mockup_interactive")]
        for task,rid in pairs:
            with self.subTest(task=task):
                r=resolver.resolve(task,"Capability Audit CI")
                self.assertEqual(r["route_rules"],[rid],r)

    def test_procedi_uses_contextual_roadmap_not_shortcut(self):
        r=resolver.resolve("Procedi con la roadmap","redesign Flutter")
        self.assertNotIn("portfolio-commands",r["modules"])

    def test_unknown_intent_uses_verified_operational_fallback(self):
        r=resolver.resolve("Procedi")
        self.assertEqual(r["selection"],"FALLBACK_BASELINE_USED",r)
        self.assertEqual(r["fallback_path"],MANIFEST["living_fallback"]["path"])

    def test_route_manifest_update_invalidates_full_fallback(self):
        from copy import deepcopy
        revised=deepcopy(MANIFEST)
        revised["task_routes"][0]["terms"].append("a future routing change")
        self.assertNotEqual(builder.render(revised),
                            (ROOT/MANIFEST["living_fallback"]["path"]).read_text(encoding="utf-8"))

    def test_golden_selection_uses_registry(self):
        r=resolver.resolve("redesign schermate",load_golden=True)
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("app_shell_responsive_visual_qa",[g["id"] for g in r["goldens"]])

    def test_pin_keystore_selects_specialized_draft_and_marks_review(self):
        r=resolver.resolve("Verifica PIN Android Keystore",
                           "sicurezza biometria forte",load_golden=True)
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("android_local_pin_verifier_keystore",
                      [g["id"] for g in r["goldens"]])
        self.assertEqual(r["golden_readiness"],"REVIEW_REQUIRED_NOT_CERTIFIED")
        pin=next(g for g in r["goldens"]
                 if g["id"]=="android_local_pin_verifier_keystore")
        self.assertTrue(pin["requires_review"])
        self.assertEqual(pin["freshness_status"],"NEEDS_REVIEW")

    def test_stale_session_pin_blocks(self):
        r=resolver.resolve("redesign schermate",expected_sha="0"*40)
        self.assertEqual(r["selection"],"BLOCKED",r)

    def test_preference_audit_is_read_only_semantically(self):
        r=resolver.resolve("audit del codice")
        self.assertEqual(r["selection"],"MODULES",r)
        self.assertIn("audit-roadmap",r["modules"])
        self.assertNotIn("factory-policy-sync",r["modules"])
        # Router only returns documents; it never grants a mutation authority.
        self.assertTrue(r["active"])

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
