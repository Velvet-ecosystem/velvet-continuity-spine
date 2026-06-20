# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.identity
===========================
IdentityRecord: public-safe identity descriptor for a Velvet AI runtime instance.

An identity record answers: who is this runtime instance, what is its role,
what memory scope does it operate within, and what authority scope governs it?

It does not grant authority. It describes identity for continuity tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from velvet_continuity.validation import require_non_empty


@dataclass(frozen=True)
class IdentityRecord:
    """
    Public-safe identity record for a Velvet AI runtime instance.

    IdentityRecord does not grant authority.
    It describes identity, lineage links, memory scope, and receipt anchoring.

    Fields
    ------
    instance_id : str
        Stable unique identifier for this runtime instance.
    name : str
        Human-readable display name.
    role : str
        Functional role of this instance (e.g. "navigator", "coordinator").
    runtime_class : str
        Runtime classification describing the instance's operational category
        (e.g. "embedded-node", "gateway", "analysis-only").
    surface : str
        Primary surface this instance is bound to (e.g. "nav", "audio", "cluster").
    memory_scope : str
        Memory scope identifier governing what this instance may access.
    authority_scope : str
        Authority scope identifier describing what governance applies.
    lineage_parent : str | None
        instance_id of the direct ancestor instance. None for genesis instances.
    receipt_chain_anchor : str | None
        Hash or identifier anchoring this record to a receipt chain entry.
    created_at : str
        ISO 8601 timestamp of record creation.
    record_id : str
        Unique record identifier (auto-generated).
    """

    instance_id: str
    name: str
    role: str
    runtime_class: str
    surface: str
    memory_scope: str
    authority_scope: str
    lineage_parent: str | None = None
    receipt_chain_anchor: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    record_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for field_name in (
            "instance_id", "name", "role", "runtime_class", "surface",
            "memory_scope", "authority_scope", "created_at", "record_id",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        if self.lineage_parent is not None:
            require_non_empty(self.lineage_parent, "lineage_parent")
        if self.receipt_chain_anchor is not None:
            require_non_empty(self.receipt_chain_anchor, "receipt_chain_anchor")

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "instance_id": self.instance_id,
            "name": self.name,
            "role": self.role,
            "runtime_class": self.runtime_class,
            "surface": self.surface,
            "memory_scope": self.memory_scope,
            "authority_scope": self.authority_scope,
            "lineage_parent": self.lineage_parent,
            "receipt_chain_anchor": self.receipt_chain_anchor,
            "created_at": self.created_at,
        }

    def has_receipt_anchor(self) -> bool:
        """Return True if this record has a receipt chain anchor set."""
        return bool(self.receipt_chain_anchor)

    def has_lineage_parent(self) -> bool:
        """Return True if this record declares a parent instance."""
        return bool(self.lineage_parent)

    def is_genesis(self) -> bool:
        """Return True if this record has no declared parent (genesis instance)."""
        return self.lineage_parent is None
