# Security Expectations for TAS-W Deployments

Non-negotiable controls for any deployment or pilot integration:

- **Receipts are mandatory:** Every `MutinyDetector` assessment and subsequent actuation (allow/block) must emit a signed receipt with a hash of `constraints_snapshot`, energy inputs, and decision.
- **Signature and anchoring:** Receipts must include a human/operator signature (`TAS_HUMAN_SIG`) and be anchored to an immutable log (e.g., ITL/ledger) to prevent repudiation.
- **Phoenix trigger points:** Any `MUTINY` decision, invalid energy (`NaN`/`Inf`/negative), or cooldown-enforced refusal must trigger Phoenix containment (block actuation, alert operators, require explicit re-authorization).
- **Threshold provenance:** Thresholds (`friction_threshold`, `mutiny_threshold`, `hysteresis`, `cooldown_seconds`) and winding targets are policy artifacts and must be versioned alongside the code that uses them.
- **Determinism:** The sensing layer is deterministic; randomness in enforcement paths is prohibited. All variance must be accounted for in the energy model, not in gatekeeping.
