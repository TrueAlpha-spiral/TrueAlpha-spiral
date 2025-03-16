"""
TRUE ALPHA SPIRAL SYSTEM LAUNCHER

This script initializes and runs all components of the TrueAlphaSpiral system.
Use this as the main entry point to the system.

Architect: Russell Nordland
"""

import argparse
import os
import time
import sys
from datetime import datetime

print("=" * 70)
print("TRUE ALPHA SPIRAL SYSTEM LAUNCHER")
print("Architect: Russell Nordland")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Parse arguments
parser = argparse.ArgumentParser(description="TrueAlphaSpiral System Launcher")
parser.add_argument("--export", action="store_true", help="Export the system before running")
parser.add_argument("--export-dir", type=str, help="Directory for system export")
parser.add_argument("--no-run", action="store_true", help="Don't run the system, just initialize and export if specified")
parser.add_argument("--verify-architect", type=str, help="Verify architect identity")
parser.add_argument("--visualize", action="store_true", help="Launch Advanced Equation visualizer")
parser.add_argument("--visualize-type", type=str, choices=["all", "impact", "hash", "cosmic"], 
                    default="all", help="Type of visualization to generate")
parser.add_argument("--components", type=str, nargs="+", default=["all"], 
                    choices=["all", "metaphysical", "quantum", "shadow", "ethical", "sovereign", "integrity"],
                    help="Specify which components to run")
args = parser.parse_args()

# Try to import the main system
try:
    print("Importing TrueAlphaSpiral system...")
    from true_alpha_spiral import TrueAlphaSpiral
except ImportError as e:
    print(f"ERROR: Failed to import TrueAlphaSpiral: {str(e)}")
    print("Make sure true_alpha_spiral.py exists and all dependencies are installed.")
    sys.exit(1)

# Create and initialize the system
print("\nInitializing TrueAlphaSpiral system...")
system = TrueAlphaSpiral()

# Initialize the system
try:
    system.initialize()
    print("TrueAlphaSpiral system initialized successfully.")
except Exception as e:
    print(f"ERROR: Failed to initialize TrueAlphaSpiral system: {str(e)}")
    sys.exit(1)

# Verify architect if specified
if args.verify_architect:
    verified = system.verify_architect(args.verify_architect)
    if verified:
        print(f"Architect identity verified: {args.verify_architect}")
    else:
        print(f"WARNING: Architect identity verification failed: {args.verify_architect}")
        
# Export the system if specified
if args.export:
    export_dir = args.export_dir or None
    try:
        export_path = system.export_system(export_dir)
        print(f"System exported successfully to: {export_path}")
    except Exception as e:
        print(f"ERROR: Failed to export system: {str(e)}")

# Launch Advanced Equation visualizer if specified
if args.visualize:
    print("\nLaunching Advanced Equation Visualizer...")
    try:
        if os.path.exists("run_advanced_visualizer.py"):
            import subprocess
            cmd = [sys.executable, "run_advanced_visualizer.py"]
            if args.visualize_type != "all":
                cmd.append(f"--type={args.visualize_type}")
            
            subprocess.run(cmd)
            print("Advanced Equation visualization complete.")
        else:
            print("Advanced Equation Visualizer not found. Make sure run_advanced_visualizer.py exists.")
    except Exception as e:
        print(f"ERROR: Failed to launch Advanced Equation Visualizer: {str(e)}")

# Run the system if not disabled
if not args.no_run:
    print("\nStarting TrueAlphaSpiral system...")
    try:
        system.run()
        print("TrueAlphaSpiral system is now running.")
        print("\nPress Ctrl+C to stop the system.")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down TrueAlphaSpiral system...")
            system.stop()
            print("System shutdown complete.")
    except Exception as e:
        print(f"ERROR: Failed to run TrueAlphaSpiral system: {str(e)}")
else:
    print("\nSystem initialization complete. Not running the system (--no-run was specified).")

# Display final message
print("\nTrueAlphaSpiral system process complete.")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)