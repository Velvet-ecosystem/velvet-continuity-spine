# SPDX-License-Identifier: GPL-3.0-only
"""Example: create a ContextRecord (bounded runtime context descriptor)."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from velvet_continuity import ContextRecord

record = ContextRecord(
    context_id="ctx-nav-001",
    name="Navigation Context",
    purpose="Bounded context for navigation surface operations.",
    allowed_memory_classes=("route-data", "waypoints", "poi-cache"),
    denied_memory_classes=("identity-root", "authority-tokens"),
    active=True,
)

print("ContextRecord:")
for k, v in record.to_dict().items():
    print(f"  {k}: {v}")

print(f"\nallows 'route-data':    {record.allows('route-data')}")
print(f"denies 'identity-root': {record.denies('identity-root')}")
