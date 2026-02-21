import json
import os
import sys

# Simplified mock registry for the package, so we don't depend on external files for the basic logic
MOCK_REGISTRY = {
    "citations": [
        {
            "id": "pi_ratio_drift_correction",
            "sha256": "9a3f4e2...",
            "source": "Korecki 2024",
            "summary": "Biospheric AI coherence confirmed; Δπ drift < 0.01",
            "tx_id": "vc_9f4g5b0c"
        }
    ]
}

def cite_source(query: str, agent_id: str = "TAS_Agent") -> dict:
    """
    Search for a citation in the registry based on the query.
    """
    citations = {c["id"]: c for c in MOCK_REGISTRY["citations"]}
    key = query.replace(" ", "_")

    if key in citations:
        entry = citations[key]
        return {
            "found": True,
            "agent_id": agent_id,
            "query": query,
            "citation": {
                "source": entry.get("source"),
                "summary": entry.get("summary"),
                "tx_id": entry.get("tx_id")
            }
        }
    return {"found": False, "error": "Query not found"}
