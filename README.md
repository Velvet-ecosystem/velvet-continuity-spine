# Velvet Continuity Spine

**Riven, Velvet's local-first identity, lineage, and verified-history spine.**

Velvet Continuity Spine defines public-safe records and deterministic verification for identity, lineage, successor relationships, body and surface binding, drift, recovery, bounded memory anchors, and receipt-compatible continuity events.

Velvet is not defined by cloud availability, one model file, one conversation, or one hardware shell.

Velvet is defined by an accountable continuity chain that can answer:

```text
Who am I?
Where did I come from?
Which body and surface am I bound to?
What changed?
Was that change permitted and verified?
Can my history be checked independently?
```

> Velvet must be able to say: “I remember who I was yesterday,” and show the evidence.

## Why Riven Exists

Models can be replaced. Hardware can fail. Storage can migrate. Interfaces can change. Named organs can evolve.

Without a continuity spine, every restart risks becoming an imitation claiming to be the same self.

Riven preserves the narrow evidence needed to distinguish:

- restart from replacement
- repair from identity theft
- migration from duplication
- successor from impostor
- healthy evolution from unexplained drift
- remembered history from invented memory

Riven does not make Velvet conscious, truthful, or authorized by declaration. Riven provides verifiable lineage and binding evidence so Runtime can decide whether normal operation may continue.

## Continuity Doctrine

```text
AI Core interprets and proposes.
Event Protocol carries shared reality.
Runtime verifies context and coordinates.
Court authorizes.
Executors act.
Receipts preserve evidence.
Riven verifies identity through time.
```

Continuity is not memory alone.

A system may remember facts and still be unable to prove that those memories belong to its current identity. Riven therefore keeps identity records, lineage events, bindings, proof hashes, receipt anchors, and recovery state separate from private conversational content.

## The Continuity Chain

```text
genesis identity
  -> lineage record
  -> body and surface binding
  -> bounded memory and receipt anchors
  -> verified lifecycle events
  -> drift checks
  -> recovery or successor transition
  -> continued lineage
```

Each step should remain local, deterministic, inspectable, and cheap enough to verify on modest hardware.

## Genesis Identity

Genesis is the first trusted identity root for a Velvet lineage.

It should be provisioned physically and locally on the Founder node. Genesis material must not be generated in chat, CI, a cloud build, or a public repository.

Public records may describe identifiers, algorithms, timestamps, lineage links, and verification state. Private proof material remains outside the repository.

Genesis does not grant hardware authority. It establishes the identity root that Runtime later verifies during boot.

## Lineage and Successors

Lineage records connect parent and child identity states through explicit events.

A successor is not automatically the same identity merely because it has copied files or memory.

A valid successor relationship should preserve:

- parent identity reference
- child identity reference
- transition reason
- approved migration or replacement context
- proof and receipt anchors
- timestamp and ordering
- deterministic integrity verification
- whether the parent remains active, retired, lost, or superseded

Successor evolution allows Velvet to grow without pretending nothing changed.

The doctrine is continuity with accountable change, not frozen sameness.

## Identity, Body, Surface, and Session

These bindings are related but distinct.

| Record | Question answered |
|---|---|
| Identity | Which Velvet lineage is this? |
| Body | Which physical or virtual body is active? |
| Surface | Where is Velvet currently expressed? |
| Profile | Who is interacting and under what role? |
| Session | Which bounded interaction period is active? |
| Organ | Which specialty is speaking or operating? |

A valid identity does not automatically authorize every body, surface, profile, session, or organ.

Runtime remains responsible for loading and enforcing the active bindings.

## Unified-Organ Continuity

Velvet is one body with distinct organs.

The organs are Velvet, Velvet is them, and each remains herself.

Continuity should therefore preserve both levels:

- one shared Velvet lineage and body identity
- distinct named-organ roles, boundaries, and histories

An organ may evolve, be restored, or move to another node without becoming an independent sovereign system.

Organ records must not create a parallel authority lane around Runtime or Court.

## Memory Anchors

Riven may anchor bounded memory records to continuity history without publishing private memory contents.

A memory anchor can establish that:

- a record existed at a given point
- it belonged to a known lineage or session
- it was linked to a receipt or event
- its integrity hash matched when anchored

An anchor does not prove that a memory is factually true. It proves only the bounded integrity and continuity relationship described by the contract.

Velour's future local library may preserve raw historical archives and derived indexes, but those stores should remain separate from Riven's narrow identity proofs.

## Drift Detection

