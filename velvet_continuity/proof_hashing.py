# SPDX-License-Identifier: GPL-3.0-only
"""Deterministic hashing and local HMAC tagging for continuity proofs."""

import hashlib
import hmac
from typing import FrozenSet, Union

from velvet_continuity.proof_records import LineageEvent, ProofIdentityRecord


_IDENTITY_HASH_EXCLUDE: FrozenSet[str] = frozenset({"integrity_tag"})
_GENESIS_ROOT_EXCLUDE: FrozenSet[str] = frozenset({"id", "lineage_root", "integrity_tag"})
_HASH_PREFIX: bytes = b"VELVET_SPINE_V1:"


def stable_hash(data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(_HASH_PREFIX + data)
    return digest.hexdigest()


def proof_identity_hash(record: ProofIdentityRecord) -> str:
    return stable_hash(record.content_for_hash(_IDENTITY_HASH_EXCLUDE))


def genesis_root_hash(record: ProofIdentityRecord) -> str:
    return stable_hash(record.content_for_hash(_GENESIS_ROOT_EXCLUDE))


def lineage_event_hash(event: LineageEvent) -> str:
    return stable_hash(event.content_for_hash())


def make_integrity_tag(
    record: Union[ProofIdentityRecord, LineageEvent],
    local_key: bytes,
) -> str:
    if isinstance(record, ProofIdentityRecord):
        message = record.content_for_hash(_IDENTITY_HASH_EXCLUDE)
    else:
        message = record.content_for_hash()
    return hmac.new(local_key, message, hashlib.sha256).hexdigest()
