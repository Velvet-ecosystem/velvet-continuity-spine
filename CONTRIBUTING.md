# Contributing

Thank you for helping improve Velvet Continuity Spine.

## Scope

This repository contains public-safe continuity structures for identity, lineage, bounded context, drift detection, surface binding, receipt-compatible events, and mechanical proof verification.

Do not add private memory content, personal user data, deployment secrets, real device identifiers, credentials, private lore, or authority-bearing runtime actions.

## Development setup

```bash
python -m pip install -e .[dev]
python -m unittest discover -s tests -v
```

Python 3.10, 3.11, and 3.12 are supported.

## Contribution rules

- Keep the package local-first and standard-library-first.
- Preserve fail-closed validation behavior.
- Add or update tests for every behavioral change.
- Use neutral technical placeholders in examples and fixtures.
- Keep receipt integration payload-only. This package must not persist receipts or grant authority.
- Add `# SPDX-License-Identifier: GPL-3.0-only` to new Python files.
- Update documentation and `CHANGELOG.md` when behavior or public interfaces change.

## Pull requests

Keep pull requests focused and describe:

1. What changed.
2. Why it changed.
3. How it was tested.
4. Whether schemas, public interfaces, or compatibility are affected.

All CI checks must pass before merge.
