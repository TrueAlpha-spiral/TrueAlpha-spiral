# ASSP Integration Blueprint

## Unified Singularity Kernel deployment and verification profile

**Status:** engineering blueprint; not a certification, authorization to operate,
or statement of federal endorsement.

## 1. Objective

This blueprint maps the repository's deterministic admission components into an
integration boundary suitable for an American Science & Security Platform
(ASSP) pilot. The integration objective is narrower than a claim of machine
infallibility:

> A protected state transition occurs only after the candidate, authority,
> semantic context, lineage head, epoch, and scope have been verified, and the
> decision has been durably recorded.

Probabilistic systems may propose candidates. They do not grant authority and
must not write protected state directly.

## 2. System boundary

```text
Untrusted / probabilistic                         Institution-controlled TCB

model, analyst, tool
        |
        v
 candidate bytes + signed envelope ---> canonical parser / context resolver
                                                  |
                                      authority + scope + epoch resolver
                                                  |
                                      lineage / replay verification
                                                  |
                                      deterministic policy evaluation
                                                  |
                              +-------------------+-------------------+
                              |                                       |
                           REFUSED                                 ADMITTED
                              |                                       |
                              +--------> durable signed receipt <-----+
                                                                      |
                                                          atomic executor
                                                                      |
                                                         protected state
```

The trusted computing base (TCB) comprises the canonical parser, definition and
context resolvers, authority resolver, signature verifier, admission policy,
receipt signer, durable decision ledger, and atomic executor. Model weights,
prompts, user interfaces, and orchestration frameworks remain outside the TCB.

The current repository implements much of the admission and evidence boundary,
but it does **not** yet provide a transactional adapter that atomically couples a
durable admission receipt to an application state mutation. That adapter is an
IOC blocker for consequential deployment.

## 3. Constitutional request contract

An integration request has two separately parsed objects:

1. **Candidate** — the exact canonical object proposed for execution.
2. **Sovereignty envelope** — the signed authorization containing the schema and
   canonicalization versions, credential and checkpoint identifiers, authority
   epoch, context snapshot hash, requested operation, candidate hash, parent
   receipt hash, nonce, signature algorithm, and signature.

The authority signature binds the canonical envelope body to the TAS authority
domain. The candidate is accepted only when its canonical hash equals the signed
`candidate_hash`. Resolved authority and semantic context must mutually bind to
the same checkpoint and effective epoch.

Every decision, including malformed or unauthorized requests where a receipt can
be safely constructed, must produce a signed, content-addressed receipt before a
result is returned. A refusal may advance the evidence timeline, but must not
advance protected application state.

## 4. Trust boundaries and ownership

| Boundary | Owner | Required control | Failure behavior |
|---|---|---|---|
| Candidate ingress | Application team | Byte and size limits; canonical JSON profile; schema version allowlist | Refuse and record |
| Human/juridical authority | Agency security authority | HSM/KMS-held signing keys; credential lifecycle; least-privilege scope | Refuse unknown, expired, or revoked authority |
| Semantic registry | Governance authority | Signed, versioned definitions and immutable context snapshots | Refuse missing or inconsistent definitions |
| Admission service | Platform security team | Reproducible build; isolated verifier; no application write credential | Fail closed |
| Decision ledger | Records/evidence service | Append-only, durable writes; retention; trusted receipt keys | Do not execute if persistence fails |
| Executor | Application owner | Single-use receipt consumption; transaction-bound preconditions | Roll back on any mismatch |
| Witness/export | Independent assessor | Read-only verification and reproducible test bundle | Alert; never repair history in place |

No personal identity is a cryptographic root merely by being named in policy.
Tier-0 authority must be represented by an approved credential, explicit scope,
documented succession/recovery procedures, and auditable governance.

## 5. Required end-to-end transaction

The executor must implement the following indivisible protocol:

