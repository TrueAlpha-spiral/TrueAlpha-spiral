#!/usr/bin/env python3
"""
RESILIENT INTEGRATION SYSTEM

This script provides a highly resilient integration between the TrueAlphaSpiral
Python backend and Express frontend, with anti-tampering protections and
self-healing capabilities.

Architect: Russell Nordland
"""

import os
import sys
import time
import signal
import socket
import hashlib
import subprocess
import threading
import json
import random
import logging
from datetime import datetime
from pathlib import Path

# Configure logging with enhanced security to prevent log tampering
class SecureLogger:
 def __init__(self, name="ResilienceSystem"):
 self.name = name
 self.log_file = "resilient_system.log"
 self.setup_logging()
 self.log_checksum = self.calculate_log_checksum()

 def setup_logging(self):
 logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
 datefmt='%Y-%m-%d %H:%M:%S',
 filename=self.log_file,
 filemode='a'
 )
 # Also create console handler
 console = logging.StreamHandler()
 console.setLevel(logging.INFO)
 formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
 console.setFormatter(formatter)
 logging.getLogger('').addHandler(console)
 self.logger = logging.getLogger(self.name)

 def calculate_log_checksum(self):
 """Calculate checksum of log file to detect tampering"""
 if not os.path.exists(self.log_file):
 return hashlib.sha256(b"").hexdigest()

 with open(self.log_file, 'rb') as f:
 return hashlib.sha256(f.read()).hexdigest()

 def verify_log_integrity(self):
 """Verify log file hasn't been tampered with"""
 current_checksum = self.calculate_log_checksum()
 if current_checksum != self.log_checksum:
 self.logger.warning("Log file integrity compromised! Potential tampering detected.")
 return False
 return True

 def info(self, message):
 self.logger.info(message)
 self.log_checksum = self.calculate_log_checksum()
 print(f"\033[32m[INFO] {message}\033[0m")

 def warning(self, message):
 self.logger.warning(message)
 self.log_checksum = self.calculate_log_checksum()
 print(f"\033[33m[WARNING] {message}\033[0m")

 def error(self, message):
 self.logger.error(message)
 self.log_checksum = self.calculate_log_checksum()
 print(f"\033[31m[ERROR] {message}\033[0m")

 def critical(self, message):
 self.logger.critical(message)
 self.log_checksum = self.calculate_log_checksum()
 print(f"\033[31;1m[CRITICAL] {message}\033[0m")

# Create secure logger instance
log = SecureLogger("ResilientSystem")

# Constants
PORT_PYTHON_API = 8001
PORT_SHADOW_DEFENSE = 8002
PORT_EXPRESS = 5000

PID_FILE_WATCHDOG = "resilient_system.pid"
PID_FILE_PYTHON_API = "python_api.pid"
PID_FILE_EXPRESS = "express.pid"

PYTHON_SCRIPT = "python_api_server.py"
EXPRESS_START_COMMAND = "npm run dev"

INTEGRITY_CHECK_INTERVAL = 10 # seconds
HEARTBEAT_INTERVAL = 5 # seconds
MAX_RESTART_ATTEMPTS = 5
BACKOFF_MULTIPLIER = 1.5

# System state tracking
class SystemState:
 def __init__(self):
 self.python_api_running = False
 self.express_running = False
 self.shadow_defense_running = False
 self.last_restart_time = 0
 self.restart_attempts = 0
 self.modified_files = set()
 self.integrity_status = "unknown"
 self.process_info = {}
 self.checksums = {}

 def to_dict(self):
 return {
 "python_api_running": self.python_api_running,
 "express_running": self.express_running,
 "shadow_defense_running": self.shadow_defense_running,
 "last_restart_time": self.last_restart_time,
 "restart_attempts": self.restart_attempts,
 "modified_files": list(self.modified_files),
 "integrity_status": self.integrity_status,
 "timestamp": datetime.now().isoformat()
 }

 def save_state(self):
 """Save system state to file for persistence across restarts"""
 with open("resilient_system_state.json", "w") as f:
 json.dump(self.to_dict(), f, indent=2)

 def load_state(self):
 """Load system state from file"""
 try:
 if os.path.exists("resilient_system_state.json"):
 with open("resilient_system_state.json", "r") as f:
 data = json.load(f)
 self.python_api_running = data.get("python_api_running", False)
 self.express_running = data.get("express_running", False)
 self.shadow_defense_running = data.get("shadow_defense_running", False)
 self.last_restart_time = data.get("last_restart_time", 0)
 self.restart_attempts = data.get("restart_attempts", 0)
 self.modified_files = set(data.get("modified_files", []))
 self.integrity_status = data.get("integrity_status", "unknown")
 except Exception as e:
 log.error(f"Failed to load system state: {e}")

