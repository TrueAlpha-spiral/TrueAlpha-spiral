"""Deterministic structural-density gate for candidate payloads."""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StabilityAssessment:
    stable: bool
    density: float
    entropy_bits_per_character: float
    canonical_size: int
    threshold: float


class StabilityMonitor:
    """Reject structurally diluted canonical payloads.

    Density is normalized character-level Shannon entropy: ``H / log2(N)``.
    Empty and single-symbol payloads have zero density.  The measure is a
    deterministic heuristic, not a claim about semantic truth.
    """

    def __init__(self, minimum_density: float = 0.15) -> None:
        if not 0.0 <= minimum_density <= 1.0:
            raise ValueError("minimum_density must be between zero and one")
        self.minimum_density = minimum_density

    def assess(self, payload: Any) -> StabilityAssessment:
        try:
            canonical = json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
        except (TypeError, ValueError):
            return StabilityAssessment(False, 0.0, 0.0, 0, self.minimum_density)

        size = len(canonical)
        if size < 2:
            entropy = density = 0.0
        else:
            counts = Counter(canonical)
            entropy = -sum(
                (count / size) * math.log2(count / size)
                for count in counts.values()
            )
            density = entropy / math.log2(size)
        return StabilityAssessment(
            stable=density >= self.minimum_density,
            density=density,
            entropy_bits_per_character=entropy,
            canonical_size=size,
            threshold=self.minimum_density,
        )

    def check_stability(self, payload: Any) -> bool:
        return self.assess(payload).stable
