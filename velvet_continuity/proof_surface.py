# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.proof_surface
=================================
Surface fingerprint generation for the v0.1.1 mechanical continuity proof
layer.

Produces a deterministic, stable identifier for the hardware/OS environment
this Velvet AI instance is running on. Safe for cheap embedded Linux hardware:
no network calls, no external dependencies, reads only stable kernel/platform
attributes.

The fingerprint is NOT a secret. It is a non-biometric, non-credential
descriptor used for lineage binding and drift detection only.
"""

from __future__ import annotations

import os
import platform

from velvet_continuity.proof_hashing import stable_hash


def generate_surface_fingerprint(user_label: str = "") -> str:
    """
    Generate a stable surface fingerprint for this hardware/OS environment.

    Combines platform metadata and, when available on Linux,
    ``/etc/machine-id``. A ``user_label`` may be supplied to
    disambiguate multiple instances on the same host.

    Parameters
    ----------
    user_label : str
        Optional caller-supplied label (e.g. deployment name or slot ID).
        Empty string is treated as ``"default"``.

    Returns
    -------
    str
        Lowercase hex SHA-256 fingerprint string.
    """
    parts: list[str] = [
        user_label.strip() or "default",
        platform.node(),
        platform.machine(),
        platform.system(),
        platform.version(),
    ]

    try:
        machine_id_path = "/etc/machine-id"
        if os.path.exists(machine_id_path):
            with open(machine_id_path, "rb") as fh:
                parts.append(fh.read().strip().decode(errors="replace"))
    except OSError:
        pass

    raw = "|".join(parts).encode("utf-8")
    return stable_hash(raw)
