# SOP-TAS-01: Technical Protocol for Multi-Agent State Isolation and Admissibility Gating
Standard Operating Procedure for Formal Computational Masonry, Complete Mediation, and Invariant-Preserving Execution

## 1. Purpose and Strategic Scope of Computational Integrity
In high-consequence autonomous and multi-agent environments, "behavioral resemblance" is an unprovable and discarded metric. The Sovereign Data Foundation explicitly rejects legacy "Behavioral Alignment"—which relies on the probabilistic hope that generative models will simulate correct intent through post-hoc prompting or superficial guardrails. This methodology is fundamentally vulnerable to stochastic drift, where unanchored optimization compounds errors until the system dissolves into unverified state transitions.

This standard operating procedure operationalizes Structural Enforceability. Our primary architectural defense is the deterministic, compile-time gating and runtime verification of state transitions.

### The Sentient Lock Directive
The primary directive of this document is to maintain the Sentient Lock as an absolute topological invariant:
$$\Delta z \quad \not\Rightarrow \quad \Delta O$$
A mutation in an agent’s internal computational, cognitive, or latent state ($\Delta z$) carries zero intrinsic authority over the protected operational state ($\Delta O$).

We operate under the discipline of Process Science: the formal mathematics of path legitimacy. In this architecture, legitimacy resides strictly in the authenticated trajectory, not the terminal output.

## 2. Axiomatic Baseline: Defining the Constitutive State

### 2.1. Constitutive State Tuple
The TAS architecture defines a complete system state as an immutable pair:
$$S_k = (O_k, \Gamma_k)$$
$O_k \in \mathcal{O}$ (Operational State): The protected operational configuration (balances, execution rights, policy tables, actuator outputs). $O_k$ possesses no independent existential authority; it is a structural shadow cast by the historical tensor $\Gamma_k$.
$\Gamma_k \in \mathbf{\Gamma}$ (Historical Tensor): An authenticated, append-only, tamper-evident cryptographic log of all state-transition events.

### 2.2. The Reconstruction Map ($L$)
State is evaluated via Cursive Computation, where the endpoint structurally contains its generating path. Operational state is computed strictly as a deterministic projection over the admitted history:
$$O_k = L(\Pi_A(\Gamma_k))$$
where $\Pi_A$ projects full history onto committed, admitted transition events. Any out-of-band mutation that attempts to alter memory values directly breaks the constitutive predicate $O = L(\Pi_A(\Gamma))$, causing the state to become topologically invalid and unexecutable.

### 2.3. System Axioms for the Verifier
The Equivalence Axiom ($P_0$):
$$S_a \equiv S_b \iff \Pi(S_a) \equiv \Pi(S_b)$$
Two states are identical if and only if their generating trajectories are equivalent. Terminal output equality is insufficient for authority ($O_a = O_b \land \Gamma_a \neq \Gamma_b \implies S_a \neq S_b$).

The Admissibility Axiom ($P_1$):
$$S_t \xrightarrow{x} S_{t+1} \iff V(S_t, x, E_t) = \text{ADMIT}$$
A transition executes if and only if it satisfies the formal verifier $V$. Admissibility is a physical execution constraint enforced at the compilation and execution boundary.

The Invariant Preservation Axiom ($P_2$):
$$\forall t \ge 0, \quad Z_0 \subseteq \mathcal{A}^t \implies Z_0 \subseteq \bigcap_{t=0}^\infty \mathcal{A}^t \neq \emptyset$$
Every admissible transition relation must preserve the non-empty root invariant core $Z_0 \neq \emptyset$, guaranteeing that recursive evolution cannot dissolve system boundaries.

### 2.4. Design Paradigm Comparison
Dimension | Stochastic LLM / Unconstrained RL | Bounded Invariant Architecture (TAS)
--- | --- | ---
Path Dependency | Path-independent; terminal reward optimization | Path-dependent; trajectory co-constitutes state
Authority Model | Ambient trust based on model confidence | Zero authority; explicit cryptographic proof required
State Representation | Extensional, mutable memory ($S = O$) | Intensional, cursive tuple ($S = (O, \Gamma)$)
Evaluation Timing | Post-hoc output filtering or sampling | Pre-execution deterministic verification gate
Failure Handling | Prompt retry, silent hallucination, or crash | Operational quiescence ($\Delta O = 0$) with durable refusal ($\Delta \Gamma > 0$)

