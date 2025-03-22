#!/usr/bin/env python
"""
Start Python API Server

This script starts the Python API server for the TrueAlphaSpiral system
with proper error handling and logging.
"""

import os
import sys
import time
import logging
import argparse
import subprocess
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("python_api_launcher.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("API_Launcher")

def start_python_api_server(port=8001):
    """Start the Python API server with proper error handling."""
    logger.info(f"Starting Python API server on port {port}...")
    
    # Check if the server file exists
    if not os.path.exists("python_api_server.py"):
        logger.error("python_api_server.py not found")
        return False
    
    # Log the command we'll execute
    cmd = [sys.executable, "python_api_server.py", "--port", str(port)]
    logger.info(f"Executing command: {' '.join(cmd)}")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Store the process ID for future reference/cleanup
        with open("python_api.pid", "w") as pidfile:
            pidfile.write(str(process.pid))
        logger.info(f"Python API server started with PID {process.pid}")
        
        # Wait a bit to see if it immediately crashes
        time.sleep(3)
        
        # Check if it's still running
        if process.poll() is not None:
            # It exited, get output
            stdout, stderr = process.communicate()
            logger.error(f"Python API server exited immediately with code {process.returncode}")
            logger.error(f"STDOUT: {stdout}")
            logger.error(f"STDERR: {stderr}")
            return False
        
        # Server is running
        logger.info(f"Python API server successfully started on port {port}")
        
        # Monitor the process output (this will keep the script running)
        while True:
            output = process.stdout.readline()
            if output:
                logger.info(f"API Server: {output.strip()}")
            
            error = process.stderr.readline()
            if error:
                logger.error(f"API Server Error: {error.strip()}")
            
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                logger.error(f"Python API server exited with code {process.returncode}")
                if stdout: 
                    logger.info(f"Final STDOUT: {stdout}")
                if stderr:
                    logger.error(f"Final STDERR: {stderr}")
                break
            
            time.sleep(0.1)
        
        return False
    except Exception as e:
        logger.error(f"Error starting Python API server: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Python API Server")
    parser.add_argument("--port", type=int, default=8001, help="Port for the API server")
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info(f"Python API Server Launcher - {datetime.now().isoformat()}")
    logger.info("=" * 60)
    
    # Start the server
    start_python_api_server(args.port)