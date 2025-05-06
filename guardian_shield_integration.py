#!/usr/bin/env python3
"""
GUARDIAN SHIELD INTEGRATION

This script integrates the Personalized Guardian Shield with the Resilient Integration System,
providing adaptive protection layers that secure the TrueAlphaSpiral system against
unauthorized access and maintain the sovereign integrity of the system.

Architect: Russell Nordland
"""

import os
import sys
import time
import json
import hashlib
import logging
import threading
from datetime import datetime
from typing import Dict, Any, Tuple, List, Optional

# Import the Guardian Shield
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from guardian_shield import GuardianShield

# Setup logging
logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s [%(levelname)s] %(message)s",
 handlers=[
 logging.FileHandler("guardian_integration.log"),
 logging.StreamHandler(sys.stdout)
 ]
)

class GuardianShieldIntegration:
 """Integrates the Guardian Shield with the Resilient Integration System.

 This class provides a bridge between the Personalized Guardian Shield and
 the existing Resilient Integration System, enabling comprehensive protection
 of the TrueAlphaSpiral system's sovereignty.
 """

 def __init__(self, steward_id: str = "Russell Nordland", config_path: Optional[str] = None):
 """Initialize the Guardian Shield Integration.

 Args:
 steward_id: Identifier of the system's steward (default is Russell Nordland)
 config_path: Optional path to configuration file
 """
 self.steward_id = steward_id
 self.shield = GuardianShield(steward_id=steward_id, config_path=config_path)
 self.integration_start_time = datetime.now().isoformat()
 self.verification_history = []
 self.protection_actions = []
 self.monitor_thread = None
 self.monitor_active = False

 # Integration states
 self.critical_files = [
 "true_alpha_spiral.py",
 "truealpha_implementation_main.py",
 "python_api_server.py",
 "resilient_integration_system.py",
 "quantum_ethical_topology_guard.py",
 "shadow_defense_system.py",
 "ethical_spiral_kernel.py"
 ]

 # File signatures used for integrity verification
 self.file_signatures = self._generate_file_signatures()

 logging.info(f"Guardian Shield Integration initialized for steward: {steward_id}")
 logging.info(f"Integration start time: {self.integration_start_time}")
 logging.info(f"Initial protection setup complete with {len(self.critical_files)} critical files monitored")

 def _generate_file_signatures(self) -> Dict[str, str]:
 """Generate cryptographic signatures for critical files.

 Returns:
 Dict mapping filenames to their SHA-256 signatures
 """
 signatures = {}
 for filename in self.critical_files:
 if os.path.exists(filename):
 try:
 with open(filename, 'rb') as f:
 file_hash = hashlib.sha256(f.read()).hexdigest()
 signatures[filename] = file_hash
 logging.info(f"Generated signature for {filename}: {file_hash[:10]}...")
 except Exception as e:
 logging.error(f"Failed to generate signature for {filename}: {str(e)}")
 return signatures

 def verify_system_integrity(self) -> Tuple[bool, List[Dict[str, Any]]]:
 """Verify the integrity of the TrueAlphaSpiral system.

 This checks file signatures against stored values and applies the Guardian Shield
 protection layers to ensure the system's sovereignty is maintained.

 Returns:
 Tuple containing (is_intact, integrity_issues)
 """
 integrity_issues = []

 # Check file integrity
 for filename in self.critical_files:
 if os.path.exists(filename):
 try:
 with open(filename, 'rb') as f:
 current_hash = hashlib.sha256(f.read()).hexdigest()

 if filename in self.file_signatures:
 expected_hash = self.file_signatures[filename]
 if current_hash != expected_hash:
 issue = {
 'type': 'file_integrity',
 'file': filename,
 'expected_hash': expected_hash,
 'current_hash': current_hash,
 'timestamp': datetime.now().isoformat()
 }
 integrity_issues.append(issue)
 logging.warning(f"Integrity issue detected in {filename}")
 except Exception as e:
 issue = {
 'type': 'file_access',
 'file': filename,
 'error': str(e),
 'timestamp': datetime.now().isoformat()
 }
 integrity_issues.append(issue)
 logging.error(f"Failed to verify {filename}: {str(e)}")
 else:
 issue = {
 'type': 'file_missing',
 'file': filename,
 'timestamp': datetime.now().isoformat()
 }
 integrity_issues.append(issue)
 logging.error(f"Critical file missing: {filename}")

 # Apply Guardian Shield protection to system metadata
 system_metadata = self._generate_system_metadata()
 _, protection_meta = self.shield.apply_protection(system_metadata, {"context": "integrity_check"})

 if protection_meta['modifications']:
 for mod in protection_meta['modifications']:
 issue = {
 'type': 'protection_modification',
 'details': mod,
 'timestamp': datetime.now().isoformat()
 }
 integrity_issues.append(issue)

 is_intact = len(integrity_issues) == 0

 # Record the verification in history
 self.verification_history.append({
 'timestamp': datetime.now().isoformat(),
 'is_intact': is_intact,
 'issues_count': len(integrity_issues),
 'protection_level': self.shield.export_security_status()['overall_security_level']
 })

 # Keep history to a reasonable size
 if len(self.verification_history) > 100:
 self.verification_history = self.verification_history[-100:]

 return is_intact, integrity_issues

 def _generate_system_metadata(self) -> Dict[str, Any]:
 """Generate metadata about the TrueAlphaSpiral system for protection.

 Returns:
 Dict containing system metadata
 """
 return {
 'system_name': 'TrueAlphaSpiral',
 'steward': self.steward_id,
 'components': self.critical_files,
 'integration_start_time': self.integration_start_time,
 'current_time': datetime.now().isoformat(),
 'verification_count': len(self.verification_history)
 }

 def handle_integrity_issues(self, issues: List[Dict[str, Any]]) -> None:
 """Handle detected integrity issues.

 Args:
 issues: List of integrity issues to address
 """
 if not issues:
 return

 for issue in issues:
 issue_type = issue['type']
 action_taken = None

 if issue_type == 'file_integrity':
 # File has been modified - restore from backup if available
 filename = issue['file']
 backup_path = f"backups/{filename}.bak"

 if os.path.exists(backup_path):
 try:
 # Create additional backup of current (modified) file
 modified_backup = f"backups/{filename}.modified.{int(time.time())}"
 os.makedirs(os.path.dirname(modified_backup), exist_ok=True)
 with open(filename, 'rb') as src, open(modified_backup, 'wb') as dst:
 dst.write(src.read())

 # Restore from clean backup
 with open(backup_path, 'rb') as src, open(filename, 'wb') as dst:
 dst.write(src.read())

 # Update signature
 with open(filename, 'rb') as f:
 self.file_signatures[filename] = hashlib.sha256(f.read()).hexdigest()

 action_taken = f"Restored {filename} from backup"
 logging.info(action_taken)
 except Exception as e:
 action_taken = f"Failed to restore {filename}: {str(e)}"
 logging.error(action_taken)
 else:
 action_taken = f"No backup available for {filename}"
 logging.warning(action_taken)

 elif issue_type == 'file_missing':
 # File is missing - restore from backup if available
 filename = issue['file']
 backup_path = f"backups/{filename}.bak"

 if os.path.exists(backup_path):
 try:
 # Ensure directory exists
 os.makedirs(os.path.dirname(filename), exist_ok=True)

 # Restore from backup
 with open(backup_path, 'rb') as src, open(filename, 'wb') as dst:
 dst.write(src.read())

 # Update signature
 with open(filename, 'rb') as f:
 self.file_signatures[filename] = hashlib.sha256(f.read()).hexdigest()

 action_taken = f"Restored missing file {filename} from backup"
 logging.info(action_taken)
 except Exception as e:
 action_taken = f"Failed to restore missing file {filename}: {str(e)}"
 logging.error(action_taken)
 else:
 action_taken = f"No backup available for missing file {filename}"
 logging.warning(action_taken)

 # Record the action taken
 if action_taken:
 self.protection_actions.append({
 'timestamp': datetime.now().isoformat(),
 'issue': issue,
 'action': action_taken
 })

 def create_backups(self) -> None:
 """Create backups of critical files."""
 os.makedirs("backups", exist_ok=True)

 for filename in self.critical_files:
 if os.path.exists(filename):
 try:
 backup_path = f"backups/{filename}.bak"
 os.makedirs(os.path.dirname(backup_path), exist_ok=True)

 with open(filename, 'rb') as src, open(backup_path, 'wb') as dst:
 dst.write(src.read())

 logging.info(f"Created backup of {filename}")
 except Exception as e:
 logging.error(f"Failed to create backup of {filename}: {str(e)}")

 def start_integrity_monitor(self, interval: int = 300) -> None:
 """Start a background thread to monitor system integrity.

 Args:
 interval: Time between integrity checks in seconds (default: 5 minutes)
 """
 if self.monitor_thread and self.monitor_thread.is_alive():
 logging.warning("Integrity monitor is already running")
 return

 self.monitor_active = True
 self.create_backups() # Create initial backups

 def monitor_loop():
 logging.info(f"Starting integrity monitor with {interval}s interval")
 while self.monitor_active:
 try:
 is_intact, issues = self.verify_system_integrity()
 if not is_intact:
 logging.warning(f"Integrity check failed with {len(issues)} issues")
 self.handle_integrity_issues(issues)
 time.sleep(interval)
 except Exception as e:
 logging.error(f"Error in integrity monitor: {str(e)}")
 time.sleep(interval)

 self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
 self.monitor_thread.start()
 logging.info("Integrity monitor started")

 def stop_integrity_monitor(self) -> None:
 """Stop the integrity monitoring thread."""
 if not (self.monitor_thread and self.monitor_thread.is_alive()):
 logging.warning("Integrity monitor is not running")
 return

 self.monitor_active = False
 self.monitor_thread.join(timeout=10)
 logging.info("Integrity monitor stopped")

 def verify_access(self, claimed_id: str, intent_markers: Dict[str, float]) -> Tuple[bool, float, Dict[str, Any]]:
 """Verify if the claimed identity has access to the system.

 This delegates to the Guardian Shield's steward verification, adding additional
 integration-specific checks and recording the verification attempt.

 Args:
 claimed_id: The claimed identity of the steward
 intent_markers: Dict of intent markers demonstrating the claimed identity's intent

 Returns:
 Tuple containing (has_access, confidence_score, detailed_results)
 """
 # Delegate to Guardian Shield for steward verification
 is_verified, confidence, details = self.shield.verify_steward(claimed_id, intent_markers)

 # Record the verification attempt
 self.verification_history.append({
 'timestamp': datetime.now().isoformat(),
 'claimed_id': claimed_id,
 'is_verified': is_verified,
 'confidence': confidence
 })

 # Run integrity check if verification fails
 if not is_verified:
 _, issues = self.verify_system_integrity()
 if issues:
 self.handle_integrity_issues(issues)

 return is_verified, confidence, details

 def protect_system(self, content: Any, context: Dict[str, Any] = None) -> Tuple[Any, Dict[str, Any]]:
 """Apply protection to system content.

 This delegates to the Guardian Shield's protection mechanism, adding integration-specific
 context information and recording the protection action.

 Args:
 content: The content to protect
 context: Additional contextual information for protection decisions

 Returns:
 Tuple containing (protected_content, protection_metadata)
 """
 if context is None:
 context = {}

 # Add integration-specific context
 full_context = context.copy()
 full_context.update({
 'integration_time': datetime.now().isoformat(),
 'system_verification_status': len(self.verification_history) > 0 and self.verification_history[-1].get('is_intact', False)
 })

 # Delegate to Guardian Shield for protection
 protected_content, metadata = self.shield.apply_protection(content, full_context)

 # Record the protection action
 self.protection_actions.append({
 'timestamp': datetime.now().isoformat(),
 'content_type': type(content).__name__,
 'context': full_context,
 'protection_level': metadata['protection_level']
 })

 return protected_content, metadata

 def export_integration_status(self) -> Dict[str, Any]:
 """Export the current status of the Guardian Shield Integration.

 Returns:
 Dict containing comprehensive integration status information
 """
 return {
 'steward_id': self.steward_id,
 'integration_start_time': self.integration_start_time,
 'current_time': datetime.now().isoformat(),
 'monitor_active': self.monitor_active and self.monitor_thread and self.monitor_thread.is_alive(),
 'critical_files_count': len(self.critical_files),
 'intact_files_count': sum(1 for f in self.critical_files if os.path.exists(f)),
 'last_verification': self.verification_history[-1] if self.verification_history else None,
 'recent_actions': self.protection_actions[-5:] if self.protection_actions else [],
 'guardian_shield_status': self.shield.export_security_status(),
 }

