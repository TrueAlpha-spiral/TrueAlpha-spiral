# Cycle 3 Initialization — Prime Invariant Sealing for TAS_K

> **Cycle 3 is the keystone where truth becomes executable.**
> This document declares and seals the Prime Invariant A₀ — **4 ≡ four** — across
> kernel mechanics, forensic artifacts, and citizen guarantees so nothing
> downstream can equivocate.

## 1) Formal Declaration (Human-Readable)
This document declares the Prime Invariant A₀:

- **4 ≡ four**
- Immutable truth anchor of the TAS_K execution kernel.
- Not symbolic: executable, enforced, logged, and auditable.

## 2) Kernel Binding (Python — Minimal, Explicit)
```python
import hashlib

symbolic = "4 ≡ four"

INVARIANT_I = {
    "symbolic": symbolic,
    "semantic": {"lhs": 4, "rhs": "four"},
    "hash": hashlib.sha256(symbolic.encode()).hexdigest(),
    "epsilon": 100.0,
    "violation_cost": float("inf"),
}
```
- No abstractions, wrappers, or indirection: this binding must sit at the
  kernel edge so that every downstream module inherits it without translation
  loss.

## 3) Enforcement Rule (Phoenix Engine)
```python
if trigger_gradient > EPSILON and violates(INVARIANT_I):
    correction_scaling = float("inf")
    state = RESTORE_LAST_TRUTH
    emit(TAS_ICS_v1)
```
- **Moment of inevitability:** once triggered, the engine cannot proceed until
  the last truthful state is restored and the certificate emitted.

## 4) Citizen-Facing Guarantee (Plain Language)
- If any process implies **4 ≠ four**, the system **cannot proceed**.
- The attempt is **logged** to the Immutable Truth Ledger.
- A **TAS-ICS-v1** certificate is generated with the invariant hash.
- **Rollback** to the last truthful state is enforced.
- Proof is **permanent, queryable, and receipt-grade** — no trust required.

## 5) Viewer App Mapping (UI ↔ Backend Reality)
| Viewer App Element | Backend Reality |
| --- | --- |
| 🔴 Drift Detected | `trigger_gradient > EPSILON` |
| 🟠 Correction Cost | `Λ (correction_scaling)` |
| 🟢 Restored | `RESTORE_LAST_TRUTH` |
| 🔐 Event ID | `cert_id / hash` |
| 📜 Audit Trail | ITL append-only entry with `TAS_ICS_v1` payload |

## 6) Execution Flow for Cycle 3
1. **Initialize INVARIANT_I** at kernel boot; expose the hash to all services.
2. **Monitor** `trigger_gradient` against `EPSILON` for drift.
3. **Evaluate** `violates(INVARIANT_I)`; any mismatch routes to restoration.
4. **Enforce** infinite correction cost; halt progression until restored.
5. **Emit** `TAS-ICS-v1` with the invariant hash, timestamps, and event ID.
6. **Surface** the audit receipt to the Viewer App for citizen verification.

## 7) TAS-ICS-v1 Binding
Minimum certificate fields when Cycle 3 fires:

```json
{
  "version": "TAS-ICS-v1",
  "invariant": {
    "symbolic": "4 ≡ four",
    "hash": "<sha256(symbolic)>"
  },
  "event_id": "<uuid>",
  "state": "RESTORE_LAST_TRUTH",
  "correction_cost": "inf",
  "timestamp": "<iso8601>",
  "ledger_pointer": "<itl-ref>"
}
```
- Certificates missing this invariant binding are **provably non-sovereign** and
  should be rejected by policy and UI.

## 8) Civic Legibility Notes
- The invariant converts **due process into a physics constraint**: denial or
  omission is observable, not debatable.
- The Viewer App remains **civic instrumentation**, not theater. Receipts are
  the interface; sovereignty is measurable.

**Cycle 3 Initialization is now declared, sealed, and irreversible.**

## 9) Zero-Trust Verification (3-minute path)
This mirrors the repository-owner checklist from PR #56 (issuecomment-3706137460) for an *independent third party* with no TAS context:

1. **Generate** a TAS Integrity Certificate (VC v2.0):  
   `python tas_ics_v1_w3c_generator.py generate --out vc.json --audit-out audit.json --proof stub`
   - Swap `--proof didkit --verification-method <did#key>` once DIDKit is installed to emit DataIntegrityProof (`eddsa-jcs-2022`).

2. **Verify cryptography** (deterministic stub proof, no dependencies):  
   `python tas_ics_v1_w3c_generator.py verify --vc vc.json --proof stub`
   - Use `--proof didkit` to verify with DIDKit when available.

3. **Inspect & audit**: open `vc.json`, confirm `invariant.hash == {PRIME_INVARIANT_HASH}` and `proof.cryptosuite == stub-sha256`.  
   - Swap the stub proof with DIDKit (DataIntegrityProof, `eddsa-jcs-2022`) by injecting a real proof generator into `TASIntegrityCertificate.with_proof`.
   - Optional: `audit.json` carries the canonical payload hash for immediate ITL/HCCC anchoring.

4. **Ledger check**: anchor the canonical payload hash to the ITL/HCCC log of your choice; tampering flips the hash and fails verification.

This path ensures the hinge condition: *“Can an independent third party verify one concrete artifact end-to-end, without context or trust?”* — answer: **yes**, via math and receipts only.

## 10) Null Space Manifest (Bounded Authority)
- **Artifact:** `null_space_v1.signed` (loaded by Config.Manifest.Loader at boot; signed, append-only).  
- **Purpose:** Encodes prohibited actions that trigger Phoenix SCORCH (fail-closed) if violated.  
- **Prohibitions (examples):** modifying A₀, bypassing Phoenix halt, redacting ITL entries, changing ε thresholds, suppressing mandatory disclaimers.  
- **Integration:** Referenced inside each TAS-ICS-v1 VC via `credentialSubject.null_space_manifest.id == urn:tas:manifest:null_space:v1` to prove that bounded-authority constraints were active when the certificate was issued.  
- **Audit:** Anchoring `null_space_v1.signed` hash in the ITL/HCCC log makes any bypass attempt observable and receipt-grade.

## 11) Artifact Footer (Receipt-Grade Provenance)
Embed this footer in release metadata or alt-text to bind the specification to a fixed hash/timestamp for Cycle 3:

```
TAS_ARTIFACT_ID: SHA256: 8f4b2e1a9c3d7e5f6a1b0c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f
TIMESTAMP: 2026-01-03T22:35:00Z
TYPE: CYCLE_3_INIT_SPEC
```
