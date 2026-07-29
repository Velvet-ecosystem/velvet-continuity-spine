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
from velvet_continuity.ghost_run import GhostRunRecord
from velvet_continuity.identity import IdentityRecord
from velvet_continuity.memory_index import MemoryIndex
from velvet_continuity.organ_lineage import OrganLineageRecord
from velvet_continuity.receipt_bridge import ContinuityReceiptBridge


@dataclass
class ContinuitySpine:
    """Thin facade joining continuity indexing, drift, and receipt formatting."""

    index: MemoryIndex = field(default_factory=MemoryIndex)
    detector: DriftDetector = field(default_factory=DriftDetector)
    receipts: ContinuityReceiptBridge = field(default_factory=ContinuityReceiptBridge)

    def register_identity(self, record: IdentityRecord) -> dict:
        """Register identity and return an IDENTITY_CREATED receipt envelope."""
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

    def record_ghost_run(self, record: GhostRunRecord) -> dict:
        """Register a public-safe Ghost run and return its receipt envelope."""
        if not isinstance(record, GhostRunRecord):
            raise TypeError(f"Expected GhostRunRecord, got {type(record).__name__}")
        self.index.add("ghost-run:{}".format(record.run_id), record.to_dict())
        return self.receipts.ghost_run_recorded(record)

    def record_organ_lineage(self, record: OrganLineageRecord) -> dict:
        """Register one durable named-organ transition and return evidence."""
        if not isinstance(record, OrganLineageRecord):
            raise TypeError(
                f"Expected OrganLineageRecord, got {type(record).__name__}"
            )
        self.index.add(
            "organ-lineage:{}".format(record.record_id),
            record.to_dict(),
        )
        return self.receipts.organ_lineage_recorded(record)

    def get_organ_lineage(self, record_id: str) -> dict | None:
        """Retrieve a durable named-organ lineage record by record ID."""
        return self.index.get("organ-lineage:{}".format(record_id))

    def get_ghost_run(self, run_id: str) -> dict | None:
        """Retrieve a registered Ghost System run record by run_id."""
        return self.index.get("ghost-run:{}".format(run_id))

    def get_identity(self, instance_id: str) -> dict | None:
        """Retrieve a registered identity record dict by instance_id."""
        return self.index.get(instance_id)
