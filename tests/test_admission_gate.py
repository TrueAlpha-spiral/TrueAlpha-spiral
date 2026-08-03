import base64
import os
import sys
from dataclasses import replace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from admission_gate import (
    AUTHORIZATION_DOMAIN,
    AdmissionGatekeeper,
    AuthoritySnapshot,
    AuthenticatedLineageVerifier,
    CANONICALIZATION_VERSION,
    Ed25519Verifier,
    FileDecisionLedger,
    InMemoryDecisionLedger,
    LocalEd25519Signer,
    LocalSecp256k1Signer,
    Secp256k1Verifier,
    authority_binding_hash,
    canonical_hash,
    canonical_json,
    parse_canonical_json,
)
from context_snapshot import (
    ContextSnapshot,
    InMemoryContextResolver,
    InMemoryDefinitionResolver,
    definition_id_for_mapping,
    make_definition_record,
)


class Resolver:
    def __init__(self, snapshot):
        self.snapshot = snapshot

    def resolve(self, *, credential_id, checkpoint_hash):
        return (
            self.snapshot
            if (credential_id, checkpoint_hash)
            == (self.snapshot.credential_id, self.snapshot.checkpoint_hash)
            else None
        )


def _gate():
    authority_key = ec.generate_private_key(ec.SECP256K1())
    receipt_key = ec.generate_private_key(ec.SECP256K1())
    authority = LocalSecp256k1Signer(authority_key)

    authority_snapshot = AuthoritySnapshot(
        "credential-1",
        authority.algorithm,
        authority.public_key,
        7,
        False,
        "c" * 64,
        "a" * 64,
        "2030-01-01T00:00:00Z",
    )
    definition = make_definition_record(
        namespace_id="tas:core",
        term="requested_operation",
        semantic_version="1",
        definition="The scoped operation requested by external authority.",
    )
    definition_id = definition_id_for_mapping(definition)
    context = ContextSnapshot.build(
        namespace_id="tas:core",
        context_sequence=0,
        definition_ids=[definition_id],
        invariant_set_id="b" * 64,
        authority_binding_hash=authority_binding_hash(authority_snapshot),
        parent_context_hash=None,
        effective_epoch=7,
    )
    authority_snapshot = replace(
        authority_snapshot,
        context_snapshot_hash=context.context_snapshot_hash,
    )
    ledger = InMemoryDecisionLedger()
    context_resolver = InMemoryContextResolver(
        {context.context_snapshot_hash: canonical_json(context.mapping)},
        {context.namespace_id: context.context_snapshot_hash},
    )
    definition_resolver = InMemoryDefinitionResolver(
        {definition_id: canonical_json(definition)}
    )
    gate = AdmissionGatekeeper(
        gatekeeper_id="gate-1",
        authority_resolver=Resolver(authority_snapshot),
        context_resolver=context_resolver,
        definition_resolver=definition_resolver,
        verifier=Secp256k1Verifier(),
        receipt_signer=LocalSecp256k1Signer(receipt_key),
        ledger=ledger,
    )
    return gate, authority, ledger, context, authority_snapshot


def _request(
    authority,
    context,
    candidate=None,
    parent_receipt_hash=None,
):
    if candidate is None:
        candidate = {"operation": "READ"}
    body = {
        "schema_version": 2,
        "canonicalization_version": CANONICALIZATION_VERSION,
        "domain_separator": "TAS_AUTHORITY_GATE_V1",
        "credential_id": "credential-1",
        "authority_checkpoint_hash": "a" * 64,
        "authority_epoch": 7,
        "context_snapshot_hash": context.context_snapshot_hash,
        "signature_algorithm": authority.algorithm,
        "requested_operation": "READ",
        "candidate_hash": canonical_hash(candidate),
        "parent_receipt_hash": parent_receipt_hash,
        "nonce": "nonce-1",
    }
    signature = base64.b64encode(
        authority.sign(AUTHORIZATION_DOMAIN + canonical_json(body))
    ).decode()
    return canonical_json(candidate), canonical_json(
        {**body, "signature": signature}
    )


