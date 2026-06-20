# Changelog

All notable changes to `velvet-continuity-spine` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [0.1.1] — Mechanical proof hardening

### Added
- `ProofIdentityRecord` — versioned, hash-chained identity snapshot with local HMAC integrity tag and explicit authority level
- `LineageEvent` — receipted link between two consecutive identity record hashes
- Canonical proof hashing helpers (`stable_hash`, `proof_identity_hash`, `genesis_root_hash`, `lineage_event_hash`) with domain prefix `VELVET_SPINE_V1:`
- Local HMAC-SHA256 integrity tags (`make_integrity_tag`) — node-local, never serialised to remote
- Genesis identity creation (`create_genesis_identity`) with fail-closed input validation
- Successor identity evolution (`create_successor_identity`) preserving `id`, `genesis_ts`, `genesis_proof`, and `lineage_root`
- Lineage event creation and verification (`create_lineage_event`, `verify_lineage_event`)
- Deterministic lineage chain verification (`verify_lineage_chain`) — returns `chain[-1].authority_level` on success, `0` on any failure
- Cheap-hardware-friendly surface fingerprint helper (`generate_surface_fingerprint`) — stdlib only, reads `/etc/machine-id` on Linux
- `require_authority_level` validator: allows `>= 0`, rejects negative and non-integer values
- 62 new proof-layer tests in `tests/test_proof_layer.py`
- `docs/mechanical_proof.md` — proof layer architecture reference

### Notes
- Hash domain prefix `VELVET_SPINE_V1:` is the committed schema version prefix. Records persisted under this prefix are forward-compatible within proof schema v1.
- No CLI, ReceiptBridge expansion, or drift policy engine in this patch.
- Total test count: 181 passing.

---

## [0.1.0] — Initial release

### Added
- `IdentityRecord` — public-safe identity descriptor for a Velvet AI runtime instance
- `LineageRecord` — parent/child continuity link between identity records
- `ContextRecord` — bounded runtime context descriptor (allowed/denied memory classes, active state)
- `DriftEvent` — structured record of a detected continuity drift condition, with `DriftSeverity` enum
- `DriftDetector` — pure comparison logic producing `DriftEvent` records from identity snapshots
- `SurfaceBinding` — association between a Velvet AI instance and a named surface
- `ContinuityReceiptBridge` — formats continuity records as receipt-compatible payload dicts
- `ContinuitySpine` — thin facade joining identity index, drift detection, and receipt formatting
- `RecoveryHooks` — registry for local drift event callbacks
- `MemoryIndex` — lightweight in-process index for continuity records
- `ValidationError` — base exception for field validation failures
- `storage.py` — local filesystem JSON persistence helpers
- JSON schemas for all record types
- 119 stdlib `unittest` tests covering construction, fail-closed validation, serialisation, and helpers
- Full `docs/` with architecture, doctrine, and boundary guidance

### Notes
- `RoomRecord` was considered and rejected as a public name; `ContextRecord` is used throughout.
- `DriftEvent` is defined in its own module (`drift_event.py`) separate from `DriftDetector`.
- No external runtime dependencies. Python 3.10+ required.
