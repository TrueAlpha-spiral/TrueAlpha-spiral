"""DefinitionID: content-addressed, versioned semantic definition unit.

Implements §3.2 (Semantic Sovereignty) and §4 (Recursive Contextualization) of
*Sovereign Innovation: Global Computational Capability Under Locally Accountable
Authority*.

A DefinitionID pins the exact meaning of a policy term, ontology entry, or
governance concept at a given version.  Future governance may create successor
DefinitionIDs; it cannot silently replace the content_hash of an existing one.

Usage::

    did = DefinitionID.from_content(
        namespace="TAS-SDF",
        name="safe",
        version="1.0",
        content="An action is safe if it produces no irreversible side-effects "
                "outside the declared execution boundary.",
    )
    str(did)  # "TAS-SDF:safe@1.0#a3f8e2b1c4d9f7e0"
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class DefinitionID:
    """Content-addressed semantic definition unit.

    Attributes
    ----------
    namespace:
        Governing namespace, e.g. ``"TAS-SDF"`` or ``"TAS-OT-1"``.
    name:
        Definition name within the namespace, e.g. ``"safe"`` or ``"authorized"``.
    version:
        Semver-style version string, e.g. ``"1.0"`` or ``"2.1.3"``.
    content_hash:
        SHA-256 hex digest of the canonical UTF-8-encoded definition text.
        Two DefinitionIDs with the same namespace/name/version but different
        content_hash values represent distinct, incompatible definitions.
    """

    namespace: str
    name: str
    version: str
    content_hash: str  # SHA-256 hex of canonical UTF-8 definition text

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_content(
        cls,
        namespace: str,
        name: str,
        version: str,
        content: str,
    ) -> "DefinitionID":
        """Create a DefinitionID from the canonical definition text.

        The ``content_hash`` is computed as SHA-256 over the UTF-8 encoding of
        ``content``.  Callers are responsible for normalising whitespace and
        encoding (NFC Unicode) before passing ``content``.
        """
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return cls(
            namespace=namespace,
            name=name,
            version=version,
            content_hash=content_hash,
        )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Short canonical form: ``namespace:name@version#hash_prefix``."""
        return f"{self.namespace}:{self.name}@{self.version}#{self.content_hash[:16]}"

    def canonical_id(self) -> str:
        """Full canonical form including the complete content hash."""
        return f"{self.namespace}:{self.name}@{self.version}#{self.content_hash}"

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "namespace": self.namespace,
            "name": self.name,
            "version": self.version,
            "content_hash": self.content_hash,
        }
