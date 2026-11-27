#!/usr/bin/env python3
"""Factory Spec Lite v1 — source-contract validation, not authorization or QA.

No network, shell execution, mutation, provider access or runtime claims.
The expected SHA values MUST come from a trusted independently resolved context,
not from the untrusted manifest itself. The --examples mode only tests fixtures.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/factory_spec_lite_v1.schema.json"
HIGH_RISK = (
    "data_loss", "security", "billing", "native_lifecycle",
    "migration", "sensitive_data", "release"
)
MODES = ("FAST", "STANDARD", "CONTROLLED")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _safe_path(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if value.startswith("/") or "\\" in value or "//" in value:
        return False
    parts = value.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def _forbidden_covers(denied: str, candidate: str) -> bool:
    if denied == candidate:
        return True
    if denied.endswith("/**"):
        prefix = denied[:-3]
        return candidate == prefix or candidate.startswith(prefix + "/")
    return False


def validate_manifest(
    doc: dict[str, Any],
    *,
    expected_factory_sha: str,
    expected_source_sha: str,
    schema: dict[str, Any] | None = None,
) -> list[str]:
    """Return all structural/semantic conflicts; never mutate the manifest."""
    errors: list[str] = []
    if not SHA_RE.fullmatch(expected_factory_sha):
        errors.append("TRUSTED_FACTORY_SHA_MISSING_OR_INVALID")
    if not SHA_RE.fullmatch(expected_source_sha):
        errors.append("TRUSTED_SOURCE_SHA_MISSING_OR_INVALID")
    if schema is None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        problems = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc),
            key=lambda e: tuple(str(k) for k in e.absolute_path),
        )
        for issue in problems:
            loc = ".".join(str(k) for k in issue.absolute_path) or "<root>"
            errors.append(f"SCHEMA:{loc}:{issue.message}")
    except (TypeError, ValueError, KeyError) as exc:
        errors.append(f"SCHEMA_VALIDATION_ERROR:{exc}")
    if not isinstance(doc, dict):
        return errors

    factory = doc.get("factory")
    target = doc.get("target")
    canonical = doc.get("canonical_refs")
    scope = doc.get("scope")
    risk = doc.get("risk")
    requirements = doc.get("requirements")
    checks = doc.get("validation")
    approval = doc.get("approval")
    verification = doc.get("verification")
    mode = doc.get("mode")

    if isinstance(factory, dict) and factory.get("sha") != expected_factory_sha:
        errors.append("FACTORY_SHA_MISMATCH")
    if isinstance(target, dict) and target.get("source_sha") != expected_source_sha:
        errors.append("SOURCE_SHA_MISMATCH")

    if isinstance(canonical, dict) and isinstance(factory, dict) and isinstance(target, dict):
        links = [("factory_current", factory.get("repository"), factory.get("sha"), "CURRENT.yaml")]
        links += [(k, target.get("repository"), target.get("source_sha"), None)
                  for k in ("product_bible", "roadmap", "agents")]
        for key, expected_repo, expected_sha, exact_path in links:
            value = canonical.get(key)
            if value is None:
                continue
            if not isinstance(value, dict):
                continue
            if value.get("repository") != expected_repo or value.get("sha") != expected_sha:
                errors.append(f"CANONICAL_REF_DRIFT:{key}")
            if exact_path is not None and value.get("path") != exact_path:
                errors.append(f"CANONICAL_REF_DRIFT:{key}")
        if canonical.get("factory_current") is None:
            errors.append("FACTORY_CURRENT_REF_MISSING")
        for golden in canonical.get("goldens", []):
            if isinstance(golden, dict):
                if (golden.get("repository") != factory.get("repository")
                    or golden.get("sha") != factory.get("sha")
                    or not str(golden.get("path", "")).startswith("golden/")):
                    errors.append("GOLDEN_REFERENCE_DRIFT")
        for entry in ("factory_current", "product_bible", "roadmap", "agents"):
            ref = canonical.get(entry)
            if isinstance(ref, dict) and not _safe_path(ref.get("path")):
                errors.append(f"INVALID_CANONICAL_PATH:{entry}")
        for golden in canonical.get("goldens", []):
            if isinstance(golden, dict) and not _safe_path(golden.get("path")):
                errors.append("INVALID_CANONICAL_PATH:goldens")

    if isinstance(scope, dict):
        allow = scope.get("allowed_paths", [])
        deny = scope.get("forbidden_paths", [])
        if isinstance(allow, list) and isinstance(deny, list):
            for value in allow + deny:
                if not _safe_path(value):
                    errors.append(f"INVALID_SCOPE_PATH:{value}")
            for value in allow:
                for blocked in deny:
                    if isinstance(value, str) and isinstance(blocked, str) and _forbidden_covers(blocked, value):
                        errors.append(f"CONFLICTING_PATH_SCOPE:{value}:{blocked}")

    if isinstance(risk, dict) and mode in MODES:
        active = [k for k in HIGH_RISK if risk.get(k) is True]
        if active and mode != "CONTROLLED":
            errors.append("HIGH_RISK_REQUIRES_CONTROLLED:" + ",".join(active))

    if isinstance(requirements, list):
        ids: set[str] = set()
        acceptance_ids: set[str] = set()
        for item in requirements:
            if not isinstance(item, dict):
                continue
            req_id = item.get("id")
            if req_id in ids:
                errors.append(f"DUPLICATE_REQUIREMENT_ID:{req_id}")
            ids.add(req_id)
            for conflict in item.get("conflicts_with", []):
                errors.append(f"UNRESOLVED_REQUIREMENT_CONFLICT:{req_id}:{conflict}")
            if item.get("status") == "APPROVED" and isinstance(approval, dict) and approval.get("status") != "APPROVED":
                errors.append(f"UNAUTHORIZED_REQUIREMENT_APPROVAL:{req_id}")
            for criterion in item.get("acceptance", []):
                if not isinstance(criterion, dict):
                    continue
                ac_id = criterion.get("id")
                if ac_id in acceptance_ids:
                    errors.append(f"DUPLICATE_ACCEPTANCE_ID:{ac_id}")
                acceptance_ids.add(ac_id)
                if isinstance(checks, dict) and criterion.get("evidence_type") not in checks.get("required_checks", []):
                    errors.append(f"ACCEPTANCE_TEST_GAP:{ac_id}")

    # An unrepresented required test kind cannot be attributed to any AC.
    # Reject at spec admission rather than let downstream evidence claim full coverage.
    if isinstance(requirements, list) and isinstance(checks, dict):
        declared = checks.get("required_checks", [])
        if isinstance(declared, list):
            mapped = {
                ac.get("evidence_type")
                for req in requirements if isinstance(req, dict)
                for ac in req.get("acceptance", []) if isinstance(ac, dict)
                if isinstance(ac.get("evidence_type"), str)
            }
            for kind in sorted({v for v in declared if isinstance(v, str)} - mapped):
                errors.append(f"REQUIRED_CHECK_UNMAPPED:{kind}")

    # Optional OpenSpec-inspired deltas. Backward-compatible with v1 manifests.
    # This proves structural consistency only, never existence of prior requirements.
    if isinstance(requirements, list):
        for req in requirements:
            if not isinstance(req, dict) or req.get("delta") is None:
                continue
            delta = req["delta"]
            if not isinstance(delta, dict):
                continue
            operation, previous = delta.get("operation"), delta.get("previous")
            rid = req.get("id")
            if operation == "ADDED" and previous is not None:
                errors.append(f"DELTA_ADDED_MUST_NOT_HAVE_PREVIOUS:{rid}")
            if operation in ("MODIFIED", "REMOVED", "RENAMED"):
                if not isinstance(previous, dict):
                    errors.append(f"DELTA_PREVIOUS_REQUIRED:{rid}")
                elif (previous.get("spec_id") == doc.get("spec_id")
                      and previous.get("requirement_id") == rid
                      and previous.get("source_sha") == target.get("source_sha")):
                    errors.append(f"DELTA_PREVIOUS_NOT_PINNED_TO_PRIOR_STATE:{rid}")
            if operation == "REMOVED" and mode == "FAST":
                errors.append(f"DELTA_REMOVAL_NOT_FAST:{rid}")

    if isinstance(approval, dict):
        status = approval.get("status")
        if status == "APPROVED":
            if not isinstance(approval.get("decision_ref"), str) or not approval["decision_ref"].startswith("https://github.com/"):
                errors.append("APPROVAL_EVIDENCE_REQUIRED")
            if not isinstance(canonical, dict) or canonical.get("product_bible") is None or canonical.get("roadmap") is None:
                errors.append("APPROVED_SCOPE_REQUIRES_PRODUCT_BIBLE_AND_ROADMAP")
            if isinstance(requirements, list) and any(
                isinstance(r, dict) and r.get("status") != "APPROVED" for r in requirements
            ):
                errors.append("PROPOSED_REQUIREMENT_CANNOT_SHIP")
        if status == "PROPOSED" and approval.get("decision_ref") is not None:
            errors.append("PROPOSAL_MUST_NOT_CLAIM_APPROVAL")

    if isinstance(verification, dict):
        if verification.get("status") != "NOT_VERIFIED" and not verification.get("evidence_links"):
            errors.append("UNPROVEN_VERIFICATION_CLAIM")
        if verification.get("status") == "NOT_VERIFIED" and verification.get("evidence_links"):
            errors.append("UNCLASSIFIED_VERIFICATION_EVIDENCE")

    if isinstance(checks, dict):
        required = checks.get("required_checks", [])
        if mode == "STANDARD" and isinstance(required, list) and not (
            {"UNIT_TEST", "INTEGRATION_TEST", "RUNTIME_TEST", "DEVICE_TEST"} & set(required)
        ):
            errors.append("STANDARD_BEHAVIOR_REGRESSION_TEST_REQUIRED")
        if mode == "CONTROLLED":
            if checks.get("manual_gate") is not True:
                errors.append("CONTROLLED_REQUIRES_MANUAL_GATE")
            rollback = checks.get("rollback_plan")
            if not isinstance(rollback, str) or len(rollback.strip()) < 30:
                errors.append("CONTROLLED_REQUIRES_ROLLBACK_PLAN")
            if isinstance(required, list) and not (
                {"INTEGRATION_TEST", "RUNTIME_TEST", "DEVICE_TEST"} & set(required)
            ):
                errors.append("CONTROLLED_REQUIRES_INTEGRATION_LEVEL_TEST")
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("--expected-factory-sha")
    parser.add_argument("--expected-source-sha")
    parser.add_argument("--examples", action="store_true", help="Fixture checks only; NOT real target-head verification")
    args = parser.parse_args(argv)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

    if args.examples:
        if args.manifest is not None:
            parser.error("--examples does not accept a manifest")
        for mode in MODES:
            doc = json.loads((ROOT / "spec_lite" / "examples" / f"{mode}.json").read_text(encoding="utf-8"))
            errs = validate_manifest(
                doc, expected_factory_sha=doc["factory"]["sha"],
                expected_source_sha=doc["target"]["source_sha"], schema=schema
            )
            if errs:
                print(json.dumps({"mode": mode, "errors": errs}, ensure_ascii=False))
                return 1
        print("EXAMPLES_SCHEMA_AND_INTERNAL_CONSISTENCY_OK; NOT_LIVE_SOURCE_VERIFIED")
        return 0

    if args.manifest is None or not args.expected_factory_sha or not args.expected_source_sha:
        parser.error("manifest, --expected-factory-sha and --expected-source-sha are required")
    try:
        doc = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"UNREADABLE_MANIFEST:{exc}", file=sys.stderr)
        return 2
    errs = validate_manifest(
        doc, expected_factory_sha=args.expected_factory_sha,
        expected_source_sha=args.expected_source_sha, schema=schema
    )
    if errs:
        for error in errs:
            print(error, file=sys.stderr)
        return 1
    print("SOURCE_CONTRACT_STRUCTURALLY_VALID; NO_AUTHORIZATION_OR_RUNTIME_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
