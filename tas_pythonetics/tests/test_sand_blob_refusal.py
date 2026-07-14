import hashlib
import json
import unittest
from unittest.mock import mock_open, patch

from tas_pythonetics.sentient_lock import SentientLock, TAS_HUMAN_SIG


class TestSandBlobRefusal(unittest.TestCase):
    def test_unlineaged_sand_blob_emits_refusal_artifact(self):
        """Axiom III: unlineaged sand is refused and serialized as evidence."""
        lineage_root = "8b1acd93996120c32a0d98ffa64fd1cc307c7b2e131fd5aae51a7d303f7e139f"
        parent_lineage_hash = lineage_root
        lock = SentientLock(genesis_root=lineage_root, human_sig=TAS_HUMAN_SIG)

        sand_content = (
            'def inert_function():\n'
            '    return "Big Data accumulation without provenance"\n'
        )
        sand_blob = {
            "index": 255,
            "content": sand_content,
            "authenticated_content_weight": 1.0,
            "subjective_context_weight": 0.0,
            "coherence_score": SentientLock.PHI_MINIMUM,
        }

        # Preserve Form and Function so the refusal proves broken Faithfulness.
        raw_payload = f"{sand_blob['index']}:{sand_blob['content']}"
        sand_blob["hash"] = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()
        sand_blob["lineage_hash"] = "UNLINEAGED_SAND_BLOB"

        with patch("builtins.open", mock_open()) as mocked_open:
            admitted = lock.verify_triple(sand_blob, parent_lineage_hash)
            mocked_open.assert_called_once_with("worm_ledger_mock.json", "a")
            handle = mocked_open()
            written_data = "".join(
                call.args[0] for call in handle.write.call_args_list
            )
            serialized = [
                json.loads(line)
                for line in written_data.splitlines()
                if line.strip()
            ]

        self.assertFalse(admitted)
        self.assertEqual(sand_blob["content"], "null_state")
        self.assertEqual(len(lock.refusal_ledger), 1)

        refusal_block = lock.refusal_ledger[0].to_dict()
        self.assertEqual(refusal_block["action"], "REFUSE")
        self.assertFalse(refusal_block["admissible"])
        self.assertEqual(refusal_block["code"], "TAS_SENTIENT_LOCK_REFUSAL")
        self.assertIn("FAITHFULNESS FAILURE", refusal_block["reason"])
        self.assertEqual(
            refusal_block["details"]["human_anchor_witness"], TAS_HUMAN_SIG
        )
        self.assertEqual(refusal_block["details"]["origin_index"], 255)
        self.assertEqual(refusal_block["details"]["status"], "SEVERED")

        # The refusal itself is preserved as an auditable first-class artifact.
        self.assertEqual(serialized, [refusal_block])


if __name__ == "__main__":
    unittest.main()
# Nonce: 36879
