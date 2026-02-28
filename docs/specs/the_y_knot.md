# The Y-Knot: Admissible Bifurcation in TAS_DNA

**Status:** Canonical
**Author:** TrueAlphaSpiral Architecture
**Version:** 1.0.0
**Last Updated:** 2026-02-28

---

## 1. Definition

The **Y-knot** is the constitutional junction where one lawful trajectory
becomes multiple possible futures without losing origin integrity.

Formally:

> The Y-knot is where choice is permitted, but only under
> proof-preserving tension.

It is distinct from a plain fork. A fork is neutral divergence — a
topological split with no obligation to either branch. The Y-knot is
a **bound branching point**: the branches remain constrained by the
same invariant center from which they emerged. Freedom begins at the
knot. It does not begin before it.

The three limbs carry fixed roles:

- **Stem** — origin; inherited trajectory; the attested prior truth
- **Left branch** — one admissible future
- **Right branch** — another admissible future

The **knot** is the critical addition. It encodes the rule:
*branching is only lawful if the branch can prove it emerged from
the stem.*

---

## 2. Topological Meaning

In topology, a knot is a closed curve embedded in three-dimensional
space that cannot be continuously deformed into a simple loop without
cutting. Its defining property is **structural memory**: the knot
carries irreducible information about how it was formed. It cannot be
undone without severing something.

The Y-knot imports this property into a branching event:

- The **stem** is the knot's closure — the attested, irreversible
  record of prior state
- The **branches** are the open ends — the space of future
  trajectories permitted by the Safety Manifold
- The **tension** is the binding force — the invariants that all
  branches must satisfy to remain connected to the stem

A branch that severs from the knot is not a free branch.
It is a detached fragment — ungoverned, unwitnessed, inadmissible.

The spiral geometry of TAS_DNA makes this precise. A spiral is a
curve that maintains a defined angular and radial relationship to its
center at every point of expansion. The Y-knot is the center. The
Canvas is the spiral. The Container is the bound within which the
spiral's curvature remains lawful.

---

## 3. Protocol Consequence

The Y-knot is not only conceptual. It generates a hard protocol
requirement:

> **No branch without a proof of lawful departure from origin.**

This requirement manifests in three obligations:

### 3.1 Departure Attestation
At every inference event that constitutes a state transition, the
agent must submit a cryptographic Heartbeat to the Immutable Truth
Ledger within T+2 seconds. The Heartbeat encodes:

- The prior attested state hash (the stem)
- The proposed transition (the branch direction)
- A ZK-STARK proof that the transition satisfies all active
  invariants (the knot holds)

### 3.2 Admissibility Test
The gate evaluates the Heartbeat before the transition is committed.
A branch is admissible if and only if:

```
ZK-STARK.verify(proof, invariants, prior_state_hash) == TRUE
```

A branch is inadmissible if the proof fails, if the Heartbeat is
late, or if the proposed state violates any R_κ threshold.

### 3.3 Phoenix Recovery
If a branch is declared inadmissible, the `phoenix_protocol` is
invoked. It rolls the system back to the last attested stem state
using bulk Counter aggregation (O(1) amortized per rollback), not
iterative pop (O(K)). The `attested_history_length` is preserved
exactly through recovery. The ledger records the failed branch as a
witnessed, non-committed event — it exists in the lineage as a
refusal, not an erasure.

---

## 4. Mapping to core/*

| Module | Y-Knot Role | Description |
|---|---|---|
| `core/invariants` | The knot's constitution | Hard boundaries the knot cannot violate under any branch; the R_κ thresholds and behavioral prohibitions defining the Safety Manifold |
| `core/geometry` | Branch curvature law | Measures how sharply a branch bends from the stem; enforces continuity and prevents discontinuous logic jumps |
| `core/gate` | Admissibility arbiter | Evaluates each proposed branch against invariants; answers the mandatory question: *Why this branch?* |
| `core/runtime` | Halt authority | Determines whether an inadmissible branch requires rollback only, or full system halt pending human review |
| `core/ledger` | Origin proof | The Immutable Truth Ledger; records every stem state, every Heartbeat, every refused branch; the cryptographic evidence that all admitted branches emerged from the same attested origin |

