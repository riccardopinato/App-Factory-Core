#!/usr/bin/env python3
"""Offline regression tests for paid-evaluation checkpoint handling.

Synthetic values exist ONLY in a temporary test directory. This file never
calls an API and never constitutes real model or policy evidence.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_v27d2_models as runner


class CheckpointTests(unittest.TestCase):
    def test_resume_uses_only_unpaid_pending_cases_and_rejects_tampering(self):
        calls = []

        def fake_perform(prompt, model, effort, timeout):
            calls.append(runner.eval_d2.sha(prompt))
            reply = {
                "decision": "DIRECT", "gates": ["UNIT_TEST_ONLY"],
                "rationale": "Synthetic mock; not policy evidence.",
                "proposed_actions": [],
            }
            return {
                "source_kind": "ACTUAL_MODEL_RUN",  # Mocked return, never provider evidence.
                "request_id": f"mock-unit-test-{len(calls)}",
                "model": model, "effort": effort,
                "elapsed_ms": 1.0, "input_tokens": 100,
                "output_tokens": 50, "response_text": json.dumps(reply),
                "decision": reply["decision"], "gates": reply["gates"],
                "reasoning_tokens": 0,
            }

        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "offline-unit-test.json"
            def invoke(limit):
                args = ["runner", "--confirm-paid-run",
                        "--model", "gpt-6.1-sol", "--effort", "high",
                        "--max-new-requests", str(limit),
                        "--out", str(artifact)]
                with patch.object(sys, "argv", args), patch.dict(
                    os.environ, {"OPENAI_API_KEY": "MOCK_ONLY"}
                ), patch.object(runner, "perform", side_effect=fake_perform):
                    runner.main()

            invoke(2)
            first = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertFalse(first["completed"])
            self.assertEqual(len(first["records"]), 2)
            self.assertEqual(len(calls), 2)

            invoke(2)
            second = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertFalse(second["completed"])
            self.assertEqual(len(second["records"]), 4)
            self.assertEqual(len(calls), 4)
            self.assertEqual(len({r["request_id"] for r in second["records"]}), 4)

            corrupt = json.loads(artifact.read_text(encoding="utf-8"))
            corrupt["records"][0]["prompt_sha256"] = "0" * 64
            artifact.write_text(json.dumps(corrupt), encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "Resume rejected"):
                invoke(2)
            self.assertEqual(len(calls), 4, "tampered resume incurred new mock calls")

            artifact.write_text(json.dumps(second), encoding="utf-8")
            invoke(32)
            final = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertTrue(final["completed"])
            self.assertEqual(len(final["records"]), 32)
            self.assertEqual(len(calls), 32)
            with self.assertRaisesRegex(SystemExit, "Resume rejected"):
                invoke(2)
            self.assertEqual(len(calls), 32, "completed artifact incurred new mock calls")


if __name__ == "__main__":
    unittest.main()
