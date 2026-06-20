# SPDX-License-Identifier: GPL-3.0-only
"""Tests for ContinuityReceiptBridge."""

import unittest
from velvet_continuity import (
    ContinuityReceiptBridge, ContextRecord, DriftEvent,
    IdentityRecord, LineageRecord, SurfaceBinding, ValidationError,
)

IDENTITY_KWARGS = dict(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
)

CONTEXT_KWARGS = dict(
    context_id="ctx-nav-001",
    name="Navigation Context",
    purpose="Bounded nav context.",
    allowed_memory_classes=("route-data",),
    denied_memory_classes=("identity-root",),
    active=True,
)

SURFACE_KWARGS = dict(
    surface_id="nav-primary",
    surface_type="nav",
    bound_instance_id="node-001",
    trusted_by="node-001",
    allowed_memory_classes=("route-data",),
    denied_memory_classes=("identity-root",),
)


def make_drift_event():
    return DriftEvent(
        drift_type="surface",
        severity="medium",
        expected="nav",
        observed="audio",
        action="review",
    )


class TestReceiptBridgeEnvelope(unittest.TestCase):

    def setUp(self):
        self.bridge = ContinuityReceiptBridge()

    def _check_envelope(self, result, expected_event_type, expected_subject):
        self.assertEqual(result["event_type"], expected_event_type)
        self.assertEqual(result["subject_id"], expected_subject)
        self.assertEqual(result["source"], "velvet-continuity-spine")
        self.assertIn("payload", result)
        self.assertIsInstance(result["payload"], dict)

    def test_identity_created(self):
        r = IdentityRecord(**IDENTITY_KWARGS)
        result = self.bridge.identity_created(r)
        self._check_envelope(result, "IDENTITY_CREATED", "node-001")
        self.assertIn("instance_id", result["payload"])
        self.assertNotIn("spark_id", result["payload"])

    def test_lineage_linked(self):
        r = LineageRecord(
            child_instance_id="node-002",
            parent_instance_id="node-001",
            relationship="successor",
        )
        result = self.bridge.lineage_linked(r)
        self._check_envelope(result, "LINEAGE_LINKED", "node-002")
        self.assertIn("child_instance_id", result["payload"])

    def test_context_recorded(self):
        r = ContextRecord(**CONTEXT_KWARGS)
        result = self.bridge.context_recorded(r)
        self._check_envelope(result, "CONTEXT_RECORDED", "ctx-nav-001")
        self.assertIn("context_id", result["payload"])
        self.assertNotIn("room_id", result["payload"])

    def test_drift_detected(self):
        result = self.bridge.drift_detected(make_drift_event(), "node-001")
        self._check_envelope(result, "DRIFT_DETECTED", "node-001")
        self.assertIn("drift_type", result["payload"])

    def test_surface_bound(self):
        b = SurfaceBinding(**SURFACE_KWARGS)
        result = self.bridge.surface_bound(b)
        self._check_envelope(result, "SURFACE_BOUND", "nav-primary")
        self.assertIn("bound_instance_id", result["payload"])
        self.assertNotIn("bound_spark_id", result["payload"])


class TestReceiptBridgeTypeSafety(unittest.TestCase):

    def setUp(self):
        self.bridge = ContinuityReceiptBridge()

    def test_identity_created_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.bridge.identity_created("not-a-record")

    def test_context_recorded_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.bridge.context_recorded({"context_id": "x"})

    def test_drift_detected_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.bridge.drift_detected("not-an-event", "node-001")

    def test_drift_detected_blank_subject_raises(self):
        with self.assertRaises(ValidationError):
            self.bridge.drift_detected(make_drift_event(), "")

    def test_format_event_wrong_payload_type_raises(self):
        with self.assertRaises(ValidationError):
            self.bridge.format_event("TEST", "not-a-dict", "node-001")

    def test_blank_source_raises(self):
        with self.assertRaises(ValidationError):
            ContinuityReceiptBridge(source="")


if __name__ == "__main__":
    unittest.main()
