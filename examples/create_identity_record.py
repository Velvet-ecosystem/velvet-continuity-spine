# SPDX-License-Identifier: GPL-3.0-only
"""Example: create and inspect an IdentityRecord."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from velvet_continuity import IdentityRecord

# Genesis instance — no lineage parent
record = IdentityRecord(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
    receipt_chain_anchor="sha256:genesis-placeholder",
)

print("IdentityRecord:")
for k, v in record.to_dict().items():
    print(f"  {k}: {v}")

print(f"\nis_genesis:           {record.is_genesis()}")
print(f"has_receipt_anchor:   {record.has_receipt_anchor()}")
print(f"has_lineage_parent:   {record.has_lineage_parent()}")
