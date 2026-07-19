"""AuthoritySnapshot: credential envelope for institutional authority.

Implements §3.1 (Institutional Sovereignty) of *Sovereign Innovation*.

An AuthoritySnapshot is the content-addressed representation of a scoped,
time-bounded, revocable institutional mandate.  It does not store the
credential itself — only an opaque reference — so that the snapshot can be
committed to a WakeChain without embedding secrets.

Key doctrinal points
--------------------
* Access to a system is not equivalent to authority over it.
* Possession of a key is not sufficient unless it resolves to an
  authenticated, scoped, unrevoked authority state.
* Cryptography does not *create* authority; it provides evidence that an
  existing authority issued a particular authorization under a particular scope.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class AuthoritySnapshot:
    """Content-addressed institutional authority envelope.

    Attributes
    ----------
    snapshot_id:
        Self-addressed SHA-256 of the canonical payload.
    principal:
        Human or juridical identity string (name, URN, DID, etc.).
    credential_reference:
        Opaque, non-secret reference to the credential (e.g. a key fingerprint,
        HSM slot reference, or credential hash).  Never the credential itself.
    permitted_scope:
        Sorted tuple of operation strings this authority is permitted to
        authorize.  Use ``"*"`` to indicate unrestricted scope only in
        explicitly trusted development contexts.
    effective_epoch:
        ISO 8601 string marking when this authority became effective.
    expiry_epoch:
        ISO 8601 string marking when this authority expires, or ``None`` for
        no automatic expiry.  Revocation is handled separately via
        ``revocation_condition``.
    jurisdiction:
        Legal, institutional, or operational jurisdiction string.
    revocation_condition:
        Human-readable condition under which this authority is to be treated
        as revoked (e.g. ``"Upon written notice from the CISO"``).
    """

    snapshot_id: str
    principal: str
    credential_reference: str
    permitted_scope: tuple        # sorted tuple of str
    effective_epoch: str          # ISO 8601
    expiry_epoch: Optional[str]   # ISO 8601 or None
    jurisdiction: str
    revocation_condition: str

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        principal: str,
        credential_reference: str,
        permitted_scope: Sequence[str],
        effective_epoch: str,
        jurisdiction: str,
        revocation_condition: str,
        expiry_epoch: Optional[str] = None,
    ) -> "AuthoritySnapshot":
        """Create and self-address an AuthoritySnapshot.

        ``permitted_scope`` is sorted before hashing and storage so that two
        snapshots with the same logical scope always produce the same
        ``snapshot_id`` regardless of the order in which scopes were supplied.
        """
        sorted_scope = sorted(set(permitted_scope))
        payload: dict = {
            "principal": principal,
            "credential_reference": credential_reference,
            "permitted_scope": sorted_scope,
            "effective_epoch": effective_epoch,
            "expiry_epoch": expiry_epoch,
            "jurisdiction": jurisdiction,
            "revocation_condition": revocation_condition,
        }
        snapshot_id = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        return cls(
            snapshot_id=snapshot_id,
            principal=principal,
            credential_reference=credential_reference,
            permitted_scope=tuple(sorted_scope),
            effective_epoch=effective_epoch,
            expiry_epoch=expiry_epoch,
            jurisdiction=jurisdiction,
            revocation_condition=revocation_condition,
        )

    # ------------------------------------------------------------------
    # Authority checks
    # ------------------------------------------------------------------

    def permits(self, scope: str) -> bool:
        """Returns True if ``scope`` is within the permitted scope set."""
        return scope in self.permitted_scope

    def is_valid_at(self, timestamp: str) -> bool:
        """Returns True if ``timestamp`` is within [effective_epoch, expiry_epoch].

        Comparison is lexicographic over ISO 8601 strings.  This is valid when
        timestamps share the same precision and timezone offset (e.g. both are
        UTC ``YYYY-MM-DDTHH:MM:SSZ``).  Callers are responsible for ensuring
        consistent timestamp formatting.
        """
        if timestamp < self.effective_epoch:
            return False
        if self.expiry_epoch is not None and timestamp > self.expiry_epoch:
            return False
        return True

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "principal": self.principal,
            "credential_reference": self.credential_reference,
            "permitted_scope": list(self.permitted_scope),
            "effective_epoch": self.effective_epoch,
            "expiry_epoch": self.expiry_epoch,
            "jurisdiction": self.jurisdiction,
            "revocation_condition": self.revocation_condition,
        }
