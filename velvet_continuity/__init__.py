# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity
=================
Local-first continuity records for Velvet AI systems.

Public API surface for v0.1.2.
"""

# --- v0.1.0 record layer ---
from velvet_continuity.context_record import ContextRecord
from velvet_continuity.drift_event import DriftEvent, DriftSeverity
from velvet_continuity.drift_detector import DriftDetector
from velvet_continuity.ghost_run import GhostRunRecord
from velvet_continuity.identity import IdentityRecord
from velvet_continuity.lineage import LineageRecord, verify_parent_link, verify_receipt_anchor
from velvet_continuity.receipt_bridge import ContinuityReceiptBridge
from velvet_continuity.recovery_hooks import RecoveryHooks
from velvet_continuity.spine import ContinuitySpine
from velvet_continuity.surface_binding import SurfaceBinding
from velvet_continuity.validation import ValidationError

# --- v0.1.1 mechanical proof layer ---
from velvet_continuity.proof_records import ProofIdentityRecord, LineageEvent
from velvet_continuity.proof_hashing import (
    proof_identity_hash,
    genesis_root_hash,
    lineage_event_hash,
    make_integrity_tag,
    stable_hash,
)
from velvet_continuity.proof_verify import (
    create_genesis_identity,
    create_successor_identity,
    create_lineage_event,
    verify_lineage_event,
    verify_lineage_chain,
)
from velvet_continuity.proof_surface import generate_surface_fingerprint

__version__ = "0.1.2"

__all__ = [
    # v0.1.0
    "ContinuityReceiptBridge",
    "ContinuitySpine",
    "ContextRecord",
    "DriftDetector",
    "DriftEvent",
    "DriftSeverity",
    "GhostRunRecord",
    "IdentityRecord",
    "LineageRecord",
    "RecoveryHooks",
    "SurfaceBinding",
    "ValidationError",
    "verify_parent_link",
    "verify_receipt_anchor",
    # v0.1.1
    "LineageEvent",
    "ProofIdentityRecord",
    "create_genesis_identity",
    "create_lineage_event",
    "create_successor_identity",
    "generate_surface_fingerprint",
    "genesis_root_hash",
    "lineage_event_hash",
    "make_integrity_tag",
    "proof_identity_hash",
    "stable_hash",
    "verify_lineage_chain",
    "verify_lineage_event",
]
