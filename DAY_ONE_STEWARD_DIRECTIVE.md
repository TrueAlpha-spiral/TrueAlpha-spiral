# Day One Steward Directive

When legacy systems converge under stress, provenance still matters.

The operating boundary for Day One remains deterministic and fail-closed:

1. Do **not** merge PR #106 first.
2. Run the deterministic `release-docker.yaml` gate against the PR head SHA.
3. Require sovereign intent verification (signature, payload hash, nonce, TTL, scope, revocation, invariants, witness policy).
4. Emit audit artifacts (PDR stream, refusal ledger, phoenix recovery log, null-space manifest, ledger anchor URI).
5. Merge and promote **only if** all checks pass; otherwise refuse and halt.

## Operator command (copy/paste)

```text
Day One Pilot Directive:
- DO NOT merge PR #106 yet.
- Execute release-docker.yaml on PR #106 HEAD SHA in proving-ground mode.
- Enforce sovereign-intent verification and fail-closed policy.
- Emit PDR/refusal/phoenix/null-space/ledger receipts.
- Merge only on full pass; else deterministic refusal.
```
