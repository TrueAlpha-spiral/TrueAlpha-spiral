import unittest
import hashlib
import hmac
from unittest.mock import patch, MagicMock
from tas_pythonetics.sentient_lock import verify_kinematic_identity, PhoenixError, TAS_KINEMATIC_PREFIX, SentientLock, StructuralIntegrityError, DilithiumSigner, calculate_structural_density, TAS_STRUCTURAL_DENSITY_MINIMUM

class TestSentientLock(unittest.TestCase):


    def setUp(self):
        self.genesis_root = "K_0_ROOT_HASH_MOCK"
        self.human_sig = "Russell Nordland"
        self.lock = SentientLock(self.genesis_root, self.human_sig)

        self.valid_node = {
            "index": 1,
            "content": "Valid Content",
            "authenticated_content_weight": 0.8,
            "subjective_context_weight": 0.2,
            "coherence_score": 0.618034
        }

        # Calculate valid form hash
        raw_payload = f"1:Valid Content"
        self.valid_node["hash"] = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

        self.parent_hash = "PARENT_HASH_MOCK"

        # Calculate valid lineage hash
        lineage_payload = f"{self.valid_node['hash']}:{self.parent_hash}"
        self.valid_node["lineage_hash"] = DilithiumSigner.sign(self.genesis_root.encode('utf-8'), lineage_payload.encode('utf-8'))

    def test_verify_triple_pass(self):
        result = self.lock.verify_triple(self.valid_node, self.parent_hash)
        self.assertTrue(result)
        self.assertEqual(len(self.lock.refusal_ledger), 0)

    def test_verify_triple_fail_form(self):
        faulty_node = self.valid_node.copy()
        faulty_node["hash"] = "invalid_hash"
        result = self.lock.verify_triple(faulty_node, self.parent_hash)
        self.assertFalse(result)
        self.assertEqual(len(self.lock.refusal_ledger), 1)
        self.assertEqual(faulty_node["content"], "null_state")
        self.assertIn("FORM FAILURE", self.lock.refusal_ledger[0].reason)

    def test_verify_triple_fail_function_subjective_weight(self):
        faulty_node = self.valid_node.copy()
        faulty_node["subjective_context_weight"] = 0.9
        result = self.lock.verify_triple(faulty_node, self.parent_hash)
        self.assertFalse(result)
        self.assertEqual(len(self.lock.refusal_ledger), 1)
        self.assertEqual(faulty_node["content"], "null_state")
        self.assertIn("FUNCTION FAILURE", self.lock.refusal_ledger[0].reason)

    def test_verify_triple_fail_function_coherence(self):
        faulty_node = self.valid_node.copy()
        faulty_node["coherence_score"] = 0.5
        result = self.lock.verify_triple(faulty_node, self.parent_hash)
        self.assertFalse(result)
        self.assertEqual(len(self.lock.refusal_ledger), 1)
        self.assertEqual(faulty_node["content"], "null_state")
        self.assertIn("FUNCTION FAILURE", self.lock.refusal_ledger[0].reason)

    def test_verify_triple_fail_faithfulness(self):
        faulty_node = self.valid_node.copy()
        faulty_node["lineage_hash"] = "invalid_lineage"
        result = self.lock.verify_triple(faulty_node, self.parent_hash)
        self.assertFalse(result)
        self.assertEqual(len(self.lock.refusal_ledger), 1)
        self.assertEqual(faulty_node["content"], "null_state")
        self.assertIn("FAITHFULNESS FAILURE", self.lock.refusal_ledger[0].reason)


    def test_structural_density_rejects_diluted_repetition(self):
        padded_loop = "A" * 100 + " " * 900

        self.assertLess(calculate_structural_density(padded_loop), TAS_STRUCTURAL_DENSITY_MINIMUM)
        with self.assertRaises(PhoenixError) as cm:
            verify_kinematic_identity(padded_loop)

        self.assertIn("Structural density", str(cm.exception))

    def test_verify_kinematic_identity_pass(self):
        # Mock sha256 to return a hash starting with the correct prefix
        mock_hash = MagicMock()
        mock_hash.hexdigest.return_value = TAS_KINEMATIC_PREFIX + "abcdef1234567890"

        with patch('hashlib.sha256', return_value=mock_hash):
            result = verify_kinematic_identity("valid_data")
            self.assertTrue(result)

    def test_verify_kinematic_identity_fail(self):
        # Mock sha256 to return a hash with incorrect prefix
        mock_hash = MagicMock()
        bad_prefix = "0" if TAS_KINEMATIC_PREFIX[0] != "0" else "1"
        mock_hash.hexdigest.return_value = f"{bad_prefix}000abcdef123456"

        with patch('hashlib.sha256', return_value=mock_hash):
            with self.assertRaises(PhoenixError) as cm:
                verify_kinematic_identity("invalid_data")
            self.assertIn(f"Expected prefix '{TAS_KINEMATIC_PREFIX}'", str(cm.exception))

    def test_verify_kinematic_identity_signature(self):
        # Ensure signature is used in payload
        # We can't easily check the input to sha256 with a simple patch on the result,
        # but we can patch hashlib.sha256 and check call args.

        mock_hash = MagicMock()
        mock_hash.hexdigest.return_value = TAS_KINEMATIC_PREFIX + "valid"

        with patch('hashlib.sha256', return_value=mock_hash) as mock_sha256:
            verify_kinematic_identity("data", signature="TEST_SIG")

            # Verify called with data + signature
            expected_payload = "dataTEST_SIG".encode()
            mock_sha256.assert_called_with(expected_payload)

if __name__ == '__main__':
    unittest.main()
# Nonce: 166897
