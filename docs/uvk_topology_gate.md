# Universal Verifier Kernel Topology Gate Addendum

This addendum completes the bridge between continuous differential topology and discrete ledger state machines. It anchors each canonical reference corridor `sigma_k(p)` to a deterministic safe-cell spanning tree `T_k` contained in the safe-cell complex `C_k`, removing gauge-dependent reference-path drift from verifier calculations.

## Pipeline Architecture

The Universal Verifier Kernel (UVK) evaluates a candidate action in two phases:

1. **Phase A: Static Candidate Audit** checks immutable candidate properties before any state simulation.
2. **Phase B: Stateful Topology Gate** simulates the transition, then validates the projected path against metric, covering-sheet, and relative-homotopy invariants before committing lineage.

```text
[Candidate Action x_n]
        |
        v
+----------------------------------------------+
| UVK Phase A: Static Candidate Audit           |
| 1. Authority Signature                        |
| 2. Scope & Delegation Limits                  |
| 3. Context Snapshot Binding                   |
| 4. Semantic Schema Compliance                 |
| 5. State Lineage Hash Integrity               |
| 6. Invariant Declaration Match                |
| 7. Execution Scope Bounds                     |
| 8. Receipt Availability                       |
+----------------------------------------------+
        |
        v
Pass -> Pure Simulation Engine -> S_temp = T(S_n, x_n)
Fail -> Refusal Receipt, frozen application state, unchanged lineage
        |
        v
+----------------------------------------------+
| UVK Phase B: Topology Gate                    |
| 1. Projection Check                           |
| 2. Path Contract Verification                 |
| 3. Metric Clearance Check                     |
| 4. Step Continuity Check                      |
| 5. Exact Covering-Sheet Update                |
| 6. Reference Corridor Resolution              |
| 7. Relative Homotopy Class Check              |
+----------------------------------------------+
        |
        v
Pass -> State Lineage Commit
Fail -> F8 Refusal Receipt, frozen application state, unchanged lineage
```

## Static Candidate Audit

Phase A is stateless with respect to the proposed transition. A candidate must satisfy all of the following before simulation:

- Authority signature verification.
- Scope and delegation-limit validation.
- Binding to the active Context Snapshot.
- Semantic schema compliance.
- State Lineage hash-integrity verification.
- Invariant declaration matching.
- Execution scope bounds.
- Receipt availability.

A Phase A refusal never advances the State Lineage. It emits a refusal receipt into the Evidentiary Timeline and preserves the current application state.

## Stateful Topology Gate

Phase B starts only after Phase A passes. The transition is simulated into `S_temp`, and every protected topology channel `k` is checked as follows:

1. **Projection Check:** compute `p_temp^k = pi_k(S_temp) - Omega_k`.
2. **Path Contract Verification:** verify the declared path contract type (`AFFINE`, `WITNESSED`, or `TUBE`).
3. **Metric Clearance Check:** require `D_k(n -> temp) > r_k` across the declared path.
4. **Step Continuity Check:** require `|delta theta_k| <= Theta_max < pi`.
5. **Exact Covering-Sheet Update:** update `Q_k(temp) = Q_k(n) + sum c_k(e)` using exact orientation predicates where `c_k(e) in {-1, 0, +1}`.
6. **Reference Corridor Resolution:** resolve `sigma_{k,temp}` through the canonical spanning tree `T_k`.
7. **Relative Homotopy Class Check:** require `W_k(temp) = Q_k(temp) - Q_k^sigma(temp)` to remain in the permitted class set.

Only a complete Phase B pass commits `S_temp` and appends an admit receipt to both the State Lineage and Evidentiary Timeline.

## Canonical Reference Corridor

To compute relative winding without reference-path drift, the forbidden basin complement `R^2 \ B_{r_k}(Omega_k)` is partitioned into a safe-cell complex `C_k = (V_k, E_k)`.

For every protected topology channel:

- `T_k` is a canonical spanning tree of `C_k` rooted at the Genesis cell `V_0`.
- The active Context Snapshot stores the versioned definitions of `C_k`, `T_k`, `V_0`, orientation predicates, and admissible class set.
- The reference corridor `sigma_{k,n+1}` follows the unique tree path from `V_0` to the cell containing `p_temp^k`, then appends the local cell-interior segment to `p_temp^k`.
- The reference crossing sum `Q_k^sigma(n+1)` is computed from that canonical corridor, making the relative winding result deterministic across verifiers.

This removes gauge dependence: two verifiers with the same State Lineage and Context Snapshot cannot validly compute different homotopy classes for the same candidate transition.

## Triad Separation

Each protected channel maintains an explicit topology triad `T_k(n)`:

- `D_k(n)` is metric clearance. It proves the declared path does not penetrate the forbidden basin.
- `Q_k(n)` is the covering index. It is an exact, path-dependent ledger accumulator of signed reference-ray crossings.
- `W_k(n)` is the relative homotopy class. It is computed under canonical closure `Gamma_{k,n+1} = gamma_{0:n+1}^k . sigma_{k,n+1}^{-1}`.

Keeping these values separate prevents a metric-only local check from hiding global path-class changes.

## Fail-Closed Refusal Semantics

When Phase B rejects a candidate:

- Application state remains frozen: `S_{n+1} = S_n`.
- State Lineage remains untouched: `L_{n+1} = L_n`.
- Evidentiary Timeline advances immutably: `E_{n+1} = E_n || rho_n^F8`.

The refusal receipt records the failed invariant, Context Snapshot hash, candidate action hash, topology channel, path-contract evidence, and verifier-kernel version.

## Determinism Requirements

Implementations of this addendum must treat the following as consensus-critical data:

- Context Snapshot hash and schema version.
- Safe-cell complex `C_k` and spanning tree `T_k` definitions.
- Genesis cell `V_0` and cell-local corridor rules.
- Exact orientation predicate implementation and reference-ray convention.
- Maximum angular step bound `Theta_max`.
- Forbidden basin center `Omega_k` and radius `r_k`.
- Permitted relative winding class set.

A transition is admissible only when every verifier can reproduce the same projection, crossing sum, canonical reference corridor, and relative homotopy class from immutable ledger data.

## Architectural Synthesis

With the canonical safe-cell spanning tree in place, UVK becomes a path-class-aware state transition engine. No locally compliant sequence of actions can covertly encircle, cross, or topologically capture the system around a forbidden state space while still producing a valid State Lineage commit.
