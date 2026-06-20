# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.storage
===========================
Simple JSON storage helpers for continuity records.

No external dependencies. No cloud I/O. Writes are fsynced.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    """Write a dict as indented JSON to path, fsyncing on completion."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, indent=2, sort_keys=True))
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())


def read_json(path: str | Path) -> dict[str, Any]:
    """Read a JSON object from path. Raises ValueError if not an object."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("stored continuity payload must be a JSON object")
    return data
