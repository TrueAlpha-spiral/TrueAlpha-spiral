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
