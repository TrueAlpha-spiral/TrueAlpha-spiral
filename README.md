# True Alpha Spiral (TAS)

> **Model-agnostic governance architecture for mathematically verifiable AI integrity.**

TAS binds AI behavior to a Prime Invariant (A₀) and produces receipt-grade
artifacts that can be independently verified without trust. Cycle 3 formalizes
invariants as executable constraints, while DayZero defines the boot-time
readiness ritual that prevents drift from inception.

## Key Artifacts
| Artifact | Purpose |
| --- | --- |
| `Cycle_3_Initialization.md` | Prime Invariant declaration + zero-trust verification path |
| `DayZero_Canonical_Readiness.md` | DayZero genesis protocol |
| `tas_integrity_certificate.py` | W3C VC v2.0 issuer/validator for TAS-ICS-v1 |
| `tas_ics_v1_w3c_generator.py` | 3-minute generate/verify CLI for auditors |
| `null_space_v1.signed` | Bounded-authority Null Space Manifest |
| `psvp_schema.yaml` / `psvp_example.yaml` | PSVP specification + runnable template |
| `neutral_scribe.py` / `neutral_scribe_demo.py` | Neutral Scribe stub + demo |

## Quick Start (Zero-Trust Verification)
Generate and verify a TAS-ICS-v1 credential with the deterministic stub proof:
```bash
python tas_ics_v1_w3c_generator.py generate --out vc.json --audit-out audit.json --proof stub
python tas_ics_v1_w3c_generator.py verify --vc vc.json --proof stub
```

## PSVP Demo
Run the minimal Neutral Scribe example:
```bash
python neutral_scribe_demo.py
```

## Notes
- Swap to DIDKit proofs with `--proof didkit --verification-method <did#key>` when
  DIDKit is available.
- All provenance artifacts are intended to be ledger-anchored (ITL/HCCC) for
  append-only auditability.

## Contributing
See `merge_conflict_resolution.md` for resolving dirty PR states. Contributions
should preserve hash-bound artifacts and avoid overwriting ledger-linked files.