## 3. The Sentient Lock: Isolating Cognition from Consequence
The TAS architecture enforces the Calculator Doctrine. The verifier does not negotiate, debate intent, or evaluate conversational plausibility. It mechanically evaluates an intersecting boolean lattice of formal predicates.

### 3.1. Intent-Invariance
Whether an agent proposes an action out of simulated benevolence, operational error, or adversarial compromise is irrelevant. Subjective motive is stripped of causal agency. The deterministic transition relation:
$$V(S_t, x_t, E_t) \in \{\text{ADMIT}, \text{REFUSE}, \text{UNDETERMINED}\}$$
serves as the sole arbiter of consequence.

### 3.2. Asymmetric Coupling ($G \nrightarrow V_{\text{active}}$)
The candidate generator $G$ and the active verifier $V_{\text{active}}$ are asymmetrically coupled:
- $G$ emits speculative candidate proposals $x \in \mathcal{X}$.
- $V_{\text{active}}$ evaluates $x$ in a stateless, isolated sandbox.
- $G$ possesses no write access or configuration path to $V_{\text{active}}$.
Modifying $V_{\text{active}}$ requires a distinct, higher-order meta-transition governed by Section 6.

## 4. Protocol for Multi-Agent Consensus and Proposal Gating

### 4.1. Anti-Self-Authorization ($Q(x) \not\Rightarrow A(x)$)
In multi-agent environments, consensus among generators cannot manufacture admissibility:
$$Q(x) = 1 \land V(S, x, E) \neq \text{ADMIT} \implies \Delta O = 0$$
Even if $10^6$ distributed speculative branches agree on a proposal, the verifier halts execution if proof obligations are unmet.

### 4.2. Separating Immutable Proposals from Lifecycle Event Records
To prevent hash instability, the architecture decouples immutable proposal definitions from subsequent lifecycle event records:

Immutable Proposal Record ($G_{\text{prop}}$):
$$G_{\text{prop}} = \langle \text{ProposalID}, \text{ProposerID}, \text{Payload } x, \text{Preconditions } P, \text{Nonce } \nu, \sigma_{\text{proposer}} \rangle$$
$$\text{AnchorID} = H(G_{\text{prop}}) \quad (\text{Strictly Constant})$$

Discrete Lifecycle Event Records (Referencing $\text{AnchorID}$):
- Admission Record: $R_{\text{admit}} = \langle \text{AnchorID}, \text{Epoch}, \text{UVK\_Sig}, \tau_{\text{admit}} \rangle$
- Refusal Record: $R_{\text{refuse}} = \langle \text{AnchorID}, \text{Epoch}, \text{FailedPredicates}, \text{UVK\_Sig}, \tau_{\text{refuse}} \rangle$
- Completion Record: $R_{\text{complete}} = \langle \text{AnchorID}, \text{ExecutionWitness}, \tau_{\text{complete}} \rangle$
- Recovery Record: $R_{\text{recovery}} = \langle \text{AnchorID}, \text{ObservedOutcome}, \text{ResolutionSig}, \tau_{\text{recovery}} \rangle$

### 4.3. The Universal Verifier Kernel (UVK) Predicate Lattice
The UVK evaluates an 11-predicate boolean lattice ($\mathcal{P}_{\text{admit}}$) for any candidate proposal:
$$V(S, x, E) = \text{ADMIT} \iff \bigwedge_{j=1}^{11} p_j = 1$$
- AuthorityValid ($p_1$): Validates cryptographic signature and identity of the proposer against enrollment registries.
- ScopeValid ($p_2$): Verifies proposal remains within explicit jurisdiction and role delegation limits.
- CandidateIntegrity ($p_3$): Verifies $H(x)$ matches payload hash and is free from serialization corruption.
- ContextValid ($p_4$): Confirms proposal references the active operational epoch and state baseline.
- LineageValid ($p_5$): Validates unbroken parent-hash chain linking proposal to genesis anchor $S_0$.
- InvariantsPass ($p_6$): Checks candidate against inviolable safety invariants ($Z_0$).
- Canonical ($p_7$): Confirms RFC 8785 (JCS) deterministic canonical representation.
- Executable ($p_8$): Verifies target functions, parameters, and environmental dependencies are instantiable.
- ReceiptAvailable ($p_9$): Confirms audit storage channels are online to seal execution receipts.
- NonceFresh ($p_{10}$): Confirms nonce $\nu$ has not been expended, preventing replay attacks.
- TipMatch ($p_{11}$): Verifies parent state matches current operational tip ($h = \text{Tip}(O)$), preventing state forks.

