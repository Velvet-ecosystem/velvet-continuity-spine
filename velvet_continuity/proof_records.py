# SPDX-License-Identifier: GPL-3.0-only
"""Immutable record types for the mechanical continuity proof layer."""

import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, FrozenSet, Optional, Tuple


@dataclass(frozen=True)
class ProofIdentityRecord:
    id: str
    genesis_ts: int
    genesis_proof: str
    model_fingerprint: str
    surface_fingerprint: str
    lineage_root: str
    active_context_hashes: Tuple[str, ...]
    authority_level: int
    previous_hash: Optional[str]
    integrity_tag: str = ""
    version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["active_context_hashes"] = list(self.active_context_hashes)
        return data

    def content_for_hash(self, exclude: FrozenSet[str] = frozenset()) -> bytes:
        data = self.to_dict()
        for field_name in exclude:
            data.pop(field_name, None)
        return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True)
class LineageEvent:
    ts: int
    event_type: str
    from_identity_hash: str
    to_identity_hash: str
    description: str
    receipt_anchor: Optional[str] = None
    integrity_tag: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def content_for_hash(self) -> bytes:
        data = self.to_dict()
        data.pop("integrity_tag", None)
        return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
