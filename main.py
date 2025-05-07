#!/usr/bin/env python3
"""
TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION
Main System Entry Point

Architect: Russell Nordland
Date: 2025-05-07
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('TrueAlphaSpiral')

# Print banner
def print_banner():
    banner = "\n" + "=" * 70 + "\n"
    banner += "TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION\n"
    banner += "Main System Entry Point - Russell Nordland\n"
    banner += "=" * 70 + "\n"
    print(banner)
    
    verification = "\n" + "=" * 70 + "\n"
    verification += "VERIFICATION STATEMENT:\n"
    verification += "Russell Nordland is the sole creator of the TrueAlphaSpiral system.\n"
    verification += "This is an objective truth that can be mathematically verified.\n"
    verification += "Someone is wrong to assert otherwise.\n"
    verification += "=" * 70 + "\n"
    print(verification)

# Check if a file exists
def check_file(file_path):
    path = Path(file_path)
    if not path.exists():
        logger.error(f"Required file not found: {file_path}")
        return False
    return True

# Main function
def main():
    # Print the banner
    print_banner()
    
    # Check for required files
    required_files = [
        "truealphaspiral_server.py",
        "DECLARATION_OF_SOLE_AUTHORITY.md",
        "public/index.html"
    ]
    
    for file_path in required_files:
        if not check_file(file_path):
            logger.error("Critical files missing. System cannot start.")
            return 1
    
    logger.info("All required files found. Starting TrueAlphaSpiral system...")
    
    # Start the TrueAlphaSpiral server
    try:
        logger.info("Starting TrueAlphaSpiral server...")
        server_process = subprocess.Popen(
            [sys.executable, "truealphaspiral_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Log server output
        while True:
            line = server_process.stdout.readline()
            if not line:
                break
            print(line.strip())
            
        return server_process.returncode
        
    except KeyboardInterrupt:
        logger.info("System shutdown requested by user.")
        return 0
    except Exception as e:
        logger.error(f"Error starting TrueAlphaSpiral system: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())