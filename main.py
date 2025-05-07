#!/usr/bin/env python3
"""
TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION
Main System Entry Point

Architect: Russell Nordland
Date: 2025-05-07

This is the central entry point for the TrueAlphaSpiral system, initializing
the API server, watchdog, and other components.
"""

import os
import sys
import time
import argparse
import subprocess
import logging
import signal
from datetime import datetime

# Import Shadow Defense System
try:
    import shadow_defense_system
except ImportError:
    print("Shadow Defense System module not found. System security will be limited.")
    shadow_defense_system = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("system.log"),
        logging.StreamHandler()
    ]
)

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print the system banner"""
    print(f"{Colors.HEADER}=================================================")
    print("TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION")
    print("Main System - PERMANENT SOLUTION")
    print("=================================================")
    print("Architect: Russell Nordland")
    print("Date: 2025-05-07")
    print("=================================================")
    print(f"Initializing TrueAlphaSpiral System{Colors.ENDC}")

def check_file(file_path):
    """Check if a file exists and return its status"""
    if os.path.exists(file_path):
        return f"{Colors.GREEN}✓{Colors.ENDC}"
    else:
        return f"{Colors.FAIL}✗{Colors.ENDC}"

def main():
    """Main entry point for the TrueAlphaSpiral system"""
    parser = argparse.ArgumentParser(description='TrueAlphaSpiral Enterprise AI Auditing Solution')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the API server on')
    parser.add_argument('--no-watchdog', action='store_true', help='Do not start the API watchdog')
    args = parser.parse_args()
    
    # Print system banner
    print_banner()
    
    # Check required files
    print("\nChecking system files:")
    print(f"  truealphaspiral_server.py: {check_file('truealphaspiral_server.py')}")
    print(f"  python_api_watchdog.py: {check_file('python_api_watchdog.py')}")
    print(f"  shadow_defense_system.py: {check_file('shadow_defense_system.py')}")
    print(f"  DECLARATION_OF_SOLE_AUTHORITY.md: {check_file('DECLARATION_OF_SOLE_AUTHORITY.md')}")
    print(f"  public/index.html: {check_file('public/index.html')}")
    print(f"  public/verification.html: {check_file('public/verification.html')}")
    
    # Ensure public directory exists
    if not os.path.exists('public'):
        os.makedirs('public')
        print(f"{Colors.WARNING}Created missing public directory{Colors.ENDC}")
    
    # Install dependencies if needed
    try:
        import flask
        import flask_cors
    except ImportError:
        print(f"\n{Colors.WARNING}Installing required Python packages...{Colors.ENDC}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
        print(f"{Colors.GREEN}Dependencies installed successfully{Colors.ENDC}")
    
    # Start API server
    print(f"\n{Colors.BLUE}Starting TrueAlphaSpiral API Server...{Colors.ENDC}")
    server_process = None
    
    if args.no_watchdog:
        # Start server directly (foreground)
        print(f"{Colors.WARNING}Starting API server in foreground mode (no watchdog){Colors.ENDC}")
        try:
            os.execv(sys.executable, [sys.executable, 'truealphaspiral_server.py', '--port', str(args.port)])
        except Exception as e:
            print(f"{Colors.FAIL}Failed to start API server: {e}{Colors.ENDC}")
            sys.exit(1)
    else:
        # Start API Watchdog
        print(f"{Colors.BLUE}Starting TrueAlphaSpiral API Watchdog...{Colors.ENDC}")
        try:
            watchdog_process = subprocess.Popen([sys.executable, 'python_api_watchdog.py'], stdout=sys.stdout, stderr=sys.stderr)
            print(f"{Colors.GREEN}API Watchdog started with PID {watchdog_process.pid}{Colors.ENDC}")
            
            # Wait for API server to start (10 seconds max)
            print("Waiting for API server to start...")
            max_attempts = 10
            for attempt in range(max_attempts):
                try:
                    if os.path.exists("python_api.pid"):
                        with open("python_api.pid", "r") as f:
                            api_pid = f.read().strip()
                        print(f"{Colors.GREEN}API server started with PID {api_pid}{Colors.ENDC}")
                        break
                except:
                    pass
                
                if attempt < max_attempts - 1:
                    time.sleep(1)
                    print(".", end="", flush=True)
                else:
                    print(f"\n{Colors.WARNING}Timeout waiting for API server to start, but watchdog will keep trying{Colors.ENDC}")
            
            print(f"\n{Colors.GREEN}TrueAlphaSpiral system started successfully!{Colors.ENDC}")
            print(f"  API Server: http://localhost:{args.port}")
            print(f"  Verification Page: http://localhost:{args.port}/verification.html")
            print("\nPress Ctrl+C to stop the system")
            
            # Initialize and start Shadow Defense System
            if shadow_defense_system:
                print(f"\n{Colors.BLUE}Initializing Shadow Defense System...{Colors.ENDC}")
                try:
                    defense = shadow_defense_system.start_defense()
                    print(f"{Colors.GREEN}Shadow Defense System activated with {defense.get_status()['active_layers']} layers{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.WARNING}Shadow Defense System initialization failed: {e}. Continuing without full protection.{Colors.ENDC}")
            
            # Keep the main process running
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Shutting down TrueAlphaSpiral system...{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        finally:
            # Stop Shadow Defense System
            if shadow_defense_system:
                try:
                    shadow_defense_system.stop_defense()
                    print(f"{Colors.BLUE}Shadow Defense System deactivated{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}Error stopping Shadow Defense System: {e}{Colors.ENDC}")
            
            # Cleanup will be handled by the watchdog's signal handlers
            print(f"{Colors.GREEN}TrueAlphaSpiral system shutdown complete{Colors.ENDC}")

if __name__ == "__main__":
    main()