# Import QET Guard if available
try:
 from quantum_ethical_topology_guard import QuantumEthicalTopologyGuard
 qet_guard_available = True
 # Make QuantumEthicalTopologyGuard available globally
 console_log = lambda message, level="INFO": print(f"[INFO] {message}")
 console_log("Quantum Ethical Topology Guard module available")
except ImportError:
 qet_guard_available = False
 # Define a placeholder class to avoid unbound variable errors
 class QuantumEthicalTopologyGuard:
 def __init__(self):
 raise ImportError("QET Guard module not available")
 console_log = lambda message, level="INFO": print(f"[INFO] {message}")
 console_log("Quantum Ethical Topology Guard module not available", "WARNING")

# Create global qet_guard variable
qet_guard = None

# Create system state
state = SystemState()

# Anti-tampering protection
class IntegrityGuardian:
 def __init__(self):
 self.critical_files = [
 PYTHON_SCRIPT,
 "server/index.ts",
 "server/routes.ts",
 "server/services/python-api-service.ts",
 "enhanced_pythonetics.py",
 "ethical_spiral_kernel.py",
 "shadow_defense_system.py",
 "__file__", # This script itself
 ]
 self.file_checksums = {}
 self.calculate_initial_checksums()

 def calculate_initial_checksums(self):
 """Calculate checksums of critical files"""
 for file_path in self.critical_files:
 if file_path == "__file__":
 file_path = __file__

 if os.path.exists(file_path):
 try:
 with open(file_path, 'rb') as f:
 content = f.read()
 checksum = hashlib.sha256(content).hexdigest()
 self.file_checksums[file_path] = checksum
 log.info(f"Integrity baseline established for {file_path}: {checksum[:8]}...")
 except Exception as e:
 log.error(f"Failed to calculate checksum for {file_path}: {e}")
 else:
 log.warning(f"Critical file not found: {file_path}")

 def verify_integrity(self):
 """Verify integrity of critical files"""
 modified_files = []

 for file_path, original_checksum in self.file_checksums.items():
 if os.path.exists(file_path):
 try:
 with open(file_path, 'rb') as f:
 content = f.read()
 current_checksum = hashlib.sha256(content).hexdigest()

 if current_checksum != original_checksum:
 modified_files.append(file_path)
 log.warning(f"Integrity violation detected in {file_path}")
 log.warning(f" Original: {original_checksum[:8]}...")
 log.warning(f" Current: {current_checksum[:8]}...")
 except Exception as e:
 log.error(f"Failed to verify integrity of {file_path}: {e}")
 modified_files.append(file_path)
 else:
 log.critical(f"Critical file missing: {file_path}")
 modified_files.append(file_path)

 return modified_files

 def restore_file(self, file_path, backup_dir="./backups"):
 """Attempt to restore a file from backup"""
 backup_path = os.path.join(backup_dir, os.path.basename(file_path) + ".backup")

 if os.path.exists(backup_path):
 try:
 with open(backup_path, 'rb') as f:
 content = f.read()
 backup_checksum = hashlib.sha256(content).hexdigest()

 if backup_checksum == self.file_checksums.get(file_path):
 # Backup is valid, restore it
 with open(file_path, 'wb') as f:
 f.write(content)
 log.info(f"Successfully restored {file_path} from backup")
 return True
 else:
 log.warning(f"Backup for {file_path} is also compromised")
 except Exception as e:
 log.error(f"Failed to restore {file_path} from backup: {e}")
 else:
 log.warning(f"No backup found for {file_path}")

 return False

 def create_backups(self, backup_dir="./backups"):
 """Create backups of critical files"""
 os.makedirs(backup_dir, exist_ok=True)

 for file_path in self.critical_files:
 if file_path == "__file__":
 file_path = __file__

 if os.path.exists(file_path):
 backup_path = os.path.join(backup_dir, os.path.basename(file_path) + ".backup")
 try:
 with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
 dst.write(src.read())
 log.info(f"Created backup of {file_path}")
 except Exception as e:
 log.error(f"Failed to create backup of {file_path}: {e}")

