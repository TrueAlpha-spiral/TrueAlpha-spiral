import unittest
import subprocess
import json
import os
import sys

# Constants for Kinematic Identity
TAS_HUMAN_SIG = "Russell Nordland"
TAS_KINEMATIC_PREFIX = "1618"

class TestTASMCPServer(unittest.TestCase):
    def setUp(self):
        # Create a temporary file with valid Kinematic Identity for testing
        self.valid_file = "valid_mcp_test.txt"
        self.invalid_file = "invalid_mcp_test.txt"

        # Mine a valid hash (same as in test_sentient_lock.py or manual test)
        # We know "test_data_39367" works with "Russell Nordland"
        with open(self.valid_file, "w") as f:
            f.write("test_data_39367")

        with open(self.invalid_file, "w") as f:
            f.write("invalid_data")

    def tearDown(self):
        if os.path.exists(self.valid_file):
            os.remove(self.valid_file)
        if os.path.exists(self.invalid_file):
            os.remove(self.invalid_file)

    def run_mcp_request(self, request):
        """
        Run the MCP server with the given request via stdin.
        """
        proc = subprocess.Popen(
            [sys.executable, "tas_mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = proc.communicate(input=json.dumps(request) + "\n")
        if stderr:
            print(f"MCP Server Stderr: {stderr}")

        return json.loads(stdout)

    def test_initialize(self):
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"}
        }
        res = self.run_mcp_request(req)
        self.assertIn("serverInfo", res["result"])
        self.assertEqual(res["result"]["serverInfo"]["name"], "tas-mcp-server")

    def test_list_tools(self):
        req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        res = self.run_mcp_request(req)
        tools = res["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        self.assertIn("tas_verify_identity", tool_names)
        self.assertIn("tas_shadow_scan", tool_names)
        self.assertIn("tas_sequence_artifact", tool_names)

    def test_call_verify_identity_valid(self):
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "tas_verify_identity",
                "arguments": {
                    "path": self.valid_file,
                    "signature": TAS_HUMAN_SIG
                }
            }
        }
        res = self.run_mcp_request(req)
        self.assertIn("content", res["result"])
        self.assertIn("Kinematic Identity Verified", res["result"]["content"][0]["text"])

    def test_call_verify_identity_invalid(self):
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "tas_verify_identity",
                "arguments": {
                    "path": self.invalid_file,
                    "signature": TAS_HUMAN_SIG
                }
            }
        }
        res = self.run_mcp_request(req)
        # Should return an error result or content with isError: true depending on implementation
        # In my implementation, I caught PhoenixError and returned result with content + isError
        self.assertTrue(res["result"].get("isError", False))
        self.assertIn("PhoenixError", res["result"]["content"][0]["text"])

if __name__ == "__main__":
    unittest.main()