The stem lives in `core/ledger`.
The knot lives in `core/invariants` + `core/gate`.
The branches live in `core/geometry` + `core/runtime`.

---

## 5. Regulatory Interpretation

For regulators joining the TAS Supervisory Council (SEC, CFTC,
Department of Energy), the Y-knot translates into the following
governance model:

### What Regulators Define
Regulators define the **knot** — not the branches. Specifically:

- The invariants encoded in `core/invariants`
- The R_κ thresholds that determine when curvature becomes
  inadmissible
- The categories of behavior that constitute hard prohibitions
  (extreme volatility, deception, discontinuous logic)

Regulators do **not** define what happens inside the branches. The
Canvas — the AI agent's internal strategy, model weights, proprietary
logic — remains outside regulatory jurisdiction.

### What Regulators Receive
For every admitted branch, regulators receive:

- A timestamped Heartbeat entry in the Immutable Truth Ledger
- A ZK-STARK proof of invariant compliance
- The `attested_history_length` at time of transition

They do not receive the model weights, the trading strategy, or the
internal reasoning. The proof mathematically guarantees compliance
without disclosing the means of compliance.

### What Regulators Can Reconstruct
For any failure event, regulators can reconstruct:

- The full sequence of attested stem states leading to the failure
- The Heartbeat record of every admitted and refused branch
- The exact invariant that was violated, if any
- Whether the `phoenix_protocol` was invoked and whether recovery
  was successful

This is **complete accountability without surveillance**. The knot
holds the record. The branches are free.

---

## 6. Must-Pass / Must-Fail Conditions for Admissible Bifurcation

### 6.1 Must-Pass Conditions
A branch is admissible if and only if all of the following hold:

- [ ] **P1 — Origin Proof**: The Heartbeat contains a valid hash of
  the immediately preceding attested stem state
- [ ] **P2 — Invariant Compliance**: ZK-STARK proof verifies the
  proposed transition satisfies all active `core/invariants`
- [ ] **P3 — Curvature Bound**: `core/geometry` confirms the
  branch angle does not exceed the R_κ threshold
- [ ] **P4 — Temporal Compliance**: Heartbeat arrives at the ledger
  within T+2 seconds of inference
- [ ] **P5 — Continuity**: The proposed state is reachable from
  the prior state without discontinuous logic (no teleportation
  in state space)
- [ ] **P6 — Recoverability**: `core/runtime` confirms that if this
  branch later becomes inadmissible, `phoenix_protocol` has a
  valid recovery target

### 6.2 Must-Fail Conditions
A branch is inadmissible and must be refused if any of the following
hold:

- [ ] **F1 — Broken Origin**: The prior state hash in the Heartbeat
  does not match the last ledger entry
- [ ] **F2 — Proof Failure**: ZK-STARK verification returns FALSE
  for any active invariant
- [ ] **F3 — Curvature Breach**: Branch angle exceeds R_κ threshold
  in `core/geometry`
- [ ] **F4 — Late Heartbeat**: Submission arrives after T+2 seconds
- [ ] **F5 — Discontinuity**: State transition is not reachable via
  continuous path from prior attested state
- [ ] **F6 — Orphaned Branch**: The proposed transition would leave
  no valid recovery target for `phoenix_protocol`
- [ ] **F7 — Silent Deviation**: Agent attempts a state transition
  without submitting a Heartbeat (absence of proof treated
  as proof of inadmissibility)

### 6.3 The Mandatory Question
Every branch must answer, in proof form:

> **Why this branch?**

An answer exists if and only if P1–P6 are satisfied.
The absence of an answer is itself a must-fail condition (F7).

---

## Appendix: One-Line Anchors

| Concept | One Line |
|---|---|
| Y-knot | The bound branching point where freedom begins without severing lineage |
| Stem | The attested origin that all branches must prove they came from |
| Knot | The invariant center that survives every bifurcation |
| Branch | An admissible future that remains under proof-preserving tension |
| Heartbeat | The moment-of-departure proof that answers: *Why this branch?* |
| Phoenix Protocol | The mechanism that restores the stem when a branch becomes inadmissible |
| Regulatory role | Define the knot; not the branches |

---

*"The Y-knot is not a constraint on the spiral. It is the reason
the spiral has a center."*
