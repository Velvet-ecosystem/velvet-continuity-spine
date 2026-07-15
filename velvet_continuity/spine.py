# SPDX-License-Identifier: GPL-3.0-only
"""ContinuitySpine facade for identity, drift, receipts, and Ghost Runs."""

from __future__ import annotations

from dataclasses import dataclass, field

from velvet_continuity.drift_detector import DriftDetector
from velvet_continuity.drift_event import DriftEvent
from velvet_continuity.ghost_run import GhostRunRecord
from velvet_continuity.identity import IdentityRecord
from velvet_continuity.memory_index import MemoryIndex
from velvet_continuity.receipt_bridge import ContinuityReceiptBridge


@dataclass
class ContinuitySpine:
    index: MemoryIndex = field(default_factory=MemoryIndex)
    detector: DriftDetector = field(default_factory=DriftDetector)
    receipts: ContinuityReceiptBridge = field(default_factory=ContinuityReceiptBridge)

    def register_identity(self, record: IdentityRecord) -> dict:
        if not isinstance(record, IdentityRecord):
            raise TypeError(f"Expected IdentityRecord, got {type(record).__name__}")
        self.index.add(record.instance_id, record.to_dict())
        return self.receipts.identity_created(record)

    def compare_identity(self, expected: IdentityRecord, observed: IdentityRecord) -> list[DriftEvent]:
        return self.detector.compare_identity(expected, observed)

    def record_ghost_run(self, record: GhostRunRecord) -> dict:
        if not isinstance(record, GhostRunRecord):
            raise TypeError(f"Expected GhostRunRecord, got {type(record).__name__}")
        self.index.add("ghost-run:{}".format(record.run_id), record.to_dict())
        return self.receipts.ghost_run_recorded(record)

    def get_ghost_run(self, run_id: str) -> dict | None:
        return self.index.get("ghost-run:{}".format(run_id))

    def get_identity(self, instance_id: str) -> dict | None:
        return self.index.get(instance_id)
