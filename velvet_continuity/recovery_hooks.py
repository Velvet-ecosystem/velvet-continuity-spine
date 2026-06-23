# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.recovery_hooks
==================================
RecoveryHooks: register and run local callbacks for drift events.

Recovery hooks are called with DriftEvent records produced by DriftDetector.
They do not execute actions directly. They are callbacks that the runtime
registers and runs under its own governance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from velvet_continuity.drift_event import DriftEvent

RecoveryCallback = Callable[[DriftEvent], None]


@dataclass
class RecoveryHooks:
    """Registry of local callbacks for drift event handling."""

    callbacks: list[RecoveryCallback] = field(default_factory=list)

    def register(self, callback: RecoveryCallback) -> None:
        if not callable(callback):
            raise TypeError(
                f"callback must be callable, got {type(callback).__name__}"
            )
        self.callbacks.append(callback)

    def run(self, event: DriftEvent) -> None:
        if not isinstance(event, DriftEvent):
            raise TypeError(
                f"event must be a DriftEvent, got {type(event).__name__}"
            )
        for callback in self.callbacks:
            callback(event)

    def clear(self) -> None:
        self.callbacks.clear()

    def __len__(self) -> int:
        return len(self.callbacks)
