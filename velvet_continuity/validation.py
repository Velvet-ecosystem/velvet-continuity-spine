# SPDX-License-Identifier: GPL-3.0-only
"""
velvet_continuity.validation
==============================
Shared validation helpers for continuity records.

All validators fail closed: missing or invalid required fields raise
ValidationError immediately. Callers must handle or propagate.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


class ValidationError(ValueError):
    """Raised when a continuity record fails field validation."""


def require_non_empty(value: str, field_name: str) -> None:
    """Fail closed when a required string field is missing or blank."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(
            f"'{field_name}' must be a non-empty string, got {value!r}"
        )


def require_string_sequence(value: Any, field_name: str) -> None:
    """
    Require a non-string sequence containing only non-empty strings.

    Accepts list or tuple; rejects bare strings, non-sequences, and
    sequences containing non-string or empty-string elements.
    Intentional empty sequence (length 0) is allowed.
    """
    if isinstance(value, str) or not isinstance(value, Sequence):
        raise ValidationError(
            f"'{field_name}' must be a sequence of strings, "
            f"got {type(value).__name__}"
        )
    for i, item in enumerate(value):
        if not isinstance(item, str):
            raise ValidationError(
                f"'{field_name}[{i}]' must be a string, "
                f"got {type(item).__name__}"
            )
        if not item.strip():
            raise ValidationError(
                f"'{field_name}[{i}]' must be a non-empty string, got {item!r}"
            )


# Keep the old name as an alias — existing callers in the v0.1.0 code use
# require_string_tuple (surface_binding.py, context_record.py).
require_string_tuple = require_string_sequence


def require_mapping(value: Mapping[str, Any], field_name: str) -> None:
    """Require a mapping (dict-like) object."""
    if not isinstance(value, Mapping):
        raise ValidationError(
            f"'{field_name}' must be a mapping, got {type(value).__name__}"
        )


def require_authority_level(value: Any, field_name: str = "authority_level") -> None:
    """
    Require a non-negative integer authority level.

    - authority_level == 0: recovery-only / downgraded state. Allowed.
    - authority_level >= 1: live operational state. Allowed.
    - authority_level < 0: rejected.
    - non-integer: rejected.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(
            f"'{field_name}' must be an integer, got {type(value).__name__}"
        )
    if value < 0:
        raise ValidationError(
            f"'{field_name}' must be >= 0, got {value}"
        )
