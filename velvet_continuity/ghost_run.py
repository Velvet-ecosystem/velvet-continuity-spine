# SPDX-License-Identifier: GPL-3.0-only
"""Public-safe continuity records for synthetic Ghost System runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Tuple
from uuid import uuid4

from velvet_continuity.validation import ValidationError, require_non_empty, require_string_sequence

GHOST_CAN_EVENT_TYPE = "vehicle.can.ghost_observation"
GHOST_RUN_RECORD_KIND = "ghost_run_record"


def _require_bool(value: bool, field_name: str) -> None:
    if not isinstance(value, bool):
        raise ValidationError("'{}' must be a bool, got {}".format(field_name, type(value).__name__))


def _require_true(value: bool, field_name: str) -> None:
    _require_bool(value, field_name)
    if value is not True:
        raise ValidationError("'{}' must be True for a public ghost run".format(field_name))


def _require_false(value: bool, field_name: str) -> None:
    _require_bool(value, field_name)
    if value is not False:
        raise ValidationError("'{}' must be False for a public ghost run".format(field_name))


def _require_non_negative_int(value: int, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError("'{}' must be a non-negative integer, got {}".format(field_name, type(value).__name__))
    if value < 0:
        raise ValidationError("'{}' must be >= 0, got {}".format(field_name, value))


@dataclass(frozen=True)
class GhostRunRecord:
    """Immutable marker proving a sealed synthetic observation run occurred."""

    run_id: str
    observation_event_id: str
    event_type: str = GHOST_CAN_EVENT_TYPE
    runtime_route: str = "can-ghost"
    surface: str = "up-squared-ghost"
    receipt_anchor: Optional[str] = None
    repo_fingerprints: Tuple[str, ...] = ()
    observed_frame_count: int = 0
    read_only: bool = True
    synthetic_fixture: bool = True
    physical_bus_opened: bool = False
    can_transmission_attempted: bool = False
    actuation_performed: bool = False
    authority_granted: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    record_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for field_name in ("run_id", "observation_event_id", "event_type", "runtime_route", "surface", "created_at", "record_id"):
            require_non_empty(getattr(self, field_name), field_name)
        if self.event_type != GHOST_CAN_EVENT_TYPE:
            raise ValidationError("'event_type' must be '{}', got '{}'".format(GHOST_CAN_EVENT_TYPE, self.event_type))
        if self.receipt_anchor is not None:
            require_non_empty(self.receipt_anchor, "receipt_anchor")
        require_string_sequence(self.repo_fingerprints, "repo_fingerprints")
        object.__setattr__(self, "repo_fingerprints", tuple(self.repo_fingerprints))
        _require_non_negative_int(self.observed_frame_count, "observed_frame_count")
        _require_true(self.read_only, "read_only")
        _require_true(self.synthetic_fixture, "synthetic_fixture")
        _require_false(self.physical_bus_opened, "physical_bus_opened")
        _require_false(self.can_transmission_attempted, "can_transmission_attempted")
        _require_false(self.actuation_performed, "actuation_performed")
        _require_false(self.authority_granted, "authority_granted")

    def safety_flags(self) -> dict[str, bool]:
        return {"read_only": self.read_only, "synthetic_fixture": self.synthetic_fixture, "physical_bus_opened": self.physical_bus_opened, "can_transmission_attempted": self.can_transmission_attempted, "actuation_performed": self.actuation_performed, "authority_granted": self.authority_granted}

    def is_public_safe(self) -> bool:
        return self.read_only is True and self.synthetic_fixture is True and self.physical_bus_opened is False and self.can_transmission_attempted is False and self.actuation_performed is False and self.authority_granted is False

    def to_dict(self) -> dict[str, Any]:
        return {"record_kind": GHOST_RUN_RECORD_KIND, "record_id": self.record_id, "run_id": self.run_id, "observation_event_id": self.observation_event_id, "event_type": self.event_type, "runtime_route": self.runtime_route, "surface": self.surface, "receipt_anchor": self.receipt_anchor, "repo_fingerprints": list(self.repo_fingerprints), "observed_frame_count": self.observed_frame_count, "read_only": self.read_only, "synthetic_fixture": self.synthetic_fixture, "physical_bus_opened": self.physical_bus_opened, "can_transmission_attempted": self.can_transmission_attempted, "actuation_performed": self.actuation_performed, "authority_granted": self.authority_granted, "created_at": self.created_at}
