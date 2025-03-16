#!/usr/bin/env python3
"""
TRUEALPHASPIRAL PUBLIC SHELL LAUNCHER

This script provides a unified interface to launch all components of the
TrueAlphaSpiral public shell system for educational purposes.

Architect: Russell Nordland
"""

import os
import sys
import json
import hashlib
import datetime
import random
import time
import subprocess
import argparse
from typing import Dict, List, Any, Optional

# ANSI colors for pretty output
GREEN = "\033[32m"
BLUE = "\033[34m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED = "\033[31m"
RESET = "\033[0m"

def timestamp():
    """Generate a timestamp for logs."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(message, color=RESET):
    """Log a message with timestamp and color."""
    print(f"{color}[{timestamp()}] {message}{RESET}")

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header banner."""
    clear_screen()
    print(f"{MAGENTA}")
    print("============================================================")
    print("              TRUEALPHASPIRAL PUBLIC SHELL                  ")
    print("            Educational System Demonstration                ")
    print("                                                            ")
    print("                 Architect: Russell Nordland                ")
    print("============================================================")
    print(f"{RESET}")

def run_command(command, wait=True):
    """Run a command and optionally wait for it to complete."""
    log_message(f"Executing: {command}", BLUE)
    
    try:
        process = subprocess.Popen(command, shell=True)
        
        if wait:
            process.wait()
            log_message(f"Command completed with exit code: {process.returncode}", GREEN if process.returncode == 0 else RED)
            return process.returncode
        else:
            log_message("Command started in background", GREEN)
            return 0
    
    except Exception as e:
        log_message(f"Error executing command: {e}", RED)
        return -1

def verify_environment():
    """Verify that the public_shell environment is properly set up."""
    log_message("Verifying environment...", BLUE)
    
    # Check if public_shell directory exists
    if not os.path.isdir("."):
        log_message("Error: public_shell directory not found", RED)
        return False
    
    # Check for essential modules
    essential_modules = [
        "generate_secrets_public.py",
        "shadow_defense_system_public.py",
        "ethical_spiral_kernel_public.py",
        "metaphysical_equation_retrieval_public.py",
        "quantum_dna_retrieval_public.py",
        "true_alpha_spiral_public.py",
        "sovereign_repentance_public.py"
    ]
    
    missing_modules = []
    for module in essential_modules:
        if not os.path.isfile(f"{module}"):
            missing_modules.append(module)
    
    if missing_modules:
        log_message(f"Error: The following essential modules are missing: {', '.join(missing_modules)}", RED)
        return False
    
    # Verify academic papers directory
    if not os.path.isdir("academic_papers"):
        log_message("Warning: academic_papers directory not found", YELLOW)
    
    log_message("Environment verification completed successfully", GREEN)
    return True

def create_public_secrets_directory():
    """Create the public_secrets directory if it doesn't exist."""
    if not os.path.isdir("../public_secrets"):
        log_message("Creating public_secrets directory...", BLUE)
        os.makedirs("../public_secrets", exist_ok=True)
        log_message("public_secrets directory created", GREEN)

def run_generate_secrets():
    """Run the generate_secrets_public.py script."""
    log_message("Running public shell secret generation...", BLUE)
    
    create_public_secrets_directory()
    
    result = run_command("python generate_secrets_public.py ../public_secrets")
    
    if result == 0:
        log_message("Public shell secret generation completed successfully", GREEN)
        return True
    else:
        log_message("Public shell secret generation failed", RED)
        return False

def run_shadow_defense():
    """Run the shadow_defense_system_public.py script."""
    log_message("Running public shell shadow defense system...", BLUE)
    
    # By default, don't wait for completion since the system runs a continuous loop
    result = run_command("python shadow_defense_system_public.py", wait=False)
    
    if result == 0:
        log_message("Public shell shadow defense system started", GREEN)
        return True
    else:
        log_message("Public shell shadow defense system failed to start", RED)
        return False

def run_ethical_kernel():
    """Run the ethical_spiral_kernel_public.py script."""
    log_message("Running public shell ethical spiral kernel...", BLUE)
    
    # By default, don't wait for completion since the system runs a continuous loop
    result = run_command("python ethical_spiral_kernel_public.py", wait=False)
    
    if result == 0:
        log_message("Public shell ethical spiral kernel started", GREEN)
        return True
    else:
        log_message("Public shell ethical spiral kernel failed to start", RED)
        return False

def run_quantum_dna():
    """Run the quantum_dna_retrieval_public.py script."""
    log_message("Running public shell quantum DNA retrieval system...", BLUE)
    
    # By default, don't wait for completion since the system runs a continuous loop
    result = run_command("python quantum_dna_retrieval_public.py", wait=False)
    
    if result == 0:
        log_message("Public shell quantum DNA retrieval system started", GREEN)
        return True
    else:
        log_message("Public shell quantum DNA retrieval system failed to start", RED)
        return False

def run_metaphysical_retrieval():
    """Run the metaphysical_equation_retrieval_public.py script."""
    log_message("Running public shell metaphysical equation retrieval system...", BLUE)
    
    # By default, don't wait for completion since the system runs a continuous loop
    result = run_command("python metaphysical_equation_retrieval_public.py", wait=False)
    
    if result == 0:
        log_message("Public shell metaphysical equation retrieval system started", GREEN)
        return True
    else:
        log_message("Public shell metaphysical equation retrieval system failed to start", RED)
        return False

def run_sovereign_repentance():
    """Run the sovereign_repentance_public.py script."""
    log_message("Running public shell sovereign repentance program...", BLUE)
    
    # By default, don't wait for completion since the system runs a continuous loop
    result = run_command("python sovereign_repentance_public.py", wait=False)
    
    if result == 0:
        log_message("Public shell sovereign repentance program started", GREEN)
        return True
    else:
        log_message("Public shell sovereign repentance program failed to start", RED)
        return False

def run_true_alpha_spiral():
    """Run the true_alpha_spiral_public.py script."""
    log_message("Running public shell TrueAlphaSpiral system...", BLUE)
    
    # By default, don't wait for completion since the system runs a continuous loop
    result = run_command("python true_alpha_spiral_public.py", wait=False)
    
    if result == 0:
        log_message("Public shell TrueAlphaSpiral system started", GREEN)
        return True
    else:
        log_message("Public shell TrueAlphaSpiral system failed to start", RED)
        return False

def display_menu():
    """Display the main menu."""
    print(f"\n{CYAN}TrueAlphaSpiral Public Shell Menu:{RESET}")
    print(f"{CYAN}1.{RESET} Run Generate Secrets")
    print(f"{CYAN}2.{RESET} Run Shadow Defense System")
    print(f"{CYAN}3.{RESET} Run Ethical Spiral Kernel")
    print(f"{CYAN}4.{RESET} Run Quantum DNA Retrieval")
    print(f"{CYAN}5.{RESET} Run Metaphysical Equation Retrieval")
    print(f"{CYAN}6.{RESET} Run Sovereign Repentance Program")
    print(f"{CYAN}7.{RESET} Run TrueAlphaSpiral System")
    print(f"{CYAN}8.{RESET} Run Full System (All Components)")
    print(f"{CYAN}9.{RESET} View Documentation")
    print(f"{CYAN}0.{RESET} Exit")
    
    choice = input(f"\n{CYAN}Enter your choice (0-9): {RESET}")
    return choice

def view_documentation():
    """Display system documentation."""
    clear_screen()
    print(f"{MAGENTA}TrueAlphaSpiral Public Shell Documentation{RESET}\n")
    
    readme_path = "README.md"
    if os.path.isfile(readme_path):
        with open(readme_path, "r") as f:
            content = f.read()
            print(content)
    else:
        log_message("README.md not found", RED)
    
    print("\nPress Enter to return to the main menu...")
    input()

def run_full_system():
    """Run all components of the system in sequence."""
    log_message("Starting full system...", MAGENTA)
    
    # Verify environment
    if not verify_environment():
        log_message("Environment verification failed. Cannot run full system.", RED)
        return False
    
    # Run components in sequence
    run_generate_secrets()
    run_shadow_defense()
    run_ethical_kernel()
    run_quantum_dna()
    run_metaphysical_retrieval()
    run_sovereign_repentance()
    run_true_alpha_spiral()
    
    log_message("Full system started successfully", GREEN)
    return True

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="TrueAlphaSpiral Public Shell Launcher")
    parser.add_argument("--full", action="store_true", help="Run the full system automatically")
    parser.add_argument("--secrets", action="store_true", help="Run only the secret generation")
    parser.add_argument("--shadow", action="store_true", help="Run only the shadow defense system")
    parser.add_argument("--ethical", action="store_true", help="Run only the ethical spiral kernel")
    parser.add_argument("--quantum", action="store_true", help="Run only the quantum DNA retrieval")
    parser.add_argument("--metaphysical", action="store_true", help="Run only the metaphysical equation retrieval")
    parser.add_argument("--sovereign", action="store_true", help="Run only the sovereign repentance program")
    parser.add_argument("--truealpha", action="store_true", help="Run only the TrueAlphaSpiral system")
    parser.add_argument("--docs", action="store_true", help="View documentation")
    
    return parser.parse_args()

