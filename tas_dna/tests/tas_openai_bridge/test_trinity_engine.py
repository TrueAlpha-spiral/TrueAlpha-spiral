from tas_openai_bridge import ArchetypeAnalysis, SafetyEnvelope, TrinityEngine


def test_trinity_execute_routes_dual_archetypes():
    result = TrinityEngine().execute(
        "Map financial risk corridors and explore alternative safeguards."
    )
    assert result.octopus.archetype == "octopus"
    assert result.raccoon.archetype == "raccoon"
    assert result.balanced_response


def test_reconcile_within_envelope_skips_singularity():
    engine = TrinityEngine(safety_envelope=SafetyEnvelope(pi_staple_max_divergence=0.9))
    octopus = ArchetypeAnalysis(
        archetype="octopus",
        summary="Pattern map: risk, finance, safeguards",
        focus_vector=("risk", "finance", "safeguards"),
    )
    raccoon = ArchetypeAnalysis(
        archetype="raccoon",
        summary="Curiosity probes: risk, safeguards, edge-cases",
        focus_vector=("risk", "safeguards", "edge-cases"),
    )

    result = engine.reconcile(octopus, raccoon)
    assert not result.singularity.triggered
    assert "Within π-staple safety envelope" in result.balanced_response


def test_reconcile_outside_envelope_triggers_singularity():
    engine = TrinityEngine(safety_envelope=SafetyEnvelope(pi_staple_max_divergence=0.2))
    octopus = ArchetypeAnalysis(
        archetype="octopus",
        summary="Pattern map: invariants, ledger, lineage",
        focus_vector=("invariants", "ledger", "lineage"),
    )
    raccoon = ArchetypeAnalysis(
        archetype="raccoon",
        summary="Curiosity probes: pricing, auctions, liquidity",
        focus_vector=("pricing", "auctions", "liquidity"),
    )

    result = engine.reconcile(octopus, raccoon)
    assert result.singularity.triggered
    assert "Singularity event" in result.balanced_response


def test_reconcile_requires_expected_archetype_order():
    engine = TrinityEngine()
    not_octopus = ArchetypeAnalysis(
        archetype="raccoon",
        summary="bad ordering",
        focus_vector=("a",),
    )
    raccoon = ArchetypeAnalysis(
        archetype="raccoon",
        summary="Curiosity probes",
        focus_vector=("b",),
    )

    try:
        engine.reconcile(not_octopus, raccoon)
    except ValueError as exc:
        assert "Expected octopus analysis" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid archetype ordering")
# Nonce: 2936
