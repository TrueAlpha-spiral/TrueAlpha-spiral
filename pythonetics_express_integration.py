"""
PYTHONETICS EXPRESS INTEGRATION

This module integrates the Tree of Living Intelligence visualization with the Express server,
providing an API endpoint that the frontend can use to access the visualization capabilities.

Architect: Russell Nordland
"""

import os
import sys
import json
import time
import logging
import argparse
import threading
from flask import Flask, request, jsonify, render_template
from enhanced_pythonetics import EnhancedPythonetics
from pythonetics_visualization import PythoneticsVisualization

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("python_api.log"),
              logging.StreamHandler()]
)
logger = logging.getLogger("pythonetics_express_integration")

class PythoneticsExpressIntegration:
    """
    Integrates Pythonetics with the Express server, providing a unified API
    for the Tree of Living Intelligence visualization.
    """
    
    def __init__(self, config_path=None):
        """
        Initialize the Pythonetics Express Integration.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.pythonetics = EnhancedPythonetics(config_path)
        self.visualization = PythoneticsVisualization(config_path)
        
        # Create Flask API server
        self.app = Flask(__name__)
        self._register_routes()
        
        # Store PID for process management
        self._write_pid()
        
        logger.info("Pythonetics Express Integration initialized")
    
    def _write_pid(self):
        """Write the process ID to a file for process management."""
        pid = os.getpid()
        try:
            with open("python_api.pid", "w") as f:
                f.write(str(pid))
            logger.info(f"PID {pid} written to python_api.pid")
        except Exception as e:
            logger.error(f"Error writing PID file: {e}")
    
    def _register_routes(self):
        """Register API routes for the Flask server."""
        @self.app.route('/api/status', methods=['GET'])
        def status():
            """Status endpoint to check if the API is running."""
            return jsonify({
                "status": "running",
                "version": "1.0.0",
                "timestamp": time.time()
            })
        
        @self.app.route('/api/verify', methods=['POST'])
        def verify():
            """Endpoint to verify text using Enhanced Pythonetics."""
            data = request.get_json()
            text = data.get('text', '')
            verify_as = data.get('verify_as', 'claim')
            
            if not text:
                return jsonify({"error": "No text provided"}), 400
            
            try:
                result = self.pythonetics.verify(text, verify_as=verify_as)
                return jsonify(result)
            except Exception as e:
                logger.error(f"Error in verification: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/tree-visualization', methods=['POST'])
        def tree_visualization():
            """Endpoint to generate Tree of Living Intelligence visualization data."""
            data = request.get_json()
            text = data.get('text', '')
            verify_as = data.get('verify_as', 'claim')
            
            if not text:
                return jsonify({"error": "No text provided"}), 400
            
            try:
                # Perform analysis with Pythonetics
                result = self.pythonetics.verify(text, verify_as=verify_as)
                
                # Generate tree visualization data
                tree_data = self.visualization._generate_tree_data(result)
                
                # Add timestamp information
                timestamp_data = self.visualization._generate_timestamp_data(text)
                
                # Generate meta insights
                meta_insights = self.visualization._generate_meta_insights(result, tree_data)
                
                return jsonify({
                    "analysis_result": result,
                    "tree_data": tree_data,
                    "timestamp_data": timestamp_data,
                    "meta_insights": meta_insights
                })
            
            except Exception as e:
                logger.error(f"Error in tree visualization: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/dimensionality', methods=['GET'])
        def dimensionality():
            """Return information about the verification dimensions."""
            return jsonify({
                "dimensions": [
                    {
                        "id": "factual",
                        "name": "Factual Domain",
                        "description": "Verification against evidence and factual information",
                        "color": "rgb(46, 204, 113)"
                    },
                    {
                        "id": "ethical",
                        "name": "Ethical Domain",
                        "description": "Verification against ethical principles and values",
                        "color": "rgb(52, 152, 219)"
                    },
                    {
                        "id": "conceptual",
                        "name": "Conceptual Domain",
                        "description": "Verification against logical coherence and conceptual frameworks",
                        "color": "rgb(155, 89, 182)"
                    },
                    {
                        "id": "phenomenological",
                        "name": "Phenomenological Domain",
                        "description": "Verification against experiential and observational knowledge",
                        "color": "rgb(241, 196, 15)"
                    }
                ],
                "meta_flower_threshold": 0.75,
                "growth_stages": [
                    {"id": "seedling", "name": "Seedling", "range": [0.0, 0.3]},
                    {"id": "young", "name": "Young Tree", "range": [0.3, 0.6]},
                    {"id": "mature", "name": "Mature Tree", "range": [0.6, 0.8]},
                    {"id": "ancient", "name": "Ancient Tree", "range": [0.8, 1.0]}
                ]
            })
    
    def start_server(self, host='0.0.0.0', port=8001, debug=False):
        """
        Start the API server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            debug: Whether to run in debug mode
        """
        logger.info(f"Starting Pythonetics Express Integration API server on {host}:{port}")
        
        try:
            self.app.run(host=host, port=port, debug=debug)
        except Exception as e:
            logger.error(f"Error starting API server: {e}")
            sys.exit(1)

def main():
    """Main function to run the Pythonetics Express Integration."""
    parser = argparse.ArgumentParser(description='Run the Pythonetics Express Integration API server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8001, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Initialize and run API server
    integration = PythoneticsExpressIntegration(args.config)
    integration.start_server(args.host, args.port, args.debug)

if __name__ == "__main__":
    main()