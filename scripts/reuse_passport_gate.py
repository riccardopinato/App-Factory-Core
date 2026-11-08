#!/usr/bin/env python3
"""Offline reuse passport manifest verifier and donor checkout blob gate."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{40}$")


def git_blob_sha(payload: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + bytes([0]) + payload).hexdigest()


def path_inside(root: Path, relative: str) -> Path:
    if not relative or relative.startswith("/") or "\\" in relative or ".." in Path(relative).parts:
        raise ValueError("unsafe checkout-relative path")
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("escaped checkout")
    return target


def load():
    data = json.loads((ROOT / "donors/REGISTRO_DONOR_CAPABILITY.json").read_text(encoding="utf8"))
    cache = json.loads((ROOT / "reuse/PASSPORTS.json").read_text(encoding="utf8"))
    recs = data["records"]
    ps = cache["passports"]
    if len(recs) != 20 or len(ps) != 20:
        raise ValueError("required 20 distinct scoped contracts/passports")
    ids = {r["id"] for r in recs}
    if len(ids) != 20 or ids != {p["id"] for p in ps}:
        raise ValueError("donor/passport IDs drift")
    for r, p in zip(recs, ps):
        if r["id"] != p["id"] or r["source_sha"] != p["source_sha"] or r["ci_url"] != p["ci_url"]:
            raise ValueError("index drift")
        if not SHA.fullmatch(r["source_sha"]):
            raise ValueError("invalid source SHA")
        if not r["ci_url"].startswith("https://github.com/riccardopinato/"):
            raise ValueError("missing evidence")
        for key in ("source_blob_sha", "test_blob_sha"):
            value = r[key]
            if value is not None and not SHA.fullmatch(value):
                raise ValueError("invalid blob SHA")
        for key in ("source_path", "test_path"):
            path_inside(Path("/tmp/donor-checkout"), r[key])
        if r["evidence"] == "E3_EXACT_HEAD_TESTS" and not r["source_blob_sha"]:
            raise ValueError("E3 new entry without blob")
    return ps


def check_checkout(passport: dict, checkout: Path) -> str:
    a, b = passport.get("source_blob"), passport.get("test_blob")
    if not a or not b:
        return "LEGACY_PASS: NEEDS_FIRST_FILE_PIN_NO_FAST_SKIP"
    pairs = [(passport["source_path"], a), (passport["test_path"], b)]
    for relative, blob in pairs:
        file = path_inside(checkout, relative)
        if not file.is_file() or git_blob_sha(file.read_bytes()) != blob:
            return "INVALIDATED: RECHECK_CHANGED_SCOPE_" + relative
    return "MATCH: DONOR_E3_REUSE_OK_CONSUMER_TESTS_REQUIRED"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--passport")
    parser.add_argument("--source-root")
    args = parser.parse_args()
    ps = load()
    if args.passport:
        p = next((p for p in ps if p["id"] == args.passport), None)
        if not p:
            raise SystemExit("passport not found")
        if not args.source_root:
            raise SystemExit("--source-root is required")
        result = check_checkout(p, Path(args.source_root))
        print(result)
        if result.startswith("INVALIDATED"):
            raise SystemExit(2)
    else:
        print(f"REUSE PASSPORT VALID: {len(ps)} scoped contracts; consumer gates preserved")


if __name__ == "__main__":
    main()
