#!/usr/bin/env python3
"""
Python API Watchdog
This script permanently ensures the Python API server is running alongside Express
"""

import os
import sys
import time
import signal
import subprocess
import atexit
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [Watchdog] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

# Constants
PORT = 8001
PID_FILE = 'python_api_watchdog.pid'
API_PID_FILE = 'python_api.pid'
LOG_FILE = 'python_api.log'
PYTHON_SCRIPT = 'python_api_server.py'
CHECK_INTERVAL = 5  # seconds

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Print colored header
print(f"{Colors.CYAN}{Colors.BOLD}======================================================================{Colors.ENDC}")
print(f"{Colors.CYAN}{Colors.BOLD}  TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION  {Colors.ENDC}")
print(f"{Colors.CYAN}{Colors.BOLD}  Python API Watchdog - PERMANENT SOLUTION  {Colors.ENDC}")
print(f"{Colors.CYAN}{Colors.BOLD}  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {Colors.ENDC}")
print(f"{Colors.CYAN}{Colors.BOLD}======================================================================{Colors.ENDC}")

# Write our PID to file for management
def write_watchdog_pid():
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    logging.info(f"Watchdog PID {os.getpid()} written to {PID_FILE}")

# Check if the Python API server is running
def is_api_running():
    if os.path.exists(API_PID_FILE):
        try:
            with open(API_PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            # Check if process is running
            os.kill(pid, 0)  # This will raise an exception if the process is not running
            return True
        except (OSError, ValueError):
            # Process not running or PID file contains invalid data
            return False
    return False

# Start the Python API server
def start_api_server():
    logging.info(f"{Colors.GREEN}Starting Python API server on port {PORT}{Colors.ENDC}")
    
    # Ensure log file exists
    with open(LOG_FILE, 'a') as f:
        f.write(f"\n--- TrueAlphaSpiral Python API Log - {datetime.now().isoformat()} ---\n")
    
    # Start the process
    process = subprocess.Popen(
        [sys.executable, PYTHON_SCRIPT, '--port', str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Line buffered
    )
    
    # Write PID to file
    with open(API_PID_FILE, 'w') as f:
        f.write(str(process.pid))
    
    logging.info(f"{Colors.GREEN}Python API server started with PID {process.pid}{Colors.ENDC}")
    
    # Start non-blocking output monitors
    start_output_monitors(process)
    
    return process

# Monitor process output in a non-blocking way
def start_output_monitors(process):
    def monitor_output(stream, is_error=False):
        prefix = f"{Colors.FAIL}[API ERROR]{Colors.ENDC}" if is_error else f"{Colors.BLUE}[API]{Colors.ENDC}"
        log_prefix = "[ERR]" if is_error else "[OUT]"
        
        for line in stream:
            line = line.strip()
            if line:  # Only process non-empty lines
                print(f"{prefix} {line}")
                with open(LOG_FILE, 'a') as log:
                    log.write(f"{log_prefix} {line}\n")
    
    # Start threads to monitor stdout and stderr
    import threading
    threading.Thread(target=monitor_output, args=(process.stdout,), daemon=True).start()
    threading.Thread(target=monitor_output, args=(process.stderr, True), daemon=True).start()

# Cleanup function for graceful shutdown
def cleanup():
    logging.info(f"{Colors.WARNING}Watchdog shutting down, cleaning up...{Colors.ENDC}")
    
    # Kill Python API server if it's running
    if os.path.exists(API_PID_FILE):
        try:
            with open(API_PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            logging.info(f"{Colors.GREEN}Sent termination signal to Python API server (PID {pid}){Colors.ENDC}")
        except (OSError, ValueError) as e:
            logging.error(f"{Colors.FAIL}Failed to terminate Python API server: {e}{Colors.ENDC}")
        try:
            os.remove(API_PID_FILE)
        except OSError:
            pass
    
    # Remove our own PID file
    try:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    except OSError as e:
        logging.error(f"{Colors.FAIL}Failed to remove watchdog PID file: {e}{Colors.ENDC}")
    
    logging.info(f"{Colors.GREEN}Cleanup complete. Exiting watchdog.{Colors.ENDC}")

# Register cleanup function to run on exit
atexit.register(cleanup)

# Handle signals
def signal_handler(sig, frame):
    logging.info(f"{Colors.WARNING}Received signal {sig}, shutting down...{Colors.ENDC}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Main watchdog loop
def main():
    write_watchdog_pid()
    api_process = None
    
    try:
        while True:
            if not is_api_running():
                logging.info(f"{Colors.WARNING}Python API server not running. Starting it...{Colors.ENDC}")
                api_process = start_api_server()
            else:
                logging.debug("Python API server is running")
            
            # Sleep before next check
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
