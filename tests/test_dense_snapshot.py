"""Regression checks for reusing a snapshot across Windows path spellings."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import dense_retrieval


class SnapshotPathTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.day6 = self.root / "Day6"
        self.source = self.day6 / ".local/chroma"
        self.source.mkdir(parents=True)
        self.target = self.root / "Day7/.local/day6_chroma"
        self.target.mkdir(parents=True)
        self.marker = self.target / "day7_snapshot.json"
        self.patch = patch.object(dense_retrieval, "ROOT", self.root / "Day7")
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def write_marker(self, source):
        self.marker.write_text(json.dumps({"source_path": str(source), "source_file_sha256": {}}), encoding="utf-8")
        (self.target / "chroma.sqlite3").write_bytes(b"existing database fixture")

    @unittest.skipUnless(os.name == "nt", "Windows path case regression")
    def test_same_directory_with_different_case(self):
        self.write_marker(str(self.source).swapcase())
        target, _ = dense_retrieval.snapshot_store(self.day6)
        self.assertTrue(target.samefile(self.target))

    def test_different_directory_is_rejected(self):
        other = self.root / "OtherDatabase"
        other.mkdir()
        self.write_marker(other)
        with self.assertRaisesRegex(ValueError, "Snapshot source differs"):
            dense_retrieval.snapshot_store(self.day6)

    def test_missing_marker_rebuilds_and_preserves_old_copy(self):
        (self.source / "chroma.sqlite3").write_bytes(b"source database fixture")
        (self.target / "keep.txt").write_text("old copy", encoding="utf-8")
        # Reproduce WinError 5 for ANY directory rename. Recovery must not use it.
        with patch.object(Path, "rename", side_effect=PermissionError("WinError 5")):
            target, info = dense_retrieval.snapshot_store(self.day6)
        self.assertEqual((target / "chroma.sqlite3").read_bytes(), b"source database fixture")
        self.assertTrue((target / "day7_snapshot.json").is_file())
        self.assertNotEqual(target, self.target)
        self.assertEqual((self.target / "keep.txt").read_text(), "old copy")
        self.assertEqual(info["source_path"], str(self.source.resolve()))
        with patch.object(Path, "rename", side_effect=PermissionError("WinError 5")):
            reused, _ = dense_retrieval.snapshot_store(self.day6)
        self.assertEqual(reused, target)

    def test_missing_source_does_not_move_incomplete_snapshot(self):
        (self.target / "keep.txt").write_text("old copy", encoding="utf-8")
        with self.assertRaises(FileNotFoundError):
            dense_retrieval.snapshot_store(self.day6)
        self.assertEqual((self.target / "keep.txt").read_text(), "old copy")


if __name__ == "__main__":
    unittest.main()
