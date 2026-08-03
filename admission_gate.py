"""Authenticated, context-bound, fail-closed admission decisions.

The gate resolves semantic context before candidate interpretation, then binds
that exact context to an immutable authority checkpoint. Private keys remain
behind ``ReceiptSigner`` and are never reconstructed from public material.
"""

from __future__ import annotations

import base64
import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from context_snapshot import (
    CANONICALIZATION_VERSION,
    CanonicalJSONError,
    ContextResolver,
    ContextSnapshot,
    ContextValidationError,
    DefinitionResolver,
    canonical_hash,
    canonical_json,
    domain_hash,
    parse_canonical_json,
    resolve_verified_context,
)

AUTHORIZATION_DOMAIN = b"TAS-AUTHORITY-GATE-V1\x00"
AUTHORITY_BINDING_DOMAIN = b"TAS-AUTHORITY-BINDING-V1\x00"
RECEIPT_DOMAIN = b"TAS-ADMISSION-RECEIPT-V1\x00"
RULE_SET_VERSION = "TAS-PI-GATE-2"
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_SECP256K1_ORDER = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)


@dataclass(frozen=True)
class AuthoritySnapshot:
    credential_id: str
    algorithm: str
    public_key: bytes
    authority_epoch: int
    revoked: bool
    scope_policy_hash: str
    checkpoint_hash: str
    valid_until: str
    context_snapshot_hash: str | None = None


def authority_binding_hash(snapshot: AuthoritySnapshot) -> str:
    """Hash the non-circular authority projection committed by a context.

    ``context_snapshot_hash`` is excluded: the context commits to this
    projection while the full AuthoritySnapshot separately commits back to the
    context hash. This creates mutual binding without a hash cycle.
    """
    body = {
        "credential_id": snapshot.credential_id,
        "algorithm": snapshot.algorithm,
        "public_key": base64.b64encode(snapshot.public_key).decode(),
        "authority_epoch": snapshot.authority_epoch,
        "revoked": snapshot.revoked,
        "scope_policy_hash": snapshot.scope_policy_hash,
        "checkpoint_hash": snapshot.checkpoint_hash,
        "valid_until": snapshot.valid_until,
    }
    return domain_hash(AUTHORITY_BINDING_DOMAIN, body)


class AuthorityResolver(Protocol):
    def resolve(
        self, *, credential_id: str, checkpoint_hash: str
    ) -> AuthoritySnapshot | None: ...


class SignatureVerifier(Protocol):
    def verify_signature(
        self,
        *,
        algorithm: str,
        public_key: bytes,
        message: bytes,
        signature: bytes,
    ) -> bool: ...


class ReceiptSigner(Protocol):
    @property
    def algorithm(self) -> str: ...

    @property
    def public_key(self) -> bytes: ...

    def sign(self, message: bytes) -> bytes: ...


class DecisionLedger(Protocol):
    def append_decision(
        self, receipt_hash: str, receipt: Mapping[str, Any]
    ) -> None: ...

    def get_receipt(self, receipt_hash: str) -> Mapping[str, Any] | None: ...


class Secp256k1Verifier:
    """DER ECDSA/SHA-256 verifier for compressed SEC1 keys and low-S signatures."""

    algorithm = "ECDSA-secp256k1-SHA256-DER-lowS"

    def verify_signature(
        self,
        *,
        algorithm: str,
        public_key: bytes,
        message: bytes,
        signature: bytes,
    ) -> bool:
        if algorithm != self.algorithm or len(public_key) != 33:
            return False
        try:
            key = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP256K1(), public_key
            )
            _r, s = decode_dss_signature(signature)
            if not 0 < s <= _SECP256K1_ORDER // 2:
                return False
            key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            return True
        except (ValueError, InvalidSignature):
            return False


