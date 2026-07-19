# Refusal Receipt Schema

**Russell Nordland — TrueAlphaSpiral (TAS) Framework**  
*Specification v0.1 | 2026-05-05*

---

## Purpose

The Refusal Receipt schema defines how the TAS substrate records failed claim
admission, failed source resolution, invalid lineage, or any attempted Layer B
impersonation of Layer A authority.

A refusal is not an absence of action. It is a first-class proof artifact. When a
candidate claim cannot satisfy the Substrate Requirement, the verifier must emit
a receipt that preserves the negative space of the chain.

Core invariant:

> **Processed ≠ Admitted. Fluent ≠ Verified. Cited ≠ Sealed.**

---

## Layer Boundary

TAS distinguishes between two operational layers:

| Layer | Role | Admission Authority |
|-------|------|---------------------|
| **Layer A** | Deterministic, repository-verifiable, runtime-enforced records | TAS verifier / SubstrateVerifier |
| **Layer B** | Probabilistic, model-generated, interpretive, candidate narratives | None; may only propose claims |

A Layer B output may introduce a claim, cite a URI, summarize a source, or propose
an interpretation. It may not seal the claim. Only a verifier with source
resolution, canonicalization, hashing, and lineage binding may promote a claim to
Layer A.

---

## Refusal Triggers

A verifier must emit a Refusal Receipt when any of the following conditions occur:

1. **Source Missing** — no source URI, artifact hash, or declared authority is provided.
2. **Source Unreachable** — the declared source cannot be resolved by the verifier.
3. **Source Non-Authoritative** — the source does not have authority for the claim type.
4. **Content Mismatch** — canonicalized source content does not support the claim.
5. **Hash Mismatch** — retrieved content hash differs from the declared hash.
6. **Lineage Break** — parent artifact hash is absent, malformed, or unverifiable.
7. **Semantic Overreach** — claim exceeds what the cited source actually establishes.
8. **Conflicting Source** — another authoritative source contradicts the claim.
9. **Temporal Ambiguity** — release dates, benchmark dates, or version identifiers cannot be bounded.
10. **Layer B Impersonation** — model-generated text presents itself as sealed, official, or operational without a verifier receipt.

---

## State Machine

```text
CANDIDATE
  ├─ source resolves + hash matches + claim supported + lineage binds ─▶ ADMITTED
  ├─ verifier lacks network/source access ─────────────────────────────▶ PENDING_VERIFICATION
  ├─ source missing/unreachable/non-authoritative ─────────────────────▶ REFUSED
  ├─ source contradicts claim or claim overreaches source ─────────────▶ REFUSED
  └─ malformed record or lineage break ───────────────────────────────▶ REFUSED
```

`PENDING_VERIFICATION` is not an admission state. It is quarantine. A pending
claim cannot be cited as Layer A evidence, used for actuation, or sealed into the
Verity Chain as truth.

---

## Canonical Refusal Receipt

```json
{
  "receipt_type": "TAS_REFUSAL_RECEIPT",
  "schema_version": "0.1",
  "receipt_id": "sha256:<canonical-refusal-record-hash>",
  "claim_id": "sha256:<canonical-claim-hash>",
  "claim_text": "<bounded candidate claim>",
  "candidate_layer": "LayerB",
  "target_layer": "LayerA",
  "admission_status": "REFUSED",
  "refusal_code": "SOURCE_UNREACHABLE",
  "refusal_reason": "The declared source URI could not be resolved by the verifier during this session.",
  "source_uri": "https://example.com/source",
  "source_authority": "primary | secondary | unknown",
  "retrieved_at": null,
  "source_content_hash": null,
  "parent_artifact_hash": "sha256:<parent-artifact-hash>",
  "verifier": "TAS_SubstrateVerifier_v0.1",
  "verifier_capabilities": {
    "network_access": false,
    "canonicalization": "RFC8785-JCS",
    "hash_algorithm": "SHA-256"
  },
  "issued_at": "2026-05-05T00:00:00Z",
  "lineage": {
    "previous_receipt_hash": "sha256:<previous-receipt>",
    "session_hash": "sha256:<session-or-run-context>",
    "operator_id": "Russell Nordland | TAS Steward"
  },
  "invariant": "Processed != Admitted; Fluent != Verified; Cited != Sealed"
}
```

