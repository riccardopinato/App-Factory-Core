#!/usr/bin/env python3
"""Security/rename/Spec Lite regressions: offline only, source-only evidence."""
import json
import sys
import unittest
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from openspec_shadow_mode import (  # noqa: E402
    GitHubAPI, IncompleteSnapshot, MAX_API_REQUESTS,
    assess, markdown, safe_markdown, snapshot,
)
from test_openspec_shadow_mode import FakeAPI, REPO  # noqa: E402


class RenameAPI(FakeAPI):
    def get(self, path):
        response = super().get(path)
        if "/pulls/75/files?" in path and response:
            response[0]["status"] = "renamed"
            response[0]["previous_filename"] = "docs/old.md"
        return response


class InvalidRenameAPI(FakeAPI):
    def get(self, path):
        response = super().get(path)
        if "/pulls/75/files?" in path and response:
            response[0]["status"] = "renamed"
        return response


class ShadowAuditFixTests(unittest.TestCase):
    def assertBlocked(self, fn, reason):
        with self.assertRaisesRegex(IncompleteSnapshot, reason):
            fn()

    def test_shadow_python_sources_have_no_invalid_escape_warnings(self):
        for relative in ("scripts/openspec_shadow_mode.py",
                         "scripts/openspec_shadow_deep_triage.py"):
            code = (ROOT / relative).read_text(encoding="utf-8")
            with warnings.catch_warnings():
                warnings.simplefilter("error", SyntaxWarning)
                compile(code, str(ROOT / relative), "exec")

    def test_rename_origins_are_included_in_review_hints(self):
        api = RenameAPI({75: ["docs/new.md"], 77: ["docs/old.md"]})
        snap = snapshot(api, REPO)
        result = assess(snap)
        self.assertEqual(result["overlap_pair_count"], 1)
        self.assertEqual(result["overlap_pairs"][0]["prs"], [75, 77])
        self.assertEqual(result["overlap_pairs"][0]["sample_paths"], ["docs/old.md"])
        self.assertEqual(result["renamed_file_records"], 1)
        p = next(p for p in snap["prs"] if p["number"] == 75)
        self.assertEqual(p["changed_paths"], ["docs/new.md"])
        self.assertEqual(p["collision_paths"], ["docs/new.md", "docs/old.md"])

    def test_malformed_rename_missing_previous_filename_blocks(self):
        api = InvalidRenameAPI({75: ["docs/new.md"], 77: ["docs/old.md"]})
        self.assertBlocked(lambda: snapshot(api, REPO), "PR_RENAME_PRIOR_PATH_INVALID")

    def test_rename_same_filename_rejected(self):
        class SameName(RenameAPI):
            def get(self, path):
                x = super().get(path)
                if "/pulls/75/files?" in path and x:
                    x[0]["previous_filename"] = x[0]["filename"]
                return x
        self.assertBlocked(lambda: snapshot(SameName({75: ["docs/new.md"]}), REPO),
                           "PR_RENAME_PRIOR_PATH_INVALID")

    def test_markdown_single_line_escaping_and_no_runner_command(self):
        unsafe = "foo\n::error::secret<svg>[x](https://evil.invalid)*_" + chr(96) + "\\\x1b[31m"
        cleaned = safe_markdown(unsafe)
        self.assertNotIn("\n", cleaned)
        self.assertNotIn("\x1b", cleaned)
        self.assertNotIn("<svg>", cleaned)
        self.assertNotIn("[x](https://evil.invalid)", cleaned)
        self.assertIn("\\u000a", cleaned)
        self.assertIn("&lt;svg&gt;", cleaned)

    def test_untrusted_path_in_real_assessment_renders_safely(self):
        unsafe = "dir/a\n::add-mask::TOKEN<script>_" + chr(96) + "file.md"
        api = FakeAPI({75: [unsafe], 77: [unsafe]})
        report = assess(snapshot(api, REPO))
        out = markdown(report)
        self.assertEqual(report["overlap_pair_count"], 1)
        self.assertNotIn("\n::add-mask::", out)
        self.assertNotIn("<script>", out)
        self.assertIn("\\u000a", out)

    def test_github_api_request_budget_denies_before_any_network(self):
        api = GitHubAPI()
        api.request_count = MAX_API_REQUESTS
        self.assertBlocked(lambda: api.get("/repos/" + REPO),
                           "GITHUB_API_READ_BUDGET_EXCEEDED")

    def test_real_factory_spec_lite_example_maps_only_as_untrusted_proposal(self):
        source = json.loads((ROOT / "spec_lite/examples/FAST.json").read_text(encoding="utf-8"))
        source["target"]["repository"] = REPO
        api = FakeAPI({75: ["docs/spec_lite/gallery/manifest.json"]}, manifest=source)
        report = assess(snapshot(api, REPO))
        self.assertEqual(report["unmapped_requirement_prs"], [])
        self.assertEqual(report["competing_requirement_deltas"], [])
        self.assertFalse(report["semantic_absence_certified"])

    def test_real_factory_spec_lite_example_overlapping_prior_is_review_only(self):
        source = json.loads((ROOT / "spec_lite/examples/FAST.json").read_text(encoding="utf-8"))
        source["target"]["repository"] = REPO
        source["requirements"][0]["delta"] = {
            "operation": "MODIFIED",
            "previous": {"spec_id": "FSL-20261127-CANONICAL1", "requirement_id": "FR-001",
                         "source_sha": "f" * 40},
            "reason": "The original behavior must be updated for a bounded pilot.",
        }
        api = FakeAPI({75: ["docs/spec_lite/a/manifest.json"],
                       77: ["docs/spec_lite/b/manifest.json"]}, manifest=source)
        report = assess(snapshot(api, REPO))
        self.assertEqual(report["competing_requirement_deltas"][0]["prs"], [75, 77])
        self.assertFalse(report["competing_requirement_deltas"][0]["verified_product_conflict"])

    def test_manifest_invalid_schema_version_fails_closed(self):
        source = {"schema_version": 66, "spec_id": "FSL-20261127-SAMPLE",
                  "target": {"repository": REPO}, "requirements": [{"id": "FR-001"}]}
        api = FakeAPI({75: ["docs/spec_lite/a/manifest.json"]}, manifest=source)
        self.assertBlocked(lambda: snapshot(api, REPO), "MANIFEST_IDENTITY_INVALID")

    def test_malformed_manifest_base64_fails_closed(self):
        class BadBase64(FakeAPI):
            def get(self, path):
                if "/contents/" in path:
                    return {"encoding": "base64", "content": "!!!!not-valid-base64"}
                return super().get(path)
        api = BadBase64({75: ["docs/spec_lite/a/manifest.json"]}, manifest={})
        self.assertBlocked(lambda: snapshot(api, REPO), "MANIFEST_JSON_INVALID")

    def test_missing_manifest_does_not_claim_verified_semantic_coverage(self):
        api = FakeAPI({75: ["lib/changed.kt"]})
        report = assess(snapshot(api, REPO))
        self.assertEqual(report["unmapped_requirement_prs"], [75])
        self.assertFalse(report["semantic_absence_certified"])

    def test_duplicate_alias_in_one_pr_not_double_counted(self):
        class RenameAlias(FakeAPI):
            def get(self, path):
                items = super().get(path)
                if "/pulls/75/files?" in path and items:
                    items[0]["status"] = "renamed"
                    items[0]["previous_filename"] = "lib/old.kt"
                return items
        api = RenameAlias({75: ["lib/new.kt", "lib/old.kt"], 77: ["lib/old.kt"]})
        report = assess(snapshot(api, REPO))
        self.assertEqual(report["overlap_pairs"][0]["count"], 1)


if __name__ == "__main__":
    unittest.main()
