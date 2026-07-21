"""Structural regression tests for the TAS v1 Ed25519 conformance artifacts."""

import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPOSITORY_ROOT / "tas-conformance-v1.json"
VECTORS_PATH = (
    REPOSITORY_ROOT / "conformance-tests" / "signatures" / "vectors_v1_ed25519.json"
)
ERROR_CODES_PATH = REPOSITORY_ROOT / "conformance-tests" / "error_codes_v1.json"


def _load_json(path: Path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def test_manifest_lists_signature_vectors_once_and_preserves_their_order():
    manifest = _load_json(MANIFEST_PATH)
    vectors = _load_json(VECTORS_PATH)

    vector_ids = [vector["vector_id"] for vector in vectors]
    assert manifest["suite_id"] == "tas-conformance-v1"
    assert manifest["protocol_version"] == "tas-v1"
    assert manifest["canonicalization"] == "RFC8785-JCS"
    assert manifest["signature_algorithm"] == "Ed25519"
    assert manifest["signature_specification"] == "RFC8032"
    assert manifest["vectors"][: len(vector_ids)] == vector_ids
    assert len(vector_ids) == len(set(vector_ids))


def test_valid_vector_has_the_specified_ed25519_byte_lengths_and_preimage():
    vectors = _load_json(VECTORS_PATH)
    valid_vectors = [v for v in vectors if v.get("expected_result") == "ACCEPT"]
    assert len(valid_vectors) == 1, "Should have exactly one valid vector"
    valid_vector = valid_vectors[0]

    header = bytes.fromhex(valid_vector["domain"]["header_hex"])
    canonical_message = bytes.fromhex(valid_vector["expected_canonical_message_hex"])
    expected_canonical_message = json.dumps(
        valid_vector["input"],
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    assert valid_vector["expected_result"] == "ACCEPT"
    assert len(bytes.fromhex(valid_vector["private_key_seed_hex"])) == 32
    assert len(bytes.fromhex(valid_vector["public_key_hex"])) == 32
    assert len(bytes.fromhex(valid_vector["expected_signature_hex"])) == 64
    assert canonical_message == expected_canonical_message
    assert bytes.fromhex(valid_vector["expected_signing_preimage_hex"]) == (
        header + canonical_message
    )


def test_rejection_vectors_reference_registered_errors_and_the_valid_base_vector():
    vectors = _load_json(VECTORS_PATH)
    error_codes = _load_json(ERROR_CODES_PATH)["errors"]
    vector_ids = {vector["vector_id"] for vector in vectors}

    rejection_vectors = [v for v in vectors if v.get("expected_result") == "REJECT"]
    assert len(rejection_vectors) > 0, "Should have at least one rejection vector"
    for vector in rejection_vectors:
        assert vector["base_vector"] in vector_ids
        assert vector["expected_error"] in error_codes
        assert vector["expected_failure_stage"]


def test_noncanonical_vector_is_valid_json_with_insignificant_whitespace():
    noncanonical_vector = _load_json(VECTORS_PATH)[-1]
    raw_input = bytes.fromhex(noncanonical_vector["raw_input_override_hex"])

    assert json.loads(raw_input) == {"nonce": 42}
    assert raw_input != json.dumps(
        {"nonce": 42}, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
