#!/usr/bin/env python3
"""Fail-closed tests for active Master alias and structured Golden admission."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from factory_integrity import verify_active_master_alias
from golden_admission import classify_legacy_status, check_admission, requires_review, reuse_scope


class HardeningTests(unittest.TestCase):
    def test_active_master_alias_positive_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = Path(tmp) / "core.txt"
            alias = Path(tmp) / "alias.txt"
            core.write_bytes(b"CURRENT v27 bytes\n")
            alias.write_bytes(core.read_bytes())
            verify_active_master_alias(core, alias)
            alias.write_bytes(alias.read_bytes() + b"TAMPER")
            with self.assertRaisesRegex(ValueError, "alias drift"):
                verify_active_master_alias(core, alias)

    def test_candidate_without_draft_is_not_admitted(self):
        entry = dict(id="ecosystem_bridge", status="CANDIDATE — NON COPY-READY",
                     admission_level="CANDIDATE", freshness_status="CURRENT")
        self.assertTrue(requires_review(entry))
        self.assertEqual(reuse_scope(entry), "NOT_AUTO_ADMISSIBLE")

    def test_freshness_does_not_certify_donor(self):
        e = dict(id="a", status="CERTIFIED DONOR — SCOPED TEST/CI EVIDENCE",
                 admission_level="CERTIFIED_DONOR", freshness_status="CURRENT")
        self.assertFalse(requires_review(e))
        self.assertEqual(reuse_scope(e), "E3_SCOPED_DONOR_CONSUMER_VERIFICATION_REQUIRED")

    def test_unknown_label_and_mismatch_fail_closed(self):
        self.assertEqual(classify_legacy_status("COPY-READY PROCESS"), "COPY_READY")
        with self.assertRaises(ValueError):
            classify_legacy_status("AVAILABLE")
        with self.assertRaises(ValueError):
            check_admission(dict(id="x",status="DRAFT / CANDIDATE",
                                 admission_level="CERTIFIED_GOLDEN"))

    def test_deprecated_never_auto_selected(self):
        x = dict(id="old",status="DEPRECATED",admission_level="DEPRECATED",
                 freshness_status="CURRENT")
        self.assertTrue(requires_review(x))


if __name__ == "__main__":
    unittest.main(verbosity=2)
