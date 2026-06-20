# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.lineage
==========================
LineageRecord: parent/child continuity link between identity records.

Lineage records allow a runtime to verify that it descends from a known
prior instance. They do not grant authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from velvet_continuity.identity import IdentityRecord
from velvet_continuity.validation import require_non_empty


@dataclass(frozen=True)
class LineageRecord:
    """
    Immutable parent/child continuity link between identity records.

    Fields
    ------
    child_instance_id : str
        The instance_id of the child (newer) identity record.
    parent_instance_id : str
        The instance_id of the parent (prior) identity record.
    relationship : str
        Description of the relationship type
        (e.g. "successor", "replacement", "fork").
    receipt_anchor : str | None
        Optional receipt chain anchor for this lineage event.
    created_at : str
        ISO 8601 timestamp of record creation.
    lineage_id : str
        Unique identifier for this lineage record (auto-generated).
    """

    child_instance_id: str
    parent_instance_id: str
    relationship: str
    receipt_anchor: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    lineage_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for field_name in (
            "child_instance_id", "parent_instance_id", "relationship",
            "created_at", "lineage_id",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        if self.receipt_anchor is not None:
            require_non_empty(self.receipt_anchor, "receipt_anchor")

    def to_dict(self) -> dict[str, Any]:
        return {
            "lineage_id": self.lineage_id,
            "child_instance_id": self.child_instance_id,
            "parent_instance_id": self.parent_instance_id,
            "relationship": self.relationship,
            "receipt_anchor": self.receipt_anchor,
            "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# Standalone helpers
# ---------------------------------------------------------------------------

def verify_parent_link(child: IdentityRecord, parent: IdentityRecord) -> bool:
    """Return True when child's lineage_parent points to parent's instance_id."""
    return child.lineage_parent == parent.instance_id


def verify_receipt_anchor(record: IdentityRecord) -> bool:
    """Return True when the identity record has a receipt chain anchor set."""
    return record.has_receipt_anchor()
