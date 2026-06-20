# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.proof_hashing
=================================
Deterministic hashing and local HMAC integrity tagging for the v0.1.1
mechanical continuity proof layer.

All functions are pure (no I/O, no side effects). Safe for cheap embedded
hardware: SHA-256 and HMAC-SHA256 only, via stdlib hashlib and hmac.

Version prefix
--------------
``stable_hash`` prefixes its input with ``b"VELVET_SPINE_V1:"`` before
hashing. This prefix is part of the hash contract for v0.1.1 records.
A future schema version bump must use a different prefix.
"""

from __future__ import annotations

import hashlib
import hmac

from velvet_continuity.proof_records import LineageEvent, ProofIdentityRecord

# Fields excluded from the identity record hash. The integrity_tag is a
# MAC over the content, so it cannot be part of the content it covers.
_IDENTITY_HASH_EXCLUDE: frozenset[str] = frozenset({"integrity_tag"})

# Fields excluded from the genesis root hash. At genesis creation time,
# id and lineage_root are not yet known — they are derived FROM this hash.
_GENESIS_ROOT_EXCLUDE: frozenset[str] = frozenset({"id", "lineage_root", "integrity_tag"})

# Domain separation prefix — part of the hash contract for this version.
_HASH_PREFIX: bytes = b"VELVET_SPINE_V1:"


def stable_hash(data: bytes) -> str:
    """
    Return the hex SHA-256 digest of ``_HASH_PREFIX + data``.

    This is the single canonical hash primitive for all proof records.
    """
    h = hashlib.sha256()
    h.update(_HASH_PREFIX + data)
    return h.hexdigest()


def proof_identity_hash(record: ProofIdentityRecord) -> str:
    """
    Return the canonical hash of a ProofIdentityRecord.

    Excludes ``integrity_tag`` so that the hash is stable regardless of
    whether the tag has been computed or re-keyed.
    """
    return stable_hash(record.content_for_hash(_IDENTITY_HASH_EXCLUDE))


def genesis_root_hash(record: ProofIdentityRecord) -> str:
    """
    Return the genesis root hash for a record.

    Excludes ``id``, ``lineage_root``, and ``integrity_tag`` so that
    the root can be computed before those fields are assigned.
    This hash becomes both the ``lineage_root`` and the suffix of ``id``.
    """
    return stable_hash(record.content_for_hash(_GENESIS_ROOT_EXCLUDE))


def lineage_event_hash(event: LineageEvent) -> str:
    """
    Return the canonical hash of a LineageEvent.

    Excludes ``integrity_tag`` so the hash is stable across re-keying.
    """
    return stable_hash(event.content_for_hash())


def make_integrity_tag(
    record: ProofIdentityRecord | LineageEvent,
    local_key: bytes,
) -> str:
    """
    Compute a local HMAC-SHA256 integrity tag for a record.

    The tag covers the same content as the hash function for that record
    type (i.e. excludes ``integrity_tag``). The tag is keyed with
    ``local_key`` and is only meaningful on the node that holds the key.

    Parameters
    ----------
    record : ProofIdentityRecord | LineageEvent
        The record to tag.
    local_key : bytes
        Node-local HMAC key. Must not be empty.

    Returns
    -------
    str
        Lowercase hex HMAC-SHA256 digest.
    """
    if isinstance(record, ProofIdentityRecord):
        msg = record.content_for_hash(_IDENTITY_HASH_EXCLUDE)
    else:
        msg = record.content_for_hash()
    return hmac.new(local_key, msg, hashlib.sha256).hexdigest()