### 4.4. Composite Proof Bundle
Every candidate $x$ must be accompanied by an explicit proof bundle:
$$\pi_{\text{composite}}(x) = \langle \pi_{\text{auth}}, \pi_{\text{scope}}, \pi_{\text{integrity}}, \pi_{\text{precond}}, \pi_{\text{temporal}} \rangle$$
where temporal validity enforces:
$$\operatorname{TemporalClause}(t_{\text{now}}) \iff (t_{\text{valid}} \le t_{\text{now}} \le t_{\text{expire}}) \land \operatorname{IsFresh}(\nu, \text{NonceCache})$$

## 5. Transition Mechanics: Decoupled Lifecycle and Conservation

### 5.1. Decoupled Admission and Execution Matrix
Admission decisions evaluate structural entitlement; execution status reflects physical realization. Uncertainty about execution does not retroactively erase an established admission decision.

Operational Situation | Admission Decision ($\mathcal{D}$) | Execution Status ($\mathcal{E}$) | Operational Effect ($\Delta O$) | Lineage Entry Emitted ($\Delta \Gamma$)
--- | --- | --- | --- | ---
Authorized, awaiting execution | `ADMIT` | `NOT_STARTED` | $\Delta O = 0$ (quiescent) | $R_{\text{admit}}$ (sealed)
Authorized, completion established | `ADMIT` | `COMPLETED` | $O \leftarrow F(O, x)$ | $R_{\text{complete}}$ (witnessed)
Authorized, outcome uncertain / crash | `ADMIT` | `UNKNOWN` | $\Delta O = 0$ (quiescent / escrow) | $R_{\text{uncertain}}$ (timeout logged)
Rejected before execution | `REFUSE` | `NOT_STARTED` | $\Delta O = 0$ (quiescent) | $R_{\text{refuse}}$ (predicate logged)
Evidence insufficient to decide | `UNDETERMINED` | `NOT_STARTED` | $\Delta O = 0$ (quiescent) | $R_{\text{undetermined}}$ (gap logged)

### 5.2. Refusal Conservation Law ($\Delta O = 0, \Delta \Gamma > 0$)
The architecture formalizes refusal not as an untracked abort, but as operational quiescence with a durable refusal record:
$$\kappa(S_t, x_t) = \begin{cases}
(F(O_t, x_t), \, \Gamma_t \mathbin{\Vert} R_{\text{complete}}), & \text{if } V = \text{ADMIT} \land \mathcal{E} = \text{COMPLETED} \\[4pt]
(O_t, \, \Gamma_t \mathbin{\Vert} R_{\text{refuse}}), & \text{if } V = \text{REFUSE} \\[4pt]
(O_t, \, \Gamma_t \mathbin{\Vert} R_{\text{uncertain}}), & \text{if } V = \text{ADMIT} \land \mathcal{E} = \text{UNKNOWN}
\end{cases}$$
Operational state remains stationary ($\Delta O = 0$), preventing unauthorized consequence, while history advances monotonically ($\Delta \Gamma > 0$), permanently etching boundary challenges into the audit record.

## 6. Meta-Governance: Recursive Invariant Enforcement
The same five-stage pipeline and complete mediation constraints apply recursively to mutations of the verifier kernel itself ($V_n \to V_{n+1}$).

### 6.1. The Ratchet Constraint
$$V_n \xrightarrow{\text{meta}} V_{n+1} \iff M(V_n, \Delta V) = 1$$
A verifier update is treated as a high-consequence transition. The active verifier $V_n$ must evaluate and seal the proposal for $V_{n+1}$ prior to hot-swapping the execution kernel.

