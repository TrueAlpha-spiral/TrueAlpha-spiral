"""Canonical TAS vertical slice orchestration.

Authority -> Context -> Admission -> TASGene -> WakeChain -> Runtime -> Receipt.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Sequence
import hashlib

from tas_openai_bridge.receipts import ProvenanceReceipt
from tas_openai_bridge.refusal import RefusalArtifact

from .authority.authority_snapshot import AuthoritySnapshot
from .gene import TASGene
from .recovery.phoenix_recovery import PhoenixRecovery, RecoveryRecord
from .runtime.sovereign_runtime import AdmissibilityObject, SovereignRuntime
from .semantics.context_snapshot import ContextSnapshot
from .verification.universal_verifier import UniversalVerifierKernel, VerificationResult
from .wakechain import WakeChain, WakeLink


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _runtime_parent_hash(
    parent_gene_id: str | None, authority: AuthoritySnapshot
) -> str:
    if parent_gene_id is None:
        return authority.snapshot_id
    if parent_gene_id.startswith("sha256:") and len(parent_gene_id) == 71:
        return parent_gene_id.split(":", 1)[1]
    if len(parent_gene_id) == 64 and all(
        c in "0123456789abcdef" for c in parent_gene_id
    ):
        return parent_gene_id
    return hashlib.sha256(parent_gene_id.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class VerticalSliceOutcome:
    admitted: bool
    verification: VerificationResult
    gene: TASGene
    link: WakeLink
    receipt: dict[str, Any]
    runtime_valid_token_indices: tuple[int, ...]
    admissibility: AdmissibilityObject
    recovery: RecoveryRecord | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "admitted": self.admitted,
            "verification": self.verification.to_dict(),
            "gene": self.gene.to_dict(),
            "wake_link": self.link.to_dict(),
            "receipt": self.receipt,
            "runtime_valid_token_indices": list(self.runtime_valid_token_indices),
            "admissibility": {
                **self.admissibility.__dict__,
                "closed_admitted_action_set": list(
                    self.admissibility.closed_admitted_action_set
                ),
            },
            "recovery": self.recovery.to_dict() if self.recovery else None,
        }


class CanonicalVerticalSlice:
    """Single enforced path for TAS transitions."""

    def __init__(
        self,
        *,
        verifier: UniversalVerifierKernel | None = None,
        recovery: PhoenixRecovery | None = None,
        conduit: str = "tas.core.vertical_slice",
    ) -> None:
        self.verifier = verifier or UniversalVerifierKernel()
        self.recovery = recovery or PhoenixRecovery()
        self.conduit = conduit

    def execute(
        self,
        *,
        origin: str,
        operation: str,
        authority: AuthoritySnapshot,
        context: ContextSnapshot,
        wakechain: WakeChain,
        runtime: SovereignRuntime | None = None,
        timestamp: str | None = None,
        parent_gene_id: str | None = None,
        required_invariants: Sequence[str] | None = None,
    ) -> VerticalSliceOutcome:
        if not origin.strip():
            raise ValueError("origin must be a non-empty string")
        if not operation.strip():
            raise ValueError("operation must be a non-empty string")
        if not isinstance(authority, AuthoritySnapshot):
            raise TypeError("authority must be an AuthoritySnapshot")
        if not isinstance(context, ContextSnapshot):
            raise TypeError("context must be a ContextSnapshot")
        if not isinstance(wakechain, WakeChain):
            raise TypeError("wakechain must be a WakeChain")

        evaluated_at = timestamp or _now_iso()
        required = (
            tuple(required_invariants)
            if required_invariants is not None
            else tuple(context.invariant_set)
        )
        parent_id = parent_gene_id
        if parent_id is None and wakechain.head.gene_id:
            parent_id = wakechain.head.gene_id

        candidate = {
            "origin": origin,
            "operation": operation,
            "namespace": context.namespace,
            "parent_gene_id": parent_id,
            "invariants": list(required),
        }
        verification = self.verifier.verify(
            candidate=candidate,
            authority=authority,
            context=context,
            timestamp=evaluated_at,
            parent_gene_id=parent_id,
            required_invariants=required,
        )
        admissibility = AdmissibilityObject.create(
            candidate_hash=verification.candidate_hash,
            authority_snapshot_id=authority.snapshot_id,
            context_snapshot_id=context.snapshot_id,
            closed_admitted_action_set=(operation,) if verification.admitted else (),
            decision="ADMITTED" if verification.admitted else "REFUSED",
            verifier_id=verification.verifier_id,
        )

        runtime_indices: tuple[int, ...] = ()
        runtime_failure: str | None = None
        if verification.admitted and runtime is not None:
            try:
                runtime_parent = _runtime_parent_hash(parent_id, authority)
                runtime.authorize_operation(operation, admissibility)
                runtime_indices = tuple(runtime.valid_token_indices(runtime_parent))
                if not runtime_indices:
                    runtime_failure = "RUNTIME_NULL_COLLAPSE"
            except Exception as exc:
                runtime_failure = f"RUNTIME_FAILURE:{type(exc).__name__}"

        if verification.admitted and runtime_failure is None:
            receipt_obj = ProvenanceReceipt(
                receipt_type="TAS_OPENAI_PROVENANCE_RECEIPT",
                schema_version="1.0",
                human_authority=authority.principal,
                conduit=self.conduit,
                action="ADMIT",
                input_hash=f"sha256:{verification.candidate_hash}",
                output_hash=f"sha256:{verification.candidate_hash}",
                model="tas-core",
                gate=verification.verifier_id,
                admissible=True,
                timestamp=evaluated_at,
            ).with_receipt_id()
            receipt = receipt_obj.to_dict()
            gene = TASGene.admit(
                origin=origin,
                context=context.snapshot_id,
                authority=authority.snapshot_id,
                operation=operation,
                parent=parent_id,
                invariants=required,
                receipt=receipt,
            )
            link = wakechain.append(gene)
            return VerticalSliceOutcome(
                admitted=True,
                verification=verification,
                gene=gene,
                link=link,
                receipt=receipt,
                runtime_valid_token_indices=runtime_indices,
                admissibility=admissibility,
                recovery=None,
            )

        failure_reason = (
            verification.failure_reason if runtime_failure is None else runtime_failure
        )
        failure_code = (
            verification.failure_code if runtime_failure is None else runtime_failure
        )
        refusal = RefusalArtifact.for_reason(
            reason=failure_reason or "Admission refused by canonical vertical slice",
            code=failure_code or "ADMISSION_REFUSED",
            parent_context=context.snapshot_id,
            verifier=verification.verifier_id,
            details={"checks_failed": list(verification.checks_failed)},
        )
        refusal_receipt = refusal.to_dict()
        gene = TASGene.refuse(
            origin=origin,
            context=context.snapshot_id,
            authority=authority.snapshot_id,
            operation=operation,
            parent=parent_id,
            invariants=required
            or tuple(context.invariant_set)
            or ("ADMISSION_REFUSED",),
            receipt=refusal_receipt,
        )
        link = wakechain.append(gene)
        recovery = self.recovery.initiate(
            failure_receipt_ids=[refusal_receipt["refusal_receipt_id"]],
            checkpoint_gene_id=parent_id or "GENESIS",
            initiated_at=evaluated_at,
        )
        return VerticalSliceOutcome(
            admitted=False,
            verification=verification,
            gene=gene,
            link=link,
            receipt=refusal_receipt,
            runtime_valid_token_indices=runtime_indices,
            admissibility=admissibility,
            recovery=recovery,
        )
