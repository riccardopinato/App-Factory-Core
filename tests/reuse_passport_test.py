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

    def test_legacy_does_not_auto_certify(self):
        p = dict(source_blob=None, test_blob=None)
        self.assertIn("NEEDS_FIRST_FILE_PIN", mod.check_checkout(p, pathlib.Path(".")))

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                mod.path_inside(pathlib.Path(temp), "../secrets")


if __name__ == "__main__":
    unittest.main()
