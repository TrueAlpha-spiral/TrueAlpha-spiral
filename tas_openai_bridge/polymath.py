"""Algorithmic Polymath for coordinated runtime constraints."""

from __future__ import annotations

from typing import Any

from .authority import HumanAPIKey, ScopedAuthority
from .bridge import tas_openai_execute
from .ledger import ImmutableTruthLedger
from .receipts import ProvenanceReceipt
from .refusal import RefusalArtifact


class AlgorithmicPolymath:
    """Coordinates runtime execution under strict authority, lineage, and ledger constraints.

    The Polymath ensures that human intent becomes bounded machine authority through
    trace-bearing, refusal-capable computation. It catches all runtime exceptions
    to emit a RefusalArtifact instead of crashing.
    """

    def __init__(
        self,
        human_api_key: HumanAPIKey | None,
        scoped_authority: ScopedAuthority | None,
        lineage_anchor: str | None,
        ledger: ImmutableTruthLedger,
    ):
        self.human_api_key = human_api_key
        self.scoped_authority = scoped_authority
        self.lineage_anchor = lineage_anchor
        self.ledger = ledger

    def execute(
        self, prompt: str, *, client: Any | None = None, model: str = "gpt-5.5"
    ) -> ProvenanceReceipt | RefusalArtifact:
        """Execute a prompt through the TAS-OpenAI bridge, failing closed on any error."""
        try:
            if not self.human_api_key or not self.human_api_key.validate():
                return RefusalArtifact(reason="Missing or invalid HumanAPI Key")

            if not self.scoped_authority or not self.scoped_authority.active:
                return RefusalArtifact(reason="Missing or inactive scoped authority")

            if not self.lineage_anchor or not self.lineage_anchor.strip():
                return RefusalArtifact(reason="Missing lineage anchor")

            result = tas_openai_execute(
                human_api_key=self.human_api_key,
                scoped_authority=self.scoped_authority,
                prompt=prompt,
                client=client,
                model=model,
            )

            try:
                self.ledger.append(result)
            except Exception as exc:
                return RefusalArtifact(
                    reason="Receipt-path failure",
                    details={"stage": "ledger.append", "error": str(exc)},
                )

            return result

        except Exception as exc:
            return RefusalArtifact(
                reason="Unhandled runtime exception escaped into Polymath",
                details={"error": str(exc)},
            )
