# SPDX-License-Identifier: GPL-3.0-only
"""Example: detect drift between two IdentityRecord snapshots."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from velvet_continuity import DriftDetector, IdentityRecord

BASE = dict(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
    receipt_chain_anchor="sha256:genesis-placeholder",
)

expected = IdentityRecord(**BASE)
# Simulate a drift: surface changed, authority_scope changed
observed = IdentityRecord(**{**BASE, "surface": "audio", "authority_scope": "unrestricted"})

events = DriftDetector().compare_identity(expected, observed)
print(f"Drift events detected: {len(events)}")
for e in events:
    print(f"  [{e.severity.upper():8}] {e.drift_type}: {e.expected!r} -> {e.observed!r}")