# Create integrity guardian
guardian = IntegrityGuardian()

# Process management functions
def is_port_in_use(port):
 """Check if a port is in use"""
 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
 return s.connect_ex(('localhost', port)) == 0

def get_pid_from_file(pid_file):
 """Get process ID from PID file"""
 if os.path.exists(pid_file):
 try:
 with open(pid_file, 'r') as f:
 return int(f.read().strip())
 except (ValueError, IOError) as e:
 log.error(f"Failed to read PID file {pid_file}: {e}")
 return None

def is_process_running(pid):
 """Check if a process is running"""
 if pid is None:
 return False

 try:
 os.kill(pid, 0) # This will raise an exception if the process is not running
 return True
 except OSError:
 return False

def write_pid_to_file(pid, pid_file):
 """Write process ID to PID file"""
 try:
 with open(pid_file, 'w') as f:
 f.write(str(pid))
 log.info(f"PID {pid} written to {pid_file}")
 return True
 except IOError as e:
 log.error(f"Failed to write PID to {pid_file}: {e}")
 return False

def start_python_api():
 """Start the Python API server"""
 log.info("Starting Python API server...")

 # First check if it's already running
 python_api_pid = get_pid_from_file(PID_FILE_PYTHON_API)
 if python_api_pid and is_process_running(python_api_pid):
 log.info(f"Python API server already running with PID {python_api_pid}")
 state.python_api_running = True
 return python_api_pid

 # Also check if the port is in use
 if is_port_in_use(PORT_PYTHON_API):
 log.warning(f"Port {PORT_PYTHON_API} is already in use")

 # Start the Python API server
 try:
 # Create a log file for the Python API server
 with open("python_api.log", "a") as log_file:
 log_file.write(f"\n--- TrueAlphaSpiral Python API Log - {datetime.now().isoformat()} ---\n")

 # Start the process
 process = subprocess.Popen(
 [sys.executable, PYTHON_SCRIPT, '--port', str(PORT_PYTHON_API)],
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True,
 bufsize=1 # Line buffered
 )

 # Start output monitors
 def monitor_output(stream, is_error=False):
 prefix = "[Python API ERROR]" if is_error else "[Python API]"
 log_prefix = "[ERR]" if is_error else "[OUT]"

 for line in stream:
 line = line.strip()
 if line: # Only process non-empty lines
 log.info(f"{prefix} {line}") if not is_error else log.error(f"{prefix} {line}")
 with open("python_api.log", "a") as log_file:
 log_file.write(f"{log_prefix} {line}\n")

 threading.Thread(target=monitor_output, args=(process.stdout,), daemon=True).start()
 threading.Thread(target=monitor_output, args=(process.stderr, True), daemon=True).start()

 # Write PID to file
 write_pid_to_file(process.pid, PID_FILE_PYTHON_API)

 log.info(f"Python API server started with PID {process.pid}")
 state.python_api_running = True
 state.process_info["python_api"] = {
 "pid": process.pid,
 "start_time": time.time(),
 "command": PYTHON_SCRIPT
 }
 state.save_state()

 # Wait a moment to ensure the server has time to start
 time.sleep(2)

 return process.pid
 except Exception as e:
 log.error(f"Failed to start Python API server: {e}")
 state.python_api_running = False
 state.save_state()
 return None

