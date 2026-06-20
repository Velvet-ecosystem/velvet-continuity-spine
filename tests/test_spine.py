# SPDX-License-Identifier: GPL-3.0-only
"""Tests for ContinuitySpine."""

import unittest
from velvet_continuity import ContinuitySpine, IdentityRecord, DriftEvent

IDENTITY_KWARGS = dict(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
    receipt_chain_anchor="sha256:genesis",
)


class TestContinuitySpine(unittest.TestCase):

    def setUp(self):
        self.spine = ContinuitySpine()

    def test_register_identity_returns_receipt_payload(self):
        r = IdentityRecord(**IDENTITY_KWARGS)
        payload = self.spine.register_identity(r)
        self.assertEqual(payload["event_type"], "IDENTITY_CREATED")
        self.assertEqual(payload["subject_id"], "node-001")

    def test_register_identity_stores_in_index(self):
        r = IdentityRecord(**IDENTITY_KWARGS)
        self.spine.register_identity(r)
        stored = self.spine.get_identity("node-001")
        self.assertIsNotNone(stored)
        self.assertEqual(stored["instance_id"], "node-001")

    def test_get_identity_missing_returns_none(self):
        result = self.spine.get_identity("does-not-exist")
        self.assertIsNone(result)

    def test_compare_identity_no_drift(self):
        r = IdentityRecord(**IDENTITY_KWARGS)
        events = self.spine.compare_identity(r, r)
        self.assertEqual(events, [])

    def test_compare_identity_detects_surface_drift(self):
        expected = IdentityRecord(**IDENTITY_KWARGS)
        observed = IdentityRecord(**{**IDENTITY_KWARGS, "surface": "audio"})
        events = self.spine.compare_identity(expected, observed)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].drift_type, "surface")

    def test_register_identity_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.spine.register_identity("not-a-record")


if __name__ == "__main__":
    unittest.main()
