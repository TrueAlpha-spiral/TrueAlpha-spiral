from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from tas_linearizer import (
    AdmissionPermit,
    Candidate,
    SQLiteLinearizer,
    domain_hash,
)


def h(label: str) -> str:
    return domain_hash(b"TEST\x00", {"label": label})


def make_candidate(engine: SQLiteLinearizer, *, nonce: str, value: int) -> Candidate:
    snap = engine.snapshot()
    return Candidate(
        expected_state_version=snap["state_version"],
        expected_state_root=snap["state_root"],
        expected_receipt_head=snap["receipt_head"],
        delta={"op": "set", "key": "value", "value": value},
        context_hash=h("context"),
        nonce=nonce,
    )


def admit(engine: SQLiteLinearizer, candidate: Candidate) -> str:
    permit = AdmissionPermit(
        candidate_hash=candidate.candidate_hash,
        expected_state_version=candidate.expected_state_version,
        expected_state_root=candidate.expected_state_root,
        expected_receipt_head=candidate.expected_receipt_head,
        context_hash=candidate.context_hash,
        nonce=candidate.nonce,
        verifier_receipt_hash=h("verifier"),
    )
    return engine.persist_admission(permit)


def test_success_is_one_atomic_state_advance(tmp_path: Path) -> None:
    engine = SQLiteLinearizer(tmp_path / "db.sqlite3", {"value": 0})
    candidate = make_candidate(engine, nonce="n-1", value=7)
    permit_hash = admit(engine, candidate)

    result = engine.linearize(candidate, permit_hash)
    snap = engine.snapshot()

    assert result.admitted is True
    assert result.delta_s == 1
    assert snap["state"] == {"value": 7}
    assert snap["state_root"] == result.state_root_after
    assert snap["receipt_head"] == result.receipt_hash
    assert engine.receipts()[-1]["kind"] == "ADMITTED"


def test_refusal_changes_evidence_head_not_state(tmp_path: Path) -> None:
    engine = SQLiteLinearizer(tmp_path / "db.sqlite3", {"value": 0})
    before = engine.snapshot()

    candidate = Candidate(
        expected_state_version=before["state_version"],
        expected_state_root=h("wrong-state"),
        expected_receipt_head=before["receipt_head"],
        delta={"op": "set", "key": "value", "value": 9},
        context_hash=h("context"),
        nonce="n-stale",
    )
    permit_hash = admit(engine, candidate)
    result = engine.linearize(candidate, permit_hash)
    after = engine.snapshot()

    assert result.admitted is False
    assert result.delta_s == 0
    assert result.failure_code == "STALE_STATE"
    assert after["state"] == before["state"]
    assert after["state_root"] == before["state_root"]
    assert after["state_version"] == before["state_version"]
    assert after["receipt_head"] != before["receipt_head"]
    assert engine.receipts()[-1]["kind"] == "REFUSED"


def test_two_candidates_same_parent_only_one_instantiates(tmp_path: Path) -> None:
    engine = SQLiteLinearizer(tmp_path / "db.sqlite3", {"value": 0})
    snap = engine.snapshot()

    c1 = Candidate(
        expected_state_version=snap["state_version"],
        expected_state_root=snap["state_root"],
        expected_receipt_head=snap["receipt_head"],
        delta={"op": "set", "key": "value", "value": 1},
        context_hash=h("context"),
        nonce="race-1",
    )
    c2 = Candidate(
        expected_state_version=snap["state_version"],
        expected_state_root=snap["state_root"],
        expected_receipt_head=snap["receipt_head"],
        delta={"op": "set", "key": "value", "value": 2},
        context_hash=h("context"),
        nonce="race-2",
    )
    p1 = admit(engine, c1)
    p2 = admit(engine, c2)

    def run(pair):
        candidate, permit_hash = pair
        return engine.linearize(candidate, permit_hash)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, [(c1, p1), (c2, p2)]))

    admitted = [r for r in results if r.admitted]
    refused = [r for r in results if not r.admitted]

    assert len(admitted) == 1
    assert len(refused) == 1
    assert refused[0].failure_code in {"STALE_STATE_VERSION", "STALE_STATE", "STALE_HEAD"}
    assert engine.snapshot()["state"]["value"] in {1, 2}


