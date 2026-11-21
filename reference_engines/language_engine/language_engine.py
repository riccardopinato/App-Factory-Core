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
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import re

ENGINE_VERSION = "1.1.2"
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


# Written numeric words 2..10 only. Articles are ambiguous, so remain REVIEW.
CARDINALS = {
    "it": "due tre quattro cinque sei sette otto nove dieci",
    "en": "two three four five six seven eight nine ten",
    "es": "dos tres cuatro cinco seis siete ocho nueve diez",
    "fr": "deux trois quatre cinq six sept huit neuf dix",
    "de": "zwei drei vier fünf sechs sieben acht neun zehn",
    "pt": "dois três quatro cinco seis sete oito nove dez",
}
CARDINALS = {locale: {word: i for i, word in enumerate(words.split(), 2)}
             for locale, words in CARDINALS.items()}
CARDINALS["pt"]["duas"] = 2
CARDINALS["pt-br"] = CARDINALS["pt"]
WORDS = re.compile(r"\b[^\W\d_]+\b", re.UNICODE)
TEMPERATURES = re.compile(r"(?<!\w)(\d+(?:[.,]\d+)?)\s*°\s*([cCfF])\b")
UNITS = re.compile(
    r"(?<!\w)(\d+(?:[.,]\d+)?)\s*(?:[-‑–]\s*)?"
    r"(mm|cm|kg|mg|g|ml|litri?|liters?|litres?|"
    r"minuti?|minutes?|minutos?|minuten|mins?|"
    r"ore|hours?|horas?|heures?|stunden?)\b", re.IGNORECASE)
UNIT_MAP = {
    "mm": ("distance_mm", 1), "cm": ("distance_mm", 10),
    "mg": ("mass_g", Decimal("0.001")), "g": ("mass_g", 1),
    "kg": ("mass_g", 1000), "ml": ("volume_ml", 1),
    "litri": ("volume_ml", 1000), "liters": ("volume_ml", 1000),
    "litres": ("volume_ml", 1000), "liter": ("volume_ml", 1000),
    "litre": ("volume_ml", 1000),
    "min": ("duration_s", 60), "mins": ("duration_s", 60),
    "minuto": ("duration_s", 60), "minuti": ("duration_s", 60),
    "minute": ("duration_s", 60), "minutes": ("duration_s", 60),
    "minutos": ("duration_s", 60), "minuten": ("duration_s", 60),
    "ore": ("duration_s", 3600),
    "hour": ("duration_s", 3600), "hours": ("duration_s", 3600),
    "horas": ("duration_s", 3600),
    "heures": ("duration_s", 3600), "stunden": ("duration_s", 3600),
}


def stable_hash(value: object) -> str:
    """Same JSON contract as Semantic QA's stable_hash()."""
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _decimal(value: str) -> Decimal:
    return Decimal(value.replace(",", "."))


def _number(value: Decimal) -> str:
    return format(value.normalize(), "f")


def _render_spelled(text: str, locale: str) -> str:
    # Only explicit frequency idioms (not general article-to-one rewriting).
    # 'Una o due volte' and 'once or twice' are equivalent counts.
    frequency = {
        "it": [(r"\buna?\s+o\s+due\s+volte\b", "1 o 2 volte")],
        "en": [(r"\bonce\s+or\s+twice\b", "1 or 2")],
        "es": [(r"\buna\s+o\s+dos\s+veces\b", "1 o 2 veces")],
        "fr": [(r"\bune\s+ou\s+deux\s+fois\b", "1 ou 2 fois")],
        "de": [(r"\beinmal\s+oder\s+zweimal\b", "1 oder 2 mal")],
        "pt": [(r"\buma\s+ou\s+duas\s+vezes\b", "1 ou 2 vezes")],
        "pt-br": [(r"\buma\s+ou\s+duas\s+vezes\b", "1 ou 2 vezes")],
    }
    for pattern, replacement in frequency.get(locale.lower(), []):
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    lexicon = CARDINALS.get(locale.lower(), {})
    return WORDS.sub(lambda m: str(lexicon.get(m.group().casefold(), m.group())), text)


def numeric_anchors(text: str, locale: str) -> Counter:
    """Conservative numeric fingerprints, including common unit conversions."""
    normalized = _render_spelled(text, locale)
    temps = []
    def consume_temp(match):
        value = _decimal(match.group(1))
        kind = match.group(2).upper()
        if kind == "F":
            value = ((value - 32) * Decimal(5) / Decimal(9)).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP)
        temps.append((kind, "°C:" + _number(value)))
        return " "
    remaining = TEMPERATURES.sub(consume_temp, normalized)
    celsius = Counter(x for kind, x in temps if kind == "C")
    found = []
    for kind, value in temps:
        # Drop only the redundant target-side F display of a C value.
        if kind == "F" and celsius[value] > 0:
            celsius[value] -= 1
        else:
            found.append(value)
    found.extend("num:" + _number(_decimal(m.group()))
                 for m in NUMBER.finditer(remaining))
    return Counter(found)


