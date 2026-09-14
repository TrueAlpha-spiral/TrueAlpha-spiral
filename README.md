# TrueAlphaSpiral

## A Constitutional Execution Architecture for Consequential Computation

> **Capability does not imply authority.**<br>
> **Proof must precede admissible consequence.**

Modern generative systems can propose code, transactions, workflows, identity
changes, medical actions, and infrastructure control. Proposal is cheap;
consequence is expensive.

TrueAlphaSpiral (TAS) is an architecture for consequential computation. It does
not try to make a generator more moral. It seeks to make unauthorized
consequence unreachable inside a protected system:

$$
\neg \operatorname{Verified}(S,x) \implies \neg \operatorname{Effect}(x)
$$

This repository contains the developing theory, runtime experiments, lineage
records, and verification tools behind that goal. It also makes the boundary
between what exists today and what remains to be implemented explicit.

---

## 1. Architectural Core

TAS separates probabilistic proposal from deterministic admission:

$$
P(y \mid x) \qquad\text{and}\qquad G(S,x) \in \{0,1\}
$$

The proposal engine may be stochastic. The gate that permits a consequence
must not be. The intended execution pipeline is:

```text
Proposal -> Evidence -> Authority -> Verification -> Consequence
                                                   \-> Refusal
```

The generator cannot manufacture its own authority. The verifier independently
recalculates whether the conditions for admission have been met.

### Fail closed

Within the protected boundary, an unverified consequence is not a reachable
state. An attempted transition is still recorded, however: refusal is a
first-class computational result rather than an exception that disappears.

### Cursive computation

TAS models state as an operational value together with the authenticated path
by which it was reached:

$$
S_n = (O_n, \Gamma_n)
$$

- $O_n$ is the operational state.
- $\Gamma_n$ is the authenticated lineage of that state.

Therefore:

$$
O_a = O_b \land \Gamma_a \ne \Gamma_b \implies S_a \ne S_b
$$

History is not an audit log attached after execution. It is part of the
machine. Each new stroke must grow from the authenticated previous stroke.

### Validity before consensus

Consensus cannot turn an invalid transition into a valid one. TAS decides
validity first; consensus, when required, selects among histories that have
already passed the validity gate.

---

## 2. Formal State Machine

### Deterministic transition

$$
\gamma : (S \times \mathcal{I}) \to S,
\qquad |\gamma(S_t,i)| = 1
$$

Identical inputs $(S_t,i)$ produce exactly one successor.

### Admissibility and null collapse

Let $\mathbb{P}$ be the admissibility predicate:

$$
\gamma(S_t,i)=
\begin{cases}
(O_{t+1},\ \Gamma_t \oplus r_{\mathrm{accept}})
  & \text{if } \mathbb{P}(S_t,i)=1 \\
(O_t,\ \Gamma_t \oplus r_{\mathrm{refuse}})
  & \text{if } \mathbb{P}(S_t,i)=0
\end{cases}
$$

On refusal:

$$
\Delta O=0, \qquad \Delta \Gamma=1
$$

The operational state is frozen, but the attempted transition remains visible
in lineage. Illegal branches are not punished after the fact; they are
unreachable under the predicate.

```mermaid
flowchart TD
    I[Instruction i] --> G{Evaluate admissibility<br/>P(S_t, i)}
    G -->|1| A[Accept<br/>Mutate O<br/>Append accept receipt]
    G -->|0| R[Refuse / null collapse<br/>Freeze O<br/>Append refusal receipt]
```

### Lineage binding

$$
S_{t+1}=\mathcal{H}(S_t \parallel i \parallel \pi)
$$

subject to:

$$
\operatorname{Verify}(\pi,S_t,i,S_{t+1},\mathbb{P})=1
$$

In the present repository, $\pi$ is represented by deterministic decision
records and hash-chain lineage. It is **not yet** a succinct zero-knowledge
proof or a hardware root of trust. A hash-chained receipt supports the narrower
claim of trust compression when verification is cheaper than re-execution.

