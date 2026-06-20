# Context Records

> **Note:** This file is named `room_records.md` for backward compatibility with the original scaffold.
> The public class is `ContextRecord`. See `context_record.py`.

## Purpose

A `ContextRecord` is a bounded runtime context descriptor. It captures: a context identifier, name, purpose, which memory classes are permitted, which are denied, and whether the context is currently active.

Context records do not store memory content. They store structural boundaries.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `context_id` | str | Unique identifier for this context |
| `name` | str | Human-readable label |
| `purpose` | str | Technical description of the context's role |
| `allowed_memory_classes` | tuple[str, ...] | Permitted memory class identifiers |
| `denied_memory_classes` | tuple[str, ...] | Explicitly excluded memory class identifiers |
| `active` | bool | Whether this context is currently active |
| `created_at` | str | ISO 8601 creation timestamp |
| `record_id` | str | Auto-generated unique record ID |

## Helpers

- `allows(memory_class)` — returns `True` if the class is in `allowed_memory_classes`
- `denies(memory_class)` — returns `True` if the class is in `denied_memory_classes`