def unit_anchors(text: str, locale: str) -> Counter:
    normalized = _render_spelled(text, locale)
    found = []
    for match in UNITS.finditer(normalized):
        unit = UNIT_MAP.get(match.group(2).casefold())
        if unit:
            dimension, factor = unit
            found.append((dimension, _number(_decimal(match.group(1)) * Decimal(factor))))
    return Counter(found)


def numeric_difference(source: str, target: str, source_locale: str, target_locale: str):
    """Return numeric drift, explainable formatting drift, and unit drift."""
    a, b = numeric_anchors(source, source_locale), numeric_anchors(target, target_locale)
    a_units, b_units = unit_anchors(source, source_locale), unit_anchors(target, target_locale)
    units_differ = bool(a_units and b_units and a_units != b_units)
    raw_a = Counter(m.group().replace(",", ".") for m in NUMBER.finditer(source))
    raw_b = Counter(m.group().replace(",", ".") for m in NUMBER.finditer(target))
    return a != b, bool(a == b and raw_a != raw_b and not units_differ), units_differ


def _number_review_issue(code: str, key: str, source: str, target: str) -> dict:
    """Actionable triage without claiming heuristic completeness."""
    if (code == "NUMBER_ANCHOR_REVIEW" and key.endswith(".name")
            and key.startswith("ingredients.")
            and re.search(r"\b(?:farina|flour)\s*0{1,2}\b", source, re.I)):
        code = "INGREDIENT_CLASSIFICATION_REVIEW"
    elif (code == "NUMBER_ANCHOR_REVIEW" and not NUMBER.search(source)
          and not NUMBER.search(target)):
        code = "WORD_NUMBER_CONTEXT_REVIEW"
    return {"code": code, "field": key, "severity": "REVIEW",
            "priority": "P1" if key.startswith("steps.") else "P2",
            "sourceEvidence": source[:200], "targetEvidence": target[:200]}


def _semantic_evidence_index(report: dict, data: dict) -> dict:
    expected = {(r["id"], locale) for r in data["records"]
                for locale in data["targetLocales"]}
    if (report.get("adapter") != data["adapter"]
            or report.get("sourceLocale") != data["sourceLocale"]
            or report.get("targetLocales") != data["targetLocales"]
            or report.get("recordCount") != len(data["records"])
            or report.get("comparisonCount") != len(expected)
            or report.get("certification") != "NOT_CERTIFIED"
            or report.get("inputFingerprint") != stable_hash(data)):
        raise ValueError("Stale/unbound Semantic QA report: regenerate against current input")
    results = report.get("results")
    if not isinstance(results, list):
        raise ValueError("Missing Semantic QA results")
    index = {}
    for row in results:
        if not isinstance(row, dict):
            raise ValueError("Malformed Semantic QA result")
        key = (row.get("id"), row.get("locale"))
        if key in index:
            raise ValueError("Duplicate Semantic QA result")
        if row.get("reviewType") not in ("OFFLINE", "OFFLINE_ONLY", "AI_SEMANTIC"):
            raise ValueError("Unknown Semantic QA reviewType")
        index[key] = row
    if set(index) != expected:
        raise ValueError("Semantic QA report coverage mismatch")
    return index


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
    source_by_id = {r["id"]: r["source"] for r in data["records"]}
    for rid, draft in draft_index.items():
        if rid not in source_by_id or draft["source"] != source_by_id[rid]:
            raise ValueError("Stale draft with absent or changed canonical source")
    semantic = _semantic_evidence_index(semantic_report, data) if semantic_report else {}

    domain = data["adapter"]
    rows = []
    counts = Counter()
    normalized_form_count = 0
    for index, item in enumerate(data["records"]):
        rid = item["id"]
        sources = flatten(item["source"])
        for locale in data["targetLocales"]:
            translated = flatten(item.get("translations", {}).get(locale, {}))
            draft = flatten(draft_index.get(rid, {}).get("translations", {}).get(locale, {}))
            proposals = []
            issues = []
            numeric_context_hints = []
            normalized_fields = []
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
                different, form_equivalent, units_differ = numeric_difference(
                    original, target, data["sourceLocale"], locale)
                if different:
                    finding = _number_review_issue("NUMBER_ANCHOR_REVIEW", key, original, target)
                    if finding["code"] == "WORD_NUMBER_CONTEXT_REVIEW":
                        # Purely written, context-dependent numeral phrases are
                        # hints; a translation is still OFFLINE_REVIEW_REQUIRED.
                        # Explicit unit mismatch below always remains REVIEW.
                        numeric_context_hints.append(finding)
                    else:
                        issues.append(finding)
                if units_differ:
                    issues.append(_number_review_issue("UNIT_ANCHOR_REVIEW", key, original, target))
                if form_equivalent:
                    normalized_fields.append(key)
                    normalized_form_count += 1
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
                "numericFormNormalizationHints": normalized_fields,
                "numericContextHints": numeric_context_hints,
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
        "triageIssuePriorities": dict(sorted(Counter(
            issue.get("priority", "P1") for row in rows for issue in row["issues"]
        ).items())),
        "numericFormNormalizationHints": normalized_form_count,
        "numericContextHints": sum(len(row["numericContextHints"]) for row in rows),
        "inputFingerprint": stable_hash(data),
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
