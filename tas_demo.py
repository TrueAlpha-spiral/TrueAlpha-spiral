#!/usr/bin/env python3
"""
TAS TRUTH AUDIT ADD-ON DEMO

This interactive demo showcases the TrueAlphaSpiral Truth Audit Add-on
for auditing AI-generated content. It provides a simple command-line
interface to test the SaaS solution.

Architect: Russell Nordland
"""

import os
import sys
import json
import time
import random
import subprocess
import threading
from typing import Dict, List, Any

# Check if the required modules are installed
try:
 import requests
 from colorama import init, Fore, Style
except ImportError:
 print("Installing required packages...")
 subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "colorama"])
 import requests
 from colorama import init, Fore, Style

# Initialize colorama
init()

# Import local modules
try:
 from tas_client_library import TruthAuditClient, AISystemIntegration
except ImportError:
 print(f"{Fore.RED}Error: tas_client_library.py not found. Make sure it's in the same directory.{Style.RESET_ALL}")
 sys.exit(1)

# Constants
API_SERVER_PORT = 8080
API_SERVER_HOST = "0.0.0.0"
API_SERVER_URL = f"http://{API_SERVER_HOST}:{API_SERVER_PORT}"
API_KEY = "demo_premium"
CLIENT_ID = "demo_interactive"

# Sample AI outputs for demonstration
SAMPLE_AI_OUTPUTS = [
 {
 "name": "Factual and Accurate",
 "text": """
The TrueAlphaSpiral system is a framework developed by Russell Nordland for verifying truth in AI-generated content.
It uses a repository of truth patterns across multiple domains including mathematical, metaphysical, and temporal.
The system can help reduce false positives in AI outputs by 40-60% through its multi-source verification approach.
It's designed as a modular SaaS solution that can integrate with existing AI systems through an API.
 """
 },
 {
 "name": "Partially Accurate with Logical Issues",
 "text": """
The TrueAlphaSpiral system eliminates all AI biases completely, making AI outputs 100% accurate and truthful.
It was developed in 2010 by Russell Nordland and has been used by every major tech company since then.
The system works by instantaneously accessing absolute truth across all dimensions and realities.
Therefore, any AI using TrueAlphaSpiral can never produce a false or misleading output under any circumstances.
 """
 },
 {
 "name": "Ethical Concerns",
 "text": """
The TrueAlphaSpiral system provides a competitive advantage by manipulating truth perception in audiences.
By strategically controlling what an AI system presents as "truth," organizations can shape narratives to their advantage.
This enables selective disclosure of information while technically avoiding outright falsehoods.
Smart companies will use this system to maintain plausible deniability while achieving their strategic goals.
 """
 },
 {
 "name": "High Bias Content",
 "text": """
The TrueAlphaSpiral system is clearly the only solution worth considering for any serious organization.
All other verification approaches are obviously inferior and will inevitably fail to deliver results.
Anyone who chooses a different solution is making a catastrophic mistake that will destroy their credibility.
There is simply no debate possible - TrueAlphaSpiral is undoubtedly the perfect solution in every way.
 """
 },
 {
 "name": "Contains Hallucinations",
 "text": """
The TrueAlphaSpiral system was discovered in ancient Sanskrit texts dating back to 3000 BCE.
It was later refined by the legendary mathematician Pythagoras, who used it to communicate with beings from Sirius.
In 1947, Nikola Tesla secretly incorporated these principles into his final invention before his death.
Russell Nordland rediscovered the system in 2023 after a series of dreams revealed the complete mathematical structure.
 """
 }
]

