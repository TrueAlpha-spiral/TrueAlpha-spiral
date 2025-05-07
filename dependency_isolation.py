#!/usr/bin/env python3
"""
DEPENDENCY ISOLATION TOOL

This script identifies and lists all files that still have external dependencies
to help us achieve complete system self-sustainability without external dependencies.

Architect: Russell Nordland
"""

import os
import sys
import re
import subprocess

# Define colors for terminal output
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"
BOLD = "\033[1m"

# List of known external dependencies to check for
EXTERNAL_DEPENDENCIES = [
    "requests",
    "flask",
    "google",
]

def find_python_files(root_dir="."):
    """Find all Python files in the given directory and its subdirectories."""
    python_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip directories that typically contain non-project Python files
        if any(skip_dir in dirpath for skip_dir in [".cache", ".pythonlibs", ".sovereign_backups", "__pycache__"]):
            continue
            
        for filename in filenames:
            if filename.endswith(".py"):
                python_files.append(os.path.join(dirpath, filename))
                
    return python_files

def check_import_statements(file_path):
    """Check for external dependencies in import statements."""
    dependencies = []
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            content = f.read()
            
            # Look for import statements
            for dep in EXTERNAL_DEPENDENCIES:
                # Match direct imports or from imports
                if re.search(r"^\s*import\s+{}(?:\.\S+)?".format(dep), content, re.MULTILINE) or \
                   re.search(r"^\s*from\s+{}(?:\.\S+)?\s+import".format(dep), content, re.MULTILINE):
                    dependencies.append(dep)
        except UnicodeDecodeError:
            print(f"{YELLOW}Warning: Skipping file due to encoding issues: {file_path}{RESET}")
            
    return dependencies

def check_for_network_calls(file_path):
    """Check for direct network calls without using requests."""
    network_calls = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            content = f.read()
            
            # Look for socket operations
            if re.search(r"socket\.socket\s*\(", content):
                if "sovereign_http_client.py" not in file_path:  # Our sovereign client uses sockets
                    network_calls.append("socket")
                    
            # Look for urllib usage
            if re.search(r"urllib\.request\.urlopen", content):
                network_calls.append("urllib")
                
            # Look for http.client usage
            if re.search(r"http\.client\.HTTPConnection", content) or \
               re.search(r"http\.client\.HTTPSConnection", content):
                network_calls.append("http.client")
        except UnicodeDecodeError:
            pass  # Already warned in check_import_statements
            
    return network_calls

def analyze_dependencies():
    """Analyze all Python files for external dependencies."""
    print(f"{BOLD}{CYAN}TRUEALPHASPIRAL DEPENDENCY ISOLATION ANALYSIS{RESET}")
    print(f"{BOLD}Architect: Russell Nordland{RESET}")
    print("-" * 80)
    
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files to analyze")
    
    # Track files with dependencies
    files_with_deps = {}
    
    # Analyze each file
    for file_path in python_files:
        import_deps = check_import_statements(file_path)
        network_deps = check_for_network_calls(file_path)
        
        if import_deps or network_deps:
            files_with_deps[file_path] = {
                "imports": import_deps,
                "network": network_deps
            }
    
    # Generate report
    report_deps_by_file(files_with_deps)
    report_deps_by_type(files_with_deps)
    
    return files_with_deps

def report_deps_by_file(files_with_deps):
    """Generate a report of dependencies organized by file."""
    print("\n" + "-" * 80)
    print(f"{BOLD}DEPENDENCIES BY FILE{RESET}")
    print("-" * 80)
    
    if not files_with_deps:
        print(f"{GREEN}No external dependencies found in any files!{RESET}")
        return
        
    for file_path, deps in sorted(files_with_deps.items()):
        print(f"\n{BOLD}{file_path}{RESET}")
        
        if deps["imports"]:
            print(f"  {YELLOW}Import dependencies:{RESET}")
            for dep in sorted(deps["imports"]):
                print(f"    - {dep}")
                
        if deps["network"]:
            print(f"  {YELLOW}Network dependencies:{RESET}")
            for dep in sorted(deps["network"]):
                print(f"    - {dep}")

