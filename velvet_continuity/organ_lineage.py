# SPDX-License-Identifier: GPL-3.0-only
"""Durable Unified-Organ body lineage records.

Riven records only lasting body changes here. Temporary overflow, short-lived
workload leases, and temporary duty absorption belong to Runtime receipts and
must not become identity lineage by accident.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, Tuple
from uuid import uuid4

from velvet_continuity.validation import (
    ValidationError,
    require_non_empty,
    require_string_sequence,
)


ORGAN_LINEAGE_RECORD_KIND = "organ_lineage_record"


class OrganTransition(str, Enum):
    JOINED = "organ_joined"
    DEPARTED = "organ_departed"
    PERMANENT_REPLACEMENT = "permanent_replacement"
    SUCCESSOR_ASSUMED = "successor_assumed"
    DURABLE_CAPABILITY_REASSIGNED = "durable_capability_reassigned"


@dataclass(frozen=True)
class OrganLineageRecord:
    """One durable, receipted body-registry transition for a named organ."""

    body_id: str
    organ: str
    transition: OrganTransition
    body_registry_revision: str
    receipt_anchor: str
    reason: str
    from_node_id: Optional[str] = None
    to_node_id: Optional[str] = None
    capabilities: Tuple[str, ...] = ()
    previous_record_id: Optional[str] = None
    permanent: bool = True
    canonical: bool = True
    authority_granted: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    record_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for field_name in (
            "body_id",
            "organ",
            "body_registry_revision",
            "receipt_anchor",
            "reason",
            "created_at",
            "record_id",
        ):
            require_non_empty(getattr(self, field_name), field_name)

        if not isinstance(self.transition, OrganTransition):
            raise ValidationError(
                "'transition' must be an OrganTransition, got {}".format(
                    type(self.transition).__name__
                )
            )

        for field_name in ("from_node_id", "to_node_id", "previous_record_id"):
            value = getattr(self, field_name)
            if value is not None:
                require_non_empty(value, field_name)

        require_string_sequence(self.capabilities, "capabilities")
        object.__setattr__(self, "capabilities", tuple(self.capabilities))

        if self.permanent is not True:
            raise ValidationError(
                "'permanent' must be True; temporary workload movement is not lineage"
            )
        if self.canonical is not True:
            raise ValidationError("'canonical' must be True for organ lineage")
        if self.authority_granted is not False:
            raise ValidationError(
                "'authority_granted' must be False; continuity evidence is not authority"
            )

        if self.transition is OrganTransition.JOINED:
            self._require_to_only()
        elif self.transition is OrganTransition.DEPARTED:
            self._require_from_only()
        elif self.transition in {
            OrganTransition.PERMANENT_REPLACEMENT,
            OrganTransition.SUCCESSOR_ASSUMED,
            OrganTransition.DURABLE_CAPABILITY_REASSIGNED,
        }:
            self._require_distinct_nodes()

        if (
            self.transition is OrganTransition.DURABLE_CAPABILITY_REASSIGNED
            and not self.capabilities
        ):
            raise ValidationError(
                "durable capability reassignment requires at least one capability"
            )

    def _require_to_only(self) -> None:
        if self.to_node_id is None:
            raise ValidationError("organ_joined requires 'to_node_id'")
        if self.from_node_id is not None:
            raise ValidationError("organ_joined cannot declare 'from_node_id'")

    def _require_from_only(self) -> None:
        if self.from_node_id is None:
            raise ValidationError("organ_departed requires 'from_node_id'")
        if self.to_node_id is not None:
            raise ValidationError("organ_departed cannot declare 'to_node_id'")

    def _require_distinct_nodes(self) -> None:
        if self.from_node_id is None or self.to_node_id is None:
            raise ValidationError(
                "{} requires both from_node_id and to_node_id".format(
                    self.transition.value
                )
            )
        if self.from_node_id == self.to_node_id:
            raise ValidationError(
                "durable organ transition requires distinct source and destination nodes"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": ORGAN_LINEAGE_RECORD_KIND,
            "record_id": self.record_id,
            "body_id": self.body_id,
            "organ": self.organ,
            "transition": self.transition.value,
            "body_registry_revision": self.body_registry_revision,
            "receipt_anchor": self.receipt_anchor,
            "reason": self.reason,
            "from_node_id": self.from_node_id,
            "to_node_id": self.to_node_id,
            "capabilities": list(self.capabilities),
            "previous_record_id": self.previous_record_id,
            "permanent": self.permanent,
            "canonical": self.canonical,
            "authority_granted": self.authority_granted,
            "created_at": self.created_at,
        }
