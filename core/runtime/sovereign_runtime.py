"""Fail-closed forward-pass guardrail for lineage-constrained generation.

The :class:`SovereignRuntime` reference implementation projects the previous
trajectory hash into a deterministic token mask before sampling.  Unvalidated
vocabulary indices receive a large negative logit bias so probability mass can
only remain on cryptographically admissible continuations.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

LOGGER = logging.getLogger(__name__)
DEFAULT_DOMAIN = b"TAS-SOVEREIGN-RUNTIME-LINEAGE-MASK-v1"


@dataclass(frozen=True)
class LineageDecision:
    """Audit record for one guarded generation step."""

    parent_hash: str
    token_id: int
    token_hash: str
    valid_paths: int


class NullCollapse(RuntimeError):
    """Raised when no token satisfies the parent boundary conditions."""


class SovereignRuntime:
    """PyTorch generation guardrail enforcing zero lineage entropy.

    Parameters
    ----------
    model:
        Callable transformer-like model.  It must return either an object with
        a ``logits`` attribute or a tensor-like logits value.
    vocab_size:
        Size of the model vocabulary ``|V|``.
    heartbeat_rate:
        Scaling factor for the unauthorized-token logit penalty.
    valid_threshold:
        Token indices are admissible when the first hash byte is below this
        threshold.  The default creates a sparse but non-empty deterministic
        mask for ordinary vocabularies while still allowing tests to force null
        collapse by setting ``valid_threshold=0``.
    penalty_floor:
        Base negative bias for unauthorized logits.  The injected penalty is
        ``penalty_floor * heartbeat_rate``.
    """

    def __init__(
        self,
        model: Callable[..., Any],
        vocab_size: int,
        *,
        heartbeat_rate: float = 0.5,
        valid_threshold: int = 16,
        penalty_floor: float = 1_000_000_000.0,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        if vocab_size <= 0:
            raise ValueError("vocab_size must be positive")
        if not 0 <= valid_threshold <= 256:
            raise ValueError("valid_threshold must be between 0 and 256")
        if heartbeat_rate <= 0:
            raise ValueError("heartbeat_rate must be positive")
        self.model = model
        self.vocab_size = vocab_size
        self.heartbeat_rate = heartbeat_rate
        self.valid_threshold = valid_threshold
        self.penalty_floor = penalty_floor
        self.logger = logger or LOGGER
        self.decisions: List[LineageDecision] = []

    def valid_token_indices(self, parent_hash: str) -> List[int]:
        """Return deterministic admissible token ids for ``parent_hash``."""
        self._validate_parent_hash(parent_hash)
        valid: List[int] = []
        for token_id in range(self.vocab_size):
            digest = self._token_digest(parent_hash, token_id)
            if digest[0] < self.valid_threshold:
                valid.append(token_id)
        return valid

    def _compute_lineage_mask(self, parent_hash: str, *, device: Any = None) -> Any:
        """Project a parent hash into ``M_t`` as a torch float32 vector."""
        torch = self._torch()
        mask = torch.zeros(self.vocab_size, dtype=torch.float32, device=device)
        indices = self.valid_token_indices(parent_hash)
        if indices:
            mask[torch.tensor(indices, dtype=torch.long, device=device)] = 1.0
        return mask

    def inject_logit_bias(self, logits: Any, parent_hash: str) -> Any:
        """Apply the fail-closed lineage mask to raw logits before softmax."""
        torch = self._torch()
        mask = self._compute_lineage_mask(parent_hash, device=logits.device)
        valid_paths = int(mask.sum().item())
        if valid_paths == 0:
            raise NullCollapse(f"Null collapse: no admissible tokens for parent {parent_hash}")
        while mask.dim() < logits.dim():
            mask = mask.unsqueeze(0)
        penalty = self.penalty_floor * self.heartbeat_rate
        return torch.where(mask.bool(), logits, logits - penalty)

    def sample_next(self, input_ids: Any, parent_hash: str, **model_kwargs: Any) -> int:
        """Run one guarded forward pass and return a validated sampled token id.

        Returns ``-1`` after logging a critical null-collapse event if the mask
        contains no admissible tokens.
        """
        torch = self._torch()
        outputs = self.model(input_ids, **model_kwargs)
        logits = getattr(outputs, "logits", outputs)
        if logits.dim() == 3:
            logits = logits[:, -1, :]
        try:
            biased_logits = self.inject_logit_bias(logits, parent_hash)
        except NullCollapse as exc:
            self.logger.critical("%s", exc)
            return -1
        probabilities = torch.softmax(biased_logits, dim=-1)
        sampled = torch.multinomial(probabilities, num_samples=1)
        token_id = int(sampled.reshape(-1)[0].item())
        token_hash = self.advance_hash(parent_hash, token_id)
        self.decisions.append(
            LineageDecision(
                parent_hash=parent_hash,
                token_id=token_id,
                token_hash=token_hash,
                valid_paths=len(self.valid_token_indices(parent_hash)),
            )
        )
        return token_id

    def advance_hash(self, parent_hash: str, token_id: int) -> str:
        """Derive the next trajectory hash after emitting ``token_id``."""
        return self._token_digest(parent_hash, token_id).hex()

    @staticmethod
    def _validate_parent_hash(parent_hash: str) -> None:
        if len(parent_hash) != 64 or any(c not in "0123456789abcdef" for c in parent_hash):
            raise ValueError("parent_hash must be a 64-character lowercase SHA-256 hex digest")

    @staticmethod
    def _token_digest(parent_hash: str, token_id: int) -> bytes:
        payload = (
            DEFAULT_DOMAIN
            + b"\0"
            + parent_hash.encode("ascii")
            + b"\0"
            + str(token_id).encode("ascii")
        )
        return hashlib.sha256(payload).digest()

    @staticmethod
    def _torch() -> Any:
        try:
            import torch  # type: ignore
        except ImportError as exc:  # pragma: no cover - exercised where torch is absent
            raise RuntimeError("SovereignRuntime forward-pass methods require PyTorch") from exc
        return torch
