"""ContextSnapshot: immutable semantic environment for candidate evaluation.

Implements §3.2 (Semantic Sovereignty) and §4 (Recursive Contextualization) of
*Sovereign Innovation*.

A ContextSnapshot fixes the exact semantic frame under which a candidate
transition is evaluated.  Every field is committed into the ``snapshot_id``
hash, so the snapshot is tamper-evident.

Interpretive immutability guarantee::

    Meaning(A, t₀) = MeaningUnder(A, C_{t₀})

    NOT:

    Meaning(A, t₀) = MeaningUnder(A, C_current)

Future governance can create a successor ContextSnapshot (setting
``parent_context_id`` to the current snapshot_id).  It cannot retroactively
replace the definitions or invariants under which a historical transition was
evaluated.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Optional, Sequence

from .definition_id import DefinitionID


@dataclass(frozen=True)
class ContextSnapshot:
    """Immutable semantic environment for candidate evaluation.

    Attributes
    ----------
    snapshot_id:
        Self-addressed SHA-256 of the canonical payload (all other fields).
    namespace:
        Governing namespace, must match the namespace of all contained
        DefinitionIDs.
    epoch:
        ISO 8601 timestamp marking when this context became effective.
    definition_ids:
        Ordered tuple of :class:`DefinitionID` instances comprising the
        semantic registry for this context.  Order is significant; the tuple
        is included verbatim in the canonical payload.
    invariant_set:
        Ordered tuple of invariant name strings that all admitted candidates
        must satisfy under this context.
    authority_binding:
        ``snapshot_id`` of the :class:`~core.authority.AuthoritySnapshot` that
        issued this context.  Binds semantic context to institutional authority.
    canonicalization_rules:
        String identifying the hash/encoding/normalisation algorithm, e.g.
        ``"SHA-256/UTF-8/NFC"``.  Must be in
        :data:`~core.verification.universal_verifier.SUPPORTED_CANONICALIZATION`.
    parent_context_id:
        ``snapshot_id`` of the predecessor :class:`ContextSnapshot`, or
        ``None`` for a root context.  Forms an append-only context chain.
    """

    snapshot_id: str
    namespace: str
    epoch: str
    definition_ids: tuple  # tuple of DefinitionID
    invariant_set: tuple   # tuple of str
    authority_binding: str
    canonicalization_rules: str
    parent_context_id: Optional[str]

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        namespace: str,
        epoch: str,
        definition_ids: Sequence[DefinitionID],
        invariant_set: Sequence[str],
        authority_binding: str,
        canonicalization_rules: str = "SHA-256/UTF-8/NFC",
        parent_context_id: Optional[str] = None,
    ) -> "ContextSnapshot":
        """Create and self-address a ContextSnapshot.

        The ``snapshot_id`` is computed as SHA-256 of the JSON-serialised
        canonical payload (all fields except ``snapshot_id`` itself, sorted
        keys).
        """
        payload: dict = {
            "namespace": namespace,
            "epoch": epoch,
            "definition_ids": [str(d) for d in definition_ids],
            "invariant_set": list(invariant_set),
            "authority_binding": authority_binding,
            "canonicalization_rules": canonicalization_rules,
            "parent_context_id": parent_context_id,
        }
        snapshot_id = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        return cls(
            snapshot_id=snapshot_id,
            namespace=namespace,
            epoch=epoch,
            definition_ids=tuple(definition_ids),
            invariant_set=tuple(invariant_set),
            authority_binding=authority_binding,
            canonicalization_rules=canonicalization_rules,
            parent_context_id=parent_context_id,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def is_root(self) -> bool:
        """Returns True if this context has no predecessor."""
        return self.parent_context_id is None

    def contains_definition(self, definition_id: DefinitionID) -> bool:
        """Returns True if the given DefinitionID is registered in this context."""
        return definition_id in self.definition_ids

    def requires_invariant(self, name: str) -> bool:
        """Returns True if the named invariant is required by this context."""
        return name in self.invariant_set

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "namespace": self.namespace,
            "epoch": self.epoch,
            "definition_ids": [
                d.to_dict() if isinstance(d, DefinitionID) else str(d)
                for d in self.definition_ids
            ],
            "invariant_set": list(self.invariant_set),
            "authority_binding": self.authority_binding,
            "canonicalization_rules": self.canonicalization_rules,
            "parent_context_id": self.parent_context_id,
        }
