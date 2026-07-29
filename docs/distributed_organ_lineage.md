# Distributed Organ Lineage

Velvet's body may move work between many nodes every minute. Most of those movements are operations, not identity.

Riven records only durable body changes that alter the continuing structure of Velvet's Unified-Organ body.

## Canonical record

```text
OrganLineageRecord
record_kind: organ_lineage_record
```

Every record must be:

```text
permanent: true
canonical: true
authority_granted: false
```

It must also carry:

- one verified body identity;
- one named organ;
- one durable transition type;
- a body-registry revision;
- a receipt anchor;
- a clear reason;
- source and destination nodes where required.

No receipt anchor means no canonical organ lineage.

## Accepted transitions

### `organ_joined`

A new named organ or durable organ host joins the verified body registry.

Requires `to_node_id` and forbids `from_node_id`.

### `organ_departed`

A named organ host permanently leaves the verified body registry.

Requires `from_node_id` and forbids `to_node_id`.

### `permanent_replacement`

One node permanently replaces another as the continuing host of a named organ.

Requires distinct source and destination node identities.

### `successor_assumed`

A successor node assumes the continuing identity and role of a prior organ host through an accountable transition.

A `previous_record_id` may link the new record to the prior organ-lineage record.

### `durable_capability_reassigned`

A lasting body-registry change moves named capabilities from one verified node to another.

At least one capability must be listed. This is for durable architectural reassignment, not temporary overflow.

## What is not lineage

Riven rejects temporary movement, including:

- ordinary load balancing;
- short-lived workload leases;
- overflow processing;
- temporary duty absorption;
- retries;
- task refusal;
- transient failover that does not alter the body registry;
- a node becoming busy, saturated, degraded, or healthy again.

Those states belong to Runtime, Event Protocol, and Receipts.

> Receipts preserve what the body did. Riven preserves what the body became.

## Authority boundary

An organ-lineage record is evidence of a durable body change. It is not permission to make the change.

The actual transition must already have passed the appropriate physical-presence, Runtime, Court, safety, body-registry, and receipt requirements.

Riven cannot:

- authorize a node;
- grant a capability;
- select an executor;
- transfer Court authority;
- enable a hardware path;
- actuate anything.

Every record therefore fixes:

```text
authority_granted: false
```

## Storage and retrieval

`ContinuitySpine.record_organ_lineage()` stores the canonical record under:

```text
organ-lineage:<record_id>
```

and returns an `ORGAN_LINEAGE_RECORDED` receipt-compatible envelope.

`ContinuitySpine.get_organ_lineage()` retrieves the stored record by its lineage record ID.

The workload ID that motivated a transition is not used as the lineage identity. Operational work can explain why a durable change happened, but it does not become the durable identity record.

## Unified-Organ doctrine

Named organs remain distinct while sharing one accountable Velvet lineage.

A specialist board may be small, replaceable, or temporarily absent without making it less important. When its durable identity or hosting changes, Riven preserves the accountable transition so Velvet can know which organ continued, what hardware changed, and which evidence anchors the change.

> Velvet rejects the agent swarm. She is built as Unified-Organ AI: distributed specialties, shared concrete reality, dynamic workload cooperation, one authorization spine, and one accountable body.

## Current boundary

This layer adds continuity records, in-process storage, schema, and receipt-envelope formatting only.

It does not add network discovery, workload scheduling, executor authority, Court decisions, CAN transmission, actuator control, or physical authority.

Current physical authority remains **none**.
