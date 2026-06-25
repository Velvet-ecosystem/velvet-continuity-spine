# Memory Record Continuity Contract

## Status

Public-safe ecosystem contract.

## Purpose

This contract defines the small metadata envelope used when Velvet systems refer to a memory event across Core, Continuity Spine, Receipts, Runtime, and human-facing archive surfaces.

It does not define private memory contents, semantic recall policy, authority, or execution.

## Core distinction

A memory record preserves something remembered.

A receipt preserves accountability for a governed decision or outcome.

A continuity record verifies identity, lineage, binding, or bounded runtime context.

These records may reference one another. They must not replace one another.

## Canonical metadata

| Field | Required | Meaning |
|---|---:|---|
| `schema_version` | yes | Positive integer version of the memory envelope |
| `event_id` | yes | Stable unique identifier for this memory event |
| `ts` | yes | Unix timestamp |
| `kind` | yes | Semantic class of memory |
| `payload` | yes | Event content; may remain private and local |
| `source` | no | Component or surface that produced the record |
| `confidence` | no | Numeric confidence from `0.0` to `1.0` |
| `authority_status` | no | Status such as observed, candidate, accepted, rejected, or superseded |
| `receipt_id` | no | Reference to an accountability receipt |
| `related_event_ids` | no | Stable links to associated memory events |
| `tags` | no | Human-readable indexing hints |

## Memory kinds

- `observation`: direct sensor or system observation
- `conversation`: conversational event or excerpt
- `inference`: derived interpretation that is not established fact
- `candidate`: proposed memory awaiting acceptance or stronger evidence
- `fact`: accepted factual memory under the applicable authority path
- `decision`: remembered decision, normally linked to a receipt when governed
- `execution_result`: remembered executor outcome, normally linked to a receipt
- `continuity`: identity, lineage, drift, binding, or recovery-related memory
- `system`: lifecycle and internal system events

## Authority status

`authority_status` describes the epistemic or governance state of a memory. It does not grant authority.

Recommended values:

- `observed`
- `candidate`
- `accepted`
- `rejected`
- `superseded`
- `historical`

An inference does not become a fact merely because its confidence rises. Acceptance must follow the appropriate owner, Court, policy, or subsystem path.

## Confidence

Confidence expresses uncertainty about a claim or interpretation. It is not permission, priority, or truth.

Confidence:

- must remain between `0.0` and `1.0`
- should name or preserve its source when practical
- may decay or be revised through new linked records
- must not rewrite the original historical record

## Immutability and correction

Memory records are append-only.

Corrections, reinterpretations, rejection, acceptance, compression, and decay are represented by new records linked through `related_event_ids`.

Original records remain inspectable.

## Privacy boundary

Public continuity structures may carry identifiers, classifications, confidence, and receipt anchors.

Private room content, raw conversation text, intimate context, biometric detail, and owner-specific narrative remain outside public continuity records unless explicitly transformed into a public-safe projection.

## Receipt bridge

When a governed decision or executor outcome exists:

1. Memory records what is remembered.
2. Receipts record policy, authority, decision, and outcome.
3. The memory record stores `receipt_id`.
4. The receipt may store the memory `event_id` in its context.
5. Neither record silently absorbs or rewrites the other.

## Continuity bridge

Continuity Spine may refer to memory `event_id` values as recovery anchors, drift evidence, lineage evidence, or bounded-context references.

Continuity Spine does not become the private memory store.

## Human-facing archive projection

Backlinks, graph views, timelines, daily notes, summaries, and Obsidian-compatible projections may be generated from these stable identifiers.

A projection is a view, not the authoritative source.

## Doctrine

Brain proposes.

Court authorizes.

Executors act.

Receipts remember accountability.

Memory preserves experience.

Continuity Spine verifies identity.
