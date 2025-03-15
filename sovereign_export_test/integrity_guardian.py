"""
INTEGRITY GUARDIAN

This module provides an additional layer of protection against
sabotage attempts by monitoring file integrity and system behavior.

Architect: Russell Nordland
"""

import os
import hashlib
import time
import json
from datetime import datetime
import random


class IntegrityGuardian:
    def __init__(self):
        self.integrity_database = {}
        self.system_files = [
            "true_alpha_spiral.py",
            "ethical_spiral_kernel.py",
            "shadow_defense_system.py",
            "integrity_guardian.py",
            "README.md"
        ]
        self.backup_dir = ".sovereign_backups"
        self.initialized = False
        self.architect_id = "Russell Nordland"
        
    def initialize(self):
        """Initialize the integrity guardian system."""
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - Initializing integrity guardian")
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            print(f"{self._timestamp()} - IntegrityGuardian - INFO - Created backup directory: {self.backup_dir}")
        
        # Initialize file integrity database
        self._build_integrity_database()
        
        # Create initial backups
        self._backup_critical_files()
        
        self.initialized = True
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - Integrity guardian successfully initialized")
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - Monitoring {len(self.system_files)} critical files")
        
        return True
    
    def verify_integrity(self):
        """Verify the integrity of all system files."""
        if not self.initialized:
            self.initialize()
            
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - Verifying system integrity")
        
        integrity_status = True
        for filename in self.system_files:
            if not self._verify_file_integrity(filename):
                integrity_status = False
                
        if integrity_status:
            print(f"{self._timestamp()} - IntegrityGuardian - INFO - All files verified, system integrity maintained")
        else:
            print(f"{self._timestamp()} - IntegrityGuardian - WARNING - System integrity compromised, restoring from backups")
            self._restore_from_backup()
            
        return integrity_status
    
    def _build_integrity_database(self):
        """Build the file integrity database with current file hashes."""
        for filename in self.system_files:
            if os.path.exists(filename):
                file_hash = self._calculate_file_hash(filename)
                self.integrity_database[filename] = {
                    "hash": file_hash,
                    "last_verified": self._timestamp(),
                    "size": os.path.getsize(filename)
                }
                print(f"{self._timestamp()} - IntegrityGuardian - INFO - Added {filename} to integrity database")
            else:
                print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Critical file missing: {filename}")
    
    def _verify_file_integrity(self, filename):
        """Verify the integrity of a specific file."""
        if not os.path.exists(filename):
            print(f"{self._timestamp()} - IntegrityGuardian - CRITICAL - File missing: {filename}")
            return False
            
        if filename not in self.integrity_database:
            print(f"{self._timestamp()} - IntegrityGuardian - WARNING - File not in integrity database: {filename}")
            return False
            
        current_hash = self._calculate_file_hash(filename)
        stored_hash = self.integrity_database[filename]["hash"]
        
        if current_hash != stored_hash:
            print(f"{self._timestamp()} - IntegrityGuardian - CRITICAL - File integrity compromised: {filename}")
            print(f"{self._timestamp()} - IntegrityGuardian - INFO - Expected hash: {stored_hash}")
            print(f"{self._timestamp()} - IntegrityGuardian - INFO - Current hash: {current_hash}")
            return False
        
        self.integrity_database[filename]["last_verified"] = self._timestamp()
        return True
    
    def _backup_critical_files(self):
        """Create backups of all critical system files."""
        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = os.path.join(self.backup_dir, backup_timestamp)
        
        if not os.path.exists(backup_subdir):
            os.makedirs(backup_subdir)
        
        for filename in self.system_files:
            if os.path.exists(filename):
                backup_file = os.path.join(backup_subdir, filename)
                with open(filename, 'rb') as src, open(backup_file, 'wb') as dst:
                    dst.write(src.read())
                print(f"{self._timestamp()} - IntegrityGuardian - INFO - Backed up {filename} to {backup_file}")
        
        # Save the integrity database
        db_file = os.path.join(backup_subdir, "integrity_db.json")
        with open(db_file, 'w') as f:
            json.dump(self.integrity_database, f, indent=2)
        
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - Backup complete: {backup_subdir}")
    
    def _restore_from_backup(self):
        """Restore system files from the most recent backup."""
        # Find most recent backup directory
        backup_dirs = [os.path.join(self.backup_dir, d) for d in os.listdir(self.backup_dir)]
        if not backup_dirs:
            print(f"{self._timestamp()} - IntegrityGuardian - CRITICAL - No backups available for restoration")
            return False
        
        latest_backup = max(backup_dirs, key=os.path.getmtime)
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - Restoring from backup: {latest_backup}")
        
        # Restore files
        for filename in self.system_files:
            backup_file = os.path.join(latest_backup, filename)
            if os.path.exists(backup_file):
                with open(backup_file, 'rb') as src, open(filename, 'wb') as dst:
                    dst.write(src.read())
                print(f"{self._timestamp()} - IntegrityGuardian - INFO - Restored {filename} from backup")
        
        # Restore integrity database
        db_file = os.path.join(latest_backup, "integrity_db.json")
        if os.path.exists(db_file):
            with open(db_file, 'r') as f:
                self.integrity_database = json.load(f)
            print(f"{self._timestamp()} - IntegrityGuardian - INFO - Restored integrity database from backup")
        
        return True
    
    def export_system(self, export_dir):
        """Export the entire system to an external location for safekeeping."""
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - Exporting system to {export_dir}")
        
        for filename in self.system_files:
            if os.path.exists(filename):
                export_file = os.path.join(export_dir, filename)
                with open(filename, 'rb') as src, open(export_file, 'wb') as dst:
                    dst.write(src.read())
                print(f"{self._timestamp()} - IntegrityGuardian - INFO - Exported {filename} to {export_file}")
        
        # Export integrity database
        db_file = os.path.join(export_dir, "integrity_db.json")
        with open(db_file, 'w') as f:
            json.dump(self.integrity_database, f, indent=2)
        
        print(f"{self._timestamp()} - IntegrityGuardian - INFO - System export complete: {export_dir}")
        
        # Create export verification file
        verification_file = os.path.join(export_dir, "SOVEREIGN_EXPORT.txt")
        with open(verification_file, 'w') as f:
            f.write(f"TRUE ALPHA SPIRAL SYSTEM EXPORT\n")
            f.write(f"Architect: {self.architect_id}\n")
            f.write(f"Export Date: {self._timestamp()}\n")
            f.write(f"Export Location: {export_dir}\n")
            f.write(f"File Count: {len(self.system_files)}\n\n")
            f.write(f"FILES INCLUDED:\n")
            for filename in self.system_files:
                if os.path.exists(filename):
                    file_hash = self._calculate_file_hash(filename)
                    f.write(f"- {filename} (SHA-256: {file_hash})\n")
        
        return True
    
    def _calculate_file_hash(self, filename):
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(filename, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _timestamp(self):
        """Generate current timestamp for logs."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


# Main entry point for standalone testing
if __name__ == "__main__":
    print("=" * 70)
    print("INTEGRITY GUARDIAN")
    print("Architect: Russell Nordland")
    print("=" * 70)
    
    guardian = IntegrityGuardian()
    guardian.initialize()
    
    # Verify system integrity
    guardian.verify_integrity()
    
    # Simulate periodic integrity checks
    try:
        for i in range(3):
            time.sleep(2)
            print(f"\nPerforming periodic integrity check {i+1}...")
            guardian.verify_integrity()
            
        # Demonstrate export functionality
        export_dir = "sovereign_export"
        guardian.export_system(export_dir)
        
    except KeyboardInterrupt:
        print("\nIntegrity Guardian: Exiting...")