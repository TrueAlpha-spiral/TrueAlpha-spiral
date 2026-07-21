import hashlib
from datetime import datetime, timedelta, timezone

from tas_pythonetics.layer0_governance import (
    ActionPayload,
    DelegationCertificate,
    Layer0GovernanceEngine,
    SignaturePayload,
    canonical_hash,
)


def make_sig(key_id: str, payload_bytes: bytes) -> SignaturePayload:
    signature = hashlib.sha256(key_id.encode() + payload_bytes).hexdigest()
    return SignaturePayload(key_id=key_id, signature=signature)


def make_engine() -> Layer0GovernanceEngine:
    validators = {
        "val_A": {"weight": 3, "capabilities": {"sys:write", "sys:read", "policy:mutate"}},
        "val_B": {"weight": 3, "capabilities": {"sys:write", "sys:read"}},
        "val_C": {"weight": 2, "capabilities": {"sys:read"}},
        "val_D": {"weight": 2, "capabilities": {"sys:read"}},
    }
    return Layer0GovernanceEngine(threshold=6, validators=validators)


def test_canonical_hash_is_order_stable():
    assert canonical_hash({"b": 2, "a": 1}) == canonical_hash({"a": 1, "b": 2})


def test_quorum_success():
    engine = make_engine()
    action = ActionPayload("act_1", "sys:write", {"data": "test"}, signatures=[])
    payload_bytes = action.get_canonical_bytes()
    action.signatures = [make_sig("val_A", payload_bytes), make_sig("val_B", payload_bytes)]

    authorized, msg = engine.verify_action_authorization(action)

    assert authorized is True
    assert "Quorum satisfied" in msg


def test_quorum_failure_insufficient_weight():
    engine = make_engine()
    action = ActionPayload("act_2", "sys:read", {"data": "test"}, signatures=[])
    payload_bytes = action.get_canonical_bytes()
    action.signatures = [make_sig("val_C", payload_bytes), make_sig("val_D", payload_bytes)]

    authorized, msg = engine.verify_action_authorization(action)

    assert authorized is False
    assert "Quorum threshold not met" in msg


def test_delegation_valid_attenuation():
    engine = make_engine()
    now = datetime.now(timezone.utc)
    cert = DelegationCertificate(
        certificate_id="cert_001",
        delegator_key_id="val_A",
        delegate_key_id="agent_leaf",
        capabilities=["sys:read"],
        delegation_depth=2,
        weight_cap=1,
        valid_from=(now - timedelta(minutes=5)).isoformat(),
        valid_until=(now + timedelta(hours=1)).isoformat(),
        nonce="nonce_123",
    )
    action = ActionPayload("act_del_1", "sys:read", {"op": "query"}, signatures=[], delegation_chain=[cert])
    action.signatures = [make_sig("agent_leaf", action.get_canonical_bytes())]

    authorized, msg = engine.verify_action_authorization(action)

    assert authorized is True
    assert "Delegated action authorized" in msg


def test_delegation_failure_capability_expansion():
    engine = make_engine()
    now = datetime.now(timezone.utc)
    cert = DelegationCertificate(
        certificate_id="cert_invalid",
        delegator_key_id="val_C",
        delegate_key_id="agent_rogue",
        capabilities=["sys:read", "policy:mutate"],
        delegation_depth=1,
        weight_cap=1,
        valid_from=(now - timedelta(minutes=5)).isoformat(),
        valid_until=(now + timedelta(hours=1)).isoformat(),
        nonce="nonce_456",
    )
    action = ActionPayload("act_del_2", "policy:mutate", {"op": "nuke"}, signatures=[], delegation_chain=[cert])
    action.signatures = [make_sig("agent_rogue", action.get_canonical_bytes())]

    authorized, msg = engine.verify_action_authorization(action)

    assert authorized is False
    assert "Capability expansion attempt detected" in msg


def test_delegation_failure_depth_exceeded():
    engine = make_engine()
    now = datetime.now(timezone.utc)
    cert = DelegationCertificate(
        certificate_id="cert_depth_err",
        delegator_key_id="val_A",
        delegate_key_id="agent_deep",
        capabilities=["sys:read"],
        delegation_depth=3,
        weight_cap=1,
        valid_from=(now - timedelta(minutes=5)).isoformat(),
        valid_until=(now + timedelta(hours=1)).isoformat(),
        nonce="nonce_789",
    )
    action = ActionPayload("act_del_3", "sys:read", {}, signatures=[], delegation_chain=[cert])
    action.signatures = [make_sig("agent_deep", action.get_canonical_bytes())]

    authorized, msg = engine.verify_action_authorization(action)

    assert authorized is False
    assert "Delegation depth violated" in msg


def test_delegation_failure_temporal_expansion():
    engine = make_engine()
    now = datetime.now(timezone.utc)
    parent = DelegationCertificate(
        certificate_id="cert_parent",
        delegator_key_id="val_A",
        delegate_key_id="agent_mid",
        capabilities=["sys:read"],
        delegation_depth=2,
        weight_cap=1,
        valid_from=(now - timedelta(minutes=5)).isoformat(),
        valid_until=(now + timedelta(minutes=30)).isoformat(),
        nonce="nonce_parent",
    )
    child = DelegationCertificate(
        certificate_id="cert_child",
        delegator_key_id="agent_mid",
        delegate_key_id="agent_leaf",
        capabilities=["sys:read"],
        delegation_depth=1,
        weight_cap=1,
        valid_from=(now - timedelta(minutes=1)).isoformat(),
        valid_until=(now + timedelta(hours=1)).isoformat(),
        nonce="nonce_child",
    )

    valid, msg = engine.validate_delegation_chain([parent, child], "sys:read")

    assert valid is False
    assert "Temporal enclosure violated" in msg


def test_emergency_key_eviction_cycle():
    engine = make_engine()
    target_key = "val_B"
    purge_bytes = f"PURGE_EVICTION_{target_key}".encode()
    votes = {
        "val_A": hashlib.sha256("val_A".encode() + purge_bytes).hexdigest(),
        "val_C": hashlib.sha256("val_C".encode() + purge_bytes).hexdigest(),
        "val_D": hashlib.sha256("val_D".encode() + purge_bytes).hexdigest(),
    }

    purged, purge_msg = engine.execute_emergency_purge(target_key, votes)

    assert purged is True
    assert "Eviction successful" in purge_msg
    assert target_key in engine.revocation_list
    assert engine.threshold == 4

    action = ActionPayload("act_evicted", "sys:write", {}, signatures=[])
    payload_bytes = action.get_canonical_bytes()
    action.signatures = [make_sig("val_B", payload_bytes), make_sig("val_C", payload_bytes)]

    authorized, msg = engine.verify_action_authorization(action)

    assert authorized is False
    assert "Quorum threshold not met" in msg
