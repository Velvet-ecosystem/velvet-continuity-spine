# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.drift_detector
==================================
DriftDetector: compares identity records and produces DriftEvent records
describing detected divergence.

The detector does not take action. It produces structured records for
consumption by recovery hooks or the receipt bridge.
"""

from __future__ import annotations

from velvet_continuity.drift_event import DriftEvent, DriftSeverity
from velvet_continuity.identity import IdentityRecord


class DriftDetector:
    """
    Fail-closed checks for identity continuity drift.

    All methods are pure: no side effects, no I/O, no state between calls.
    """

    # Fields to compare and their severity if they diverge
    _IDENTITY_CHECKS: tuple[tuple[str, str], ...] = (
        ("instance_id",      DriftSeverity.CRITICAL),
        ("role",             DriftSeverity.HIGH),
        ("runtime_class",    DriftSeverity.HIGH),
        ("surface",          DriftSeverity.MEDIUM),
        ("memory_scope",     DriftSeverity.HIGH),
        ("authority_scope",  DriftSeverity.CRITICAL),
        ("lineage_parent",   DriftSeverity.MEDIUM),
        ("receipt_chain_anchor", DriftSeverity.CRITICAL),
    )

    def compare_identity(
        self,
        expected: IdentityRecord,
        observed: IdentityRecord,
    ) -> list[DriftEvent]:
        """
        Compare two IdentityRecord snapshots and return DriftEvents for any
        diverging fields. Returns an empty list if all checked fields match.
        """
        if not isinstance(expected, IdentityRecord):
            raise TypeError(f"expected must be an IdentityRecord, got {type(expected).__name__}")
        if not isinstance(observed, IdentityRecord):
            raise TypeError(f"observed must be an IdentityRecord, got {type(observed).__name__}")

        events: list[DriftEvent] = []
        for field_name, severity in self._IDENTITY_CHECKS:
            expected_value = getattr(expected, field_name)
            observed_value = getattr(observed, field_name)
            if expected_value != observed_value:
                action = (
                    "quarantine_and_review"
                    if severity == DriftSeverity.CRITICAL
                    else "review"
                )
                events.append(DriftEvent(
                    drift_type=field_name,
                    severity=severity,
                    expected=str(expected_value),
                    observed=str(observed_value),
                    action=action,
                ))
        return events

    def require_receipt_anchor(self, record: IdentityRecord) -> list[DriftEvent]:
        """
        Return a CRITICAL DriftEvent if the record has no receipt chain anchor.
        Returns an empty list if the anchor is present.
        """
        if not isinstance(record, IdentityRecord):
            raise TypeError(f"record must be an IdentityRecord, got {type(record).__name__}")
        if record.has_receipt_anchor():
            return []
        return [DriftEvent(
            drift_type="receipt_chain_anchor",
            severity=DriftSeverity.CRITICAL,
            expected="non-empty receipt_chain_anchor",
            observed="missing",
            action="quarantine_and_review",
            notes=(
                "Identity without a receipt anchor cannot be treated as "
                "verified continuity."
            ),
        )]

    def has_critical_drift(self, events: list[DriftEvent]) -> bool:
        """Return True if any event in the list is CRITICAL severity."""
        return any(e.severity == DriftSeverity.CRITICAL for e in events)

    def highest_severity(self, events: list[DriftEvent]) -> str | None:
        """Return the highest severity value among events, or None if empty."""
        if not events:
            return None
        order = [s.value for s in DriftSeverity]
        return max(events, key=lambda e: order.index(e.severity)).severity
