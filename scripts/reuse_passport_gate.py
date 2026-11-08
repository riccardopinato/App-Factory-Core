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
        # A changed passport path/hash could falsely authorize unrelated source.
        fields = {
            "source": "source_repo", "source_sha": "source_sha",
            "source_blob": "source_blob_sha", "test_blob": "test_blob_sha",
            "source_path": "source_path", "test_path": "test_path",
            "ci_url": "ci_url", "certificate": "evidence",
            "scope": "scope", "exclusions": "excluded",
        }
        if any(p.get(pk) != r.get(rk) for pk, rk in fields.items()):
            raise ValueError("PASSPORT_SOURCE_OR_EVIDENCE_DRIFT: " + r["id"])
        if p.get("consumer_gate") != "FOCUSED_ADAPTER_TESTS; physical/provider/store only if in scope":
            raise ValueError("PASSPORT_CONSUMER_GATE_DRIFT: " + r["id"])

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
        if r["evidence"] == "E3_EXACT_HEAD_TESTS":
            if not r["source_blob_sha"] or not r["test_blob_sha"]:
                raise ValueError("E3 certificate requires both source and test fingerprint")
            if "e3_admission" in r:
                proof = r["e3_admission"]
                if (proof["exact_run_head_sha"] != r["source_sha"]
                        or not proof["source_blob_same_on_main"]
                        or not proof["test_blob_same_on_main"]
                        or p.get("e3_admission") != proof):
                    raise ValueError("E3 proof does not match source/Passport")
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
