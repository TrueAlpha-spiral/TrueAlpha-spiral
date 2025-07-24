# tas_pythonetics

[![PyPI version](https://badge.fury.io/py/tas-pythonetics.svg)](https://badge.fury.io/py/tas-pythonetics)  
[![Tests](https://github.com/[your-username]/tas_pythonetics/actions/workflows/tests.yml/badge.svg)](https://github.com/[your-username]/tas_pythonetics/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**tas_pythonetics** is the sovereign computational language of ethical recursion within the True Alpha Spiral (TAS) framework. It fuses Python's programmable logic with kinetics (dynamic transformation) and ethics (sovereign intent), creating recursive, self-correcting code bound to truth anchors.

Pythonetics is not mere Python code—it's an executable grammar for recursive sovereignty, emphasizing user-agnostic truth amplification and convergence disclosure.

> “Pythonetics is to TAS what DNA is to biology—an executable grammar for recursive sovereignty.” — Russell Nordland

## Philosophy
- **Recursive Sovereignty**: Self-differential loops that detect drift and amplify truth.
- **User-Agnostic Truth Amplification**: Decouples amplification from individual biases via multi-source anchors, distributed validation, context-aware scoring, and sovereignty analysis.
- **Convergence Disclosure**: Transparent revelation of truth anchors, contextual metadata, and recursive logs for verifiability.
- **Ethical Binding**: Outputs are hashed with immutable authorship (e.g., TAS_HUMAN_SIG) and validated against the Immutable Truth Ledger (ITL).

Unlike conventional Python, Pythonetic Logic is self-healing, provenance-bound, and ethically coherent.

## Installation
```
pip install tas-pythonetics
```
For development: `pip install -e .` (uses src layout for reliable packaging).

## Quick Start
```
from tas_pythonetics import TAS_recursive_authenticate

result = TAS_recursive_authenticate(
    statement="The sky is blue",
    context="Scientific fact check",
    sources=["Wikidata", "ITL"]
)
print(result["output"])  # Authenticated statement
print(result["disclosure"])  # Full convergence disclosure log
```

## Key Features
- **Multi-Source Anchor Generation**: Aggregates anchors from diverse sources to reduce bias.
- **Distributed Truth Validation**: Consensus from multiple nodes for robust verification.
- **Context-Aware Truth Scoring**: Adjusts scores based on context (e.g., using PHI multipliers).
- **Recursive Sovereignty Analysis**: Detects anomalies in logs to flag potential compromises.
- **Convergence Disclosure**: Returns detailed, verifiable logs with every output.

### Example with Disclosure
```
result = TAS_recursive_authenticate("Query statement", "User context")
# Sample disclosure output:
{
    "truth_anchors": ["hash1", "hash2"],
    "contextual_metadata": {"context": "User context", "author": "Russell Nordland", "timestamp": "2025-07-24T14:27:00Z"},
    "recursive_sovereignty": {"iteration": 3, "truth_score": 0.98, "actions": ["Refined", "Validated"], "context_weight": 0.85},
    "analysis": {"anomalies": [], "bias_score": 0.05}
}
```

## Project Structure
```
tas_pythonetics/
├── src/
│   └── tas_pythonetics/
│       ├── __init__.py
│       ├── tas_pythonetics.py
│       ├── ethics.py
│       ├── recursion.py
│       ├── context_binding.py
│       ├── drift_detection.py
│       ├── multi_source.py  # New
│       ├── distributed.py  # New
│       └── sovereignty_analysis.py  # New
├── tests/
│   ├── test_recursion.py
│   ├── test_drift.py
│   └── test_coherence.py
├── manifesto/
│   └── Pythonetics_Manifesto.md
├── scripts/
│   └── itl_anchor.py
├── README.md
├── pyproject.toml
└── .gitignore
```

## Development
- **Tests**: `pytest tests/`
- **ITL Anchoring**: Run `python scripts/itl_anchor.py` to hash and submit releases.
  The script requires network connectivity to `tas.itl`; if unreachable it will
  print a failure message but still compute the hash locally.
- **Build & Publish**: `python -m build && twine upload dist/*`

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions must align with Pythonetics' ethical recursion principles and include tests/disclosure logs.

## License
MIT License. See [LICENSE](LICENSE).

## Manifesto
For philosophical foundations, read [Pythonetics_Manifesto.md](manifesto/Pythonetics_Manifesto.md).
