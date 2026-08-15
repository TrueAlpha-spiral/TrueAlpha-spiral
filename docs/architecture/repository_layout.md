# First Sip repository architecture

This document is the navigation contract for the consolidated TAS/SDF
repository. It describes owned module locations without claiming that planned
controls are already implemented.

| Layer | Canonical location | Responsibility |
|---|---|---|
| Doctrine and specifications | `README.md`, `docs/specs/` | Axioms, terminology, schemas, and threat models |
| Architecture | `docs/architecture/` | Trust boundaries, integration topology, and lineage contracts |
| Verification | `core/verification/` | Deterministic verification and authenticated admission |
| Authority | `core/authority/` | Authority snapshots and least-authority capabilities |
| Evidence | `core/wakechain.py` | Append-only admission and refusal history |
| Recovery | `core/recovery/` | Evidence-preserving Phoenix recovery |
| Sensing | `core/sensing/` | Drift, stability, and violation detection |
| Semantics | `core/semantics/` | Immutable context and definition identities |
| Rust verification | `tas-merkle/` | Merkle proofs, checkpoints, and rollback primitives |
| External integration | `tas_openai_bridge/`, `sdf_tas_interface.py` | Untrusted proposal adapters and civic reference interface |
| Conformance | `conformance-tests/`, `tests/` | Portable vectors, unit tests, and adversarial checks |

## Import policy

New Python integrations should import control-plane types through the `core`
package. Root-level modules remain compatibility entry points until a separately
versioned migration removes them. In particular, authenticated admission is
available from `core.verification.admission_gate`, while the policy-oriented
nine-check reference monitor remains in `core.verification.universal_verifier`.

## First Sip implemented boundary

The release includes:

- canonical candidate and context verification;
- cryptographic authority and receipt verification;
- registered, scoped, expiring, and revocable capability tokens;
- append-only admission and refusal evidence;
- deterministic structural-density assessment;
- ordered, evidence-preserving recovery records; and
- Rust Merkle proof and rollback primitives.

Hardware-backed key custody, a durable distributed replay store, transactional
coupling of admission to application state, and independent differential
implementations remain deployment work. See the ASSP integration blueprint for
their IOC exit criteria.
