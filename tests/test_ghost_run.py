# SPDX-License-Identifier: GPL-3.0-only
"""Tests for public-safe Ghost System continuity records."""

import unittest

from velvet_continuity import ContinuityReceiptBridge, ContinuitySpine, GhostRunRecord, ValidationError

VALID_KWARGS = dict(
    run_id="ghost-run-001",
    observation_event_id="ghost-event-001",
    receipt_anchor="receipt:ghost-can-001",
    repo_fingerprints=("velvet-vehicle-can@ghost-system-v0", "velvet-runtime@ghost-system-v0"),
    observed_frame_count=4,
)


class TestGhostRunRecord(unittest.TestCase):
    def test_valid_record_to_dict(self):
        payload = GhostRunRecord(**VALID_KWARGS).to_dict()
        self.assertEqual(payload["record_kind"], "ghost_run_record")
        self.assertEqual(payload["event_type"], "vehicle.can.ghost_observation")
        self.assertTrue(payload["read_only"])
        self.assertFalse(payload["authority_granted"])

    def test_public_safe_flags(self):
        record = GhostRunRecord(**VALID_KWARGS)
        self.assertTrue(record.is_public_safe())

    def test_wrong_event_type_rejected(self):
        with self.assertRaises(ValidationError):
            GhostRunRecord(**dict(VALID_KWARGS, event_type="vehicle.can.live"))

    def test_opened_bus_rejected(self):
        with self.assertRaises(ValidationError):
            GhostRunRecord(**dict(VALID_KWARGS, physical_bus_opened=True))

    def test_transmission_attempt_rejected(self):
        with self.assertRaises(ValidationError):
            GhostRunRecord(**dict(VALID_KWARGS, can_transmission_attempted=True))

    def test_actuation_rejected(self):
        with self.assertRaises(ValidationError):
            GhostRunRecord(**dict(VALID_KWARGS, actuation_performed=True))

    def test_authority_rejected(self):
        with self.assertRaises(ValidationError):
            GhostRunRecord(**dict(VALID_KWARGS, authority_granted=True))


class TestGhostRunReceiptBridge(unittest.TestCase):
    def test_ghost_run_recorded_envelope(self):
        payload = ContinuityReceiptBridge().ghost_run_recorded(GhostRunRecord(**VALID_KWARGS))
        self.assertEqual(payload["event_type"], "GHOST_RUN_RECORDED")
        self.assertEqual(payload["subject_id"], "ghost-run-001")


class TestGhostRunContinuitySpine(unittest.TestCase):
    def test_record_ghost_run_stores_and_returns_receipt_payload(self):
        spine = ContinuitySpine()
        receipt_payload = spine.record_ghost_run(GhostRunRecord(**VALID_KWARGS))
        self.assertEqual(receipt_payload["event_type"], "GHOST_RUN_RECORDED")
        self.assertEqual(spine.get_ghost_run("ghost-run-001")["run_id"], "ghost-run-001")


if __name__ == "__main__":
    unittest.main()
