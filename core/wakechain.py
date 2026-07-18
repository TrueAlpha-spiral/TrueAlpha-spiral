"""WakeChain: append-only chronological evidence structure.

Implements the WakeChain described in §10 of *Intelligent Self-Similar Design
in TrueAlphaSpiral*:

    Prompt → Intent → Authority → Execution Gate →
    State Change or Refusal → Receipt → Witness

WakeChain carries the echo of every action.  Each link binds:
  - its own hash
  - a sequence number
  - a parent receipt hash (None at Genesis)
  - event metadata
  - authentication

Two parallel histories are maintained (§3):
  - the *evidence timeline*  E_n → E_{n+1}  (admissions AND refusals)
  - the *state sequence*     S_n → S_{n+1}  (admissions only)

A refusal changes what is known about the system without changing the
authorised operational state.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterator

from .gene import TASGene, Decision, _canonical_hash


# ------------------------------------------------------------------ #
# Link                                                                #
# ------------------------------------------------------------------ #

class LinkKind(str, Enum):
    ADMISSION = "ADMISSION"
    REFUSAL   = "REFUSAL"
    GENESIS   = "GENESIS"


@dataclass(frozen=True)
class WakeLink:
    """One link in the WakeChain evidence timeline.

    Every link — whether an admission or a refusal — follows the same
    evidentiary discipline.  That is self-similarity at the branch level.
    """

    seq: int
    kind: LinkKind
    event_hash: str          # hash of the gene or genesis payload
    parent_hash: str | None  # hash of the previous link (None at seq=0)
    gene_id: str | None      # gene_id of the TASGene that produced this link
    metadata: dict[str, Any]
    timestamp: str
    link_hash: str = field(default="")

    @classmethod
    def genesis(cls, author: str) -> "WakeLink":
        ts = datetime.now(timezone.utc).isoformat()
        payload: dict[str, Any] = {
            "seq": 0,
            "kind": LinkKind.GENESIS.value,
            "author": author,
            "timestamp": ts,
        }
        event_hash = _canonical_hash(payload)
        link = cls(
            seq=0,
            kind=LinkKind.GENESIS,
            event_hash=event_hash,
            parent_hash=None,
            gene_id=None,
            metadata={"author": author},
            timestamp=ts,
        )
        return link._with_hash()

    @classmethod
    def from_gene(cls, gene: TASGene, seq: int, parent_hash: str | None) -> "WakeLink":
        kind = (
            LinkKind.ADMISSION if gene.decision == Decision.ADMITTED else LinkKind.REFUSAL
        )
        ts = datetime.now(timezone.utc).isoformat()
        link = cls(
            seq=seq,
            kind=kind,
            event_hash=gene.lineage_hash(),
            parent_hash=parent_hash,
            gene_id=gene.gene_id,
            metadata=gene.to_dict(),
            timestamp=ts,
        )
        return link._with_hash()

    # ------------------------------------------------------------------ #

    def _with_hash(self) -> "WakeLink":
        payload = {
            "seq":         self.seq,
            "kind":        self.kind.value,
            "event_hash":  self.event_hash,
            "parent_hash": self.parent_hash,
            "gene_id":     self.gene_id,
            "timestamp":   self.timestamp,
        }
        object.__setattr__(self, "link_hash", _canonical_hash(payload))
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "seq":         self.seq,
            "kind":        self.kind.value,
            "event_hash":  self.event_hash,
            "parent_hash": self.parent_hash,
            "gene_id":     self.gene_id,
            "metadata":    self.metadata,
            "timestamp":   self.timestamp,
            "link_hash":   self.link_hash,
        }


# ------------------------------------------------------------------ #
# WakeChain                                                           #
# ------------------------------------------------------------------ #

class WakeChain:
    """Append-only chronological evidence chain.

    Usage::

        chain = WakeChain.start(author="RN")
        chain.append(gene)          # admitted or refused — both are recorded
        admitted = chain.state_sequence()   # only admitted genes

    The chain is fail-closed: appending a gene that has no constitutional
    form raises ``ConstitutionalError`` rather than silently corrupting the
    evidence timeline.
    """

    class ConstitutionalError(ValueError):
        """Raised when a gene fails the constitutional completeness check."""

    def __init__(self, genesis_link: WakeLink) -> None:
        self._links: list[WakeLink] = [genesis_link]

    # ------------------------------------------------------------------ #
    # Factory                                                             #
    # ------------------------------------------------------------------ #

    @classmethod
    def start(cls, author: str = "TAS") -> "WakeChain":
        """Initialise a new chain from Genesis."""
        return cls(WakeLink.genesis(author=author))

    # ------------------------------------------------------------------ #
    # Mutation (append-only)                                              #
    # ------------------------------------------------------------------ #

    def append(self, gene: TASGene) -> WakeLink:
        """Record a gene on the evidence timeline.

        Both admitted and refused genes are recorded.  Refusals change what
        is *known* about the system; they do not change the authorised state.
        Raises ``ConstitutionalError`` if the gene is not constitutional.
        """
        if not gene.is_constitutional():
            raise self.ConstitutionalError(
                f"Gene {gene.gene_id!r} is not constitutional — "
                "all fields (origin, context, authority, operation, "
                "invariants, decision, receipt) must be present."
            )
        parent_hash = self._links[-1].link_hash
        link = WakeLink.from_gene(gene, seq=len(self._links), parent_hash=parent_hash)
        self._links.append(link)
        return link

    # ------------------------------------------------------------------ #
    # Queries                                                             #
    # ------------------------------------------------------------------ #

    @property
    def head(self) -> WakeLink:
        return self._links[-1]

    @property
    def length(self) -> int:
        return len(self._links)

    def evidence_timeline(self) -> list[WakeLink]:
        """All links — admissions and refusals (E_n sequence)."""
        return list(self._links)

    def state_sequence(self) -> list[WakeLink]:
        """Only admitted links — the authorised state progression (S_n sequence)."""
        return [lnk for lnk in self._links if lnk.kind in (LinkKind.ADMISSION, LinkKind.GENESIS)]

    def verify_integrity(self) -> bool:
        """Walk the chain and confirm every parent_hash reference is consistent."""
        for i, link in enumerate(self._links):
            if i == 0:
                if link.parent_hash is not None:
                    return False
                continue
            if link.parent_hash != self._links[i - 1].link_hash:
                return False
        return True

    def __iter__(self) -> Iterator[WakeLink]:
        return iter(self._links)

    def __len__(self) -> int:
        return self.length

    def to_dict(self) -> dict[str, Any]:
        return {
            "length": self.length,
            "head_hash": self.head.link_hash,
            "links": [lnk.to_dict() for lnk in self._links],
        }
