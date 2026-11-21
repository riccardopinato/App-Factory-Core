#!/usr/bin/env python3
"""Language Engine v1: deterministic Fast Track localization memory + QA preflight.

No network, model or source mutations. Translation models (for example an
authoring-time MarianMT adapter) provide draft candidates separately.
Even approved translation-memory hits need consumer-specific publication gates.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ENGINE_VERSION = "1.0.0"
PLACEHOLDER = re.compile(r"\{[a-zA-Z_][\w.]*\}|%\d*\$?[sd]|\$\{[^{}]+\}")
NUMBER = re.compile(r"(?<![\w])\d+(?:[.,]\d+)?")
PRIVATE = {"PRIVATE", "PERSONAL", "SENSITIVE", "HEALTH"}


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def flatten(data: object, prefix: str = "") -> dict[str, str]:
    if isinstance(data, dict):
        result = {}
        for key, value in sorted(data.items()):
            if not isinstance(key, str):
                raise ValueError("String object keys required")
            path = f"{prefix}.{key}" if prefix else key
            result.update(flatten(value, path))
        return result
    if isinstance(data, list):
        result = {}
        for index, value in enumerate(data):
            result.update(flatten(value, f"{prefix}[{index}]"))
        return result
    if data is None:
        return {prefix: ""}
    if not isinstance(data, (str, int, float, bool)):
        raise ValueError("Unsupported translatable value")
    return {prefix: str(data)}


def _anchor_mismatch(a: str, b: str) -> bool:
    # Nonblocking: translations may spell numbers out or convert units.
    aa = Counter(match.group().replace(",", ".") for match in NUMBER.finditer(a))
    bb = Counter(match.group().replace(",", ".") for match in NUMBER.finditer(b))
    return bool(aa) and aa != bb


def _validate_record_set(source: dict) -> None:
    if source.get("schemaVersion") != 1:
        raise ValueError("Unsupported normalized data schema")
    if not isinstance(source.get("records"), list):
        raise ValueError("Missing records")
    locales = source.get("targetLocales")
    if not isinstance(locales, list) or not locales or len(set(locales)) != len(locales):
        raise ValueError("targetLocales must be a nonempty unique list")
    if source.get("sourceLocale") in locales:
        raise ValueError("sourceLocale must be outside targetLocales")
    if not isinstance(source.get("adapter"), str) or not source["adapter"]:
        raise ValueError("adapter is required")
    seen = set()
    for item in source["records"]:
        rid = item.get("id")
        if not isinstance(rid, str) or not rid or rid in seen:
            raise ValueError("Missing or duplicate canonical record ID")
        seen.add(rid)
        if not isinstance(item.get("source"), dict):
            raise ValueError(f"{rid}: source missing")
        if not isinstance(item.get("translations", {}), dict):
            raise ValueError(f"{rid}: translations must be an object")


def _approved_memory_index(memory: dict) -> dict[tuple, dict]:
    result = {}
    for row in memory.get("entries", []):
        if row.get("status") != "approved":
            continue
        text = row.get("sourceText")
        translated = row.get("targetText")
        if not isinstance(text, str) or not text or not isinstance(translated, str) or not translated.strip():
            raise ValueError("Approved memory entry must have nonempty source/target")
        if row.get("sourceSha256") != fingerprint(text):
            raise ValueError("Stale or missing approved memory fingerprint")
        key = (row.get("domain"), row.get("sourceLocale"), row.get("targetLocale"), text)
        if key in result and result[key]["targetText"] != translated:
            raise ValueError("Conflicting approved memory entries")
        result[key] = row
    return result


def run(
    data: dict,
    *,
    memory: dict | None = None,
    glossary: dict | None = None,
    drafts: dict | None = None,
    semantic_report: dict | None = None,
    max_records_per_lane: int = 100,
) -> dict:
    _validate_record_set(data)
    if max_records_per_lane < 1 or max_records_per_lane > 100:
        raise ValueError("Fast Track lanes must be 1..100 IDs")
    memory_index = _approved_memory_index(memory or {})
    glossary_rows = (glossary or {}).get("entries", [])
    if not isinstance(glossary_rows, list):
        raise ValueError("glossary entries must be a list")
    if drafts:
        _validate_record_set(drafts)
        if (drafts["adapter"], drafts["sourceLocale"], drafts["targetLocales"]) != (
            data["adapter"], data["sourceLocale"], data["targetLocales"]
        ):
            raise ValueError("Drafts do not match source adapter/locales")
    draft_index = {r["id"]: r for r in drafts["records"]} if drafts else {}
    semantic = {}
    if semantic_report:
        if semantic_report.get("adapter") != data["adapter"]:
            raise ValueError("Semantic report adapter mismatch")
        if semantic_report.get("certification") != "NOT_CERTIFIED":
            raise ValueError("Unrecognized semantic report certification")
        semantic = {(r["id"], r["locale"]): r for r in semantic_report.get("results", [])}

    domain = data["adapter"]
    rows = []
    counts = Counter()
    for index, item in enumerate(data["records"]):
        rid = item["id"]
        sources = flatten(item["source"])
        for locale in data["targetLocales"]:
            translated = flatten(item.get("translations", {}).get(locale, {}))
            draft = flatten(draft_index.get(rid, {}).get("translations", {}).get(locale, {}))
            proposals = []
            issues = []
            for key, original in sources.items():
                target = translated.get(key, "")
                if not original.strip():
                    continue
                if not target.strip():
                    mem = memory_index.get((domain, data["sourceLocale"], locale, original))
                    candidate = mem["targetText"] if mem else draft.get(key, "")
                    origin = "APPROVED_MEMORY" if mem else "MACHINE_DRAFT" if candidate else "MISSING"
                    proposals.append({
                        "field": key, "sourceSha256": fingerprint(original),
                        "candidate": candidate, "origin": origin,
                        "status": "REVIEW_REQUIRED" if candidate else "NEEDS_TRANSLATION",
                    })
                    issues.append({"code": "MISSING_TRANSLATION", "field": key, "severity": "HOLD"})
                    continue
                if sorted(PLACEHOLDER.findall(original)) != sorted(PLACEHOLDER.findall(target)):
                    issues.append({"code": "PLACEHOLDER_DRIFT", "field": key, "severity": "HOLD"})
                if _anchor_mismatch(original, target):
                    issues.append({"code": "NUMBER_ANCHOR_REVIEW", "field": key, "severity": "REVIEW"})
                for term in glossary_rows:
                    if term.get("domain") not in (None, domain):
                        continue
                    source_term = term.get("source")
                    expected = term.get("targets", {}).get(locale)
                    if (isinstance(source_term, str) and isinstance(expected, str)
                            and source_term.casefold() in original.casefold()
                            and expected.casefold() not in target.casefold()):
                        issues.append({
                            "code": "GLOSSARY_TERM_REVIEW", "field": key,
                            "severity": "REVIEW", "term": source_term, "expected": expected,
                        })
            for key in translated.keys() - sources.keys():
                issues.append({"code": "EXTRA_TRANSLATION_FIELD", "field": key, "severity": "REVIEW"})
            witness = semantic.get((rid, locale))
            if witness and witness.get("state") in ("HOLD", "AI_REVIEW_HOLD"):
                issues.append({"code": "SEMANTIC_HOLD", "field": "*", "severity": "HOLD"})
            if any(it["severity"] == "HOLD" for it in issues):
                state = "HOLD"
            elif issues or proposals:
                state = "REVIEW"
            else:
                state = "OFFLINE_REVIEW_REQUIRED"
            counts[state] += 1
            rows.append({
                "id": rid, "locale": locale,
                "lane": index // max_records_per_lane,
                "state": state,
                "semanticReviewType": witness.get("reviewType", "NOT_RUN") if witness else "NOT_RUN",
                "proposals": proposals, "issues": issues,
            })
    return {
        "engine": "app_factory_language_engine",
        "version": ENGINE_VERSION,
        "adapter": domain,
        "sourceLocale": data["sourceLocale"],
        "targetLocales": data["targetLocales"],
        "sourceRecords": len(data["records"]),
        "comparisons": len(rows),
        "laneCount": (len(data["records"]) + max_records_per_lane - 1) // max_records_per_lane,
        "states": dict(sorted(counts.items())),
        "privacy": data.get("privacy", "UNSPECIFIED"),
        "providerCalls": 0,
        "mode": "OFFLINE_MEMORY_AND_QA",
        "publicationAuthorized": False,
        "certification": "NOT_CERTIFIED",
        "results": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Source-locked Language Engine / Fast Track preflight")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--memory", type=Path)
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--drafts", type=Path)
    parser.add_argument("--semantic-report", type=Path)
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()
    read = lambda p: json.loads(p.read_text(encoding="utf-8")) if p else None
    output = run(
        read(args.input),
        memory=read(args.memory),
        glossary=read(args.glossary),
        drafts=read(args.drafts),
        semantic_report=read(args.semantic_report),
        max_records_per_lane=args.batch_size,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "engine": output["engine"], "comparisons": output["comparisons"],
        "states": output["states"], "providerCalls": 0, "certification": "NOT_CERTIFIED",
    }, ensure_ascii=False))
    return 2 if output["states"].get("HOLD") else 0


if __name__ == "__main__":
    raise SystemExit(main())