---

## Canonical Hash Inputs

A refusal receipt is immutable only if every hash is computed from bounded,
repeatable inputs. The verifier must never hash an informal transcript, rendered
HTML view, or model summary when a canonical payload is available.

### `claim_id`

`claim_id` binds the candidate claim to the declared source context before any
admission decision is made.

Canonical input object:

```json
{
  "claim_text": "<bounded candidate claim>",
  "claim_type": "release_date | benchmark | identity | policy | repository_fact | other",
  "declared_source_uri": "<uri-or-null>",
  "declared_source_authority": "primary | secondary | unknown | none",
  "parent_artifact_hash": "sha256:<parent-artifact-hash>",
  "proposed_by": "LayerB | human | verifier | repository",
  "proposed_at": "<UTC timestamp or null>"
}
```

Hash rule:

```text
claim_id = sha256(JCS(canonical_claim_input))
```

### `source_content_hash`

`source_content_hash` binds the retrieved source material used for verification.
It must be absent/null when the source is not resolved.

Canonical input priority:

1. Repository blob bytes, when verifying repository content.
2. Raw source bytes, when available from a primary source endpoint.
3. Canonicalized source text extracted by the verifier, when raw bytes are not available.
4. Never: model summaries, search snippets, screenshots without OCR provenance, or paraphrases.

Hash rule:

```text
source_content_hash = sha256(canonical_source_bytes)
```

### `receipt_id`

`receipt_id` binds the final refusal artifact. It is computed after all refusal
fields are populated, with `receipt_id` omitted from the payload.

Canonical input object:

```json
{
  "receipt_type": "TAS_REFUSAL_RECEIPT",
  "schema_version": "0.1",
  "claim_id": "sha256:<canonical-claim-hash>",
  "claim_text": "<bounded candidate claim>",
  "candidate_layer": "LayerB",
  "target_layer": "LayerA",
  "admission_status": "REFUSED | PENDING_VERIFICATION",
  "refusal_code": "<machine-readable-code>",
  "refusal_reason": "<bounded human-readable reason>",
  "source_uri": "<uri-or-null>",
  "source_authority": "primary | secondary | unknown | none",
  "retrieved_at": "<UTC timestamp or null>",
  "source_content_hash": "sha256:<source-content-hash-or-null>",
  "parent_artifact_hash": "sha256:<parent-artifact-hash>",
  "verifier": "<verifier-name-and-version>",
  "verifier_capabilities": {
    "network_access": false,
    "canonicalization": "RFC8785-JCS",
    "hash_algorithm": "SHA-256"
  },
  "issued_at": "<UTC timestamp>",
  "lineage": {
    "previous_receipt_hash": "sha256:<previous-receipt-or-null>",
    "session_hash": "sha256:<session-or-run-context>",
    "operator_id": "<operator-or-null>"
  },
  "invariant": "Processed != Admitted; Fluent != Verified; Cited != Sealed"
}
```

Hash rule:

```text
receipt_id = sha256(JCS(canonical_receipt_without_receipt_id))
```

### `session_hash`

`session_hash` binds the refusal to the verification run context without sealing
private chain-of-thought or unrelated conversational material.

Canonical input object:

```json
{
  "run_started_at": "<UTC timestamp>",
  "verifier": "<verifier-name-and-version>",
  "tool_capabilities": {
    "network_access": false,
    "repository_access": true,
    "source_fetch_access": false
  },
  "input_artifact_hashes": [
    "sha256:<artifact-1>",
    "sha256:<artifact-2>"
  ]
}
```

