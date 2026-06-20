# SPDX-License-Identifier: GPL-3.0-only
"""Example: format continuity records as receipt-compatible payloads."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from velvet_continuity import ContinuityReceiptBridge, IdentityRecord, DriftEvent

bridge = ContinuityReceiptBridge()

# Identity created
record = IdentityRecord(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
)
payload = bridge.identity_created(record)
print("Receipt payload (IDENTITY_CREATED):")
for k, v in payload.items():
    if k != "payload":
        print(f"  {k}: {v}")
print()

# Drift detected
event = DriftEvent(
    drift_type="surface",
    severity="medium",
    expected="nav",
    observed="audio",
    action="review",
)
drift_payload = bridge.drift_detected(event, subject_id="node-001")
print("Receipt payload (DRIFT_DETECTED):")
for k, v in drift_payload.items():
    if k != "payload":
        print(f"  {k}: {v}")
print()
print("Pass these dicts to your velvet-receipts layer for persistence.")
