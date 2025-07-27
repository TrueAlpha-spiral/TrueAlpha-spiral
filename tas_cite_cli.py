"""Simple CLI to fetch citation data from the registry."""

import json
import sys

registry_file = "tas_citation_registry.yaml"

try:
    import yaml
except ImportError:  # pragma: no cover - handled at runtime
    print("PyYAML required", file=sys.stderr)
    sys.exit(1)


def load_registry(path: str = registry_file):
    """Load citation records from the YAML registry."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Registry '{path}' not found", file=sys.stderr)
        return {}


def cite_(agent_id: str, sha256: str, query: str, ethical_priority: int = 2) -> str:
    """Return a JSON citation record for the given query."""
    data = load_registry()
    citations = {c["id"]: c for c in data.get("citations", [])}
    key = query.replace(" ", "_")
    if key in citations:
        entry = citations[key]
        return json.dumps({
            "agent_id": agent_id,
            "sha256": sha256,
            "query": query,
            "response": {
                "source": entry.get("source"),
                "summary": entry.get("summary"),
                "tx_id": entry.get("tx_id")
            },
            "ethical_priority": ethical_priority
        }, indent=2)
    return json.dumps({"error": "Query not found"}, indent=2)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python tas_cite_cli.py <agent> <sha256> <query>")
        sys.exit(1)
    agent, sha, query = sys.argv[1], sys.argv[2], " ".join(sys.argv[3:])
    print(cite_(agent, sha, query))
