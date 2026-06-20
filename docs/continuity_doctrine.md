# Continuity Doctrine

## Core Statement

A Velvet AI system must be able to answer: *"Who am I, and what was I doing?"* after any restart, surface transition, or hardware reset — using only locally stored records. Cloud connectivity is not required and must not be required.

## Doctrine Rules

### 1. Local-first identity
Identity is established from locally stored `IdentityRecord` and `LineageRecord` data. If no local records exist, the system starts as a genesis instance. It does not query a remote authority.

### 2. Fail-closed construction
Record construction rejects incomplete or invalid input immediately. A partially constructed record must never be used. Callers handle `ValidationError` at construction time.

### 3. Separation of structure and content
This repository stores structural records: identifiers, hashes, timestamps, surface names, and memory class labels. It does not store memory content, conversation history, private user data, or session narratives.

### 4. No authority bypass
A continuity record does not grant permissions. Records are informational, not authoritative.

### 5. No actuation
This package produces records. It does not trigger actions, write to the event bus, or call executor interfaces.

### 6. Receipt compatibility
Continuity events that warrant logging must be formatted as receipt-compatible payloads via `ContinuityReceiptBridge` and passed to the receipts layer. They must not be silently discarded.

### 7. Drift is informational, not self-correcting
`DriftDetector` emits `DriftEvent` records. It does not initiate recovery. The runtime or a recovery hook decides whether to act on a drift event, and under what authority.

## Governance Chain

```
LLMs propose.
Court decides.
Executors enforce.
Receipts remember.
Continuity Spine verifies identity.
```
