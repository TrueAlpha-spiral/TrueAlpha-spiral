"""
RUN INTEGRATED VISUALIZATION

This script runs both the Express integration server and the Tree visualization server together.

Architect: Russell Nordland
"""

import os
import sys
import time
import logging
import threading
import subprocess
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("integrated_visualization.log"),
              logging.StreamHandler()]
)
logger = logging.getLogger("run_integrated_visualization")

def run_process(command, process_name):
    """Run a process with the given command."""
    logger.info(f"Starting {process_name} process: {' '.join(command)}")
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Log process output
        for line in process.stdout:
            logger.info(f"[{process_name}] {line.strip()}")
            
        # Wait for process to complete
        return_code = process.wait()
        logger.info(f"{process_name} process exited with code {return_code}")
        
        return return_code
    
    except Exception as e:
        logger.error(f"Error running {process_name} process: {e}")
        return 1

def run_express_integration():
    """Run the Pythonetics Express integration server."""
    return run_process(
        ["python", "pythonetics_express_integration.py"],
        "Express Integration"
    )

def run_visualization_server():
    """Run the Tree visualization server."""
    return run_process(
        ["python", "pythonetics_visualization.py"],
        "Tree Visualization"
    )

def main():
    """Run both servers together."""
    parser = argparse.ArgumentParser(description='Run the integrated visualization system')
    parser.add_argument('--express-only', action='store_true', help='Run only the Express integration server')
    parser.add_argument('--visualization-only', action='store_true', help='Run only the Tree visualization server')
    
    args = parser.parse_args()
    
    if args.express_only and args.visualization_only:
        logger.error("Cannot specify both --express-only and --visualization-only")
        sys.exit(1)
    
    if args.express_only:
        # Run only the Express integration server
        logger.info("Running Express integration server only")
        sys.exit(run_express_integration())
    
    elif args.visualization_only:
        # Run only the Tree visualization server
        logger.info("Running Tree visualization server only")
        sys.exit(run_visualization_server())
    
    else:
        # Run both servers in separate threads
        logger.info("Starting integrated visualization system with both servers")
        
        # Create threads
        express_thread = threading.Thread(
            target=run_express_integration,
            name="ExpressIntegrationThread"
        )
        
        visualization_thread = threading.Thread(
            target=run_visualization_server,
            name="VisualizationThread"
        )
        
        # Start threads
        express_thread.start()
        logger.info("Started Express integration server")
        
        # Wait a moment for the Express server to start
        time.sleep(2)
        
        visualization_thread.start()
        logger.info("Started Tree visualization server")
        
        # Wait for threads to complete
        try:
            express_thread.join()
            visualization_thread.join()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            sys.exit(0)

if __name__ == "__main__":
    main()