# PSVP State Machine & Neutral Scribe Consumption

## State Machine Summary
- **Initial**: `s_0` (genesis: DayZero hash committed)
- **States**: `s_t → s_tp1` where `H(s_tp1) <= H(s_t)`
- **Transitions**:

| From | To   | Guard |
| --- | --- | --- |
| s_t | s_tp1 | `spec_id preserved` AND `default_invariant(s_t, s_tp1)` AND `diff_drift(h_t, h_tp1)` |

- **Terminal**: fork detected (`ΔH > 0`) → silence (no bundle emitted)

## Scribe Consumption
1. Load PSVP YAML → extract `spec_id`, `axiom_set_hash`, `invariant_set_hash` → init `NeutralScribe`.
2. Propose `s_tp1` → `gate0_spec_integrity` enforces equality; apply `default_invariant` and `diff_drift`.
3. If admissible, emit bundle `{trace_id, s_tp1, proof}` for ITL/HCCC anchoring.
4. Replit test: `scribe(s_0, mock_s1)` verifies the ratchet clicks.

## Minimal Runnable Example
1. Use `psvp_example.yaml` as a template for the PSVP input.
2. Run the demo to emit a bundle:
   `python neutral_scribe_demo.py`
