import copy
import decimal
import json
from datetime import datetime, timezone

import pytest

from tas_logos_gatekeeper import (
    HMACLineageResolver,
    HMACReceiptSigner,
    TASLogosGatekeeper,
    _serialize_canonical,
)


LINEAGE_KEY = b"L" * 32
RECEIPT_KEY = b"R" * 32
ZERO_HASH = "0" * 64


@pytest.fixture
def components():
    fixed_clock = lambda: datetime(2026, 7, 16, 12, 0, 0, tzinfo=timezone.utc)
    receipt_signer = HMACReceiptSigner("gatekeeper-test", RECEIPT_KEY)
    resolver = HMACLineageResolver({"steward_01": LINEAGE_KEY})
    gatekeeper = TASLogosGatekeeper(
        receipt_signer=receipt_signer,
        lineage_verifier=resolver.verify,
        clock=fixed_clock,
    )
    return gatekeeper, resolver, receipt_signer


def sign_payload(gatekeeper, resolver, payload):
    unsigned = copy.deepcopy(payload)
    authorization_hash = gatekeeper.compute_authorization_hash(unsigned)
    payload["lineage"]["signature"] = resolver.sign(payload, authorization_hash)
    return payload


def base_payload(value=42):
    return {
        "credential_id": "steward_01",
        "operation": "MUTATE_STATE",
        "state_delta": {"param_x": value},
        "lineage": {
            "parent_hash": ZERO_HASH,
            "history": [],
        },
    }


def test_syntactic_variation_has_same_candidate_hash(components):
    gatekeeper, resolver, receipt_signer = components
    payload = sign_payload(gatekeeper, resolver, base_payload())
    signature = payload["lineage"]["signature"]

    payload_a = f"""{{
        "credential_id": "steward_01",
        "operation": "MUTATE_STATE",
        "state_delta": {{"param_x": 42.0}},
        "lineage": {{
            "parent_hash": "{ZERO_HASH}",
            "signature": "{signature}",
            "history": []
        }}
    }}""".encode()

    payload_b = f"""{{
      "state_delta": {{"param_x": 42.00000}},
      "operation": "MUTATE_STATE",
      "lineage": {{
        "signature": "{signature}",
        "parent_hash": "{ZERO_HASH}",
        "history": []
      }},
      "credential_id": "steward_01"
    }}""".encode()

    result_a = gatekeeper.process_payload(payload_a)
    result_b = gatekeeper.process_payload(payload_b)

    assert result_a["state"] == "ADMITTED"
    assert result_b["state"] == "ADMITTED"
    assert result_a["candidate_hash"] == result_b["candidate_hash"]
    assert result_a["authorization_hash"] == result_b["authorization_hash"]
    assert result_a["receipt"]["raw_payload_hash"] != result_b["receipt"]["raw_payload_hash"]
    assert receipt_signer.verify(
        _serialize_canonical(result_a["receipt"]), result_a["receipt_signature"]
    )


def test_missing_signature_is_refused_without_short_circuit(components):
    gatekeeper, _, _ = components
    result = gatekeeper.process_payload(json.dumps(base_payload()).encode())

    assert result["state"] == "REFUSED"
    logs = result["receipt"]["rule_evaluation_logs"]
    assert [log["rule_id"] for log in logs] == [
        "INV_01_STRUCTURE",
        "INV_02_SIGNATURE",
        "INV_03_LINEAGE_LOOP",
        "INV_04_RESOURCE_BOUNDS",
    ]
    assert logs[1] == {
        "rule_id": "INV_02_SIGNATURE",
        "status": "FAILED",
        "detail_code": "LINEAGE_FIELDS_MISSING",
    }


def test_circular_lineage_is_refused(components):
    gatekeeper, resolver, _ = components
    parent = "a" * 64
    payload = base_payload(10)
    payload["lineage"]["parent_hash"] = parent
    payload["lineage"]["history"] = ["b" * 64, parent]
    sign_payload(gatekeeper, resolver, payload)

    result = gatekeeper.process_payload(_serialize_canonical(payload))

    assert result["state"] == "REFUSED"
    failure = result["receipt"]["rule_evaluation_logs"][2]
    assert failure["detail_code"] == "CIRCULAR_LINEAGE"


def test_state_delta_over_limit_is_refused(components):
    gatekeeper, resolver, _ = components
    payload = base_payload()
    payload["state_delta"] = {"bloat": "X" * (1024 * 1024 + 100)}
    sign_payload(gatekeeper, resolver, payload)

    result = gatekeeper.process_payload(_serialize_canonical(payload))

    assert result["state"] == "REFUSED"
    failure = result["receipt"]["rule_evaluation_logs"][3]
    assert failure["detail_code"] == "STATE_DELTA_TOO_LARGE"


def test_duplicate_key_is_ingress_rejected_without_a_signed_receipt(components):
    gatekeeper, _, _ = components
    raw = b'{"credential_id":"first","credential_id":"second"}'

    result = gatekeeper.process_payload(raw)

    assert result["state"] == "INGRESS_REJECTED"
    assert result["candidate_hash"] is None
    assert result["error_code"] == "DUPLICATE_KEY"
    assert "receipt" not in result


def test_non_finite_number_is_refused(components):
    gatekeeper, _, _ = components
    result = gatekeeper.process_payload(
        b'{"credential_id":"steward_01","operation":"MUTATE_STATE",'
        b'"state_delta":{"x":NaN},"lineage":{"parent_hash":"'
        + ZERO_HASH.encode()
        + b'","history":[]}}'
    )
    assert result["state"] == "INGRESS_REJECTED"
    assert result["error_code"] == "NON_FINITE_NUMBER"


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("12345678901234567890123456789", "12345678901234567890123456789"),
        ("9" * 128, "9" * 128),
        ("1234567890123456789012345678900", "1234567890123456789012345678900"),
        ("0.00000000000000000000000000012345678901234567890123456789", "0.00000000000000000000000000012345678901234567890123456789"),
    ],
)
def test_decimal_canonicalization_is_exact_outside_ambient_precision(source, expected):
    original_context = decimal.getcontext().copy()
    try:
        decimal.getcontext().prec = 28
        assert _serialize_canonical(decimal.Decimal(source)) == expected.encode("ascii")
    finally:
        decimal.setcontext(original_context)


def test_hostile_json_nesting_is_a_bounded_ingress_rejection(components):
    gatekeeper, _, _ = components
    raw = b'{"x":' + (b"[" * 2_000) + b"0" + (b"]" * 2_000) + b"}"

    result = gatekeeper.process_payload(raw)

    assert result == {
        "state": "INGRESS_REJECTED",
        "candidate_hash": None,
        "authorization_hash": None,
        "raw_payload_hash": gatekeeper.compute_hash(raw),
        "error_code": "MAX_DEPTH_EXCEEDED",
    }


def test_same_raw_input_and_fixed_clock_produce_identical_receipt(components):
    gatekeeper, resolver, _ = components
    payload = sign_payload(gatekeeper, resolver, base_payload())
    raw = _serialize_canonical(payload)

    first = gatekeeper.process_payload(raw)
    second = gatekeeper.process_payload(raw)

    assert first == second
# Nonce: 12187