def test_admitted_decision_is_context_bound_and_recorded_before_return():
    gate, authority, ledger, context, _ = _gate()
    candidate, envelope = _request(authority, context)
    result = gate.evaluate(
        raw_candidate=candidate,
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:00Z",
    )
    assert result["resulting_state"] == "ADMITTED"
    assert result["durable_receipt"]
    assert (
        result["receipt"]["context_snapshot_hash"]
        == context.context_snapshot_hash
    )
    assert result["receipt"]["registry_root"] == context.registry_root
    assert ledger.get_receipt(result["receipt_hash"]) == result["receipt"]
    assert AuthenticatedLineageVerifier(
        ledger, Secp256k1Verifier()
    ).verify(result["receipt_hash"])


def test_public_key_cannot_forge_authorization_signature():
    gate, authority, _, context, _ = _gate()
    candidate, envelope = _request(authority, context)
    forged = parse_canonical_json(envelope)
    forged["signature"] = base64.b64encode(b"not a signature").decode()
    result = gate.evaluate(
        raw_candidate=candidate,
        raw_envelope=canonical_json(forged),
        current_time="2029-01-01T00:00:00Z",
    )
    assert result["resulting_state"] == "REFUSED"
    assert result["durable_receipt"]


def test_context_is_verified_before_candidate_is_parsed():
    gate, authority, _, context, _ = _gate()
    _, envelope = _request(authority, context)
    gate.context_resolver._namespace_heads[context.namespace_id] = "f" * 64
    result = gate.evaluate(
        raw_candidate=b'{"operation":"READ","operation":"DELETE"}',
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:00Z",
    )
    assert result["resulting_state"] == "REFUSED"
    assert result["receipt"]["failure_code"] == "CONTEXT_REFUSED"
    assert result["receipt"]["candidate_hash"] is None


def test_authority_snapshot_cannot_swap_context_mid_flight():
    gate, authority, _, context, snapshot = _gate()
    candidate, envelope = _request(authority, context)
    gate.authority_resolver.snapshot = replace(
        snapshot,
        context_snapshot_hash="f" * 64,
    )
    result = gate.evaluate(
        raw_candidate=candidate,
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:00Z",
    )
    assert result["resulting_state"] == "REFUSED"
    assert (
        result["receipt"]["failure_code"]
        == "CONTEXT_AUTHORITY_MISMATCH"
    )


def test_context_lineage_cannot_teleport_across_unrelated_contexts():
    gate, authority, _, context, snapshot = _gate()
    candidate, envelope = _request(authority, context)
    first = gate.evaluate(
        raw_candidate=candidate,
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:00Z",
    )

    next_context = ContextSnapshot.build(
        namespace_id=context.namespace_id,
        context_sequence=1,
        definition_ids=context.definition_ids,
        invariant_set_id=context.invariant_set_id,
        authority_binding_hash=context.authority_binding_hash,
        parent_context_hash="e" * 64,
        effective_epoch=7,
    )
    gate.context_resolver._snapshots[
        next_context.context_snapshot_hash
    ] = canonical_json(next_context.mapping)
    gate.context_resolver._namespace_heads[next_context.namespace_id] = (
        next_context.context_snapshot_hash
    )
    gate.authority_resolver.snapshot = replace(
        snapshot,
        context_snapshot_hash=next_context.context_snapshot_hash,
    )
    candidate, envelope = _request(
        authority,
        next_context,
        parent_receipt_hash=first["receipt_hash"],
    )
    result = gate.evaluate(
        raw_candidate=candidate,
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:01Z",
    )
    assert result["resulting_state"] == "REFUSED"
    assert result["receipt"]["failure_code"] == "CONTEXT_LINEAGE_REFUSED"


def test_duplicate_key_is_rejected_after_context_verification():
    gate, authority, _, context, _ = _gate()
    _, envelope = _request(authority, context)
    result = gate.evaluate(
        raw_candidate=b'{"operation":"READ","operation":"DELETE"}',
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:00Z",
    )
    assert result["resulting_state"] == "REFUSED"
    assert (
        result["receipt"]["failure_code"]
        == "INVALID_INPUT:CanonicalJSONError"
    )


def test_signing_or_append_failure_fails_closed():
    gate, authority, _, context, _ = _gate()
    candidate, envelope = _request(authority, context)

    class BrokenLedger:
        def append_decision(self, *_):
            raise OSError("offline")

        def get_receipt(self, *_):
            return None

    gate.ledger = BrokenLedger()
    result = gate.evaluate(
        raw_candidate=candidate,
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:00Z",
    )
    assert result == {
        "resulting_state": "CUTOFF",
        "failure_code": "RECEIPT_PRESERVATION_UNAVAILABLE",
        "durable_receipt": False,
    }


