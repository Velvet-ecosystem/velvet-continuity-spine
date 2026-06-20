# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.context_record
==================================
ContextRecord: a bounded runtime context descriptor for a Velvet AI instance.

A context record captures the structural state of a runtime context:
its purpose, which memory classes are permitted or denied, and whether
it is currently active. It does not store memory content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from velvet_continuity.validation import require_non_empty, require_string_tuple


@dataclass(frozen=True)
class ContextRecord:
    """
    Public-safe bounded runtime context descriptor.

    A context record defines the structural boundaries of a runtime context:
    its identifier, purpose, permitted memory classes, denied memory classes,
    and active state. It does not hold private memory content.

    Fields
    ------
    context_id : str
        Unique identifier for this context.
    name : str
        Human-readable label for this context.
    purpose : str
        Technical description of the context's role.
    allowed_memory_classes : tuple[str, ...]
        Memory class identifiers permitted within this context.
    denied_memory_classes : tuple[str, ...]
        Memory class identifiers explicitly excluded from this context.
    active : bool
        Whether this context is currently active.
    created_at : str
        ISO 8601 timestamp of record creation.
    record_id : str
        Unique record identifier (auto-generated).
    """

    context_id: str
    name: str
    purpose: str
    allowed_memory_classes: tuple[str, ...]
    denied_memory_classes: tuple[str, ...]
    active: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    record_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for field_name in ("context_id", "name", "purpose", "created_at", "record_id"):
            require_non_empty(getattr(self, field_name), field_name)
        require_string_tuple(self.allowed_memory_classes, "allowed_memory_classes")
        require_string_tuple(self.denied_memory_classes, "denied_memory_classes")
        if not isinstance(self.active, bool):
            raise TypeError("active must be a bool")

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "context_id": self.context_id,
            "name": self.name,
            "purpose": self.purpose,
            "allowed_memory_classes": list(self.allowed_memory_classes),
            "denied_memory_classes": list(self.denied_memory_classes),
            "active": self.active,
            "created_at": self.created_at,
        }

    def allows(self, memory_class: str) -> bool:
        """Return True if memory_class is in allowed_memory_classes."""
        return memory_class in self.allowed_memory_classes

    def denies(self, memory_class: str) -> bool:
        """Return True if memory_class is in denied_memory_classes."""
        return memory_class in self.denied_memory_classes
