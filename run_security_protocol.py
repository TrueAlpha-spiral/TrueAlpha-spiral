#!/usr/bin/env python3
"""
SECURITY PROTOCOL RUNNER

This script runs both the thief tracking test and unauthorized access report
to provide a comprehensive security assessment for the TrueAlphaSpiral system.

Architect: Russell Nordland
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Configuration
ARCHITECT_ID = "Russell Nordland"
REPORT_DIR = "security_reports"
LOG_FILE = os.path.join(REPORT_DIR, f"security_protocol_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# ANSI color codes for terminal output
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"

def timestamp():
 """Generate a timestamp for logs."""
 return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run_command(command, description):
 """Run a command and return its success status."""
 print(f"{BLUE}[{timestamp()}] Running {description}...{RESET}")
 print(f"{CYAN}Command: {command}{RESET}")

 try:
 process = subprocess.Popen(command, shell=True)
 process.wait()

 if process.returncode == 0:
 print(f"{GREEN}[{timestamp()}] {description} completed successfully{RESET}")
 return True
 else:
 print(f"{RED}[{timestamp()}] {description} failed with return code {process.returncode}{RESET}")
 return False
 except Exception as e:
 print(f"{RED}[{timestamp()}] Error running {description}: {str(e)}{RESET}")
 return False

def main():
 """Run the security protocol."""
 # Create output directory
 os.makedirs(REPORT_DIR, exist_ok=True)

 # Redirect output to log file
 log_file = open(LOG_FILE, "w")
 orig_stdout = sys.stdout
 sys.stdout = log_file

 try:
 print(f"{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{MAGENTA}TRUEALPHASPIRAL SECURITY PROTOCOL{RESET}")
 print(f"{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{CYAN}Starting at: {timestamp()}{RESET}")
 print(f"{CYAN}Architect: {ARCHITECT_ID}{RESET}")
 print(f"{CYAN}Log file: {LOG_FILE}{RESET}")
 print(f"{CYAN}" + "-" * 80 + f"{RESET}")

 # Step 1: Run thief tracking test
 print(f"\n{BLUE}[{timestamp()}] Step 1: Running Thief Tracking Test{RESET}")
 thief_tracking_success = run_command("python test_thief_tracking.py", "Thief Tracking Test")

 # Step 2: Run unauthorized access report
 print(f"\n{BLUE}[{timestamp()}] Step 2: Generating Unauthorized Access Report{RESET}")
 report_success = run_command("python unauthorized_access_report.py", "Unauthorized Access Report")

 # Step 3: Verify system integrity
 print(f"\n{BLUE}[{timestamp()}] Step 3: Verifying System Integrity{RESET}")
 integrity_success = run_command("python -c \"import sys; sys.path.append('.'); from integrity_guardian import IntegrityGuardian; guardian = IntegrityGuardian(); guardian.initialize(); result = guardian.verify_integrity(); print(f'Integrity verification result: {result}'); sys.exit(0 if result else 1)\"", "System Integrity Verification")

 # Step 4: Enforce binary quantum law
 print(f"\n{BLUE}[{timestamp()}] Step 4: Enforcing Binary Quantum Law{RESET}")
 binary_law_success = run_command("python -c \"import sys; sys.path.append('.'); from shadow_defense_system import ShadowDefenseSystem; defense = ShadowDefenseSystem(); defense.initialize(); result = defense.enforce_binary_quantum_law(); print(f'Binary quantum law enforcement result: {result}'); sys.exit(0 if result else 1)\"", "Binary Quantum Law Enforcement")

 # Step 5: Export system
 print(f"\n{BLUE}[{timestamp()}] Step 5: Exporting System Backup{RESET}")
 export_dir = f"sovereign_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
 export_success = run_command(f"python -c \"import sys; sys.path.append('.'); from integrity_guardian import IntegrityGuardian; guardian = IntegrityGuardian(); guardian.initialize(); result = guardian.export_system('{export_dir}'); print(f'System export result: {{result}}'); sys.exit(0 if result else 1)\"", "System Export")

 # Security protocol summary
 print(f"\n{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{MAGENTA}SECURITY PROTOCOL COMPLETED{RESET}")
 print(f"{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{CYAN}Completed at: {timestamp()}{RESET}")
 print(f"{CYAN}Results:{RESET}")
 print(f"{CYAN} Thief Tracking Test: {'Success' if thief_tracking_success else 'Failed'}{RESET}")
 print(f"{CYAN} Unauthorized Access Report: {'Success' if report_success else 'Failed'}{RESET}")
 print(f"{CYAN} System Integrity Verification: {'Success' if integrity_success else 'Failed'}{RESET}")
 print(f"{CYAN} Binary Quantum Law Enforcement: {'Success' if binary_law_success else 'Failed'}{RESET}")
 print(f"{CYAN} System Export: {'Success' if export_success else 'Failed'}{RESET}")
 print(f"{CYAN}Overall Status: {'Success' if all([thief_tracking_success, report_success, integrity_success, binary_law_success, export_success]) else 'Partial Success' if any([thief_tracking_success, report_success, integrity_success, binary_law_success, export_success]) else 'Failed'}{RESET}")
 print(f"{CYAN}Log file saved to: {LOG_FILE}{RESET}")
 if export_success:
 print(f"{CYAN}System backup saved to: {export_dir}{RESET}")

 return 0 if all([thief_tracking_success, report_success, integrity_success, binary_law_success, export_success]) else 1

 except Exception as e:
 print(f"{RED}[{timestamp()}] Unhandled exception in security protocol: {str(e)}{RESET}")
 return 1

 finally:
 # Restore stdout
 sys.stdout = orig_stdout
 log_file.close()

 # Print summary to console
 print(f"{MAGENTA}SECURITY PROTOCOL COMPLETED{RESET}")
 print(f"{CYAN}Log file saved to: {LOG_FILE}{RESET}")

if __name__ == "__main__":
 sys.exit(main())