class Ed25519Verifier:
    """Strict Ed25519 verifier for production authority and receipt proofs."""

    algorithm = "Ed25519"

    def verify_signature(
        self,
        *,
        algorithm: str,
        public_key: bytes,
        message: bytes,
        signature: bytes,
    ) -> bool:
        if algorithm != self.algorithm or len(public_key) != 32:
            return False
        try:
            Ed25519PublicKey.from_public_bytes(public_key).verify(
                signature, message
            )
            return True
        except (ValueError, InvalidSignature):
            return False


class LocalEd25519Signer:
    """Local Ed25519 signer; production deployments can replace it with KMS."""

    algorithm = Ed25519Verifier.algorithm

    def __init__(self, private_key: Ed25519PrivateKey) -> None:
        self._private_key = private_key

    @property
    def public_key(self) -> bytes:
        return self._private_key.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )

    def sign(self, message: bytes) -> bytes:
        return self._private_key.sign(message)


class LocalSecp256k1Signer:
    """Private-key-backed signer suitable for a KMS/HSM adapter replacement."""

    algorithm = Secp256k1Verifier.algorithm

    def __init__(self, private_key: ec.EllipticCurvePrivateKey) -> None:
        if not isinstance(private_key.curve, ec.SECP256K1):
            raise ValueError("receipt signer requires a secp256k1 private key")
        self._private_key = private_key

    @property
    def public_key(self) -> bytes:
        return self._private_key.public_key().public_bytes(
            Encoding.X962, PublicFormat.CompressedPoint
        )

    def sign(self, message: bytes) -> bytes:
        r, s = decode_dss_signature(
            self._private_key.sign(message, ec.ECDSA(hashes.SHA256()))
        )
        from cryptography.hazmat.primitives.asymmetric.utils import (
            encode_dss_signature,
        )

        return encode_dss_signature(r, min(s, _SECP256K1_ORDER - s))


class InMemoryDecisionLedger:
    """Test/development append-only reader; production stores must be durable."""

    def __init__(self) -> None:
        self._records: dict[str, Mapping[str, Any]] = {}

    def append_decision(
        self, receipt_hash: str, receipt: Mapping[str, Any]
    ) -> None:
        if receipt_hash in self._records:
            raise ValueError("receipt hash already recorded")
        self._records[receipt_hash] = dict(receipt)

    def get_receipt(self, receipt_hash: str) -> Mapping[str, Any] | None:
        receipt = self._records.get(receipt_hash)
        return dict(receipt) if receipt else None