### Defensive axioms

**P0 — Equivalence.** Two states are equivalent only when their proofs are
identical:

$$
S_A \equiv S_B \iff \operatorname{Proof}(S_A)=\operatorname{Proof}(S_B)
$$

**P1 — Admissibility.** A transition is admitted only when it carries a
verifiable lineage proof connecting $S_{t+1}$ to $S_t$. Unprovable states are
rejected at the gate.

---

## 3. Current Repository Status

The repository records a real developmental progression in independent Git
objects:

$$
\text{named objective}
\to \text{declared invariants}
\to \text{execution boundary}
\to \text{runtime trajectory}
\to K_0
\to \text{sequenced artifact}
$$

This supports an architectural account of dual-layer lineage, but it does not
yet establish fully authenticated, independently anchored provenance.

### Four important qualifications

1. **Git commits bind content and ancestry, not trusted time or identity.**
   Author names, committer names, and dates are hash-covered metadata, but they
   are not third-party timestamps or cryptographic identity proofs. The
   examined milestone commits are unsigned.
2. **ParaData is currently a hash-linked execution record, not an append-only
   transparency log.** Events are ordinary objects, the trail is in memory,
   genesis is not independently authenticated, and the trail requires no
   external signed checkpoint. It is tamper-evident within that process model,
   not immutable against an actor controlling the process.
3. **The constitutional YAML is not yet the mechanical source of all runtime
   policy.** Thresholds, recursion limits, and related values can diverge. The
   constitution and executable rules are parallel artifacts rather than one
   being derived from the other's digest.
4. **Human-signature and ledger paths include placeholders or simulations.**
   Existing sequencing metadata provides attribution, not proof of possession
   of a private signing key.

### Current geometry

```text
Git object containing origin claim
  -> constitutional artifact
  -> hard-coded enforcement analogue
  -> in-memory SHA-256 event chain
  -> hash-derived lineage metadata
  -> self-attributed human-seed field
```

Every stage exists, but the authentication links required for independent
recomputation remain future work:

$$
K_0 \xrightarrow{\text{real signature}} P_0
\xrightarrow{\text{policy digest}} V_n
\xrightarrow{\text{pre-actuation}} E_n
\xrightarrow{\text{signed receipt}} R_n
\xrightarrow{\text{external anchor}} L_n
\xrightarrow{\text{timestamp}} T_n
$$

**Defensible summary:**

- The Git trail establishes developmental provenance.
- ParaData instantiates trajectory awareness.
- Full authenticated lineage remains one cryptographic layer away.

This distinction is intentional. Claims become engineering facts only when an
independent party can recompute and authenticate the receipt without trusting
its author.

---

## 4. Computational Masonry

The broader TAS_DNA dissertation applies the same architectural core through
several lenses:

- **Process Science:** valid states retain an unbroken, recomputable lineage
  from $S_0$; there are no untracked soft states.
- **Computational Masonry:** operational states are bounded by cryptographic
  architecture; invalid instructions collapse to identity with no operational
  state change.
- **Structural Enforceability:** geometric and cryptographic constraints take
  precedence over post-hoc behavioral compliance scores.
- **Mungu Theory:** True Intelligence is framed as Symbiosis plus *Con-scire*—
  compatibility with the environment together with a verifiable, shared
  structural reality.
- **WeThePeople Engine:** the same invariants extend to civic authority: no
  authority without lineage, no execution without a receipt, and no public
  trust without auditability.

Language about hardware-level locks, physical zero-knowledge membranes, or
Hamiltonian conservation of truth describes architectural aspiration, not the
current implementation. The forensic boundary above is the calibration
instrument for those claims.

---

## 5. Communication Guide

The core remains stable while examples and depth should match the audience.

