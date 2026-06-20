# Cross-Surface Memory Governance

## What This Package Provides

- `SurfaceBinding` records — which instance is bound to which surface, under what authority, with what memory class permissions
- `ContextRecord.allowed_memory_classes` / `denied_memory_classes` — memory boundary definition per context
- Receipt-compatible payloads for surface bind events via `ContinuityReceiptBridge.surface_bound()`

## What This Package Does Not Provide

- Shared memory content across surfaces (belongs in layers with appropriate access controls)
- Cross-surface event routing (belongs in `velvet-event-protocol`)
- Surface rendering or display logic (belongs in surface-specific layers)
- Authority grants based on surface type (surface type is informational only)

## SurfaceBinding Fields

| Field | Description |
|-------|-------------|
| `surface_id` | Unique surface identifier (e.g. "nav-primary") |
| `surface_type` | Classification (e.g. "nav", "audio", "cluster", "mobile", "home", "custom") |
| `bound_instance_id` | The Velvet AI instance bound to this surface |
| `trusted_by` | Authority scope or instance_id that authorised this binding |
| `allowed_memory_classes` | Memory classes permitted on this surface |
| `denied_memory_classes` | Memory classes explicitly excluded |
| `receipt_anchor` | Optional receipt chain anchor for this binding event |

## Transition Pattern

When an instance transitions between surfaces:
1. Create a new `SurfaceBinding` for the new surface
2. Format `SURFACE_BOUND` receipt payload via `ContinuityReceiptBridge`
3. Record a new `ContextRecord` reflecting the updated surface set
4. Pass both to the receipts layer
