# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.drift_event
==============================
DriftEvent: structured record of a detected continuity drift condition.

DriftEvents are produced by DriftDetector and consumed by recovery hooks
or formatted for receipt logging via ReceiptBridge. They do not trigger
actions themselves.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from velvet_continuity.validation import require_non_empty


class DriftSeverity(str, Enum):
    """
    Severity classification for a detected drift event.

    INFO     - Informational divergence; no action required.
    LOW      - Minor divergence; log and continue.
    MEDIUM   - Notable divergence; flag for review.
    HIGH     - Significant divergence; recovery may be warranted.
    CRITICAL - Severe divergence; runtime should halt or escalate.
    """
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class DriftEvent:
    """
    Immutable record of a detected drift condition.

    Fields
    ------
    drift_type : str
        Short descriptor of what drifted (e.g. "surface", "memory_scope",
        "authority_scope", "receipt_chain_anchor").
    severity : str
        Severity level. Use DriftSeverity values: "info", "low", "medium",
        "high", "critical".
    expected : str
        The expected value at the time of comparison.
    observed : str
        The observed (actual) value at the time of comparison.
    action : str
        Recommended response (e.g. "review", "quarantine_and_review").
    notes : str
        Optional human-readable elaboration.
    created_at : str
        ISO 8601 timestamp when drift was detected.
    event_id : str
        Unique identifier for this event (auto-generated).
    """

    drift_type: str
    severity: str
    expected: str
    observed: str
    action: str
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for field_name in (
            "drift_type", "severity", "expected", "observed",
            "action", "created_at", "event_id",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        if not isinstance(self.notes, str):
            raise TypeError("notes must be a string")
        valid = {s.value for s in DriftSeverity}
        if self.severity not in valid:
            raise ValueError(
                f"severity must be one of {sorted(valid)}, got {self.severity!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "drift_type": self.drift_type,
            "severity": self.severity,
            "expected": self.expected,
            "observed": self.observed,
            "action": self.action,
            "notes": self.notes,
            "created_at": self.created_at,
        }

    def is_critical(self) -> bool:
        """Return True if this event is CRITICAL severity."""
        return self.severity == DriftSeverity.CRITICAL

    def is_actionable(self) -> bool:
        """Return True if severity is MEDIUM or higher."""
        order = [s.value for s in DriftSeverity]
        return order.index(self.severity) >= order.index(DriftSeverity.MEDIUM)
