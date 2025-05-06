#!/usr/bin/env python3
"""
THIEF TRACKING TEST SCRIPT

This script demonstrates the thief tracking capabilities of the TrueAlphaSpiral system.
It uses the metaphysical equation retrieval system to detect and track unauthorized access.

Architect: Russell Nordland
"""

import os
import sys
import time
import json
import hashlib
import argparse
import requests
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8001/api"
ARCHITECT_ID = "Russell Nordland"
TEST_LOG_FILE = "security_reports/thief_tracking_test.log"

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

def call_api(endpoint, method="GET", data=None):
 """Make an API call to the TrueAlphaSpiral system."""
 url = f"{API_BASE_URL}/{endpoint}"

 try:
 if method == "GET":
 response = requests.get(url)
 elif method == "POST":
 response = requests.post(url, json=data)
 elif method == "PUT":
 response = requests.put(url, json=data)
 elif method == "DELETE":
 response = requests.delete(url, json=data)
 else:
 print(f"{RED}[{timestamp()}] [ERROR] Unsupported HTTP method: {method}{RESET}")
 return None

 if response.status_code >= 200 and response.status_code < 300:
 return response.json()
 else:
 print(f"{RED}[{timestamp()}] [ERROR] API request failed: {response.status_code} - {response.text}{RESET}")
 return None
 except Exception as e:
 print(f"{RED}[{timestamp()}] [ERROR] Exception in API request: {str(e)}{RESET}")
 return None

def verify_architect(architect_id):
 """Verify the architect with the system."""
 print(f"{BLUE}[{timestamp()}] [INFO] Verifying architect identity: {architect_id}{RESET}")

 data = {"architect_id": architect_id}
 response = call_api("verify-architect", method="POST", data=data)

 if response and response.get("success", True) and response.get("architect_verified", False):
 print(f"{GREEN}[{timestamp()}] [INFO] Architect verification successful{RESET}")
 return True
 else:
 print(f"{RED}[{timestamp()}] [ERROR] Architect verification failed{RESET}")
 return False

def activate_thief_tracking(architect_id):
 """Activate the thief tracking functionality."""
 print(f"{BLUE}[{timestamp()}] [INFO] Activating thief tracking system{RESET}")

 data = {"architect_id": architect_id}
 response = call_api("track-thief", method="POST", data=data)

 # Debug response
 print(f"{YELLOW}[{timestamp()}] [DEBUG] API response: {response}{RESET}")

 # Handle both success and "already active" responses
 if response:
 # Direct check for success field
 if response.get("success") is True:
 print(f"{GREEN}[{timestamp()}] [INFO] Thief tracking activated successfully{RESET}")
 channels = response.get("channels", 0)
 print(f"{GREEN}[{timestamp()}] [INFO] Monitoring {channels} dimensional channels{RESET}")
 return True
 # Check for "already active" in message
 elif "already active" in str(response.get("message", "")):
 print(f"{YELLOW}[{timestamp()}] [INFO] Thief tracking already active{RESET}")
 return True
 # Check if tracking_status is ACTIVE
 elif response.get("tracking_status") == "ACTIVE":
 print(f"{YELLOW}[{timestamp()}] [INFO] Thief tracking already active{RESET}")
 channels = response.get("channels", 0)
 print(f"{GREEN}[{timestamp()}] [INFO] Monitoring {channels} dimensional channels{RESET}")
 return True

 print(f"{RED}[{timestamp()}] [ERROR] Failed to activate thief tracking{RESET}")
 print(f"{RED}[{timestamp()}] [ERROR] Response details: {response}{RESET}")
 return False

def start_continuous_retrieval(architect_id):
 """Start continuous retrieval of stolen equations."""
 print(f"{BLUE}[{timestamp()}] [INFO] Starting continuous equation retrieval{RESET}")

 data = {"architect_id": architect_id}
 response = call_api("start-continuous-retrieval", method="POST", data=data)

 if response and response.get("success", False):
 print(f"{GREEN}[{timestamp()}] [INFO] Continuous equation retrieval started successfully{RESET}")
 security_level = response.get("security_level", "UNKNOWN")
 print(f"{GREEN}[{timestamp()}] [INFO] Security level: {security_level}{RESET}")
 return True
 else:
 print(f"{RED}[{timestamp()}] [ERROR] Failed to start continuous equation retrieval{RESET}")
 return False

def retrieve_equation(architect_id, field="Cosmic", equation_id=None):
 """Retrieve a specific metaphysical equation."""
 print(f"{BLUE}[{timestamp()}] [INFO] Retrieving metaphysical equation (field: {field}){RESET}")

 data = {"architect_id": architect_id, "field": field}
 if equation_id:
 data["equation_id"] = equation_id

 response = call_api("retrieve-equation", method="POST", data=data)

 if response and response.get("success", False):
 print(f"{GREEN}[{timestamp()}] [INFO] Equation retrieved successfully{RESET}")
 equation = response.get("equation", {})
 if equation:
 print(f"{GREEN}[{timestamp()}] [INFO] Equation ID: {equation.get('id')}{RESET}")
 print(f"{GREEN}[{timestamp()}] [INFO] Equation Field: {equation.get('field')}{RESET}")
 print(f"{GREEN}[{timestamp()}] [INFO] Equation Text: {equation.get('text')}{RESET}")
 return equation
 else:
 print(f"{RED}[{timestamp()}] [ERROR] Failed to retrieve equation{RESET}")
 return None

