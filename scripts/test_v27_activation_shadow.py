#!/usr/bin/env python3
"""Offline v27E shadow activation compatibility tests (without switching CURRENT).

Never writes the production repository. Simulates the version-27 CURRENT
contract in an isolated temporary copy; actual v27 promotion is NOT performed.
"""
from __future__ import annotations
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import yaml
import resolve_v27_candidate as resolver

ROOT=Path(__file__).resolve().parents[1]
MANIFEST_PATH="v27/candidate/MODULE_MAP.json"

def make_shadow(tmp: str)->Path:
    root=Path(tmp)
    manifest=json.loads((ROOT/MANIFEST_PATH).read_text(encoding="utf-8"))
    paths=[
        manifest["core"]["path"],manifest["living_fallback"]["path"],
        *[x["path"] for x in manifest["modules"]],
        *[x["path"] for x in manifest["policy_updates"]],
    ]
    for path in paths:
        dest=root/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/path,dest)
    current=yaml.safe_load((ROOT/"CURRENT.yaml").read_text(encoding="utf-8"))
    current["master"].update(
        version="27",path=manifest["core"]["path"],
        versioned_path=manifest["living_fallback"]["path"],
        modular_manifest=MANIFEST_PATH
    )
    (root/"CURRENT.yaml").write_text(yaml.safe_dump(current,sort_keys=False),
                                     encoding="utf-8")
    manifest["status"]="ACTIVE"
    dest=root/MANIFEST_PATH
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",
                    encoding="utf-8")
    registry=yaml.safe_load((ROOT/"golden/GOLDEN_REGISTRY.yaml").read_text(encoding="utf-8"))
    registry["master_version"]="27"
    goldens=root/"golden/GOLDEN_REGISTRY.yaml"
    goldens.parent.mkdir(parents=True,exist_ok=True)
    goldens.write_text(yaml.safe_dump(registry,sort_keys=False,allow_unicode=True),
                       encoding="utf-8")
    for entry in registry["goldens"]:
        if entry["id"] in ("app_shell_responsive_visual_qa","roadmap_fast_continuous_maintenance"):
            loc=root/entry["path"]
            loc.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/entry["path"],loc)
    return root

class ActivationShadowTests(unittest.TestCase):
    def test_current_v27_schema_accepts_shadow_and_rejects_wrong_paths(self):
        from jsonschema import Draft202012Validator
        schema=json.loads((ROOT/"schemas/current.schema.json").read_text(encoding="utf-8"))
        validator=Draft202012Validator(schema)
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            active=yaml.safe_load((root/"CURRENT.yaml").read_text(encoding="utf-8"))
            # Match validate_factory.py's YAML date->ISO string normalization.
            active=json.loads(json.dumps(active,default=str))
            self.assertFalse(list(validator.iter_errors(active)),"v27 shadow schema invalid")
            active["master"]["path"]="master/MASTER_PROMPT_CURRENT.txt"
            self.assertTrue(list(validator.iter_errors(active)),
                            "unsafe v27 core path passed schema")

    def test_active_candidate_structural_validation(self):
        import validate_v27_candidate as structure
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            manifest=json.loads((root/MANIFEST_PATH).read_text(encoding="utf-8"))
            source=(ROOT/manifest["original"]["source_path"]).read_bytes()
            docs={m["path"]:(root/m["path"]).read_text(encoding="utf-8")
                  for m in manifest["modules"]}
            core=(root/manifest["core"]["path"]).read_text(encoding="utf-8")
            current=(root/"CURRENT.yaml").read_text(encoding="utf-8")
            self.assertEqual(structure.validate(manifest,source,docs,core,current),[])

    def test_release_branch_current_selects_v27(self):
        data=yaml.safe_load((ROOT/"CURRENT.yaml").read_text(encoding="utf-8"))
        self.assertEqual(str(data["master"]["version"]),"27")

    def test_shadow_is_active_and_loads_minimal_context(self):
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            r=resolver.resolve("Procedi con la roadmap",
                               "redesign schermate",root=root,load_golden=True)
            self.assertEqual(r["selection"],"MODULES",r)
            self.assertTrue(r["active"])
            self.assertIn("authority-execution",r["modules"])
            self.assertIn("experience",r["modules"])
            self.assertIn("app_shell_responsive_visual_qa",
                          [g["id"] for g in r["goldens"]])

    def test_active_ambiguous_uses_verified_living_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            r=resolver.resolve("Procedi",root=root)
            self.assertTrue(r["active"])
            self.assertEqual(r["selection"],"FALLBACK_BASELINE_USED",r)

    def test_missing_module_falls_back_but_corrupt_full_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            mod=root/"v27/candidate/modules/40-experience.txt"
            mod.write_bytes(mod.read_bytes()+b"\nCORRUPTED")
            r=resolver.resolve("redesign schermate",root=root)
            self.assertEqual(r["selection"],"FALLBACK_BASELINE_USED",r)
            fb=root/"v27/candidate/MASTER_FULL_FALLBACK_GENERATED.txt"
            fb.write_bytes(fb.read_bytes()+b"\nCORRUPTED")
            r=resolver.resolve("redesign schermate",root=root)
            self.assertEqual(r["selection"],"BLOCKED_FACTORY_BASELINE_UNVERIFIED",r)

    def test_shadow_wrong_core_or_manifest_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            p=root/"CURRENT.yaml"
            current=yaml.safe_load(p.read_text(encoding="utf-8"))
            current["master"]["path"]="master/MASTER_PROMPT_CURRENT.txt"
            p.write_text(yaml.safe_dump(current,sort_keys=False),encoding="utf-8")
            r=resolver.resolve("redesign schermate",root=root)
            self.assertEqual(r["selection"],"BLOCKED",r)

    def test_cannot_activate_candidate_manifest_implicitly(self):
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            p=root/MANIFEST_PATH
            manifest=json.loads(p.read_text(encoding="utf-8"))
            manifest["status"]="CANDIDATE_NOT_ACTIVE"
            p.write_text(json.dumps(manifest),encoding="utf-8")
            r=resolver.resolve("redesign schermate",root=root)
            self.assertEqual(r["selection"],"BLOCKED",r)

    def test_legacy_registry_cannot_validate_v27_golden(self):
        with tempfile.TemporaryDirectory() as d:
            root=make_shadow(d)
            p=root/"golden/GOLDEN_REGISTRY.yaml"
            registry=yaml.safe_load(p.read_text(encoding="utf-8"))
            registry["master_version"]="26.8"
            p.write_text(yaml.safe_dump(registry,sort_keys=False),encoding="utf-8")
            r=resolver.resolve("redesign schermate",load_golden=True,root=root)
            self.assertEqual(r["selection"],"FALLBACK_BASELINE_USED",r)

if __name__=="__main__":
    unittest.main(verbosity=2)
