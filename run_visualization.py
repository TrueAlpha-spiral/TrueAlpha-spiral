"""
RUN VISUALIZATION

This script starts the Tree of Living Intelligence visualization server.

Architect: Russell Nordland
"""

import os
import sys
import logging
import argparse
from pythonetics_visualization import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("visualization_server.log"),
              logging.StreamHandler()]
)
logger = logging.getLogger("run_visualization")

def main():
    """Start the visualization server."""
    parser = argparse.ArgumentParser(description='Run the Tree of Living Intelligence visualization server')
    parser.add_argument('--port', type=int, default=8002, help='Port to run the server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    logger.info(f"Starting Tree of Living Intelligence visualization server on {args.host}:{args.port}")
    logger.info(f"Debug mode: {args.debug}")
    
    try:
        # Start the server
        app.run(host=args.host, port=args.port, debug=args.debug)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()