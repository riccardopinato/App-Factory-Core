#!/usr/bin/env python3
"""App Factory Performance QA: bounded synthetic fixtures and honest comparisons.

Offline, Python standard library only. Never scans or deletes real user files.
This is a QA harness, NOT a replacement for a native app's runtime engine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

VERSION = 1
MAX_FILES = 100_000
MAX_BYTES = 256 * 1024 * 1024
METRIC_FIELDS = ("file_rows_ms", "scan_ms", "wall_ms", "peak_bytes")
IDENTITY_FIELDS = (
    "fixture_id", "device", "api_level", "mode", "file_count",
    "rows_reused", "rows_replaced", "integrity_digest",
)


class EvidenceError(ValueError):
    """Fail closed when fixture or evidence is incomplete or incomparable."""


def _canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fixture_id(seed: int, files: int, duplicate_pairs: int) -> str:
    return _digest(_canonical([VERSION, seed, files, duplicate_pairs]))[:24]


def _payload(seed: int, index: int, duplicate_pairs: int) -> bytes:
    # Pair indices 0/1, 2/3, ... share bytes; every other index is unique.
    family = index // 2 if index < duplicate_pairs * 2 else duplicate_pairs + index - duplicate_pairs * 2
    value = hashlib.sha256(f"factory-qa-v1:{seed}:{family}".encode("ascii")).digest()
    size = 80 + family % 79
    return (value * 5)[:size]


def build_fixture(destination: Path, files: int, duplicate_pairs: int, seed: int = 19,
                  byte_budget: int = 64 * 1024 * 1024) -> dict:
    if not (1 <= files <= MAX_FILES):
        raise EvidenceError(f"files must be 1..{MAX_FILES}")
    if not (0 <= duplicate_pairs <= files // 2):
        raise EvidenceError("duplicate_pairs must be 0..files/2")
    if not (1 <= byte_budget <= MAX_BYTES):
        raise EvidenceError("invalid byte_budget")
    # Reject a pre-existing destination: never overwrite or clean arbitrary paths.
    if destination.is_symlink() or destination.exists():
        raise EvidenceError("destination must be a NEW directory; no overwrite")
    estimated = sum(len(_payload(seed, i, duplicate_pairs)) for i in range(files))
    if estimated > byte_budget:
        raise EvidenceError(f"fixture would exceed byte budget: {estimated} > {byte_budget}")
    destination.mkdir(parents=True, exist_ok=False)
    records = []
    for i in range(files):
        name = f"synthetic_{i:06d}.bin"
        data = _payload(seed, i, duplicate_pairs)
        (destination / name).write_bytes(data)
        records.append({"name": name, "size": len(data), "sha256": _digest(data)})
    manifest = {
        "schema_version": VERSION, "fixture_id": fixture_id(seed, files, duplicate_pairs),
        "seed": seed, "files": files, "duplicate_pairs": duplicate_pairs,
        "total_bytes": estimated, "records": records,
        "expected_duplicate_groups": duplicate_pairs,
    }
    (destination / "manifest.json").write_bytes(_canonical(manifest) + b"\n")
    return {"fixture_id": manifest["fixture_id"], "files": files, "duplicate_pairs": duplicate_pairs,
            "total_bytes": estimated, "verification": "NOT_VERIFIED"}


def verify_fixture(directory: Path) -> dict:
    if not directory.is_dir() or directory.is_symlink():
        raise EvidenceError("fixture root missing or symlink")
    manifest_file = directory / "manifest.json"
    if manifest_file.is_symlink():
        raise EvidenceError("manifest must not be a symlink")
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise EvidenceError("invalid manifest") from error
    if not isinstance(manifest, dict):
        raise EvidenceError("manifest must be an object")
    if manifest.get("schema_version") != VERSION:
        raise EvidenceError("unsupported schema")
    seed, files, pairs = manifest.get("seed"), manifest.get("files"), manifest.get("duplicate_pairs")
    if any(type(x) is not int for x in (seed, files, pairs)):
        raise EvidenceError("invalid fixture numeric fields")
    if not (1 <= files <= MAX_FILES and 0 <= pairs <= files // 2):
        raise EvidenceError("invalid fixture size/pairs")
    if manifest.get("fixture_id") != fixture_id(seed, files, pairs):
        raise EvidenceError("fixture identity mismatch")
    records = manifest.get("records")
    if not isinstance(records, list) or len(records) != files:
        raise EvidenceError("record count mismatch")
    expected_names = {"manifest.json"}
    total = 0
    digest_groups: dict[str, int] = {}
    for i, row in enumerate(records):
        if not isinstance(row, dict):
            raise EvidenceError("invalid record")
        name = f"synthetic_{i:06d}.bin"
        expected = _payload(seed, i, pairs)
        if row.get("name") != name or row.get("size") != len(expected) or row.get("sha256") != _digest(expected):
            raise EvidenceError("fixture manifest tampered or inconsistent")
        item = directory / name
        if item.is_symlink() or not item.is_file():
            raise EvidenceError(f"fixture file missing or symlink: {name}")
        if item.stat().st_size != len(expected) or _digest(item.read_bytes()) != row["sha256"]:
            raise EvidenceError(f"fixture contents changed: {name}")
        expected_names.add(name)
        total += len(expected)
        digest_groups[row["sha256"]] = digest_groups.get(row["sha256"], 0) + 1
    if {p.name for p in directory.iterdir()} != expected_names:
        raise EvidenceError("unexpected/missing files in fixture")
    if total != manifest.get("total_bytes"):
        raise EvidenceError("total byte count mismatch")
    found_pairs = sum(1 for count in digest_groups.values() if count == 2)
    if found_pairs != pairs or any(count > 2 for count in digest_groups.values()):
        raise EvidenceError("duplicate family mismatch")
    return {"fixture_id": manifest["fixture_id"], "files": files, "duplicate_pairs": pairs,
            "total_bytes": total, "verification": "PASS", "integrity_digest": _digest(_canonical(records))}


def _read_runs(path: Path, metric: str, minimum: int) -> list[dict]:
    if not path.is_file():
        raise EvidenceError("evidence file missing")
    runs = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError as error:
                raise EvidenceError("invalid JSONL evidence") from error
            if not isinstance(row, dict) or row.get("schema_version") != VERSION:
                raise EvidenceError("unsupported evidence schema")
            if any(field not in row for field in IDENTITY_FIELDS):
                raise EvidenceError("missing identity/integrity evidence")
            if not isinstance(row.get("source_sha"), str) or re.fullmatch(r"[0-9a-f]{40}", row["source_sha"]) is None:
                raise EvidenceError("missing full Git source SHA")
            if not isinstance(row.get("integrity_digest"), str) or re.fullmatch(r"sha256:[0-9a-f]{64}", row["integrity_digest"]) is None:
                raise EvidenceError("missing full integrity SHA-256")
            if row.get("environment") not in ("physical", "emulator"):
                raise EvidenceError("missing environment provenance")
            if type(row.get(metric)) not in (int, float) or not (0 <= row[metric] < 1e12):
                raise EvidenceError("invalid numeric metric")
            if any(type(row[f]) is not int for f in ("file_count", "rows_reused", "rows_replaced", "api_level")):
                raise EvidenceError("invalid inventory/OS numbers")
            if row["file_count"] <= 0 or row["rows_reused"] + row["rows_replaced"] != row["file_count"]:
                raise EvidenceError("inventory row count inconsistent")
            runs.append(row)
            if len(runs) > 1_000:
                raise EvidenceError("evidence too large")
    if len(runs) < minimum:
        raise EvidenceError(f"need at least {minimum} independent measurements")
    first = runs[0]
    for row in runs[1:]:
        if any(row[f] != first[f] for f in IDENTITY_FIELDS) or row["environment"] != first["environment"] or row["source_sha"] != first["source_sha"]:
            raise EvidenceError("different source/fixture/runner mixed in one series")
    return runs


def compare_series(baseline: Path, candidate: Path, metric: str = "file_rows_ms",
                   min_runs: int = 3, max_regression_pct: float = 5.0) -> dict:
    if metric not in METRIC_FIELDS:
        raise EvidenceError("metric not recognized")
    if not (3 <= min_runs <= 50) or not (0 <= max_regression_pct <= 100):
        raise EvidenceError("invalid evidence policy")
    old = _read_runs(baseline, metric, min_runs)
    new = _read_runs(candidate, metric, min_runs)
    if any(old[0][f] != new[0][f] for f in IDENTITY_FIELDS) or old[0]["environment"] != new[0]["environment"]:
        raise EvidenceError("INCOMPARABLE: baseline and candidate use different fixture/hardware/mode/integrity")
    a = statistics.median(r[metric] for r in old)
    b = statistics.median(r[metric] for r in new)
    if a <= 0:
        raise EvidenceError("baseline median must be positive")
    delta_pct = round((b / a - 1) * 100, 3)
    environment = old[0]["environment"]
    gate = "REVIEW_REGRESSION" if delta_pct > max_regression_pct else (
        "PHYSICAL_REPLAY_REQUIRED" if environment == "emulator" else "CANDIDATE_NO_CERTIFICATION"
    )
    return {
        "schema_version": VERSION, "metric": metric, "fixture_id": old[0]["fixture_id"],
        "baseline_sha": old[0]["source_sha"], "candidate_sha": new[0]["source_sha"],
        "environment": environment, "mode": old[0]["mode"],
        "sample_counts": [len(old), len(new)],
        "baseline_median": a, "candidate_median": b, "delta_pct": delta_pct,
        "max_regression_pct": max_regression_pct, "gate": gate,
        "certification": "NOT_CERTIFIED",
        "note": "Only comparable phase metrics; no battery/OEM/storage or release certification.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    fixture = commands.add_parser("fixture", help="create bounded synthetic files in a new directory")
    fixture.add_argument("--output", type=Path, required=True)
    fixture.add_argument("--files", type=int, default=200)
    fixture.add_argument("--duplicate-pairs", type=int, default=10)
    fixture.add_argument("--seed", type=int, default=19)
    fixture.add_argument("--byte-budget", type=int, default=64 * 1024 * 1024)
    check = commands.add_parser("verify", help="validate expected bytes, size, identity and groups")
    check.add_argument("--input", type=Path, required=True)
    compare = commands.add_parser("compare", help="compare compatible JSONL measurements")
    compare.add_argument("--baseline", type=Path, required=True)
    compare.add_argument("--candidate", type=Path, required=True)
    compare.add_argument("--metric", choices=METRIC_FIELDS, default="file_rows_ms")
    compare.add_argument("--min-runs", type=int, default=3)
    compare.add_argument("--max-regression-pct", type=float, default=5.0)
    compare.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "fixture":
            result = build_fixture(args.output, args.files, args.duplicate_pairs, args.seed, args.byte_budget)
        elif args.command == "verify":
            result = verify_fixture(args.input)
        else:
            result = compare_series(args.baseline, args.candidate, args.metric,
                                    args.min_runs, args.max_regression_pct)
            if args.report:
                if args.report.exists() or args.report.is_symlink():
                    raise EvidenceError("report path must not exist; no overwrite")
                args.report.write_bytes(_canonical(result) + b"\n")
        print(json.dumps(result, sort_keys=True))
        return 0
    except (EvidenceError, OSError) as error:
        print(json.dumps({"gate": "BLOCKED", "reason": str(error), "certification": "NOT_CERTIFIED"}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
