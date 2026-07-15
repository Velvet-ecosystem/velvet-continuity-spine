# SPDX-License-Identifier: GPL-3.0-only
"""Create a public-safe Ghost System continuity record."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from velvet_continuity import ContinuitySpine, GhostRunRecord


def main() -> int:
    spine = ContinuitySpine()
    record = GhostRunRecord(
        run_id="ghost-run-demo-0001",
        observation_event_id="ghost-can-event-demo-0001",
        receipt_anchor="receipt:ghost-can-demo-0001",
        repo_fingerprints=(
            "velvet-vehicle-can@ghost-system-v0",
            "velvet-runtime@ghost-system-v0",
            "velvet-interface@ghost-system-v0",
        ),
        observed_frame_count=4,
    )
    print(json.dumps(spine.record_ghost_run(record), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