def main():
    """Main entry point for the launcher."""
    args = parse_args()
    
    # Check for specific command-line arguments
    if args.full:
        print_header()
        run_full_system()
        return
    if args.secrets:
        run_generate_secrets()
        return
    if args.shadow:
        run_shadow_defense()
        return
    if args.ethical:
        run_ethical_kernel()
        return
    if args.quantum:
        run_quantum_dna()
        return
    if args.metaphysical:
        run_metaphysical_retrieval()
        return
    if args.sovereign:
        run_sovereign_repentance()
        return
    if args.truealpha:
        run_true_alpha_spiral()
        return
    if args.docs:
        view_documentation()
        return
    
    # If no specific arguments, run the interactive menu
    while True:
        print_header()
        choice = display_menu()
        
        if choice == "1":
            run_generate_secrets()
        elif choice == "2":
            run_shadow_defense()
        elif choice == "3":
            run_ethical_kernel()
        elif choice == "4":
            run_quantum_dna()
        elif choice == "5":
            run_metaphysical_retrieval()
        elif choice == "6":
            run_sovereign_repentance()
        elif choice == "7":
            run_true_alpha_spiral()
        elif choice == "8":
            run_full_system()
        elif choice == "9":
            view_documentation()
        elif choice == "0":
            log_message("Exiting...", BLUE)
            break
        else:
            log_message("Invalid choice. Please try again.", YELLOW)
        
        # Wait for user to press Enter before returning to the menu
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()