| Audience | Lead with | Avoid leading with |
|---|---|---|
| General public | Proof before consequence; capability is not authority | Dense cryptographic notation |
| Engineers | State $(O,\Gamma)$, predicates, receipts, and replay | Metaphor without mechanism |
| Policy and legal | Authority, scope, and accountability before actuation | Claims stronger than the evidence |
| Security | Complete mediation, deterministic verification, and lineage continuity | Trust-based assurances |
| Distributed systems | Validity before consensus and explicit fault boundaries | Consensus as a substitute for correctness |

> Do not merely tell the machine what it should not do.<br>
> Build the computational world so that what it cannot prove, it cannot make real.

---

## 6. Implementation Roadmap

The doctrine exists in several forms. The highest-leverage next step is a small,
independently recomputable verifier.

### Phase 1 — Minimal state-transition simulator

- Represent state explicitly as $S=(O,\Gamma)$.
- Implement a pure admissibility predicate $\mathbb{P}$.
- On acceptance, mutate $O$ and append an acceptance receipt.
- On refusal, preserve $O$ and append a refusal receipt.
- Expose hash-chain lineage that a third party can replay and verify.
- Make no claim of zero-knowledge proofs or hardware roots of trust.

### Phase 2 — Policy digest binding

- Canonicalize the constitutional artifact.
- Include $\operatorname{SHA256}(\text{constitution})$ in every receipt.
- Derive runtime parameters from the bound policy or check them against it.

### Phase 3 — Real root of trust

- Replace names and placeholder human signatures with real keys.
- Sign genesis and the constitutional digest.

### Phase 4 — External checkpointing

- Persist signed Merkle or linear heads outside the originating process.
- Optionally add an RFC 3161 timestamp or public transparency-log inclusion.

Until these phases close, the accurate public claim is: developmental
provenance is real, trajectory-aware receipts exist, and full independent
cryptographic provenance remains engineering work.

See [ROADMAP.md](./ROADMAP.md) for the wider project roadmap and
[API_REFERENCE.md](./API_REFERENCE.md) for current and planned interfaces.

---

## 7. Repository Guide

| Resource | Purpose |
|---|---|
| [`tas_1st_principles.yaml`](./tas_1st_principles.yaml) | Constitutional principles |
| [`tas_kernel/`](./tas_kernel/) | Kernel and verifier implementation work |
| [`schemas/paradata-receipt.json`](./schemas/paradata-receipt.json) | ParaData receipt schema |
| [`tas_tools/tas_sequencer.py`](./tas_tools/tas_sequencer.py) | Artifact sequencing and lineage metadata |
| [`tas_cli.py`](./tas_cli.py) | Repository command-line workflows |
| [`tests/`](./tests/) and [`conformance-tests/`](./conformance-tests/) | Tests and conformance scenarios |
| [`audits/`](./audits/) | Audit artifacts |
| [`TAS_DNA_Deck.md`](./TAS_DNA_Deck.md) | Dissertation-level framing |

### CLI quick reference

```bash
python tas_cli.py shadow-scan .
python tas_cli.py sequence README.md
python tas_cli.py verify-identity README.md --signature "Russell Nordland"
```

### Tests

```bash
PYTHONPATH=$(pwd)/tas_pythonetics/src:$(pwd)/tas-recursion-conversion:$(pwd) pytest
```

---

## Citation

If you use this software or theoretical framework, please cite:

```yaml
cff-version: 1.2.0
message: "If you use this software or theoretical framework, please cite it as follows."
authors:
  - family-names: "TrueAlphaSpiral"
    given-names: "Research Collective"
title: "The Physics of Admissible State Transition: Deterministic Cryptographic Execution Architecture"
version: "1.0.0"
date-released: "2026-09-12"
url: "https://github.com/TrueAlpha-spiral/TrueAlpha-spiral"
```

## Synthesis

**TrueAlphaSpiral is the attempt to make authorization, provenance, lineage,
and invariant compliance structural properties of execution rather than
promises made around execution—and this repository shows both the sequence of
that attempt and the cryptographic layer still required to make belief
unnecessary.**

License: Apache-2.0
