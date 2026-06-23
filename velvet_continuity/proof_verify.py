# SPDX-License-Identifier: GPL-3.0-only
"""Factory and verification functions for mechanical continuity proofs."""

import time
from dataclasses import replace
from typing import List, Optional, Sequence, Tuple, Union

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


ContextHashes = Optional[Union[List[str], Tuple[str, ...]]]


def _require_local_key(local_key: bytes) -> None:
    if not isinstance(local_key, bytes) or len(local_key) == 0:
        raise ValidationError("'local_key' must be a non-empty bytes value")


def _validate_context_hashes(hashes: object) -> Tuple[str, ...]:
    require_string_sequence(hashes, "active_context_hashes")
    return tuple(hashes)  # type: ignore[arg-type]


def create_genesis_identity(
    genesis_proof: str,
    model_fp: str,
    surface_fp: str,
    local_key: bytes,
    active_context_hashes: ContextHashes = None,
    authority_level: int = 1,
) -> ProofIdentityRecord:
    _require_local_key(local_key)
    require_non_empty(genesis_proof, "genesis_proof")
    require_non_empty(model_fp, "model_fp")
    require_non_empty(surface_fp, "surface_fp")
    require_authority_level(authority_level)

    context_hashes = _validate_context_hashes(
        active_context_hashes if active_context_hashes is not None else []
    )

    base = ProofIdentityRecord(
        id="",
        genesis_ts=int(time.time() * 1_000_000_000),
        genesis_proof=genesis_proof,
        model_fingerprint=model_fp,
        surface_fingerprint=surface_fp,
        lineage_root="",
        active_context_hashes=context_hashes,
        authority_level=authority_level,
        previous_hash=None,
        integrity_tag="",
    )

    root_hash = genesis_root_hash(base)
    unsigned = replace(
        base,
        id="velvet:instance:{}".format(root_hash),
        lineage_root=root_hash,
        integrity_tag="",
    )
    return replace(unsigned, integrity_tag=make_integrity_tag(unsigned, local_key))


def create_successor_identity(
    previous: ProofIdentityRecord,
    local_key: bytes,
    model_fp: Optional[str] = None,
    surface_fp: Optional[str] = None,
    active_context_hashes: ContextHashes = None,
    authority_level: Optional[int] = None,
) -> ProofIdentityRecord:
    if not isinstance(previous, ProofIdentityRecord):
        raise TypeError(
            "'previous' must be a ProofIdentityRecord, got {}".format(
                type(previous).__name__
            )
        )

    _require_local_key(local_key)

    new_model = model_fp if model_fp is not None else previous.model_fingerprint
    new_surface = surface_fp if surface_fp is not None else previous.surface_fingerprint
    new_authority = (
        authority_level if authority_level is not None else previous.authority_level
    )

    if model_fp is not None:
        require_non_empty(model_fp, "model_fp")
    if surface_fp is not None:
        require_non_empty(surface_fp, "surface_fp")
    require_authority_level(new_authority)

    if active_context_hashes is not None:
        new_context = _validate_context_hashes(active_context_hashes)
    else:
        new_context = previous.active_context_hashes

    unsigned = replace(
        previous,
        model_fingerprint=new_model,
        surface_fingerprint=new_surface,
        active_context_hashes=new_context,
        authority_level=new_authority,
        previous_hash=proof_identity_hash(previous),
        integrity_tag="",
    )
    return replace(unsigned, integrity_tag=make_integrity_tag(unsigned, local_key))


def create_lineage_event(
    from_record: ProofIdentityRecord,
    to_record: ProofIdentityRecord,
    event_type: str,
    description: str,
    local_key: bytes,
    receipt_anchor: Optional[str] = None,
) -> LineageEvent:
    if not isinstance(from_record, ProofIdentityRecord):
        raise TypeError(
            "'from_record' must be a ProofIdentityRecord, got {}".format(
                type(from_record).__name__
            )
        )
    if not isinstance(to_record, ProofIdentityRecord):
        raise TypeError(
            "'to_record' must be a ProofIdentityRecord, got {}".format(
                type(to_record).__name__
            )
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
    return replace(unsigned, integrity_tag=make_integrity_tag(unsigned, local_key))


def verify_lineage_event(
    event: LineageEvent,
    from_record: ProofIdentityRecord,
    to_record: ProofIdentityRecord,
    local_key: bytes,
) -> Tuple[bool, List[str]]:
    _require_local_key(local_key)
    errors: List[str] = []

    if event.from_identity_hash != proof_identity_hash(from_record):
        errors.append("from_identity_hash mismatch")
    if event.to_identity_hash != proof_identity_hash(to_record):
        errors.append("to_identity_hash mismatch")
    if event.integrity_tag != make_integrity_tag(event, local_key):
        errors.append("integrity_tag mismatch")

    return len(errors) == 0, errors


def verify_lineage_chain(
    chain: Sequence[ProofIdentityRecord],
    local_key: Optional[bytes] = None,
) -> Tuple[bool, List[str], int]:
    errors: List[str] = []

    if not chain:
        return False, ["chain is empty"], 0

    if local_key is not None:
        _require_local_key(local_key)

    genesis = chain[0]
    expected_genesis_id = "velvet:instance:{}".format(genesis_root_hash(genesis))
    if genesis.id != expected_genesis_id or genesis.previous_hash is not None:
        errors.append("invalid genesis record")

    previous_hash = proof_identity_hash(genesis)

    for position, record in enumerate(chain):
        if local_key is not None:
            expected_tag = make_integrity_tag(record, local_key)
            if record.integrity_tag != expected_tag:
                errors.append(
                    "integrity_tag mismatch at position {}".format(position)
                )

        if position > 0:
            if record.previous_hash != previous_hash:
                errors.append("broken chain link at position {}".format(position))
            if record.lineage_root != genesis.lineage_root:
                errors.append("lineage_root changed at position {}".format(position))
            if record.id != genesis.id:
                errors.append("instance id changed at position {}".format(position))

        previous_hash = proof_identity_hash(record)

    if errors:
        return False, errors, 0

    return True, [], chain[-1].authority_level
