import pytest
from tas_pythonetics.citation import cite_source, MOCK_REGISTRY

def test_cite_source_exact_match():
    # Test finding a citation exactly matching the ID
    result = cite_source("pi_ratio_drift_correction")
    assert result["found"] is True
    assert result["agent_id"] == "TAS_Agent"
    assert result["query"] == "pi_ratio_drift_correction"
    assert result["citation"]["source"] == "Korecki 2024"

def test_cite_source_with_spaces():
    # Test finding a citation with spaces replaced by underscores
    result = cite_source("pi ratio drift correction")
    assert result["found"] is True
    assert result["query"] == "pi ratio drift correction"
    assert result["citation"]["tx_id"] == "vc_9f4g5b0c"

def test_cite_source_custom_agent():
    # Test setting a custom agent_id
    result = cite_source("pi_ratio_drift_correction", agent_id="Custom_Agent")
    assert result["found"] is True
    assert result["agent_id"] == "Custom_Agent"

def test_cite_source_not_found():
    # Test the not found case
    result = cite_source("non_existent_citation")
    assert result["found"] is False
    assert result["error"] == "Query not found"
    assert "citation" not in result
# Nonce: 29241