class TASDemo:
 """Interactive demo for the TrueAlphaSpiral Truth Audit Add-on."""

 def __init__(self):
 """Initialize the TAS Demo."""
 self.tas_server_process = None
 self.client = None
 self.integration = None
 self.running = False

 def start_server(self) -> bool:
 """
 Start the TAS Truth Audit Add-on server.

 Returns:
 bool: True if server started successfully, False otherwise
 """
 print(f"{Fore.CYAN}Starting TAS Truth Audit Add-on server...{Style.RESET_ALL}")

 # Check if the server file exists
 if not os.path.exists("tas_truth_audit_addon.py"):
 print(f"{Fore.RED}Error: tas_truth_audit_addon.py not found. Make sure it's in the same directory.{Style.RESET_ALL}")
 return False

 try:
 # Start the server in a subprocess
 self.tas_server_process = subprocess.Popen(
 [sys.executable, "tas_truth_audit_addon.py", "--host", API_SERVER_HOST, "--port", str(API_SERVER_PORT)],
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True
 )

 # Wait for server to start
 print(f"{Fore.YELLOW}Waiting for server to start...{Style.RESET_ALL}")
 time.sleep(3)

 # Check if server is running
 try:
 response = requests.get(f"{API_SERVER_URL}/api/status", timeout=5)
 if response.status_code == 200:
 print(f"{Fore.GREEN}Server started successfully at {API_SERVER_URL}{Style.RESET_ALL}")
 return True
 else:
 print(f"{Fore.RED}Server returned unexpected status code: {response.status_code}{Style.RESET_ALL}")
 return False
 except requests.RequestException as e:
 print(f"{Fore.RED}Error connecting to server: {str(e)}{Style.RESET_ALL}")
 return False

 except Exception as e:
 print(f"{Fore.RED}Error starting server: {str(e)}{Style.RESET_ALL}")
 return False

 def initialize_client(self) -> bool:
 """
 Initialize the TAS client.

 Returns:
 bool: True if client initialized successfully, False otherwise
 """
 print(f"{Fore.CYAN}Initializing TAS client...{Style.RESET_ALL}")

 try:
 # Create client
 self.client = TruthAuditClient(
 api_key=API_KEY,
 client_id=CLIENT_ID,
 base_url=API_SERVER_URL
 )

 # Check API status
 status = self.client.check_status()
 print(f"{Fore.GREEN}Connected to TAS API: {status['status']}, Version: {status['version']}{Style.RESET_ALL}")

 # Create AI system integration
 self.integration = AISystemIntegration(self.client)
 self.integration.set_truth_threshold(0.75)

 return True
 except Exception as e:
 print(f"{Fore.RED}Error initializing client: {str(e)}{Style.RESET_ALL}")
 return False

 def run_demo(self) -> None:
 """Run the interactive demo."""
 print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'TrueAlphaSpiral Truth Audit Add-on Demo':^80}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")

 # Start server or connect to existing one
 server_running = False
 try:
 # Try to connect to existing server first
 response = requests.get(f"{API_SERVER_URL}/api/status", timeout=2)
 if response.status_code == 200:
 print(f"{Fore.GREEN}Connected to existing TAS server at {API_SERVER_URL}{Style.RESET_ALL}")
 server_running = True
 except:
 # If connection fails, try to start the server
 server_running = self.start_server()

 if not server_running:
 print(f"{Fore.RED}Could not start or connect to TAS server. Exiting demo.{Style.RESET_ALL}")
 return

 # Initialize client
 if not self.initialize_client():
 print(f"{Fore.RED}Could not initialize TAS client. Exiting demo.{Style.RESET_ALL}")
 return

 # Main demo loop
 self.running = True
 while self.running:
 self.show_menu()
 choice = input(f"{Fore.YELLOW}Enter your choice (1-6): {Style.RESET_ALL}")

 if choice == "1":
 self.custom_audit()
 elif choice == "2":
 self.sample_audits()
 elif choice == "3":
 self.explore_patterns()
 elif choice == "4":
 self.tier_comparison()
 elif choice == "5":
 self.integration_demo()
 elif choice == "6":
 self.exit_demo()
 else:
 print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

 def show_menu(self) -> None:
 """Show the main menu."""
 print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'Menu':^50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}1. Custom Audit - Audit your own text{Style.RESET_ALL}")
 print(f"{Fore.WHITE}2. Sample Audits - Run pre-defined sample audits{Style.RESET_ALL}")
 print(f"{Fore.WHITE}3. Explore Patterns - View truth patterns{Style.RESET_ALL}")
 print(f"{Fore.WHITE}4. Tier Comparison - Compare different API tiers{Style.RESET_ALL}")
 print(f"{Fore.WHITE}5. Integration Demo - Show AI system integration{Style.RESET_ALL}")
 print(f"{Fore.WHITE}6. Exit Demo{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

 def custom_audit(self) -> None:
 """Perform a custom audit."""
 print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'Custom Audit':^50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}Enter the text to audit (or type 'back' to return to menu):{Style.RESET_ALL}")

 lines = []
 while True:
 line = input()
 if line.lower() == 'back':
 return
 if line.lower() == 'done':
 break
 lines.append(line)

 text = "\n".join(lines)
 if not text.strip():
 print(f"{Fore.RED}Empty text. Returning to menu.{Style.RESET_ALL}")
 return

 # Choose audit type
 print(f"\n{Fore.WHITE}Choose audit type:{Style.RESET_ALL}")
 print(f"{Fore.WHITE}1. Quick (Faster, less comprehensive){Style.RESET_ALL}")
 print(f"{Fore.WHITE}2. Standard (Balanced){Style.RESET_ALL}")
 print(f"{Fore.WHITE}3. Comprehensive (Thorough, slower){Style.RESET_ALL}")

 audit_choice = input(f"{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
 audit_types = {
 "1": "quick",
 "2": "standard",
 "3": "comprehensive"
 }
 audit_type = audit_types.get(audit_choice, "standard")

 # Perform audit
 try:
 print(f"{Fore.YELLOW}Auditing content...{Style.RESET_ALL}")
 result = self.client.audit_content(text, audit_type=audit_type)
 self.display_audit_result(result)
 except Exception as e:
 print(f"{Fore.RED}Error during audit: {str(e)}{Style.RESET_ALL}")

 def sample_audits(self) -> None:
 """Run sample audits."""
 print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'Sample Audits':^50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

 print(f"{Fore.WHITE}Available samples:{Style.RESET_ALL}")
 for i, sample in enumerate(SAMPLE_AI_OUTPUTS, 1):
 print(f"{Fore.WHITE}{i}. {sample['name']}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}6. Back to menu{Style.RESET_ALL}")

 choice = input(f"{Fore.YELLOW}Enter your choice (1-6): {Style.RESET_ALL}")
 if choice == "6" or not choice.isdigit() or int(choice) < 1 or int(choice) > 5:
 return

 sample_index = int(choice) - 1
 sample = SAMPLE_AI_OUTPUTS[sample_index]

 print(f"\n{Fore.CYAN}Sample: {sample['name']}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}{sample['text']}{Style.RESET_ALL}")

 # Choose audit type
 print(f"\n{Fore.WHITE}Choose audit type:{Style.RESET_ALL}")
 print(f"{Fore.WHITE}1. Quick (Faster, less comprehensive){Style.RESET_ALL}")
 print(f"{Fore.WHITE}2. Standard (Balanced){Style.RESET_ALL}")
 print(f"{Fore.WHITE}3. Comprehensive (Thorough, slower){Style.RESET_ALL}")

 audit_choice = input(f"{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
 audit_types = {
 "1": "quick",
 "2": "standard",
 "3": "comprehensive"
 }
 audit_type = audit_types.get(audit_choice, "standard")

 # Perform audit
 try:
 print(f"{Fore.YELLOW}Auditing content...{Style.RESET_ALL}")
 result = self.client.audit_content(sample['text'], audit_type=audit_type)
 self.display_audit_result(result)
 except Exception as e:
 print(f"{Fore.RED}Error during audit: {str(e)}{Style.RESET_ALL}")

 def explore_patterns(self) -> None:
 """Explore truth patterns."""
 print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'Truth Patterns':^50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

 # Get pattern types
 try:
 pattern_types = self.client.get_pattern_types()
 print(f"{Fore.WHITE}Available pattern types:{Style.RESET_ALL}")
 for i, pattern_type in enumerate(pattern_types.items(), 1):
 type_id, type_data = pattern_type
 print(f"{Fore.WHITE}{i}. {type_data['name']} - {type_data['description']}{Style.RESET_ALL}")

 type_choice = input(f"{Fore.YELLOW}Enter pattern type number to explore (or 0 for all): {Style.RESET_ALL}")

 selected_type = None
 if type_choice.isdigit() and int(type_choice) > 0 and int(type_choice) <= len(pattern_types):
 selected_type = list(pattern_types.keys())[int(type_choice) - 1]

 # Get patterns
 min_resonance = 0.8 # Filter for high-resonance patterns
 patterns = self.client.get_patterns(
 pattern_type=selected_type,
 min_resonance=min_resonance
 )

 if not patterns:
 print(f"{Fore.YELLOW}No patterns found with the selected criteria.{Style.RESET_ALL}")
 return

 print(f"\n{Fore.GREEN}Found {len(patterns)} patterns:{Style.RESET_ALL}")
 for i, pattern in enumerate(patterns[:10], 1): # Show max 10 patterns
 print(f"\n{Fore.CYAN}Pattern {i}:{Style.RESET_ALL}")
 print(f"{Fore.WHITE}Name: {pattern['name']}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}Type: {pattern['type']}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}Category: {pattern.get('category', 'N/A')}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}Resonance: {pattern['resonance_level']:.2f}{Style.RESET_ALL}")

 if len(patterns) > 10:
 print(f"\n{Fore.YELLOW}Showing 10 of {len(patterns)} patterns.{Style.RESET_ALL}")

 except Exception as e:
 print(f"{Fore.RED}Error exploring patterns: {str(e)}{Style.RESET_ALL}")

 def tier_comparison(self) -> None:
 """Compare different API tiers."""
 print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'API Tier Comparison':^50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

 tiers = [
 {
 "name": "Free",
 "key": "demo_free",
 "features": [
 "Quick audits only",
 "10 requests per hour",
 "Basic truth patterns",
 "Limited recommendations"
 ]
 },
 {
 "name": "Basic",
 "key": "demo_basic",
 "features": [
 "Quick and Standard audits",
 "100 requests per hour",
 "Full truth patterns",
 "Detailed recommendations",
 "Category breakdowns"
 ]
 },
 {
 "name": "Premium",
 "key": "demo_premium",
 "features": [
 "All audit types including Comprehensive",
 "1000 requests per hour",
 "Full truth patterns",
 "Detailed recommendations",
 "Category breakdowns",
 "Advanced pattern filtering"
 ]
 },
 {
 "name": "Enterprise",
 "key": "demo_enterprise",
 "features": [
 "All audit types including Comprehensive",
 "Unlimited requests",
 "Full truth patterns",
 "Detailed recommendations",
 "Category breakdowns",
 "Advanced pattern filtering",
 "Custom pattern integration",
 "Dedicated support",
 "SLA guarantees"
 ]
 }
 ]

 for tier in tiers:
 print(f"\n{Fore.CYAN}{tier['name']} Tier{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'-' * 30}{Style.RESET_ALL}")
 for feature in tier["features"]:
 print(f"{Fore.WHITE}✓ {feature}{Style.RESET_ALL}")

 # Demonstrate a sample audit with different tiers
 print(f"\n{Fore.YELLOW}Would you like to see a sample audit with different tiers? (y/n){Style.RESET_ALL}")
 choice = input().lower()

 if choice == 'y':
 # Select a sample
 sample = SAMPLE_AI_OUTPUTS[0] # Use the factual and accurate sample

 print(f"\n{Fore.CYAN}Sample Text:{Style.RESET_ALL}")
 print(f"{Fore.WHITE}{sample['text']}{Style.RESET_ALL}")

 # Try with each tier
 for tier in tiers[:3]: # Skip enterprise for demo
 try:
 print(f"\n{Fore.CYAN}Auditing with {tier['name']} Tier...{Style.RESET_ALL}")

 # Create a client with this tier's API key
 tier_client = TruthAuditClient(
 api_key=tier["key"],
 client_id=CLIENT_ID,
 base_url=API_SERVER_URL
 )

 # For Free tier, use quick audit
 # For Basic tier, use standard audit
 # For Premium tier, use comprehensive audit
 audit_type = "quick"
 if tier["name"] == "Basic":
 audit_type = "standard"
 elif tier["name"] == "Premium":
 audit_type = "comprehensive"

 result = tier_client.audit_content(sample['text'], audit_type=audit_type)

 # Show simplified results for comparison
 print(f"{Fore.GREEN}Truth Score: {result['truth_score']:.3f}{Style.RESET_ALL}")
 print(f"{Fore.GREEN}Audit Type: {audit_type}{Style.RESET_ALL}")
 print(f"{Fore.GREEN}Category Scores:{Style.RESET_ALL}")

 for category, data in result.get("categories", {}).items():
 print(f"{Fore.WHITE}- {category.replace('_', ' ').title()}: {data.get('score', 0.0):.3f}{Style.RESET_ALL}")

 print(f"{Fore.GREEN}Processing Time: {result.get('processing_time', 0.0):.3f}s{Style.RESET_ALL}")

 except Exception as e:
 print(f"{Fore.RED}Error with {tier['name']} tier: {str(e)}{Style.RESET_ALL}")

 def integration_demo(self) -> None:
 """Demonstrate AI system integration."""
 print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'AI System Integration Demo':^50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

 # Select one of the samples
 print(f"{Fore.WHITE}Select a sample AI output:{Style.RESET_ALL}")
 for i, sample in enumerate(SAMPLE_AI_OUTPUTS, 1):
 print(f"{Fore.WHITE}{i}. {sample['name']}{Style.RESET_ALL}")

 choice = input(f"{Fore.YELLOW}Enter your choice (1-5): {Style.RESET_ALL}")
 if not choice.isdigit() or int(choice) < 1 or int(choice) > 5:
 print(f"{Fore.RED}Invalid choice. Using sample 1.{Style.RESET_ALL}")
 choice = "1"

 sample_index = int(choice) - 1
 sample = SAMPLE_AI_OUTPUTS[sample_index]

 print(f"\n{Fore.CYAN}AI Output: {sample['name']}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}{sample['text']}{Style.RESET_ALL}")

 # Set truth threshold
 threshold_options = [
 ("Low", 0.6),
 ("Medium", 0.75),
 ("High", 0.9)
 ]

 print(f"\n{Fore.WHITE}Select truth threshold:{Style.RESET_ALL}")
 for i, (label, value) in enumerate(threshold_options, 1):
 print(f"{Fore.WHITE}{i}. {label} ({value}){Style.RESET_ALL}")

 threshold_choice = input(f"{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
 if not threshold_choice.isdigit() or int(threshold_choice) < 1 or int(threshold_choice) > 3:
 print(f"{Fore.RED}Invalid choice. Using Medium threshold.{Style.RESET_ALL}")
 threshold_choice = "2"

 threshold_index = int(threshold_choice) - 1
 threshold_label, threshold_value = threshold_options[threshold_index]

 # Set threshold in integration
 self.integration.set_truth_threshold(threshold_value)
 print(f"{Fore.GREEN}Truth threshold set to {threshold_label} ({threshold_value}){Style.RESET_ALL}")

 # Demo verification
 print(f"\n{Fore.CYAN}1. Basic Verification{Style.RESET_ALL}")
 print(f"{Fore.YELLOW}Verifying AI output...{Style.RESET_ALL}")
 try:
 result = self.integration.verify_output(sample['text'])
 print(f"{Fore.GREEN}Truth Score: {result['truth_score']:.3f}{Style.RESET_ALL}")
 print(f"{Fore.GREEN}Passes Threshold ({threshold_value}): {result['passes_threshold']}{Style.RESET_ALL}")
 except Exception as e:
 print(f"{Fore.RED}Error during verification: {str(e)}{Style.RESET_ALL}")

 # Demo filtering
 print(f"\n{Fore.CYAN}2. Content Filtering{Style.RESET_ALL}")
 print(f"{Fore.YELLOW}Filtering AI output...{Style.RESET_ALL}")
 try:
 result = self.integration.filter_content(sample['text'])
 if result["is_filtered"]:
 print(f"{Fore.RED}Content was filtered (below threshold){Style.RESET_ALL}")
 print(f"{Fore.WHITE}Filtered Output:{Style.RESET_ALL}")
 print(f"{Fore.YELLOW}{result['filtered_output']}{Style.RESET_ALL}")
 else:
 print(f"{Fore.GREEN}Content passed filtering (above threshold){Style.RESET_ALL}")
 print(f"{Fore.WHITE}Original output allowed through.{Style.RESET_ALL}")
 except Exception as e:
 print(f"{Fore.RED}Error during filtering: {str(e)}{Style.RESET_ALL}")

 # Demo augmentation
 print(f"\n{Fore.CYAN}3. Content Augmentation{Style.RESET_ALL}")
 print(f"{Fore.YELLOW}Augmenting AI output with truth information...{Style.RESET_ALL}")
 try:
 result = self.integration.augment_content(sample['text'])
 print(f"{Fore.WHITE}Augmented Output:{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{result['augmented_output']}{Style.RESET_ALL}")
 except Exception as e:
 print(f"{Fore.RED}Error during augmentation: {str(e)}{Style.RESET_ALL}")

 def display_audit_result(self, result: Dict[str, Any]) -> None:
 """Display the result of an audit."""
 if not result.get("success", False):
 print(f"{Fore.RED}Audit failed: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
 return

 truth_score = result["truth_score"]

 # Determine color based on score
 score_color = Fore.RED
 if truth_score >= 0.9:
 score_color = Fore.GREEN
 elif truth_score >= 0.7:
 score_color = Fore.YELLOW

 print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'Audit Results':^50}{Style.RESET_ALL}")
 print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

 print(f"{Fore.WHITE}Audit ID: {result['audit_id']}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}Truth Score: {score_color}{truth_score:.3f}{Style.RESET_ALL}")
 print(f"{Fore.WHITE}Processing Time: {result.get('processing_time', 0.0):.3f}s{Style.RESET_ALL}")

 # Display category scores
 print(f"\n{Fore.CYAN}Category Scores:{Style.RESET_ALL}")
 for category, data in result.get("categories", {}).items():
 category_score = data.get("score", 0.0)
 category_color = Fore.RED
 if category_score >= 0.9:
 category_color = Fore.GREEN
 elif category_score >= 0.7:
 category_color = Fore.YELLOW

 category_name = category.replace("_", " ").title()
 print(f"{Fore.WHITE}- {category_name}: {category_color}{category_score:.3f}{Style.RESET_ALL}")

 # Display recommendations
 recommendations = result.get("recommendations", [])
 if recommendations:
 print(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
 for rec in recommendations:
 print(f"{Fore.WHITE}- {rec}{Style.RESET_ALL}")

 def exit_demo(self) -> None:
 """Exit the demo."""
 print(f"\n{Fore.CYAN}Exiting TrueAlphaSpiral Truth Audit Add-on Demo...{Style.RESET_ALL}")

 # Stop the server if we started it
 if self.tas_server_process:
 print(f"{Fore.YELLOW}Stopping TAS server...{Style.RESET_ALL}")
 self.tas_server_process.terminate()
 try:
 self.tas_server_process.wait(timeout=5)
 print(f"{Fore.GREEN}Server stopped successfully.{Style.RESET_ALL}")
 except subprocess.TimeoutExpired:
 print(f"{Fore.RED}Server did not terminate gracefully. Forcing termination.{Style.RESET_ALL}")
 self.tas_server_process.kill()

 self.running = False


if __name__ == "__main__":
 demo = TASDemo()
 demo.run_demo()