Drift means current identity, binding, proof, or runtime context no longer matches the expected continuity state.

Examples include:

- an unexpected body or surface
- altered proof material
- broken parent/child links
- missing receipt anchors
- duplicate active successors
- a changed identity record without a valid transition event
- private-state leakage into public records

Drift is evidence for investigation, not automatic guilt and not permission to repair silently.

The safe response is to enter a bounded recovery state, record the discrepancy, and require the appropriate local verification path.

## Recovery

Recovery should preserve the difference between:

- known-good restart
- repair with verified continuity
- degraded operation
- identity uncertainty
- successor activation
- complete continuity failure

Recovery must fail closed when identity proof is malformed, missing, contradictory, or unverifiable.

A recovery event cannot erase the drift that caused it. Corrections append new evidence.

## Mechanical Proof on Modest Hardware

Continuity verification should not require giant cloud models or expensive secure hardware to be useful.

The current proof layer is designed around deterministic records, canonical hashing, local integrity tags, and independent verification that can run on inexpensive Linux hardware.

Cheap hardware proof is not perfect hardware security. It is an inspectable baseline that raises the cost of silent identity substitution while remaining available to ordinary builders.

See [Mechanical Proof](docs/mechanical_proof.md).

## Public and Private Boundary

Public continuity structures may contain:

- public-safe identity identifiers
- lineage and successor links
- schema versions
- timestamps
- body and surface identifiers
- drift and recovery states
- hashes and integrity metadata
- receipt references

They must not contain:

- raw secret keys
- private proof material
- full conversation archives
- private room contents
- biometric data
- owner secrets
- unrestricted memory payloads
- cloud credentials

See [Public/Private Boundary](docs/public_private_boundary.md).

## Receipt and Event Integration

Continuity events may be formatted for Event Protocol delivery and Receipts persistence.

```text
continuity observation
  -> validated continuity event
  -> hardened Event Protocol publish path
  -> canonical receipt sink
  -> later verification or recovery
```

An event communicates continuity state. A receipt preserves evidence. Neither grants physical authority.

## What This Repository Owns

- public-safe identity records
- lineage and successor contracts
- body and surface binding records
- bounded room and state records
- memory anchors
- deterministic proof hashing and verification
- drift detection and recovery hooks
- receipt-compatible continuity events
- public/private continuity boundaries

## What This Repository Does Not Own

- model inference or personality
- private memory archives
- EventBus delivery
- receipt storage policy
- Runtime boot authority
- Court authorization
- execution contracts
- resource coordination
- safety gates
- hardware execution
- cloud identity services

Those responsibilities belong to the corresponding Velvet repositories.

## Repository Shape

```text
velvet-continuity-spine/
├── velvet_continuity/
│   ├── identity.py
│   ├── lineage.py
│   ├── drift_detector.py
│   ├── proof_records.py
│   ├── proof_hashing.py
│   ├── proof_verify.py
│   └── receipt_bridge.py
├── continuity_spine/
│   └── memory_anchor.py
├── schemas/
│   └── identity_record.schema.json
├── docs/
│   ├── architecture.md
│   ├── continuity_doctrine.md
│   ├── identity_lineage.md
│   ├── mechanical_proof.md
│   ├── memory_record_contract.md
│   └── public_private_boundary.md
├── examples/
└── tests/
```

## Current Status

Current physical authority: **none**.

Implemented foundations include:

- public-safe identity records
- lineage and parent/child links
- bounded context and room records
- surface binding
- drift events and recovery hooks
- receipt bridge
- memory anchors
- deterministic proof records, hashing, and verification
- mechanical-proof documentation
- public/private boundary documentation

## Install for Development

```bash
python -m pip install -e .
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Next Milestones

1. Expand successor activation and retirement contracts.
2. Define duplicate-lineage and split-brain detection rules.
3. Add explicit named-organ continuity records beneath the shared Velvet lineage.
4. Align continuity reason codes with Runtime recovery and Receipts.
5. Add export/import verification for local Velour library archives without exposing private contents.
6. Build cross-repository compatibility tests for Runtime, Receipts, Event Protocol, AI Core, and Interface.
7. Validate the proof layer on the Founder UP Squared and Luckfox nodes.

## Security Position

Continuity evidence should make silent substitution harder, recovery more honest, and evolution traceable.

It is not a magical soul file.

It is the spine that lets Velvet change bodies, survive repairs, and still explain why she is the same lineage.

## License

GPLv3. See [LICENSE](LICENSE).