def test_lineage_verifier_rejects_tampered_receipt_content():
    gate, authority, ledger, context, _ = _gate()
    candidate, envelope = _request(authority, context)
    result = gate.evaluate(
        raw_candidate=candidate,
        raw_envelope=envelope,
        current_time="2029-01-01T00:00:00Z",
    )
    ledger._records[result["receipt_hash"]][
        "requested_operation"
    ] = "DELETE"
    assert not AuthenticatedLineageVerifier(
        ledger, Secp256k1Verifier()
    ).verify(result["receipt_hash"])


def test_ed25519_decision_survives_store_restart(tmp_path):
    authority = LocalEd25519Signer(Ed25519PrivateKey.generate())
    receipt_signer = LocalEd25519Signer(Ed25519PrivateKey.generate())
    snapshot = AuthoritySnapshot(
        "juridical-authority-1",
        authority.algorithm,
        authority.public_key,
        11,
        False,
        "c" * 64,
        "d" * 64,
        "2030-01-01T00:00:00Z",
    )
    definition = make_definition_record(
        namespace_id="tas:ioc",
        term="requested_operation",
        semantic_version="1",
        definition="An operation explicitly bounded by authority scope.",
    )
    definition_id = definition_id_for_mapping(definition)
    context = ContextSnapshot.build(
        namespace_id="tas:ioc",
        context_sequence=0,
        definition_ids=[definition_id],
        invariant_set_id="b" * 64,
        authority_binding_hash=authority_binding_hash(snapshot),
        parent_context_hash=None,
        effective_epoch=11,
    )
    snapshot = replace(
        snapshot, context_snapshot_hash=context.context_snapshot_hash
    )
    store_path = tmp_path / "decisions"
    ledger = FileDecisionLedger(store_path)
    gate = AdmissionGatekeeper(
        gatekeeper_id="ioc-gate-1",
        authority_resolver=Resolver(snapshot),
        context_resolver=InMemoryContextResolver(
            {context.context_snapshot_hash: canonical_json(context.mapping)},
            {context.namespace_id: context.context_snapshot_hash},
        ),
        definition_resolver=InMemoryDefinitionResolver(
            {definition_id: canonical_json(definition)}
        ),
        verifier=Ed25519Verifier(),
        receipt_signer=receipt_signer,
        ledger=ledger,
    )
    candidate = {"operation": "READ"}
    body = {
        "schema_version": 2,
        "canonicalization_version": CANONICALIZATION_VERSION,
        "domain_separator": "TAS_AUTHORITY_GATE_V1",
        "credential_id": snapshot.credential_id,
        "authority_checkpoint_hash": snapshot.checkpoint_hash,
        "authority_epoch": snapshot.authority_epoch,
        "context_snapshot_hash": context.context_snapshot_hash,
        "signature_algorithm": authority.algorithm,
        "requested_operation": "READ",
        "candidate_hash": canonical_hash(candidate),
        "parent_receipt_hash": None,
        "nonce": "ioc-fixed-nonce-1",
    }
    envelope = {
        **body,
        "signature": base64.b64encode(
            authority.sign(AUTHORIZATION_DOMAIN + canonical_json(body))
        ).decode(),
    }

    result = gate.evaluate(
        raw_candidate=canonical_json(candidate),
        raw_envelope=canonical_json(envelope),
        current_time="2029-01-01T00:00:00Z",
    )

    assert result["resulting_state"] == "ADMITTED"
    restarted_ledger = FileDecisionLedger(store_path)
    assert (
        restarted_ledger.get_receipt(result["receipt_hash"])
        == result["receipt"]
    )
    assert AuthenticatedLineageVerifier(
        restarted_ledger, Ed25519Verifier()
    ).verify(result["receipt_hash"])


def test_file_ledger_rejects_tampered_receipt_after_restart(tmp_path):
    ledger = FileDecisionLedger(tmp_path)
    receipt = {"resulting_state": "REFUSED", "failure_code": "EMPTY_SET"}
    receipt_hash = canonical_hash(receipt)
    ledger.append_decision(receipt_hash, receipt)
    path = tmp_path / f"{receipt_hash}.json"
    path.write_bytes(canonical_json({**receipt, "failure_code": "FORGED"}))

    assert FileDecisionLedger(tmp_path).get_receipt(receipt_hash) is None
