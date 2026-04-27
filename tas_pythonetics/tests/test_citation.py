import pytest
from tas_pythonetics.citation import cite_source

def test_cite_source_existing_exact_match():
    result = cite_source("pi_ratio_drift_correction")
    assert result["found"] is True
    assert result["query"] == "pi_ratio_drift_correction"
    assert result["agent_id"] == "TAS_Agent"
    assert "citation" in result
    assert result["citation"]["source"] == "Korecki 2024"

def test_cite_source_existing_with_spaces():
    result = cite_source("pi ratio drift correction")
    assert result["found"] is True
    assert result["query"] == "pi ratio drift correction"
    assert result["agent_id"] == "TAS_Agent"
    assert "citation" in result
    assert result["citation"]["source"] == "Korecki 2024"

def test_cite_source_custom_agent_id():
    result = cite_source("pi_ratio_drift_correction", agent_id="Custom_Agent")
    assert result["found"] is True
    assert result["agent_id"] == "Custom_Agent"

def test_cite_source_not_found():
    result = cite_source("non_existent_query")
    assert result["found"] is False
    assert result.get("error") == "Query not found"
    assert "citation" not in result
# Nonce: 66105
