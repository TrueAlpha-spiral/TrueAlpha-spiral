# Sovereign Data Foundation Public Campaign: Proof Before Consequence

## Executive Summary & Core Demand
The Sovereign Data Foundation (SDF) centers its public campaign on one non-negotiable demand: **Proof before consequence.**

The campaign establishes a clear distinction between:
1. **Proposal Generation:** A machine generating an unconstrained candidate proposal or statistical prediction.
2. **Consequential Action:** A system possessing verified, cryptographically authenticated permission to execute an operational mutation or state transition.

In Sovereign Intelligence—governed by the TrueAlphaSpiral (TAS) architecture—no protected action can be executed without first proving it possesses structural authority, valid scope, and unbroken lineage.

---

## Three Core Architectural Adjustments
To ensure maximum public defensibility and mathematical rigour, the campaign incorporates three foundational principles:

1. **A Receipt Proves Specific Operational Invariants:**
   A cryptographic receipt is not a generic claim of righteousness or moral justice. It strictly proves four recorded elements:
   - Recorded inputs
   - Authenticated authorization (`AuthoritySnapshot`)
   - Pre-condition and invariant checks (`Deterministic Verifier` $V(S, X, Y)$)
   - Recorded outcomes and state mutations (or refusal state preservation)

2. **Probabilistic Generation Remains Enclosed:**
   Probabilistic models (LLMs, neural network candidate generators) can remain inside the architecture as proposal engines. The fundamental shift is the enforcement of a deterministic boundary (`CanonicalVerticalSlice` & `SovereignRuntime`) around all consequences. Every protected action must pass through this boundary before execution.

3. **Public Control Demands Practical Rights & Access:**
   Public trust cannot rely on black-box assurances. Sovereign Intelligence provides actionable mechanisms:
   - Independent verification ($V = 1$ vs $V = 0$)
   - Meaningful challenge protocols
   - Auditable correction loops (remediation adds evidence without rewriting historical events)

---

## Public Messaging Framework

| Public Message | Concrete Meaning | Demonstration Mechanism |
|---|---|---|
| **Your permission has boundaries.** | Access does not authorize every use. Permitted scope is strictly bounded by credential epoch and jurisdiction. | Refuse an action outside its authorized scope (`SCOPE_NOT_PERMITTED`). |
| **Every consequential action needs a receipt.** | Identify the authority, applicable rules, and recorded result in an unalterable log. | Let an independent verifier check the cryptographic signature and hash chain. |
| **An unverified request stays stopped.** | Failed or missing proof deterministically blocks protected action (Refusal Integrity). | Show unchanged operational state alongside the recorded refusal receipt (`Delta O = 0`). |
| **Corrections preserve the record.** | Remediation adds new evidence to the lineage without history fabrication or rewriting past events. | Trace a discrepancy through an authorized correction and verified outcome on the WakeChain. |

---

## Centerpiece: Reproducible Demonstration Blueprint

For the launch campaign, SDF delivers **one reproducible demonstration** built directly on the TAS `CanonicalVerticalSlice` and `WakeChain` engine:

1. **Test Case 1: Authorized Request Succeeds**
   - **Input:** Valid `AuthoritySnapshot` with scope `["codex.run"]`.
   - **Action:** Execute `codex.run`.
   - **Result:** $V = 1$ (Admitted). Lineage extends on the `WakeChain`; execution receipt recorded; operational state transitions cleanly.

2. **Test Case 2: Missing/Exceeded Authority Refused**
   - **Input:** Same `AuthoritySnapshot` with scope `["codex.run"]`.
   - **Action:** Attempt unauthorized operation `codex.delete`.
   - **Result:** $V = 0$ (Hard Stop / Refused). Operational state remains strictly unchanged ($\Delta O = 0$). Refusal receipt recorded with permanent failure code (`SCOPE_NOT_PERMITTED`).

3. **Test Case 3: Altered Receipt Fails Verification**
   - **Input:** Tampered/corrupted receipt hash or altered payload.
   - **Action:** Verification sweep by independent verifier.
   - **Result:** Verification failure ($V = 0$). System detects hash mismatch and triggers Phoenix Recovery checkpoint without advancing state.

---

## Architectural Commitments & Boundary Limits
The campaign describes **Sovereign Intelligence** as the Foundation's explicit architectural commitment:

- **Demonstrated Properties:**
  - Deterministic gating ($V(S,X,Y)$)
  - Refusal Conservation Law ($\Delta O = 0$ on failure)
  - Stable refusal receipt IDs (`sha256:` content-addressed)
  - Hash-anchored evidence timelines (`WakeChain`)

- **Planned / Future Roadmap:**
  - Cross-jurisdictional multi-party consensus protocols
  - Automated zero-knowledge state proofs for zero-trust federated nodes

---

## The Three Public Audit Questions
Every member of the public should leave the campaign equipped with three fundamental questions to inspect any automated system:

1. **Who authorized this?** (Where is the `AuthoritySnapshot` and credential scope?)
2. **What actually happened?** (Where is the verifiable execution or refusal receipt on the ledger?)
3. **How can I challenge it?** (How do I submit a contestation or initiate a verified correction trail?)
