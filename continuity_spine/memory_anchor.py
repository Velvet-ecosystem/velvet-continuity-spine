# SPDX-License-Identifier: GPL-3.0-only
"""Public-safe memory anchors for continuity and lineage evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

_FORBIDDEN_KEYS = {
    "payload",
    "raw_memory",
    "conversation",
    "biometric_data",
    "embedding",
    "capability_token",
    "command",
    "executor",
}

_ALLOWED_PURPOSES = {
    "identity-evidence",
    "lineage-evidence",
    "recovery-evidence",
    "drift-evidence",
}


@dataclass(frozen=True)
class MemoryAnchor:
    memory_event_id: str
    purpose: str
    memory_kind: str
    authority_status: str
    receipt_id: Optional[str] = None

    def to_record(self) -> Dict[str, Any]:
        _text(self.memory_event_id, "memory_event_id")
        _text(self.memory_kind, "memory_kind")
        _text(self.authority_status, "authority_status")
        if self.purpose not in _ALLOWED_PURPOSES:
            raise ValueError("unsupported memory anchor purpose")
        if self.receipt_id is not None:
            _text(self.receipt_id, "receipt_id")

        record: Dict[str, Any] = {
            "schema": "velvet.continuity.memory-anchor.v1",
            "memory_event_id": self.memory_event_id,
            "purpose": self.purpose,
            "memory_kind": self.memory_kind,
            "authority_status": self.authority_status,
            "private_payload_included": False,
            "authority_granted": False,
        }
        if self.receipt_id is not None:
            record["receipt_id"] = self.receipt_id
        return record


def validate_memory_anchor(document: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(document, Mapping):
        raise ValueError("memory anchor must be a mapping")
    if _FORBIDDEN_KEYS.intersection(document):
        raise ValueError("memory anchor contains forbidden private fields")

    allowed = {
        "schema",
        "memory_event_id",
        "purpose",
        "memory_kind",
        "authority_status",
        "receipt_id",
        "private_payload_included",
        "authority_granted",
    }
    if set(document) - allowed:
        raise ValueError("memory anchor contains unsupported fields")
    if document.get("schema") not in (None, "velvet.continuity.memory-anchor.v1"):
        raise ValueError("unsupported memory anchor schema")
    if document.get("private_payload_included") not in (None, False):
        raise ValueError("memory anchor cannot include private payload")
    if document.get("authority_granted") not in (None, False):
        raise ValueError("memory anchor cannot grant authority")

    return MemoryAnchor(
        memory_event_id=document.get("memory_event_id"),
        purpose=document.get("purpose"),
        memory_kind=document.get("memory_kind"),
        authority_status=document.get("authority_status"),
        receipt_id=document.get("receipt_id"),
    ).to_record()


def _text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("{} must be a non-empty string".format(name))