def report_deps_by_type(files_with_deps):
    """Generate a report of dependencies organized by dependency type."""
    print("\n" + "-" * 80)
    print(f"{BOLD}DEPENDENCIES BY TYPE{RESET}")
    print("-" * 80)
    
    if not files_with_deps:
        return
        
    # Collect all dependencies by type
    import_deps = {}
    network_deps = {}
    
    for file_path, deps in files_with_deps.items():
        for dep in deps["imports"]:
            if dep not in import_deps:
                import_deps[dep] = []
            import_deps[dep].append(file_path)
            
        for dep in deps["network"]:
            if dep not in network_deps:
                network_deps[dep] = []
            network_deps[dep].append(file_path)
    
    # Report import dependencies
    if import_deps:
        print(f"\n{YELLOW}Import Dependencies:{RESET}")
        for dep, files in sorted(import_deps.items()):
            print(f"\n  {BOLD}{dep}{RESET} ({len(files)} files)")
            for file_path in sorted(files):
                print(f"    - {file_path}")
    
    # Report network dependencies
    if network_deps:
        print(f"\n{YELLOW}Network Dependencies:{RESET}")
        for dep, files in sorted(network_deps.items()):
            print(f"\n  {BOLD}{dep}{RESET} ({len(files)} files)")
            for file_path in sorted(files):
                print(f"    - {file_path}")

def generate_replacement_script():
    """Generate a script to replace external dependencies."""
    files_with_deps = analyze_dependencies()
    
    if not files_with_deps:
        print(f"\n{GREEN}No external dependencies to replace. The system is already fully self-sustainable!{RESET}")
        return
        
    print("\n" + "-" * 80)
    print(f"{BOLD}SUGGESTED REMEDIATION STEPS{RESET}")
    print("-" * 80)
    
    print(f"\n{CYAN}Here are the suggested steps to make the system fully self-sustaining:{RESET}")
    
    # Identify files with requests dependency
    requests_files = [f for f, deps in files_with_deps.items() if "requests" in deps["imports"]]
    if requests_files:
        print(f"\n{YELLOW}1. Replace 'requests' with 'sovereign_http_client' in the following files:{RESET}")
        for file_path in sorted(requests_files):
            print(f"   - {file_path}")
            
    # Identify files with flask dependency
    flask_files = [f for f, deps in files_with_deps.items() if "flask" in deps["imports"]]
    if flask_files:
        print(f"\n{YELLOW}2. Replace 'flask' with a self-contained HTTP server in:{RESET}")
        for file_path in sorted(flask_files):
            print(f"   - {file_path}")
    
    # Identify files with Google API dependency
    google_files = [f for f, deps in files_with_deps.items() if "google" in deps["imports"]]
    if google_files:
        print(f"\n{YELLOW}3. Remove or replace Google API dependencies in:{RESET}")
        for file_path in sorted(google_files):
            print(f"   - {file_path}")
    
    print(f"\n{CYAN}Implementation recommendations:{RESET}")
    print(f"1. For 'requests' replacements: Add 'from sovereign_http_client import get, post, put, delete'")
    print(f"2. For 'flask' replacements: Implement a custom HTTP server using the socket module")
    print(f"3. For 'google' API replacements: Replace with custom implementations that don't rely on external services")
    
    print(f"\n{CYAN}Once these changes are complete, run this script again to verify full isolation.{RESET}")

if __name__ == "__main__":
    print("=" * 80)
    print(f"{BOLD}{MAGENTA}TRUEALPHASPIRAL DEPENDENCY ISOLATION TOOL{RESET}")
    print(f"{BOLD}Architect: Russell Nordland{RESET}")
    print("=" * 80)
    
    generate_replacement_script()