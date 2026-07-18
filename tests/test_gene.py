"""Tests for core.gene — TASGene constitutional unit.

Covers §4 (G_i structure) and §11 (self-similarity of failures).
"""

import pytest
from core.gene import TASGene, Decision


SAMPLE_RECEIPT = {"receipt_id": "r1", "gate": "TAS", "admissible": True}
SAMPLE_REFUSED_RECEIPT = {"receipt_id": "r0", "gate": "TAS", "admissible": False,
                          "rule_version": "TAS-SDF-1.0"}


def _base_kwargs(**overrides):
    defaults = dict(
        origin="Russell Nordland — human intent",
        context="IOC preparation cycle",
        authority="HumanAPIKey:rn-001",
        operation="sequence README.md",
        parent=None,
        invariants=("P0", "P1", "Rκ"),
        receipt=SAMPLE_RECEIPT,
    )
    defaults.update(overrides)
    return defaults


# ------------------------------------------------------------------ #
# Construction                                                         #
# ------------------------------------------------------------------ #

class TestConstruction:
    def test_admit_creates_admitted_gene(self):
        gene = TASGene.admit(**_base_kwargs())
        assert gene.decision == Decision.ADMITTED

    def test_refuse_creates_refused_gene(self):
        gene = TASGene.refuse(**_base_kwargs(receipt=SAMPLE_REFUSED_RECEIPT))
        assert gene.decision == Decision.REFUSED

    def test_gene_id_is_deterministic_hash(self):
        g1 = TASGene.admit(**_base_kwargs())
        assert g1.gene_id.startswith("sha256:")
        assert len(g1.gene_id) == 7 + 64  # "sha256:" + 64 hex chars

    def test_parent_none_at_genesis(self):
        gene = TASGene.admit(**_base_kwargs(parent=None))
        assert gene.parent is None

    def test_parent_carries_forward(self):
        g1 = TASGene.admit(**_base_kwargs())
        g2 = TASGene.admit(**_base_kwargs(parent=g1.gene_id))
        assert g2.parent == g1.gene_id


# ------------------------------------------------------------------ #
# Constitutional check (§4)                                           #
# ------------------------------------------------------------------ #

class TestConstitutionalCheck:
    def test_well_formed_gene_is_constitutional(self):
        gene = TASGene.admit(**_base_kwargs())
        assert gene.is_constitutional()

    def test_empty_origin_fails_constitutional(self):
        gene = TASGene.admit(**_base_kwargs(origin=""))
        assert not gene.is_constitutional()

    def test_empty_authority_fails_constitutional(self):
        gene = TASGene.admit(**_base_kwargs(authority=""))
        assert not gene.is_constitutional()

    def test_empty_invariants_fails_constitutional(self):
        gene = TASGene.admit(**_base_kwargs(invariants=()))
        assert not gene.is_constitutional()

    def test_refused_gene_is_constitutional(self):
        """§11: refusals must be as structurally sound as admissions."""
        gene = TASGene.refuse(**_base_kwargs(receipt=SAMPLE_REFUSED_RECEIPT))
        assert gene.is_constitutional()


# ------------------------------------------------------------------ #
# Serialisation                                                        #
# ------------------------------------------------------------------ #

class TestSerialisation:
    def test_to_dict_contains_all_gi_fields(self):
        gene = TASGene.admit(**_base_kwargs())
        d = gene.to_dict()
        for key in ("gene_id", "origin", "context", "authority", "operation",
                    "parent", "invariants", "decision", "receipt", "timestamp"):
            assert key in d, f"Missing field: {key}"

    def test_invariants_serialised_as_list(self):
        gene = TASGene.admit(**_base_kwargs())
        assert isinstance(gene.to_dict()["invariants"], list)

    def test_lineage_hash_changes_with_decision(self):
        g_admit = TASGene.admit(**_base_kwargs())
        g_refuse = TASGene.refuse(**_base_kwargs(receipt=SAMPLE_REFUSED_RECEIPT))
        # Same payload except decision → different lineage hashes
        assert g_admit.lineage_hash() != g_refuse.lineage_hash()
