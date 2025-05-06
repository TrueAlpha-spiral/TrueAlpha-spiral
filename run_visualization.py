#!/usr/bin/env python3
"""
RUN VISUALIZATION

This script runs the Tree of Living Intelligence visualization system for the TrueAlphaSpiral Framework.
It starts the API server and provides visualization capabilities for the system.

Architect: Russell Nordland
"""

import os
import sys
import time
import logging
import argparse
import subprocess
from pythonetics_visualization import PythoneticsVisualization, app

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s [%(levelname)s] %(message)s',
 handlers=[logging.FileHandler("run_visualization.log"),
 logging.StreamHandler()]
)
logger = logging.getLogger("run_visualization")

def check_dependencies():
 """Check if required dependencies are installed."""
 try:
 import flask
 import enhanced_pythonetics
 import factual_verifier
 import ethical_analyzer
 return True
 except ImportError as e:
 logger.error(f"Missing dependency: {e}")
 return False

def run_standalone_server(host='0.0.0.0', port=8002, debug=False, config_path=None):
 """Run the standalone visualization server."""
 logger.info(f"Starting standalone visualization server on {host}:{port}")

 try:
 visualization = PythoneticsVisualization(config_path)
 visualization.start_server(host, port, debug)
 except Exception as e:
 logger.error(f"Error starting visualization server: {e}")
 sys.exit(1)

def run_tree_demo(host='0.0.0.0', port=8080):
 """Run the Tree of Living Intelligence demo."""
 logger.info(f"Starting Tree of Living Intelligence demo on {host}:{port}")

 try:
 # Import here to avoid dependency issues if not needed
 from tree_demo import app as demo_app
 demo_app.run(host=host, port=port)
 except Exception as e:
 logger.error(f"Error starting tree demo: {e}")
 sys.exit(1)

def main():
 """Main entry point for the visualization system."""
 parser = argparse.ArgumentParser(description='Run the Tree of Living Intelligence visualization system')
 parser.add_argument('--mode', type=str, choices=['standalone', 'integrated', 'demo'],
 default='standalone', help='Visualization mode to run')
 parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
 parser.add_argument('--port', type=int, default=8002, help='Port to bind to')
 parser.add_argument('--debug', action='store_true', help='Run in debug mode')
 parser.add_argument('--config', type=str, help='Path to configuration file')

 args = parser.parse_args()

 # Check dependencies
 if not check_dependencies():
 logger.error("Missing required dependencies. Please install them first.")
 sys.exit(1)

 # Run in specified mode
 if args.mode == 'standalone':
 run_standalone_server(args.host, args.port, args.debug, args.config)
 elif args.mode == 'integrated':
 # Import here to avoid dependency issues if not needed
 from pythonetics_express_integration import PythoneticsExpressIntegration
 integration = PythoneticsExpressIntegration(args.config)
 integration.start_server(args.host, args.port, args.debug)
 elif args.mode == 'demo':
 run_tree_demo(args.host, args.port)
 else:
 logger.error(f"Unknown mode: {args.mode}")
 sys.exit(1)

if __name__ == "__main__":
 main()