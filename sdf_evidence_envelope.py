"""SDF Evidence Envelope — the boundary between authentic evidence and truth.

An ``SDFEvidenceEnvelope`` is the canonical object that the Sovereign Data
Foundation (SDF) emits.  TAS consumes it as input to the admissibility
boundary; it never emits it.

The three predicates this module enforces at the boundary
---------------------------------------------------------

.. math::

    \\operatorname{Authentic}(E)
    \\not\\Rightarrow
    \\operatorname{True}(\\operatorname{claim}(E))

    \\operatorname{Authentic}(E)
    \\not\\Rightarrow
    \\operatorname{Authorized}(P)

    \\operatorname{Authentic}(E)
    \\not\\Rightarrow
    \\operatorname{Admissible}(E, C)

``verify_evidence`` returns an ``EvidenceVerdict`` that partitions the three
predicates cleanly so that callers cannot accidentally conflate them:

* ``authentic``      — the signature over the envelope body is valid.
* ``lineage_intact`` — the genesis and parent hashes form a coherent chain.
* ``scope_covered``  — the issuer's authority scope covers the proposal type.
* ``context_match``  — the envelope context matches the current system context.
* ``nonce_fresh``    — the nonce has not been seen before (anti-replay).

``admissible`` is the conjunction of all five AND an external invariant check
supplied by the caller.  Even when ``admissible`` is False, the verdict is a
    deterministic, serialisable record — so that the refusal receipt (ΔS = 0)
carries the same evidentiary quality as an admission receipt.

What is deliberately absent from the envelope
---------------------------------------------

There is no ``truth`` field.  SDF never sets a ``truth`` bit.
"""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Any, FrozenSet, Mapping, Optional, Protocol, Set

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes as crypto_hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)

# ---------------------------------------------------------------------------
# Domain separator — ensures signatures cannot be replayed across TAS
# subsystems even if a key is reused.
# ---------------------------------------------------------------------------

SDF_ENVELOPE_DOMAIN = b"TAS-SDF-ENVELOPE-V1\x00"
SDF_VERDICT_DOMAIN = b"TAS-SDF-VERDICT-V1\x00"

SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# Canonical JSON helpers
# ---------------------------------------------------------------------------


