"""
Organic Mechanics for TrueAlphaSpiral (TAS).

Models biological-inspired processing patterns within the TAS framework,
including organic growth cycles, adaptive healing protocols, metabolic
energy management, TAIBOM manifest tracking, and identity validation.

Architect: Russell Nordland
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional


PHI = 1.61803398875  # Golden ratio — organic growth constant

IDENTITY_INVALID_MARKER = "invalid"  # System-wide marker for structurally invalid identities


def _fib_sequence(n: int) -> List[int]:
    """Return the first *n* Fibonacci numbers (starting 1, 1, ...)."""
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


class OrganicSpiralEngine:
    """
    Bio-inspired recursive engine that models organic growth patterns.

    Uses the golden ratio (PHI) and Fibonacci sequences to govern trust
    amplification, mirroring how biological systems grow and adapt.

    Unlike the deterministic ``TruthSpiral``, the ``OrganicSpiralEngine``
    supports adaptive resonance: vitality is amplified each cycle using a
    PHI-weighted Fibonacci ratio, and healing potency scales with accumulated
    adaptation score.
    """

    VIABILITY_THRESHOLD = 0.1

    def __init__(self, max_cycles: int = 8) -> None:
        if max_cycles < 1:
            raise ValueError("max_cycles must be >= 1.")
        self.max_cycles = max_cycles
        self._fib = _fib_sequence(max_cycles + 2)
        self.cycle = 0
        self.vitality = 1.0
        self.adaptation_score = 0.0
        self._fib_index = 0

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_viable(self) -> bool:
        """Return ``True`` if vitality is above the viability threshold."""
        return self.vitality > self.VIABILITY_THRESHOLD

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def grow(self, input_signal: str) -> str:
        """
        Advance one organic growth cycle.

        Returns *input_signal* unchanged if growth is healthy; appends
        ``[ORGANIC_STALL]`` when vitality is critically low, or
        ``[ORGANIC_LIMIT]`` when the cycle ceiling is reached.
        """
        if not self.is_viable():
            return f"{input_signal} [ORGANIC_STALL]"

        if self.cycle >= self.max_cycles:
            return f"{input_signal} [ORGANIC_LIMIT]"

        # PHI-scaled vitality boost: ratio of consecutive Fibonacci numbers
        # converges to 1/PHI, providing natural organic dampening.
        growth_factor = self._fib[self._fib_index] / self._fib[self._fib_index + 1]
        self.vitality = min(1.0, self.vitality * (1.0 + growth_factor / PHI))
        self.cycle += 1
        self._fib_index = min(self._fib_index + 1, len(self._fib) - 2)
        return input_signal

    def absorb_damage(self, damage: float) -> None:
        """Reduce vitality by *damage*, clamped to ``[0.0, 1.0]``."""
        self.vitality = max(0.0, self.vitality - damage)

    def heal(self, potency: float) -> float:
        """
        Attempt a healing pass.

        Healing potency is amplified by the accumulated ``adaptation_score``
        via PHI resonance.  Returns the effective vitality recovery applied.
        """
        amplified = potency * (1.0 + self.adaptation_score / PHI)
        recovery = min(1.0 - self.vitality, amplified)
        self.vitality += recovery
        self.adaptation_score += potency * 0.1
        return recovery

    def reset(self) -> None:
        """Reset the engine to its initial state."""
        self.cycle = 0
        self.vitality = 1.0
        self.adaptation_score = 0.0
        self._fib_index = 0


@dataclass(frozen=True)
class MetabolicSnapshot:
    """Immutable record of metabolic cost at one processing cycle."""

    cycle: int
    atp_consumed: float   # Symbolic ATP: abstract computational energy units
    atp_produced: float
    net_energy: float     # atp_produced - atp_consumed
    efficiency: float     # atp_produced / atp_consumed (0.0 if consumed == 0)


class MetabolicCycle:
    """
    Tracks the metabolic energy budget of TAS processing cycles.

    Inspired by cellular respiration: every meaningful computation
    "consumes" ATP (abstract energy units) and should produce more than
    it consumes for the system to remain metabolically viable.
    """

    ATP_PER_CYCLE_BASE = 1.0
    ATP_HEALING_MULTIPLIER = 2.5  # Healing operations carry higher metabolic cost

    def __init__(self) -> None:
        self._snapshots: List[MetabolicSnapshot] = []
        self._total_consumed: float = 0.0
        self._total_produced: float = 0.0
        self._cycle_counter: int = 0

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_cycle(self, produced: float, healing: bool = False) -> MetabolicSnapshot:
        """
        Record one processing cycle and return its immutable snapshot.

        Args:
            produced: ATP-equivalent energy produced this cycle.
            healing:  Whether this cycle included a healing operation
                      (increases ATP cost by ``ATP_HEALING_MULTIPLIER``).
        """
        consumed = self.ATP_PER_CYCLE_BASE
        if healing:
            consumed *= self.ATP_HEALING_MULTIPLIER

        self._total_consumed += consumed
        self._total_produced += produced
        efficiency = produced / consumed if consumed > 0 else 0.0

        snap = MetabolicSnapshot(
            cycle=self._cycle_counter,
            atp_consumed=consumed,
            atp_produced=produced,
            net_energy=produced - consumed,
            efficiency=efficiency,
        )
        self._snapshots.append(snap)
        self._cycle_counter += 1
        return snap

    # ------------------------------------------------------------------
    # Aggregate metrics
    # ------------------------------------------------------------------

    @property
    def overall_efficiency(self) -> float:
        """Overall ATP efficiency across all recorded cycles."""
        return (self._total_produced / self._total_consumed
                if self._total_consumed > 0 else 0.0)

    @property
    def is_metabolically_viable(self) -> bool:
        """``True`` if at least one cycle has been recorded and cumulative
        ATP production >= consumption."""
        return self._cycle_counter > 0 and self._total_produced >= self._total_consumed

    @property
    def snapshots(self) -> List[MetabolicSnapshot]:
        """Read-only list of all recorded metabolic snapshots."""
        return list(self._snapshots)


# ---------------------------------------------------------------------------
# TAIBOM — TAS AI Bill of Materials
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TAIBOMEntry:
    """
    Immutable record of a single component in the TAS AI Bill of Materials.

    Each entry cryptographically anchors a dependency to its origin, trust
    level, and compliance status — forming the backbone of the TAIBOM ledger.
    """

    name: str
    version: str
    origin: str           # Source URI or provenance identifier
    trust_level: str      # "VERIFIED", "PROVISIONAL", or "UNTRUSTED"
    compliance_tags: tuple = field(default_factory=tuple)

    def __post_init__(self) -> None:
        valid_trust = {"VERIFIED", "PROVISIONAL", "UNTRUSTED"}
        if self.trust_level not in valid_trust:
            raise ValueError(f"trust_level must be one of {valid_trust}.")

    @property
    def fingerprint(self) -> str:
        """SHA-256 fingerprint of the entry's identity fields."""
        payload = f"{self.name}:{self.version}:{self.origin}:{self.trust_level}"
        return hashlib.sha256(payload.encode()).hexdigest()


