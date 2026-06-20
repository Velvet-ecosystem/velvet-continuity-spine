# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.memory_index
================================
MemoryIndex: lightweight in-process index for continuity records.

Used by ContinuitySpine to hold registered identity records during
a runtime session. Not persistent — use storage.py for disk writes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryIndex:
    """
    Simple in-process key/value index for continuity record dicts.

    Not thread-safe. Intended for single-threaded runtime use or
    test scaffolding.
    """

    records: dict[str, dict[str, Any]] = field(default_factory=dict)

    def add(self, key: str, value: dict[str, Any]) -> None:
        """
        Store a record dict under key. Overwrites any existing entry.

        Raises ValueError if key is empty.
        """
        if not key or not key.strip():
            raise ValueError("key must be a non-empty string")
        if not isinstance(value, dict):
            raise TypeError(f"value must be a dict, got {type(value).__name__}")
        self.records[key] = dict(value)

    def get(self, key: str) -> dict[str, Any] | None:
        """Return a copy of the stored dict for key, or None if not found."""
        value = self.records.get(key)
        return None if value is None else dict(value)

    def remove(self, key: str) -> bool:
        """Remove the record for key. Returns True if it existed."""
        if key in self.records:
            del self.records[key]
            return True
        return False

    def keys(self) -> list[str]:
        """Return a sorted list of all registered keys."""
        return sorted(self.records.keys())

    def __len__(self) -> int:
        return len(self.records)
