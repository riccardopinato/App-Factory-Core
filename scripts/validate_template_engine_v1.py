#!/usr/bin/env python3
"""App Factory Template Engine v1: static, fail-closed manifest validation.

No template is executed or installed by this validator; no app store or
consumer adapter is certified by a passing result.
"""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "template_engine_v1"
SCHEMA_PATH = CONTRACT / "manifest.schema.json"
EXAMPLES = CONTRACT / "examples"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict, schema: dict | None = None) -> list[str]:
    """Return deterministic validation errors. Never writes app data."""
    schema = schema if schema is not None else _read(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    problems = []
    for error in validator.iter_errors(manifest):
        loc = ".".join(str(part) for part in error.absolute_path) or "<root>"
        problems.append(f"{loc}: {error.message}")

    # Check cross-field constraints even when schema-level fields are malformed.
    if not isinstance(manifest, dict):
        return sorted(problems)
    loc = manifest.get("localization")
    cmp = manifest.get("compatibility")
    if isinstance(loc, dict) and isinstance(cmp, dict):
        translations = loc.get("translations", {})
        locales = cmp.get("target_locales", [])
        if isinstance(translations, dict) and isinstance(locales, list):
            if set(translations) != set(locales):
                problems.append("localization: translations must match compatibility.target_locales exactly")
            if loc.get("default_locale") not in translations:
                problems.append("localization.default_locale: missing from translations")

    if isinstance(cmp, dict):
        low, high = cmp.get("min_app_build"), cmp.get("max_app_build")
        if isinstance(low, int) and isinstance(high, int) and high < low:
            problems.append("compatibility: max_app_build must not be below min_app_build")

    preview = manifest.get("preview")
    if isinstance(preview, dict):
        path = preview.get("asset_path")
        if isinstance(path, str):
            normalized = path.replace("\\", "/")
            parts = normalized.split("/")
            if (normalized.startswith("/") or ":" in normalized
                    or any(p in (".", "..", "") for p in parts)
                    or any(p.startswith(".") for p in parts)):
                problems.append("preview.asset_path: must be a safe relative first-party path")

    access = manifest.get("access")
    if isinstance(access, dict):
        paid = access.get("tier") == "paid_once"
        has_key = bool(access.get("entitlement_key"))
        if paid and not has_key:
            problems.append("access.entitlement_key: paid_once requires a logical entitlement")
        if not paid and "entitlement_key" in access:
            problems.append("access.entitlement_key: free template must not carry entitlement")

    conf = manifest.get("configuration")
    if isinstance(conf, dict) and isinstance(conf.get("fields"), list):
        fields = conf["fields"]
        keys = [f.get("key") for f in fields if isinstance(f, dict) and isinstance(f.get("key"), str)]
        if len(keys) != len(set(keys)):
            problems.append("configuration.fields: duplicate keys")
        for i, field in enumerate(fields):
            if not isinstance(field, dict) or not isinstance(field.get("kind"), str):
                continue
            kind, default = field["kind"], field.get("default")
            where = f"configuration.fields.{i}"
            if kind == "boolean" and type(default) is not bool:
                problems.append(f"{where}: boolean default required")
            elif kind == "integer":
                if type(default) is not int:
                    problems.append(f"{where}: integer default required")
                elif (type(field.get("min")) is int and default < field["min"] or
                      type(field.get("max")) is int and default > field["max"]):
                    problems.append(f"{where}: default outside bounds")
                if type(field.get("min")) is int and type(field.get("max")) is int and field["min"] > field["max"]:
                    problems.append(f"{where}: min greater than max")
            elif kind == "text":
                if not isinstance(default, str):
                    problems.append(f"{where}: text default required")
                elif type(field.get("max_length")) is int and len(default) > field["max_length"]:
                    problems.append(f"{where}: default exceeds max_length")
            elif kind == "choice":
                opts = field.get("options", [])
                if not isinstance(default, str) or not isinstance(opts, list) or default not in opts:
                    problems.append(f"{where}: choice default must be in options")
            if kind != "choice" and "options" in field:
                problems.append(f"{where}: options only allowed for choice")
            if kind != "integer" and any(k in field for k in ("min", "max")):
                problems.append(f"{where}: min/max only allowed for integer")
            if kind != "text" and "max_length" in field:
                problems.append(f"{where}: max_length only allowed for text")

    return sorted(set(problems))


def validate_examples() -> list[str]:
    schema = _read(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    errors = []
    ids: set[tuple[str, str, str]] = set()
    examples = sorted(EXAMPLES.glob("*.json"))
    if len(examples) < 2:
        return ["expected at least two cross-app example manifests"]
    apps: set[str] = set()
    for path in examples:
        try:
            manifest = _read(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        for problem in validate_manifest(manifest, schema):
            errors.append(f"{path.name}: {problem}")
        apps.add(str(manifest.get("app_id")))
        identity = (str(manifest.get("app_id")), str(manifest.get("template_id")), str(manifest.get("template_version")))
        if identity in ids:
            errors.append(f"{path.name}: duplicate app/template/version")
        ids.add(identity)
    if len(apps) < 2:
        errors.append("examples must cover at least two different consumer apps")
    return sorted(errors)


def main() -> int:
    try:
        issues = validate_examples()
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL Template Engine v1: {exc}")
        return 1
    for issue in issues:
        print(f"FAIL {issue}")
    if issues:
        return 1
    print("PASS Template Engine v1: schema + cross-app sample manifests (static only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