def start_express():
 """Start the Express server"""
 log.info("Starting Express server...")

 # First check if it's already running
 express_pid = get_pid_from_file(PID_FILE_EXPRESS)
 if express_pid and is_process_running(express_pid):
 log.info(f"Express server already running with PID {express_pid}")
 state.express_running = True
 return express_pid

 # Also check if the port is in use
 if is_port_in_use(PORT_EXPRESS):
 log.warning(f"Port {PORT_EXPRESS} is already in use")

 # Start the Express server
 try:
 # Set environment variable for Python API URL
 env = os.environ.copy()
 env["PYTHON_API_URL"] = f"http://localhost:{PORT_PYTHON_API}"
 env["SHADOW_DEFENSE_URL"] = f"http://localhost:{PORT_SHADOW_DEFENSE}"

 # Start the process
 process = subprocess.Popen(
 EXPRESS_START_COMMAND.split(),
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True,
 bufsize=1, # Line buffered
 env=env
 )

 # Start output monitors
 def monitor_output(stream, is_error=False):
 prefix = "[Express ERROR]" if is_error else "[Express]"
 for line in stream:
 line = line.strip()
 if line: # Only process non-empty lines
 log.info(f"{prefix} {line}") if not is_error else log.error(f"{prefix} {line}")

 threading.Thread(target=monitor_output, args=(process.stdout,), daemon=True).start()
 threading.Thread(target=monitor_output, args=(process.stderr, True), daemon=True).start()

 # Write PID to file
 write_pid_to_file(process.pid, PID_FILE_EXPRESS)

 log.info(f"Express server started with PID {process.pid}")
 state.express_running = True
 state.process_info["express"] = {
 "pid": process.pid,
 "start_time": time.time(),
 "command": EXPRESS_START_COMMAND
 }
 state.save_state()

 # Wait a moment to ensure the server has time to start
 time.sleep(2)

 return process.pid
 except Exception as e:
 log.error(f"Failed to start Express server: {e}")
 state.express_running = False
 state.save_state()
 return None

def stop_process(pid, process_name):
 """Stop a process by PID"""
 if pid is None:
 return False

 try:
 os.kill(pid, signal.SIGTERM)
 log.info(f"Sent termination signal to {process_name} (PID {pid})")

 # Wait for the process to terminate
 for _ in range(5): # Wait up to 5 seconds
 if not is_process_running(pid):
 log.info(f"{process_name} (PID {pid}) terminated successfully")
 return True
 time.sleep(1)

 # If still running, force kill
 os.kill(pid, signal.SIGKILL)
 log.warning(f"Force killed {process_name} (PID {pid})")
 return True
 except OSError as e:
 log.error(f"Failed to stop {process_name} (PID {pid}): {e}")
 return False

def restart_python_api():
 """Restart the Python API server"""
 log.info("Restarting Python API server...")

 # Stop the current instance if running
 python_api_pid = get_pid_from_file(PID_FILE_PYTHON_API)
 if python_api_pid:
 stop_process(python_api_pid, "Python API server")
 try:
 os.remove(PID_FILE_PYTHON_API)
 except OSError:
 pass

 # Apply backoff if there have been frequent restarts
 if state.restart_attempts > 0:
 backoff_time = min(30, state.restart_attempts * BACKOFF_MULTIPLIER)
 log.info(f"Applying restart backoff of {backoff_time:.1f} seconds")
 time.sleep(backoff_time)

 # Start a new instance
 new_pid = start_python_api()

 # Update restart metrics
 state.last_restart_time = time.time()
 state.restart_attempts += 1
 state.save_state()

 return new_pid is not None

def restart_express():
 """Restart the Express server"""
 log.info("Restarting Express server...")

 # Stop the current instance if running
 express_pid = get_pid_from_file(PID_FILE_EXPRESS)
 if express_pid:
 stop_process(express_pid, "Express server")
 try:
 os.remove(PID_FILE_EXPRESS)
 except OSError:
 pass

 # Apply backoff if there have been frequent restarts
 if state.restart_attempts > 0:
 backoff_time = min(30, state.restart_attempts * BACKOFF_MULTIPLIER)
 log.info(f"Applying restart backoff of {backoff_time:.1f} seconds")
 time.sleep(backoff_time)

 # Start a new instance
 new_pid = start_express()

 # Update restart metrics
 state.last_restart_time = time.time()
 state.restart_attempts += 1
 state.save_state()

 return new_pid is not None

