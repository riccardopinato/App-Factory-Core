#!/usr/bin/env python3
"""Semantic QA Engine v1: portable editorial comparison, cache and optional LLM.

No application data is modified. Offline mode is a deterministic, conservative
preflight. OpenAI mode performs meaning-level review only when explicitly
opted in for PUBLIC editorial content with a configured API key. A PASS from
a model is never professional certification or verified primary-source truth.

CLI:
  python3 semantic_qa.py --input normalized.json --report report.json \
    --cache cache.json --provider offline --workers 4 --batch-size 100
  python3 semantic_qa.py --input normalized.json --report report.json \
    --cache cache.json --provider openai --allow-external --second-pass
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen

ENGINE_VERSION = "1.0.2"
LOCALES = ("en", "it", "es", "fr", "de", "pt", "pt-BR")
RISK_ORDER = {"PASS": 0, "REVIEW": 1, "HOLD": 2}
AMOUNTS = re.compile(
    r"(?<!\w)\d+(?:[.,]\d+)?\s*(?:°\s*[cf]|%|ml|kg|mg|g|"
    r"minutes?|mins?|minuti?|minutos?|minuten|ore|hours?|horas?|"
    r"secondes?|seconds?|sekunden|sec|secondi|\b)",
    re.IGNORECASE,
)
LANGUAGE_UNKNOWN = ("not established", "non accertato", "non établi",
                    "nicht belegt", "não confirmado", "no acreditado")


def stable_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def normalize(value: object) -> dict:
    """A field map is stable across adapters and can contain nested lists/maps."""
    if not isinstance(value, dict):
        raise ValueError("source/translation must be a field dictionary")
    return value


def flatten(value: object, prefix: str = "") -> dict[str, str]:
    if isinstance(value, dict):
        result: dict[str, str] = {}
        for key in sorted(value):
            if key.startswith("_"):
                continue
            result.update(flatten(value[key], f"{prefix}.{key}" if prefix else key))
        return result
    if isinstance(value, list):
        result = {}
        for index, item in enumerate(value):
            result.update(flatten(item, f"{prefix}[{index}]"))
        return result
    return {prefix: str(value) if value is not None else ""}


def preflight(source: dict, target: dict, protected: list[str]) -> list[dict]:
    """Do not infer cross-locale meaning from text similarity or token equality."""
    a, b = flatten(source), flatten(target)
    problems = []
    for path in sorted(set(a) - set(b)):
        problems.append({"code": "MISSING_TARGET_FIELD", "severity": "HOLD",
                         "field": path, "sourceEvidence": a[path][:100],
                         "targetEvidence": "", "suggestion": ""})
    for path in sorted(set(a) & set(b)):
        if a[path].strip() and not b[path].strip():
            problems.append({"code": "EMPTY_TRANSLATION", "severity": "HOLD",
                             "field": path, "sourceEvidence": a[path][:100],
                             "targetEvidence": "", "suggestion": ""})
        # Compare measurable anchors only as a REVIEW. E.g. 74 C -> 165 F
        # is a valid conversion and needs contextual reasoning.
        x, y = AMOUNTS.findall(a[path]), AMOUNTS.findall(b[path])
        if x and Counter(re.sub(r"\s+", "", t.lower()) for t in x) != Counter(
                re.sub(r"\s+", "", t.lower()) for t in y):
            problems.append({"code": "NUMERIC_ANCHOR_DRIFT", "severity": "REVIEW",
                             "field": path, "sourceEvidence": ", ".join(x)[:140],
                             "targetEvidence": ", ".join(y)[:140],
                             "suggestion": "Compare quantities, durations, dates and valid conversions."})
    target_blob = json.dumps(target, ensure_ascii=False).casefold()
    source_blob = json.dumps(source, ensure_ascii=False).casefold()
    for token in sorted(set(protected)):
        if token and token.casefold() in source_blob and token.casefold() not in target_blob:
            problems.append({"code": "PROTECTED_ENTITY_MISSING", "severity": "REVIEW",
                             "field": "*", "sourceEvidence": token,
                             "targetEvidence": "", "suggestion": "Check entity translation or omission."})
    return problems


FORMAT = {
    "type": "json_schema", "name": "semantic_qa_review", "strict": True,
    "schema": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "verdict": {"type": "string", "enum": ["PASS", "REVIEW", "HOLD"]},
            "issues": {
                "type": "array",
                "items": {"type": "object", "additionalProperties": False,
                    "properties": {
                        "code": {"type": "string"}, "severity": {"type": "string",
                          "enum": ["REVIEW", "HOLD"]},
                        "field": {"type": "string"},
                        "sourceEvidence": {"type": "string"},
                        "targetEvidence": {"type": "string"},
                        "suggestion": {"type": "string"},
                    },
                    "required": ["code", "severity", "field", "sourceEvidence",
                                 "targetEvidence", "suggestion"],
                },
            },
        },
        "required": ["verdict", "issues"],
    },
}

PROMPT = (
    "You review public editorial translations for semantic fidelity. "
    "Compare the full original and translated structured record in context. "
    "Look for wrong objects/actions, negations, unsafe food instructions, "
    "changed measurements and dates, ungrounded claims, named entities, "
    "factual chronology, idiomatic culinary or institutional terminology, "
    "and missing or added information. The target language must sound natural. "
    "Do not infer that matching numbers or fluent grammar proves equivalence. "
    "Return PASS only if no material problem is found, REVIEW for uncertain "
    "cases, HOLD for a concrete harmful or meaning-changing error. "
    "Give exact evidence snippets for each finding. Never invent an external "
    "source, an ingredient, a date or a certification. "
    "A supplied source reference is metadata, not independently verified proof."
)


def openai_review(task: dict, *, model: str, second: bool = False) -> dict:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY unavailable; semantic review NOT run")
    instruction = PROMPT
    if second:
        instruction += (
            " Independent second-pass reviewer: critically re-evaluate the "
            "original and translation without relying on any previous verdict."
        )
    payload = {
        "model": model, "store": False,
        "instructions": instruction,
        "input": json.dumps(task, ensure_ascii=False, sort_keys=True),
        "text": {"format": FORMAT},
        "max_output_tokens": 1800,
    }
    body = json.dumps(payload).encode("utf-8")
    request = Request("https://api.openai.com/v1/responses", data=body, method="POST",
                      headers={"Authorization": "Bearer " + key,
                               "Content-Type": "application/json"})
    with urlopen(request, timeout=90) as response:
        result = json.load(response)
    for item in result.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    verdict = json.loads(part["text"])
                    if verdict.get("verdict") not in RISK_ORDER or not isinstance(
                            verdict.get("issues"), list):
                        raise ValueError("Invalid structured semantic reviewer result")
                    return verdict
                if part.get("type") == "refusal":
                    raise RuntimeError("Model refused semantic comparison")
    raise RuntimeError("No model structured output; semantic comparison not completed")


def issue(code: str, severity: str, details: str) -> dict:
    return {"code": code, "severity": severity, "field": "*",
            "sourceEvidence": details[:160], "targetEvidence": "", "suggestion": ""}


def review_one(entry: dict, locale: str, cfg: dict, cache: dict) -> dict:
    source, translations = entry["source"], entry["translations"]
    target = translations.get(locale)
    if not isinstance(target, dict):
        return {"id": entry["id"], "locale": locale, "state": "HOLD",
                "reviewType": "OFFLINE", "cached": False,
                "findings": [issue("MISSING_LOCALE", "HOLD", locale)]}
    protected = entry.get("protectedTerms", [])
    known = preflight(source, target, protected)
    task = {
        "adapter": cfg["adapter"], "sourceLocale": cfg["sourceLocale"],
        "targetLocale": locale, "recordId": entry["id"],
        "source": source, "translation": target,
        "context": entry.get("context", {}),
        "sourceRefs": entry.get("sourceRefs", []),
        "domainRubric": cfg.get("domainRubric", ""),
    }
    fingerprint = stable_hash({"engine": ENGINE_VERSION, "task": task,
                               "mode": cfg["provider"], "model": cfg["model"],
                               "second": cfg["secondPass"]})
    if fingerprint in cache:
        result = dict(cache[fingerprint])
        return {**result, "id": entry["id"], "locale": locale, "cached": True}
    verdict = max(("PASS", *(item["severity"] for item in known)),
                  key=RISK_ORDER.get)
    checked = cfg["provider"] == "openai"
    findings = list(known)
    if checked:
        try:
            first = openai_review(task, model=cfg["model"])
            passes = [first]
            if cfg["secondPass"]:
                passes.append(openai_review(task, model=cfg["model"], second=True))
            for response in passes:
                if response["verdict"] not in RISK_ORDER:
                    raise ValueError("Unexpected reviewer verdict")
                verdict = max((verdict, response["verdict"]), key=RISK_ORDER.get)
                findings.extend(response["issues"])
            if any(p["verdict"] != passes[0]["verdict"] for p in passes[1:]):
                verdict = max((verdict, "REVIEW"), key=RISK_ORDER.get)
                findings.append(issue("REVIEWER_DISAGREEMENT", "REVIEW",
                                      "Independent semantic passes disagreed"))
        except Exception as exc:
            checked = False
            verdict = max((verdict, "REVIEW"), key=RISK_ORDER.get)
            findings.append(issue("PROVIDER_ERROR", "REVIEW",
                                  f"{type(exc).__name__}: semantic review incomplete"))
    # Offline PASS means structural ONLY, never semantic fidelity.
    state = ("AI_REVIEW_" + verdict) if checked else (
        "HOLD" if verdict == "HOLD" else "OFFLINE_REVIEW_REQUIRED")
    result = {"id": entry["id"], "locale": locale, "state": state,
              "reviewType": "AI_SEMANTIC" if checked else "OFFLINE_ONLY",
              "cached": False, "fingerprint": fingerprint, "findings": findings}
    if checked or not any(x["code"] == "PROVIDER_ERROR" for x in findings):
        cache[fingerprint] = {k: v for k, v in result.items() if k not in (
            "id", "locale", "cached")}
    return result


def audit(data: dict, *, provider: str = "offline", model: str = "",
          second_pass: bool = False, workers: int = 4, batch_size: int = 100,
          cache: dict | None = None, allow_external: bool = False) -> dict:
    if data.get("schemaVersion") != 1 or not isinstance(data.get("records"), list):
        raise ValueError("Expected schemaVersion=1 with records array")
    source_locale, locales = data.get("sourceLocale"), data.get("targetLocales")
    if source_locale not in LOCALES or not isinstance(locales, list) or not locales:
        raise ValueError("Invalid sourceLocale/targetLocales")
    if len(locales) != len(set(locales)) or source_locale in locales:
        raise ValueError("Duplicate/invalid target locale")
    if any(l not in LOCALES for l in locales):
        raise ValueError("Unsupported locale")
    if not 1 <= workers <= 8 or not 1 <= batch_size <= 100:
        raise ValueError("workers must be 1..8 and batch-size 1..100")
    if provider not in ("offline", "openai"):
        raise ValueError("Invalid provider")
    if provider == "openai" and (
            not allow_external or data.get("privacy") != "PUBLIC_EDITORIAL"
            or not model or not os.environ.get("OPENAI_API_KEY")):
        raise ValueError("OpenAI requires explicit opt-in, PUBLIC_EDITORIAL, model and key")
    rows = data["records"]
    ids = [r.get("id") for r in rows]
    if any(not isinstance(rid, str) or not rid for rid in ids):
        raise ValueError("Missing canonical record id")
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate canonical record id")
    cfg = {"adapter": data.get("adapter", "generic"), "sourceLocale": source_locale,
           "domainRubric": data.get("domainRubric", ""), "provider": provider,
           "model": model, "secondPass": bool(second_pass)}
    store = cache if cache is not None else {}
    results = []
    # One source ID is a unit of work; separate disjoint batches and bound
    # concurrency. Results sorted to be insensitive to worker completion order.
    for start in range(0, len(rows), batch_size):
        chunk = rows[start:start + batch_size]
        tasks = [(r, locale) for r in chunk for locale in locales]
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results.extend(pool.map(lambda t: review_one(t[0], t[1], cfg, store),
                                    tasks))
    results.sort(key=lambda r: (r["id"], r["locale"]))
    counts = dict(Counter(r["state"] for r in results))
    return {
        "schemaVersion": 1, "engineVersion": ENGINE_VERSION,
        "mode": provider.upper(),
        "semanticModelActuallyUsed": any(r["reviewType"] == "AI_SEMANTIC" for r in results),
        "sourceLocale": source_locale, "targetLocales": locales,
        "adapter": cfg["adapter"], "recordCount": len(rows),
        "inputFingerprint": stable_hash(data),
        "comparisonCount": len(results), "batchSize": batch_size,
        "maxWorkers": workers, "cachedComparisons": sum(r["cached"] for r in results),
        "counts": counts, "results": results,
        "certification": "NOT_CERTIFIED",
        "warning": ("Offline mode validates selected invariants only; semantic "
                    "fidelity and external facts remain unverified. Provider "
                    "output is an AI opinion, not independent primary-source proof."),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--cache", type=Path)
    p.add_argument("--provider", choices=("offline", "openai"), default="offline")
    p.add_argument("--model", default=os.environ.get("SEMANTIC_QA_MODEL", ""))
    p.add_argument("--allow-external", action="store_true")
    p.add_argument("--second-pass", action="store_true")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--batch-size", type=int, default=100)
    args = p.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    cache = {}
    if args.cache and args.cache.is_file():
        obj = json.loads(args.cache.read_text(encoding="utf-8"))
        if obj.get("schemaVersion") != 1 or not isinstance(obj.get("entries"), dict):
            raise ValueError("Malformed semantic cache")
        cache = obj["entries"]
    report = audit(data, provider=args.provider, model=args.model,
                   second_pass=args.second_pass, workers=args.workers,
                   batch_size=args.batch_size, cache=cache,
                   allow_external=args.allow_external)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    if args.cache:
        args.cache.parent.mkdir(parents=True, exist_ok=True)
        args.cache.write_text(json.dumps({"schemaVersion": 1, "entries": cache},
                                          ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    summary = {k: report[k] for k in ("adapter", "recordCount", "comparisonCount",
                                      "cachedComparisons", "counts", "mode")}
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
