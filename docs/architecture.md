# Architecture

## Overview

`velvet-continuity-spine` is a structural layer in the Velvet AI ecosystem. It defines record types, validation rules, and payload formatters that allow a Velvet AI runtime to maintain coherent identity and context across restarts, surface transitions, and hardware resets — without cloud dependency.

This repository defines **structure only**. It produces records. Other layers consume them.

## Position in the Velvet Ecosystem

```
velvet-event-protocol       ← event language and enforcement bus
velvet-receipts             ← accountability and hash-chained logging
velvet-runtime              ← bootstrap, wiring, enforcement
velvet-continuity-spine     ← identity, lineage, context, drift (this repo)
velvet-gateway              ← external interface layer
velvet-ecu-intelligence     ← read-only firmware analysis
VelvetNAV                   ← perception and spatial awareness
```

The continuity spine feeds into the receipts layer via `ContinuityReceiptBridge`. It does not depend on the receipts layer at runtime.

## Record Types

| Record | Module | Purpose |
|--------|--------|---------|
| `IdentityRecord` | `identity.py` | Stable identity descriptor for a runtime instance |
| `LineageRecord` | `lineage.py` | Verified parent/child continuity link |
| `ContextRecord` | `context_record.py` | Bounded runtime context snapshot |
| `DriftEvent` | `drift_event.py` | Structured description of detected divergence |
| `SurfaceBinding` | `surface_binding.py` | Instance-to-surface association record |

## Supporting Modules

| Module | Purpose |
|--------|---------|
| `drift_detector.py` | Pure comparison logic producing `DriftEvent` records |
| `receipt_bridge.py` | Formats records as receipt-compatible payload dicts |
| `spine.py` | Thin facade joining index, detector, and bridge |
| `memory_index.py` | In-process key/value store for identity records |
| `recovery_hooks.py` | Callback registry for drift event handling |
| `storage.py` | Local filesystem JSON persistence |
| `validation.py` | Shared fail-closed field validators |

## Data Flow

```
Runtime boot
  └─ IdentityRecord established
       └─ LineageRecord computed and linked
            └─ ContextRecord captured (initial snapshot)
                 └─ [periodic] ContextRecord captured
                      └─ DriftDetector.compare_identity(expected, observed)
                           └─ DriftEvent(s) produced
                                └─ ContinuityReceiptBridge formats payloads
                                     └─ velvet-receipts logs them
                                └─ RecoveryHooks.run(event) dispatches locally
```

## Design Constraints

- **Stdlib only.** No external runtime dependencies.
- **Fail-closed.** Records with missing required fields raise `ValidationError` at construction. No partial construction.
- **Immutable records.** All record dataclasses are `frozen=True`.
- **No actuation.** No executor calls, no event bus writes, no network I/O.
- **No private content.** Records store structural descriptors only.