1. Read the current protected-state version and current receipt head.
2. Submit the candidate and signed envelope to the admission service.
3. Require a durable `ADMITTED` receipt whose candidate, operation, context,
   authority epoch, and parent head match the pending transaction.
4. In one serializable transaction, compare the state version and receipt head,
   mark the admission receipt consumed, apply the candidate, and append the new
   application state commitment.
5. Roll back all writes if any precondition changes or receipt consumption is not
   unique.
6. Emit an execution receipt linked to both the admission receipt and resulting
   state commitment.

This compare-and-commit step is the control that closes the verification/use
(TOCTOU) race. A standalone successful admission response is never an execution
authorization after its bound state has changed.

## 6. Verification-domain matrix

| Domain | Admission proof | Required negative test | IOC evidence |
|---|---|---|---|
| Canonicalization | One byte representation and domain-separated hash | Duplicate keys, non-canonical bytes, number/Unicode drift | Cross-implementation vector digest |
| Authority | Signature resolves to the checkpoint credential | Forged, unknown, expired, or substituted key | Credential and validation transcript |
| Lineage | Parent receipt exists and ancestry validates to a trust root | Missing, cyclic, tampered, or cross-context parent | Verified receipt-chain export |
| Revocation | Resolved snapshot is current and not revoked | Previously valid signature after revocation | Revocation publication and refusal receipt |
| Replay | Nonce and admission receipt have single-use semantics | Same request before and after restart; concurrent duplicate | Durable nonce/consumption record |
| Epoch | Envelope, context, and authority epochs agree | Stale and future epoch substitution | Epoch-transition vectors |
| Scope | Requested operation is covered by the resolved policy hash | Operation and policy mutation | Scope-policy artifact and refusal receipt |
| Execution | Compare-and-commit binds admitted and used state | Head/state mutation between verify and use | Transaction log and execution receipt |
| Receipt | Signed canonical receipt is persisted before return | Disk failure, truncation, signature and ancestry tampering | Offline verifier report |

## 7. Six-stage verification campaign

### Stage 1 — specification baseline

Freeze the schemas, canonicalization profile, domain separators, error taxonomy,
state machine, threat model, key lifecycle, and refusal invariants. Assign every
normative requirement a stable identifier (`USK-REQ-*`).

### Stage 2 — deterministic conformance

Publish positive and negative vectors for every matrix row. Runs must use fixed
inputs and compare canonical result and receipt hashes, not timestamps or prose.
Record toolchain versions and SHA-256 hashes of the test bundle.

### Stage 3 — differential verification

Build an independent canonicalizer and offline receipt/lineage verifier without
sharing parsing code with the production gate. Compare acceptance, refusal code,
and normalized hashes across both implementations.

### Stage 4 — adversarial campaign

Exercise malformed encodings, key substitution, stale and revoked credentials,
lineage forks, nonce races, ledger failure, clock boundary behavior, compromised
dependency inputs, and verification/use races. Preserve every refusal as evidence
without treating receipt creation as protected-state mutation.

### Stage 5 — closure demonstration

Run fault injection at each compare-and-commit step. Prove that an admitted and
consumed receipt identifies the exact candidate and pre-state used, while all
failed paths leave protected state unchanged.

### Stage 6 — independent reproduction

Provide a clean-room operator with source revision, dependency lock data, build
instructions, public verification keys, vectors, and expected digests. The
operator must reproduce the suite without private signing keys; test-only keys
must be clearly marked and excluded from production trust.

## 8. Deployment topology

| Plane | Services | Network posture |
|---|---|---|
| Proposal | Model gateways, analyst UI, workflow adapters | Untrusted; cannot reach protected data stores directly |
| Control | API gateway, admission gate, context/authority resolvers | Default deny; mutually authenticated service identities |
| Evidence | Receipt ledger, witness exporter, offline verifier | Append-only writer path; read-only assessor path |
| Consequence | Transaction coordinator and application-specific executor | Accepts only locally verified, unconsumed receipts |
| Governance | Credential issuance/revocation, policy registry, change control | Separation of duties and dual control for trust-root changes |

