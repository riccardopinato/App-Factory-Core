import importlib.util
import pathlib
import tempfile
import unittest

P = pathlib.Path(__file__).resolve().parents[1]
S = importlib.util.spec_from_file_location("reuse_gate", P / "scripts/reuse_passport_gate.py")
mod = importlib.util.module_from_spec(S)
S.loader.exec_module(mod)


class ReusePassportTests(unittest.TestCase):
    def test_registry_has_20_valid_contracts(self):
        self.assertEqual(len(mod.load()), 20)

    def test_six_legacy_donors_now_have_exact_e3_proofs(self):
        ids = {"anna_media", "notes_links", "camper_backup", "world_content_pack", "battery_estimation", "phone_security_policy"}
        data = mod.json.loads((P / "donors/REGISTRO_DONOR_CAPABILITY.json").read_text())
        passports = {p["id"]: p for p in mod.load()}
        records = {r["id"]: r for r in data["records"]}
        self.assertEqual(len([r for r in records.values() if r["evidence"] == "E3_EXACT_HEAD_TESTS"]), 15)
        for ident in ids:
            item = records[ident]
            passport = passports[ident]
            self.assertEqual(item["status"], "CERTIFIED_DONOR_SCOPED")
            self.assertEqual(item["source_sha"], item["e3_admission"]["exact_run_head_sha"])
            self.assertTrue(item["e3_admission"]["source_blob_same_on_main"])
            self.assertTrue(item["e3_admission"]["test_blob_same_on_main"])
            self.assertEqual(passport["source_blob"], item["source_blob_sha"])
            self.assertEqual(passport["test_blob"], item["test_blob_sha"])
        self.assertEqual(records["send_upload_bounds"]["status"], "SOURCE_CANDIDATE")

    def test_matching_and_changed_blob(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            (root / "lib").mkdir()
            (root / "lib" / "source.dart").write_bytes(b"source")
            (root / "lib" / "test.dart").write_bytes(b"test")
            p = dict(source_path="lib/source.dart", source_blob=mod.git_blob_sha(b"source"),
                     test_path="lib/test.dart", test_blob=mod.git_blob_sha(b"test"))
            self.assertTrue(mod.check_checkout(p, root).startswith("MATCH:"))
            (root / "lib" / "source.dart").write_bytes(b"new")
            self.assertTrue(mod.check_checkout(p, root).startswith("INVALIDATED:"))

    def test_passport_fields_identical_to_donor_record(self):
        items = mod.load()
        self.assertEqual(len(items), 20)
        data = mod.json.loads((P / "donors/REGISTRO_DONOR_CAPABILITY.json").read_text())
        r = next(x for x in data["records"] if x["id"] == "focus_score")
        p = next(x for x in items if x["id"] == "focus_score")
        self.assertEqual(p["source_blob"], r["source_blob_sha"])
        self.assertEqual(p["source_path"], r["source_path"])
        # Tamper test remains an explicit invariant in load() itself.
    
    def test_legacy_does_not_auto_certify(self):
        p = dict(source_blob=None, test_blob=None)
        self.assertIn("NEEDS_FIRST_FILE_PIN", mod.check_checkout(p, pathlib.Path(".")))

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                mod.path_inside(pathlib.Path(temp), "../secrets")


if __name__ == "__main__":
    unittest.main()
