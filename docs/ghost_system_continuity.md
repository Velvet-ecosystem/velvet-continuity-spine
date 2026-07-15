# Ghost System Continuity

Velvet Continuity Spine records that a sealed public Ghost System run happened without storing private memory or granting physical authority.

## Canonical event

```text
vehicle.can.ghost_observation
```

## Record

`GhostRunRecord` links a synthetic observation event to an optional receipt anchor, public repo fingerprints, a bounded frame count, and explicit safety assertions.

A valid record requires:

```text
read_only: true
synthetic_fixture: true
physical_bus_opened: false
can_transmission_attempted: false
actuation_performed: false
authority_granted: false
```

Any unsafe value fails closed.

## Receipt bridge

`ContinuityReceiptBridge.ghost_run_recorded(record)` produces a plain `GHOST_RUN_RECORDED` envelope. The bridge does not import `velvet-receipts`, publish events, or write files.

## Spine facade

`ContinuitySpine.record_ghost_run(record)` stores the public-safe record under:

```text
ghost-run:<run_id>
```

and returns the receipt-compatible envelope.

## Boundary

The record must not contain private conversations, handmaiden memory, medical logic, driver-assist logic, real vehicle actuation data, secrets, tokens, or dangerous wiring details.

It remembers the sealed run, not the contents of a private mind. The ghost car stays in the jar, but it leaves a verifiable footprint.