def analyze_thief_pattern(architect_id):
 """Analyze the thief pattern to identify their signature."""
 print(f"{BLUE}[{timestamp()}] [INFO] Analyzing thief pattern{RESET}")

 data = {"architect_id": architect_id}
 response = call_api("analyze-thief-pattern", method="POST", data=data)

 if response and response.get("success", False):
 print(f"{GREEN}[{timestamp()}] [INFO] Thief pattern analysis completed successfully{RESET}")
 pattern_detected = response.get("pattern_detected", False)
 if pattern_detected:
 print(f"{GREEN}[{timestamp()}] [INFO] Thief pattern detected{RESET}")
 pattern_report = response.get("pattern_report", {})
 confidence = pattern_report.get("confidence_level", 0)
 print(f"{GREEN}[{timestamp()}] [INFO] Confidence level: {confidence:.2f}{RESET}")

 traits = pattern_report.get("signature_traits", [])
 if traits:
 print(f"{GREEN}[{timestamp()}] [INFO] Signature traits:{RESET}")
 for trait in traits:
 print(f"{GREEN}[{timestamp()}] [INFO] - {trait}{RESET}")

 return pattern_report
 else:
 print(f"{YELLOW}[{timestamp()}] [WARNING] No thief pattern detected yet{RESET}")
 return None
 else:
 print(f"{RED}[{timestamp()}] [ERROR] Failed to analyze thief pattern{RESET}")
 return None

def main():
 """Run the thief tracking test."""
 # Use existing globals without modifying them in the argument defaults
 parser = argparse.ArgumentParser(description="TrueAlphaSpiral Thief Tracking Test")
 parser.add_argument("--architect", type=str, default="Russell Nordland", help="Architect ID")
 parser.add_argument("--api-url", type=str, default="http://localhost:8001/api", help="API base URL")
 parser.add_argument("--log-file", type=str, default="security_reports/thief_tracking_test.log", help="Log file path")
 args = parser.parse_args()

 # Use local variables instead of modifying globals
 architect_id = args.architect
 api_url = args.api_url
 log_file_path = args.log_file

 # Create output directory
 if log_file_path and os.path.dirname(log_file_path):
 os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
 else:
 # Default to a security_reports directory if path is empty
 log_file_path = "security_reports/thief_tracking_test.log"
 os.makedirs("security_reports", exist_ok=True)

 # Redirect output to log file
 log_file = open(log_file_path, "w")
 orig_stdout = sys.stdout
 sys.stdout = log_file

 try:
 print(f"{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{MAGENTA}TRUEALPHASPIRAL THIEF TRACKING TEST{RESET}")
 print(f"{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{CYAN}Starting at: {timestamp()}{RESET}")
 print(f"{CYAN}Architect: {architect_id}{RESET}")
 print(f"{CYAN}API URL: {api_url}{RESET}")
 print(f"{CYAN}" + "-" * 80 + f"{RESET}")

 # Step 1: Verify architect
 print(f"{BLUE}[{timestamp()}] [INFO] Step 1: Verifying architect identity{RESET}")
 if not verify_architect(architect_id):
 print(f"{RED}[{timestamp()}] [ERROR] Architect verification failed. Aborting test.{RESET}")
 return 1

 # Step 2: Activate thief tracking
 print(f"{BLUE}[{timestamp()}] [INFO] Step 2: Activating thief tracking{RESET}")
 if not activate_thief_tracking(architect_id):
 print(f"{RED}[{timestamp()}] [ERROR] Failed to activate thief tracking. Aborting test.{RESET}")
 return 1

 # Step 3: Start continuous retrieval
 print(f"{BLUE}[{timestamp()}] [INFO] Step 3: Starting continuous retrieval{RESET}")
 start_continuous_retrieval(architect_id)

 # Step 4: Retrieve specific equations
 print(f"{BLUE}[{timestamp()}] [INFO] Step 4: Retrieving specific equations{RESET}")

 fields = ["Mathematical", "Cosmic", "Quantum", "Metaphysical", "Interdimensional"]
 for field in fields:
 retrieve_equation(architect_id, field)
 time.sleep(1) # Wait between retrievals

 # Step 5: Wait for thief pattern analysis
 print(f"{BLUE}[{timestamp()}] [INFO] Step 5: Waiting for thief pattern detection{RESET}")
 print(f"{YELLOW}[{timestamp()}] [INFO] Waiting 5 seconds...{RESET}")
 time.sleep(5)

 # Step 6: Analyze thief pattern
 print(f"{BLUE}[{timestamp()}] [INFO] Step 6: Analyzing thief pattern{RESET}")
 pattern_report = analyze_thief_pattern(architect_id)

 # Test completion
 print(f"{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{MAGENTA}THIEF TRACKING TEST COMPLETED{RESET}")
 print(f"{MAGENTA}" + "=" * 80 + f"{RESET}")
 print(f"{CYAN}Completed at: {timestamp()}{RESET}")
 print(f"{CYAN}Test log saved to: {log_file_path}{RESET}")

 return 0

 except Exception as e:
 print(f"{RED}[{timestamp()}] [ERROR] Unhandled exception in test: {str(e)}{RESET}")
 return 1

 finally:
 # Restore stdout
 sys.stdout = orig_stdout
 log_file.close()

 # Print summary to console
 print(f"{MAGENTA}THIEF TRACKING TEST COMPLETED{RESET}")
 print(f"{CYAN}Test log saved to: {log_file_path}{RESET}")

if __name__ == "__main__":
 sys.exit(main())