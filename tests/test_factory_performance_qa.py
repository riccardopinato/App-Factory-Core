import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference_engines" / "performance_qa"))
from factory_performance_qa import (  # noqa: E402
    EvidenceError, build_fixture, compare_series, main, verify_fixture,
)


class FactoryPerformanceQaTests(unittest.TestCase):
    def test_fixture_is_reproducible_and_exactly_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "one"
            second = Path(tmp) / "two"
            a = build_fixture(first, files=84, duplicate_pairs=7, seed=42)
            b = build_fixture(second, files=84, duplicate_pairs=7, seed=42)
            self.assertEqual(a["fixture_id"], b["fixture_id"])
            p = verify_fixture(first)
            q = verify_fixture(second)
            self.assertEqual(p["verification"], "PASS")
            self.assertEqual(p, q)
            self.assertEqual(p["duplicate_pairs"], 7)
            self.assertEqual(len(list(first.glob("*.bin"))), 84)

    def test_refuses_existing_destination_without_mutating_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "existing"
            output.mkdir()
            keep = output / "personal-note.txt"
            keep.write_text("DO NOT TOUCH")
            with self.assertRaises(EvidenceError):
                build_fixture(output, files=10, duplicate_pairs=1)
            self.assertEqual(keep.read_text(), "DO NOT TOUCH")

    def test_malformed_manifest_shape_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "fixture"
            build_fixture(output, files=10, duplicate_pairs=2)
            (output / "manifest.json").write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(EvidenceError, "must be an object"):
                verify_fixture(output)

    def test_refuses_oversized_or_invalid_fixture_before_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "not-created"
            with self.assertRaises(EvidenceError):
                build_fixture(output, files=100_001, duplicate_pairs=0)
            with self.assertRaises(EvidenceError):
                build_fixture(output, files=100, duplicate_pairs=51)
            with self.assertRaises(EvidenceError):
                build_fixture(output, files=300, duplicate_pairs=0, byte_budget=100)
            self.assertFalse(output.exists())

    def test_detects_corrupt_missing_and_unknown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "fixture"
            build_fixture(target, files=10, duplicate_pairs=2)
            file0 = target / "synthetic_000000.bin"
            file0.write_bytes(b"changed payload")
            with self.assertRaises(EvidenceError):
                verify_fixture(target)
            target2 = Path(tmp) / "clean"
            build_fixture(target2, files=10, duplicate_pairs=2)
            (target2 / "surprise.bin").write_bytes(b"not expected")
            with self.assertRaises(EvidenceError):
                verify_fixture(target2)
            target3 = Path(tmp) / "missing"
            build_fixture(target3, files=10, duplicate_pairs=2)
            (target3 / "synthetic_000000.bin").unlink()
            with self.assertRaises(EvidenceError):
                verify_fixture(target3)

    @staticmethod
    def sample(source_sha, value, environment="emulator", fixture="f001", mode="cold"):
        return {
            "schema_version": 1, "fixture_id": fixture,
            "device": "Pixel-API35", "environment": environment, "api_level": 35,
            "mode": mode, "file_count": 1200, "rows_reused": 1200,
            "rows_replaced": 0, "integrity_digest": "sha256:" + "e" * 64,
            "source_sha": source_sha, "file_rows_ms": value,
        }

    def write_runs(self, path, values, source, **extra):
        path.write_text(
            "".join(json.dumps(self.sample(source, value, **extra)) + "\n" for value in values),
            encoding="utf-8",
        )

    def test_comparison_requires_matched_environment_and_three_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path(tmp) / "baseline.jsonl"
            new = Path(tmp) / "candidate.jsonl"
            self.write_runs(old, [110, 120, 130], "a" * 40)
            self.write_runs(new, [90, 100, 110], "b" * 40)
            result = compare_series(old, new)
            self.assertEqual(result["baseline_median"], 120)
            self.assertEqual(result["candidate_median"], 100)
            self.assertEqual(result["delta_pct"], -16.667)
            self.assertEqual(result["gate"], "PHYSICAL_REPLAY_REQUIRED")
            self.assertEqual(result["certification"], "NOT_CERTIFIED")
            self.write_runs(new, [90, 100, 110], "b" * 40, mode="warm")
            with self.assertRaisesRegex(EvidenceError, "INCOMPARABLE"):
                compare_series(old, new)
            self.write_runs(new, [90, 100], "b" * 40)
            with self.assertRaisesRegex(EvidenceError, "at least 3"):
                compare_series(old, new)

    def test_comparison_detects_regression_and_mixed_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path(tmp) / "baseline.jsonl"
            new = Path(tmp) / "candidate.jsonl"
            self.write_runs(old, [100, 100, 100], "a" * 40, environment="physical")
            self.write_runs(new, [115, 130, 120], "b" * 40, environment="physical")
            result = compare_series(old, new, max_regression_pct=5)
            self.assertEqual(result["gate"], "REVIEW_REGRESSION")
            self.assertEqual(result["delta_pct"], 20)
            new.write_text(
                json.dumps(self.sample("b" * 40, 99, environment="physical")) + "\n"
                + json.dumps(self.sample("c" * 40, 98, environment="physical")) + "\n"
                + json.dumps(self.sample("b" * 40, 97, environment="physical")) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(EvidenceError, "mixed"):
                compare_series(old, new)

    def test_cli_returns_failure_on_incomparable_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = Path(tmp) / "baseline.jsonl"
            new = Path(tmp) / "candidate.jsonl"
            self.write_runs(old, [100, 110, 100], "a" * 40)
            self.write_runs(new, [100, 110, 100], "b" * 40, fixture="different")
            self.assertEqual(main(["compare", "--baseline", str(old), "--candidate", str(new)]), 2)


if __name__ == "__main__":
    unittest.main()
