# SPDX-License-Identifier: GPL-3.0-only
"""Surface fingerprint generation for the continuity proof layer."""

import os
import platform
from typing import List

from velvet_continuity.proof_hashing import stable_hash


def generate_surface_fingerprint(user_label: str = "") -> str:
    parts: List[str] = [
        user_label.strip() or "default",
        platform.node(),
        platform.machine(),
        platform.system(),
        platform.version(),
    ]

    try:
        machine_id_path = "/etc/machine-id"
        if os.path.exists(machine_id_path):
            with open(machine_id_path, "rb") as file_handle:
                parts.append(file_handle.read().strip().decode(errors="replace"))
    except OSError:
        pass

    raw = "|".join(parts).encode("utf-8")
    return stable_hash(raw)
