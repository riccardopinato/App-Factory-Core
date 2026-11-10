#!/usr/bin/env python3
"""Strict, version-neutral Golden admission gate.

Canonical readiness is structured and NOT inferred from freshness. Human-facing
legacy status is retained for index/history; this adapter rejects unknown
statuses instead of promoting a candidate by substring accident.
"""
from __future__ import annotations

ADMISSION_LEVELS = frozenset((
    "CERTIFIED_GOLDEN", "CERTIFIED_PROCESS", "CERTIFIED_DONOR",
    "COPY_READY", "CANDIDATE", "DEPRECATED",
))


def classify_legacy_status(status: str) -> str:
    if not isinstance(status, str):
        raise ValueError("Golden status must be text")
    label = status.strip().upper()
    if label == "DEPRECATED":
        return "DEPRECATED"
    if label.startswith("CERTIFIED GOLDEN"):
        return "CERTIFIED_GOLDEN"
    if label.startswith("CERTIFIED PROCESS"):
        return "CERTIFIED_PROCESS"
    if label.startswith("CERTIFIED DONOR"):
        return "CERTIFIED_DONOR"
    if label.startswith("COPY-READY"):
        return "COPY_READY"
    if "DRAFT" in label or "CANDIDATE" in label:
        return "CANDIDATE"
    raise ValueError("Unknown Golden status, explicit review needed: " + status)


def check_admission(entry: dict) -> str:
    declared = entry.get("admission_level")
    inferred = classify_legacy_status(entry.get("status"))
    if declared not in ADMISSION_LEVELS:
        raise ValueError("Missing/invalid admission_level: " + str(entry.get("id")))
    if declared != inferred:
        raise ValueError("Golden status/admission mismatch: " + str(entry.get("id")))
    if declared == "DEPRECATED" and entry.get("freshness_status") != "DEPRECATED":
        # Historical records may retain CURRENT freshness: deprecated status wins
        # for selection, but must never be promoted.
        return declared
    return declared


def requires_review(entry: dict) -> bool:
    level = check_admission(entry)
    return level in ("CANDIDATE", "DEPRECATED") or entry.get("freshness_status") != "CURRENT"


def reuse_scope(entry: dict) -> str:
    level = check_admission(entry)
    if level == "CERTIFIED_DONOR":
        return "E3_SCOPED_DONOR_CONSUMER_VERIFICATION_REQUIRED"
    if level == "CERTIFIED_GOLDEN":
        return "CERTIFIED_GOLDEN_WITH_SCOPE_LIMITS"
    if level == "COPY_READY":
        return "COPY_READY_CONSUMER_TESTS_REQUIRED"
    if level == "CERTIFIED_PROCESS":
        return "CERTIFIED_PROCESS_SCOPE_ONLY"
    return "NOT_AUTO_ADMISSIBLE"
