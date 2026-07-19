import copy
import decimal
import hashlib
import hmac
import json
import math
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple


CANONICALIZATION_VERSION = "TAS-CJSON-1"
RULE_SET_VERSION = "TAS-LOGOS-GATE-1"
RECEIPT_VERSION = "TAS-DECISION-RECEIPT-1"
AUTHORIZATION_DOMAIN = "TAS-LINEAGE-AUTHORIZATION-1"
RECEIPT_DOMAIN = "TAS-GATEKEEPER-RECEIPT-1"

_HASH_RE = re.compile(r"^[0-9a-f]{64}$")


class SovereignStructuralViolation(Exception):
    """Raised when an execution trace violates the mathematical bounds of Log(os)."""

    pass


class GatekeeperError(Exception):
    """Stable, fail-closed gatekeeper error."""

    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class LogosRefusalReceipt:
    nonce: int
    parent_hash: str
    shannon_entropy: float
    logos_density: float
    timestamp: int = field(default_factory=lambda: int(time.time()))
    circuit_broken: bool = True


class LogosValidationLoop:
    """Legacy density gate retained for compatibility with existing callers."""

    def __init__(self, invariant_check: Callable[[], bool], min_density_floor: float = 0.15):
        self._invariant_check = invariant_check
        self._min_density_floor = min_density_floor

    def _calculate_shannon_entropy(self, payload_str: str) -> float:
        if not payload_str:
            return 0.0
        frequencies: Dict[str, int] = {}
        for char in payload_str:
            frequencies[char] = frequencies.get(char, 0) + 1

        entropy = 0.0
        total_chars = len(payload_str)
        for count in frequencies.values():
            p = count / total_chars
            entropy -= p * math.log2(p)
        return entropy

    def evaluate_logos_bounds(
        self, current_state_hash: bytes, manifest: Dict[str, Any], nonce: int
    ) -> bool:
        observed_entropy = 0.0
        logos_density = 1.0
        parent_hash_hex = current_state_hash.hex()

        try:
            lineage_match = manifest.get("lineage_parent_hash") == current_state_hash
            invariants_held = self._invariant_check()
            payload_data = json.dumps(manifest.get("payload_vector", {}), sort_keys=True)
            payload_length = len(payload_data)

            if payload_length > 0:
                observed_entropy = self._calculate_shannon_entropy(payload_data)
                logos_density = (observed_entropy * math.log(payload_length)) / payload_length
            else:
                logos_density = 0.0

            if not (
                lineage_match
                and invariants_held
                and logos_density >= self._min_density_floor
            ):
                raise SovereignStructuralViolation(
                    f"Biconditional collapse. Lineage: {lineage_match}, "
                    f"Invariants: {invariants_held}, Density: {logos_density:.4f} "
                    f"(Floor: {self._min_density_floor})"
                )
            return True

        except Exception as exc:
            self._engage_sentient_lock(
                nonce, parent_hash_hex, observed_entropy, logos_density, str(exc)
            )
            return False

    def _engage_sentient_lock(
        self, nonce: int, parent_hash: str, entropy: float, density: float, fault: str
    ) -> None:
        receipt = LogosRefusalReceipt(
            nonce=nonce,
            parent_hash=parent_hash,
            shannon_entropy=entropy,
            logos_density=density,
        )
        print(f"[SENTIENT_LOCK] Execution context frozen by Logos Layer. Fault: {fault}")
        print(
            "[ITL_RECORD] Non-compliance witness packet compiled:\n"
            f"{json.dumps(receipt.__dict__, default=str, indent=2)}"
        )


class _CanonicalBudget:
    def __init__(self, max_depth: int, max_nodes: int):
        self.max_depth = max_depth
        self.remaining_nodes = max_nodes

    def consume(self, depth: int) -> None:
        if depth > self.max_depth:
            raise GatekeeperError("MAX_DEPTH_EXCEEDED", "JSON nesting exceeds the configured limit.")
        self.remaining_nodes -= 1
        if self.remaining_nodes < 0:
            raise GatekeeperError("MAX_NODES_EXCEEDED", "JSON node count exceeds the configured limit.")


