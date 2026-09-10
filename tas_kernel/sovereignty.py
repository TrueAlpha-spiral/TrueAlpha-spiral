"""Executable primitives for the Canonical Sovereignty Theorem.

The kernel mediates consequences, not proposals.  It refuses an action unless
both its proposed trajectory and agency coordinate are valid, and it records a
timeout rather than applying a transition when the bounded fairness premise is
not satisfied.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    Protocol,
    TypeAlias,
    TypeVar,
    runtime_checkable,
)
from uuid import uuid4

S = TypeVar("S")
X = TypeVar("X")


@runtime_checkable
class AdmissibilityPredicate(Protocol[S, X]):
    """Decide whether applying ``action`` to ``state`` is admissible."""

    def is_admissible(self, state: S, action: X) -> bool:
        """Return a deterministic admissibility verdict."""
        ...


@runtime_checkable
class AuthenticatedAgencyCoordinate(Protocol[X]):
    """Authenticate the authority attached to an action."""

    def authenticate(self, action: X) -> bool:
        """Return whether the action carries valid, sufficient authority."""
        ...


class ReceiptStatus(str, Enum):
    COMMITTED = "COMMITTED"
    REFUSED = "REFUSED"
    TIMEOUT = "TIMEOUT"


class ViolationCode(str, Enum):
    INADMISSIBLE_TRAJECTORY = "E_INADMISSIBLE_TRAJECTORY"
    AUTHENTICATION_FAILURE = "E_AUTHENTICATION_FAILURE"


def _receipt_id() -> str:
    return str(uuid4())


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class ParadataReceipt:
    receipt_id: str
    timestamp: str
    status: ReceiptStatus
    elapsed_ms: int
    metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RefusalReceipt:
    receipt_id: str
    timestamp: str
    status: ReceiptStatus
    violation_codes: tuple[ViolationCode, ...]
    metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["violation_codes"] = [code.value for code in self.violation_codes]
        return payload


@dataclass(frozen=True, slots=True)
class TimeoutReceipt:
    receipt_id: str
    timestamp: str
    status: ReceiptStatus
    timeout_ms: int
    reason: str
    metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


Receipt: TypeAlias = ParadataReceipt | RefusalReceipt | TimeoutReceipt


class SovereignKernel(Generic[S, X]):
    """Apply a transition only after sovereign safety and liveness checks.

    ``fairness`` represents the theorem's bounded scheduling premise ``F_T``.
    A false value is the Axiom of Exhaustion: no transition function is called
    and a :class:`TimeoutReceipt` is emitted.
    """

    def __init__(
        self,
        admissibility: AdmissibilityPredicate[S, X],
        agency: AuthenticatedAgencyCoordinate[X],
        transition_fn: Callable[[S, X], S] | None = None,
    ) -> None:
        self._admissibility = admissibility
        self._agency = agency
        self._transition_fn = transition_fn

    def execute(
        self,
        state: S,
        action: X,
        *,
        fairness: bool = True,
        timeout_ms: int = 0,
        metadata: Mapping[str, Any] | None = None,
    ) -> tuple[S, Receipt]:
        """Evaluate ``action`` and return the resulting state and receipt.

        Safety checks precede the fairness check so an inadmissible action can
        never be misreported as a scheduling failure.  Multiple failed safety
        premises are preserved together in the refusal receipt.
        """
        if timeout_ms < 0:
            raise ValueError("timeout_ms must be non-negative")

        receipt_metadata = dict(metadata or {})
        violations: list[ViolationCode] = []
        if not self._admissibility.is_admissible(state, action):
            violations.append(ViolationCode.INADMISSIBLE_TRAJECTORY)
        if not self._agency.authenticate(action):
            violations.append(ViolationCode.AUTHENTICATION_FAILURE)

        if violations:
            return state, RefusalReceipt(
                receipt_id=_receipt_id(),
                timestamp=_timestamp(),
                status=ReceiptStatus.REFUSED,
                violation_codes=tuple(violations),
                metadata=receipt_metadata,
            )

        if not fairness:
            return state, TimeoutReceipt(
                receipt_id=_receipt_id(),
                timestamp=_timestamp(),
                status=ReceiptStatus.TIMEOUT,
                timeout_ms=timeout_ms,
                reason="AXIOM_OF_EXHAUSTION",
                metadata=receipt_metadata,
            )

        next_state = self._transition_fn(state, action) if self._transition_fn else state
        return next_state, ParadataReceipt(
            receipt_id=_receipt_id(),
            timestamp=_timestamp(),
            status=ReceiptStatus.COMMITTED,
            elapsed_ms=0,
            metadata=receipt_metadata,
        )
