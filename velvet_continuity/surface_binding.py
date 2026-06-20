# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.surface_binding
===================================
SurfaceBinding: association between a Velvet AI instance and a named surface.

Surface bindings record which instance is active on which surface,
what memory classes are permitted, and what classes are denied.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from velvet_continuity.validation import require_non_empty, require_string_tuple


@dataclass(frozen=True)
class SurfaceBinding:
    """
    Immutable binding between a Velvet AI instance and a named surface.

    Fields
    ------
    surface_id : str
        Unique identifier for the surface (e.g. "nav-primary", "cluster-left").
    surface_type : str
        Classification of the surface (e.g. "nav", "audio", "cluster",
        "mobile", "home", "custom").
    bound_instance_id : str
        The instance_id of the Velvet AI instance bound to this surface.
    trusted_by : str
        The authority scope or instance_id that authorised this binding.
    allowed_memory_classes : tuple[str, ...]
        Memory class identifiers permitted on this surface binding.
    denied_memory_classes : tuple[str, ...]
        Memory class identifiers explicitly excluded from this surface binding.
    receipt_anchor : str | None
        Optional receipt chain anchor for this binding event.
    created_at : str
        ISO 8601 timestamp of record creation.
    binding_id : str
        Unique identifier for this binding record (auto-generated).
    """

    surface_id: str
    surface_type: str
    bound_instance_id: str
    trusted_by: str
    allowed_memory_classes: tuple[str, ...]
    denied_memory_classes: tuple[str, ...]
    receipt_anchor: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    binding_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for field_name in (
            "surface_id", "surface_type", "bound_instance_id",
            "trusted_by", "created_at", "binding_id",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        require_string_tuple(self.allowed_memory_classes, "allowed_memory_classes")
        require_string_tuple(self.denied_memory_classes, "denied_memory_classes")
        if self.receipt_anchor is not None:
            require_non_empty(self.receipt_anchor, "receipt_anchor")

    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "surface_id": self.surface_id,
            "surface_type": self.surface_type,
            "bound_instance_id": self.bound_instance_id,
            "trusted_by": self.trusted_by,
            "allowed_memory_classes": list(self.allowed_memory_classes),
            "denied_memory_classes": list(self.denied_memory_classes),
            "receipt_anchor": self.receipt_anchor,
            "created_at": self.created_at,
        }
