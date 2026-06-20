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
from velvet_continuity.identity import IdentityRecord
from velvet_continuity.lineage import LineageRecord
from velvet_continuity.surface_binding import SurfaceBinding
from velvet_continuity.validation import require_non_empty, require_mapping


@dataclass(frozen=True)
class ContinuityReceiptBridge:
    """
    Format continuity events as receipt-compatible payload dicts.

    All methods return plain dicts. No I/O is performed. The caller is
    responsible for passing the dict to the appropriate receipt logger.
    """

    source: str = "velvet-continuity-spine"

    def __post_init__(self) -> None:
        require_non_empty(self.source, "source")

    def format_event(
        self,
        event_type: str,
        payload: dict[str, Any],
        subject_id: str,
    ) -> dict[str, Any]:
        """
        Wrap a payload dict in the standard receipt envelope.

        Parameters
        ----------
        event_type : str
            Namespaced event descriptor (e.g. "IDENTITY_CREATED").
        payload : dict
            The record data to include.
        subject_id : str
            The instance_id or record identifier this event concerns.
        """
        require_non_empty(event_type, "event_type")
        require_non_empty(subject_id, "subject_id")
        require_mapping(payload, "payload")
        return {
            "event_type": event_type,
            "source": self.source,
            "subject_id": subject_id,
            "payload": dict(payload),
        }

    def identity_created(self, record: IdentityRecord) -> dict[str, Any]:
        """Format a receipt payload for: an identity record was established."""
        if not isinstance(record, IdentityRecord):
            raise TypeError(f"Expected IdentityRecord, got {type(record).__name__}")
        return self.format_event("IDENTITY_CREATED", record.to_dict(), record.instance_id)

    def lineage_linked(self, record: LineageRecord) -> dict[str, Any]:
        """Format a receipt payload for: a lineage link was recorded."""
        if not isinstance(record, LineageRecord):
            raise TypeError(f"Expected LineageRecord, got {type(record).__name__}")
        return self.format_event(
            "LINEAGE_LINKED", record.to_dict(), record.child_instance_id
        )

    def context_recorded(self, record: ContextRecord) -> dict[str, Any]:
        """Format a receipt payload for: a context record was captured."""
        if not isinstance(record, ContextRecord):
            raise TypeError(f"Expected ContextRecord, got {type(record).__name__}")
        return self.format_event(
            "CONTEXT_RECORDED", record.to_dict(), record.context_id
        )

    def drift_detected(self, event: DriftEvent, subject_id: str) -> dict[str, Any]:
        """Format a receipt payload for: a drift event was detected."""
        if not isinstance(event, DriftEvent):
            raise TypeError(f"Expected DriftEvent, got {type(event).__name__}")
        require_non_empty(subject_id, "subject_id")
        return self.format_event("DRIFT_DETECTED", event.to_dict(), subject_id)

    def surface_bound(self, record: SurfaceBinding) -> dict[str, Any]:
        """Format a receipt payload for: a surface binding was established."""
        if not isinstance(record, SurfaceBinding):
            raise TypeError(f"Expected SurfaceBinding, got {type(record).__name__}")
        return self.format_event("SURFACE_BOUND", record.to_dict(), record.surface_id)
