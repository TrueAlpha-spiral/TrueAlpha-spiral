import unittest
from unittest.mock import MagicMock
from tas_pythonetics.hollow_tree import HollowTreePsi
from tas_pythonetics.paradata import ParadoxReconciler

class TestHollowTreePsi(unittest.TestCase):
    def setUp(self):
        self.reconciler = MagicMock(spec=ParadoxReconciler)
        self.reconciler.register_paradox.return_value = 0.8 # Mock high coherence
        self.psi = HollowTreePsi(self.reconciler)

    def test_inject_paradox(self):
        pid = self.psi.inject_paradox("A", "B", "ctx")
        self.assertIsNotNone(pid)
        self.assertEqual(len(self.psi.active_paradoxes), 1)
        self.assertEqual(self.psi.active_paradoxes[0]["coherence"], 0.8)

    def test_prune_fractal_high_coherence(self):
        # Setup: One high coherence item (0.8) and threshold (0.618)
        self.psi.active_paradoxes = [{"id": "1", "coherence": 0.8, "status": "ACTIVE"}]
        self.psi.coherence_threshold = 0.618

        pruned = self.psi.prune_fractal()
        self.assertEqual(pruned, 0)
        self.assertEqual(len(self.psi.active_paradoxes), 1)

    def test_prune_fractal_low_coherence(self):
        # Setup: One low coherence item (0.3)
        self.psi.active_paradoxes = [{"id": "2", "coherence": 0.3, "status": "ACTIVE"}]
        self.psi.coherence_threshold = 0.618

        pruned = self.psi.prune_fractal()
        self.assertEqual(pruned, 1)
        self.assertEqual(len(self.psi.active_paradoxes), 0)
        self.assertEqual(len(self.psi.pruned_branches), 1)

    def test_anneal_simulation_success(self):
        # Setup: One high coherence item (0.9), mock RNG to ensure success
        self.psi.active_paradoxes = [{"id": "3", "coherence": 0.9, "status": "ACTIVE"}]

        # We need to patch random locally for deterministic testing
        # Or, just trust the logic: roll < coherence -> success.
        # But random.random() is non-deterministic. Let's patch it.
        import random
        random.seed(42) # Seed fixed. But better to patch.
        # 0.9 coherence -> high chance.
        # If roll is 0.5 -> success.

        # For simplicity, let's mock the internal call or just rely on probability being high enough?
        # No, unit tests must be deterministic.
        with unittest.mock.patch('random.random', return_value=0.1):
             success = self.psi.anneal_simulation("3")
             self.assertTrue(success)
             self.assertEqual(len(self.psi.resolved_merges), 1)
             self.assertEqual(len(self.psi.active_paradoxes), 0)

    def test_anneal_simulation_failure(self):
        self.psi.active_paradoxes = [{"id": "4", "coherence": 0.2, "status": "ACTIVE"}]

        with unittest.mock.patch('random.random', return_value=0.9):
             success = self.psi.anneal_simulation("4")
             self.assertFalse(success)
             self.assertEqual(len(self.psi.resolved_merges), 0)
             # Friction should increase
             self.assertGreater(self.psi.friction_level, 0.0)

    def test_diagnostics(self):
        self.psi.inject_paradox("A", "B", "ctx")
        diag = self.psi.get_diagnostics()
        self.assertEqual(diag["active_count"], 1)
        self.assertEqual(diag["friction_level"], 0.0)

if __name__ == "__main__":
    unittest.main()
