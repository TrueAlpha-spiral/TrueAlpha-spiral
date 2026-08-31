from typing import Any, Dict
from scripts.tasverify import (
    extract_receipt_hash,
    extract_lineage_parent,
    extract_receipt_id,
    extract_prime_invariant,
    extract_human_steward,
    extract_boundary_checks,
)

def test_extract_receipt_hash():
    subject = {"source_hash": "abc"}
    receipt: Dict[str, Any] = {}
    assert extract_receipt_hash(receipt, subject) == "sha256:abc"

    subject = {"artifact_hash": "sha256:def"}
    assert extract_receipt_hash(receipt, subject) == "sha256:def"

    subject = {}
    receipt = {"verification": {"hash_value": "ghi"}}
    assert extract_receipt_hash(receipt, subject) == "sha256:ghi"


def test_extract_lineage_parent():
    subject = {"lineage_parent": "abc"}
    assert extract_lineage_parent(subject) == "sha256:abc"

    subject = {"parent_hash": "sha256:def"}
    assert extract_lineage_parent(subject) == "sha256:def"


def test_extract_receipt_id():
    subject = {"canonical_event": "evt_123"}
    receipt: Dict[str, Any] = {}
    assert extract_receipt_id(receipt, subject) == "evt_123"

    subject = {"receipt_id": "rcpt_456"}
    assert extract_receipt_id(receipt, subject) == "rcpt_456"

    subject = {}
    receipt = {"id": "id_789"}
    assert extract_receipt_id(receipt, subject) == "id_789"


def test_extract_prime_invariant():
    subject = {"prime_invariant": "4 ≡ four"}
    receipt: Dict[str, Any] = {}
    assert extract_prime_invariant(receipt, subject) == "4 ≡ four"

    subject = {}
    receipt = {"prime_invariant": "REALITY != SIMULATION"}
    assert extract_prime_invariant(receipt, subject) == "REALITY != SIMULATION"


def test_extract_human_steward():
    subject = {"paradata": {"human_initiator": "alice"}}
    receipt: Dict[str, Any] = {}
    assert extract_human_steward(receipt, subject) == "alice"

    subject = {"human_steward": "bob"}
    assert extract_human_steward(receipt, subject) == "bob"

    subject = {}
    receipt = {"provenance": {"author_steward": "charlie"}}
    assert extract_human_steward(receipt, subject) == "charlie"


def test_extract_boundary_checks():
    subject = {"boundary_checks": {"test": True}}
    receipt: Dict[str, Any] = {}
    assert extract_boundary_checks(receipt, subject) == {"test": True}

    subject = {}
    receipt = {"boundary_checks": {"other": False}}
    assert extract_boundary_checks(receipt, subject) == {"other": False}

# Nonce: 34792
