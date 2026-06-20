# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.spine
========================
ContinuitySpine: convenience facade joining identity indexing,
drift detection, and receipt payload formatting.

This is a thin coordinator. It does not execute actions or grant authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from velvet_continuity.drift_detector import DriftDetector
from velvet_continuity.drift_event import DriftEvent
from velvet_continuity.identity import IdentityRecord
from velvet_continuity.memory_index import MemoryIndex
from velvet_continuity.receipt_bridge import ContinuityReceiptBridge


@dataclass
class ContinuitySpine:
    """
    Thin facade joining identity index, drift detection, and receipt formatting.

    Attributes
    ----------
    index : MemoryIndex
        In-process index of registered identity records.
    detector : DriftDetector
        Drift comparison logic.
    receipts : ContinuityReceiptBridge
        Receipt payload formatter.
    """

    index: MemoryIndex = field(default_factory=MemoryIndex)
    detector: DriftDetector = field(default_factory=DriftDetector)
    receipts: ContinuityReceiptBridge = field(default_factory=ContinuityReceiptBridge)

    def register_identity(self, record: IdentityRecord) -> dict:
        """
        Register an identity record in the local index and return a
        receipt-compatible payload for the IDENTITY_CREATED event.
        """
        if not isinstance(record, IdentityRecord):
            raise TypeError(f"Expected IdentityRecord, got {type(record).__name__}")
        self.index.add(record.instance_id, record.to_dict())
        return self.receipts.identity_created(record)

    def compare_identity(
        self,
        expected: IdentityRecord,
        observed: IdentityRecord,
    ) -> list[DriftEvent]:
        """Compare two identity records and return any drift events."""
        return self.detector.compare_identity(expected, observed)

    def get_identity(self, instance_id: str) -> dict | None:
        """Retrieve a registered identity record dict by instance_id."""
        return self.index.get(instance_id)
