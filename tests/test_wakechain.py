"""Tests for core.wakechain — WakeChain evidence chain.

Covers §3 (gated recurrence, dual histories) and §10 (Echosystem / WakeChain).
"""

import pytest
from core.gene import TASGene, Decision
from core.wakechain import WakeChain, WakeLink, LinkKind


RECEIPT_ADMIT = {"receipt_id": "a1", "admissible": True}
RECEIPT_REFUSE = {"receipt_id": "r1", "admissible": False, "rule_version": "TAS-SDF-1.0"}


def _admitted(**kw) -> TASGene:
    defaults = dict(
        origin="human-intent",
        context="test-context",
        authority="HumanAPIKey:test",
        operation="test-op",
        parent=None,
        invariants=("P0", "P1"),
        receipt=RECEIPT_ADMIT,
    )
    defaults.update(kw)
    return TASGene.admit(**defaults)


def _refused(**kw) -> TASGene:
    defaults = dict(
        origin="human-intent",
        context="test-context",
        authority="HumanAPIKey:test",
        operation="bad-op",
        parent=None,
        invariants=("P0",),
        receipt=RECEIPT_REFUSE,
    )
    defaults.update(kw)
    return TASGene.refuse(**defaults)


# ------------------------------------------------------------------ #
# Genesis                                                              #
# ------------------------------------------------------------------ #

class TestGenesis:
    def test_chain_starts_with_genesis_link(self):
        chain = WakeChain.start(author="test")
        assert chain.length == 1
        assert chain.head.kind == LinkKind.GENESIS

    def test_genesis_has_no_parent(self):
        chain = WakeChain.start()
        assert chain.head.parent_hash is None

    def test_genesis_link_hash_is_set(self):
        chain = WakeChain.start()
        assert chain.head.link_hash.startswith("sha256:")


# ------------------------------------------------------------------ #
# Append (§3 gated recurrence)                                        #
# ------------------------------------------------------------------ #

class TestAppend:
    def test_admitted_gene_appended(self):
        chain = WakeChain.start()
        gene = _admitted()
        link = chain.append(gene)
        assert link.kind == LinkKind.ADMISSION
        assert chain.length == 2

    def test_refused_gene_appended_to_evidence_timeline(self):
        """§3: a refusal changes what is *known* without changing state."""
        chain = WakeChain.start()
        gene = _refused()
        link = chain.append(gene)
        assert link.kind == LinkKind.REFUSAL
        assert chain.length == 2

    def test_seq_increments(self):
        chain = WakeChain.start()
        g1 = _admitted()
        g2 = _admitted()
        l1 = chain.append(g1)
        l2 = chain.append(g2)
        assert l1.seq == 1
        assert l2.seq == 2

    def test_parent_hash_chains_correctly(self):
        chain = WakeChain.start()
        l1 = chain.append(_admitted())
        l2 = chain.append(_admitted())
        assert l2.parent_hash == l1.link_hash

    def test_unconstitutional_gene_raises(self):
        chain = WakeChain.start()
        bad_gene = TASGene.admit(
            origin="",          # empty origin — unconstitutional
            context="ctx",
            authority="auth",
            operation="op",
            parent=None,
            invariants=("P0",),
            receipt=RECEIPT_ADMIT,
        )
        with pytest.raises(WakeChain.ConstitutionalError):
            chain.append(bad_gene)


# ------------------------------------------------------------------ #
# Dual histories (§3)                                                  #
# ------------------------------------------------------------------ #

class TestDualHistories:
    def test_evidence_timeline_includes_refusals(self):
        chain = WakeChain.start()
        chain.append(_admitted())
        chain.append(_refused())
        chain.append(_admitted())
        # genesis + 2 admissions + 1 refusal = 4
        assert len(chain.evidence_timeline()) == 4

    def test_state_sequence_excludes_refusals(self):
        """§3: S_n advances only through admitted transitions."""
        chain = WakeChain.start()
        chain.append(_admitted())
        chain.append(_refused())
        chain.append(_admitted())
        # genesis + 2 admissions = 3
        state_links = chain.state_sequence()
        assert len(state_links) == 3
        assert all(lnk.kind in (LinkKind.ADMISSION, LinkKind.GENESIS)
                   for lnk in state_links)


# ------------------------------------------------------------------ #
# Integrity verification                                               #
# ------------------------------------------------------------------ #

class TestIntegrity:
    def test_fresh_chain_passes_integrity(self):
        chain = WakeChain.start()
        chain.append(_admitted())
        chain.append(_refused())
        assert chain.verify_integrity()

    def test_tampered_parent_hash_fails_integrity(self):
        chain = WakeChain.start()
        chain.append(_admitted())
        # Tamper: overwrite parent_hash on the last link
        bad_link = chain._links[-1]
        object.__setattr__(bad_link, "parent_hash", "sha256:" + "0" * 64)
        assert not chain.verify_integrity()


# ------------------------------------------------------------------ #
# Serialisation                                                        #
# ------------------------------------------------------------------ #

class TestSerialisation:
    def test_to_dict_contains_expected_keys(self):
        chain = WakeChain.start()
        chain.append(_admitted())
        d = chain.to_dict()
        assert "length" in d
        assert "head_hash" in d
        assert "links" in d
        assert len(d["links"]) == 2

    def test_link_to_dict_contains_section11_fields(self):
        chain = WakeChain.start()
        link = chain.append(_admitted())
        d = link.to_dict()
        for key in ("seq", "kind", "event_hash", "parent_hash",
                    "gene_id", "timestamp", "link_hash"):
            assert key in d, f"Missing WakeLink field: {key}"