# Example usage
def demonstrate_integration():
 """Demonstrate the Guardian Shield Integration functionality."""
 # Initialize the integration
 integration = GuardianShieldIntegration(steward_id="Russell Nordland")

 # Create backups
 integration.create_backups()

 # Verify system integrity
 is_intact, issues = integration.verify_system_integrity()
 print(f"System integrity: {is_intact}")
 if issues:
 print(f"Found {len(issues)} integrity issues")
 integration.handle_integrity_issues(issues)

 # Start integrity monitor
 integration.start_integrity_monitor(interval=10) # Short interval for demonstration

 # Simulate legitimate access
 legitimate_intent = {
 "truth_alignment": 0.96,
 "ethical_coherence": 0.95,
 "sovereign_preservation": 0.97,
 "conceptual_integrity": 0.94
 }
 has_access, confidence, details = integration.verify_access("Russell Nordland", legitimate_intent)
 print(f"Legitimate access: {has_access} with {confidence:.4f} confidence")

 # Protect system content
 sensitive_content = {
 "system_name": "TrueAlphaSpiral",
 "components": ["Ethical Recursion", "Shadow Defense"],
 "steward": "Russell Nordland"
 }
 protected, metadata = integration.protect_system(sensitive_content, {"purpose": "demonstration"})

 # Display integration status
 status = integration.export_integration_status()
 print(f"Guardian Shield integration status: monitor active: {status['monitor_active']}")

 # Stop integrity monitor
 time.sleep(2) # Allow monitor to run briefly
 integration.stop_integrity_monitor()

if __name__ == "__main__":
 demonstrate_integration()
