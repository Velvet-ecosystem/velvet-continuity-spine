# SPDX-License-Identifier: GPL-3.0-only
"""Tests for MemoryIndex."""

import unittest
from velvet_continuity.memory_index import MemoryIndex


class TestMemoryIndex(unittest.TestCase):

    def setUp(self):
        self.index = MemoryIndex()

    def test_add_and_get(self):
        self.index.add("node-001", {"instance_id": "node-001"})
        result = self.index.get("node-001")
        self.assertEqual(result["instance_id"], "node-001")

    def test_get_returns_copy(self):
        self.index.add("node-001", {"instance_id": "node-001"})
        result = self.index.get("node-001")
        result["instance_id"] = "mutated"
        self.assertEqual(self.index.get("node-001")["instance_id"], "node-001")

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.index.get("does-not-exist"))

    def test_add_overwrites_existing(self):
        self.index.add("node-001", {"v": 1})
        self.index.add("node-001", {"v": 2})
        self.assertEqual(self.index.get("node-001")["v"], 2)

    def test_add_empty_key_raises(self):
        with self.assertRaises(ValueError):
            self.index.add("", {"instance_id": "x"})

    def test_add_non_dict_value_raises(self):
        with self.assertRaises(TypeError):
            self.index.add("node-001", "not-a-dict")

    def test_remove_existing_returns_true(self):
        self.index.add("node-001", {"instance_id": "node-001"})
        removed = self.index.remove("node-001")
        self.assertTrue(removed)
        self.assertIsNone(self.index.get("node-001"))

    def test_remove_missing_returns_false(self):
        self.assertFalse(self.index.remove("does-not-exist"))

    def test_keys_returns_sorted(self):
        self.index.add("node-002", {})
        self.index.add("node-001", {})
        self.assertEqual(self.index.keys(), ["node-001", "node-002"])

    def test_len(self):
        self.assertEqual(len(self.index), 0)
        self.index.add("node-001", {})
        self.assertEqual(len(self.index), 1)


if __name__ == "__main__":
    unittest.main()