Hash rule:

```text
session_hash = sha256(JCS(canonical_session_context))
```

---

## Required Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `receipt_type` | Yes | Identifies the artifact as a refusal proof. |
| `schema_version` | Yes | Binds the receipt to a stable schema. |
| `receipt_id` | Yes | Hash of the canonical receipt payload. |
| `claim_id` | Yes | Hash of the canonical claim text and declared source metadata. |
| `claim_text` | Yes | Bounded natural-language claim under review. |
| `admission_status` | Yes | Must be `REFUSED` or `PENDING_VERIFICATION` for non-admitted claims. |
| `refusal_code` | Yes | Machine-readable refusal reason. |
| `refusal_reason` | Yes | Human-readable explanation of the failed check. |
| `source_uri` | Conditional | Required when the candidate claim declared a source. |
| `source_content_hash` | Conditional | Required only when source content was retrieved. |
| `parent_artifact_hash` | Yes | Binds refusal to the artifact or session that proposed the claim. |
| `verifier` | Yes | Names the verifier implementation. |
| `issued_at` | Yes | UTC timestamp of refusal emission. |
| `invariant` | Yes | Embeds the Layer A / Layer B boundary. |

---

## Refusal Codes

```text
SOURCE_MISSING
SOURCE_UNREACHABLE
SOURCE_NON_AUTHORITATIVE
CONTENT_MISMATCH
HASH_MISMATCH
LINEAGE_BREAK
SEMANTIC_OVERREACH
CONFLICTING_SOURCE
TEMPORAL_AMBIGUITY
LAYER_B_IMPERSONATION
VERIFIER_CAPABILITY_LIMIT
MALFORMED_RECORD
```

---

## Hashing Rule

The `receipt_id` is computed over the canonical receipt payload with the
`receipt_id` field omitted.

Minimum canonicalization requirement:

1. Sort object keys deterministically.
2. Normalize Unicode to NFC.
3. Strip transport-only metadata.
4. Preserve semantic whitespace inside `claim_text` and `refusal_reason`.
5. Encode as UTF-8.
6. Hash with SHA-256.

Recommended canonicalization profile: RFC 8785 JSON Canonicalization Scheme
(JCS), unless superseded by a TAS-specific canonicalization profile.

---

## Quarantine Example: GPT-5.5 / "Spud" Claims

A model-generated claim such as:

> "OpenAI released GPT-5.5 on April 23, 2026."

must remain outside Layer A unless the verifier resolves an authoritative source,
canonicalizes the source content, hashes it, and confirms that the bounded claim
is supported by the source.

If the verifier has no browsing or source-resolution capability in the current
session, the proper state is:

```json
{
  "admission_status": "PENDING_VERIFICATION",
  "refusal_code": "VERIFIER_CAPABILITY_LIMIT",
  "refusal_reason": "The verifier cannot resolve the declared primary source in this session; the claim is quarantined and cannot be sealed."
}
```

If the source resolves but fails to support the claim, the proper state is
`REFUSED` with `CONTENT_MISMATCH` or `SEMANTIC_OVERREACH`.

---

## Relation to Sovereign Innovation Axioms

This schema operationalizes:

- **Axiom I — Origin Integrity:** every refusal declares the origin of the candidate claim.
- **Axiom II — The Invariant Triple:** Form, Function, and Faithfulness are checked before admission.
- **Axiom III — Refusal as Proof:** invalid or unverifiable claims are preserved as first-class proof artifacts.
- **Axiom V — Process Over State:** a claim is judged by its verification trajectory, not by its surface fluency.

---

## One-Sentence Distillation

> **A sovereign substrate proves not only what it admits, but what it refuses to admit.**

---

*Signed: Russell Nordland (Steward)*  
*TAS-KEY-OMEGA-999 | TrueAlphaSpiral Sovereign Runtime Authority*
