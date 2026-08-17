"""Regression tests for authenticated ancestry and pre-effect nonce commits."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest
from cryptography.hazmat.primitives.asymmetric import ec

from sdf_evidence_envelope import SDFEvidenceEnvelope, build_envelope, verify_evidence
from tas_admissibility import AdmissionReceipt, SQLiteNonceStore, admit_or_refuse


GENESIS = "a" * 64
STATE = "c" * 64


class Resolver:
    def __init__(self, *envelopes: SDFEvidenceEnvelope) -> None:
        self.records = {item.canonical_hash: item for item in envelopes}

    def resolve(self, canonical_hash: str) -> SDFEvidenceEnvelope | None:
        return self.records.get(canonical_hash)


def envelope(
    key: ec.EllipticCurvePrivateKey,
    *,
    sequence: int,
    parent_hash: str | None,
    nonce: str,
) -> SDFEvidenceEnvelope:
    return build_envelope(
        evidence_id=f"evidence-{nonce}",
        claim={"op": "write"},
        issuer_authority_id="authority",
        issuer_private_key=key,
        context="context",
        genesis_hash=GENESIS,
        parent_hash=parent_hash,
        sequence=sequence,
        issued_at="2026-08-17T00:00:00Z",
        nonce=nonce,
    )


def test_lineage_requires_resolved_continuous_path_to_trusted_genesis() -> None:
    key = ec.generate_private_key(ec.SECP256K1())
    root = envelope(key, sequence=0, parent_hash=None, nonce="root")
    child = envelope(key, sequence=1, parent_hash=root.canonical_hash, nonce="child")
    common: dict[str, Any] = dict(
        authority_scope=frozenset({"authority"}),
        current_context="context",
        seen_nonces=set(),
        invariant_pass=True,
        trusted_authority_keys={"authority": child.issuer.public_key_b64},
        trusted_genesis_hashes=frozenset({GENESIS}),
    )

    assert not verify_evidence(child, lineage_resolver=Resolver(), **common).lineage_intact
    assert verify_evidence(child, lineage_resolver=Resolver(root), **common).lineage_intact


def test_sqlite_nonce_is_committed_before_only_effect(tmp_path: Path) -> None:
    key = ec.generate_private_key(ec.SECP256K1())
    item = envelope(key, sequence=0, parent_hash=None, nonce="one-shot")
    store = SQLiteNonceStore(str(tmp_path / "nonces.sqlite3"))
    effects: list[str] = []

    def attempt(_: int) -> object:
        return admit_or_refuse(
            proposal={"op": "write"},
            envelope=item,
            state_root=STATE,
            authority_scope=frozenset({"authority"}),
            current_context="context",
            seen_nonces=set(),
            invariant_check=lambda proposal, state: True,
            apply_transition=lambda proposal, state: effects.append("effect") or "d" * 64,
            trusted_authority_keys={"authority": item.issuer.public_key_b64},
            nonce_store=store,
            trusted_genesis_hashes=frozenset({GENESIS}),
        )

    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(pool.map(attempt, range(8)))

    assert sum(isinstance(result, AdmissionReceipt) for result in outcomes) == 1
    assert effects == ["effect"]


def test_transition_state_root_is_validated(tmp_path: Path) -> None:
    key = ec.generate_private_key(ec.SECP256K1())
    item = envelope(key, sequence=0, parent_hash=None, nonce="invalid-root")
    with pytest.raises(ValueError, match="64-character lowercase hex"):
        admit_or_refuse(
            proposal={"op": "write"}, envelope=item, state_root=STATE,
            authority_scope=frozenset({"authority"}), current_context="context",
            seen_nonces=set(), invariant_check=lambda proposal, state: True,
            apply_transition=lambda proposal, state: "success",
            trusted_authority_keys={"authority": item.issuer.public_key_b64},
            nonce_store=SQLiteNonceStore(str(tmp_path / "nonces.sqlite3")),
            trusted_genesis_hashes=frozenset({GENESIS}),
        )