class FileDecisionLedger:
    """Append-only, crash-durable receipt store keyed by receipt hash.

    Each canonical receipt is written once to a content-addressed file.  The
    temporary file and directory are fsynced around atomic publication so a
    returned decision remains available after process restart.
    """

    def __init__(self, directory: str | os.PathLike[str]) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, receipt_hash: str) -> Path:
        if not _HEX_64.fullmatch(receipt_hash):
            raise ValueError("invalid receipt hash")
        return self.directory / f"{receipt_hash}.json"

    def append_decision(
        self, receipt_hash: str, receipt: Mapping[str, Any]
    ) -> None:
        payload = canonical_json(receipt)
        if hashlib.sha256(payload).hexdigest() != receipt_hash:
            raise ValueError("receipt hash does not match receipt")
        destination = self._path(receipt_hash)
        temporary = self.directory / f".{receipt_hash}.{os.getpid()}.tmp"
        try:
            descriptor = os.open(
                temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
            )
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, destination)
            except FileExistsError as error:
                raise ValueError("receipt hash already recorded") from error
            temporary.unlink()
            directory_fd = os.open(self.directory, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            temporary.unlink(missing_ok=True)

    def get_receipt(self, receipt_hash: str) -> Mapping[str, Any] | None:
        path = self._path(receipt_hash)
        try:
            raw = path.read_bytes()
        except FileNotFoundError:
            return None
        try:
            receipt = parse_canonical_json(raw)
            valid = (
                canonical_json(receipt) == raw
                and isinstance(receipt, Mapping)
                and canonical_hash(receipt) == receipt_hash
            )
        except CanonicalJSONError:
            valid = False
        if not valid:
            return None
        return dict(receipt)


class AuthenticatedLineageVerifier:
    """Verify bounded, signed receipt ancestry from a ledger reader."""

    def __init__(
        self,
        store: DecisionLedger,
        verifier: SignatureVerifier,
        max_depth: int = 128,
    ) -> None:
        self._store = store
        self._verifier = verifier
        self._max_depth = max_depth

    def verify(self, receipt_hash: str) -> bool:
        seen: set[str] = set()
        child: Mapping[str, Any] | None = None
        current_hash = receipt_hash
        for _ in range(self._max_depth):
            if current_hash in seen or not _HEX_64.fullmatch(current_hash):
                return False
            seen.add(current_hash)
            receipt = self._store.get_receipt(current_hash)
            if (
                receipt is None
                or canonical_hash(receipt) != current_hash
                or not self._valid_signature(receipt)
            ):
                return False
            if (
                child is not None
                and child.get("sequence") != receipt.get("sequence", -1) + 1
            ):
                return False
            parent = receipt.get("parent_receipt_hash")
            if parent is None:
                return receipt.get("sequence") == 0
            if not isinstance(parent, str):
                return False
            child, current_hash = receipt, parent
        return False

    def _valid_signature(self, receipt: Mapping[str, Any]) -> bool:
        try:
            signature = base64.b64decode(receipt["signature"], validate=True)
            public_key = base64.b64decode(
                receipt["gatekeeper_public_key"], validate=True
            )
            body = {
                key: value
                for key, value in receipt.items()
                if key
                not in {
                    "signature",
                    "signature_algorithm",
                    "gatekeeper_public_key",
                }
            }
            return self._verifier.verify_signature(
                algorithm=receipt["signature_algorithm"],
                public_key=public_key,
                message=RECEIPT_DOMAIN + canonical_json(body),
                signature=signature,
            )
        except (KeyError, TypeError, ValueError, CanonicalJSONError):
            return False


class AdmissionGatekeeper:
    """Resolve context first, then authenticate, interpret, sign, and append."""

    _FIELDS = frozenset(
        {
            "schema_version",
            "canonicalization_version",
            "domain_separator",
            "credential_id",
            "authority_checkpoint_hash",
            "authority_epoch",
            "context_snapshot_hash",
            "signature_algorithm",
            "requested_operation",
            "candidate_hash",
            "parent_receipt_hash",
            "nonce",
            "signature",
        }
    )

    def __init__(
        self,
        *,
        gatekeeper_id: str,
        authority_resolver: AuthorityResolver,
        context_resolver: ContextResolver,
        definition_resolver: DefinitionResolver,
        verifier: SignatureVerifier,
        receipt_signer: ReceiptSigner,
        ledger: DecisionLedger,
    ) -> None:
        self.gatekeeper_id = gatekeeper_id
        self.authority_resolver = authority_resolver
        self.context_resolver = context_resolver
        self.definition_resolver = definition_resolver
        self.verifier = verifier
        self.receipt_signer = receipt_signer
        self.ledger = ledger

    def evaluate(
        self, *, raw_candidate: bytes, raw_envelope: bytes, current_time: str
    ) -> dict[str, Any]:
        """Return only a signed-and-appended decision, otherwise fail closed."""
        envelope: Mapping[str, Any] = {}
        snapshot: AuthoritySnapshot | None = None
        context: ContextSnapshot | None = None
        candidate: Any = None
        admitted = False
        failure: str | None = None
        raw_candidate_hash = (
            hashlib.sha256(raw_candidate).hexdigest()
            if isinstance(raw_candidate, bytes)
            else None
        )

        try:
            envelope = parse_canonical_json(raw_envelope)
            self._validate_envelope(envelope)

            # No candidate semantics are interpreted before context verification.
            context = resolve_verified_context(
                context_snapshot_hash=envelope["context_snapshot_hash"],
                context_resolver=self.context_resolver,
                definition_resolver=self.definition_resolver,
            )

            snapshot = self.authority_resolver.resolve(
                credential_id=envelope["credential_id"],
                checkpoint_hash=envelope["authority_checkpoint_hash"],
            )
            if not self._context_authority_valid(envelope, context, snapshot):
                failure = "CONTEXT_AUTHORITY_MISMATCH"
            elif not self._context_lineage_valid(envelope, context):
                failure = "CONTEXT_LINEAGE_REFUSED"
            else:
                candidate = parse_canonical_json(raw_candidate)
                if envelope["candidate_hash"] != canonical_hash(candidate):
                    raise ValueError("candidate binding mismatch")
                admitted = self._authorized(envelope, snapshot, current_time)
                failure = None if admitted else "AUTHORIZATION_REFUSED"
        except ContextValidationError:
            failure = "CONTEXT_REFUSED"
        except Exception as error:
            failure = f"INVALID_INPUT:{type(error).__name__}"

        return self._record(
            envelope=envelope,
            snapshot=snapshot,
            context=context,
            candidate=candidate,
            raw_candidate_hash=raw_candidate_hash,
            current_time=current_time,
            admitted=admitted,
            failure=failure,
        )

    def _validate_envelope(self, envelope: Any) -> None:
        if not isinstance(envelope, dict) or set(envelope) != self._FIELDS:
            raise ValueError("invalid envelope field set")
        if (
            envelope["schema_version"] != 2
            or envelope["canonicalization_version"]
            != CANONICALIZATION_VERSION
        ):
            raise ValueError("unsupported envelope version")
        if envelope["domain_separator"] != "TAS_AUTHORITY_GATE_V1":
            raise ValueError("invalid authorization domain")
        string_fields = (
            "credential_id",
            "signature_algorithm",
            "requested_operation",
            "signature",
            "nonce",
        )
        if not all(
            isinstance(envelope[field], str) and envelope[field]
            for field in string_fields
        ):
            raise ValueError("invalid string envelope field")
        if (
            not isinstance(envelope["authority_epoch"], int)
            or isinstance(envelope["authority_epoch"], bool)
            or not _HEX_64.fullmatch(envelope["authority_checkpoint_hash"])
            or not _HEX_64.fullmatch(envelope["context_snapshot_hash"])
            or not _HEX_64.fullmatch(envelope["candidate_hash"])
            or (
                envelope["parent_receipt_hash"] is not None
                and (
                    not isinstance(envelope["parent_receipt_hash"], str)
                    or not _HEX_64.fullmatch(envelope["parent_receipt_hash"])
                )
            )
        ):
            raise ValueError("invalid envelope identifier field")

    def _context_authority_valid(
        self,
        envelope: Mapping[str, Any],
        context: ContextSnapshot,
        snapshot: AuthoritySnapshot | None,
    ) -> bool:
        if snapshot is None:
            return False
        return (
            snapshot.context_snapshot_hash == context.context_snapshot_hash
            and snapshot.context_snapshot_hash
            == envelope["context_snapshot_hash"]
            and snapshot.checkpoint_hash
            == envelope["authority_checkpoint_hash"]
            and snapshot.authority_epoch == context.effective_epoch
            and context.authority_binding_hash
            == authority_binding_hash(snapshot)
        )

    def _context_lineage_valid(
        self, envelope: Mapping[str, Any], context: ContextSnapshot
    ) -> bool:
        parent_hash = envelope["parent_receipt_hash"]
        if parent_hash is None:
            return True
        parent = self.ledger.get_receipt(parent_hash)
        if parent is None:
            return False
        parent_context_hash = parent.get("context_snapshot_hash")
        return parent_context_hash in {
            context.context_snapshot_hash,
            context.parent_context_hash,
        }

    def _authorized(
        self,
        envelope: Mapping[str, Any],
        snapshot: AuthoritySnapshot | None,
        current_time: str,
    ) -> bool:
        if (
            snapshot is None
            or snapshot.revoked
            or envelope["authority_epoch"] != snapshot.authority_epoch
        ):
            return False
        if (
            envelope["signature_algorithm"] != snapshot.algorithm
            or current_time > snapshot.valid_until
        ):
            return False
        try:
            signature = base64.b64decode(envelope["signature"], validate=True)
        except (ValueError, TypeError):
            return False
        body = {
            key: value
            for key, value in envelope.items()
            if key != "signature"
        }
        return self.verifier.verify_signature(
            algorithm=snapshot.algorithm,
            public_key=snapshot.public_key,
            message=AUTHORIZATION_DOMAIN + canonical_json(body),
            signature=signature,
        )

    def _record(
        self,
        *,
        envelope: Mapping[str, Any],
        snapshot: AuthoritySnapshot | None,
        context: ContextSnapshot | None,
        candidate: Any,
        raw_candidate_hash: str | None,
        current_time: str,
        admitted: bool,
        failure: str | None,
    ) -> dict[str, Any]:
        parent_hash = envelope.get("parent_receipt_hash")
        try:
            if parent_hash is None:
                sequence = 0
            else:
                parent = self.ledger.get_receipt(parent_hash)
                if parent is None or not isinstance(parent.get("sequence"), int):
                    raise ValueError("unknown lineage parent")
                sequence = parent["sequence"] + 1
        except Exception:
            return {
                "resulting_state": "CUTOFF",
                "failure_code": "LINEAGE_UNAVAILABLE",
                "durable_receipt": False,
            }

        decision_material = {
            "nonce": envelope.get("nonce"),
            "declared_candidate_hash": envelope.get("candidate_hash"),
            "context_snapshot_hash": envelope.get("context_snapshot_hash"),
            "evaluated_at": current_time,
        }
        body = {
            "schema_version": 2,
            "canonicalization_version": CANONICALIZATION_VERSION,
            "rule_set_version": RULE_SET_VERSION,
            "gatekeeper_id": self.gatekeeper_id,
            "event_type": "ADMISSION_DECISION",
            "evaluated_at": current_time,
            "sequence": sequence,
            "decision_id": canonical_hash(decision_material),
            "resulting_state": "ADMITTED" if admitted else "REFUSED",
            "credential_id": envelope.get("credential_id"),
            "authority_epoch": (
                snapshot.authority_epoch if snapshot else None
            ),
            "authority_checkpoint_hash": (
                snapshot.checkpoint_hash if snapshot else None
            ),
            "context_snapshot_hash": (
                context.context_snapshot_hash
                if context is not None
                else envelope.get("context_snapshot_hash")
            ),
            "context_parent_hash": (
                context.parent_context_hash if context else None
            ),
            "namespace_id": context.namespace_id if context else None,
            "registry_root": context.registry_root if context else None,
            "invariant_set_id": context.invariant_set_id if context else None,
            "authority_binding_hash": (
                context.authority_binding_hash if context else None
            ),
            "candidate_hash": (
                canonical_hash(candidate) if candidate is not None else None
            ),
            "declared_candidate_hash": envelope.get("candidate_hash"),
            "candidate_bytes_hash": raw_candidate_hash,
            "authorization_envelope_hash": (
                canonical_hash(envelope) if envelope else None
            ),
            "requested_operation": envelope.get("requested_operation"),
            "parent_receipt_hash": parent_hash,
            "nonce": envelope.get("nonce"),
            "failure_code": failure,
        }
        try:
            signature = self.receipt_signer.sign(
                RECEIPT_DOMAIN + canonical_json(body)
            )
            receipt = {
                **body,
                "signature_algorithm": self.receipt_signer.algorithm,
                "gatekeeper_public_key": base64.b64encode(
                    self.receipt_signer.public_key
                ).decode(),
                "signature": base64.b64encode(signature).decode(),
            }
            receipt_hash = canonical_hash(receipt)
            self.ledger.append_decision(receipt_hash, receipt)
            return {
                "resulting_state": body["resulting_state"],
                "durable_receipt": True,
                "receipt_hash": receipt_hash,
                "receipt": receipt,
            }
        except Exception:
            return {
                "resulting_state": "CUTOFF",
                "failure_code": "RECEIPT_PRESERVATION_UNAVAILABLE",
                "durable_receipt": False,
            }
