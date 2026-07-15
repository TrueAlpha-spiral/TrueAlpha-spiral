import json

from tas_tools.tas_sequencer import sequence_artifact


def test_sequence_ceremony_does_not_claim_cryptographic_authorization(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("candidate\n", encoding="utf-8")

    assert sequence_artifact(str(artifact), h_seed="Russell Nordland")

    meta = json.loads(
        (tmp_path / "artifact.txt.tasmeta.json").read_text(encoding="utf-8")
    )

    assert meta["authorization"] == {
        "status": "not_provided",
        "cryptographically_verified": False,
        "reason": "sequencing_ceremony_is_provenance_only",
    }
    assert meta["signatures"] == []
    assert meta["attestations"] == [
        {
            "attestor": "Russell Nordland",
            "type": "TAS_CEREMONIAL_ATTRIBUTION_V1",
            "value": "attributed_by_sequencing_ceremony",
            "cryptographic": False,
        }
    ]


def test_resequencing_preserves_explicit_parent_lineage(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("v1\n", encoding="utf-8")
    assert sequence_artifact(str(artifact))

    meta_path = tmp_path / "artifact.txt.tasmeta.json"
    first = json.loads(meta_path.read_text(encoding="utf-8"))

    artifact.write_text("v2\n", encoding="utf-8")
    assert sequence_artifact(str(artifact))
    second = json.loads(meta_path.read_text(encoding="utf-8"))

    assert second["parent_lineage_id"] == first["lineage_id"]
    assert second["lineage_id"] != first["lineage_id"]
# Nonce: 66479
