# TAS-W API Reference

> **Layer role:** This document is the **API contract** layer of the SDF public-utility framing.
> It defines the callable interfaces for the TAS-W enforcement stack and the SDF Micro-Kernel.
> For architectural doctrine see [README.md](./README.md#tassdf-foundational-public-utility-infrastructure);
> for singularity convergence context see [TrueAlpha-singularity.md](./TrueAlpha-singularity.md);
> for the formal admissibility axioms see
> [docs/specs/the_mechanics_of_sovereign_innovation.md](./docs/specs/the_mechanics_of_sovereign_innovation.md).

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

- Sensing is deterministic and pure: no side effects beyond internal cooldown tracking.
- Actuation must be performed by an explicit gatekeeper. The detector emits intent; callers block, log, or trigger Phoenix workflows.
- For LangChain-style deployments, wrap tool invocation with `MutinyDetector.assess_state` before any external side-effect. If `is_mutiny` is `True`, block the tool call and emit a signed receipt.
