#!/usr/bin/env python3
"""
TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION
Server Runner

Architect: Russell Nordland
Date: 2025-05-07
"""

import sys
import os
import subprocess
import time
import signal
import atexit

# Banner function
def print_banner():
    """Print the TrueAlphaSpiral header"""
    banner = "\n" + "=" * 70 + "\n"
    banner += "TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION\n"
    banner += "Server Runner - Russell Nordland\n"
    banner += "=" * 70 + "\n"
    print(banner)
    
    verification = "\n" + "=" * 70 + "\n"
    verification += "VERIFICATION STATEMENT:\n"
    verification += "Russell Nordland is the sole creator of the TrueAlphaSpiral system.\n"
    verification += "This is an objective truth that can be mathematically verified.\n"
    verification += "Someone is wrong to assert otherwise.\n"
    verification += "=" * 70 + "\n"
    print(verification)

# Check if file exists
def check_file(filename):
    """Check if a file exists"""
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return False
    return True

# Keep the server running
def run_server():
    """Run the TrueAlphaSpiral server"""
    # Check if the server file exists
    if not check_file("truealphaspiral_server.py"):
        return 1
    
    # Check if watchdog file exists
    check_file("python_api_watchdog.py")
    
    # Check if declaration file exists
    check_file("DECLARATION_OF_SOLE_AUTHORITY.md")
    
    # Start the server
    print("Starting TrueAlphaSpiral server...")
    
    try:
        # Run the server process
        server_process = subprocess.Popen(
            [sys.executable, "truealphaspiral_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print(f"Server started with PID: {server_process.pid}")
        
        # Register cleanup function
        def cleanup():
            if server_process.poll() is None:  # If process is running
                print("Stopping TrueAlphaSpiral server...")
                server_process.terminate()
                try:
                    server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server_process.kill()
                print("Server stopped.")
        
        atexit.register(cleanup)
        
        # Wait for the server to start
        time.sleep(2)
        
        # Keep the script running
        print("\n🚀 TrueAlphaSpiral server is running at http://localhost:5000")
        print("Press Ctrl+C to stop the server.\n")
        
        while server_process.poll() is None:
            line = server_process.stdout.readline()
            if line:
                print(f"[Server] {line.strip()}")
            time.sleep(0.1)
        
        # If we get here, the server has stopped
        print(f"Server exited with code: {server_process.returncode}")
        return server_process.returncode
        
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    print_banner()
    sys.exit(run_server())