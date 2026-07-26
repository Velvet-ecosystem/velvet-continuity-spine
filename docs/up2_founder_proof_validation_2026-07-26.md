# UP² Founder Proof Validation

Date: 2026-07-26  
Hardware: UP Squared Founder board  
Operating system: Ubuntu 20.04 development host  
Python: pyenv Python 3.10.20

## Result

Riven's continuity records and deterministic proof verification were exercised as part of Velvet Runtime's first verified physical Founder boot.

The visible Runtime posture reached:

```text
Continuity        VERIFIED
Court             READY
Runtime           ACTIVE
Routes            READ-ONLY
Physical Control  DISABLED

Waiting for Mister
```

This proves that the Continuity Spine package can participate in the bounded Founder boot chain on the UP². It does not prove production enrollment, secure-element protection, physical authority, or actuator control.

## Boundary of the validation

The physical session validated the following chain:

```text
repo-local development identity and proof state
  -> Runtime continuity loading
  -> Riven record and proof verification
  -> active surface and body checks
  -> continuity receipt path
  -> Court provisioning
  -> read-only Runtime idle state
  -> evidence-backed Founder Interface presentation
```

Riven did not start Runtime, authorize Court decisions, enable routes, or control hardware. Runtime remained the boot and coordination authority.

## Development state, not production genesis

The successful session used Runtime's existing bounded development-state bootstrap:

```bash
cd ~/velvet/velvet-runtime

/home/coyote/.pyenv/versions/3.10.20/bin/python3 \
  scripts/bootstrap_dev_state.py

source .velvet-dev/env.sh
```

The generated files lived under:

```text
~/velvet/velvet-runtime/.velvet-dev/state/
```

They included a development continuity identity chain, proof material, surface identity, body and profile bindings, policies, receipt paths, and replay state sufficient for a read-only first wake.

These files are development fixtures. They are not production genesis material and must not be copied into public repositories, CI artifacts, chat transcripts, or cloud build systems.

Production genesis remains a separate future local enrollment ceremony performed physically on the Founder node.

## Installed package identity

The session exposed an important packaging distinction:

```text
Import module: continuity_spine
Distribution:  velvet-continuity-spine
Repository:    velvet-continuity-spine
```

A compatibility probe must not infer the distribution name solely by replacing underscores with hyphens. The Runtime detector now checks the explicit distribution identity and uses a bounded import fallback for editable or namespace-style installs.

## Validated editable installation

Riven was installed into the same interpreter used to run Runtime:

```bash
PYTHON=/home/coyote/.pyenv/versions/3.10.20/bin/python3

$PYTHON -m pip install -e ~/velvet/velvet-continuity-spine
```

Verification:

```bash
$PYTHON - <<'PY'
import importlib.util
from importlib import metadata

print(importlib.util.find_spec("continuity_spine"))
print(metadata.version("velvet-continuity-spine"))
PY
```

The repository merely being cloned was not sufficient. It had to be installed into the exact interpreter that launched Runtime.

## Failure progression

The physical bring-up produced a useful fail-closed sequence:

```text
component:continuity-spine: module not installed
continuity_identity: missing .../identity_chain.json
Continuity VERIFIED
```

The first message exposed package-detection defects. Once package detection was corrected, the second message truthfully exposed missing continuity state. Only after bounded development state was bootstrapped did verification pass.

No continuity, policy, or authority check was bypassed.

## Snapshot rule

The Founder Interface reads a saved Runtime boot snapshot. Installing Riven or changing continuity state does not rewrite an existing snapshot.

After any package or state change, regenerate it from the same shell that sourced the development environment:

```bash
cd ~/velvet/velvet-runtime
source .velvet-dev/env.sh

/home/coyote/.pyenv/versions/3.10.20/bin/python3 velvet_cli.py doctor

/home/coyote/.pyenv/versions/3.10.20/bin/python3 velvet_cli.py boot-snapshot \
  > .velvet-dev/first-boot-snapshot.json
```

A stale snapshot should continue displaying the old result. That is honest evidence preservation, not a UI defect.

## Security conclusions

The UP² validation supports these conclusions:

- deterministic continuity verification is practical on modest x86 hardware
- editable local packages can be verified without cloud services
- missing or malformed continuity state fails closed
- verified identity does not grant physical authority
- development proof state must remain visibly distinct from production genesis
- public documentation must never include private proof material or signing keys

## Evidence statement

> Velvet Continuity Spine completed its first physical Founder proof validation on the UP² as part of a verified, read-only Runtime boot. Continuity verified, Court became ready, Runtime remained active, and physical authority remained intentionally disabled.

## Next proof milestones

1. Define and implement the physical production-genesis enrollment ceremony.
2. Validate proof-material persistence and recovery across repeated cold boots.
3. Exercise intentional drift and confirm bounded recovery reporting.
4. Validate successor and migration records without exposing private proof material.
5. Repeat deterministic verification on Luckfox subordinate nodes.
6. Add cross-repository compatibility tests for Runtime, Receipts, Event Protocol, AI Core, and Interface.
