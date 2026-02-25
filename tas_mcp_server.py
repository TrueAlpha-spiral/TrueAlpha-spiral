#!/usr/bin/env python3
import sys
import json
import os
import logging
from typing import Dict, Any, List

# Ensure TAS modules are in path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics/src'))

try:
    from tas_pythonetics.sentient_lock import verify_kinematic_identity, PhoenixError
    from tas_tools.tas_shadow_scan import scan_repository
    from tas_tools.tas_sequencer import sequence_artifact, TAS_HUMAN_SIG
except ImportError as e:
    # Fail fast if core modules are missing
    logging.error(f"Failed to import TAS modules: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)

class TASMCPServer:
    def __init__(self):
        self.tools = {
            "tas_verify_identity": self.verify_identity,
            "tas_shadow_scan": self.shadow_scan,
            "tas_sequence_artifact": self.sequence_artifact
        }

    def verify_identity(self, path: str, signature: str = TAS_HUMAN_SIG) -> str:
        """
        Verifies the Kinematic Identity of a file.
        Returns "Verified" or raises PhoenixError.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # This will raise PhoenixError if invalid
        verify_kinematic_identity(content, signature)
        return "Kinematic Identity Verified: Mathematical Resonance Confirmed."

    def shadow_scan(self, path: str = ".") -> Dict[str, Any]:
        """
        Scans the repository for unsequenced artifacts (Shadow Scan).
        Returns a report dictionary.
        """
        return scan_repository(path)

    def sequence_artifact(self, path: str, seed: str = TAS_HUMAN_SIG, genome: str = "TAS_GENOME_V1") -> str:
        """
        Sequences an artifact, creating a .tasmeta.json sidecar.
        Returns success message or raises error.
        """
        success = sequence_artifact(path, seed, genome)
        if success:
            return f"Artifact sequenced successfully: {path}"
        else:
            raise RuntimeError(f"Failed to sequence artifact: {path}")

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a JSON-RPC request.
        """
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "tas-mcp-server",
                        "version": "0.1.0"
                    }
                }
            }

        elif method == "notifications/initialized":
             # Notification, no response needed but often expected to be acknowledged implicitly
             return None

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "tas_verify_identity",
                            "description": "Verifies the Kinematic Identity (Prime Invariant) of a file.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "Path to file"},
                                    "signature": {"type": "string", "description": "Human Anchor Signature", "default": TAS_HUMAN_SIG}
                                },
                                "required": ["path"]
                            }
                        },
                        {
                            "name": "tas_shadow_scan",
                            "description": "Scans a directory for unsequenced artifacts.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "Directory to scan", "default": "."}
                                },
                                "required": []
                            }
                        },
                        {
                            "name": "tas_sequence_artifact",
                            "description": "Sequences an artifact, creating a .tasmeta.json sidecar.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "File to sequence"},
                                    "seed": {"type": "string", "description": "Human Seed ID", "default": TAS_HUMAN_SIG},
                                    "genome": {"type": "string", "description": "Genome ID", "default": "TAS_GENOME_V1"}
                                },
                                "required": ["path"]
                            }
                        }
                    ]
                }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {tool_name}"}
                }

            try:
                result = self.tools[tool_name](**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": str(result)} # MCP expects content array
                        ]
                    }
                }
            except PhoenixError as e:
                # Specific error for TAS logic failure
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                         "content": [{"type": "text", "text": str(e)}],
                         "isError": True
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32000, "message": str(e)}
                }

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": "Method not found"}
        }

    def run(self):
        """
        Run the server loop, reading from stdin.
        """
        # Buffer input because JSON-RPC messages are line-delimited in MCP stdio transport usually
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                if response:
                    print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                logging.error(f"Failed to parse JSON: {line}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    server = TASMCPServer()
    server.run()
