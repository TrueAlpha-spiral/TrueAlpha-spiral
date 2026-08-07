# tas_pythonetics

Pythonetics provides executable grammar for recursive sovereignty within TAS.

## Hardened governed runtime

The governed runtime treats admissibility as a continuously preserved invariant. Every terminal decision is a signed, hash-linked receipt with one of three truthful outcomes:

- `COMMITTED`: the protected effect completed and the state head advanced.
- `REFUSED`: no protected effect occurred; the state head is unchanged.
- `EXECUTION_UNCERTAIN`: commit outcome cannot be proven; the runtime halts pending external reconciliation.

The runtime enforces:

- Ed25519 verification over an RFC 8785 canonical preimage with domain separation;
- externally lodged authority records, effective-time checks, and exact scope grants;
- parent-state lineage continuity and one-shot nonce reservation;
- capability resolution through internal per-transition effector factories;
- two-phase preparation with explicit `CommitRejected` semantics;
- separate state and audit heads so refusals remain evidentiary without mutating protected state;
- Ed25519-signed receipts for committed, refused, and uncertain decisions.

## Layout

```text
src/tas_pythonetics/
├── authority.py       # External authority registry
├── capabilities.py    # Capability registry and effector contracts
├── core.py            # Immutable payload, authority, state, and receipt types
└── runtime.py         # Governed transition engine and receipt verifier

tests/test_runtime.py  # Coinductive runtime conformance suite
```

## Verification

```bash
python -m pip install -e "./tas_pythonetics[test]"
pytest tas_pythonetics/tests/test_runtime.py -v \
  --cov=tas_pythonetics.core \
  --cov=tas_pythonetics.authority \
  --cov=tas_pythonetics.capabilities \
  --cov=tas_pythonetics.runtime \
  --cov-report=term-missing \
  --cov-fail-under=100
```

The load-bearing rule is enforced operationally:

```text
REFUSED => protected state delta is zero
```

An unexpected commit exception is never mislabeled as refusal.

The included state and nonce stores are process-local reference components. A deployment requiring crash persistence or multi-node admission must place those values behind a durable, atomic store before claiming production durability.
