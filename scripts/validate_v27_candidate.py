#!/usr/bin/env python3
"""Structural, fail-closed checks for the non-authoritative v27 modular candidate.

This validates lossless source coverage and fallback identity, NOT model
behavior or runtime speed. The CURRENT resolver remains on v26.8.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "v27/candidate/MODULE_MAP.json"
PATTERN = re.compile(
    r"(?m)^={70}\n(?P<heading>(?P<id>\d+(?:\.\d+)?[A-Z]?)\.?\s+[^\n]+)\n={70}\n"
)
EXPECTED_CHOICES = {
    "DIRECT", "PARALLEL_ELIGIBLE", "CONTROLLED",
    "READ_ONLY", "INVALIDATE_OLD_EVIDENCE",
}


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def split_sections(content: str):
    matches = list(PATTERN.finditer(content))
    if not matches:
        return content, []
    prefix = content[:matches[0].start()]
    pieces = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        pieces.append({
            "id": match.group("id"),
            "heading": match.group("heading"),
            "content": content[match.start():end],
        })
    return prefix, pieces


def safely_read(path: str) -> str:
    target = (ROOT / path).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("unsafe candidate path: " + path)
    return target.read_text(encoding="utf-8")


def validate(manifest: dict, source_bytes: bytes, module_texts: dict,
             core_text: str, current_text: str):
    errors = []
    import yaml
    try:
        current_master=yaml.safe_load(current_text)["master"]
        current_version=str(current_master["version"])
    except (KeyError,TypeError,yaml.YAMLError):
        current_master={}
        current_version="UNVERIFIED"
    if current_version=="26.8":
        if manifest.get("status")!="CANDIDATE_NOT_ACTIVE":
            errors.append("v26.8 CURRENT requires inactive v27 manifest")
        if "v26_8_FULL.txt" not in current_text:
            errors.append("v26.8 current full Master pointer absent")
    elif current_version in ("27","27.0"):
        if manifest.get("status")!="ACTIVE":
            errors.append("v27 CURRENT requires ACTIVE manifest")
        if current_master.get("path")!=manifest.get("core",{}).get("path"):
            errors.append("active master path differs from v27 core")
        if current_master.get("versioned_path")!=manifest.get("living_fallback",{}).get("path"):
            errors.append("active full fallback pointer mismatch")
    else:
        errors.append("unsupported CURRENT version for v27 validator")

    original = manifest.get("original", {})
    fallback = manifest.get("fallback", {})
    expected_blob = original.get("git_blob_sha")
    actual_blob = git_blob_sha(source_bytes)
    if expected_blob != actual_blob:
        errors.append("pinned original source blob identity mismatch")
    if fallback.get("git_blob_sha") != expected_blob:
        errors.append("fallback blob mismatch")
    if fallback.get("path") != original.get("source_path"):
        errors.append("fallback must reuse the existing versioned v26.8 full Master")
    if fallback.get("commit_sha") != original.get("commit_sha"):
        errors.append("fallback commit pin diverged")
    if fallback.get("mode") != "EXACT_PINNED_MASTER":
        errors.append("fallback mode must fail closed on exact identity")
    if "FALLBACK_BASELINE_USED" not in fallback.get("rule", ""):
        errors.append("fallback disclosure marker missing")

    source_text = source_bytes.decode("utf-8")
    prefix, original_parts = split_sections(source_text)
    if manifest.get("original", {}).get("prefix") != prefix:
        errors.append("source prefix mismatch")
    source_by_id = {part["id"]: part for part in original_parts}
    if len(source_by_id) != len(original_parts):
        errors.append("duplicate section in original Master")
    if len(original_parts) != original.get("section_count"):
        errors.append("original section count changed")

    sections = manifest.get("sections", [])
    section_ids = [x.get("id") for x in sections]
    if section_ids != [x["id"] for x in original_parts]:
        errors.append("section inventory missing, duplicate or reordered")
    modules = manifest.get("modules", [])
    declared_mod_ids = [m.get("id") for m in modules]
    declared_paths = [m.get("path") for m in modules]
    if len(declared_mod_ids) != len(set(declared_mod_ids)):
        errors.append("duplicate module IDs")
    if len(declared_paths) != len(set(declared_paths)):
        errors.append("duplicate module paths")
    by_module = {x["id"]: x["module"] for x in sections}
    recovered = {}

    for mod in modules:
        mid, path = mod.get("id"), mod.get("path")
        if not isinstance(path, str) or not path.startswith("v27/candidate/modules/"):
            errors.append("module path outside candidate scope")
            continue
        body = module_texts.get(path)
        if body is None:
            errors.append("missing module: " + path)
            continue
        leading, parts = split_sections(body)
        if leading:
            errors.append("module contains untracked prefix: " + mid)
        found_ids = [part["id"] for part in parts]
        if found_ids != mod.get("section_ids"):
            errors.append("module section ordering/ownership mismatch: " + mid)
        for part in parts:
            sid = part["id"]
            if sid in recovered:
                errors.append("duplicated section across modules: " + sid)
            recovered[sid] = part["content"]
            if sid not in source_by_id:
                errors.append("unknown legacy section: " + sid)
            elif source_by_id[sid]["content"] != part["content"]:
                errors.append("modified original section: " + sid)
            if by_module.get(sid) != mid:
                errors.append("manifest routing mismatch: " + sid)

    if set(recovered) != set(source_by_id):
        errors.append("uncovered or extra original sections")
    if not errors:
        rebuilt = prefix + "".join(recovered[sid] for sid in section_ids)
        if rebuilt.encode("utf-8") != source_bytes:
            errors.append("reconstructed original bytes differ")

    core = manifest.get("core", {})
    if core.get("path") != "v27/candidate/MASTER_CORE_v27_CANDIDATE.txt":
        errors.append("unexpected core entrypoint")
    if len(core_text.splitlines()) > core.get("max_lines", 300):
        errors.append("candidate core exceeds line budget")
    required_tokens=("CURRENT.yaml", "Procedi", "DIRECT", "PARALLEL",
                     "CONTROLLED", "READ", "FALLBACK_BASELINE_USED",
                     "exact-head", "no silent", "source")
    if manifest.get("status")=="CANDIDATE_NOT_ACTIVE":
        required_tokens+=("CANDIDATE",)
    else:
        required_tokens+=("v27",)
    for token in required_tokens:
        if token.casefold() not in core_text.casefold():
            errors.append("core lacks necessary invariant: " + token)

    cases = manifest.get("scenario_tests", [])
    if len(cases) < 5 or len({x.get("id") for x in cases}) != len(cases):
        errors.append("scenario inventory too short or contains duplicates")
    for case in cases:
        if case.get("expected") not in EXPECTED_CHOICES:
            errors.append("invalid scenario outcome")
        if not case.get("trigger") or not case.get("scope"):
            errors.append("scenario missing trigger or scope")
        for mod_id in case.get("modules", []):
            if mod_id not in declared_mod_ids:
                errors.append("scenario selects unknown module: " + mod_id)
    if len(modules) != 8:
        errors.append("unexpected module count")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(safely_read(MANIFEST))
    source = (ROOT / manifest["original"]["source_path"]).read_bytes()
    module_texts = {m["path"]: safely_read(m["path"]) for m in manifest["modules"]}
    core = safely_read(manifest["core"]["path"])
    current = safely_read("CURRENT.yaml")
    errors = validate(manifest, source, module_texts, core, current)
    if errors:
        print("V27 CANDIDATE VALIDATION: FAIL")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    if args.self_test:
        bad_inventory = copy.deepcopy(manifest)
        bad_inventory["sections"].pop()
        if not validate(bad_inventory, source, module_texts, core, current):
            raise SystemExit("negative control failed: missing section accepted")
        bad_fallback = copy.deepcopy(manifest)
        bad_fallback["fallback"]["git_blob_sha"] = "0" * 40
        if not validate(bad_fallback, source, module_texts, core, current):
            raise SystemExit("negative control failed: corrupted fallback accepted")
        bad_module = dict(module_texts)
        first_path = manifest["modules"][0]["path"]
        bad_module[first_path] = bad_module[first_path].replace(
            "SOURCE OF TRUTH", "CHANGED SOURCE", 1
        )
        if not validate(manifest, source, bad_module, core, current):
            raise SystemExit("negative control failed: modified section accepted")
        bad_route = copy.deepcopy(manifest)
        bad_route["scenario_tests"][0]["modules"].append("missing-module")
        if not validate(bad_route, source, module_texts, core, current):
            raise SystemExit("negative control failed: unknown route accepted")

    print("V27 CANDIDATE VALIDATION: PASS "
          f"({len(manifest['sections'])} sections, "
          f"{len(manifest['modules'])} modules, exact pinned v26.8 fallback; "
          f"negative controls {'PASS' if args.self_test else 'not run'}).")


if __name__ == "__main__":
    main()
