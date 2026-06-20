# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.proof_records
=================================
Immutable record types for the v0.1.1 mechanical continuity proof layer.

ProofIdentityRecord  — a versioned, hash-chained identity snapshot with a
                       local HMAC integrity tag and an explicit authority level.
LineageEvent         — a receipted link between two consecutive identity hashes.

These records are the substrate for deterministic, offline-verifiable continuity
proofs. They do not grant authority by themselves — verification is performed
by velvet_continuity.proof_verify.

Design constraints
------------------
- stdlib only, no external dependencies
- frozen=True: all records are immutable after construction
- No __post_init__ validation here; construction happens via factory functions
  in proof_verify.py which apply full validation before calling these constructors.
  Direct construction is possible but callers are responsible for field correctness.
- active_context_hashes is stored as tuple[str, ...] for hashability
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass(frozen=True)
class ProofIdentityRecord:
    """
    Versioned, hash-chained identity snapshot for a Velvet AI instance.

    Fields
    ------
    id : str
        Stable instance identifier. Derived at genesis as
        ``"velvet:instance:<genesis_root_hash>"`` and never changes across
        the lifetime of the lineage chain.
    genesis_ts : int
        Nanosecond-precision Unix timestamp recorded at genesis creation.
        Copied unchanged into every successor record.
    genesis_proof : str
        Caller-supplied proof string establishing the genesis context
        (e.g. a hardware attestation hash or deployment token hash).
    model_fingerprint : str
        Hash or label identifying the model/firmware version active at
        the time this record was created.
    surface_fingerprint : str
        Stable surface fingerprint produced by ``generate_surface_fingerprint()``.
    lineage_root : str
        The genesis root hash for this lineage chain. Never changes.
    active_context_hashes : tuple[str, ...]
        Hashes of the bounded runtime contexts active at record creation time.
        Empty tuple is valid (no active contexts).
    authority_level : int
        Current operational authority. 0 = recovery/downgraded. >= 1 = live.
    previous_hash : str | None
        SHA-256 hash of the immediately preceding record in the chain.
        None only for the genesis record.
    integrity_tag : str
        Local HMAC-SHA256 tag over the record content (excluding this field).
        Computed and verified using a node-local key; not transmitted.
    version : int
        Schema version. Default 1.
    """

    id: str
    genesis_ts: int
    genesis_proof: str
    model_fingerprint: str
    surface_fingerprint: str
    lineage_root: str
    active_context_hashes: tuple[str, ...]
    authority_level: int
    previous_hash: str | None
    integrity_tag: str = ""
    version: int = 1

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dict with active_context_hashes as a list."""
        d = asdict(self)
        d["active_context_hashes"] = list(self.active_context_hashes)
        return d

    def content_for_hash(self, exclude: frozenset[str] = frozenset()) -> bytes:
        """
        Return canonical UTF-8 JSON bytes for hashing, excluding named fields.

        Uses ``active_context_hashes`` as a list in the serialised form so that
        the hash is stable regardless of whether the caller stores a list or tuple.
        """
        d = self.to_dict()
        for f in exclude:
            d.pop(f, None)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True)
class LineageEvent:
    """
    Receipted link between two consecutive ProofIdentityRecord hashes.

    Fields
    ------
    ts : int
        Nanosecond-precision Unix timestamp of event creation.
    event_type : str
        Short descriptor (e.g. ``"MODEL_UPGRADE"``, ``"SURFACE_CHANGE"``).
    from_identity_hash : str
        Hash of the predecessor ProofIdentityRecord.
    to_identity_hash : str
        Hash of the successor ProofIdentityRecord.
    description : str
        Human-readable description of the transition.
    receipt_anchor : str | None
        Optional anchor into the velvet-receipts chain for this event.
    integrity_tag : str
        Local HMAC-SHA256 tag over the event content (excluding this field).
    """

    ts: int
    event_type: str
    from_identity_hash: str
    to_identity_hash: str
    description: str
    receipt_anchor: str | None = None
    integrity_tag: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def content_for_hash(self) -> bytes:
        """Return canonical UTF-8 JSON bytes for hashing, excluding integrity_tag."""
        d = self.to_dict()
        d.pop("integrity_tag", None)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")
