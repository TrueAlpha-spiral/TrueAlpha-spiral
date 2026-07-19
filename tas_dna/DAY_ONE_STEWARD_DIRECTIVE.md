# Day One Steward Directive

When legacy systems converge under stress, provenance still matters.

**PR #106 is historical substrate.** It has already been merged and is no longer
the Day One gate. The operating boundary for Day One is now the
release-docker / sovereign-intent / receipt-emission process run against the
**current PR head SHA**.

The operating boundary remains deterministic and fail-closed:

1. Do **not** treat a merged PR as a completed gate.
2. Confirm that `README.md` exists on the `main` branch before treating the
   doctrine layer as available for promotion.
3. Emit the doctrine receipt with `scripts/day-one-payload-steward.py`.
4. Run the deterministic release gate (`release-docker.yaml` when available;
   `blank.yml` is the current verification workflow) against the **active head SHA**
   through an explicit human-triggered path.
5. Require sovereign-intent verification (signature, payload hash, nonce, TTL,
   scope, revocation, invariants, witness policy).
6. Emit audit artifacts (PDR stream, refusal ledger, phoenix recovery log,
   null-space manifest, ledger anchor URI).
7. Merge and promote **only if** all checks pass; otherwise refuse and halt.

## Operator command (copy/paste)

```text
Day One Pilot Directive:
- PR #106 is merged; it is historical substrate, not the active gate.
- Confirm README.md exists on the `main` branch before promotion.
- Identify the active PR head SHA.
- Emit the doctrine receipt with `scripts/day-one-payload-steward.py`.
- Execute the release gate workflow (blank.yml / release-docker.yaml) against
  that SHA in proving-ground mode through explicit human intent.
- Enforce sovereign-intent verification and fail-closed policy.
- Emit PDR/refusal/phoenix/null-space/ledger receipts.
- Merge only on full pass; else deterministic refusal.
```

## Clean invariant

```text
A passing badge is not a receipt.
A merged PR is not sufficient proof.
A visible final state is not process equivalence.

Only the verified path admits the state.
```
