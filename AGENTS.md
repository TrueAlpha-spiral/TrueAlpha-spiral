# Testing Instructions
Run tests with `PYTHONPATH=$(pwd)/tas_pythonetics/src:$(pwd)/tas-recursion-conversion:$(pwd) pytest`

## Jules (Google) Agent Guidance

Jules is a Google autonomous coding agent that operates directly on GitHub repositories.
The following guidance applies when Jules is assigned a task in this repo.

### Test Command
```
PYTHONPATH=$(pwd)/tas_pythonetics/src:$(pwd)/tas-recursion-conversion:$(pwd) pytest -q
```
Jules must run this command after every change to confirm no regressions.

### Safe-to-Edit Paths
- `tas_pythonetics/`
- `tas-recursion-conversion/`
- `tas_openai_bridge/`
- `scripts/`
- `tests/`
- `docs/`
- `core/`

### Locked Files — Do Not Modify Without Human Approval
- `README.md`
- `AGENTS.md`
- `valid_identity.txt`
- `LICENSE_RIDER.txt`
- `TAS_GENOME_ANCHOR.json`
- `citation.bib`
- `tas_1st_principles.yaml`
- `DAY_ONE_STEWARD_DIRECTIVE.md`

### Bridge Contract
All agents (Jules, Copilot, Replit) share a single source of truth at
[`bridge_config.yaml`](./bridge_config.yaml). Read it before beginning any task
to understand entry points, locked files, permitted scopes, and the canonical
test command.

### CI Gate
Every pull request from Jules must pass both jobs in
`.github/workflows/bridge-sync.yml`:
1. `validate-bridge-config` — confirms `bridge_config.yaml` is valid
2. `run-tests` — confirms the full test suite passes
