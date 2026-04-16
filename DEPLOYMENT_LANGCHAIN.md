# LangChain Deployment Fit for TAS-W

This document shows how to wrap LangChain agents with TAS-W enforcement without changing LangChain internals.

## Pattern Overview
1. Let LangChain produce candidate actions as usual (LLM reasoning + tool selection).
2. Before any tool call or side effect:
   - Compute the `EnergyState` for the candidate action (include winding target/constraints in the snapshot).
   - Run `MutinyDetector.assess_state` on that energy.
   - If the result is `MUTINY`, block actuation and emit a signed receipt (Phoenix / gatekeeper).
   - Otherwise, execute the tool and log the receipt.
3. Use callbacks for telemetry, but keep enforcement in the pre-tool boundary.

## Where to Hook
- **Tool invocation wrapper (recommended):** wrap `Tool.run()` or the router that dispatches tool calls.
- **Agent executor layer:** intercept `agent_action` before execution.
- **Callbacks:** `on_tool_start`/`on_tool_end` for receipts; enforcement must occur before the call.

## Minimal Pseudocode
```python
from core.physics.tasw_hamiltonian import EnergyState
from core.sensing.mutiny_detector import MutinyDetector

mutiny = MutinyDetector(
    friction_threshold=1000.0,
    mutiny_threshold=5000.0,
    hysteresis=0.1,
    cooldown_seconds=5.0,
)


def enforce_then_run(tool, tool_input, constraints_snapshot):
    energy = compute_constitutional_energy(tool, tool_input, constraints_snapshot)
    event = mutiny.assess_state(EnergyState(total=energy.total, winding=energy.winding))

    if event.is_mutiny:
        record_receipt(event, constraints_snapshot)
        raise RuntimeError("Phoenix block: actuation refused")

    record_receipt(event, constraints_snapshot)
    return tool.run(tool_input)
```

## Operational Notes
- Receipts should be signed and anchored (ITL or equivalent) to preserve auditability.
- Cooldown is optional; enable it for high-risk tools to prevent immediate re-entry after a trip.
- Thresholds and winding targets are policy-defined; document them alongside the chain configuration.
