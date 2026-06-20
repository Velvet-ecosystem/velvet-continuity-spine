# SPDX-License-Identifier: GPL-3.0-only
"""Tests for SurfaceBinding."""

import unittest
from velvet_continuity import SurfaceBinding, ValidationError

VALID = dict(
    surface_id="nav-primary",
    surface_type="nav",
    bound_instance_id="node-001",
    trusted_by="node-001",
    allowed_memory_classes=("route-data", "waypoints"),
    denied_memory_classes=("identity-root",),
)


class TestSurfaceBindingConstruction(unittest.TestCase):

    def test_valid_construction(self):
        b = SurfaceBinding(**VALID)
        self.assertEqual(b.surface_id, "nav-primary")
        self.assertEqual(b.surface_type, "nav")
        self.assertEqual(b.bound_instance_id, "node-001")

    def test_to_dict_keys(self):
        b = SurfaceBinding(**VALID)
        d = b.to_dict()
        self.assertIn("bound_instance_id", d)
        self.assertNotIn("bound_spark_id", d)

    def test_to_dict_memory_classes_are_lists(self):
        b = SurfaceBinding(**VALID)
        d = b.to_dict()
        self.assertIsInstance(d["allowed_memory_classes"], list)
        self.assertIsInstance(d["denied_memory_classes"], list)

    def test_blank_surface_id_fails_closed(self):
        with self.assertRaises(ValidationError):
            SurfaceBinding(**{**VALID, "surface_id": ""})

    def test_blank_surface_type_fails_closed(self):
        with self.assertRaises(ValidationError):
            SurfaceBinding(**{**VALID, "surface_type": ""})

    def test_blank_bound_instance_id_fails_closed(self):
        with self.assertRaises(ValidationError):
            SurfaceBinding(**{**VALID, "bound_instance_id": ""})

    def test_blank_trusted_by_fails_closed(self):
        with self.assertRaises(ValidationError):
            SurfaceBinding(**{**VALID, "trusted_by": ""})

    def test_allowed_memory_classes_not_sequence_fails_closed(self):
        with self.assertRaises((ValidationError, TypeError)):
            SurfaceBinding(**{**VALID, "allowed_memory_classes": "route-data"})

    def test_receipt_anchor_optional(self):
        b = SurfaceBinding(**VALID)
        self.assertIsNone(b.receipt_anchor)

    def test_receipt_anchor_set(self):
        b = SurfaceBinding(**VALID, receipt_anchor="sha256:abc")
        self.assertEqual(b.receipt_anchor, "sha256:abc")

    def test_blank_receipt_anchor_fails_closed(self):
        with self.assertRaises(ValidationError):
            SurfaceBinding(**VALID, receipt_anchor="")

    def test_frozen(self):
        b = SurfaceBinding(**VALID)
        with self.assertRaises((AttributeError, TypeError)):
            b.surface_type = "audio"

    def test_binding_id_auto_generated(self):
        b = SurfaceBinding(**VALID)
        self.assertTrue(b.binding_id)


if __name__ == "__main__":
    unittest.main()
