# SPDX-License-Identifier: GPL-3.0-only
"""Tests for LineageRecord and lineage helpers."""

import unittest
from velvet_continuity import (
    IdentityRecord, LineageRecord, ValidationError,
    verify_parent_link, verify_receipt_anchor,
)

VALID_LINEAGE = dict(
    child_instance_id="node-002",
    parent_instance_id="node-001",
    relationship="successor",
)

PARENT_IDENTITY = dict(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
)

CHILD_IDENTITY = dict(
    instance_id="node-002",
    name="Node Beta",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
    lineage_parent="node-001",
)


class TestLineageRecordConstruction(unittest.TestCase):

    def test_valid_construction(self):
        r = LineageRecord(**VALID_LINEAGE)
        self.assertEqual(r.child_instance_id, "node-002")
        self.assertEqual(r.parent_instance_id, "node-001")
        self.assertEqual(r.relationship, "successor")

    def test_to_dict_keys(self):
        r = LineageRecord(**VALID_LINEAGE)
        d = r.to_dict()
        self.assertIn("child_instance_id", d)
        self.assertIn("parent_instance_id", d)
        self.assertNotIn("child_spark_id", d)
        self.assertNotIn("parent_spark_id", d)

    def test_with_receipt_anchor(self):
        r = LineageRecord(**VALID_LINEAGE, receipt_anchor="sha256:abc")
        self.assertEqual(r.receipt_anchor, "sha256:abc")

    def test_blank_child_instance_id_fails_closed(self):
        with self.assertRaises(ValidationError):
            LineageRecord(**{**VALID_LINEAGE, "child_instance_id": ""})

    def test_blank_parent_instance_id_fails_closed(self):
        with self.assertRaises(ValidationError):
            LineageRecord(**{**VALID_LINEAGE, "parent_instance_id": ""})

    def test_blank_relationship_fails_closed(self):
        with self.assertRaises(ValidationError):
            LineageRecord(**{**VALID_LINEAGE, "relationship": ""})

    def test_frozen(self):
        r = LineageRecord(**VALID_LINEAGE)
        with self.assertRaises((AttributeError, TypeError)):
            r.relationship = "fork"

    def test_lineage_id_auto_generated(self):
        r = LineageRecord(**VALID_LINEAGE)
        self.assertTrue(r.lineage_id)


class TestVerifyHelpers(unittest.TestCase):

    def test_verify_parent_link_true(self):
        parent = IdentityRecord(**PARENT_IDENTITY)
        child = IdentityRecord(**CHILD_IDENTITY)
        self.assertTrue(verify_parent_link(child, parent))

    def test_verify_parent_link_false(self):
        parent = IdentityRecord(**PARENT_IDENTITY)
        child = IdentityRecord(**{**CHILD_IDENTITY, "lineage_parent": "node-999"})
        self.assertFalse(verify_parent_link(child, parent))

    def test_verify_receipt_anchor_with_anchor(self):
        r = IdentityRecord(**PARENT_IDENTITY, receipt_chain_anchor="sha256:genesis")
        self.assertTrue(verify_receipt_anchor(r))

    def test_verify_receipt_anchor_without_anchor(self):
        r = IdentityRecord(**PARENT_IDENTITY)
        self.assertFalse(verify_receipt_anchor(r))


if __name__ == "__main__":
    unittest.main()
