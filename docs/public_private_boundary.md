# Public / Private Boundary

## What Belongs in This Repository

- Record dataclasses (`IdentityRecord`, `LineageRecord`, `ContextRecord`, `DriftEvent`, `SurfaceBinding`)
- Validation logic and helpers
- Drift detection logic (structural field comparison)
- `ContinuityReceiptBridge` (payload formatting only — no receipt persistence)
- Local storage helpers (`storage.py`)
- JSON schemas for all record types
- Public-safe examples using neutral placeholder values
- Architecture and doctrine documentation

## What Does Not Belong Here

- Private memory content of any kind
- Session narratives or conversation history
- Personal user data
- Deployment-specific secrets, credentials, or tokens
- Internal project naming conventions or symbolic identifiers beyond technical field names
- Private lore, thematic material, or roleplay content
- Real hardware fingerprints, serial numbers, or device identifiers
- Authentication material or access tokens

## Example Value Standards

All example code and test fixtures must use neutral technical placeholder values:

| Do use | Do not use |
|--------|-----------|
| `"node-001"` | Internal symbolic instance names |
| `"navigator"` | Internal role titles |
| `"embedded-node"` | Internal classification names |
| `"nav"`, `"audio"`, `"cluster"` | Private surface identifiers |
| `"local-bounded"` | Internal scope descriptors tied to private naming |
| `"sha256:genesis-placeholder"` | Real hash values |

## Contribution Guidelines

1. All example code must use neutral placeholder values.
2. All documentation must describe structural concerns only.
3. New record types must follow the established pattern: frozen dataclass, fail-closed `__post_init__`, `to_dict()`, JSON schema.
4. Tests must cover both valid construction and fail-closed rejection of invalid input.
5. No external runtime dependencies. Use the Python standard library.
6. SPDX license header required on all new Python files: `# SPDX-License-Identifier: GPL-3.0-only`

## License

All contributions are licensed under GPL-3.0-only. See `LICENSE`.
