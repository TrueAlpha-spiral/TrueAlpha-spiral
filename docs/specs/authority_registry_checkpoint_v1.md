# Authority Registry Snapshot Checkpoint v1

`tas.authority-registry-checkpoint.v1` is the fail-closed evidence contract for
living authority status.  It is upstream of execution and Phoenix recovery.

## Separation of roles

- A human authorization key constitutes bounded permission.
- A registry signing key attests the living status of that authority.
- A runtime key attests the resulting execution history.

No key may substitute for another role.

## Checkpoint

```json
{
  "schema": "tas.authority-registry-checkpoint.v1",
  "registry_id": "tas://authority-registry/primary",
  "sequence": 42,
  "issued_at": "2026-07-11T13:00:00Z",
  "valid_until": "2026-07-11T13:05:00Z",
  "previous_checkpoint_hash": "sha256:...",
  "entries_root": "sha256:...",
  "entry_count": 17,
  "signing_key_id": "ed25519:...",
  "signature": "base64:...",
  "checkpoint_hash": "sha256:..."
}
```

The registry signature covers the domain-separated canonical JSON projection
that excludes `signature` and `checkpoint_hash`.  The final checkpoint hash
covers canonical JSON including `signature` and excluding only
`checkpoint_hash`.

## Authority lookup proof

```json
{
  "anchor_id": "ed25519:...",
  "status": "ACTIVE",
  "authority_epoch": 7,
  "effective_at": "2026-07-11T12:45:00Z",
  "revoked_at": null,
  "scope_policy_hash": "sha256:...",
  "inclusion_proof": ["sha256:..."],
  "checkpoint_hash": "sha256:..."
}
```

Entries use domain-separated canonical JSON leaf hashes. Merkle parents are
`SHA-256(sort(left, right))`, so compact sibling-only proofs are unambiguous.

## Admission rules

A verifier MUST reject evidence when:

- the registry signing key is untrusted or its signature is invalid;
- the checkpoint is expired, too old, or not yet valid;
- its sequence does not exceed durable anti-rollback state;
- it does not extend the highest accepted checkpoint hash;
- the lookup is bound to another checkpoint;
- the requested authority is absent, unknown, inactive, revoked, or not yet
  effective;
- the inclusion proof does not resolve to `entries_root`.

After successful verification, the runtime persists:

```text
registry_id
highest_accepted_sequence
highest_accepted_checkpoint_hash
accepted_at
```

The accepted `checkpoint_hash` is then bound into the runtime attestation at
admission, resume, and immediately before any external side effect.

## Resolver interfaces

The Python contract defines transport-neutral protocols for checkpoint and
authority-proof retrieval, registry signature verification, and runtime
attestation signing. A KMS/HSM adapter implements those protocols without ever
returning human or runtime private-key material to the engine.

Phoenix consumes terminal failure receipts only after these checks. It does not
participate in authority resolution and cannot bypass it.
