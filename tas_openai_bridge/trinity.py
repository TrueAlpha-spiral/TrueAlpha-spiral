"""Trinity Engine cognitive archetypes and safety-envelope reconciliation."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re


TOKEN_PATTERN = re.compile(r"[a-z0-9']+")


def _tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def _jaccard_distance(left: tuple[str, ...], right: tuple[str, ...]) -> float:
    left_set, right_set = set(left), set(right)
    if not left_set and not right_set:
        return 0.0
    union = left_set | right_set
    if not union:
        return 0.0
    similarity = len(left_set & right_set) / len(union)
    return 1.0 - similarity


@dataclass(frozen=True)
class ArchetypeAnalysis:
    archetype: str
    summary: str
    focus_vector: tuple[str, ...]
    confidence: float = 0.5


@dataclass(frozen=True)
class SafetyEnvelope:
    pi_staple_max_divergence: float = 0.55


@dataclass(frozen=True)
class SingularityEvent:
    triggered: bool
    divergence: float
    threshold: float
    reason: str


@dataclass(frozen=True)
class TrinityResult:
    octopus: ArchetypeAnalysis
    raccoon: ArchetypeAnalysis
    singularity: SingularityEvent
    balanced_response: str


class OctopusArchetype:
    """Deep-pattern archetype focused on stable, recurring structure."""

    def analyze(self, query: str) -> ArchetypeAnalysis:
        tokens = _tokenize(query)
        counts = Counter(tokens)
        ranked = [token for token, _ in counts.most_common(6)]
        focus = tuple(ranked[:3])
        if not focus:
            focus = ("signal",)
        summary = "Pattern map: " + ", ".join(focus)
        return ArchetypeAnalysis(
            archetype="octopus",
            summary=summary,
            focus_vector=focus,
            confidence=0.78,
        )


class RaccoonArchetype:
    """Exploratory archetype focused on edge hypotheses and curiosity paths."""

    def analyze(self, query: str) -> ArchetypeAnalysis:
        tokens = _tokenize(query)
        counts = Counter(tokens)
        ascending = sorted(counts.items(), key=lambda item: (item[1], item[0]))
        focus = tuple(token for token, _ in ascending[:3])
        if not focus:
            focus = ("hypothesis",)
        summary = "Curiosity probes: " + ", ".join(focus)
        return ArchetypeAnalysis(
            archetype="raccoon",
            summary=summary,
            focus_vector=focus,
            confidence=0.7,
        )


class SemanticRouter:
    """Routes a query into dual archetype analyses."""

    def __init__(
        self,
        octopus: OctopusArchetype | None = None,
        raccoon: RaccoonArchetype | None = None,
    ):
        self.octopus = octopus or OctopusArchetype()
        self.raccoon = raccoon or RaccoonArchetype()

    def route(self, query: str) -> tuple[ArchetypeAnalysis, ArchetypeAnalysis]:
        return self.octopus.analyze(query), self.raccoon.analyze(query)


class TrinityEngine:
    """Sovereign n+1 reasoning layer with π-staple safety reconciliation."""

    def __init__(
        self,
        router: SemanticRouter | None = None,
        safety_envelope: SafetyEnvelope | None = None,
    ):
        self.router = router or SemanticRouter()
        self.safety_envelope = safety_envelope or SafetyEnvelope()

    def execute(self, query: str) -> TrinityResult:
        octopus, raccoon = self.router.route(query)
        return self.reconcile(octopus, raccoon)

    def reconcile(
        self,
        octopus: ArchetypeAnalysis,
        raccoon: ArchetypeAnalysis,
    ) -> TrinityResult:
        if octopus.archetype != "octopus":
            raise ValueError("Expected octopus analysis for first perspective")
        if raccoon.archetype != "raccoon":
            raise ValueError("Expected raccoon analysis for second perspective")

        divergence = _jaccard_distance(octopus.focus_vector, raccoon.focus_vector)
        triggered = divergence > self.safety_envelope.pi_staple_max_divergence
        if triggered:
            reason = (
                "Singularity event triggered: dual analyses exceeded π-staple "
                "safety envelope and were reconciled into a coherent synthesis."
            )
            balance = (
                "Singularity event: "
                f"{octopus.summary} | {raccoon.summary} | "
                "Balanced synthesis preserved user-controlled coherence."
            )
        else:
            reason = "Dual analyses remained within the π-staple safety envelope."
            balance = (
                "Within π-staple safety envelope: "
                f"{octopus.summary} | {raccoon.summary}"
            )

        event = SingularityEvent(
            triggered=triggered,
            divergence=divergence,
            threshold=self.safety_envelope.pi_staple_max_divergence,
            reason=reason,
        )
        return TrinityResult(
            octopus=octopus,
            raccoon=raccoon,
            singularity=event,
            balanced_response=balance,
        )
# Nonce: 47171
