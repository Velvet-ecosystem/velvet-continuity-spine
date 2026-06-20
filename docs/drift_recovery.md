# Drift Detection and Recovery

## What is Drift?

Drift is detected divergence between two identity snapshots for the same runtime instance. The `DriftDetector` compares `IdentityRecord` pairs field by field and emits `DriftEvent` records for any divergence found.

## Severity Levels

| Value | Meaning |
|-------|---------|
| `info` | Informational; no action required |
| `low` | Minor change; log and continue |
| `medium` | Notable change; flag for review |
| `high` | Significant change; recovery may be warranted |
| `critical` | Severe condition; runtime should halt or escalate |

Use `DriftSeverity` enum values for comparison. `DriftEvent.is_critical()` and `DriftEvent.is_actionable()` are convenience helpers.

## DriftDetector API

- `compare_identity(expected, observed)` — returns a list of `DriftEvent` records (empty if no drift)
- `require_receipt_anchor(record)` — returns a CRITICAL event if the record has no receipt anchor
- `has_critical_drift(events)` — True if any event is CRITICAL
- `highest_severity(events)` — the maximum severity string in a list of events

## Recovery

Recovery logic is not in this package. When drift events are produced:

1. Format them via `ContinuityReceiptBridge.drift_detected()` and pass to the receipts layer.
2. Pass events to registered `RecoveryHooks` callbacks.
3. The runtime (under Court authority) decides what action to take.

This package produces structured records. It does not initiate recovery.
