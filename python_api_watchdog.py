#!/usr/bin/env python3

"""
TrueAlphaSpiral Python API Watchdog

This script monitors the Python API server and restarts it if it crashes.
It operates independently of the main system launcher.

Architect: Russell Nordland
"""

import os
import sys
import time
import subprocess
import signal
import requests
import datetime

# Configuration
API_PORT = 8001
API_URL = f"http://localhost:{API_PORT}"
HEALTH_CHECK_ENDPOINT = f"{API_URL}/api/status"
CHECK_INTERVAL = 5  # Seconds between health checks
RESTART_DELAY = 5  # Seconds to wait before restarting
MAX_RESTART_ATTEMPTS = 3  # Maximum restart attempts in a row
COOLDOWN_PERIOD = 60  # Seconds to wait after max restarts
LOG_FILE = "python_api_watchdog.log"

# Setup basic logging
def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}"
    print(log_message)
    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")

# Save PID for management
def save_pid():
    with open("python_api_watchdog.pid", "w") as f:
        f.write(str(os.getpid()))

# Check if the API server is running
def is_api_running():
    try:
        response = requests.get(HEALTH_CHECK_ENDPOINT, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Start the API server
def start_api_server():
    log("Starting Python API server...")
    try:
        process = subprocess.Popen(
            [sys.executable, "python_api_server.py", "--port", str(API_PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        
        # Save PID for management
        with open("python_api.pid", "w") as f:
            f.write(str(process.pid))
            
        log(f"Python API server started with PID {process.pid}")
        return process
    except Exception as e:
        log(f"Failed to start Python API server: {str(e)}")
        return None

# Stop the API server
def stop_api_server():
    log("Stopping Python API server...")
    try:
        if os.path.exists("python_api.pid"):
            with open("python_api.pid", "r") as f:
                pid = int(f.read().strip())
                try:
                    os.kill(pid, signal.SIGTERM)
                    log(f"Sent SIGTERM to process {pid}")
                    time.sleep(2)
                    # Force kill if still running
                    try:
                        os.kill(pid, 0)  # Check if process exists
                        os.kill(pid, signal.SIGKILL)
                        log(f"Sent SIGKILL to process {pid}")
                    except OSError:
                        pass  # Process is already gone
                except OSError:
                    log(f"Process {pid} not found")
            os.remove("python_api.pid")
    except Exception as e:
        log(f"Error stopping Python API server: {str(e)}")

# Main watchdog function
def watchdog_main():
    log("Starting TrueAlphaSpiral Python API Watchdog")
    save_pid()
    
    # Variables to track restarts
    restart_attempts = 0
    last_restart_time = 0
    api_process = None
    
    # Initial start
    if not is_api_running():
        api_process = start_api_server()
        time.sleep(5)  # Allow time for startup
    
    # Main monitoring loop
    try:
        while True:
            current_time = time.time()
            
            # Check if we should reset the restart counter
            if restart_attempts > 0 and current_time - last_restart_time > COOLDOWN_PERIOD:
                log(f"Cooldown period passed, resetting restart attempts from {restart_attempts} to 0")
                restart_attempts = 0
            
            # Check if API is running
            if not is_api_running():
                log("Python API server is not responding")
                
                # Check if we've hit the restart limit
                if restart_attempts >= MAX_RESTART_ATTEMPTS:
                    log(f"Maximum restart attempts ({MAX_RESTART_ATTEMPTS}) reached. Waiting for cooldown.")
                    time.sleep(COOLDOWN_PERIOD)
                    restart_attempts = 0
                    continue
                
                # Stop any existing process
                stop_api_server()
                
                # Wait before restart
                time.sleep(RESTART_DELAY)
                
                # Start the API server again
                api_process = start_api_server()
                last_restart_time = time.time()
                restart_attempts += 1
                
                # Give it time to start up
                time.sleep(5)
            else:
                # If successfully running, log periodically
                if int(current_time) % 60 == 0:  # Log every minute
                    log("Python API server is running normally")
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        log("Watchdog stopping due to keyboard interrupt")
    finally:
        if os.path.exists("python_api_watchdog.pid"):
            os.remove("python_api_watchdog.pid")
        log("Watchdog stopped")

# Handle signals
def signal_handler(sig, frame):
    log(f"Received signal {sig}, shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    watchdog_main()
