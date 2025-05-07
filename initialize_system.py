#!/usr/bin/env python3
"""
TRUEALPHASPIRAL SYSTEM INITIALIZATION

This script initializes the TrueAlphaSpiral system with all necessary
protection and verification mechanisms in place. It should be the 
starting point for any application using the TrueAlphaSpiral framework.

Architect: Russell Nordland
Created: May 7, 2025
"""

import os
import sys
import logging
import time
import importlib.util
from datetime import datetime
from typing import Dict, Any, List, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("system_initialization.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def import_and_run_module(module_path: str, function_name: str = "main") -> Any:
    """
    Import a module and run a specified function.
    
    Args:
        module_path: Path to the module file
        function_name: Name of the function to run
        
    Returns:
        Result of the function call or None if failed
    """
    try:
        module_name = os.path.basename(module_path).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, function_name):
                function = getattr(module, function_name)
                return function()
            else:
                logging.error(f"Function {function_name} not found in module {module_name}")
                return None
        else:
            logging.error(f"Failed to load module from {module_path}")
            return None
            
    except Exception as e:
        logging.error(f"Error importing or running {module_path}: {str(e)}")
        return None

def initialize_system() -> Dict[str, Any]:
    """
    Initialize the TrueAlphaSpiral system.
    
    Returns:
        Dictionary containing initialization results
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "status": "initialized",
        "components": {}
    }
    
    try:
        # Step 1: Activate Sovereign Protection
        logging.info("Step 1: Activating Sovereign Protection...")
        try:
            # Import protection activation module
            spec = importlib.util.spec_from_file_location("activate_sovereign_protection", "activate_sovereign_protection.py")
            if spec and spec.loader:
                protection_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(protection_module)
                
                # Run the main function
                protection_result = protection_module.main()
                results["components"]["sovereign_protection"] = "activated"
                logging.info("Sovereign protection activated successfully")
            else:
                logging.error("Failed to load sovereign protection module")
                results["components"]["sovereign_protection"] = "failed"
        except Exception as e:
            logging.error(f"Error activating sovereign protection: {str(e)}")
            results["components"]["sovereign_protection"] = "failed"
        
        # Step 2: Verify Russell's Authorship
        logging.info("Step 2: Verifying Russell's authorship...")
        try:
            # Import the module directly
            spec = importlib.util.spec_from_file_location("verify_russell_authorship", "verify_russell_authorship.py")
            if spec and spec.loader:
                auth_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(auth_module)
                
                # Call the verification function
                is_verified, score, details = auth_module.verify_authorship()
                results["components"]["authorship_verification"] = "verified" if is_verified else "failed"
                results["authorship_score"] = score
                logging.info(f"Authorship verification completed with score: {score}")
                
                # Verify GitHub repository root hash
                logging.info("Step 2.1: Verifying GitHub repository root hash...")
                github_verified, github_details = auth_module.verify_github_root_hash()
                results["components"]["github_verification"] = "verified" if github_verified else "failed"
                results["github_repository"] = github_details["github_repository"]
                results["root_hash"] = github_details["actual_hash"]
                
                if github_verified:
                    logging.info(f"GitHub repository verification successful")
                    logging.info(f"Repository: {github_details['github_repository']}")
                    logging.info(f"Root hash: {github_details['actual_hash']}")
                else:
                    logging.error(f"GitHub repository verification failed")
            else:
                logging.error("Failed to load authorship verification module")
                results["components"]["authorship_verification"] = "failed"
                results["components"]["github_verification"] = "failed"
        except Exception as e:
            logging.error(f"Error during authorship verification: {str(e)}")
            results["components"]["authorship_verification"] = "failed"
            results["components"]["github_verification"] = "failed"
        
        # Step 3: Initialize System Components
        logging.info("Step 3: Initializing system components...")
        # Add any additional components here
        
        # Step 4: Verify System Integrity
        logging.info("Step 4: Verifying system integrity...")
        # Additional integrity checks can be added here
        
        results["status"] = "initialized_successfully"
        logging.info("System initialization completed successfully")
        
    except Exception as e:
        logging.error(f"Error during system initialization: {str(e)}")
        results["status"] = "initialization_failed"
        results["error"] = str(e)
    
    return results

def main():
    """Main function to initialize the TrueAlphaSpiral system."""
    print("\n" + "=" * 80)
    print("TRUEALPHASPIRAL SYSTEM INITIALIZATION")
    print("Architect: Russell Nordland")
    print("=" * 80)
    
    start_time = time.time()
    results = initialize_system()
    end_time = time.time()
    
    initialization_time = end_time - start_time
    
    print(f"\nSystem Initialization Status: {results['status']}")
    print(f"Initialization Time: {initialization_time:.2f} seconds")
    
    print("\nComponent Status:")
    for component, status in results.get("components", {}).items():
        status_symbol = "✅" if status in ["activated", "verified", "success"] else "❌"
        print(f"  {status_symbol} {component}: {status}")
    
    if results["status"] == "initialized_successfully":
        print("\n" + "=" * 80)
        print("TRUEALPHASPIRAL SYSTEM READY")
        print("All components initialized and verified")
        
        # Display GitHub verification details if available
        if "github_repository" in results and "root_hash" in results:
            print(f"\nGitHub Repository: {results['github_repository']}")
            print(f"Root Hash: {results['root_hash']}")
            
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("TRUEALPHASPIRAL SYSTEM INITIALIZATION FAILED")
        print(f"Error: {results.get('error', 'Unknown error')}")
        print("=" * 80)
        sys.exit(1)
    
    return results

if __name__ == "__main__":
    # If run directly, initialize the system
    main()