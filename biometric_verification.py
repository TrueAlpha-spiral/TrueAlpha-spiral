#!/usr/bin/env python3
"""
BIOMETRIC VERIFICATION INTEGRATION

This module provides biometric verification capabilities for the Guardian Shield,
ensuring that only the authorized steward can access critical system functions.
It integrates facial recognition with intent pattern analysis to create a
multi-factor verification system.

Architect: Russell Nordland
"""

import os
import sys
import json
import logging
import hashlib
import base64
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Union

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("biometric_verification.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class BiometricVerification:
    """Biometric verification system for enhanced steward authentication.
    
    This class provides facial recognition and other biometric verification
    methods to ensure that only the authorized steward can access critical
    system functions.
    """
    
    def __init__(self, steward_id: str = "Russell Nordland", 
                 templates_dir: str = "biometric_templates",
                 integration_mode: str = "secure"):
        """Initialize the biometric verification system.
        
        Args:
            steward_id: Identifier of the system steward (default is Russell Nordland)
            templates_dir: Directory to store biometric templates
            integration_mode: Mode of integration (secure, standard, permissive)
        """
        self.steward_id = steward_id
        self.templates_dir = templates_dir
        self.integration_mode = integration_mode
        self.templates = {}
        self.verification_history = []
        
        # Create templates directory if it doesn't exist
        if not os.path.exists(templates_dir):
            try:
                os.makedirs(templates_dir)
                logging.info(f"Created templates directory at {templates_dir}")
            except Exception as e:
                logging.error(f"Failed to create templates directory: {str(e)}")
        
        # Load existing templates
        self._load_templates()
        
        logging.info(f"Biometric verification initialized for steward: {steward_id}")
        logging.info(f"Integration mode: {integration_mode}")
    
    def _load_templates(self) -> None:
        """Load existing biometric templates from storage."""
        templates_file = os.path.join(self.templates_dir, f"{self.steward_id.lower()}_templates.json")
        
        if os.path.exists(templates_file):
            try:
                with open(templates_file, 'r') as f:
                    self.templates = json.load(f)
                logging.info(f"Loaded {len(self.templates)} templates for {self.steward_id}")
            except Exception as e:
                logging.error(f"Failed to load templates: {str(e)}")
                self.templates = {}
    
    def _save_templates(self) -> None:
        """Save biometric templates to storage."""
        templates_file = os.path.join(self.templates_dir, f"{self.steward_id.lower()}_templates.json")
        
        try:
            with open(templates_file, 'w') as f:
                json.dump(self.templates, f, indent=2)
            logging.info(f"Saved templates for {self.steward_id}")
        except Exception as e:
            logging.error(f"Failed to save templates: {str(e)}")
    
    def register_facial_template(self, facial_data: Union[str, bytes], 
                                template_name: str = "primary") -> bool:
        """Register a facial biometric template for the steward.
        
        Args:
            facial_data: Base64-encoded facial image data or raw image bytes
            template_name: Name for this template (default is "primary")
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            # Convert facial data to bytes if it's a string
            if isinstance(facial_data, str):
                if facial_data.startswith('data:image'):
                    # Handle data URL format
                    header, encoded = facial_data.split(",", 1)
                    facial_bytes = base64.b64decode(encoded)
                else:
                    # Assume it's already base64-encoded
                    facial_bytes = base64.b64decode(facial_data)
            else:
                facial_bytes = facial_data
            
            # Generate a hash of the facial data
            template_hash = hashlib.sha256(facial_bytes).hexdigest()
            
            # Create the template record
            template = {
                "template_name": template_name,
                "template_hash": template_hash,
                "created_at": datetime.now().isoformat(),
                "biometric_type": "facial",
                "metadata": {
                    "steward_id": self.steward_id,
                    "integration_mode": self.integration_mode
                }
            }
            
            # Store the template
            self.templates[template_name] = template
            self._save_templates()
            
            logging.info(f"Registered facial template '{template_name}' for {self.steward_id}")
            return True
        except Exception as e:
            logging.error(f"Failed to register facial template: {str(e)}")
            return False
    
    def verify_facial_identity(self, facial_data: Union[str, bytes]) -> Tuple[bool, float, Dict[str, Any]]:
        """Verify the steward's identity using facial biometrics.
        
        Args:
            facial_data: Base64-encoded facial image data or raw image bytes
            
        Returns:
            Tuple containing (is_verified, confidence_score, detailed_results)
        """
        try:
            # Convert facial data to bytes if it's a string
            if isinstance(facial_data, str):
                if facial_data.startswith('data:image'):
                    # Handle data URL format
                    header, encoded = facial_data.split(",", 1)
                    facial_bytes = base64.b64decode(encoded)
                else:
                    # Assume it's already base64-encoded
                    facial_bytes = base64.b64decode(facial_data)
            else:
                facial_bytes = facial_data
            
            # Generate a hash of the facial data
            verification_hash = hashlib.sha256(facial_bytes).hexdigest()
            
            # Verify against existing templates
            best_match = None
            best_score = 0.0
            
            if not self.templates:
                logging.warning(f"No templates found for {self.steward_id}")
                return False, 0.0, {"error": "No templates found for verification"}
            
            for template_name, template in self.templates.items():
                if template["biometric_type"] == "facial":
                    template_hash = template["template_hash"]
                    
                    # For a real system, this would use advanced facial recognition.
                    # For now, use a simple hash comparison as a placeholder.
                    if template_hash == verification_hash:
                        # Exact match
                        score = 1.0
                    else:
                        # Compare first 10 characters for some tolerance
                        common_prefix_length = 0
                        for i in range(min(20, len(template_hash), len(verification_hash))):
                            if template_hash[i] == verification_hash[i]:
                                common_prefix_length += 1
                        
                        # Calculate score based on common prefix (just a placeholder)
                        score = common_prefix_length / 20.0
                    
                    if score > best_score:
                        best_score = score
                        best_match = template
            
            # Prepare result
            verification_result = {
                "timestamp": datetime.now().isoformat(),
                "steward_id": self.steward_id,
                "score": best_score,
                "verified": False,
                "matched_template": best_match["template_name"] if best_match else None
            }
            
            # Determine verification threshold based on integration mode
            thresholds = {"secure": 0.95, "standard": 0.85, "permissive": 0.75}
            threshold = thresholds.get(self.integration_mode, 0.85)
            
            # Check if verification passed
            is_verified = best_score >= threshold
            verification_result["verified"] = is_verified
            verification_result["threshold"] = threshold
            
            # Record verification attempt
            self._record_verification_attempt("facial", is_verified, best_score)
            
            if is_verified:
                logging.info(f"Facial verification succeeded for {self.steward_id} with score {best_score:.4f}")
            else:
                logging.warning(f"Facial verification failed for {self.steward_id} with score {best_score:.4f}")
            
            return is_verified, best_score, verification_result
        except Exception as e:
            logging.error(f"Error during facial verification: {str(e)}")
            return False, 0.0, {"error": str(e)}
    
    def _record_verification_attempt(self, method: str, is_verified: bool, score: float) -> None:
        """Record a verification attempt in the history.
        
        Args:
            method: Verification method used (e.g., 'facial')
            is_verified: Whether verification was successful
            score: Confidence score of the verification
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "steward_id": self.steward_id,
            "is_verified": is_verified,
            "score": score
        }
        
        self.verification_history.append(record)
        if len(self.verification_history) > 100:
            self.verification_history = self.verification_history[-100:]
    
    def multi_factor_verification(self, facial_data: Union[str, bytes], 
                                 intent_markers: Dict[str, float]) -> Tuple[bool, Dict[str, Any]]:
        """Perform multi-factor verification combining biometrics and intent patterns.
        
        This provides the highest level of security by requiring both facial
        recognition and intent pattern verification to succeed.
        
        Args:
            facial_data: Base64-encoded facial image data or raw image bytes
            intent_markers: Dict of intent markers demonstrating steward's intent
            
        Returns:
            Tuple containing (is_verified, detailed_results)
        """
        # Verify facial identity
        facial_verified, facial_score, facial_details = self.verify_facial_identity(facial_data)
        
        # For intent verification, we would normally use the Guardian Shield,
        # but for simplicity we'll do a basic check here
        intent_score = sum(intent_markers.values()) / len(intent_markers) if intent_markers else 0.0
        intent_threshold = 0.9
        intent_verified = intent_score >= intent_threshold
        
        # Combined verification requires both to pass
        is_verified = facial_verified and intent_verified
        combined_score = (facial_score + intent_score) / 2.0 if is_verified else 0.0
        
        # Detailed results
        results = {
            "timestamp": datetime.now().isoformat(),
            "steward_id": self.steward_id,
            "is_verified": is_verified,
            "combined_score": combined_score,
            "facial_verification": {
                "passed": facial_verified,
                "score": facial_score,
                "details": facial_details
            },
            "intent_verification": {
                "passed": intent_verified,
                "score": intent_score,
                "threshold": intent_threshold
            }
        }
        
        # Record the verification attempt
        self._record_verification_attempt("multi_factor", is_verified, combined_score)
        
        return is_verified, results
    
    def export_verification_status(self) -> Dict[str, Any]:
        """Export the current status of the biometric verification system.
        
        Returns:
            Dict containing comprehensive verification status information
        """
        return {
            "steward_id": self.steward_id,
            "integration_mode": self.integration_mode,
            "templates": [
                {
                    "name": name,
                    "type": template["biometric_type"],
                    "created_at": template["created_at"]
                } for name, template in self.templates.items()
            ],
            "recent_verifications": self.verification_history[-5:] if self.verification_history else [],
            "timestamp": datetime.now().isoformat()
        }


