# SPDX-License-Identifier: GPL-3.0-only
# Mechanical Proof Layer (v0.1.1)

The v0.1.1 proof layer adds deterministic, offline-verifiable continuity
proofs to the Velvet AI continuity spine. It is designed for cheap embedded
Linux hardware: stdlib only, SHA-256 and HMAC-SHA256, no network calls.

## Modules

| Module | Purpose |
|--------|---------|
| `proof_records.py` | `ProofIdentityRecord`, `LineageEvent` dataclasses |
| `proof_hashing.py` | Canonical hash primitives and HMAC integrity tagging |
| `proof_verify.py` | Factory functions and verification logic |
| `proof_surface.py` | Hardware surface fingerprint generation |

---

## Core concepts

### Genesis root

A genesis identity record is the root of a lineage chain. Its `id` and
`lineage_root` are both derived from a single hash of the record's stable
fields (`genesis_proof`, `model_fingerprint`, `surface_fingerprint`,
`genesis_ts`, etc.) — computed before `id` and `lineage_root` are assigned,
so there is no circularity.

```
lineage_root = stable_hash(record_content_excluding_id_and_root)
id           = "velvet:instance:<lineage_root>"
```

Both values are frozen into every successor record and never change for
the lifetime of the chain.

### Successor identity

A successor record extends the chain by setting `previous_hash` to the
hash of its predecessor. All other lineage fields (`id`, `genesis_ts`,
`genesis_proof`, `lineage_root`) are copied unchanged.

```
successor.previous_hash = proof_identity_hash(predecessor)
```

Only `model_fingerprint`, `surface_fingerprint`, `active_context_hashes`,
and `authority_level` may change between records.

### Lineage events

A `LineageEvent` is a receipted link between two consecutive record hashes.
It records the `from_identity_hash`, `to_identity_hash`, `event_type`,
`description`, and an optional `receipt_anchor` for the velvet-receipts
layer. It carries its own HMAC integrity tag.

```python
event = create_lineage_event(from_record, to_record, "MODEL_UPGRADE", "...", key)
valid, errors = verify_lineage_event(event, from_record, to_record, key)
```

### Integrity tags

Every `ProofIdentityRecord` and `LineageEvent` carries a local
HMAC-SHA256 `integrity_tag`. The tag is computed over the record content
**excluding** the `integrity_tag` field itself, keyed with a node-local
`bytes` key that is never serialised or transmitted.

The tag is excluded from the canonical content hash so that re-keying a
record does not change its hash identity.

### Tail authority

`verify_lineage_chain` returns a three-tuple `(valid, errors, authority)`.

- **Valid chain** → `authority = chain[-1].authority_level`
- **Invalid chain** → `authority = 0`

Genesis defines identity root. The tail record defines current live
authority. `authority_level == 0` is a valid downgraded/recovery state.
Negative authority levels are rejected at construction time.

### Cheap-hardware proof class

The proof layer is designed to run on constrained embedded Linux hardware:

- One hash primitive: SHA-256 via `hashlib`
- One MAC primitive: HMAC-SHA256 via `hmac`
- No external dependencies
- No floating-point, no network, no threads
- Deterministic: same inputs always produce the same hashes

`generate_surface_fingerprint()` produces a stable hardware descriptor
from platform metadata and `/etc/machine-id` (when available), suitable
for use as `surface_fp` in genesis records.

---

## Not in this patch

- No CLI
- No ReceiptBridge integration (proof payloads are formatted here but
  passing them to velvet-receipts is deferred to a future patch)
- No drift policy engine
- No LLM-based verification
