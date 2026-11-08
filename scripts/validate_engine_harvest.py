#!/usr/bin/env python3
"""Check Golden engine harvest artifacts and portable consumer test-vector shape.

This deliberately does NOT run donor Dart implementations or certify a consumer.
Actual behavioral acceptance requires an adapter in each app plus exact-head CI.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
NEW = {
    "gpx_interoperability_engine": "golden/data/GOLDEN_GPX_INTEROPERABILITY_ENGINE_v1_DRAFT.txt",
    "hybrid_local_search_engine": "golden/data/GOLDEN_HYBRID_LOCAL_SEARCH_ENGINE_v1_DRAFT.txt",
    "civil_date_recurrence_engine": "golden/data/GOLDEN_CIVIL_DATE_RECURRENCE_ENGINE_v1.txt",
    "local_rules_automation_engine": "golden/data/GOLDEN_LOCAL_RULES_AUTOMATION_ENGINE_v1_DRAFT.txt",
    "infinite_canvas_ink_engine": "golden/ui/GOLDEN_INFINITE_CANVAS_INK_ENGINE_v1_DRAFT.txt",
    "spatial_clustering_engine": "golden/data/GOLDEN_SPATIAL_CLUSTERING_ENGINE_v1_DRAFT.txt",
    "explainable_recommendation_engine": "golden/data/GOLDEN_EXPLAINABLE_RECOMMENDATION_ENGINE_v1_DRAFT.txt",
    "performance_regression_fixtures": "golden/governance/GOLDEN_PERFORMANCE_REGRESSION_FIXTURES_v1_DRAFT.txt",
}
UPDATED = {
    "golden/data/GOLDEN_IMPORT_EXPORT_PORTABILITY_FLUTTER_v1_DRAFT.txt": "INTEGRAZIONE 03/11/2026",
    "golden/data/GOLDEN_OFFLINE_CONTENT_PACKS_FLUTTER_v1_DRAFT.txt": "INTEGRAZIONE 03/11/2026",
    "golden/data/GOLDEN_BACKUP_RECOVERY_FLUTTER_v1_DRAFT.txt": "INTEGRAZIONE 03/11/2026",
    "golden/data/GOLDEN_VERSIONED_EDITORIAL_CATALOG_FLUTTER_v1_DRAFT.txt": "INTEGRAZIONE 03/11/2026",
    "golden/data/GOLDEN_INCREMENTAL_PERSISTENT_INDEXING_v1_DRAFT.txt": "INTEGRAZIONE 03/11/2026",
    "golden/governance/GOLDEN_SINGLE_DONOR_CAPABILITY_ADMISSION_v1.txt": "E3 EXECUTION RECIPE",
    "golden/release/GOLDEN_IMMUTABLE_BUILD_TEST_ARTIFACT_v1.txt": "EXACT SOURCE TEST-WORKFLOW",
}
CORE_VECTORS = set(list(NEW)[:4])


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise AssertionError(reason)


def main() -> None:
    registry = yaml.safe_load((ROOT / "golden/GOLDEN_REGISTRY.yaml").read_text(encoding="utf-8"))
    current = yaml.safe_load((ROOT / "CURRENT.yaml").read_text(encoding="utf-8"))
    index = (ROOT / "golden/GOLDEN_INDEX_CURRENT.txt").read_text(encoding="utf-8")
    index_version = current["golden_index"]["version"]
    require(index_version >= 28, "Golden Index older than engine harvest baseline v28")
    require(registry["index_version"] == index_version, "Golden Registry vs CURRENT index drift")
    registered = {entry["id"]: entry for entry in registry["goldens"]}
    require(len(registered) == len(registry["goldens"]), "duplicate registry IDs")
    require(len(registered) >= 59, "engine harvest baseline must retain all 59 legacy Goldens")
    scoped_e5 = {
        "hybrid_local_search_ephemeral_scoped": "golden/data/GOLDEN_HYBRID_LOCAL_SEARCH_EPHEMERAL_CORE_v1.txt",
        "gpx_read_only_preview_scoped": "golden/data/GOLDEN_GPX_READ_ONLY_PREVIEW_CORE_v1.txt",
    }
    if index_version >= 29:
        for ident, rel in scoped_e5.items():
            require(ident in registered, "missing scoped E5 Golden: " + ident)
            item = registered[ident]
            require(item["status"] == "CERTIFIED GOLDEN" and item["path"] == rel,
                    "scoped E5 registry mismatch: " + ident)
            doc = (ROOT / rel).read_text(encoding="utf8")
            require("E5" in doc and "INDEPENDENT" in doc.upper() and "NOT CERTIFIED" in doc.upper() or
                    "E5" in doc and "Independent consumer" in doc and "NOT" in doc,
                    "scoped Golden must state evidence and negative boundary: " + ident)
        require(len(registered) == 61, "v29 scoped index must have 61 Goldens")
    else:
        require(len(registered) == 59, "v28 legacy Golden count drift")
    for ident, rel in NEW.items():
        require(ident in registered, "unregistered engine: " + ident)
        entry = registered[ident]
        require(entry["path"] == rel, "wrong path: " + ident)
        if ident == "civil_date_recurrence_engine":
            require(entry["status"].startswith("COPY-READY GOLDEN"), "consumer pilot missing: " + ident)
        else:
            require(entry["status"].startswith("DRAFT /"), "unearned certification: " + ident)
        doc = (ROOT / rel).read_text(encoding="utf-8")
        require("DONOR SOURCE (PINNED)" in doc, "missing provenance: " + ident)
        require(re.search(r"@[0-9a-f]{40}", doc) is not None, "missing original SHA: " + ident)
        require("test/" in doc, "missing source test path: " + ident)
        require("CONSUMER TEST MATRIX" in doc or "TEST MATRIX" in doc, "missing consumer gates: " + ident)
        require("END GOLDEN" in doc, "unclosed contract: " + ident)
        require(rel.split("/")[-1] in index, "missing index entry: " + ident)
    for rel, marker in UPDATED.items():
        doc = (ROOT / rel).read_text(encoding="utf-8")
        require(marker in doc, "missing donor consolidation: " + rel)
    fixture = json.loads((ROOT / "contracts/engine_reuse_acceptance_v1.json").read_text(encoding="utf-8"))
    require(fixture["schemaVersion"] == 1, "wrong fixture schema")
    require(fixture["status"] == "CONSUMER_ACCEPTANCE_VECTORS_NOT_IMPLEMENTATION_TESTS",
            "fixtures may not claim runtime correctness")
    vectors = fixture["contracts"]
    require({v["id"] for v in vectors} == CORE_VECTORS, "wrong fixture contract set")
    seen = set()
    count = 0
    for contract in vectors:
        cases = contract["cases"]
        require(len(cases) >= 5, "too few cases: " + contract["id"])
        require(any(c["kind"] == "reject" for c in cases) or (contract["id"] == "civil_date_recurrence_engine" and any(c["expected"].get("resolved") is False for c in cases)), "missing reject or unresolved case: " + contract["id"])
        for case in cases:
            case_id = case["id"]
            require(case_id not in seen, "duplicate case ID: " + case_id)
            seen.add(case_id)
            require(case["kind"] in ("success", "reject"), "unsupported kind: " + case_id)
            require(isinstance(case["input"], dict) and isinstance(case["expected"], dict),
                    "invalid test vector: " + case_id)
            require(bool(case["expected"]), "missing expected results: " + case_id)
            count += 1
    reference_verified = {
        "hybrid_local_search_engine": "reference_engines/lib/src/hybrid_search.dart",
        "local_rules_automation_engine": "reference_engines/lib/src/local_rules.dart",
        "explainable_recommendation_engine": "reference_engines/lib/src/explainable_recommendation.dart",
        "spatial_clustering_engine": "reference_engines/lib/src/spatial_clustering.dart",
    }
    for ident, path in reference_verified.items():
        entry = registered[ident]
        require("REFERENCE IMPLEMENTED" in entry["status"],
                "reference evidence not reflected in registry: " + ident)
        require((ROOT / path).is_file(), "reference implementation missing: " + path)
        require("REFERENCE IMPLEMENTATION / TEST EVIDENCE" in (ROOT / NEW[ident]).read_text(),
                "reference evidence missing in Golden: " + ident)
    partial_reference_verified = {
        "infinite_canvas_ink_engine": "reference_engines/lib/src/canvas_ink.dart",
        "performance_regression_fixtures": "reference_engines/lib/src/performance_fixtures.dart",
    }
    for ident, path in partial_reference_verified.items():
        entry = registered[ident]
        require("IMPLEMENTED" in entry["status"],
                "reference implementation status stale: " + ident)
        require((ROOT / path).is_file(), "missing reference module: " + path)
        require("PARTIAL REFERENCE" in (ROOT / NEW[ident]).read_text(),
                "missing scoped partial certification: " + ident)
    for source in ("reference_engines/lib/src/gpx.dart",
                   "reference_engines/lib/src/civil_date.dart",
                   "reference_engines/test/acceptance_vectors_test.dart"):
        require((ROOT / source).is_file(), "missing reference source: " + source)
    print(f"GOLDEN ENGINE CONTRACT SHAPE: PASS ({len(NEW)} specs, "
          f"{len(UPDATED)} extensions, {count} portable acceptance vectors)")
    print("IMPORTANT: structural/fixture validation only; not consumer Dart runtime tests.")


if __name__ == "__main__":
    main()