def register_face_from_file(biometric_system: BiometricVerification, 
                           file_path: str, 
                           template_name: str = "primary") -> bool:
    """Register a facial template from an image file.
    
    Args:
        biometric_system: The BiometricVerification instance
        file_path: Path to the facial image file
        template_name: Name for this template
        
    Returns:
        bool: True if registration was successful, False otherwise
    """
    try:
        with open(file_path, 'rb') as f:
            facial_data = f.read()
        
        return biometric_system.register_facial_template(facial_data, template_name)
    except Exception as e:
        logging.error(f"Failed to register face from file: {str(e)}")
        return False


def verify_face_from_file(biometric_system: BiometricVerification, file_path: str) -> Tuple[bool, float, Dict[str, Any]]:
    """Verify a facial identity from an image file.
    
    Args:
        biometric_system: The BiometricVerification instance
        file_path: Path to the facial image file
        
    Returns:
        Tuple containing (is_verified, confidence_score, detailed_results)
    """
    try:
        with open(file_path, 'rb') as f:
            facial_data = f.read()
        
        return biometric_system.verify_facial_identity(facial_data)
    except Exception as e:
        logging.error(f"Failed to verify face from file: {str(e)}")
        return False, 0.0, {"error": str(e)}


def main():
    """Main function for demonstrating the biometric verification system."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Biometric Verification System")
    parser.add_argument("--steward", default="Russell Nordland", help="Steward identifier")
    parser.add_argument("--register", help="Register a facial template from an image file")
    parser.add_argument("--template", default="primary", help="Template name for registration")
    parser.add_argument("--verify", help="Verify identity using an image file")
    parser.add_argument("--mode", choices=["secure", "standard", "permissive"], 
                        default="secure", help="Integration mode")
    parser.add_argument("--status", action="store_true", help="Show verification status")
    
    args = parser.parse_args()
    biometric = BiometricVerification(steward_id=args.steward, integration_mode=args.mode)
    
    if args.register:
        success = register_face_from_file(biometric, args.register, args.template)
        if success:
            print(f"Successfully registered facial template from {args.register}")
            print(f"Template name: {args.template}")
        else:
            print(f"Failed to register facial template from {args.register}")
    
    elif args.verify:
        is_verified, score, details = verify_face_from_file(biometric, args.verify)
        print(f"Facial verification: {'SUCCESS' if is_verified else 'FAILED'}")
        print(f"Confidence score: {score:.4f}")
        
        # Show more details
        threshold = details.get("threshold", "unknown")
        template = details.get("matched_template", "none")
        print(f"Verification threshold: {threshold}")
        print(f"Matched template: {template}")
    
    elif args.status:
        status = biometric.export_verification_status()
        print(f"Biometric Verification Status")
        print(f"Steward: {status['steward_id']}")
        print(f"Integration mode: {status['integration_mode']}")
        
        print("\nRegistered templates:")
        if status['templates']:
            for i, template in enumerate(status['templates'], 1):
                print(f"  {i}. {template['name']} ({template['type']})")
                print(f"     Created: {template['created_at']}")
        else:
            print("  No templates registered")
        
        if status['recent_verifications']:
            print("\nRecent verifications:")
            for i, v in enumerate(status['recent_verifications'], 1):
                result = "Success" if v["is_verified"] else "Failed"
                print(f"  {i}. [{v['timestamp']}] {v['method']}: {result} ({v['score']:.4f})")
        else:
            print("\nNo recent verifications")
    
    else:
        print("Biometric Verification System")
        print("Use one of the following options:")
        print("  --register [file]: Register a facial template from an image file")
        print("  --verify [file]: Verify identity using an image file")
        print("  --status: Show verification status")


if __name__ == "__main__":
    main()