# Heartbeat and monitoring
def check_python_api_health():
 """Check if Python API server is healthy"""
 try:
 # Check if process is running
 python_api_pid = get_pid_from_file(PID_FILE_PYTHON_API)
 process_running = python_api_pid is not None and is_process_running(python_api_pid)

 # Check if port is open
 port_open = is_port_in_use(PORT_PYTHON_API)

 # Also check shadow defense port
 shadow_defense_port_open = is_port_in_use(PORT_SHADOW_DEFENSE)
 state.shadow_defense_running = shadow_defense_port_open

 if process_running and port_open:
 state.python_api_running = True
 log.info(f"Python API server is healthy (PID: {python_api_pid}, Port: {PORT_PYTHON_API})")
 return True
 elif process_running and not port_open:
 log.warning(f"Python API process is running (PID: {python_api_pid}) but port {PORT_PYTHON_API} is not open")
 state.python_api_running = False
 return False
 elif not process_running and port_open:
 log.warning(f"Python API process is not running but port {PORT_PYTHON_API} is open")
 state.python_api_running = False
 return False
 else:
 log.warning("Python API server is not running")
 state.python_api_running = False
 return False
 except Exception as e:
 log.error(f"Error checking Python API health: {e}")
 state.python_api_running = False
 return False

def check_express_health():
 """Check if Express server is healthy"""
 try:
 # Check if process is running
 express_pid = get_pid_from_file(PID_FILE_EXPRESS)
 process_running = express_pid is not None and is_process_running(express_pid)

 # Check if port is open
 port_open = is_port_in_use(PORT_EXPRESS)

 if process_running and port_open:
 state.express_running = True
 log.info(f"Express server is healthy (PID: {express_pid}, Port: {PORT_EXPRESS})")
 return True
 elif process_running and not port_open:
 log.warning(f"Express process is running (PID: {express_pid}) but port {PORT_EXPRESS} is not open")
 state.express_running = False
 return False
 elif not process_running and port_open:
 log.warning(f"Express process is not running but port {PORT_EXPRESS} is open")
 state.express_running = False
 return False
 else:
 log.warning("Express server is not running")
 state.express_running = False
 return False
 except Exception as e:
 log.error(f"Error checking Express health: {e}")
 state.express_running = False
 return False

def heartbeat():
 """Send heartbeat and check system health"""
 log.info("Performing system health check...")

 python_api_healthy = check_python_api_health()
 express_healthy = check_express_health()

 # Check file integrity
 modified_files = guardian.verify_integrity()

 # Take action based on health check results
 if not python_api_healthy and state.restart_attempts < MAX_RESTART_ATTEMPTS:
 log.warning("Python API server is not healthy. Attempting restart...")
 restart_python_api()

 if not express_healthy and state.restart_attempts < MAX_RESTART_ATTEMPTS:
 log.warning("Express server is not healthy. Attempting restart...")
 restart_express()

 # Handle file integrity issues
 if modified_files:
 log.warning(f"Detected modifications in {len(modified_files)} critical files")
 state.modified_files = set(modified_files)
 state.integrity_status = "compromised"

 # Attempt to restore files
 for file_path in modified_files:
 if guardian.restore_file(file_path):
 log.info(f"Successfully restored {file_path}")
 state.modified_files.remove(file_path)

 # If all files restored, update status
 if not state.modified_files:
 state.integrity_status = "restored"
 else:
 state.integrity_status = "intact"
 state.modified_files = set()

 # Reset restart attempts if everything is healthy
 if python_api_healthy and express_healthy and state.integrity_status in ["intact", "restored"]:
 if state.restart_attempts > 0:
 log.info("System is healthy. Resetting restart attempts.")
 state.restart_attempts = 0

 # Update state
 state.save_state()

