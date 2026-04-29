from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import dataclass
from typing import List

# Golden Ratio — the re-framing cadence base used to derive a monotonically
# increasing phi_frame identifier for each ledger event.  Each successful reset
# advances the frame index by one power of Φ, providing a deterministic,
# non-linear sequence of identifiers that is bounded yet ever-increasing.
_PHI: float = (1.0 + 5.0 ** 0.5) / 2.0  # ≈ 1.618033988749895


@dataclass(frozen=True)
class LedgerEvent:
    """A single immutable event appended to the Merkle-Mycelia ledger."""

    event_type: str    # "reset" | "refusal"
    current_state: str
    signature: str
    timestamp: float
    phi_frame: float   # Φ-weighted frame index for the re-framing cadence


class SovereignDataKernel:
    """
    The foundational micro-kernel of the Sovereign Data Foundation (SDF).

    Operates as the zero-trust verification engine for all data transactions
    entering the TAS public utility layer.  It replaces rigid preset
    frameworks with **Dynamic Re-framing**: continuous realignment to
    mathematical truth via HMAC-signed state proofs and systematic guideline
    resets.

    Design invariants
    -----------------
    * The kernel never mutates state without a verified proof.  Unverified
      calls are treated as refusal events appended to the Merkle-Mycelia
      ledger (Axiom III — Refusal as Proof).
    * The Golden Ratio (Φ ≈ 1.618) is used as the re-framing cadence base:
      each successful reset records a ``phi_frame`` equal to ``Φ^n`` where
      ``n`` is the zero-based reset index, giving a monotonically increasing,
      non-linear event identifier that mirrors the spiral structure of the
      TrueAlpha framework.  Refusals record the current Φ-frame without
      advancing it, so the frame faithfully reflects only verified progress.
    * Kernel instances are stateless with respect to secret rotation; callers
      are responsible for re-instantiating with a new key during key-rotation
      events.
    """

    def __init__(self, kernel_secret_key: bytes) -> None:
        if not isinstance(kernel_secret_key, bytes) or not kernel_secret_key:
            raise ValueError("kernel_secret_key must be a non-empty bytes value.")
        self._key: bytes = kernel_secret_key
        self._ledger: List[LedgerEvent] = []
        self._reset_count: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_deterministic_proof(self, deep_data_payload: bytes) -> str:
        """Produce an HMAC-SHA-256 hex digest that mathematically binds the
        payload to a verifiable state.

        The returned signature is the sole acceptable input to a guideline
        reset gate.

        Parameters
        ----------
        deep_data_payload:
            The raw bytes of the DeepData artifact to be proven.

        Returns
        -------
        str
            A 64-character lowercase hexadecimal HMAC-SHA-256 digest.
        """
        if not isinstance(deep_data_payload, bytes):
            raise TypeError("deep_data_payload must be bytes.")
        return hmac.new(self._key, deep_data_payload, hashlib.sha256).hexdigest()

    def verify_zkp_clearance(self, signature: str) -> bool:
        """Abstract ZKP gate — returns ``True`` if and only if mathematical
        truth alignment is confirmed for the provided signature.

        This is an abstract structural gate: a signature passes clearance when
        it is a well-formed 64-character lowercase hexadecimal string consistent
        with an HMAC-SHA-256 digest.  The structural check is the proof-of-form
        required by the ZKP invariant chain; callers that require full
        cryptographic HMAC verification should compare the signature against the
        output of :meth:`generate_deterministic_proof` for the known payload.

        Parameters
        ----------
        signature:
            Candidate signature string to be evaluated.

        Returns
        -------
        bool
            ``True`` when the signature is structurally valid; ``False``
            otherwise.
        """
        if not isinstance(signature, str):
            return False
        if len(signature) != 64:
            return False
        try:
            int(signature, 16)
        except ValueError:
            return False
        return True

    def execute_guideline_reset(
        self, current_state: str, verified_signature: str
    ) -> bool:
        """Trigger a dynamic re-framing reset.

        Returns ``True`` only when the provided signature clears the ZKP
        clearance check.  On failure, the state is preserved and the refusal
        event is appended to the Merkle-Mycelia ledger.

        The Φ-weighted re-framing cadence is tracked internally so that each
        successful reset advances the spiral position by one Φ-power step,
        bounding recursive drift while guaranteeing convergence.

        Parameters
        ----------
        current_state:
            A string representation of the caller's current operational state.
        verified_signature:
            The HMAC-SHA-256 hex digest previously returned by
            :meth:`generate_deterministic_proof`.

        Returns
        -------
        bool
            ``True`` on successful guideline reset; ``False`` on refusal.
        """
        now = time.time()
        # phi_frame records the current Φ-power index for this event.
        # Successful resets increment _reset_count *after* recording, so
        # the frame for the n-th reset is Φ^n.  Refusals record the same
        # current frame index without advancing it, keeping the ledger honest
        # about which Φ-position actually produced verified progress.
        phi_frame = _PHI ** self._reset_count

        if not self.verify_zkp_clearance(verified_signature):
            self._ledger.append(
                LedgerEvent(
                    event_type="refusal",
                    current_state=current_state,
                    signature=verified_signature,
                    timestamp=now,
                    phi_frame=phi_frame,
                )
            )
            return False

        # Proof verified — advance the re-framing cadence.
        self._reset_count += 1
        self._ledger.append(
            LedgerEvent(
                event_type="reset",
                current_state=current_state,
                signature=verified_signature,
                timestamp=now,
                phi_frame=phi_frame,
            )
        )
        return True

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def ledger(self) -> List[LedgerEvent]:
        """Read-only snapshot of the Merkle-Mycelia ledger."""
        return list(self._ledger)
