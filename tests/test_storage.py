# SPDX-License-Identifier: GPL-3.0-only
"""Tests for storage helpers."""

import json
import tempfile
import unittest
from pathlib import Path
from velvet_continuity.storage import write_json, read_json


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_write_and_read_roundtrip(self):
        path = self.base / "test.json"
        payload = {"instance_id": "node-001", "active": True}
        write_json(path, payload)
        result = read_json(path)
        self.assertEqual(result["instance_id"], "node-001")
        self.assertTrue(result["active"])

    def test_write_creates_parent_dirs(self):
        path = self.base / "subdir" / "deep" / "record.json"
        write_json(path, {"key": "value"})
        self.assertTrue(path.exists())

    def test_read_non_object_raises(self):
        path = self.base / "array.json"
        path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
        with self.assertRaises(ValueError):
            read_json(path)

    def test_read_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            read_json(self.base / "does-not-exist.json")

    def test_written_file_is_valid_json(self):
        path = self.base / "test.json"
        write_json(path, {"x": 1})
        raw = path.read_text(encoding="utf-8")
        parsed = json.loads(raw)
        self.assertEqual(parsed["x"], 1)


if __name__ == "__main__":
    unittest.main()