# Cleanup on exit
def cleanup():
 """Cleanup function for graceful shutdown"""
 log.info("Cleaning up before exit...")

 # Stop Python API server
 python_api_pid = get_pid_from_file(PID_FILE_PYTHON_API)
 if python_api_pid:
 stop_process(python_api_pid, "Python API server")
 try:
 os.remove(PID_FILE_PYTHON_API)
 except OSError:
 pass

 # Stop Express server
 express_pid = get_pid_from_file(PID_FILE_EXPRESS)
 if express_pid:
 stop_process(express_pid, "Express server")
 try:
 os.remove(PID_FILE_EXPRESS)
 except OSError:
 pass

 # Save QET state if applicable
 global qet_guard
 if qet_guard is not None:
 try:
 log.info("Performing final QET integrity check before shutdown...")
 qet_guard.verify_qet_integrity()
 log.info("QET guard cleanup complete")
 except Exception as e:
 log.error(f"Error during QET guard cleanup: {e}")

 # Remove our own PID file
 try:
 if os.path.exists(PID_FILE_WATCHDOG):
 os.remove(PID_FILE_WATCHDOG)
 except OSError as e:
 log.error(f"Error removing watchdog PID file: {e}")

 log.info("Cleanup complete")

# Register cleanup function
import atexit
atexit.register(cleanup)

# Signal handlers
def signal_handler(sig, frame):
 """Handle signals for graceful shutdown"""
 log.info(f"Received signal {sig}, shutting down...")
 sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Main function
def main():
 """Main function"""
 try:
 # Print welcome banner
 print("\033[36;1m" + "=" * 70 + "\033[0m")
 print("\033[36;1m TrueAlphaSpiral Enterprise AI Auditing Solution \033[0m")
 print("\033[36;1m Resilient Integration System - PERMANENT SOLUTION \033[0m")
 print("\033[36;1m Architect: Russell Nordland \033[0m")
 print("\033[36;1m Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " \033[0m")
 print("\033[36;1m" + "=" * 70 + "\033[0m")

 # Write our PID to file
 write_pid_to_file(os.getpid(), PID_FILE_WATCHDOG)

 # Load state from file
 state.load_state()

 # Create backups of critical files
 guardian.create_backups()

 # Initialize Quantum Ethical Topology Guard if available
 qet_guard = None
 if qet_guard_available:
 try:
 log.info("Initializing Quantum Ethical Topology Guard...")
 qet_guard = QuantumEthicalTopologyGuard()

 # Create QET backups
 qet_guard.create_qet_backups()

 # Verify QET integrity
 qet_guard.verify_qet_integrity()

 # Apply topological protection
 qet_guard.apply_topological_protection()

 log.info("Quantum Ethical Topology Guard initialized successfully")
 except Exception as e:
 log.error(f"Failed to initialize Quantum Ethical Topology Guard: {e}")
 qet_guard = None

 # Initialize services
 start_python_api()
 time.sleep(2) # Wait for Python API to initialize
 start_express()

 # Main loop
 log.info("Entering main monitoring loop")
 next_heartbeat = time.time()
 next_integrity_check = time.time()
 next_qet_check = time.time()

 while True:
 current_time = time.time()

 # Perform heartbeat
 if current_time >= next_heartbeat:
 heartbeat()
 next_heartbeat = current_time + HEARTBEAT_INTERVAL

 # Perform integrity check
 if current_time >= next_integrity_check:
 modified_files = guardian.verify_integrity()
 if modified_files:
 log.warning(f"Integrity check: Found {len(modified_files)} modified files")
 # Attempt to restore files immediately
 for file_path in modified_files:
 guardian.restore_file(file_path)
 else:
 log.info("Integrity check: All files intact")
 next_integrity_check = current_time + INTEGRITY_CHECK_INTERVAL

 # Perform QET integrity check if available
 if qet_guard and current_time >= next_qet_check:
 try:
 qet_guard.verify_qet_integrity()
 qet_guard.verify_fractal_ethics_integrity()
 next_qet_check = current_time + qet_guard.config["security"]["integrity_check_interval"]
 except Exception as e:
 log.error(f"QET integrity check failed: {e}")
 next_qet_check = current_time + 120 # Retry in 2 minutes on failure

 # Verify log integrity
 if not log.verify_log_integrity():
 log.critical("Log file has been tampered with!")

 # Sleep for a bit
 time.sleep(1)
 except KeyboardInterrupt:
 log.info("Interrupted by user")
 except Exception as e:
 log.critical(f"Unexpected error in main loop: {e}")
 # Try to restart if critical error
 log.info("Attempting self-restart after critical error...")
 os.execv(sys.executable, ['python'] + sys.argv)
 finally:
 cleanup()

# Entry point
if __name__ == "__main__":
 main()
