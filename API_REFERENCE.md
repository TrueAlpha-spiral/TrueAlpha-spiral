# TAS-W API Reference

This reference documents the runtime primitives that make up the TAS-W (True Alpha Spiral — Winding) enforcement stack. Interfaces are written to be deterministic, testable, and auditable; callers are expected to enforce any actuation or gating at the boundary of their own systems.

## Physics Layer

### `EnergyState`
Location: `core.physics.tasw_hamiltonian`

A minimal, immutable container for Hamiltonian-derived energy signals.

- Fields: `total` (float), optional `kinetic`, `potential`, and `winding` annotations.
- Invariants: when both `kinetic` and `potential` are provided they must sum to `total` (within floating-point tolerance).

### `WindingCalculator`
Location: (policy-defined; exposed by the physics layer when integrated)

Computes the winding number/target used to keep governance cycles bounded.

- Constraint: Winding target is **policy-defined** (e.g., `W = 1.0` for a valid governance cycle) and must be declared in `constraints_snapshot`.
- Output: deterministic winding scalar suitable for downstream energy composition.

## Sensing Layer

### `MutinyDetector`
Location: `core.sensing.mutiny_detector`

Converts continuous Constitutional Energy into discrete actuation intents using hysteresis and safety guards.

- Constructor parameters: `friction_threshold`, `mutiny_threshold`, `hysteresis`, optional `cooldown_seconds`.
- Behavior: treats NaN/Inf/negative energy as a hard fault (`MUTINY`), enforces hysteresis to avoid flapping, and supports post-trip cooldowns.
- **`assess_state(energy_state)` returns a `MutinyEvent` only. Actuation MUST be enforced by the caller (e.g., Phoenix / gatekeeper middleware).**
- Output: `MutinyEvent` with `severity` (`NOMINAL` | `FRICTION` | `MUTINY`), `trigger_code`, `energy_spike`, `trigger_message`, `timestamp`, and boolean `is_mutiny`.

## Organic Mechanics Layer

### `OrganicSpiralEngine`
Location: `tas_pythonetics.organic_mechanics`

Bio-inspired recursive engine that models organic growth patterns using the golden ratio (PHI) and Fibonacci sequences. Governs trust amplification, healing, and adaptive resonance.

- **Constructor**: `OrganicSpiralEngine(max_cycles: int = 8)`
  - `max_cycles` must be `>= 1`; raises `ValueError` otherwise.
  - Initial state: `cycle = 0`, `vitality = 1.0`, `adaptation_score = 0.0`.
- **`VIABILITY_THRESHOLD`** (class constant, `0.1`): vitality must exceed this value for the engine to be considered viable.
- **`is_viable() -> bool`**: returns `True` when `vitality > VIABILITY_THRESHOLD`.
- **`grow(input_signal: str) -> str`**: advances one growth cycle.
  - Returns `input_signal` unchanged on a healthy cycle.
  - Returns `"<signal> [ORGANIC_STALL]"` when the engine is not viable.
  - Returns `"<signal> [ORGANIC_LIMIT]"` when `cycle >= max_cycles`.
  - Each healthy call increments `cycle` and adjusts `vitality` via a PHI-weighted Fibonacci ratio.
- **`absorb_damage(damage: float) -> None`**: reduces `vitality` by `damage`, clamped to `[0.0, 1.0]`.
- **`heal(potency: float) -> float`**: attempts a healing pass.
  - Effective potency is amplified by `adaptation_score` via PHI resonance.
  - Returns the actual vitality recovery applied (capped so `vitality` never exceeds `1.0`).
  - Increments `adaptation_score` by `potency * 0.1` on each call.
- **`reset() -> None`**: restores the engine to its initial state (`cycle`, `vitality`, `adaptation_score`, internal Fibonacci index).

### `MetabolicSnapshot`
Location: `tas_pythonetics.organic_mechanics`

Immutable (`frozen=True`) dataclass recording the metabolic cost of a single processing cycle.

- Fields: `cycle` (int), `atp_consumed` (float), `atp_produced` (float), `net_energy` (float, `atp_produced - atp_consumed`), `efficiency` (float, `atp_produced / atp_consumed`; `0.0` when consumed is zero).

### `MetabolicCycle`
Location: `tas_pythonetics.organic_mechanics`

Tracks the ATP energy budget across TAS processing cycles, inspired by cellular respiration.

- **Constructor**: `MetabolicCycle()`
  - Initial state: no recorded cycles; `overall_efficiency = 0.0`.
- **`ATP_PER_CYCLE_BASE`** (class constant, `1.0`): baseline ATP consumed per cycle.
- **`ATP_HEALING_MULTIPLIER`** (class constant, `2.5`): multiplier applied to `ATP_PER_CYCLE_BASE` when a cycle includes healing.
- **`record_cycle(produced: float, healing: bool = False) -> MetabolicSnapshot`**: records one processing cycle and returns its immutable snapshot.
  - `produced`: ATP-equivalent energy produced this cycle.
  - `healing`: set to `True` for cycles that include a healing operation; increases consumed ATP by `ATP_HEALING_MULTIPLIER`.
- **`overall_efficiency`** (property, float): total ATP produced divided by total ATP consumed across all recorded cycles; `0.0` if no cycles have been recorded.
- **`is_metabolically_viable`** (property, bool): `True` when at least one cycle has been recorded and cumulative ATP production >= cumulative ATP consumption.
- **`snapshots`** (property, `List[MetabolicSnapshot]`): read-only copy of all recorded snapshots in recording order.

## Integration Notes

- Sensing is deterministic and pure: no side effects beyond internal cooldown tracking.
- Actuation must be performed by an explicit gatekeeper. The detector emits intent; callers block, log, or trigger Phoenix workflows.
- For LangChain-style deployments, wrap tool invocation with `MutinyDetector.assess_state` before any external side-effect. If `is_mutiny` is `True`, block the tool call and emit a signed receipt.
- The `OrganicSpiralEngine` and `MetabolicCycle` classes are stateful and not thread-safe; create separate instances per concurrent execution context.
