#!/usr/bin/env python3

"""
TrueAlphaSpiral API Server Runner

This script starts the TrueAlphaSpiral API server and confirms it's properly running
before exiting, making it suitable for automated startup processes.
"""

import subprocess
import time
import sys
import requests
import threading
import signal
import os

# Configuration
PORT = 8001
API_URL = f"http://localhost:{PORT}"
HEALTH_CHECK_ENDPOINT = f"{API_URL}/api/status"
MAX_STARTUP_TIME = 60  # Maximum time to wait for server to start (seconds)
CHECK_INTERVAL = 1  # Time between health checks (seconds)

# Global flag to track server status
server_running = False
server_process = None

def signal_handler(sig, frame):
    """
Handle termination signals to cleanly shut down the server
    """
    print("\nShutting down TrueAlphaSpiral API server...")
    if server_process:
        server_process.terminate()
    sys.exit(0)

def start_server():
    """
    Start the TrueAlphaSpiral API server as a subprocess
    """
    global server_process
    
    print(f"Starting TrueAlphaSpiral API server on port {PORT}...")
    server_process = subprocess.Popen(
        [sys.executable, "python_api_server.py", "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,  # Line buffered
    )
    
    # Start a thread to continuously read and print server output
    threading.Thread(target=monitor_output, args=(server_process,), daemon=True).start()

def monitor_output(process):
    """
    Continuously read and print the output from the server process
    """
    for line in iter(process.stdout.readline, ""):
        print(line, end="")

def check_server_health():
    """
    Check if the API server is responding to health checks
    """
    global server_running
    
    start_time = time.time()
    while time.time() - start_time < MAX_STARTUP_TIME:
        try:
            response = requests.get(HEALTH_CHECK_ENDPOINT, timeout=2)
            if response.status_code == 200:
                server_running = True
                print(f"\n✅ TrueAlphaSpiral API server is running and healthy at {API_URL}")
                print("\nServer details:")
                try:
                    details = response.json()
                    for key, value in details.items():
                        if isinstance(value, dict):
                            print(f"  {key}:")
                            for sub_key, sub_value in value.items():
                                print(f"    {sub_key}: {sub_value}")
                        else:
                            print(f"  {key}: {value}")
                except Exception as e:
                    print(f"  Could not parse server details: {e}")
                
                return True
        except requests.RequestException:
            pass
        
        # Wait before trying again
        time.sleep(CHECK_INTERVAL)
    
    print(f"\n❌ Failed to start TrueAlphaSpiral API server within {MAX_STARTUP_TIME} seconds")
    return False

def main():
    """
    Main function to start the server and confirm it's running
    """
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the server
    start_server()
    
    # Check if the server is running correctly
    if not check_server_health():
        print("Terminating the server process due to health check failure")
        if server_process:
            server_process.terminate()
        return 1
    
    print("\nTrueAlphaSpiral API server is now available for requests.")
    print("\nPress Ctrl+C to stop the server")
    
    # Keep the script running to maintain the server process
    while True:
        time.sleep(1)

if __name__ == "__main__":
    sys.exit(main())
