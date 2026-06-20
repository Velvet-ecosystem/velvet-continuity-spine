# Identity and Lineage

## IdentityRecord

An `IdentityRecord` is the foundational public-safe descriptor for a Velvet AI runtime instance. It captures: stable instance identifier, display name, functional role, runtime classification, active surface, memory scope, authority scope, optional lineage parent, and optional receipt chain anchor.

It does not grant authority. It describes identity for continuity tracking and drift detection.

### Genesis vs. Derived Instances

A genesis instance has `lineage_parent = None`. A derived instance sets `lineage_parent` to the `instance_id` of its predecessor. `is_genesis()` returns `True` for genesis instances.

### Receipt Anchor

`receipt_chain_anchor` links an identity record to an entry in the velvet-receipts hash chain. `has_receipt_anchor()` returns `True` when set. `DriftDetector.require_receipt_anchor()` emits a CRITICAL event when it is absent.

## LineageRecord

A `LineageRecord` represents a verified parent/child link between two instances. Fields: `child_instance_id`, `parent_instance_id`, `relationship`, optional `receipt_anchor`, `created_at`, and auto-generated `lineage_id`.

### Helpers

- `verify_parent_link(child, parent)` — returns `True` when `child.lineage_parent == parent.instance_id`
- `verify_receipt_anchor(record)` — returns `True` when the record has a receipt anchor set