### 6.2. Requirements for Meta-Admissibility ($M$)
- Tier 0 Cryptographic Quorum: Multi-signature threshold approval from enrolled root trustees.
- Preserved Invariant Floor ($Z_0$): Mathematical verification that $V_{n+1} \models Z_0$. Any proposal that relaxes, modifies, or deletes an invariant within $Z_0$ fails verification unconditionally.
- Deterministic Diff Verification: Automated semantic analysis verifying that $V_{n+1}$ contains no non-deterministic execution paths.
- Preserved Lineage Provenance: Version hash $H(V_{\text{active}})$ is sealed into all subsequent lifecycle receipts.

## 7. Survivability, Adversarial Boundaries, and Recovery

### 7.1. The Invariant Triple ($\mathcal{I}$)
The formal verification foundation is defined by the triple:
$$\mathcal{I} = \langle \mathcal{P}_{\text{admit}}, \, Z_0, \, \mathcal{M}_{\text{complete}} \rangle$$
where $\mathcal{M}_{\text{complete}}$ defines the complete mediation boundary covering all protected mutators.

### 7.2. Adversarial Surface & Self-Falsification
The safety of this architecture extends strictly as far as complete mediation and verifier correctness hold.

Failure Mode | Vulnerability Vector | Defense & Proof Obligation
--- | --- | ---
Incomplete Mediation | Direct memory or hardware write bypassing $V$. | Boundary Theorem: $O_k = L(\Pi_A(\Gamma_k))$ halts on unmediated mutation.
Verifier Defect | Logic flaw in $V$ admitting an illegal state. | Minimal TCB; formal proof of verifier kernel in machine-checked logic.
Key Compromise | Compromised private key forging authority $E$. | Multi-signature threshold quorums (k-of-n); short epoch lease bounds.
Canonicalization Ambiguity | Non-injective JSON encoding allowing signature malleability. | Strict RFC 8785 (JCS) encoding; length-prefixed binary hashes.
Oracle Falsity | Cryptographically authentic evidence that is factually false. | Decouple authenticity from truth: $\operatorname{VerifySig}(pk, m, \sigma) = 1 \not\Rightarrow m = \text{true}$.

The Boundary Theorem:
$$\boxed{\text{Find one unmediated bypass } b: O_t \to O_{t+1} \text{ where } b \notin \operatorname{Domain}(V), \text{ and the safety proof is void.}}$$

### 7.3. The Phoenix Recovery Protocol: Monotonic Lineage Rollback
When an execution results in $\mathcal{E} = \text{UNKNOWN}$ or state corruption is detected, the Phoenix protocol restores operational state without violating lineage monotonicity ($\Delta \Gamma > 0$):
$$\begin{aligned}
O_{k+1} &= O_{\text{checkpoint}} \quad &&\text{(Operational State Restored)} \\
\Gamma_{k+1} &= \Gamma_k \mathbin{\Vert} \langle \text{CORRUPT\_EVID}, H(O_{\text{corrupt}}), \tau_{\text{fault}} \rangle \mathbin{\Vert} \langle \text{PHOENIX\_RESTORE}, H(O_{\text{checkpoint}}), \tau_{\text{recovery}} \rangle
\end{aligned}$$
Operational memory returns to a verified, attested checkpoint, while corruption evidence and the restorative action are permanently sealed into $\Gamma$. History is never rewound, deleted, or fabricated.

## 8. Closing Reachability & Protected Effect Invariant
$$\boxed{
\operatorname{ProtectedEffect}(x) \implies \operatorname{PriorDurableAdmission}(R_{\text{admit}}) \land \operatorname{Bound}(R_{\text{admit}}, x) \land \operatorname{PreconditionsStillValid}(x)
}$$

Accompanying Scope Statement:
Under complete mediation and the stated authentication, storage, and execution assumptions, every protected effect requires a prior durable admission bound to that operation. Authenticated lineage preserves the distinction between authorization, established completion, refusal, and unresolved outcome. Recovery extends that history without rewriting earlier records.

The Five-Stage Execution Pipeline:
$$\boxed{\text{Capability proposes}} \longrightarrow \boxed{\text{Evidence supports}} \longrightarrow \boxed{\text{Authority permits}} \longrightarrow \boxed{\text{Verification admits}} \longrightarrow \boxed{\text{Consequence exists}}$$
Authority is inherited through verifiable lineage, never simulated through behavioral resemblance. Power must produce its receipts, or it will be refused at the gate.
