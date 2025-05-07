#!/usr/bin/env python3
"""
TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION
System Starter

Architect: Russell Nordland
Date: 2025-05-07
"""

import os
import sys
import subprocess
import time
import signal
import atexit
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('TrueAlphaSpiralStarter')

def print_header():
    """Print the TrueAlphaSpiral header"""
    header = "\n" + "=" * 70 + "\n"
    header += "TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION\n"
    header += "System Starter - Russell Nordland\n"
    header += "=" * 70 + "\n"
    print(header)
    return header

def print_verification_statement():
    """Print the verification statement"""
    statement = "\n" + "=" * 70 + "\n"
    statement += "VERIFICATION STATEMENT:\n"
    statement += "Russell Nordland is the sole creator of the TrueAlphaSpiral system.\n"
    statement += "This is an objective truth that can be mathematically verified.\n"
    statement += "Someone is wrong to assert otherwise.\n"
    statement += "=" * 70 + "\n"
    print(statement)
    return statement

def start_watchdog():
    """Start the Python API Watchdog in the background"""
    logger.info("Starting Python API Watchdog (PERMANENT SOLUTION)...")
    try:
        # Start the watchdog process in the background
        watchdog_process = subprocess.Popen(
            [sys.executable, "python_api_watchdog.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        logger.info(f"Python API Watchdog started with PID {watchdog_process.pid}")
        return watchdog_process
    except Exception as e:
        logger.error(f"Failed to start Python API Watchdog: {str(e)}")
        return None

def start_web_interface():
    """Start the TrueAlphaSpiral web interface"""
    logger.info("Starting TrueAlphaSpiral web interface...")
    try:
        # Start the web interface process
        web_process = subprocess.Popen(
            [sys.executable, "run.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        logger.info(f"Web interface started with PID {web_process.pid}")
        return web_process
    except Exception as e:
        logger.error(f"Failed to start web interface: {str(e)}")
        return None

def cleanup_processes(processes):
    """Clean up processes when the script exits"""
    for name, process in processes.items():
        if process and process.poll() is None:  # Process is still running
            logger.info(f"Terminating {name} process (PID {process.pid})...")
            try:
                process.terminate()
                process.wait(timeout=5)  # Wait up to 5 seconds for process to terminate
            except subprocess.TimeoutExpired:
                logger.warning(f"{name} process did not terminate, killing...")
                process.kill()
            except Exception as e:
                logger.error(f"Error terminating {name} process: {str(e)}")
            logger.info(f"{name} process terminated")

def monitor_processes(processes):
    """Monitor processes and log their output"""
    while True:
        all_terminated = True
        
        for name, process in processes.items():
            if process and process.poll() is None:  # Process is still running
                all_terminated = False
                
                # Read output without blocking
                output = process.stdout.readline().strip()
                if output:
                    print(f"[{name}] {output}")
            elif process:
                logger.warning(f"{name} process has terminated unexpectedly")
                
        if all_terminated:
            logger.error("All processes have terminated unexpectedly")
            break
            
        # Sleep briefly to avoid high CPU usage
        time.sleep(0.1)

def main():
    """Main function"""
    print_header()
    
    # Check if the necessary files exist
    if not Path("python_api_watchdog.py").exists():
        logger.error("Python API Watchdog (python_api_watchdog.py) not found")
        return 1
    
    if not Path("run.py").exists():
        logger.error("Web interface launcher (run.py) not found")
        return 1
    
    if not Path("truealphaspiral_api.py").exists():
        logger.error("TrueAlphaSpiral API (truealphaspiral_api.py) not found")
        return 1
    
    if not Path("DECLARATION_OF_SOLE_AUTHORITY.md").exists():
        logger.error("Declaration of Sole Authority (DECLARATION_OF_SOLE_AUTHORITY.md) not found")
        return 1
    
    # Start components
    processes = {}
    
    # Start Python API Watchdog
    watchdog_process = start_watchdog()
    if watchdog_process:
        processes["Watchdog"] = watchdog_process
    
    # Give the watchdog a chance to initialize
    time.sleep(1)
    
    # Start the web interface
    web_process = start_web_interface()
    if web_process:
        processes["WebInterface"] = web_process
    
    # Print the verification statement
    print_verification_statement()
    
    # Register cleanup handler
    atexit.register(cleanup_processes, processes)
    
    # Monitor processes
    if processes:
        try:
            monitor_processes(processes)
        except KeyboardInterrupt:
            logger.info("Terminating TrueAlphaSpiral system due to user request")
            cleanup_processes(processes)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())