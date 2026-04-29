import pytest
import json
import base64
import zlib
from tas_hccc import CursiveCoherenceEngine, PolicyAnchor, Cell

def test_attest_creates_compressed_payload():
    # Setup test anchors ensuring TAS-SES constraints (>=1 A_C, >=2 S_C)
    anchors = [
        PolicyAnchor("ref1", "A_C", "ac1"),
        PolicyAnchor("ref2", "S_C", "sc1"),
        PolicyAnchor("ref3", "S_C", "sc2"),
    ]
    engine = CursiveCoherenceEngine("anchor1", anchors, weights=(1.0, 1.0, 1.0, 1.0))

    # Call attest
    cell = engine.attest(
        status="OK",
        entailment=0.9,
        trust=0.8,
        lineage=0.7,
        contradiction=0.1
    )

    # Verify return type
    assert isinstance(cell, Cell)

    # Verify timestamp exists
    assert cell.timestamp is not None
    assert len(cell.timestamp) > 0

    # Verify payload format
    assert "encoding" in cell.payload
    assert cell.payload["encoding"] == "b64zlib"
    assert "data" in cell.payload

    # Verify payload can be decompressed and decoded
    decoded = base64.b64decode(cell.payload["data"])
    decompressed = zlib.decompress(decoded)
    payload_dict = json.loads(decompressed.decode())

    # Verify payload contents
    assert payload_dict["status"] == "OK"
    assert payload_dict["policy_anchor"] == "anchor1"
    assert payload_dict["mgi_status"] == "pending"
    assert len(payload_dict["anchors"]) == 3
    assert payload_dict["anchors"][0]["ref"] == "ref1"

    # Verify metrics
    metrics = payload_dict["metrics"]
    assert metrics["entailment"] == 0.9
    assert metrics["source_trust"] == 0.8
    assert metrics["lineage_integrity"] == 0.7
    assert metrics["contradiction_mass"] == 0.1

    # Verify phi calculation matches coherence method
    expected_phi = engine.coherence(0.9, 0.8, 0.7, 0.1)
    assert metrics["phi"] == expected_phi
