# SPDX-License-Identifier: GPL-3.0-only
"""Tests for ContextRecord (formerly RoomRecord)."""

import unittest
from velvet_continuity import ContextRecord, ValidationError

VALID = dict(
    context_id="ctx-nav-001",
    name="Navigation Context",
    purpose="Bounded context for navigation surface operations.",
    allowed_memory_classes=("route-data", "waypoints"),
    denied_memory_classes=("identity-root", "authority-tokens"),
)


class TestContextRecordConstruction(unittest.TestCase):

    def test_valid_construction(self):
        r = ContextRecord(**VALID)
        self.assertEqual(r.context_id, "ctx-nav-001")
        self.assertFalse(r.active)

    def test_active_true(self):
        r = ContextRecord(**VALID, active=True)
        self.assertTrue(r.active)

    def test_allows(self):
        r = ContextRecord(**VALID)
        self.assertTrue(r.allows("route-data"))
        self.assertFalse(r.allows("identity-root"))

    def test_denies(self):
        r = ContextRecord(**VALID)
        self.assertTrue(r.denies("identity-root"))
        self.assertFalse(r.denies("route-data"))

    def test_to_dict_keys(self):
        r = ContextRecord(**VALID)
        d = r.to_dict()
        self.assertIn("context_id", d)
        self.assertIn("allowed_memory_classes", d)
        self.assertNotIn("room_id", d)

    def test_to_dict_memory_classes_are_lists(self):
        r = ContextRecord(**VALID)
        d = r.to_dict()
        self.assertIsInstance(d["allowed_memory_classes"], list)
        self.assertIsInstance(d["denied_memory_classes"], list)

    def test_blank_context_id_fails_closed(self):
        with self.assertRaises(ValidationError):
            ContextRecord(**{**VALID, "context_id": ""})

    def test_blank_purpose_fails_closed(self):
        with self.assertRaises(ValidationError):
            ContextRecord(**{**VALID, "purpose": ""})

    def test_allowed_memory_classes_not_sequence_fails_closed(self):
        with self.assertRaises((ValidationError, TypeError)):
            ContextRecord(**{**VALID, "allowed_memory_classes": "route-data"})

    def test_allowed_memory_classes_with_empty_string_fails_closed(self):
        with self.assertRaises(ValidationError):
            ContextRecord(**{**VALID, "allowed_memory_classes": ("route-data", "")})

    def test_active_non_bool_raises(self):
        with self.assertRaises(TypeError):
            ContextRecord(**VALID, active="yes")

    def test_frozen(self):
        r = ContextRecord(**VALID)
        with self.assertRaises((AttributeError, TypeError)):
            r.active = True

    def test_record_id_auto_generated(self):
        r = ContextRecord(**VALID)
        self.assertTrue(r.record_id)


if __name__ == "__main__":
    unittest.main()