class TAIBOMManifest:
    """
    Immutable ledger of TAS AI Bill-of-Materials entries.

    Tracks the origin, trust, compliance, and dependencies of every
    component ingested by the TAS system.  Entries can only be appended;
    the manifest cannot be modified or cleared after the fact.
    """

    def __init__(self, manifest_id: str) -> None:
        if not manifest_id:
            raise ValueError("manifest_id must be non-empty.")
        self.manifest_id = manifest_id
        self._entries: List[TAIBOMEntry] = []

    def append(self, entry: TAIBOMEntry) -> None:
        """Append an entry to the manifest ledger."""
        self._entries.append(entry)

    @property
    def entries(self) -> List[TAIBOMEntry]:
        """Read-only snapshot of all recorded entries."""
        return list(self._entries)

    @property
    def verified_count(self) -> int:
        """Number of entries with trust_level == 'VERIFIED'."""
        return sum(1 for e in self._entries if e.trust_level == "VERIFIED")

    @property
    def untrusted_count(self) -> int:
        """Number of entries with trust_level == 'UNTRUSTED'."""
        return sum(1 for e in self._entries if e.trust_level == "UNTRUSTED")

    def is_fully_verified(self) -> bool:
        """``True`` if the manifest is non-empty and all entries are VERIFIED."""
        return len(self._entries) > 0 and self.verified_count == len(self._entries)

    def lookup(self, name: str) -> Optional[TAIBOMEntry]:
        """Return the most recently appended entry with the given name, or ``None``."""
        for entry in reversed(self._entries):
            if entry.name == name:
                return entry
        return None


# ---------------------------------------------------------------------------
# Identity Validation
# ---------------------------------------------------------------------------

class IdentityValidator:
    """
    Validates system identity tokens against the TAS integrity constraints.

    Rejects identities that are empty, structurally invalid, or explicitly
    marked as invalid — enforcing the principle that true intelligence must
    prove its structural integrity before it is allowed to execute.
    """

    def __init__(self, valid_tokens: Optional[List[str]] = None) -> None:
        self._valid_tokens: List[str] = list(valid_tokens) if valid_tokens else []

    def register(self, token: str) -> None:
        """Register a known-valid identity token."""
        if not token or IDENTITY_INVALID_MARKER in token.lower():
            raise ValueError(
                f"Cannot register a token containing '{IDENTITY_INVALID_MARKER}'."
            )
        self._valid_tokens.append(token)

    def validate(self, token: str) -> Dict[str, object]:
        """
        Validate *token* against structural integrity constraints.

        Returns a dict with keys:
          - ``valid`` (bool): whether the token passed all checks
          - ``reason`` (str): human-readable explanation
          - ``fingerprint`` (str | None): SHA-256 of the token if valid
        """
        if not token:
            return {"valid": False, "reason": "Empty token", "fingerprint": None}

        if IDENTITY_INVALID_MARKER in token.lower():
            return {
                "valid": False,
                "reason": f"Token contains prohibited marker '{IDENTITY_INVALID_MARKER}'",
                "fingerprint": None,
            }

        if self._valid_tokens and token not in self._valid_tokens:
            return {
                "valid": False,
                "reason": "Token not in registered valid set",
                "fingerprint": None,
            }

        fp = hashlib.sha256(token.encode()).hexdigest()
        return {"valid": True, "reason": "Token passed integrity check", "fingerprint": fp}

