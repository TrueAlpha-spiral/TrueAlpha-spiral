"""Refusal artifacts for fail-closed TAS bridge behavior.

§11 of *Intelligent Self-Similar Design in TrueAlphaSpiral* requires that a
refusal is not merely a negative result — it is the *negative image* of
intelligent design.  A system is self-similar when its failures preserve the
same integrity structure as its successes.

A TAS refusal must contain (§11):
  - candidate identity or hash
  - governing rule version
  - parent or evaluation context
  - stable failure codes
  - decision state
  - signer or verifier evidence
  - durable chronology

    No state change ≠ no event.

The refused operation does not mutate the application state, but the refusal
itself becomes part of the evidence history.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import hashlib
import json


_RULE_VERSION = "TAS-SDF-1.0"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_hash(obj: Any) -> str:
    encoded = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class RefusalArtifact:
    """Negative proof emitted when a TAS bridge transition is inadmissible.

    Every field maps to a §11 requirement so that refusals are structurally
    indistinguishable from admissions in terms of evidentiary completeness.
    """

    # §11: reason for refusal (human-readable)
    reason: str

    # §11: stable failure code — caller should use a domain-specific code;
    # defaults to the generic bridge code for backward compatibility.
    code: str = "TAS_OPENAI_REFUSAL"

    # §11: candidate identity or hash — hash of the candidate payload that
    # triggered the refusal, if available.
    candidate_hash: str = ""

    # §11: governing rule version in effect at the time of evaluation.
    rule_version: str = _RULE_VERSION

    # §11: parent or evaluation context — the context frame in which the
    # candidate was evaluated (e.g. gate name, chain head hash).
    parent_context: str = ""

    # §11: decision state — always REFUSED here; carried explicitly so the
    # field is present on every artifact regardless of caller.
    decision_state: str = "REFUSED"

    # §11: signer or verifier evidence — identity of the gate or verifier
    # that produced the refusal.
    verifier: str = "TAS_OPENAI_BRIDGE"

    # §11: durable chronology — when the candidate reached the constitutional
    # boundary.
    timestamp: str = field(default_factory=_now_iso)

    # Retained for backward compatibility and structured detail.
    action: str = "REFUSE"
    admissible: bool = False
    details: dict[str, Any] = field(default_factory=dict)

    # Self-computed refusal receipt ID (hash of the artifact's own payload).
    refusal_receipt_id: str = field(default="")

    # ------------------------------------------------------------------ #
    # Construction helpers                                                 #
    # ------------------------------------------------------------------ #

    @classmethod
    def from_gate_result(cls, gate_result: Any) -> "RefusalArtifact":
        candidate = getattr(gate_result, "candidate", None)
        candidate_hash = ""
        if candidate is not None:
            try:
                candidate_hash = _canonical_hash(candidate.to_dict())
            except Exception:
                candidate_hash = ""
        artifact = cls(
            reason=getattr(gate_result, "reason", "TAS gate rejected candidate"),
            code="TAS_GATE_REFUSAL",
            candidate_hash=candidate_hash,
            parent_context=getattr(gate_result, "gate", "unknown"),
            verifier="TAS_ADMISSIBILITY_GATEWAY",
            details={"gate": getattr(gate_result, "gate", "unknown")},
        )
        return artifact._with_receipt_id()

    @classmethod
    def for_reason(
        cls,
        reason: str,
        *,
        code: str = "TAS_OPENAI_REFUSAL",
        candidate_hash: str = "",
        parent_context: str = "",
        verifier: str = "TAS_OPENAI_BRIDGE",
        details: dict[str, Any] | None = None,
    ) -> "RefusalArtifact":
        """Convenience constructor with explicit §11 fields."""
        artifact = cls(
            reason=reason,
            code=code,
            candidate_hash=candidate_hash,
            parent_context=parent_context,
            verifier=verifier,
            details=details or {},
        )
        return artifact._with_receipt_id()

    # ------------------------------------------------------------------ #
    # Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _with_receipt_id(self) -> "RefusalArtifact":
        payload = self._core_payload()
        receipt_id = _canonical_hash(payload)
        object.__setattr__(self, "refusal_receipt_id", receipt_id)
        return self

    def _core_payload(self) -> dict[str, Any]:
        return {
            "reason":          self.reason,
            "code":            self.code,
            "candidate_hash":  self.candidate_hash,
            "rule_version":    self.rule_version,
            "parent_context":  self.parent_context,
            "decision_state":  self.decision_state,
            "verifier":        self.verifier,
            "timestamp":       self.timestamp,
        }

    # ------------------------------------------------------------------ #
    # Serialisation                                                        #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict[str, Any]:
        return {
            **self._core_payload(),
            "action":             self.action,
            "admissible":         self.admissible,
            "details":            dict(self.details),
            "refusal_receipt_id": self.refusal_receipt_id,
        }
# Nonce: 27497
