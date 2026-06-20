# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.proof_verify
================================
Factory functions and verification logic for the v0.1.1 mechanical
continuity proof layer.

All factory functions validate inputs fail-closed before constructing
records. All verify functions are pure (no I/O, no side effects).

Authority model
---------------
- ``authority_level == 0``: recovery-only / downgraded state.
- ``authority_level >= 1``: live operational state.
- Negative authority levels are rejected at construction time.
- ``verify_lineage_chain`` returns ``chain[-1].authority_level`` for a
  valid chain, and ``0`` for any chain with errors.

Local key contract
------------------
All functions that compute or verify integrity tags require a non-empty
``local_key: bytes``. The key is node-local and never serialised.
"""

from __future__ import annotations

import time
from dataclasses import replace

from velvet_continuity.proof_hashing import (
    genesis_root_hash,
    make_integrity_tag,
    proof_identity_hash,
)
from velvet_continuity.proof_records import LineageEvent, ProofIdentityRecord
from velvet_continuity.validation import (
    ValidationError,
    require_authority_level,
    require_non_empty,
    require_string_sequence,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _require_local_key(local_key: bytes) -> None:
    """Fail closed if local_key is empty or not bytes."""
    if not isinstance(local_key, bytes) or len(local_key) == 0:
        raise ValidationError("'local_key' must be a non-empty bytes value")


def _validate_context_hashes(hashes: object) -> tuple[str, ...]:
    """
    Validate and normalise active_context_hashes.

    Accepts list or tuple of non-empty strings. Empty sequence allowed.
    Returns a tuple[str, ...] for storage in the frozen record.
    """
    require_string_sequence(hashes, "active_context_hashes")
    return tuple(hashes)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------

def create_genesis_identity(
    genesis_proof: str,
    model_fp: str,
    surface_fp: str,
    local_key: bytes,
    active_context_hashes: list[str] | tuple[str, ...] | None = None,
    authority_level: int = 1,
) -> ProofIdentityRecord:
    """
    Create a genesis ProofIdentityRecord.

    The instance ``id`` and ``lineage_root`` are both derived from the
    genesis root hash and are therefore stable for the lifetime of this
    lineage chain.

    Parameters
    ----------
    genesis_proof : str
        Non-empty proof string establishing the genesis context.
    model_fp : str
        Non-empty model/firmware fingerprint.
    surface_fp : str
        Non-empty surface fingerprint (from ``generate_surface_fingerprint``
        or a caller-supplied stable string).
    local_key : bytes
        Non-empty node-local HMAC key.
    active_context_hashes : list[str] | tuple[str, ...] | None
        Optional initial context hashes. Empty list is valid. Default: empty.
    authority_level : int
        Initial authority level. Must be >= 0. Default: 1.

    Returns
    -------
    ProofIdentityRecord
        Fully constructed and integrity-tagged genesis record.

    Raises
    ------
    ValidationError
        If any required input is empty, invalid, or out of range.
    """
    _require_local_key(local_key)
    require_non_empty(genesis_proof, "genesis_proof")
    require_non_empty(model_fp, "model_fp")
    require_non_empty(surface_fp, "surface_fp")
    require_authority_level(authority_level)

    ctx = _validate_context_hashes(
        active_context_hashes if active_context_hashes is not None else []
    )

    # Build the base record with empty id/lineage_root so genesis_root_hash
    # can compute the root without circular dependency.
    base = ProofIdentityRecord(
        id="",
        genesis_ts=int(time.time() * 1_000_000_000),
        genesis_proof=genesis_proof,
        model_fingerprint=model_fp,
        surface_fingerprint=surface_fp,
        lineage_root="",
        active_context_hashes=ctx,
        authority_level=authority_level,
        previous_hash=None,
        integrity_tag="",
    )

    g_root = genesis_root_hash(base)

    # Fill in derived fields; leave integrity_tag empty until after.
    unsigned = replace(
        base,
        id=f"velvet:instance:{g_root}",
        lineage_root=g_root,
        integrity_tag="",
    )

    tag = make_integrity_tag(unsigned, local_key)
    return replace(unsigned, integrity_tag=tag)


def create_successor_identity(
    previous: ProofIdentityRecord,
    local_key: bytes,
    model_fp: str | None = None,
    surface_fp: str | None = None,
    active_context_hashes: list[str] | tuple[str, ...] | None = None,
    authority_level: int | None = None,
) -> ProofIdentityRecord:
    """
    Create a successor ProofIdentityRecord from an existing record.

    Preserves ``id``, ``genesis_ts``, ``genesis_proof``, and
    ``lineage_root`` from the predecessor. Updates ``previous_hash``
    to the hash of ``previous``.

    Parameters
    ----------
    previous : ProofIdentityRecord
        The record this successor extends.
    local_key : bytes
        Non-empty node-local HMAC key.
    model_fp : str | None
        Updated model fingerprint. If None, inherits from ``previous``.
    surface_fp : str | None
        Updated surface fingerprint. If None, inherits from ``previous``.
    active_context_hashes : list[str] | tuple[str, ...] | None
        Updated context hashes. If None, inherits from ``previous``.
        Intentional empty list ``[]`` clears all active contexts.
    authority_level : int | None
        Updated authority level. If None, inherits from ``previous``.
        Must be >= 0 if supplied.

    Returns
    -------
    ProofIdentityRecord
        Fully constructed and integrity-tagged successor record.

    Raises
    ------
    ValidationError
        If any supplied input is invalid or out of range.
    TypeError
        If ``previous`` is not a ProofIdentityRecord.
    """
    if not isinstance(previous, ProofIdentityRecord):
        raise TypeError(
            f"'previous' must be a ProofIdentityRecord, "
            f"got {type(previous).__name__}"
        )
    _require_local_key(local_key)

    new_model = model_fp if model_fp is not None else previous.model_fingerprint
    new_surface = surface_fp if surface_fp is not None else previous.surface_fingerprint
    new_auth = authority_level if authority_level is not None else previous.authority_level

    if model_fp is not None:
        require_non_empty(model_fp, "model_fp")
    if surface_fp is not None:
        require_non_empty(surface_fp, "surface_fp")
    require_authority_level(new_auth)

    if active_context_hashes is not None:
        new_ctx = _validate_context_hashes(active_context_hashes)
    else:
        new_ctx = previous.active_context_hashes

    unsigned = replace(
        previous,
        model_fingerprint=new_model,
        surface_fingerprint=new_surface,
        active_context_hashes=new_ctx,
        authority_level=new_auth,
        previous_hash=proof_identity_hash(previous),
        integrity_tag="",
    )

    tag = make_integrity_tag(unsigned, local_key)
    return replace(unsigned, integrity_tag=tag)


def create_lineage_event(
    from_record: ProofIdentityRecord,
    to_record: ProofIdentityRecord,
    event_type: str,
    description: str,
    local_key: bytes,
    receipt_anchor: str | None = None,
) -> LineageEvent:
    """
    Create a LineageEvent linking two consecutive ProofIdentityRecords.

    Parameters
    ----------
    from_record : ProofIdentityRecord
        The predecessor record.
    to_record : ProofIdentityRecord
        The successor record.
    event_type : str
        Non-empty short descriptor (e.g. ``"MODEL_UPGRADE"``).
    description : str
        Non-empty human-readable description of the transition.
    local_key : bytes
        Non-empty node-local HMAC key.
    receipt_anchor : str | None
        Optional anchor into the velvet-receipts chain.

    Returns
    -------
    LineageEvent
        Fully constructed and integrity-tagged event record.

    Raises
    ------
    ValidationError
        If any required input is empty or invalid.
    """
    if not isinstance(from_record, ProofIdentityRecord):
        raise TypeError(
            f"'from_record' must be a ProofIdentityRecord, "
            f"got {type(from_record).__name__}"
        )
    if not isinstance(to_record, ProofIdentityRecord):
        raise TypeError(
            f"'to_record' must be a ProofIdentityRecord, "
            f"got {type(to_record).__name__}"
        )
    _require_local_key(local_key)
    require_non_empty(event_type, "event_type")
    require_non_empty(description, "description")

    unsigned = LineageEvent(
        ts=int(time.time() * 1_000_000_000),
        event_type=event_type,
        from_identity_hash=proof_identity_hash(from_record),
        to_identity_hash=proof_identity_hash(to_record),
        description=description,
        receipt_anchor=receipt_anchor,
        integrity_tag="",
    )
    tag = make_integrity_tag(unsigned, local_key)
    return replace(unsigned, integrity_tag=tag)


# ---------------------------------------------------------------------------
# Verification functions
# ---------------------------------------------------------------------------

def verify_lineage_event(
    event: LineageEvent,
    from_record: ProofIdentityRecord,
    to_record: ProofIdentityRecord,
    local_key: bytes,
) -> tuple[bool, list[str]]:
    """
    Verify the integrity of a LineageEvent against its flanking records.

    Checks:
    - ``from_identity_hash`` matches the hash of ``from_record``
    - ``to_identity_hash`` matches the hash of ``to_record``
    - ``integrity_tag`` matches the HMAC recomputed with ``local_key``

    Returns
    -------
    tuple[bool, list[str]]
        ``(True, [])`` if all checks pass.
        ``(False, [error, ...])`` listing all failures.
    """
    _require_local_key(local_key)
    errors: list[str] = []

    if event.from_identity_hash != proof_identity_hash(from_record):
        errors.append("from_identity_hash mismatch")
    if event.to_identity_hash != proof_identity_hash(to_record):
        errors.append("to_identity_hash mismatch")
    if event.integrity_tag != make_integrity_tag(event, local_key):
        errors.append("integrity_tag mismatch")

    return len(errors) == 0, errors


def verify_lineage_chain(
    chain: list[ProofIdentityRecord],
    local_key: bytes | None = None,
) -> tuple[bool, list[str], int]:
    """
    Verify a sequence of ProofIdentityRecords as a coherent lineage chain.

    Checks (in order):
    1. Chain is non-empty.
    2. ``chain[0]`` is a valid genesis record:
       - ``id == "velvet:instance:<genesis_root_hash>"``
       - ``previous_hash is None``
    3. For every record (including genesis, if ``local_key`` is provided):
       - ``integrity_tag`` matches the HMAC recomputed with ``local_key``
    4. For every record after the first:
       - ``previous_hash`` equals the hash of the preceding record
       - ``lineage_root`` equals the genesis ``lineage_root``
       - ``id`` equals the genesis ``id``

    Authority reporting
    -------------------
    - Valid chain  → returns ``chain[-1].authority_level``
    - Invalid chain → returns ``0``

    This means the caller always gets the *current* live authority of the
    tail record on success, and a hard zero on any verification failure.

    Parameters
    ----------
    chain : list[ProofIdentityRecord]
        Ordered list of records from genesis to most recent.
    local_key : bytes | None
        If provided, integrity tags are verified for every record.
        If None, structural checks only (no HMAC verification).

    Returns
    -------
    tuple[bool, list[str], int]
        ``(valid, errors, authority_level)``
    """
    errors: list[str] = []

    if not chain:
        return False, ["chain is empty"], 0

    if local_key is not None:
        _require_local_key(local_key)

    genesis = chain[0]

    # --- Genesis structural check ---
    expected_genesis_id = f"velvet:instance:{genesis_root_hash(genesis)}"
    if genesis.id != expected_genesis_id or genesis.previous_hash is not None:
        errors.append("invalid genesis record")

    prev_hash = proof_identity_hash(genesis)

    for i, record in enumerate(chain):
        # --- HMAC integrity check (all records, including genesis) ---
        if local_key is not None:
            expected_tag = make_integrity_tag(record, local_key)
            if record.integrity_tag != expected_tag:
                errors.append(f"integrity_tag mismatch at position {i}")

        # --- Chain structural checks (successors only) ---
        if i > 0:
            if record.previous_hash != prev_hash:
                errors.append(f"broken chain link at position {i}")
            if record.lineage_root != genesis.lineage_root:
                errors.append(f"lineage_root changed at position {i}")
            if record.id != genesis.id:
                errors.append(f"instance id changed at position {i}")

        prev_hash = proof_identity_hash(record)

    if errors:
        return False, errors, 0

    return True, [], chain[-1].authority_level