Begin at sovereignty profile S2 (private authority and execution boundary) for a
consequential pilot. Advance to S3–S5 only when private inference, disconnected
operation, or hardware attestation is justified by the system threat model; a
higher label does not substitute for control testing.

## 9. IOC work packages and exit criteria

| Work package | Deliverable | Exit criterion |
|---|---|---|
| WP-1 Contract freeze | Versioned schemas, state machine, requirement IDs | Architecture and security authorities approve one baseline |
| WP-2 Authority operations | HSM/KMS adapter, issuance, revocation, recovery runbooks | Expired/revoked credentials refuse during restart and partition tests |
| WP-3 Evidence durability | Production ledger and offline verifier | Acknowledged decisions survive crash and independently verify |
| WP-4 Atomic consequence | Application transaction adapter | Fault injection produces no unauthorized protected-state delta |
| WP-5 Conformance | Portable signed vector bundle | Two independent implementations produce matching outcomes |
| WP-6 Adversarial assessment | Threat-model report and remediation ledger | No unresolved critical finding; residual risks accepted in writing |
| WP-7 Reproduction | Hermetic build/test manifest and operator guide | Independent team reproduces expected digests and refusal behavior |
| WP-8 Operations | Monitoring, incident response, key rotation, continuity | Tabletop and recovery exercise meet approved objectives |

IOC readiness requires all work-package evidence, not a narrative declaration.
Authorization to operate, privacy review, records scheduling, accessibility,
procurement, and mission-specific legal review remain decisions of the responsible
institutions.

## 10. Repository evidence and gaps

### Available building blocks

- `context_snapshot.py` supplies canonical JSON, domain hashing, definition
  resolution, and immutable semantic context snapshots.
- `admission_gate.py` supplies authority snapshots, Ed25519 and secp256k1
  verification, context-bound admission decisions, durable receipt storage, and
  authenticated receipt ancestry verification.
- `core/wakechain.py` models distinct evidence and admitted-state sequences.
- `core/deployment_profile.py` defines S0–S5 operational maturity profiles.
- `conformance-tests/` and `tests/` provide initial deterministic and adversarial
  checks.

### Must be completed before consequential IOC

1. Implement durable global nonce consumption; a nonce field alone is not replay
   prevention.
2. Implement and test the atomic executor protocol in Section 5.
3. Replace local/test keys and in-memory resolvers with governed production
   services and hardware-backed receipt custody where required.
4. Add independent canonicalization and verifier implementations.
5. Define normative scope-policy evaluation; binding a policy hash is not the
   same as evaluating whether an operation is permitted.
6. Define receipt retention, privacy minimization, redaction/export, time source,
   availability, recovery, and trust-root rotation procedures.
7. Produce a requirements traceability matrix linking every `USK-REQ-*` control
   to code, tests, evidence, owner, and residual risk.

## 11. Pilot sequence

1. Select a reversible, low-impact read-only workflow.
2. Inventory protected states, operations, authorities, and semantic definitions.
3. Establish keys, revocation, scope policies, and a genesis trust checkpoint.
4. Deploy proposal and control planes with no consequence-plane write path.
5. Complete conformance, differential, crash, replay, and red-team campaigns.
6. Enable shadow execution and compare intended effects without mutating state.
7. Enable narrowly scoped consequence writes behind the atomic adapter.
8. Review evidence at a fixed checkpoint before expanding scope.

## 12. Readiness declaration template

A readiness declaration should identify the exact source revision, build and
vector digests, trust roots, approved scope, deployment profile, assessor,
unresolved risks, and expiration date. It should state only what the evidence
supports. Authorship, architectural provenance, and organizational authority are
separate records and must not replace cryptographic or operational proof.
