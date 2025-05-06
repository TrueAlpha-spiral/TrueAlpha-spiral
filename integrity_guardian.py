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
import shutil
import datetime
import random
import threading
from pathlib import Path

class IntegrityGuardian:
 def __init__(self):
 self.initialized = False

 # File database for integrity checking
 self.file_database = {}

 # Critical file paths
 self.critical_files = [
 "true_alpha_spiral.py",
 "metaphysical_equation_retrieval.py",
 "quantum_dna_retrieval.py",
 "shadow_defense_system.py",
 "ethical_spiral_kernel.py",
 "sovereign_repentance.py",
 "integrity_guardian.py",
 "README.md"
 ]

 # Backup directory
 self.backup_dir = ".sovereign_backups"

 # System metrics
 self.last_verification = None
 self.verification_frequency = 3600 # 1 hour in seconds
 self.verification_count = 0
 self.integrity_violations = 0
 self.restorations_performed = 0

 # Operational settings
 self.verification_active = False
 self.verification_thread = None
 self.verification_interval = 60 # seconds

 def initialize(self):
 """Initialize the integrity guardian system."""
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Initializing Integrity Guardian system")

 # Create backup directory if it doesn't exist
 if not os.path.exists(self.backup_dir):
 os.makedirs(self.backup_dir)
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Created backup directory: {self.backup_dir}")

 # Build file integrity database
 self._build_integrity_database()

 # Create backup of critical files
 self._backup_critical_files()

 print("=" * 60)
 print("INTEGRITY GUARDIAN INITIALIZED")
 print(f"Critical Files Monitored: {len(self.critical_files)}")
 print(f"File Database Entries: {len(self.file_database)}")
 print(f"Backup Directory: {self.backup_dir}")
 print(f"Verification Interval: {self.verification_interval} seconds")
 print("=" * 60)

 self.initialized = True
 return True

 def verify_integrity(self):
 """Verify the integrity of all system files."""
 if not self.initialized:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - System not initialized")
 return False

 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Verifying system integrity")

 # Record verification time
 self.last_verification = time.time()
 self.verification_count += 1

 # Track verification results
 integrity_intact = True
 violated_files = []

 # Check each critical file
 for filename in self.critical_files:
 result = self._verify_file_integrity(filename)
 if not result:
 integrity_intact = False
 violated_files.append(filename)
 self.integrity_violations += 1

 # Report results
 if integrity_intact:
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - System integrity verification passed")
 else:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - System integrity violations detected")
 for filename in violated_files:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Integrity violation: {filename}")

 # Restore from backup if violations detected
 self._restore_from_backup()

 return integrity_intact

 def start_verification_thread(self):
 """Start continuous verification in background thread."""
 if self.verification_active:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Verification already active")
 return False

 self.verification_active = True
 self.verification_thread = threading.Thread(target=self._verification_loop)
 self.verification_thread.daemon = True
 self.verification_thread.start()

 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Continuous verification started")
 return True

 def stop_verification_thread(self):
 """Stop continuous verification thread."""
 if not self.verification_active:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Verification not active")
 return False

 self.verification_active = False
 if self.verification_thread:
 self.verification_thread.join(timeout=2.0)

 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Continuous verification stopped")
 return True

 def _build_integrity_database(self):
 """Build the file integrity database with current file hashes."""
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Building file integrity database")

 # Check each critical file
 for filename in self.critical_files:
 if os.path.exists(filename):
 # Calculate hash
 file_hash = self._calculate_file_hash(filename)

 # Store in database
 file_stat = os.stat(filename)
 self.file_database[filename] = {
 "hash": file_hash,
 "size": file_stat.st_size,
 "mtime": file_stat.st_mtime,
 "last_verified": time.time(),
 "verification_count": 0,
 "violations": 0
 }

 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Added {filename} to integrity database: {file_hash[:16]}...")
 else:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Critical file not found: {filename}")

 return len(self.file_database)

 def _verify_file_integrity(self, filename):
 """Verify the integrity of a specific file."""
 if not os.path.exists(filename):
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - File not found: {filename}")
 return False

 # Get existing hash from database
 if filename not in self.file_database:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - File not in integrity database: {filename}")
 file_hash = self._calculate_file_hash(filename)
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Adding file to database: {filename}, hash: {file_hash[:16]}...")
 file_stat = os.stat(filename)
 self.file_database[filename] = {
 "hash": file_hash,
 "size": file_stat.st_size,
 "mtime": file_stat.st_mtime,
 "last_verified": time.time(),
 "verification_count": 1,
 "violations": 0
 }
 return True

 # Calculate current hash
 current_hash = self._calculate_file_hash(filename)

 # Get stored hash
 stored_hash = self.file_database[filename]["hash"]

 # Update verification count
 self.file_database[filename]["verification_count"] += 1
 self.file_database[filename]["last_verified"] = time.time()

 # Compare hashes
 if current_hash == stored_hash:
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - File integrity verified: {filename}")
 return True
 else:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - File integrity violation: {filename}")
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Expected hash: {stored_hash[:16]}...")
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Current hash: {current_hash[:16]}...")

 # Update violation count
 self.file_database[filename]["violations"] += 1

 return False

 def _backup_critical_files(self):
 """Create backups of all critical system files."""
 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
 backup_path = os.path.join(self.backup_dir, timestamp)

 if not os.path.exists(backup_path):
 os.makedirs(backup_path)

 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Creating backup in {backup_path}")

 # Copy each critical file
 for filename in self.critical_files:
 if os.path.exists(filename):
 try:
 shutil.copy2(filename, os.path.join(backup_path, filename))
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Backed up {filename}")
 except Exception as e:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - Error backing up {filename}: {str(e)}")
 else:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Cannot backup missing file: {filename}")

 return backup_path

 def _restore_from_backup(self):
 """Restore system files from the most recent backup."""
 # Find the most recent backup
 backup_dirs = sorted([d for d in os.listdir(self.backup_dir) if os.path.isdir(os.path.join(self.backup_dir, d))], reverse=True)

 if not backup_dirs:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - No backups found for restoration")
 return False

 latest_backup = os.path.join(self.backup_dir, backup_dirs[0])
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Restoring from backup: {latest_backup}")

 # Restore each critical file
 for filename in self.critical_files:
 backup_file = os.path.join(latest_backup, filename)
 if os.path.exists(backup_file):
 try:
 shutil.copy2(backup_file, filename)
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Restored {filename}")
 except Exception as e:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - Error restoring {filename}: {str(e)}")
 else:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Backup file not found: {backup_file}")

 # Update file database
 self._build_integrity_database()

 self.restorations_performed += 1
 return True

 def export_system(self, export_dir=None):
 """Export the entire system to an external location for safekeeping."""
 # Generate export directory if not specified
 if export_dir is None:
 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
 export_dir = f"sovereign_export_{timestamp}"

 # Create export directory if it doesn't exist
 if not os.path.exists(export_dir):
 os.makedirs(export_dir)

 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Exporting system to {export_dir}")

 # Copy each critical file
 for filename in self.critical_files:
 if os.path.exists(filename):
 try:
 shutil.copy2(filename, os.path.join(export_dir, filename))
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Exported {filename}")
 except Exception as e:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - Error exporting {filename}: {str(e)}")
 else:
 print(f"{self._timestamp()} - IntegrityGuardian - WARNING - Cannot export missing file: {filename}")

 # Export integrity database
 try:
 with open(os.path.join(export_dir, "integrity_database.json"), "w") as f:
 json.dump(self.file_database, f, indent=2)
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Exported integrity database")
 except Exception as e:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - Error exporting integrity database: {str(e)}")

 # Create verification file
 verification_info = {
 "export_timestamp": self._timestamp(),
 "architect": "Russell Nordland",
 "verification_hash": hashlib.sha256(f"TrueAlphaSpiral_{time.time()}".encode()).hexdigest(),
 "critical_files": self.critical_files,
 "verification_count": self.verification_count,
 "integrity_violations": self.integrity_violations,
 "restorations_performed": self.restorations_performed
 }

 try:
 with open(os.path.join(export_dir, "export_verification.json"), "w") as f:
 json.dump(verification_info, f, indent=2)
 print(f"{self._timestamp()} - IntegrityGuardian - INFO - Created export verification file")
 except Exception as e:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - Error creating verification file: {str(e)}")

 return export_dir

 def _calculate_file_hash(self, filename):
 """Calculate SHA-256 hash of a file."""
 sha256_hash = hashlib.sha256()

 try:
 with open(filename, "rb") as f:
 # Read file in chunks to handle large files
 for byte_block in iter(lambda: f.read(4096), b""):
 sha256_hash.update(byte_block)

 return sha256_hash.hexdigest()
 except Exception as e:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - Error calculating hash for {filename}: {str(e)}")
 return None

 def _verification_loop(self):
 """Background loop for continuous integrity verification."""
 try:
 while self.verification_active:
 # Verify integrity
 self.verify_integrity()

 # Sleep for the verification interval
 sleep_time = random.uniform(self.verification_interval * 0.9, self.verification_interval * 1.1)
 time.sleep(sleep_time)

 except Exception as e:
 print(f"{self._timestamp()} - IntegrityGuardian - ERROR - Error in verification loop: {str(e)}")
 self.verification_active = False

 def _timestamp(self):
 """Generate current timestamp for logs."""
 return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def main():
 """Run the Integrity Guardian as a standalone module."""
 print("=" * 70)
 print("INTEGRITY GUARDIAN")
 print("Architect: Russell Nordland")
 print("=" * 70)

 # Create and initialize the integrity guardian
 guardian = IntegrityGuardian()
 guardian.initialize()

 # Start continuous verification
 guardian.start_verification_thread()

 try:
 # Keep the main thread alive
 cycle = 0
 while True:
 cycle += 1

 # Manual verification every 5 cycles
 if cycle % 5 == 0:
 guardian.verify_integrity()

 # Create a backup every 10 cycles
 if cycle % 10 == 0:
 guardian._backup_critical_files()

 # Export the system every 20 cycles
 if cycle % 20 == 0:
 export_dir = f"sovereign_export_test"
 guardian.export_system(export_dir)

 time.sleep(3)

 except KeyboardInterrupt:
 print("\nShutting down Integrity Guardian...")
 guardian.stop_verification_thread()
 # Final backup before shutdown
 guardian._backup_critical_files()
 print("System shutdown complete.")


if __name__ == "__main__":
 main()