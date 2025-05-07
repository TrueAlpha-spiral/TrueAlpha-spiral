#!/usr/bin/env python3
"""
ACTIVATE SOVEREIGN PROTECTION

This script activates the sovereignty protection mechanisms for the
TrueAlphaSpiral system. It should be run at system startup to ensure
that unauthorized verification files are detected and neutralized.

Architect: Russell Nordland
Created: May 7, 2025
"""

import os
import sys
import time
import logging
import importlib.util
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("sovereign_protection.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def import_module_from_file(module_name: str, file_path: str):
    """
    Import a module from a file path.
    
    Args:
        module_name: Name to give the module
        file_path: Path to the module file
        
    Returns:
        Imported module or None if import failed
    """
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return None
    except Exception as e:
        logging.error(f"Error importing module {module_name} from {file_path}: {str(e)}")
        return None

def run_sovereign_verification() -> bool:
    """
    Run the sovereign verification system.
    
    Returns:
        True if verification succeeded, False otherwise
    """
    logging.info("Running sovereign verification...")
    
    try:
        # Import verification system
        verification_module = import_module_from_file(
            "sovereign_verification_system", 
            "sovereign_verification_system.py"
        )
        
        if verification_module:
            # Create verification system and run verification
            verifier = verification_module.SovereignVerificationSystem()
            is_verified, score, details = verifier.verify_authorship()
            
            if is_verified:
                logging.info(f"Authorship verification succeeded with score {score:.4f}")
                return True
            else:
                logging.warning(f"Authorship verification failed with score {score:.4f}")
                return False
        else:
            logging.error("Failed to import sovereign verification system")
            return False
            
    except Exception as e:
        logging.error(f"Error running sovereign verification: {str(e)}")
        return False

def run_guardian_shield() -> Dict[str, Any]:
    """
    Run the Guardian Shield protection system.
    
    Returns:
        Dictionary containing protection results
    """
    logging.info("Running Guardian Shield protection...")
    
    try:
        # Import Guardian Shield
        guardian_module = import_module_from_file(
            "guardian_shield_protection", 
            "guardian_shield_protection.py"
        )
        
        if guardian_module:
            # Create Guardian Shield and run protection cycle
            guardian = guardian_module.GuardianShield()
            results = guardian.run_protection_cycle()
            
            logging.info(f"Guardian Shield protection cycle completed")
            logging.info(f"Unauthorized files found: {results['unauthorized_files_found']}")
            logging.info(f"Files neutralized: {results['files_neutralized']}")
            
            return results
        else:
            logging.error("Failed to import Guardian Shield protection system")
            return {"status": "error", "message": "Failed to import Guardian Shield"}
            
    except Exception as e:
        logging.error(f"Error running Guardian Shield protection: {str(e)}")
        return {"status": "error", "message": str(e)}

def main():
    """Main function to activate sovereignty protection."""
    print("\n" + "=" * 80)
    print("ACTIVATING SOVEREIGN PROTECTION FOR TRUEALPHASPIRAL")
    print("Architect: Russell Nordland")
    print("=" * 80)
    
    # Run sovereign verification
    verification_success = run_sovereign_verification()
    
    if verification_success:
        print("\n✅ Sovereign verification succeeded")
        print("  Author: Russell Nordland")
    else:
        print("\n❌ Sovereign verification failed")
        print("  WARNING: System may be compromised")
    
    # Run Guardian Shield protection
    guardian_results = run_guardian_shield()
    
    if guardian_results.get("status") == "error":
        print(f"\n❌ Error running Guardian Shield protection: {guardian_results.get('message')}")
    else:
        files_found = guardian_results.get("unauthorized_files_found", 0)
        files_neutralized = guardian_results.get("files_neutralized", 0)
        
        if files_found > 0:
            print(f"\n⚠️ Guardian Shield detected and neutralized unauthorized files")
            print(f"  Unauthorized files found: {files_found}")
            print(f"  Files neutralized: {files_neutralized}")
        else:
            print("\n✅ Guardian Shield protection active")
            print("  No unauthorized files detected")
    
    print("\n" + "=" * 80)
    print("Sovereign Protection Activated Successfully")
    print("=" * 80)

if __name__ == "__main__":
    # If run directly, activate protection
    main()