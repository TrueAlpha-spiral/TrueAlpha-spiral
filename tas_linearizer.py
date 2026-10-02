"""
TAS Linearizer Prototype
========================

Purpose
-------
Instantiate the missing compare-and-commit boundary:

    compare live parent
    + consume admission permit
    + consume nonce
    + mutate protected state
    + append execution/refusal receipt
    + advance heads

inside one SQLite BEGIN IMMEDIATE transaction.

This is a prototype, not a production cryptographic verifier. Admission permits
are expected to have already passed the repository's authority/signature/context
verification boundary. This module re-checks deterministic permit/candidate
bindings at execution time and provides the atomic consequence boundary.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

STATE_DOMAIN = b"TAS-PROTOTYPE-STATE-V1\x00"
CANDIDATE_DOMAIN = b"TAS-PROTOTYPE-CANDIDATE-V1\x00"
ADMISSION_DOMAIN = b"TAS-PROTOTYPE-ADMISSION-V1\x00"
EXECUTION_DOMAIN = b"TAS-PROTOTYPE-EXECUTION-V1\x00"
REFUSAL_DOMAIN = b"TAS-PROTOTYPE-REFUSAL-V1\x00"

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _normalize(value: Any) -> Any:
    """Restricted deterministic JSON model: no floats, bytes, or exotic keys."""
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if isinstance(value, dict):
        if not all(isinstance(k, str) for k in value):
            raise TypeError("object keys must be strings")
        return {k: _normalize(v) for k, v in value.items()}
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")


def canonical_json(value: Any) -> bytes:
    normalized = _normalize(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def domain_hash(domain: bytes, value: Any) -> str:
    return hashlib.sha256(domain + canonical_json(value)).hexdigest()


def state_root(state: Mapping[str, Any]) -> str:
    return domain_hash(STATE_DOMAIN, dict(state))


@dataclass(frozen=True)
class Candidate:
    """A preimage-bound candidate. Rebasing creates a different candidate hash."""

    expected_state_version: int
    expected_state_root: str
    expected_receipt_head: str
    delta: Mapping[str, Any]
    context_hash: str
    nonce: str

    def body(self) -> dict[str, Any]:
        return {
            "expected_state_version": self.expected_state_version,
            "expected_state_root": self.expected_state_root,
            "expected_receipt_head": self.expected_receipt_head,
            "delta": _normalize(dict(self.delta)),
            "context_hash": self.context_hash,
            "nonce": self.nonce,
        }

    @property
    def candidate_hash(self) -> str:
        return domain_hash(CANDIDATE_DOMAIN, self.body())


@dataclass(frozen=True)
class AdmissionPermit:
    """Durable output of the admission layer, before consequence execution."""

    candidate_hash: str
    expected_state_version: int
    expected_state_root: str
    expected_receipt_head: str
    context_hash: str
    nonce: str
    verifier_receipt_hash: str

    def body(self) -> dict[str, Any]:
        return {
            "admitted": True,
            "candidate_hash": self.candidate_hash,
            "expected_state_version": self.expected_state_version,
            "expected_state_root": self.expected_state_root,
            "expected_receipt_head": self.expected_receipt_head,
            "context_hash": self.context_hash,
            "nonce": self.nonce,
            "verifier_receipt_hash": self.verifier_receipt_hash,
        }

    @property
    def receipt_hash(self) -> str:
        return domain_hash(ADMISSION_DOMAIN, self.body())


@dataclass(frozen=True)
class LinearizationResult:
    admitted: bool
    delta_s: int
    receipt_hash: str
    state_root_before: str
    state_root_after: str
    receipt_head_before: str
    receipt_head_after: str
    failure_code: str | None
    candidate_hash: str
    admission_receipt_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "admitted": self.admitted,
            "delta_s": self.delta_s,
            "receipt_hash": self.receipt_hash,
            "state_root_before": self.state_root_before,
            "state_root_after": self.state_root_after,
            "receipt_head_before": self.receipt_head_before,
            "receipt_head_after": self.receipt_head_after,
            "failure_code": self.failure_code,
            "candidate_hash": self.candidate_hash,
            "admission_receipt_hash": self.admission_receipt_hash,
        }


class SQLiteLinearizer:
    """
    Single-writer consequence boundary.

    Protected application state and evidence metadata share one SQLite database,
    so rollback covers permit consumption, replay consumption, state mutation,
    receipt append, and head advancement together.
    """

    def __init__(self, path: str | Path, genesis_state: Mapping[str, Any]) -> None:
        self.path = str(path)
        self._init_lock = threading.Lock()
        self._initialize(dict(genesis_state))

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.path,
            isolation_level=None,
            check_same_thread=False,
            timeout=30.0,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=30000")
        return conn

    def _initialize(self, genesis_state: dict[str, Any]) -> None:
        genesis_state = _normalize(genesis_state)
        genesis_root = state_root(genesis_state)
        genesis_head = domain_hash(
            EXECUTION_DOMAIN,
            {
                "kind": "GENESIS",
                "state_root": genesis_root,
                "sequence": 0,
            },
        )

        with self._init_lock:
            conn = self._connect()
            try:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS runtime (
                        singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                        evidence_sequence INTEGER NOT NULL,
                        state_version INTEGER NOT NULL,
                        state_json BLOB NOT NULL,
                        state_root TEXT NOT NULL,
                        receipt_head TEXT NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS admission_permits (
                        receipt_hash TEXT PRIMARY KEY,
                        body_json BLOB NOT NULL,
                        candidate_hash TEXT NOT NULL,
                        expected_state_version INTEGER NOT NULL,
                        expected_state_root TEXT NOT NULL,
                        expected_receipt_head TEXT NOT NULL,
                        context_hash TEXT NOT NULL,
                        nonce TEXT NOT NULL,
                        verifier_receipt_hash TEXT NOT NULL,
                        consumed INTEGER NOT NULL DEFAULT 0 CHECK (consumed IN (0,1))
                    );

                    CREATE TABLE IF NOT EXISTS consumed_nonces (
                        nonce TEXT PRIMARY KEY,
                        candidate_hash TEXT NOT NULL,
                        execution_receipt_hash TEXT NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS receipts (
                        sequence INTEGER PRIMARY KEY,
                        receipt_hash TEXT UNIQUE NOT NULL,
                        parent_receipt_hash TEXT NOT NULL,
                        kind TEXT NOT NULL CHECK (kind IN ('ADMITTED','REFUSED')),
                        candidate_hash TEXT NOT NULL,
                        admission_receipt_hash TEXT NOT NULL,
                        state_root_before TEXT NOT NULL,
                        state_root_after TEXT NOT NULL,
                        body_json BLOB NOT NULL
                    );
                    """
                )
                conn.execute(
                    """
                    INSERT OR IGNORE INTO runtime(
                        singleton, evidence_sequence, state_version,
                        state_json, state_root, receipt_head
                    ) VALUES (1, 0, 0, ?, ?, ?)
                    """,
                    (canonical_json(genesis_state), genesis_root, genesis_head),
                )
            finally:
                conn.close()

    def snapshot(self) -> dict[str, Any]:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT evidence_sequence, state_version, state_json, state_root, receipt_head "
                "FROM runtime WHERE singleton = 1"
            ).fetchone()
            assert row is not None
            return {
                "evidence_sequence": row["evidence_sequence"],
                "state_version": row["state_version"],
                "state": json.loads(bytes(row["state_json"]).decode("utf-8")),
                "state_root": row["state_root"],
                "receipt_head": row["receipt_head"],
            }
        finally:
            conn.close()

    def persist_admission(self, permit: AdmissionPermit) -> str:
        """
        Durably store a gate-approved permit before execution.

        Production integration should call this only after verifying the signed
        admission receipt using the repository's admission verifier.
        """
        for name in (
            "candidate_hash",
            "expected_state_root",
            "expected_receipt_head",
            "context_hash",
            "verifier_receipt_hash",
        ):
            value = getattr(permit, name)
            if not isinstance(value, str) or not _HEX64.fullmatch(value):
                raise ValueError(f"{name} must be 64 lowercase hex characters")
        if (
            not isinstance(permit.expected_state_version, int)
            or isinstance(permit.expected_state_version, bool)
            or permit.expected_state_version < 0
        ):
            raise ValueError("expected_state_version must be a non-negative integer")
        if not isinstance(permit.nonce, str) or not permit.nonce:
            raise ValueError("nonce must be a non-empty string")

        body = permit.body()
        receipt_hash = permit.receipt_hash
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                """
                INSERT INTO admission_permits(
                    receipt_hash, body_json, candidate_hash,
                    expected_state_version, expected_state_root, expected_receipt_head,
                    context_hash, nonce, verifier_receipt_hash, consumed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    receipt_hash,
                    canonical_json(body),
                    permit.candidate_hash,
                    permit.expected_state_version,
                    permit.expected_state_root,
                    permit.expected_receipt_head,
                    permit.context_hash,
                    permit.nonce,
                    permit.verifier_receipt_hash,
                ),
            )
            conn.execute("COMMIT")
            return receipt_hash
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def linearize(
        self,
        candidate: Candidate,
        admission_receipt_hash: str,
        *,
        fault_after: str | None = None,
    ) -> LinearizationResult:
        """
        Execute Linearize(K_n, C_i).

        fault_after is test-only fault injection:
          - "consume_permit"
          - "consume_nonce"
          - "mutate_state"
          - "append_receipt"
        """
        if not isinstance(admission_receipt_hash, str) or not _HEX64.fullmatch(
            admission_receipt_hash
        ):
            raise ValueError("admission_receipt_hash must be 64 lowercase hex chars")

        if (
            not isinstance(candidate.expected_state_version, int)
            or isinstance(candidate.expected_state_version, bool)
            or candidate.expected_state_version < 0
        ):
            raise ValueError("candidate expected_state_version must be a non-negative integer")

        candidate_hash = candidate.candidate_hash
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")

            runtime = conn.execute(
                "SELECT evidence_sequence, state_version, state_json, state_root, receipt_head "
                "FROM runtime WHERE singleton = 1"
            ).fetchone()
            assert runtime is not None

            before_state_root = runtime["state_root"]
            before_head = runtime["receipt_head"]
            evidence_sequence = int(runtime["evidence_sequence"])
            state_version = int(runtime["state_version"])

            permit = conn.execute(
                "SELECT * FROM admission_permits WHERE receipt_hash = ?",
                (admission_receipt_hash,),
            ).fetchone()

            failure: str | None = None
            if permit is None:
                failure = "ADMISSION_RECEIPT_UNKNOWN"
            elif int(permit["consumed"]) != 0:
                failure = "ADMISSION_RECEIPT_CONSUMED"
            elif permit["candidate_hash"] != candidate_hash:
                failure = "CANDIDATE_BINDING_MISMATCH"
            elif int(permit["expected_state_version"]) != candidate.expected_state_version:
                failure = "PERMIT_VERSION_BINDING_MISMATCH"
            elif permit["expected_state_root"] != candidate.expected_state_root:
                failure = "PERMIT_STATE_BINDING_MISMATCH"
            elif permit["expected_receipt_head"] != candidate.expected_receipt_head:
                failure = "PERMIT_HEAD_BINDING_MISMATCH"
            elif permit["context_hash"] != candidate.context_hash:
                failure = "CONTEXT_BINDING_MISMATCH"
            elif permit["nonce"] != candidate.nonce:
                failure = "NONCE_BINDING_MISMATCH"
            elif state_version != candidate.expected_state_version:
                failure = "STALE_STATE_VERSION"
            elif before_state_root != candidate.expected_state_root:
                failure = "STALE_STATE"
            elif before_head != candidate.expected_receipt_head:
                failure = "STALE_HEAD"
            elif conn.execute(
                "SELECT 1 FROM consumed_nonces WHERE nonce = ?", (candidate.nonce,)
            ).fetchone():
                failure = "REPLAY"

            if failure is not None:
                result = self._append_refusal(
                    conn=conn,
                    evidence_sequence=evidence_sequence,
                    state_root=before_state_root,
                    receipt_head=before_head,
                    candidate_hash=candidate_hash,
                    admission_receipt_hash=admission_receipt_hash,
                    failure_code=failure,
                )
                conn.execute("COMMIT")
                return result

            # From here through head advancement is one transaction.
            updated = conn.execute(
                """
                UPDATE admission_permits
                SET consumed = 1
                WHERE receipt_hash = ? AND consumed = 0
                """,
                (admission_receipt_hash,),
            )
            if updated.rowcount != 1:
                # Defensive: BEGIN IMMEDIATE should already serialize this.
                result = self._append_refusal(
                    conn=conn,
                    evidence_sequence=evidence_sequence,
                    state_root=before_state_root,
                    receipt_head=before_head,
                    candidate_hash=candidate_hash,
                    admission_receipt_hash=admission_receipt_hash,
                    failure_code="ADMISSION_RECEIPT_CONSUMED",
                )
                conn.execute("COMMIT")
                return result

            if fault_after == "consume_permit":
                raise RuntimeError("fault injection after permit consumption")

            # Reserve nonce in the same transaction. A placeholder receipt hash
            # is updated before commit.
            conn.execute(
                """
                INSERT INTO consumed_nonces(nonce, candidate_hash, execution_receipt_hash)
                VALUES (?, ?, ?)
                """,
                (candidate.nonce, candidate_hash, "0" * 64),
            )

            if fault_after == "consume_nonce":
                raise RuntimeError("fault injection after nonce consumption")

            old_state = json.loads(bytes(runtime["state_json"]).decode("utf-8"))
            new_state = self._apply_delta(old_state, candidate.delta)
            new_root = state_root(new_state)

            next_sequence = evidence_sequence + 1
            next_state_version = state_version + 1
            receipt_body = {
                "kind": "ADMITTED",
                "evidence_sequence": next_sequence,
                "state_version_before": state_version,
                "state_version_after": next_state_version,
                "candidate_hash": candidate_hash,
                "admission_receipt_hash": admission_receipt_hash,
                "nonce": candidate.nonce,
                "context_hash": candidate.context_hash,
                "state_root_before": before_state_root,
                "state_root_after": new_root,
                "receipt_head_before": before_head,
                "delta_s": 1,
            }
            execution_hash = domain_hash(EXECUTION_DOMAIN, receipt_body)

            runtime_update = conn.execute(
                """
                UPDATE runtime
                SET evidence_sequence = ?, state_version = ?,
                    state_json = ?, state_root = ?, receipt_head = ?
                WHERE singleton = 1
                  AND evidence_sequence = ?
                  AND state_version = ?
                  AND state_root = ?
                  AND receipt_head = ?
                """,
                (
                    next_sequence,
                    next_state_version,
                    canonical_json(new_state),
                    new_root,
                    execution_hash,
                    evidence_sequence,
                    state_version,
                    before_state_root,
                    before_head,
                ),
            )
            if runtime_update.rowcount != 1:
                raise RuntimeError("compare-and-commit runtime update failed")

            if fault_after == "mutate_state":
                raise RuntimeError("fault injection after state mutation")

            conn.execute(
                """
                INSERT INTO receipts(
                    sequence, receipt_hash, parent_receipt_hash, kind,
                    candidate_hash, admission_receipt_hash,
                    state_root_before, state_root_after, body_json
                ) VALUES (?, ?, ?, 'ADMITTED', ?, ?, ?, ?, ?)
                """,
                (
                    next_sequence,
                    execution_hash,
                    before_head,
                    candidate_hash,
                    admission_receipt_hash,
                    before_state_root,
                    new_root,
                    canonical_json(receipt_body),
                ),
            )

            conn.execute(
                """
                UPDATE consumed_nonces
                SET execution_receipt_hash = ?
                WHERE nonce = ? AND candidate_hash = ?
                """,
                (execution_hash, candidate.nonce, candidate_hash),
            )

            if fault_after == "append_receipt":
                raise RuntimeError("fault injection after receipt append")

            conn.execute("COMMIT")
            return LinearizationResult(
                admitted=True,
                delta_s=1,
                receipt_hash=execution_hash,
                state_root_before=before_state_root,
                state_root_after=new_root,
                receipt_head_before=before_head,
                receipt_head_after=execution_hash,
                failure_code=None,
                candidate_hash=candidate_hash,
                admission_receipt_hash=admission_receipt_hash,
            )
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.OperationalError:
                pass
            raise
        finally:
            conn.close()

    def _append_refusal(
        self,
        *,
        conn: sqlite3.Connection,
        evidence_sequence: int,
        state_root: str,
        receipt_head: str,
        candidate_hash: str,
        admission_receipt_hash: str,
        failure_code: str,
    ) -> LinearizationResult:
        """
        Refusal advances evidence lineage only. Protected state root is unchanged.
        """
        runtime_row = conn.execute(
            "SELECT state_version FROM runtime WHERE singleton = 1"
        ).fetchone()
        assert runtime_row is not None
        state_version = int(runtime_row["state_version"])
        next_sequence = evidence_sequence + 1
        body = {
            "kind": "REFUSED",
            "evidence_sequence": next_sequence,
            "state_version_before": state_version,
            "state_version_after": state_version,
            "candidate_hash": candidate_hash,
            "admission_receipt_hash": admission_receipt_hash,
            "failure_code": failure_code,
            "state_root_before": state_root,
            "state_root_after": state_root,
            "receipt_head_before": receipt_head,
            "delta_s": 0,
        }
        refusal_hash = domain_hash(REFUSAL_DOMAIN, body)

        conn.execute(
            """
            INSERT INTO receipts(
                sequence, receipt_hash, parent_receipt_hash, kind,
                candidate_hash, admission_receipt_hash,
                state_root_before, state_root_after, body_json
            ) VALUES (?, ?, ?, 'REFUSED', ?, ?, ?, ?, ?)
            """,
            (
                next_sequence,
                refusal_hash,
                receipt_head,
                candidate_hash,
                admission_receipt_hash,
                state_root,
                state_root,
                canonical_json(body),
            ),
        )
        conn.execute(
            """
            UPDATE runtime
            SET evidence_sequence = ?, receipt_head = ?
            WHERE singleton = 1
              AND evidence_sequence = ?
              AND state_version = ?
              AND state_root = ?
              AND receipt_head = ?
            """,
            (
                next_sequence,
                refusal_hash,
                evidence_sequence,
                state_version,
                state_root,
                receipt_head,
            ),
        )

        return LinearizationResult(
            admitted=False,
            delta_s=0,
            receipt_hash=refusal_hash,
            state_root_before=state_root,
            state_root_after=state_root,
            receipt_head_before=receipt_head,
            receipt_head_after=refusal_hash,
            failure_code=failure_code,
            candidate_hash=candidate_hash,
            admission_receipt_hash=admission_receipt_hash,
        )

    @staticmethod
    def _apply_delta(state: dict[str, Any], delta: Mapping[str, Any]) -> dict[str, Any]:
        """
        Prototype application reducer.

        Supported:
          {"op": "set", "key": <str>, "value": <canonical-json value>}
          {"op": "delete", "key": <str>}
          {"op": "increment", "key": <str>, "amount": <int>}
        """
        delta = _normalize(dict(delta))
        op = delta.get("op")
        key = delta.get("key")
        if not isinstance(key, str) or not key:
            raise ValueError("delta.key must be a non-empty string")

        out = dict(state)

        if op == "set":
            if "value" not in delta:
                raise ValueError("set requires value")
            out[key] = delta["value"]
            return out

        if op == "delete":
            out.pop(key, None)
            return out

        if op == "increment":
            amount = delta.get("amount")
            if not isinstance(amount, int) or isinstance(amount, bool):
                raise ValueError("increment amount must be an integer")
            current = out.get(key, 0)
            if not isinstance(current, int) or isinstance(current, bool):
                raise ValueError("increment target must be an integer")
            out[key] = current + amount
            return out

        raise ValueError(f"unsupported delta op: {op!r}")

    def receipts(self) -> list[dict[str, Any]]:
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT sequence, receipt_hash, kind, body_json "
                "FROM receipts ORDER BY sequence"
            ).fetchall()
            return [
                {
                    "sequence": row["sequence"],
                    "receipt_hash": row["receipt_hash"],
                    "kind": row["kind"],
                    "body": json.loads(bytes(row["body_json"]).decode("utf-8")),
                }
                for row in rows
            ]
        finally:
            conn.close()
