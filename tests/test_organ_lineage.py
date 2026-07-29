# SPDX-License-Identifier: GPL-3.0-only

import unittest

from velvet_continuity import (
    ContinuityReceiptBridge,
    ContinuitySpine,
    OrganLineageRecord,
    OrganTransition,
    ValidationError,
)


class OrganLineageRecordTests(unittest.TestCase):
    def record(self, **overrides):
        values = {
            "body_id": "velvet-founder",
            "organ": "velour",
            "transition": OrganTransition.PERMANENT_REPLACEMENT,
            "body_registry_revision": "body-registry-r12",
            "receipt_anchor": "receipt-abc-123",
            "reason": "original specialist node retired",
            "from_node_id": "velour-01",
            "to_node_id": "velour-02",
            "capabilities": ("logging", "receipt-indexing"),
            "created_at": "2026-07-29T02:00:00+00:00",
            "record_id": "organ-lineage-001",
        }
        values.update(overrides)
        return OrganLineageRecord(**values)

    def test_records_permanent_replacement(self):
        record = self.record()
        payload = record.to_dict()
        self.assertEqual(payload["record_kind"], "organ_lineage_record")
        self.assertEqual(payload["transition"], "permanent_replacement")
        self.assertEqual(payload["from_node_id"], "velour-01")
        self.assertEqual(payload["to_node_id"], "velour-02")
        self.assertTrue(payload["permanent"])
        self.assertTrue(payload["canonical"])
        self.assertFalse(payload["authority_granted"])

    def test_records_organ_join(self):
        record = self.record(
            transition=OrganTransition.JOINED,
            from_node_id=None,
            to_node_id="ruby-01",
            organ="ruby",
        )
        self.assertEqual(record.transition, OrganTransition.JOINED)

    def test_records_organ_departure(self):
        record = self.record(
            transition=OrganTransition.DEPARTED,
            from_node_id="ruby-01",
            to_node_id=None,
            organ="ruby",
            capabilities=(),
        )
        self.assertEqual(record.transition, OrganTransition.DEPARTED)

    def test_records_successor_assumption(self):
        record = self.record(
            transition=OrganTransition.SUCCESSOR_ASSUMED,
            previous_record_id="organ-lineage-000",
        )
        self.assertEqual(record.previous_record_id, "organ-lineage-000")

    def test_durable_capability_reassignment_requires_capabilities(self):
        with self.assertRaisesRegex(ValidationError, "requires at least one capability"):
            self.record(
                transition=OrganTransition.DURABLE_CAPABILITY_REASSIGNED,
                capabilities=(),
            )

    def test_rejects_temporary_workload_movement(self):
        with self.assertRaisesRegex(ValidationError, "temporary workload movement"):
            self.record(permanent=False)

    def test_rejects_noncanonical_lineage(self):
        with self.assertRaisesRegex(ValidationError, "canonical"):
            self.record(canonical=False)

    def test_rejects_authority_claim(self):
        with self.assertRaisesRegex(ValidationError, "continuity evidence is not authority"):
            self.record(authority_granted=True)

    def test_rejects_missing_receipt_anchor(self):
        with self.assertRaisesRegex(ValidationError, "receipt_anchor"):
            self.record(receipt_anchor="")

    def test_rejects_same_source_and_destination_node(self):
        with self.assertRaisesRegex(ValidationError, "distinct source and destination"):
            self.record(to_node_id="velour-01")

    def test_join_cannot_claim_source_node(self):
        with self.assertRaisesRegex(ValidationError, "cannot declare 'from_node_id'"):
            self.record(
                transition=OrganTransition.JOINED,
                from_node_id="old-node",
                to_node_id="new-node",
            )

    def test_departure_cannot_claim_destination_node(self):
        with self.assertRaisesRegex(ValidationError, "cannot declare 'to_node_id'"):
            self.record(
                transition=OrganTransition.DEPARTED,
                from_node_id="old-node",
                to_node_id="new-node",
            )

    def test_rejects_unrecognized_transition_string(self):
        with self.assertRaisesRegex(ValidationError, "must be an OrganTransition"):
            self.record(transition="overflow")

    def test_receipt_bridge_formats_durable_transition(self):
        envelope = ContinuityReceiptBridge().organ_lineage_recorded(self.record())
        self.assertEqual(envelope["event_type"], "ORGAN_LINEAGE_RECORDED")
        self.assertEqual(envelope["subject_id"], "organ-lineage-001")
        self.assertEqual(envelope["payload"]["receipt_anchor"], "receipt-abc-123")
        self.assertFalse(envelope["payload"]["authority_granted"])

    def test_spine_stores_and_retrieves_organ_lineage(self):
        spine = ContinuitySpine()
        record = self.record()
        envelope = spine.record_organ_lineage(record)
        stored = spine.get_organ_lineage(record.record_id)
        self.assertEqual(envelope["event_type"], "ORGAN_LINEAGE_RECORDED")
        self.assertEqual(stored, record.to_dict())

    def test_spine_rejects_wrong_record_type(self):
        with self.assertRaisesRegex(TypeError, "Expected OrganLineageRecord"):
            ContinuitySpine().record_organ_lineage({"record_id": "wrong"})

    def test_same_record_produces_same_payload(self):
        first = self.record().to_dict()
        second = self.record().to_dict()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
