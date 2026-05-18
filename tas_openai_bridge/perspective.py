"""Perspective Intelligence (π_i) kernel for TAS admissibility.

The kernel encodes the rule of engagement:

- No perspective without provenance.
- No provenance without authority.
- No authority without receipt.
- No witnessed intent, no transformation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any

PHI = (1 + math.sqrt(5)) / 2


class GateStatus(str, Enum):
    """Terminal Perspective Intelligence gate states."""

    ADMITTED = "ADMITTED"
    REFUSED = "REFUSED"


@dataclass(frozen=True)
class PerspectiveOperator:
    """Irrational observability operator for witnessed human intent."""

    observer_locus: str
    human_api_key_id: str
    data_anchor: str
    temporal_index: int
    curvature_value: float

    def has_observer_locus(self) -> bool:
        try:
            return bool(self.observer_locus.strip())
        except (AttributeError, TypeError):
            return False

    def compute_curvature_ratio(self, authority_diameter: float) -> float:
        try:
            diameter = float(authority_diameter)
            curvature = float(self.curvature_value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Authority diameter and curvature must be numeric.") from exc

        if diameter <= 0:
            raise ValueError("Authority diameter must be positive.")
        return curvature / diameter


@dataclass(frozen=True)
class PerspectiveProvenanceReceipt:
    """Minimal receipt trace required before perspective may enter state."""

    receipt_id: str
    identity_anchor: str
    lineage_hash: str

    def is_valid_trace(self) -> bool:
        try:
            return all(
                [
                    self.receipt_id.strip(),
                    self.identity_anchor.strip(),
                    self.lineage_hash.strip(),
                ]
            )
        except (AttributeError, TypeError):
            return False


@dataclass(frozen=True)
class LedgerAuthority:
    """Authority diameter enforced by lineage, invariant law, and receipts."""

    root_anchor: str
    authority_diameter: float

    def verifies(self, identity_anchor: str) -> bool:
        try:
            return bool(identity_anchor.strip()) and bool(self.root_anchor.strip())
        except (AttributeError, TypeError):
            return False


@dataclass(frozen=True)
class PerspectiveGateResult:
    """Structured output of the Perspective Intelligence gate."""

    status: GateStatus
    reason: str
    pi_i_ratio: float | None = None
    receipt_id: str | None = None

    @property
    def admissible(self) -> bool:
        return self.status is GateStatus.ADMITTED


@dataclass(frozen=True)
class PerspectiveContext:
    """Convenience bundle for bridge-level perspective validation."""

    pi_i: PerspectiveOperator
    provenance_receipt: PerspectiveProvenanceReceipt
    ledger_authority: LedgerAuthority
    resonance_threshold: float = PHI


def validate_perspective_operator(
    pi_i: Any,
    provenance_receipt: Any,
    ledger_authority: Any,
    resonance_threshold: float = PHI,
) -> PerspectiveGateResult:
    """Validate Perspective Intelligence before a transformation is admitted.

    Truth is perspective-bound without being perspective-determined: witnessed
    intent may introduce contextual curvature, but the Φ-bounded authority
    diameter decides whether that curvature is structurally admissible.
    """

    try:
        has_observer = bool(pi_i.has_observer_locus())
    except (AttributeError, TypeError, ValueError):
        has_observer = False

    if not has_observer:
        return PerspectiveGateResult(
            status=GateStatus.REFUSED,
            reason="Unwitnessed Intent Void",
        )

    try:
        valid_trace = bool(provenance_receipt.is_valid_trace())
    except (AttributeError, TypeError, ValueError):
        valid_trace = False

    if not valid_trace:
        return PerspectiveGateResult(
            status=GateStatus.REFUSED,
            reason="No Perspective Without Provenance",
        )

    try:
        verified = bool(ledger_authority.verifies(provenance_receipt.identity_anchor))
    except (AttributeError, TypeError, ValueError):
        verified = False

    if not verified:
        return PerspectiveGateResult(
            status=GateStatus.REFUSED,
            reason="No Provenance Without Authority",
        )

    try:
        ratio = pi_i.compute_curvature_ratio(ledger_authority.authority_diameter)
        threshold = float(resonance_threshold)
    except (AttributeError, TypeError, ValueError) as exc:
        return PerspectiveGateResult(
            status=GateStatus.REFUSED,
            reason=f"Invalid Authority Diameter: {exc}",
        )

    if ratio > threshold:
        return PerspectiveGateResult(
            status=GateStatus.REFUSED,
            reason="Recursive Dissociation Threat - Exceeds Structural Bounds",
            pi_i_ratio=ratio,
        )

    return PerspectiveGateResult(
        status=GateStatus.ADMITTED,
        reason="Perspective Intelligence Admitted",
        pi_i_ratio=ratio,
        receipt_id=provenance_receipt.receipt_id,
    )


def validate_perspective_context(context: Any) -> PerspectiveGateResult:
    """Validate a bundled perspective context without raw-crashing."""

    try:
        return validate_perspective_operator(
            context.pi_i,
            context.provenance_receipt,
            context.ledger_authority,
            context.resonance_threshold,
        )
    except (AttributeError, TypeError, ValueError) as exc:
        return PerspectiveGateResult(
            status=GateStatus.REFUSED,
            reason=f"Invalid Perspective Context: {exc}",
        )
