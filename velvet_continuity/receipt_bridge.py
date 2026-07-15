# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.receipt_bridge
==================================
ContinuityReceiptBridge: formats continuity records as receipt-compatible
payload dicts.

This bridge deliberately does not import or depend on velvet-receipts.
It returns plain dicts that another layer passes to a receipt logger.

Pattern: format here, pass the dict to the receipts layer separately.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from velvet_continuity.context_record import ContextRecord
from velvet_continuity.drift_event import DriftEvent
from velvet_continuity.ghost_run import GhostRunRecord
from velvet_continuity.identity import IdentityRecord
from velvet_continuity.lineage import LineageRecord
from velvet_continuity.surface_binding import SurfaceBinding
from velvet_continuity.validation import require_non_empty, require_mapping


@dataclass(frozen=True)
class ContinuityReceiptBridge:
    """Format continuity events as receipt-compatible payload dicts."""

    source: str = "velvet-continuity-spine"

    def __post_init__(self) -> None:
        require_non_empty(self.source, "source")

    def format_event(self, event_type: str, payload: dict[str, Any], subject_id: str) -> dict[str, Any]:
        require_non_empty(event_type, "event_type")
        require_non_empty(subject_id, "subject_id")
        require_mapping(payload, "payload")
        return {"event_type": event_type, "source": self.source, "subject_id": subject_id, "payload": dict(payload)}

    def identity_created(self, record: IdentityRecord) -> dict[str, Any]:
        if not isinstance(record, IdentityRecord):
            raise TypeError(f"Expected IdentityRecord, got {type(record).__name__}")
        return self.format_event("IDENTITY_CREATED", record.to_dict(), record.instance_id)

    def lineage_linked(self, record: LineageRecord) -> dict[str, Any]:
        if not isinstance(record, LineageRecord):
            raise TypeError(f"Expected LineageRecord, got {type(record).__name__}")
        return self.format_event("LINEAGE_LINKED", record.to_dict(), record.child_instance_id)

    def context_recorded(self, record: ContextRecord) -> dict[str, Any]:
        if not isinstance(record, ContextRecord):
            raise TypeError(f"Expected ContextRecord, got {type(record).__name__}")
        return self.format_event("CONTEXT_RECORDED", record.to_dict(), record.context_id)

    def drift_detected(self, event: DriftEvent, subject_id: str) -> dict[str, Any]:
        if not isinstance(event, DriftEvent):
            raise TypeError(f"Expected DriftEvent, got {type(event).__name__}")
        require_non_empty(subject_id, "subject_id")
        return self.format_event("DRIFT_DETECTED", event.to_dict(), subject_id)

    def ghost_run_recorded(self, record: GhostRunRecord) -> dict[str, Any]:
        if not isinstance(record, GhostRunRecord):
            raise TypeError(f"Expected GhostRunRecord, got {type(record).__name__}")
        return self.format_event("GHOST_RUN_RECORDED", record.to_dict(), record.run_id)

    def surface_bound(self, record: SurfaceBinding) -> dict[str, Any]:
        if not isinstance(record, SurfaceBinding):
            raise TypeError(f"Expected SurfaceBinding, got {type(record).__name__}")
        return self.format_event("SURFACE_BOUND", record.to_dict(), record.surface_id)
