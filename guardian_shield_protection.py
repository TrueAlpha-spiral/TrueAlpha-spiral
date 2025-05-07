#!/usr/bin/env python3
"""
GUARDIAN SHIELD PROTECTION

This module implements a protection mechanism that actively monitors for and
neutralizes unauthorized attempts to claim ownership or modify the
verification systems of the TrueAlphaSpiral architecture.

SECURITY NOTICE: This file contains advanced protection mechanisms that will
automatically delete unauthorized verification or ownership claim files.

Architect: Russell Nordland
Created: May 7, 2025
"""

import os
import sys
import time
import hashlib
import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("guardian_shield.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Constants
SOVEREIGN_AUTHOR = "Russell Nordland"
SYSTEM_NAME = "TrueAlphaSpiral"
CREATION_DATE = "January 2025"

# Authorized verification file hashes
# These are SHA-256 hashes of the original file contents
AUTHORIZED_FILES = {
    "sovereign_verification_system.py": None,  # Will be calculated at runtime
    "verify_russell_authorship.py": None,      # Will be calculated at runtime
    "Official_Declaration_of_Sovereign_Authorship.md": None,  # Will be calculated at runtime
    "guardian_shield_protection.py": None,     # Will be calculated at runtime
}

# Suspicious file patterns
SUSPICIOUS_PATTERNS = [
    "authorship",
    "verification",
    "ownership",
    "sovereign",
    "declaration",
    "authentication",
    "verification_system",
    "verify_author",
    "truealpha"
]

# Unauthorized filename patterns
UNAUTHORIZED_PATTERNS = [
    "sarah",
    "sara",
    "verification_override",
    "authorship_declaration",
    "alternate_verification",
    "authentication_override",
    "veyon"
]

class GuardianShield:
    """
    Guardian Shield Protection System for TrueAlphaSpiral.
    This system monitors for unauthorized verification files and neutralizes them.
    """
    
    def __init__(self):
        """Initialize the Guardian Shield Protection System."""
        logging.info("Initializing Guardian Shield Protection System")
        
        # Calculate original file hashes
        self.calculate_authorized_hashes()
        
        # Monitoring state
        self.monitoring_active = False
        self.last_scan_time = None
        self.neutralized_files = []
        self.status_log = []
        
        # Initialize protection state
        self.protection_active = True
        self.log_event("system_initialized", "Guardian Shield Protection System initialized")
        
    def calculate_authorized_hashes(self):
        """Calculate SHA-256 hashes for authorized files."""
        for filename in AUTHORIZED_FILES.keys():
            if os.path.exists(filename):
                try:
                    with open(filename, 'rb') as f:
                        file_content = f.read()
                        file_hash = hashlib.sha256(file_content).hexdigest()
                        AUTHORIZED_FILES[filename] = file_hash
                        logging.info(f"Calculated hash for {filename}: {file_hash}")
                except Exception as e:
                    logging.error(f"Error calculating hash for {filename}: {str(e)}")
    
    def scan_for_unauthorized_files(self) -> List[str]:
        """
        Scan the system for unauthorized verification files.
        
        Returns:
            List of paths to unauthorized files
        """
        unauthorized_files = []
        
        # Check current directory and subdirectories
        for root, dirs, files in os.walk('.'):
            for file in files:
                # Check for suspicious filenames
                file_lowercase = file.lower()
                
                # Skip files in __pycache__ directories
                if "__pycache__" in root:
                    continue
                    
                # Skip standard system files
                if file in [".env", ".gitignore", "README.md", "LICENSE"]:
                    continue
                
                # Flag unauthorized verification files
                if any(pattern in file_lowercase for pattern in UNAUTHORIZED_PATTERNS):
                    file_path = os.path.join(root, file)
                    unauthorized_files.append(file_path)
                    logging.warning(f"Found unauthorized file: {file_path}")
                    continue
                
                # Check suspicious files more carefully
                if any(pattern in file_lowercase for pattern in SUSPICIOUS_PATTERNS):
                    file_path = os.path.join(root, file)
                    
                    # Skip authorized files
                    if file in AUTHORIZED_FILES:
                        continue
                    
                    # Check file content for unauthorized claims
                    try:
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            content_text = content.decode('utf-8', errors='ignore').lower()
                            
                            # Look for competing authorship claims
                            if "author" in content_text and SOVEREIGN_AUTHOR.lower() not in content_text:
                                if "verification" in content_text or "authorship" in content_text:
                                    unauthorized_files.append(file_path)
                                    logging.warning(f"Found competing authorship claim in: {file_path}")
                    except Exception as e:
                        logging.error(f"Error checking file {file_path}: {str(e)}")
                        
        self.last_scan_time = datetime.now().isoformat()
        logging.info(f"Scan completed. Found {len(unauthorized_files)} unauthorized files.")
        return unauthorized_files
    
    def neutralize_unauthorized_files(self, unauthorized_files: List[str]) -> int:
        """
        Neutralize unauthorized verification files.
        
        Args:
            unauthorized_files: List of paths to unauthorized files
            
        Returns:
            Number of files neutralized
        """
        neutralized_count = 0
        
        for file_path in unauthorized_files:
            try:
                # Create backup before removing
                backup_path = f"{file_path}.backup"
                with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
                    dst.write(src.read())
                
                # Remove the unauthorized file
                os.remove(file_path)
                
                self.neutralized_files.append({
                    "file_path": file_path,
                    "backup_path": backup_path,
                    "timestamp": datetime.now().isoformat()
                })
                
                neutralized_count += 1
                logging.info(f"Neutralized unauthorized file: {file_path}")
                self.log_event("file_neutralized", f"Neutralized unauthorized file: {file_path}")
                
            except Exception as e:
                logging.error(f"Error neutralizing file {file_path}: {str(e)}")
                self.log_event("neutralization_error", f"Error neutralizing file {file_path}: {str(e)}")
        
        return neutralized_count
    
    def verify_integrity_of_authorized_files(self) -> Dict[str, bool]:
        """
        Verify the integrity of authorized verification files.
        
        Returns:
            Dictionary mapping filenames to integrity status (True if intact)
        """
        integrity_status = {}
        
        for filename, original_hash in AUTHORIZED_FILES.items():
            if not original_hash:  # Skip files without stored hashes
                continue
                
            if os.path.exists(filename):
                try:
                    with open(filename, 'rb') as f:
                        file_content = f.read()
                        current_hash = hashlib.sha256(file_content).hexdigest()
                        
                        is_intact = current_hash == original_hash
                        integrity_status[filename] = is_intact
                        
                        if not is_intact:
                            logging.warning(f"Integrity check failed for {filename}")
                            self.log_event("integrity_failure", f"Integrity check failed for {filename}")
                        
                except Exception as e:
                    logging.error(f"Error checking integrity for {filename}: {str(e)}")
                    integrity_status[filename] = False
            else:
                logging.warning(f"Authorized file missing: {filename}")
                integrity_status[filename] = False
                
        return integrity_status
    
    def log_event(self, event_type: str, message: str) -> Dict[str, Any]:
        """
        Log a security event.
        
        Args:
            event_type: Type of security event
            message: Event message
            
        Returns:
            Event record
        """
        event = {
            "event_type": event_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "system_name": SYSTEM_NAME,
            "author": SOVEREIGN_AUTHOR
        }
        
        self.status_log.append(event)
        return event
    
    def export_status_report(self, output_path: str = "guardian_shield_report.json") -> str:
        """
        Export a status report of Guardian Shield activities.
        
        Args:
            output_path: Path to save the report
            
        Returns:
            Path to the exported report
        """
        report = {
            "system_name": SYSTEM_NAME,
            "author": SOVEREIGN_AUTHOR,
            "report_timestamp": datetime.now().isoformat(),
            "protection_active": self.protection_active,
            "last_scan_time": self.last_scan_time,
            "neutralized_files": self.neutralized_files,
            "authorized_files": AUTHORIZED_FILES,
            "status_log": self.status_log
        }
        
        try:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            logging.info(f"Status report exported to: {output_path}")
            return output_path
        except Exception as e:
            logging.error(f"Error exporting status report: {str(e)}")
            return ""
    
    def run_protection_cycle(self) -> Dict[str, Any]:
        """
        Run a complete protection cycle.
        
        Returns:
            Protection cycle results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "unauthorized_files_found": 0,
            "files_neutralized": 0,
            "integrity_checks": {},
            "status": "completed"
        }
        
        try:
            # Scan for unauthorized files
            unauthorized_files = self.scan_for_unauthorized_files()
            results["unauthorized_files_found"] = len(unauthorized_files)
            
            # Neutralize unauthorized files
            if unauthorized_files:
                neutralized_count = self.neutralize_unauthorized_files(unauthorized_files)
                results["files_neutralized"] = neutralized_count
            
            # Verify integrity of authorized files
            integrity_status = self.verify_integrity_of_authorized_files()
            results["integrity_checks"] = integrity_status
            
        except Exception as e:
            logging.error(f"Error in protection cycle: {str(e)}")
            results["status"] = "error"
            results["error_message"] = str(e)
            
        self.log_event("protection_cycle", f"Protection cycle completed with status: {results['status']}")
        return results

def main():
    """Main function to run the Guardian Shield Protection System."""
    print("\n" + "=" * 80)
    print("TRUEALPHASPIRAL GUARDIAN SHIELD PROTECTION SYSTEM")
    print("Architect: Russell Nordland")
    print("=" * 80)
    
    guardian = GuardianShield()
    
    print("\nRunning protection cycle...")
    results = guardian.run_protection_cycle()
    
    print(f"\nProtection cycle completed at: {results['timestamp']}")
    print(f"Unauthorized files found: {results['unauthorized_files_found']}")
    
    if results['unauthorized_files_found'] > 0:
        print(f"Files neutralized: {results['files_neutralized']}")
    
    print("\nIntegrity check results:")
    for file, status in results['integrity_checks'].items():
        status_text = "✅ Intact" if status else "❌ Compromised"
        print(f"  {file}: {status_text}")
    
    # Export report
    report_path = guardian.export_status_report()
    if report_path:
        print(f"\nDetailed report exported to: {report_path}")
        
    print("\n" + "=" * 80)

if __name__ == "__main__":
    # If run directly, execute the protection system
    main()