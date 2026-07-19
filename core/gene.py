"""TASGene: the canonical minimal transition unit.

Implements the G_i structure from §4 of *Intelligent Self-Similar Design in
TrueAlphaSpiral*:

    G_i = (origin, context, authority, operation, parent, invariants, decision, receipt)

Every valid computational unit must carry enough structural information to
establish where it came from, what authorized it, what rules constrained it,
what it produced, and how it connects to the larger organism.  The local
structure carries the grammar of the global structure.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Decision(str, Enum):
    ADMITTED = "ADMITTED"
    REFUSED  = "REFUSED"
    PENDING  = "PENDING"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_hash(obj: Any) -> str:
    """Stable SHA-256 of a JSON-serialisable object."""
    encoded = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class TASGene:
    """Minimal transition unit — the whole constitutional structure in one unit.

    Fields map directly to the G_i tuple:
      - origin:     the initiating intent or prompt (human-sourced)
      - context:    operational frame at the time of the transition
      - authority:  scoped authorization carried into this transition
      - operation:  the candidate action or transformation being proposed
      - parent:     SHA-256 of the parent gene (None at Genesis)
      - invariants: rule labels that were evaluated
      - decision:   ADMITTED | REFUSED | PENDING
      - receipt:    evidentiary record emitted after the decision
    """

    origin: str
    context: str
    authority: str
    operation: str
    parent: str | None
    invariants: tuple[str, ...]
    decision: Decision
    receipt: dict[str, Any]
    gene_id: str = field(default="")
    timestamp: str = field(default_factory=_now_iso)

    # ------------------------------------------------------------------ #
    # Construction helpers                                                 #
    # ------------------------------------------------------------------ #

    @classmethod
    def admit(
        cls,
        *,
        origin: str,
        context: str,
        authority: str,
        operation: str,
        parent: str | None,
        invariants: tuple[str, ...],
        receipt: dict[str, Any],
    ) -> "TASGene":
        """Construct an admitted gene."""
        return cls._build(
            origin=origin,
            context=context,
            authority=authority,
            operation=operation,
            parent=parent,
            invariants=invariants,
            decision=Decision.ADMITTED,
            receipt=receipt,
        )

    @classmethod
    def refuse(
        cls,
        *,
        origin: str,
        context: str,
        authority: str,
        operation: str,
        parent: str | None,
        invariants: tuple[str, ...],
        receipt: dict[str, Any],
    ) -> "TASGene":
        """Construct a refused gene — preserves the negative evidence branch."""
        return cls._build(
            origin=origin,
            context=context,
            authority=authority,
            operation=operation,
            parent=parent,
            invariants=invariants,
            decision=Decision.REFUSED,
            receipt=receipt,
        )

    @classmethod
    def _build(cls, **kwargs: Any) -> "TASGene":
        ts = _now_iso()
        payload = {**kwargs, "timestamp": ts}
        gene_id = _canonical_hash(payload)
        return cls(**kwargs, gene_id=gene_id, timestamp=ts)

    # ------------------------------------------------------------------ #
    # Serialisation                                                        #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict[str, Any]:
        return {
            "gene_id":    self.gene_id,
            "timestamp":  self.timestamp,
            "origin":     self.origin,
            "context":    self.context,
            "authority":  self.authority,
            "operation":  self.operation,
            "parent":     self.parent,
            "invariants": list(self.invariants),
            "decision":   self.decision.value,
            "receipt":    self.receipt,
        }

    def lineage_hash(self) -> str:
        """Hash of just the lineage-bearing fields (parent chain + decision)."""
        return _canonical_hash({
            "gene_id":  self.gene_id,
            "parent":   self.parent,
            "decision": self.decision.value,
        })

    # ------------------------------------------------------------------ #
    # Self-similarity check                                                #
    # ------------------------------------------------------------------ #

    def is_constitutional(self) -> bool:
        """Return True iff the gene carries all required constitutional fields.

        Per §4: no field may be absent.  An empty string for origin or
        authority signals a gap in provenance and fails the check.
        """
        return bool(
            self.origin.strip()
            and self.context.strip()
            and self.authority.strip()
            and self.operation.strip()
            and self.invariants
            and self.decision in Decision
            and isinstance(self.receipt, dict)
        )
