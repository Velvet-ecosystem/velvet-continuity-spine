# SPDX-License-Identifier: GPL-3.0-only
"""Tests for IdentityRecord."""

import unittest
from velvet_continuity import IdentityRecord, ValidationError

# Neutral placeholder values — no private names
VALID = dict(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
)


class TestIdentityRecordConstruction(unittest.TestCase):

    def test_valid_construction(self):
        r = IdentityRecord(**VALID)
        self.assertEqual(r.instance_id, "node-001")
        self.assertEqual(r.role, "navigator")
        self.assertTrue(r.is_genesis())

    def test_with_lineage_parent(self):
        r = IdentityRecord(**VALID, lineage_parent="node-000")
        self.assertFalse(r.is_genesis())
        self.assertTrue(r.has_lineage_parent())

    def test_without_lineage_parent(self):
        r = IdentityRecord(**VALID)
        self.assertFalse(r.has_lineage_parent())

    def test_with_receipt_anchor(self):
        r = IdentityRecord(**VALID, receipt_chain_anchor="sha256:genesis")
        self.assertTrue(r.has_receipt_anchor())

    def test_without_receipt_anchor(self):
        r = IdentityRecord(**VALID)
        self.assertFalse(r.has_receipt_anchor())

    def test_blank_instance_id_fails_closed(self):
        with self.assertRaises(ValidationError):
            IdentityRecord(**{**VALID, "instance_id": ""})

    def test_whitespace_instance_id_fails_closed(self):
        with self.assertRaises(ValidationError):
            IdentityRecord(**{**VALID, "instance_id": "   "})

    def test_blank_role_fails_closed(self):
        with self.assertRaises(ValidationError):
            IdentityRecord(**{**VALID, "role": ""})

    def test_blank_runtime_class_fails_closed(self):
        with self.assertRaises(ValidationError):
            IdentityRecord(**{**VALID, "runtime_class": ""})

    def test_blank_surface_fails_closed(self):
        with self.assertRaises(ValidationError):
            IdentityRecord(**{**VALID, "surface": ""})

    def test_blank_memory_scope_fails_closed(self):
        with self.assertRaises(ValidationError):
            IdentityRecord(**{**VALID, "memory_scope": ""})

    def test_blank_authority_scope_fails_closed(self):
        with self.assertRaises(ValidationError):
            IdentityRecord(**{**VALID, "authority_scope": ""})

    def test_frozen(self):
        r = IdentityRecord(**VALID)
        with self.assertRaises((AttributeError, TypeError)):
            r.instance_id = "other"

    def test_to_dict_keys(self):
        r = IdentityRecord(**VALID)
        d = r.to_dict()
        self.assertIn("instance_id", d)
        self.assertIn("runtime_class", d)
        self.assertNotIn("spark_id", d)
        self.assertNotIn("stem", d)

    def test_record_id_auto_generated(self):
        r = IdentityRecord(**VALID)
        self.assertTrue(r.record_id)

    def test_created_at_auto_generated(self):
        r = IdentityRecord(**VALID)
        self.assertTrue(r.created_at)


if __name__ == "__main__":
    unittest.main()
