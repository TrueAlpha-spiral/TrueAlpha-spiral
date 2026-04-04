import json
import hashlib
import sys

registry_file = "tas_citation_registry.yaml"

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(1)


def load_registry(path=registry_file):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def cite_(agent_id, sha256, query, ethical_priority=2):
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