def _reject_duplicate_keys(pairs: Sequence[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GatekeeperError("DUPLICATE_KEY", "Duplicate JSON object keys are forbidden.")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise GatekeeperError("NON_FINITE_NUMBER", f"JSON constant {value!r} is forbidden.")


def _validate_text(value: str) -> None:
    for char in value:
        codepoint = ord(char)
        if 0xD800 <= codepoint <= 0xDFFF:
            raise GatekeeperError("INVALID_UNICODE", "Unicode surrogate code points are forbidden.")


def _canonical_decimal(value: decimal.Decimal) -> bytes:
    """Render a finite Decimal exactly, independently of the active context."""
    if not value.is_finite():
        raise GatekeeperError("NON_FINITE_NUMBER", "Non-finite numbers are forbidden.")

    sign, coefficient, exponent = value.as_tuple()
    if not any(coefficient):
        return b"0"

    # Remove only insignificant trailing coefficient zeros.  Unlike normalize(),
    # this does not round according to decimal.getcontext().prec.
    digits = list(coefficient)
    while digits[-1] == 0:
        digits.pop()
        exponent += 1

    significant_digits = len(digits)
    adjusted = exponent + significant_digits - 1
    if significant_digits > 128 or abs(adjusted) > 308:
        raise GatekeeperError("NUMBER_OUT_OF_RANGE", "Number exceeds canonical numeric bounds.")

    coefficient_text = "".join(str(digit) for digit in digits)
    if exponent >= 0:
        rendered = coefficient_text + ("0" * exponent)
    else:
        decimal_point = len(coefficient_text) + exponent
        if decimal_point > 0:
            rendered = (
                coefficient_text[:decimal_point]
                + "."
                + coefficient_text[decimal_point:]
            )
        else:
            rendered = "0." + ("0" * -decimal_point) + coefficient_text
    if sign:
        rendered = "-" + rendered
    return rendered.encode("ascii")


def _serialize_canonical(
    obj: Any,
    *,
    max_depth: int = 64,
    max_nodes: int = 100_000,
) -> bytes:
    budget = _CanonicalBudget(max_depth=max_depth, max_nodes=max_nodes)

    def encode(value: Any, depth: int) -> bytes:
        budget.consume(depth)

        if value is None:
            return b"null"
        if isinstance(value, bool):
            return b"true" if value else b"false"
        if isinstance(value, int):
            return _canonical_decimal(decimal.Decimal(value))
        if isinstance(value, decimal.Decimal):
            return _canonical_decimal(value)
        if isinstance(value, str):
            _validate_text(value)
            return json.dumps(
                value, ensure_ascii=False, separators=(",", ":")
            ).encode("utf-8")
        if isinstance(value, list):
            return b"[" + b",".join(encode(item, depth + 1) for item in value) + b"]"
        if isinstance(value, dict):
            parts: List[bytes] = []
            for key in sorted(value.keys()):
                if not isinstance(key, str):
                    raise GatekeeperError("NON_STRING_KEY", "JSON object keys must be strings.")
                _validate_text(key)
                encoded_key = json.dumps(
                    key, ensure_ascii=False, separators=(",", ":")
                ).encode("utf-8")
                parts.append(encoded_key + b":" + encode(value[key], depth + 1))
            return b"{" + b",".join(parts) + b"}"

        raise GatekeeperError(
            "UNSUPPORTED_TYPE",
            f"Unsupported value type: {type(value).__name__}.",
        )

    return encode(obj, 0)


class HMACReceiptSigner:
    """Deterministic symmetric signer for tests and closed deployments."""

    algorithm = "HMAC-SHA256"

    def __init__(self, key_id: str, key: bytes):
        if not key_id:
            raise ValueError("key_id must be non-empty")
        if not isinstance(key, bytes) or len(key) < 32:
            raise ValueError("HMAC signing keys must contain at least 32 bytes")
        self.key_id = key_id
        self._key = key

    def sign(self, receipt_bytes: bytes) -> Dict[str, str]:
        domain_bound = RECEIPT_DOMAIN.encode("ascii") + b"\x00" + receipt_bytes
        value = hmac.new(self._key, domain_bound, hashlib.sha256).hexdigest()
        return {
            "algorithm": self.algorithm,
            "key_id": self.key_id,
            "value": value,
        }

    def verify(self, receipt_bytes: bytes, signature: Mapping[str, str]) -> bool:
        if (
            signature.get("algorithm") != self.algorithm
            or signature.get("key_id") != self.key_id
        ):
            return False
        domain_bound = RECEIPT_DOMAIN.encode("ascii") + b"\x00" + receipt_bytes
        expected = hmac.new(self._key, domain_bound, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature.get("value", ""))


class HMACLineageResolver:
    """
    Deterministic credential resolver for regression testing and closed deployments.

    Production public-verification deployments should replace this resolver with
    an asymmetric KMS/HSM-backed verifier.
    """

    algorithm = "HMAC-SHA256"

    def __init__(self, credential_keys: Mapping[str, bytes]):
        if not credential_keys:
            raise ValueError("At least one credential key is required")
        for credential_id, key in credential_keys.items():
            if not credential_id or not isinstance(key, bytes) or len(key) < 32:
                raise ValueError("Each credential must have an id and a 32-byte key")
        self._credential_keys = dict(credential_keys)

    @staticmethod
    def build_envelope(
        payload: Mapping[str, Any], authorization_hash: str
    ) -> Dict[str, Any]:
        lineage = payload.get("lineage", {})
        return {
            "domain": AUTHORIZATION_DOMAIN,
            "canonicalization_version": CANONICALIZATION_VERSION,
            "credential_id": payload.get("credential_id"),
            "authorization_hash": authorization_hash,
            "operation": payload.get("operation"),
            "parent_hash": lineage.get("parent_hash") if isinstance(lineage, dict) else None,
        }

    def sign(self, payload: Mapping[str, Any], authorization_hash: str) -> str:
        credential_id = payload.get("credential_id")
        key = self._credential_keys.get(credential_id)
        if key is None:
            raise GatekeeperError("UNKNOWN_CREDENTIAL", "Credential is not registered.")
        envelope = self.build_envelope(payload, authorization_hash)
        envelope_bytes = _serialize_canonical(envelope)
        value = hmac.new(key, envelope_bytes, hashlib.sha256).hexdigest()
        return f"hmac-sha256:{value}"

    def verify(
        self, payload: Mapping[str, Any], authorization_hash: str
    ) -> Tuple[bool, str]:
        credential_id = payload.get("credential_id")
        key = self._credential_keys.get(credential_id)
        if key is None:
            return False, "UNKNOWN_CREDENTIAL"

        lineage = payload.get("lineage")
        if not isinstance(lineage, dict):
            return False, "INVALID_LINEAGE_OBJECT"

        supplied = lineage.get("signature")
        if not isinstance(supplied, str) or not supplied.startswith("hmac-sha256:"):
            return False, "MALFORMED_SIGNATURE"

        envelope = self.build_envelope(payload, authorization_hash)
        envelope_bytes = _serialize_canonical(envelope)
        expected = hmac.new(key, envelope_bytes, hashlib.sha256).hexdigest()
        actual = supplied.split(":", 1)[1]
        if not hmac.compare_digest(expected, actual):
            return False, "SIGNATURE_MISMATCH"
        return True, "SIGNATURE_VALID"


class TASLogosGatekeeper:
    """Gate 1 deterministic canonicalization, evaluation, and receipt pipeline."""

    def __init__(
        self,
        *,
        receipt_signer: HMACReceiptSigner,
        lineage_verifier: Callable[[Mapping[str, Any], str], Tuple[bool, str]],
        allowed_operations: Optional[Sequence[str]] = None,
        gatekeeper_id: str = "tas_logos_gatekeeper",
        max_raw_payload_bytes: int = 2 * 1024 * 1024,
        max_state_delta_bytes: int = 1024 * 1024,
        max_depth: int = 64,
        max_nodes: int = 100_000,
        clock: Optional[Callable[[], datetime]] = None,
    ):
        if receipt_signer is None or lineage_verifier is None:
            raise ValueError("receipt_signer and lineage_verifier are required")
        self.receipt_signer = receipt_signer
        self.lineage_verifier = lineage_verifier
        self.allowed_operations = frozenset(allowed_operations or ("MUTATE_STATE",))
        self.gatekeeper_id = gatekeeper_id
        self.max_raw_payload_bytes = max_raw_payload_bytes
        self.max_state_delta_bytes = max_state_delta_bytes
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def parse_and_canonicalize(self, raw_payload: bytes) -> Tuple[Dict[str, Any], bytes]:
        if not isinstance(raw_payload, bytes):
            raise GatekeeperError("RAW_TYPE_INVALID", "Raw payload must be bytes.")
        if len(raw_payload) > self.max_raw_payload_bytes:
            raise GatekeeperError("RAW_PAYLOAD_TOO_LARGE", "Raw payload exceeds the configured limit.")

        try:
            text = raw_payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise GatekeeperError("INVALID_UTF8", "Payload is not valid UTF-8.") from exc

        try:
            parsed = json.loads(
                text,
                parse_float=decimal.Decimal,
                parse_int=decimal.Decimal,
                parse_constant=_reject_json_constant,
                object_pairs_hook=_reject_duplicate_keys,
            )
        except GatekeeperError:
            raise
        except RecursionError as exc:
            raise GatekeeperError(
                "MAX_DEPTH_EXCEEDED", "JSON nesting exceeds the configured limit."
            ) from exc
        except (json.JSONDecodeError, decimal.InvalidOperation, ValueError) as exc:
            raise GatekeeperError("MALFORMED_JSON", "Payload is not valid strict JSON.") from exc

        if not isinstance(parsed, dict):
            raise GatekeeperError("ROOT_NOT_OBJECT", "Top-level JSON value must be an object.")

        canonical = _serialize_canonical(
            parsed, max_depth=self.max_depth, max_nodes=self.max_nodes
        )
        return parsed, canonical

    def canonicalize(self, raw_payload: bytes) -> bytes:
        _, canonical = self.parse_and_canonicalize(raw_payload)
        return canonical

    @staticmethod
    def compute_hash(canonical_payload: bytes) -> str:
        return hashlib.sha256(canonical_payload).hexdigest()

    def compute_authorization_hash(self, payload: Mapping[str, Any]) -> str:
        authorization_view = copy.deepcopy(dict(payload))
        lineage = authorization_view.get("lineage")
        if isinstance(lineage, dict):
            lineage.pop("signature", None)
        canonical = _serialize_canonical(
            authorization_view,
            max_depth=self.max_depth,
            max_nodes=self.max_nodes,
        )
        return self.compute_hash(canonical)

    def evaluate_invariants(
        self,
        payload: Dict[str, Any],
        candidate_hash: str,
        authorization_hash: str,
    ) -> Tuple[bool, List[Dict[str, str]]]:
        rules = (
            ("INV_01_STRUCTURE", self._rule_has_mandatory_fields),
            ("INV_02_SIGNATURE", self._rule_valid_lineage_signature),
            ("INV_03_LINEAGE_LOOP", self._rule_no_circular_lineage),
            ("INV_04_RESOURCE_BOUNDS", self._rule_within_resource_limits),
        )

        context = {
            "payload": payload,
            "candidate_hash": candidate_hash,
            "authorization_hash": authorization_hash,
        }
        logs: List[Dict[str, str]] = []
        all_passed = True

        for rule_id, rule in rules:
            try:
                passed, detail_code = rule(context)
            except Exception:
                passed, detail_code = False, "RULE_EXCEPTION"

            logs.append(
                {
                    "rule_id": rule_id,
                    "status": "PASSED" if passed else "FAILED",
                    "detail_code": detail_code,
                }
            )
            all_passed = all_passed and passed

        return all_passed, logs

    def _rule_has_mandatory_fields(
        self, context: Mapping[str, Any]
    ) -> Tuple[bool, str]:
        payload = context["payload"]
        required = {"credential_id", "operation", "lineage", "state_delta"}
        allowed = required | {"context"}

        missing = required - set(payload)
        if missing:
            return False, "MISSING_MANDATORY_FIELDS"
        if set(payload) - allowed:
            return False, "UNKNOWN_TOP_LEVEL_FIELDS"
        if not isinstance(payload.get("credential_id"), str) or not payload["credential_id"]:
            return False, "INVALID_CREDENTIAL_ID"
        if len(payload["credential_id"].encode("utf-8")) > 128:
            return False, "CREDENTIAL_ID_TOO_LONG"
        if payload.get("operation") not in self.allowed_operations:
            return False, "OPERATION_NOT_ALLOWED"
        if not isinstance(payload.get("lineage"), dict):
            return False, "INVALID_LINEAGE_OBJECT"
        if not isinstance(payload.get("state_delta"), dict):
            return False, "INVALID_STATE_DELTA"
        return True, "STRUCTURE_VALID"

    def _rule_valid_lineage_signature(
        self, context: Mapping[str, Any]
    ) -> Tuple[bool, str]:
        payload = context["payload"]
        authorization_hash = context["authorization_hash"]
        lineage = payload.get("lineage")
        if not isinstance(lineage, dict):
            return False, "INVALID_LINEAGE_OBJECT"
        if "signature" not in lineage or "parent_hash" not in lineage:
            return False, "LINEAGE_FIELDS_MISSING"
        return self.lineage_verifier(payload, authorization_hash)

    def _rule_no_circular_lineage(
        self, context: Mapping[str, Any]
    ) -> Tuple[bool, str]:
        payload = context["payload"]
        candidate_hash = context["candidate_hash"]
        lineage = payload.get("lineage")
        if not isinstance(lineage, dict):
            return False, "INVALID_LINEAGE_OBJECT"

        allowed_lineage_fields = {"parent_hash", "signature", "history"}
        if set(lineage) - allowed_lineage_fields:
            return False, "UNKNOWN_LINEAGE_FIELDS"

        parent_hash = lineage.get("parent_hash")
        history = lineage.get("history", [])
        if not isinstance(parent_hash, str) or _HASH_RE.fullmatch(parent_hash) is None:
            return False, "INVALID_PARENT_HASH"
        if not isinstance(history, list):
            return False, "INVALID_HISTORY_TYPE"
        if any(not isinstance(item, str) or _HASH_RE.fullmatch(item) is None for item in history):
            return False, "INVALID_HISTORY_HASH"
        if len(history) != len(set(history)):
            return False, "DUPLICATE_ANCESTOR"
        if parent_hash in history or candidate_hash in history or candidate_hash == parent_hash:
            return False, "CIRCULAR_LINEAGE"
        return True, "LINEAGE_ACYCLIC"

    def _rule_within_resource_limits(
        self, context: Mapping[str, Any]
    ) -> Tuple[bool, str]:
        payload = context["payload"]
        state_delta = payload.get("state_delta")
        if not isinstance(state_delta, dict):
            return False, "INVALID_STATE_DELTA"
        canonical_delta = _serialize_canonical(
            state_delta,
            max_depth=self.max_depth,
            max_nodes=self.max_nodes,
        )
        if len(canonical_delta) > self.max_state_delta_bytes:
            return False, "STATE_DELTA_TOO_LARGE"
        return True, "RESOURCE_BOUNDS_VALID"

    def _timestamp(self) -> str:
        current = self.clock()
        if current.tzinfo is None:
            current = current.replace(tzinfo=timezone.utc)
        return current.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    def _finalize_receipt(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        receipt_bytes = _serialize_canonical(
            receipt, max_depth=self.max_depth, max_nodes=self.max_nodes
        )
        receipt_hash = self.compute_hash(receipt_bytes)
        signature = self.receipt_signer.sign(receipt_bytes)
        return {
            "receipt": receipt,
            "receipt_hash": receipt_hash,
            "receipt_signature": signature,
        }

    def process_payload(self, raw_payload: bytes) -> Dict[str, Any]:
        raw_hash = (
            hashlib.sha256(raw_payload).hexdigest()
            if isinstance(raw_payload, bytes)
            else None
        )

        try:
            payload, canonical_bytes = self.parse_and_canonicalize(raw_payload)
            candidate_hash = self.compute_hash(canonical_bytes)
            authorization_hash = self.compute_authorization_hash(payload)
            admitted, logs = self.evaluate_invariants(
                payload, candidate_hash, authorization_hash
            )
            state = "ADMITTED" if admitted else "REFUSED"
        except GatekeeperError as error:
            # Canonicalization failures are malformed ingress, not evaluated
            # transitions.  Keep them outside the signed receipt pipeline so an
            # unauthenticated sender cannot turn invalid transport into durable
            # constitutional evidence.
            return {
                "state": "INGRESS_REJECTED",
                "candidate_hash": None,
                "authorization_hash": None,
                "raw_payload_hash": raw_hash,
                "error_code": error.code,
            }

        receipt = {
            "receipt_version": RECEIPT_VERSION,
            "gatekeeper_id": self.gatekeeper_id,
            "canonicalization_version": CANONICALIZATION_VERSION,
            "rule_set_version": RULE_SET_VERSION,
            "state": state,
            "evaluated_at": self._timestamp(),
            "raw_payload_hash": raw_hash,
            "candidate_hash": candidate_hash,
            "authorization_hash": authorization_hash,
            "rule_evaluation_logs": logs,
        }
        finalized = self._finalize_receipt(receipt)
        return {
            "state": state,
            "candidate_hash": candidate_hash,
            "authorization_hash": authorization_hash,
            **finalized,
        }
# Nonce: 22278
