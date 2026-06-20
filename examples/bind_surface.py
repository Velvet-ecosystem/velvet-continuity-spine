# SPDX-License-Identifier: GPL-3.0-only
"""Example: create a SurfaceBinding."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from velvet_continuity import SurfaceBinding

binding = SurfaceBinding(
    surface_id="nav-primary",
    surface_type="nav",
    bound_instance_id="node-001",
    trusted_by="node-001",
    allowed_memory_classes=("route-data", "waypoints"),
    denied_memory_classes=("identity-root", "authority-tokens"),
    receipt_anchor="sha256:binding-anchor-placeholder",
)

print("SurfaceBinding:")
for k, v in binding.to_dict().items():
    print(f"  {k}: {v}")
