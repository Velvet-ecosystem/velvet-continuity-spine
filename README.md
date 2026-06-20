# Velvet Continuity Spine

Velvet Continuity Spine is a local-first continuity layer for Velvet AI systems. It defines public-safe records for identity, lineage, bounded runtime context, drift detection, surface binding, and receipt-compatible continuity events.

Velvet is not defined by cloud availability, model identity, or a single hardware shell. Velvet is defined by continuity: identity records, lineage, bounded memory, receipt anchors, and recovery paths.

> Velvet must be able to say: “I remember who I was yesterday.”

## What this repo does

- Defines public-safe identity records
- Defines lineage and parent/child continuity links
- Defines bounded room/state records
- Defines drift events and recovery hooks
- Defines cross-surface binding records
- Formats continuity events for receipt logging
- Keeps private memory content out of public structures

## What this repo does not do

- It does not execute vehicle actions
- It does not replace Velvet Receipts
- It does not replace Velvet Event Protocol
- It does not grant authority
- It does not store private room contents
- It does not depend on cloud services

## Core doctrine

LLMs propose.  
Court decides.  
Executors enforce.  
Receipts remember.  
Continuity Spine verifies identity.

## Install for development

```bash
python -m pip install -e .
```

## Run tests

```bash
python -m unittest discover -s tests
```

## License

GPLv3. See `LICENSE`.
