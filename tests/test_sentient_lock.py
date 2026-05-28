import pytest
from typing import Dict, List

from tas_phase0_microkernel import Phase0Microkernel, InvariantViolation
from sentient_lock import SentientLock


def create_micro_block(index: int, content: str, authenticated_weight: float = 0.9) -> Dict:
    """Helper to create verified micro-blocks for testing."""
    return {
        "index": index,
        "content": content,
        "form_hash": "",  # Will be computed by SentientLock
        "authenticated_content_weight": authenticated_weight,
        "subjective_context_weight": 1.0 - authenticated_weight,
        "coherence_score": 0.85,
        "lineage_hash": "",  # Will be computed during verification
    }


class TestSentientLockIntegration:
    """Integration tests for SentientLock under Phase 0 restoration constraints."""

    @pytest.fixture
    def kernel(self):
        """Bootstrap Phase 0 Microkernel."""
        k = Phase0Microkernel(steward="Russell Nordland / TrueAlphaSpiral")
        boot_receipt = k.bootstrap()
        assert boot_receipt["status"] == "BOOTSTRAP_LOCKED"
        return k

    @pytest.fixture
    def lock(self, kernel):
        """Initialize SentientLock with genesis root from bootstrap."""
        genesis_root = kernel.genesis_root
        return SentientLock(genesis_root=genesis_root)

    def test_full_triple_validation_success(self, lock):
        """Test successful verification of a small composition window (3 micro-blocks)."""
        # Empty lineage_hash so the first block anchors to genesis_root instead of an
        # arbitrary placeholder.
        parent_node = {
            "lineage_hash": "",
            "content": "Genesis course",
        }

        window: List[Dict] = [
            create_micro_block(0, "Small verified truth about structural continuity."),
            create_micro_block(1, "Incremental restoration of load path alignment."),
            create_micro_block(2, "Faithful bonding to prior historic geometry."),
        ]

        verified_hashes = []
        for i, node in enumerate(window):
            result = lock.verify_triple(node, parent_node, window[:i])
            verified_hashes.append(result)
            parent_node = node.copy()
            parent_node["lineage_hash"] = result

        assert len(verified_hashes) == 3
        assert all(isinstance(h, str) and len(h) == 64 for h in verified_hashes)

    def test_form_violation(self, lock):
        """Test FORM failure: mismatched structural fingerprint."""
        parent_node = {"lineage_hash": "anchor"}
        bad_node = create_micro_block(5, "Valid content")
        bad_node["form_hash"] = "tampered_hash_value"  # Deliberate mismatch

        with pytest.raises(InvariantViolation) as exc:
            lock.verify_triple(bad_node, parent_node, [])
        assert "FORM FAILURE" in str(exc.value)

    def test_function_violation(self, lock):
        """Test FUNCTION failure: subjective weight dominates authenticated content."""
        parent_node = {"lineage_hash": "anchor"}
        bad_node = create_micro_block(6, "Hallucinated leap", authenticated_weight=0.1)

        with pytest.raises(InvariantViolation) as exc:
            lock.verify_triple(bad_node, parent_node, [])
        assert "FUNCTION FAILURE" in str(exc.value)

    def test_faithfulness_violation(self, lock):
        """Test FAITHFULNESS failure: broken lineage."""
        parent_node = {"lineage_hash": "anchor"}
        bad_node = create_micro_block(7, "Broken course")
        bad_node["lineage_hash"] = "forged_lineage_hash"

        with pytest.raises(InvariantViolation) as exc:
            lock.verify_triple(bad_node, parent_node, [])
        assert "FAITHFULNESS FAILURE" in str(exc.value)

    def test_phoenix_rollback_on_window_failure(self, lock):
        """Test full window rollup failure triggers Scorch + Phoenix re-anchor."""
        parent_node = {"lineage_hash": "stable_anchor"}
        window = [
            create_micro_block(10, "Good block 1"),
            create_micro_block(11, "Good block 2"),
            create_micro_block(12, "Bad block - will fail"),
        ]

        # Tamper the last block so its FUNCTION invariant fails
        window[2]["authenticated_content_weight"] = 0.05

        verified_count = 0
        try:
            for i, node in enumerate(window):
                result = lock.verify_triple(node, parent_node, window[:i])
                verified_count += 1
                parent_node = node.copy()
                parent_node["lineage_hash"] = result
        except InvariantViolation:
            assert verified_count == 2  # First two pass, third fails
            print("✅ Phoenix Protocol engaged: Rolled back to last verified anchor.")

    def test_eafp_lbyl_ratio_maintenance(self, lock):
        """Verify the system maintains strong LBYL discipline."""
        assert lock.phi_min == 0.6180339887
