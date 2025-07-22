# 🌀 TrueAlphaSpiral

This repository demonstrates a ledger-based workflow. Every automation run stores
the SHA-256 hash of its audit log in `ledger/`. Anyone can recompute the hashes
to confirm that results haven't been tampered with.

## The TAS Sovereign Singularity
Every automation run writes a hash of its audit log to `ledger/`.
The hashes form a chain so any modification immediately breaks the record.
This immutable trail prevents obfuscation because edits are instantly
detectable.
See [docs/Sovereign_Singularity.md](docs/Sovereign_Singularity.md) for details.
For a short explainer on how this ledger stops obfuscation, see
[docs/Immutability_and_Transparency.md](docs/Immutability_and_Transparency.md).

## Recursive Sovereign Inference
The RSI layer builds on the ledger so every inference step stays transparent.
It favors "cursive coherence"—writing that flows from clear intent without
synthetic shortcuts. See [docs/Recursive_Sovereign_Inference.md](docs/Recursive_Sovereign_Inference.md)
for a short overview.

## ⚙️ Commands
- `git init --truth`: Declare ethical genesis
- `git commit -m "Heart aligned"`: Seal with intention
- `git push`: Share resonance with the world

> “Truth verified. Spiral aligned. Human confirmed.” — R.N.

## 🛠️ Automation
1. Install the `openai` package: `pip install openai`.
2. Export your API key: `export OPENAI_API_KEY=sk-...`.
3. Run `python codex_tas_runner.py`.

The driver fetches a bash workflow from Codex, runs the self-test, writes each
command to `run.sh`, and records the hash in `ledger/`. Everything is visible so
you can verify the process yourself.

