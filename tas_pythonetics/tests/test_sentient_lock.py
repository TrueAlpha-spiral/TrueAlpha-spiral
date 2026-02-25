import unittest
from unittest.mock import patch, MagicMock
from tas_pythonetics.sentient_lock import verify_kinematic_identity, PhoenixError, TAS_KINEMATIC_PREFIX

class TestSentientLock(unittest.TestCase):

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
        mock_hash.hexdigest.return_value = "0000abcdef123456" # Not 1618

        with patch('hashlib.sha256', return_value=mock_hash):
            with self.assertRaises(PhoenixError) as cm:
                verify_kinematic_identity("invalid_data")
            self.assertIn("Expected prefix '1618'", str(cm.exception))

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
