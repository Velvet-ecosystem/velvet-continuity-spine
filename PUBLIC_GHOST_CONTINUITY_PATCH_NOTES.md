# Public Ghost Continuity Patch Notes

Adds a public-safe continuity marker for Velvet Ghost System v0.

## Added

- `velvet_continuity/ghost_run.py`
- `schemas/ghost_run_record.schema.json`
- `examples/record_ghost_run.py`
- `docs/ghost_system_continuity.md`
- `tests/test_ghost_run.py`

## Integrated

- `ContinuityReceiptBridge.ghost_run_recorded(record)`
- `ContinuitySpine.record_ghost_run(record)`
- `ContinuitySpine.get_ghost_run(run_id)`
- Public package export and version `0.1.2`

## Safety invariants

A Ghost Run record requires read-only synthetic evidence, no physical bus opening, no CAN transmission attempt, no actuation, and no authority grant. Any violation fails closed.