def _canonical_json(obj: Any) -> bytes:
    """Deterministic JSON: sorted keys, no whitespace, UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _domain_hash(domain: bytes, body: Any) -> str:
    return _sha256_hex(domain + _canonical_json(body))


# ---------------------------------------------------------------------------
# Issuer sub-record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SDFIssuer:
    """Identifies the authority that issued the evidence envelope.

    ``authority_id`` is a human-stable identifier (e.g. DID or cert CN).
    ``public_key_b64`` is the base-64 DER-encoded uncompressed secp256k1/
    ed25519 public key used to verify the envelope signature.
    ``credential_ref`` is an opaque reference to a credential registered in
    the SDF lineage DAG — it is checked externally by the caller.
    """

    authority_id: str
    public_key_b64: str
    credential_ref: str

    def public_key_bytes(self) -> bytes:
        return base64.b64decode(self.public_key_b64)


# ---------------------------------------------------------------------------
# Lineage sub-record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SDFLineage:
    """Cryptographic lineage anchoring the envelope in the SDF DAG.

    ``genesis_hash`` — SHA-256 hex of the root artifact that started this
        chain of custody (e.g. TAS_GENOME_V1).
    ``parent_hash``  — SHA-256 hex of the immediately preceding artifact, or
        ``None`` for genesis artifacts.
    ``sequence``     — monotonically increasing integer within this chain.
    """

    genesis_hash: str
    parent_hash: Optional[str]
    sequence: int


class LineageResolver(Protocol):
    """External, read-only source of authenticated ancestry records."""

    def resolve(self, canonical_hash: str) -> "SDFEvidenceEnvelope | None": ...


# ---------------------------------------------------------------------------
# The envelope itself
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SDFEvidenceEnvelope:
    """Canonical SDF evidence object consumed by the TAS admissibility gate.

    Deliberately absent: a ``truth`` field.
    SDF does not decide whether ``claim`` describes reality.
    TAS receives ``(P, E, C, S_n)`` and computes admissibility independently.
    """

    evidence_id: str
    schema_version: int
    claim: Any                  # Arbitrary claim — SDF makes no truth assertion.
    issuer: SDFIssuer
    context: str                # Opaque context identifier.
    lineage: SDFLineage
    issued_at: str              # ISO-8601 timestamp string.
    nonce: str                  # Unique per-issuance string; enables anti-replay.
    signature: str              # base64-encoded signature over the envelope body.
    canonical_hash: str         # SHA-256 of the body before signature.

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "schema_version": self.schema_version,
            "claim": self.claim,
            "issuer": {
                "authority_id": self.issuer.authority_id,
                "public_key_b64": self.issuer.public_key_b64,
                "credential_ref": self.issuer.credential_ref,
            },
            "context": self.context,
            "lineage": {
                "genesis_hash": self.lineage.genesis_hash,
                "parent_hash": self.lineage.parent_hash,
                "sequence": self.lineage.sequence,
            },
            "issued_at": self.issued_at,
            "nonce": self.nonce,
            "signature": self.signature,
            "canonical_hash": self.canonical_hash,
        }

    # ------------------------------------------------------------------
    # Body — the bytes that were signed (excludes signature itself)
    # ------------------------------------------------------------------

    def body_dict(self) -> dict[str, Any]:
        d = self.to_dict()
        d.pop("signature")
        d.pop("canonical_hash")
        return d


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EvidenceVerdict:
    """The result of ``verify_evidence``.

    ``authentic``      — cryptographic signature over the body is valid.
    ``lineage_intact`` — genesis_hash and parent_hash are well-formed 64-char
                         hex strings; sequence is non-negative.
    ``scope_covered``  — the issuer's claimed authority_id appears in the
                         ``authority_scope`` set passed by the caller.
    ``context_match``  — the envelope's ``context`` field equals the
                         ``current_context`` passed by the caller.
    ``nonce_fresh``    — the nonce was not in the ``seen_nonces`` set.
    ``invariant_pass`` — the external invariant supplied by the caller passed.

    ``admissible``     — the conjunction of all six predicates.  Only when
                         this is True may the caller perform a state transition
                         (ΔS ≠ 0).

    ``failed_predicate`` — name of the first failing predicate, or None.
    ``receipt_hash``     — deterministic SHA-256 of the verdict body; serves as
                           an integrity identifier (not signer authentication) regardless of
                           the admission outcome.
    """

    authentic: bool
    lineage_intact: bool
    scope_covered: bool
    context_match: bool
    nonce_fresh: bool
    invariant_pass: bool

    admissible: bool
    failed_predicate: Optional[str]
    receipt_hash: str

    def delta_s(self) -> int:
        """Return 0 (refused) or 1 (admitted).  ΔS is 0 on any refusal."""
        return 1 if self.admissible else 0


# ---------------------------------------------------------------------------
# Predicate evaluation order (short-circuit on first failure)
# ---------------------------------------------------------------------------

_PREDICATE_ORDER: tuple[str, ...] = (
    "authentic",
    "lineage_intact",
    "scope_covered",
    "context_match",
    "nonce_fresh",
    "invariant_pass",
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def verify_evidence(
    envelope: SDFEvidenceEnvelope,
    *,
    authority_scope: FrozenSet[str],
    current_context: str,
    seen_nonces: Set[str],
    invariant_pass: bool,
    trusted_authority_keys: Mapping[str, str] | None = None,
    trusted_credential_keys: Mapping[str, tuple[str, str]] | None = None,
    lineage_resolver: LineageResolver | None = None,
    trusted_genesis_hashes: FrozenSet[str] | None = None,
) -> EvidenceVerdict:
    """Deterministically evaluate all six predicates and return a verdict.

    Short-circuits on the first failure to preserve the fail-closed property:
    no further information is leaked about predicates downstream of the failure.

    Parameters
    ----------
    envelope:
        The ``SDFEvidenceEnvelope`` to evaluate.
    authority_scope:
        The set of ``authority_id`` values whose signatures are accepted for the
        current proposal type.  The caller is responsible for establishing this
        set independently of the envelope itself — the generator cannot supply
        the scope that authorises its own output.
    current_context:
        The context identifier the system is currently operating under.
    seen_nonces:
        The mutable set of nonces already consumed.  If the envelope's nonce is
        present, the predicate ``nonce_fresh`` fails (replay attack).  When the
        verdict is admissible, the caller **must** add the nonce to this set
        before performing the state transition.
    invariant_pass:
        Result of whatever external system-level invariant check the caller has
        already performed (e.g. InvariantPass(P, S_n)).  Separating this from
        the envelope verification ensures neither SDF nor the model can
        manufacture an invariant result.

    Returns
    -------
    EvidenceVerdict
        Always returns a verdict — never raises.  The verdict carries a
        deterministic ``receipt_hash`` usable as a refusal or admission receipt.
    """
    results: dict[str, bool] = {}
    failed: Optional[str] = None

    # --- 1. Authentic -------------------------------------------------------
    results["authentic"] = _check_authentic(
        envelope,
        trusted_authority_keys=trusted_authority_keys,
        trusted_credential_keys=trusted_credential_keys,
    )
    if not results["authentic"]:
        failed = "authentic"

    # --- 2. Lineage intact --------------------------------------------------
    if failed is None:
        results["lineage_intact"] = _check_lineage(
            envelope,
            lineage_resolver=lineage_resolver,
            trusted_genesis_hashes=trusted_genesis_hashes,
            trusted_authority_keys=trusted_authority_keys,
            trusted_credential_keys=trusted_credential_keys,
        )
        if not results["lineage_intact"]:
            failed = "lineage_intact"

    # --- 3. Scope covered ---------------------------------------------------
    if failed is None:
        results["scope_covered"] = envelope.issuer.authority_id in authority_scope
        if not results["scope_covered"]:
            failed = "scope_covered"

    # --- 4. Context match ---------------------------------------------------
    if failed is None:
        results["context_match"] = envelope.context == current_context
        if not results["context_match"]:
            failed = "context_match"

    # --- 5. Nonce fresh -----------------------------------------------------
    if failed is None:
        results["nonce_fresh"] = envelope.nonce not in seen_nonces
        if not results["nonce_fresh"]:
            failed = "nonce_fresh"

    # --- 6. Invariant pass --------------------------------------------------
    if failed is None:
        results["invariant_pass"] = bool(invariant_pass)
        if not results["invariant_pass"]:
            failed = "invariant_pass"

    # Fill remaining predicates as False (they were not evaluated)
    for p in _PREDICATE_ORDER:
        results.setdefault(p, False)

    admissible = failed is None

    # Build the deterministic receipt body
    receipt_body: dict[str, Any] = {
        "evidence_id": envelope.evidence_id,
        "envelope_canonical_hash": envelope.canonical_hash,
        "authentic": results["authentic"],
        "lineage_intact": results["lineage_intact"],
        "scope_covered": results["scope_covered"],
        "context_match": results["context_match"],
        "nonce_fresh": results["nonce_fresh"],
        "invariant_pass": results["invariant_pass"],
        "admissible": admissible,
        "failed_predicate": failed,
        "delta_s": 1 if admissible else 0,
    }
    receipt_hash = _domain_hash(SDF_VERDICT_DOMAIN, receipt_body)

    return EvidenceVerdict(
        authentic=results["authentic"],
        lineage_intact=results["lineage_intact"],
        scope_covered=results["scope_covered"],
        context_match=results["context_match"],
        nonce_fresh=results["nonce_fresh"],
        invariant_pass=results["invariant_pass"],
        admissible=admissible,
        failed_predicate=failed,
        receipt_hash=receipt_hash,
    )


# ---------------------------------------------------------------------------
# Internal predicate implementations
# ---------------------------------------------------------------------------


_HEX_64 = frozenset("0123456789abcdef")


def _is_hex64(s: Any) -> bool:
    return isinstance(s, str) and len(s) == 64 and all(c in _HEX_64 for c in s)


def _check_authentic(
    envelope: SDFEvidenceEnvelope,
    *,
    trusted_authority_keys: Mapping[str, str] | None = None,
    trusted_credential_keys: Mapping[str, tuple[str, str]] | None = None,
) -> bool:
    """Return True iff the envelope signature verifies against the issuer key.

    Supports uncompressed secp256k1 public keys (65 bytes, prefix 0x04).
    When ``trusted_authority_keys`` or ``trusted_credential_keys`` is provided,
    authenticity becomes allowlist-based: the envelope must resolve to a trusted
    key entry and that trusted key must match the envelope key exactly.
    If the key format or signature is invalid, returns False without raising.
    """
    try:
        trusted_key_b64: str | None = None
        if trusted_credential_keys is not None:
            credential = trusted_credential_keys.get(envelope.issuer.credential_ref)
            if credential is not None:
                credential_authority, trusted_key_b64 = credential
                if credential_authority != envelope.issuer.authority_id:
                    return False
        if trusted_key_b64 is None and trusted_authority_keys is not None:
            trusted_key_b64 = trusted_authority_keys.get(
                envelope.issuer.authority_id
            )

        if trusted_key_b64 is not None:
            trusted_pub_bytes = base64.b64decode(trusted_key_b64, validate=True)
            if trusted_pub_bytes != envelope.issuer.public_key_bytes():
                return False
            pub_bytes = trusted_pub_bytes
        elif (
            trusted_authority_keys is not None
            or trusted_credential_keys is not None
        ):
            return False
        else:
            pub_bytes = envelope.issuer.public_key_bytes()

        pub_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), pub_bytes)
        sig_bytes = base64.b64decode(envelope.signature)
        body_bytes = SDF_ENVELOPE_DOMAIN + _canonical_json(envelope.body_dict())
        pub_key.verify(sig_bytes, body_bytes, ec.ECDSA(crypto_hashes.SHA256()))
        return True
    except (InvalidSignature, Exception):
        return False


def _check_lineage(
    envelope: SDFEvidenceEnvelope,
    *,
    lineage_resolver: LineageResolver | None = None,
    trusted_genesis_hashes: FrozenSet[str] | None = None,
    trusted_authority_keys: Mapping[str, str] | None = None,
    trusted_credential_keys: Mapping[str, tuple[str, str]] | None = None,
) -> bool:
    """Prove ancestry by walking an external resolver to a trusted genesis.

    * ``genesis_hash`` must be a 64-char lowercase hex string.
    * ``parent_hash``  must be None (genesis) or a 64-char lowercase hex string.
    * ``sequence``     must be a non-negative integer.
    * If ``sequence`` == 0, ``parent_hash`` must be None.
    * If ``sequence`` >  0, ``parent_hash`` must be a valid hex64.
    * The ``canonical_hash`` stored in the envelope must equal the recomputed
      SHA-256 of the body dict — guards against silent field mutation.
    """
    lin = envelope.lineage
    if not _is_hex64(lin.genesis_hash):
        return False
    if not isinstance(lin.sequence, int) or isinstance(lin.sequence, bool):
        return False
    if lin.sequence < 0:
        return False
    if lin.sequence == 0:
        if lin.parent_hash is not None:
            return False
    else:
        if not _is_hex64(lin.parent_hash):
            return False
    # Recompute canonical_hash to detect any field mutation after construction.
    expected = _domain_hash(SDF_ENVELOPE_DOMAIN, envelope.body_dict())
    if envelope.canonical_hash != expected:
        return False

    # Backwards-compatible structural checking is retained only when neither
    # trust input is supplied.  Consequence-bearing callers supply both.
    if lineage_resolver is None and trusted_genesis_hashes is None:
        return True
    if trusted_genesis_hashes is None:
        return False

    current = envelope
    visited: set[str] = set()
    # The sequence is also a natural, attacker-independent walk bound.
    for _ in range(envelope.lineage.sequence + 1):
        current_hash = current.canonical_hash
        if current_hash in visited:
            return False
        visited.add(current_hash)
        lineage = current.lineage
        if lineage.genesis_hash != envelope.lineage.genesis_hash:
            return False
        if lineage.sequence == 0:
            return (
                lineage.parent_hash is None
                and lineage.genesis_hash in trusted_genesis_hashes
            )
        if lineage_resolver is None or not _is_hex64(lineage.parent_hash):
            return False
        parent = lineage_resolver.resolve(lineage.parent_hash)
        if parent is None:
            return False
        if parent.canonical_hash != lineage.parent_hash:
            return False
        if _domain_hash(SDF_ENVELOPE_DOMAIN, parent.body_dict()) != parent.canonical_hash:
            return False
        if not _check_authentic(
            parent,
            trusted_authority_keys=trusted_authority_keys,
            trusted_credential_keys=trusted_credential_keys,
        ):
            return False
        if parent.lineage.sequence + 1 != lineage.sequence:
            return False
        current = parent
    return False


# ---------------------------------------------------------------------------
# Envelope builder (for tests and SDF-side tooling)
# ---------------------------------------------------------------------------


def build_envelope(
    *,
    evidence_id: str,
    claim: Any,
    issuer_authority_id: str,
    issuer_private_key: ec.EllipticCurvePrivateKey,
    context: str,
    genesis_hash: str,
    parent_hash: Optional[str],
    sequence: int,
    issued_at: str,
    nonce: str,
) -> SDFEvidenceEnvelope:
    """Construct a correctly signed ``SDFEvidenceEnvelope``.

    Used by tests and SDF-side tooling only.  Production SDF systems sign
    envelopes with HSM-managed keys; this builder is a convenience wrapper.
    """
    pub_bytes = issuer_private_key.public_key().public_bytes(
        Encoding.X962, PublicFormat.UncompressedPoint
    )
    pub_b64 = base64.b64encode(pub_bytes).decode()
    issuer = SDFIssuer(
        authority_id=issuer_authority_id,
        public_key_b64=pub_b64,
        credential_ref=f"cred:{issuer_authority_id}",
    )
    lineage = SDFLineage(
        genesis_hash=genesis_hash,
        parent_hash=parent_hash,
        sequence=sequence,
    )
    # Partial envelope (no sig / canonical_hash yet) to compute body
    partial = SDFEvidenceEnvelope(
        evidence_id=evidence_id,
        schema_version=SCHEMA_VERSION,
        claim=claim,
        issuer=issuer,
        context=context,
        lineage=lineage,
        issued_at=issued_at,
        nonce=nonce,
        signature="",
        canonical_hash="",
    )
    body_bytes = SDF_ENVELOPE_DOMAIN + _canonical_json(partial.body_dict())
    sig_bytes = issuer_private_key.sign(body_bytes, ec.ECDSA(crypto_hashes.SHA256()))
    sig_b64 = base64.b64encode(sig_bytes).decode()

    # canonical_hash commits to the body (pre-signature)
    can_hash = _domain_hash(SDF_ENVELOPE_DOMAIN, partial.body_dict())

    return SDFEvidenceEnvelope(
        evidence_id=evidence_id,
        schema_version=SCHEMA_VERSION,
        claim=claim,
        issuer=issuer,
        context=context,
        lineage=lineage,
        issued_at=issued_at,
        nonce=nonce,
        signature=sig_b64,
        canonical_hash=can_hash,
    )
