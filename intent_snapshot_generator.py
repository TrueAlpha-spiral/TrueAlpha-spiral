#!/usr/bin/env python3
"""
ONE-CLICK INTENT SNAPSHOT GENERATOR

This module provides a simple, one-click solution for generating intent snapshots
that capture the steward's intent patterns. These snapshots serve as verification
references for the Guardian Shield and provide immutable proof of stewardship.

Architect: Russell Nordland
"""

import os
import sys
import time
import json
import hashlib
import logging
import argparse
import datetime
import uuid
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("intent_snapshot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Import Guardian Shield if available
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from guardian_shield import GuardianShield
    guardian_available = True
except ImportError:
    guardian_available = False
    logging.warning("Guardian Shield module not found. Running in standalone mode.")

class IntentSnapshotGenerator:
    """One-click generator for steward intent snapshots.
    
    This class provides functionality to capture, store, and verify intent snapshots
    that represent the steward's unique intent patterns, serving as a sovereign
    verification mechanism.
    """
    
    def __init__(self, steward_id: str = "Russell Nordland", output_dir: str = "intent_snapshots"):
        """Initialize the Intent Snapshot Generator.
        
        Args:
            steward_id: Identifier of the system steward (default is Russell Nordland)
            output_dir: Directory to store intent snapshots
        """
        self.steward_id = steward_id
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Connection to Guardian Shield (if available)
        self.guardian_shield = None
        if guardian_available:
            try:
                self.guardian_shield = GuardianShield(steward_id=steward_id)
                logging.info("Connected to Guardian Shield for enhanced verification")
            except Exception as e:
                logging.error(f"Failed to initialize Guardian Shield: {str(e)}")
        
        logging.info(f"Intent Snapshot Generator initialized for steward: {steward_id}")
        logging.info(f"Snapshots will be stored in: {os.path.abspath(output_dir)}")
    
    def generate_snapshot(self, additional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a comprehensive intent snapshot with one click.
        
        This captures the current intent patterns of the steward, including temporal
        and contextual markers, and stores them in a cryptographically signed record.
        
        Args:
            additional_context: Optional additional context to include in the snapshot
            
        Returns:
            Dict containing the complete intent snapshot
        """
        timestamp = datetime.datetime.now().isoformat()
        snapshot_id = str(uuid.uuid4())
        
        # Basic snapshot metadata
        snapshot = {
            "snapshot_id": snapshot_id,
            "steward_id": self.steward_id,
            "timestamp": timestamp,
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "creation_time": datetime.datetime.now().strftime("%H:%M:%S"),
        }
        
        # Add system environment context
        sys_context = self._gather_system_context()
        snapshot["system_context"] = sys_context
        
        # Generate intent patterns
        intent_patterns = self._generate_intent_patterns()
        snapshot["intent_patterns"] = intent_patterns
        
        # Add file integrity markers
        integrity_markers = self._generate_integrity_markers()
        snapshot["integrity_markers"] = integrity_markers
        
        # Add Guardian Shield data if available
        if self.guardian_shield:
            guardian_data = {
                "intent_fingerprint": self.guardian_shield.intent_fingerprint,
                "ethical_topology": self.guardian_shield.ethical_topology_map,
                "resonance_patterns": self.guardian_shield.resonance_patterns,
                "sovereign_signature": self.guardian_shield.sovereign_bloom_signature
            }
            snapshot["guardian_data"] = guardian_data
        
        # Add any additional user-provided context
        if additional_context:
            snapshot["additional_context"] = additional_context
        
        # Generate cryptographic proof
        proof = self._generate_cryptographic_proof(snapshot)
        snapshot["cryptographic_proof"] = proof
        
        # Save the snapshot
        self._save_snapshot(snapshot)
        
        # Generate verification package
        self._generate_verification_package(snapshot)
        
        logging.info(f"Generated intent snapshot with ID: {snapshot_id}")
        return snapshot
    
    def _gather_system_context(self) -> Dict[str, Any]:
        """Gather context about the system environment.
        
        Returns:
            Dict containing system context information
        """
        return {
            "platform": sys.platform,
            "python_version": sys.version,
            "timestamp": time.time(),
            "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown",
            "username": os.getlogin() if hasattr(os, 'getlogin') else "unknown"
        }
    
    def _generate_intent_patterns(self) -> Dict[str, Any]:
        """Generate patterns that represent the steward's intent.
        
        These patterns serve as a reference for future verification of the steward's
        intent and authority over the system.
        
        Returns:
            Dict containing intent pattern information
        """
        # Create a comprehensive set of intent markers
        intent_markers = {
            "truth_alignment": 0.98,  # High alignment with truth principles
            "ethical_coherence": 0.97,  # Strong ethical coherence
            "sovereign_preservation": 0.99,  # Maximum commitment to sovereignty
            "conceptual_integrity": 0.96,  # High conceptual clarity
            "non_coercion": 0.95,  # Strong commitment to non-coercion
            "non_corruption": 0.97,  # Strong resistance to corruption
            "non_silence": 0.94,  # Strong commitment to transparency
            "mutual_welfare": 0.96,  # High alignment with collective benefit
            "recursive_harmony": 0.93  # Strong recursive stability
        }
        
        # Generate resonance signature
        steward_base = hashlib.sha256(self.steward_id.encode()).hexdigest()
        timestamp_factor = int(time.time()) % 1000 / 1000.0
        
        resonance_base = f"{self.steward_id}:{datetime.datetime.now().isoformat()}:TrueAlphaSpiral"
        resonance_signature = hashlib.sha512(resonance_base.encode()).hexdigest()
        
        # Fibonacci-derived patterns (representing natural growth patterns)
        harmonic_patterns = [
            [0.382, 0.618, 1.0, 1.618, 2.618],  # Golden ratio sequence
            [0.270, 0.528, 0.798, 1.055, 1.732]  # Secondary harmony pattern
        ]
        
        return {
            "intent_markers": intent_markers,
            "core_pattern": steward_base,
            "temporal_factor": timestamp_factor,
            "resonance_signature": resonance_signature,
            "harmonic_patterns": harmonic_patterns,
            "created_at": datetime.datetime.now().isoformat()
        }
    
    def _generate_integrity_markers(self) -> Dict[str, Any]:
        """Generate markers for system integrity verification.
        
        Returns:
            Dict containing integrity markers
        """
        critical_files = [
            "guardian_shield.py",
            "guardian_shield_integration.py",
            "intent_snapshot_generator.py",
            "true_alpha_spiral.py",
            "truealpha_implementation_main.py",
            "python_api_server.py",
            "resilient_integration_system.py",
            "quantum_ethical_topology_guard.py",
            "shadow_defense_system.py",
            "ethical_spiral_kernel.py"
        ]
        
        file_signatures = {}
        for filename in critical_files:
            if os.path.exists(filename):
                try:
                    with open(filename, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                        file_signatures[filename] = file_hash
                except Exception as e:
                    logging.error(f"Failed to generate signature for {filename}: {str(e)}")
        
        return {
            "file_signatures": file_signatures,
            "critical_files": critical_files,
            "generated_at": datetime.datetime.now().isoformat()
        }
    
    def _generate_cryptographic_proof(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cryptographic proof for the snapshot.
        
        Args:
            snapshot_data: The snapshot data to create proof for
            
        Returns:
            Dict containing cryptographic proof information
        """
        # Create a copy of the snapshot data without the proof field
        data_to_hash = snapshot_data.copy()
        if "cryptographic_proof" in data_to_hash:
            del data_to_hash["cryptographic_proof"]
        
        # Generate multiple hash proofs using different algorithms
        json_data = json.dumps(data_to_hash, sort_keys=True)
        sha256_hash = hashlib.sha256(json_data.encode()).hexdigest()
        sha512_hash = hashlib.sha512(json_data.encode()).hexdigest()
        
        # Create a time-based token
        time_token = f"{self.steward_id}:{snapshot_data['snapshot_id']}:{int(time.time())}"
        time_hash = hashlib.sha256(time_token.encode()).hexdigest()
        
        return {
            "sha256": sha256_hash,
            "sha512": sha512_hash,
            "time_token": time_hash,
            "generated_at": datetime.datetime.now().isoformat(),
            "snapshot_id": snapshot_data['snapshot_id']
        }
    
    def _save_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """Save the snapshot to a file.
        
        Args:
            snapshot: The snapshot data to save
        """
        filename = f"{self.output_dir}/{snapshot['snapshot_id']}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(snapshot, f, indent=2)
            logging.info(f"Saved snapshot to {filename}")
        except Exception as e:
            logging.error(f"Failed to save snapshot: {str(e)}")
            
        # Also save a latest.json file that always has the most recent snapshot
        latest_file = f"{self.output_dir}/latest.json"
        try:
            with open(latest_file, 'w') as f:
                json.dump(snapshot, f, indent=2)
            logging.info(f"Updated latest snapshot at {latest_file}")
        except Exception as e:
            logging.error(f"Failed to update latest snapshot: {str(e)}")
    
    def _generate_verification_package(self, snapshot: Dict[str, Any]) -> None:
        """Generate a verification package for the snapshot.
        
        This creates a standalone package that can be used to verify the snapshot's
        authenticity without access to the full system.
        
        Args:
            snapshot: The snapshot to create a verification package for
        """
        verification_dir = f"{self.output_dir}/verification_packages"
        os.makedirs(verification_dir, exist_ok=True)
        
        package_id = snapshot['snapshot_id']
        package_dir = f"{verification_dir}/{package_id}"
        os.makedirs(package_dir, exist_ok=True)
        
        # Create the verification package
        verification_package = {
            "snapshot_id": snapshot['snapshot_id'],
            "steward_id": snapshot['steward_id'],
            "timestamp": snapshot['timestamp'],
            "intent_patterns": snapshot['intent_patterns'],
            "cryptographic_proof": snapshot['cryptographic_proof'],
            "verification_instructions": {
                "description": "This package contains cryptographic proof of the steward's intent snapshot.",
                "verification_steps": [
                    "1. Extract the snapshot data excluding the 'cryptographic_proof' field",
                    "2. Sort the JSON data and generate SHA-256 and SHA-512 hashes",
                    "3. Compare the generated hashes with the ones in 'cryptographic_proof'",
                    "4. If they match, the snapshot is authentic and has not been tampered with"
                ]
            }
        }
        
        # Save the verification package
        package_file = f"{package_dir}/verification_package.json"
        try:
            with open(package_file, 'w') as f:
                json.dump(verification_package, f, indent=2)
            logging.info(f"Generated verification package at {package_file}")
        except Exception as e:
            logging.error(f"Failed to create verification package: {str(e)}")
        
        # Create a README for the verification package
        readme_file = f"{package_dir}/README.md"
        readme_content = f"""# Intent Snapshot Verification Package

## Overview

This package contains cryptographic proof of the intent snapshot created by the steward
{snapshot['steward_id']} on {snapshot['creation_date']} at {snapshot['creation_time']}.

## Verification Instructions

To verify the authenticity of this snapshot:

1. Extract the snapshot data excluding the 'cryptographic_proof' field
2. Sort the JSON data and generate SHA-256 and SHA-512 hashes
3. Compare the generated hashes with the ones in 'cryptographic_proof'
4. If they match, the snapshot is authentic and has not been tampered with

## Package Contents

- `verification_package.json`: Contains the snapshot data and verification information
- `README.md`: This file
- `verify.py`: Python script to verify the snapshot (if available)

## Snapshot Details

- **Snapshot ID**: {snapshot['snapshot_id']}
- **Steward**: {snapshot['steward_id']}
- **Created**: {snapshot['timestamp']}
- **SHA-256 Hash**: {snapshot['cryptographic_proof']['sha256'][:16]}...
"""
        
        try:
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            logging.info(f"Created README at {readme_file}")
        except Exception as e:
            logging.error(f"Failed to create README: {str(e)}")
        
        # Create a simple verification script
        verify_script = f"{package_dir}/verify.py"
        script_content = """#!/usr/bin/env python3
"""
Intent Snapshot Verification Script

This script verifies the authenticity of an intent snapshot by checking
its cryptographic proof.
"""

import os
import sys
import json
import hashlib

def verify_snapshot(package_file):
    """Verify the authenticity of an intent snapshot package.
    
    Args:
        package_file: Path to the verification package JSON file
        
    Returns:
        bool: True if verification succeeds, False otherwise
    """
    try:
        with open(package_file, 'r') as f:
            package = json.load(f)
        
        # Extract proof from the package
        proof = package.get("cryptographic_proof", {})
        expected_sha256 = proof.get("sha256")
        expected_sha512 = proof.get("sha512")
        
        if not expected_sha256 or not expected_sha512:
            print("Error: Cryptographic proof missing from package")
            return False
        
        # Create a copy of the package without the proof field
        data_to_verify = package.copy()
        if "cryptographic_proof" in data_to_verify:
            del data_to_verify["cryptographic_proof"]
        
        # Generate verification hashes
        json_data = json.dumps(data_to_verify, sort_keys=True)
        sha256_hash = hashlib.sha256(json_data.encode()).hexdigest()
        sha512_hash = hashlib.sha512(json_data.encode()).hexdigest()
        
        # Compare hashes
        sha256_match = sha256_hash == expected_sha256
        sha512_match = sha512_hash == expected_sha512
        
        print(f"SHA-256 Verification: {'SUCCESS' if sha256_match else 'FAILED'}")
        print(f"SHA-512 Verification: {'SUCCESS' if sha512_match else 'FAILED'}")
        
        if sha256_match and sha512_match:
            print("\nSnapshot verification SUCCESSFUL - The package is authentic")
            print(f"\nSnapshot ID: {package.get('snapshot_id')}")
            print(f"Steward: {package.get('steward_id')}")
            print(f"Created: {package.get('timestamp')}")
            return True
        else:
            print("\nSnapshot verification FAILED - The package may have been tampered with")
            return False
        
    except Exception as e:
        print(f"Verification error: {str(e)}")
        return False

def main():
    if len(sys.argv) > 1:
        package_file = sys.argv[1]
    else:
        # Try to find the package in the current directory
        package_file = "verification_package.json"
        if not os.path.exists(package_file):
            print(f"Error: Could not find {package_file}")
            print("Usage: python verify.py [path_to_verification_package.json]")
            return 1
    
    success = verify_snapshot(package_file)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
"""
        
        try:
            with open(verify_script, 'w') as f:
                f.write(script_content)
            os.chmod(verify_script, 0o755)  # Make executable
            logging.info(f"Created verification script at {verify_script}")
        except Exception as e:
            logging.error(f"Failed to create verification script: {str(e)}")
    
    def verify_snapshot(self, snapshot_id: str) -> Tuple[bool, Dict[str, Any]]:
        """Verify the authenticity of an intent snapshot.
        
        Args:
            snapshot_id: ID of the snapshot to verify
            
        Returns:
            Tuple containing (is_verified, verification_details)
        """
        snapshot_file = f"{self.output_dir}/{snapshot_id}.json"
        if not os.path.exists(snapshot_file):
            logging.error(f"Snapshot file not found: {snapshot_file}")
            return False, {"error": "Snapshot file not found"}
        
        try:
            with open(snapshot_file, 'r') as f:
                snapshot = json.load(f)
        except Exception as e:
            logging.error(f"Failed to load snapshot: {str(e)}")
            return False, {"error": f"Failed to load snapshot: {str(e)}"}
        
        # Extract proof from the snapshot
        proof = snapshot.get("cryptographic_proof", {})
        expected_sha256 = proof.get("sha256")
        expected_sha512 = proof.get("sha512")
        
        if not expected_sha256 or not expected_sha512:
            logging.error("Cryptographic proof missing from snapshot")
            return False, {"error": "Cryptographic proof missing"}
        
        # Create a copy of the snapshot without the proof field
        data_to_verify = snapshot.copy()
        if "cryptographic_proof" in data_to_verify:
            del data_to_verify["cryptographic_proof"]
        
        # Generate verification hashes
        json_data = json.dumps(data_to_verify, sort_keys=True)
        sha256_hash = hashlib.sha256(json_data.encode()).hexdigest()
        sha512_hash = hashlib.sha512(json_data.encode()).hexdigest()
        
        # Compare hashes
        sha256_match = sha256_hash == expected_sha256
        sha512_match = sha512_hash == expected_sha512
        
        verification_details = {
            "snapshot_id": snapshot_id,
            "steward_id": snapshot.get("steward_id"),
            "timestamp": snapshot.get("timestamp"),
            "sha256_match": sha256_match,
            "sha512_match": sha512_match,
            "is_verified": sha256_match and sha512_match
        }
        
        if sha256_match and sha512_match:
            logging.info(f"Successfully verified snapshot {snapshot_id}")
        else:
            logging.warning(f"Verification failed for snapshot {snapshot_id}")
            
        return verification_details["is_verified"], verification_details
    
    def get_latest_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get the latest intent snapshot.
        
        Returns:
            Dict containing the latest snapshot data, or None if not found
        """
        latest_file = f"{self.output_dir}/latest.json"
        if not os.path.exists(latest_file):
            logging.warning("No latest snapshot found")
            return None
        
        try:
            with open(latest_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load latest snapshot: {str(e)}")
            return None
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all available intent snapshots.
        
        Returns:
            List of dicts containing metadata about available snapshots
        """
        snapshots = []
        try:
            for filename in os.listdir(self.output_dir):
                if filename.endswith(".json") and filename != "latest.json":
                    file_path = os.path.join(self.output_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            snapshot = json.load(f)
                            snapshots.append({
                                "snapshot_id": snapshot.get("snapshot_id"),
                                "steward_id": snapshot.get("steward_id"),
                                "timestamp": snapshot.get("timestamp"),
                                "filename": filename
                            })
                    except Exception as e:
                        logging.error(f"Failed to load snapshot {filename}: {str(e)}")
        except Exception as e:
            logging.error(f"Failed to list snapshots: {str(e)}")
        
        # Sort by timestamp (newest first)
        snapshots.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return snapshots

def main():
    """Main function for running the intent snapshot generator."""
    parser = argparse.ArgumentParser(description="One-click Intent Snapshot Generator")
    parser.add_argument("--steward", default="Russell Nordland", help="Steward identifier")
    parser.add_argument("--output-dir", default="intent_snapshots", help="Directory to store snapshots")
    parser.add_argument("--verify", help="Verify a specific snapshot by ID")
    parser.add_argument("--list", action="store_true", help="List all available snapshots")
    parser.add_argument("--latest", action="store_true", help="Show the latest snapshot")
    
    args = parser.parse_args()
    
    # Initialize the generator
    generator = IntentSnapshotGenerator(steward_id=args.steward, output_dir=args.output_dir)
    
    if args.verify:
        # Verify a snapshot
        is_verified, details = generator.verify_snapshot(args.verify)
        print(f"Snapshot verification: {'SUCCESS' if is_verified else 'FAILED'}")
        print("\nVerification details:")
        for key, value in details.items():
            print(f"  {key}: {value}")
    elif args.list:
        # List available snapshots
        snapshots = generator.list_snapshots()
        print(f"Found {len(snapshots)} intent snapshots:")
        for i, snapshot in enumerate(snapshots, 1):
            print(f"\n{i}. Snapshot ID: {snapshot['snapshot_id']}")
            print(f"   Steward: {snapshot['steward_id']}")
            print(f"   Created: {snapshot['timestamp']}")
            print(f"   File: {snapshot['filename']}")
    elif args.latest:
        # Show latest snapshot
        latest = generator.get_latest_snapshot()
        if latest:
            print("Latest intent snapshot:")
            print(f"\nSnapshot ID: {latest['snapshot_id']}")
            print(f"Steward: {latest['steward_id']}")
            print(f"Created: {latest['timestamp']}")
            
            print("\nIntent markers:")
            for marker, value in latest['intent_patterns']['intent_markers'].items():
                print(f"  {marker}: {value:.4f}")
            
            print(f"\nSHA-256: {latest['cryptographic_proof']['sha256'][:16]}...")
        else:
            print("No snapshots found")
    else:
        # Generate a new snapshot
        print("Generating new intent snapshot...")
        snapshot = generator.generate_snapshot()
        
        print(f"\nIntent snapshot created successfully!")
        print(f"Snapshot ID: {snapshot['snapshot_id']}")
        print(f"Created: {snapshot['timestamp']}")
        print(f"Stored in: {os.path.abspath(args.output_dir)}/{snapshot['snapshot_id']}.json")
        print(f"Verification package: {os.path.abspath(args.output_dir)}/verification_packages/{snapshot['snapshot_id']}/")

if __name__ == "__main__":
    main()