@pytest.mark.parametrize(
    "fault_after",
    ["consume_permit", "consume_nonce", "mutate_state", "append_receipt"],
)
def test_fault_rolls_back_entire_linearization(
    tmp_path: Path, fault_after: str
) -> None:
    engine = SQLiteLinearizer(tmp_path / f"{fault_after}.sqlite3", {"value": 0})
    candidate = make_candidate(engine, nonce=f"fault-{fault_after}", value=99)
    permit_hash = admit(engine, candidate)
    before = engine.snapshot()

    with pytest.raises(RuntimeError, match="fault injection"):
        engine.linearize(candidate, permit_hash, fault_after=fault_after)

    after = engine.snapshot()
    assert after == before
    assert engine.receipts() == []

    # The permit and nonce were rolled back too, so the same exact candidate
    # can still instantiate after recovery.
    retry = engine.linearize(candidate, permit_hash)
    assert retry.admitted is True
    assert engine.snapshot()["state"]["value"] == 99


def test_rebase_is_new_candidate_not_rewrite(tmp_path: Path) -> None:
    engine = SQLiteLinearizer(tmp_path / "db.sqlite3", {"value": 0})
    original = make_candidate(engine, nonce="original", value=1)
    original_hash = original.candidate_hash
    original_permit = admit(engine, original)
    first = engine.linearize(original, original_permit)
    assert first.admitted

    # The old preimage is now stale.
    stale_again = engine.linearize(original, original_permit)
    assert stale_again.admitted is False

    # Rebase means a complete new preimage and therefore a different hash.
    current = engine.snapshot()
    rebased = Candidate(
        expected_state_version=current["state_version"],
        expected_state_root=current["state_root"],
        expected_receipt_head=current["receipt_head"],
        delta={"op": "set", "key": "value", "value": 2},
        context_hash=original.context_hash,
        nonce="rebased",
    )
    assert rebased.candidate_hash != original_hash

    rebased_permit = admit(engine, rebased)
    second = engine.linearize(rebased, rebased_permit)
    assert second.admitted
    assert engine.snapshot()["state"]["value"] == 2


def test_permit_cannot_authorize_different_candidate(tmp_path: Path) -> None:
    engine = SQLiteLinearizer(tmp_path / "db.sqlite3", {"value": 0})
    candidate = make_candidate(engine, nonce="bound", value=1)
    permit_hash = admit(engine, candidate)

    tampered = Candidate(
        expected_state_version=candidate.expected_state_version,
        expected_state_root=candidate.expected_state_root,
        expected_receipt_head=candidate.expected_receipt_head,
        delta={"op": "set", "key": "value", "value": 999},
        context_hash=candidate.context_hash,
        nonce=candidate.nonce,
    )
    result = engine.linearize(tampered, permit_hash)

    assert result.admitted is False
    assert result.failure_code == "CANDIDATE_BINDING_MISMATCH"
    assert engine.snapshot()["state"]["value"] == 0


def test_durability_survives_restart(tmp_path: Path) -> None:
    db = tmp_path / "restart.sqlite3"
    engine = SQLiteLinearizer(db, {"value": 0})
    candidate = make_candidate(engine, nonce="restart", value=41)
    permit_hash = admit(engine, candidate)
    result = engine.linearize(candidate, permit_hash)
    assert result.admitted

    reopened = SQLiteLinearizer(db, {"value": -999})
    snap = reopened.snapshot()
    assert snap["state"] == {"value": 41}
    assert snap["receipt_head"] == result.receipt_hash
    assert snap["state_version"] == 1


def test_refusal_head_forces_full_rebase_even_when_state_is_unchanged(tmp_path: Path) -> None:
    engine = SQLiteLinearizer(tmp_path / "db.sqlite3", {"value": 0})
    before = engine.snapshot()

    pending = Candidate(
        expected_state_version=before["state_version"],
        expected_state_root=before["state_root"],
        expected_receipt_head=before["receipt_head"],
        delta={"op": "set", "key": "value", "value": 5},
        context_hash=h("context"),
        nonce="pending",
    )
    pending_permit = admit(engine, pending)

    bad = Candidate(
        expected_state_version=before["state_version"],
        expected_state_root=h("bad"),
        expected_receipt_head=before["receipt_head"],
        delta={"op": "set", "key": "value", "value": 8},
        context_hash=h("context"),
        nonce="bad",
    )
    bad_permit = admit(engine, bad)
    refusal = engine.linearize(bad, bad_permit)
    assert not refusal.admitted

    after_refusal = engine.snapshot()
    assert after_refusal["state_root"] == before["state_root"]
    assert after_refusal["state_version"] == before["state_version"]
    assert after_refusal["receipt_head"] != before["receipt_head"]

    stale = engine.linearize(pending, pending_permit)
    assert not stale.admitted
    assert stale.failure_code == "STALE_HEAD"
