# SPDX-License-Identifier: GPL-3.0-only

import unittest

from continuity_spine.memory_anchor import MemoryAnchor, validate_memory_anchor


class MemoryAnchorTests(unittest.TestCase):
    def test_builds_public_safe_anchor(self):
        record = MemoryAnchor(
            memory_event_id="memory-1",
            purpose="lineage-evidence",
            memory_kind="continuity",
            authority_status="accepted",
            receipt_id="receipt-1",
        ).to_record()

        self.assertEqual(record["schema"], "velvet.continuity.memory-anchor.v1")
        self.assertFalse(record["private_payload_included"])
        self.assertFalse(record["authority_granted"])
        self.assertEqual(record["receipt_id"], "receipt-1")

    def test_rejects_private_payload_and_authority(self):
        base = {
            "memory_event_id": "memory-1",
            "purpose": "identity-evidence",
            "memory_kind": "fact",
            "authority_status": "accepted",
        }
        with self.assertRaises(ValueError):
            validate_memory_anchor(dict(base, payload={"private": True}))
        with self.assertRaises(ValueError):
            validate_memory_anchor(dict(base, authority_granted=True))

    def test_rejects_unknown_purpose(self):
        with self.assertRaises(ValueError):
            MemoryAnchor("memory-1", "decision", "fact", "accepted").to_record()


if __name__ == "__main__":
    unittest.main()
