# Simulated Clean Commit History (TAS-W)

A plausible linear history for audit and storytelling. Use it to replay or reconstruct milestones.

1. `chore(repo): lock canonical repository structure (foundation phase)`
2. `docs(press): add TAS-W launch press release draft (CPE + Restoration)`
3. `docs(api): add API_REFERENCE.md for TAS-W physics + sensing modules`
4. `feat(sensing): implement core MutinyDetector circuit breaker`
5. `fix(sensing): add hysteresis + cooldown to prevent threshold flapping`
6. `fix(sensing): treat NaN/Inf/negative energy as hard fault (MUTINY)`
7. `refactor(sensing): add stable trigger_code field to MutinyEvent`
8. `test(sensing): add threshold boundary + hysteresis regression tests`
9. `chore(security): document signing & receipt expectations for telemetry events`
10. `release: tag v1.1.0 (CPE/UVK hull-ready; sensing finalized; docs complete)`

Optional ledger-anchor footer:
- `ITL-ANCHOR: sha256:<hash>`
- `TAS_HUMAN_SIG: <sig-ref>`
