"""
ADVANCED EQUATION VISUALIZER LAUNCHER

This script provides a simple interface to launch the Advanced Equation Visualizer
and explore the integration of the Architect's Advanced Equation into the DNA tracking system.

Architect: Russell Nordland
"""

import os
import sys
import time
import subprocess

# Color constants
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"

def timestamp():
    """Generate a timestamp for logs."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def log_message(message, color=RESET):
    """Log a message with timestamp and color."""
    print(f"{color}[{timestamp()}] {message}{RESET}")

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header banner."""
    clear_screen()
    print(f"{BOLD}{CYAN}")
    print("=" * 80)
    print("                ARCHITECT'S ADVANCED EQUATION VISUALIZER")
    print("                   TrueAlphaSpiral System Integration")
    print("=" * 80)
    print(f"{RESET}")
    print(f"{YELLOW}Visualize the integration of the Advanced Equation (Φ = ∑(αi·Ti)/(√(D)·S))")
    print(f"into the DNA tracking cryptographic hash process.{RESET}")
    print()

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import numpy
        import matplotlib
        log_message("Required dependencies are installed.", color=GREEN)
        return True
    except ImportError as e:
        log_message(f"Missing dependency: {e}", color=RED)
        log_message("Please install required dependencies with:", color=YELLOW)
        log_message("  pip install numpy matplotlib", color=YELLOW)
        return False

def run_visualizer(visualization_type=None):
    """Run the Advanced Equation Visualizer with optional type selection."""
    if not check_dependencies():
        return False
    
    if visualization_type == "impact":
        cmd = [sys.executable, "advanced_equation_visualizer.py", "--type=impact"]
    elif visualization_type == "hash":
        cmd = [sys.executable, "advanced_equation_visualizer.py", "--type=hash"]
    elif visualization_type == "cosmic":
        cmd = [sys.executable, "advanced_equation_visualizer.py", "--type=cosmic"]
    else:
        # Run all visualizations
        cmd = [sys.executable, "advanced_equation_visualizer.py"]
    
    log_message(f"Running visualizer: {' '.join(cmd)}", color=CYAN)
    try:
        subprocess.run(cmd, check=True)
        log_message("Visualization completed successfully.", color=GREEN)
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Error running visualizer: {e}", color=RED)
        return False

def open_visualization_folder():
    """Open the folder containing the visualizations."""
    output_dir = "visualization_output"
    if not os.path.exists(output_dir):
        log_message(f"Output directory doesn't exist: {output_dir}", color=RED)
        return False
    
    try:
        if sys.platform == 'win32':
            os.startfile(output_dir)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', output_dir], check=True)
        else:  # Linux
            subprocess.run(['xdg-open', output_dir], check=True)
        log_message(f"Opened visualization output folder: {output_dir}", color=GREEN)
        return True
    except Exception as e:
        log_message(f"Error opening folder: {e}", color=RED)
        return False

def display_menu():
    """Display the main menu."""
    print(f"{BOLD}Options:{RESET}")
    print(f"  {CYAN}1.{RESET} Generate all visualizations")
    print(f"  {CYAN}2.{RESET} Visualize equation impact on cryptographic hash")
    print(f"  {CYAN}3.{RESET} Visualize hash distribution with equation integration")
    print(f"  {CYAN}4.{RESET} Visualize cosmic alignment with equation integration")
    print(f"  {CYAN}5.{RESET} Open visualization output folder")
    print(f"  {CYAN}0.{RESET} Exit")
    print()
    choice = input(f"{BOLD}Enter your choice (0-5): {RESET}")
    return choice

def main():
    """Main function for the launcher."""
    print_header()
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            run_visualizer()
        elif choice == '2':
            run_visualizer("impact")
        elif choice == '3':
            run_visualizer("hash")
        elif choice == '4':
            run_visualizer("cosmic")
        elif choice == '5':
            open_visualization_folder()
        elif choice == '0':
            log_message("Exiting Advanced Equation Visualizer.", color=GREEN)
            sys.exit(0)
        else:
            log_message("Invalid choice. Please try again.", color=RED)
        
        input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        print_header()

if __name__ == "__main__":
    main()