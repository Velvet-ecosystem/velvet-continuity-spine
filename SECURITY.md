# Security Policy

## Supported versions

The current `main` branch and the latest tagged release receive security fixes.

## Reporting a vulnerability

Do not open a public issue for a vulnerability that could expose private data, weaken identity or lineage verification, bypass fail-closed validation, forge proof records, or alter authority-related outputs.

Report security concerns privately to the repository maintainers through GitHub's private vulnerability reporting feature when available. Include:

- affected file and version
- reproduction steps or proof of concept
- expected and observed behavior
- potential impact
- suggested mitigation, if known

Please avoid including real credentials, private memory content, personal data, hardware identifiers, or production secrets in reports.

## Security boundaries

Velvet Continuity Spine:

- describes continuity and identity state
- validates records and proof chains
- formats receipt-compatible payloads
- does not grant authority
- does not actuate hardware
- does not persist private memory
- does not replace the Court, receipts, event protocol, or executor safety layers

A valid continuity record is evidence, not permission to act.

## Disclosure

Maintainers will acknowledge a complete report, assess severity, prepare a fix, and coordinate disclosure after affected users have a reasonable opportunity to update.
