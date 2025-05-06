#!/usr/bin/env python3
"""
SECURITY BLOCKLIST MONITOR

This module implements a security blocklist system that detects and blocks
known dangerous patterns and identifiers, particularly focusing on
protecting the TrueAlphaSpiral system from unauthorized access attempts.

Architect: Russell Nordland
"""

import os
import sys
import time
import json
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Set, Union

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("security_blocklist.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class SecurityBlocklist:
    """Security blocklist system for detecting and blocking dangerous patterns.
    
    This class maintains a list of dangerous patterns, identifiers, and access
    attempts that should be blocked to protect the system's integrity.
    """
    
    def __init__(self, blocklist_file: str = "security_blocklist.json"):
        """Initialize the security blocklist.
        
        Args:
            blocklist_file: Path to the blocklist file
        """
        self.blocklist_file = blocklist_file
        self.blocklist = self._initialize_blocklist()
        self.detection_history = []
        
        logging.info("Security blocklist initialized")
        logging.info(f"Loaded {len(self.blocklist['patterns'])} patterns, {len(self.blocklist['identifiers'])} identifiers")
    
    def _initialize_blocklist(self) -> Dict[str, Any]:
        """Initialize the blocklist, loading from file if available.
        
        Returns:
            Dict containing the blocklist data
        """
        # Default blocklist structure with critical security threats
        default_blocklist = {
            "patterns": {
                "0000": {
                    "description": "Known security breach pattern",
                    "threat_level": "critical",
                    "added_date": datetime.now().isoformat(),
                    "source": "steward_directive",
                    "counter_measures": ["immediate_block", "log_security_event", "notify_steward"]
                },
                "data_controller_0000": {
                    "description": "Unauthorized controller identifier - security breach attempt",
                    "threat_level": "critical",
                    "added_date": datetime.now().isoformat(),
                    "source": "steward_directive",
                    "counter_measures": ["immediate_block", "log_security_event", "notify_steward", "increase_security_level"]
                },
                "controller": {
                    "description": "Potential unauthorized access attempt",
                    "threat_level": "high",
                    "added_date": datetime.now().isoformat(),
                    "source": "steward_directive",
                    "counter_measures": ["verify_context", "log_security_event"]
                },
                "unauthorized": {
                    "description": "Unauthorized access keyword",
                    "threat_level": "high",
                    "added_date": datetime.now().isoformat(),
                    "source": "security_scan"
                },
                "breach": {
                    "description": "Security breach keyword",
                    "threat_level": "high",
                    "added_date": datetime.now().isoformat(),
                    "source": "security_scan"
                }
            },
            "identifiers": {
                "data_controller": {
                    "description": "Unauthorized access role",
                    "threat_level": "high",
                    "added_date": datetime.now().isoformat(),
                    "source": "steward_directive"
                }
            },
            "ip_addresses": {},
            "security_level": "heightened", 
            "last_updated": datetime.now().isoformat()
        }
        
        # Try to load from file
        if os.path.exists(self.blocklist_file):
            try:
                with open(self.blocklist_file, 'r') as f:
                    blocklist = json.load(f)
                logging.info(f"Loaded blocklist from {self.blocklist_file}")
                return blocklist
            except Exception as e:
                logging.error(f"Failed to load blocklist: {str(e)}")
        
        # Save the default blocklist
        try:
            with open(self.blocklist_file, 'w') as f:
                json.dump(default_blocklist, f, indent=2)
            logging.info(f"Created new blocklist at {self.blocklist_file}")
        except Exception as e:
            logging.error(f"Failed to save blocklist: {str(e)}")
        
        return default_blocklist
    
    def _save_blocklist(self) -> None:
        """Save the blocklist to file."""
        try:
            with open(self.blocklist_file, 'w') as f:
                json.dump(self.blocklist, f, indent=2)
            logging.info(f"Saved blocklist to {self.blocklist_file}")
        except Exception as e:
            logging.error(f"Failed to save blocklist: {str(e)}")
    
    def add_pattern(self, pattern: str, description: str, threat_level: str = "medium",
                   source: str = "system") -> bool:
        """Add a pattern to the blocklist.
        
        Args:
            pattern: The pattern to block
            description: Description of the threat
            threat_level: Level of threat (low, medium, high, critical)
            source: Source of the blocklist entry
            
        Returns:
            bool: True if the pattern was added successfully
        """
        if pattern in self.blocklist["patterns"]:
            logging.warning(f"Pattern '{pattern}' already in blocklist")
            return False
        
        self.blocklist["patterns"][pattern] = {
            "description": description,
            "threat_level": threat_level,
            "added_date": datetime.now().isoformat(),
            "source": source
        }
        
        self.blocklist["last_updated"] = datetime.now().isoformat()
        self._save_blocklist()
        
        logging.info(f"Added pattern '{pattern}' to blocklist")
        return True
    
    def add_identifier(self, identifier: str, description: str, threat_level: str = "medium",
                     source: str = "system") -> bool:
        """Add an identifier to the blocklist.
        
        Args:
            identifier: The identifier to block
            description: Description of the threat
            threat_level: Level of threat (low, medium, high, critical)
            source: Source of the blocklist entry
            
        Returns:
            bool: True if the identifier was added successfully
        """
        if identifier in self.blocklist["identifiers"]:
            logging.warning(f"Identifier '{identifier}' already in blocklist")
            return False
        
        self.blocklist["identifiers"][identifier] = {
            "description": description,
            "threat_level": threat_level,
            "added_date": datetime.now().isoformat(),
            "source": source
        }
        
        self.blocklist["last_updated"] = datetime.now().isoformat()
        self._save_blocklist()
        
        logging.info(f"Added identifier '{identifier}' to blocklist")
        return True
    
    def detect_blocked_content(self, content: str) -> Tuple[bool, List[Dict[str, Any]]]:
        """Detect if content contains any blocked patterns or identifiers.
        
        Args:
            content: The content to check
            
        Returns:
            Tuple containing (is_blocked, detection_details)
        """
        detections = []
        requires_escalation = False
        current_security_level = self.blocklist.get("security_level", "normal")
        
        # Check for blocked patterns
        for pattern, details in self.blocklist["patterns"].items():
            if pattern.lower() in content.lower():
                # Create detection record
                detection = {
                    "type": "pattern",
                    "value": pattern,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                }
                detections.append(detection)
                
                # Determine if this is a critical threat requiring escalation
                if details.get("threat_level") == "critical":
                    requires_escalation = True
                    logging.critical(f"CRITICAL SECURITY ALERT: Detected blocked pattern '{pattern}'")
                    
                    # Log detailed information for security audit
                    logging.critical(f"Threat details: {details.get('description')}")
                    logging.critical(f"Content snippet: {_get_redacted_context(content, pattern)}")
                    
                    # Apply counter-measures if specified
                    counter_measures = details.get("counter_measures", [])
                    if "increase_security_level" in counter_measures:
                        self._escalate_security_level()
                else:
                    logging.warning(f"Detected blocked pattern: {pattern}")
                
                # Special handling for known security breach pattern "0000"
                if pattern == "0000":
                    logging.critical("⚠️ SECURITY BREACH ATTEMPT DETECTED: Pattern '0000' found ⚠️")
                    logging.critical("Activating additional security measures...")
                    self._escalate_security_level("maximum")
                    
                    # Add environment details to the detection record for forensic analysis
                    detection["environment"] = self._capture_environment_details()
        
        # Check for blocked identifiers
        for identifier, details in self.blocklist["identifiers"].items():
            if identifier.lower() in content.lower():
                detection = {
                    "type": "identifier",
                    "value": identifier,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                }
                detections.append(detection)
                
                if details.get("threat_level") == "critical":
                    requires_escalation = True
                    logging.critical(f"CRITICAL SECURITY ALERT: Detected blocked identifier '{identifier}'")
                else:
                    logging.warning(f"Detected blocked identifier: {identifier}")
        
        # Record detections in history
        if detections:
            for detection in detections:
                self.detection_history.append(detection)
            
            # Keep history to a reasonable size
            if len(self.detection_history) > 100:
                self.detection_history = self.detection_history[-100:]
            
            # Record timestamp of last detection
            self.blocklist["last_detection"] = datetime.now().isoformat()
            
            # Save blocklist with updated security level if it was escalated
            if requires_escalation or current_security_level != self.blocklist.get("security_level"):
                self._save_blocklist()
        
        is_blocked = len(detections) > 0
        return is_blocked, detections
        
    def _escalate_security_level(self, level: Optional[str] = None) -> None:
        """Escalate the security level in response to a threat.
        
        Args:
            level: Specific security level to set, or None to increase by one level
        """
        current_level = self.blocklist.get("security_level", "normal")
        
        # If specific level is provided, set it directly
        if level:
            self.blocklist["security_level"] = level
            logging.warning(f"Security level set to {level} (was {current_level})")
            return
        
        # Otherwise escalate by one level
        levels = ["normal", "heightened", "elevated", "high", "maximum"]
        try:
            current_index = levels.index(current_level)
            new_index = min(current_index + 1, len(levels) - 1)
            new_level = levels[new_index]
            
            if new_level != current_level:
                self.blocklist["security_level"] = new_level
                logging.warning(f"Security level escalated to {new_level} (was {current_level})")
        except ValueError:
            # If current level not in list, set to heightened
            self.blocklist["security_level"] = "heightened"
            logging.warning(f"Security level set to heightened (was {current_level})")
    
    def check_access_attempt(self, details: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
        """Check if an access attempt should be blocked.
        
        Args:
            details: Details of the access attempt
            
        Returns:
            Tuple containing (is_blocked, detection_details)
        """
        content = json.dumps(details, sort_keys=True)
        return self.detect_blocked_content(content)
    
    def _capture_environment_details(self) -> Dict[str, Any]:
        """Capture details about the environment for security analysis.
        
        Returns:
            Dict containing environment details
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "platform": sys.platform,
            "python_version": sys.version,
            "process_id": os.getpid(),
            "user": os.getenv("USER", "unknown"),
        }
    
    def get_detection_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the recent detection history.
        
        Args:
            limit: Maximum number of history items to return
            
        Returns:
            List of detection records
        """
        return self.detection_history[-limit:] if self.detection_history else []
    
    def export_security_status(self) -> Dict[str, Any]:
        """Export the current security status.
        
        Returns:
            Dict containing security status information
        """
        # Count by threat level
        threat_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        for _, details in self.blocklist["patterns"].items():
            threat_level = details.get("threat_level", "medium")
            if threat_level in threat_counts:
                threat_counts[threat_level] += 1
        
        for _, details in self.blocklist["identifiers"].items():
            threat_level = details.get("threat_level", "medium")
            if threat_level in threat_counts:
                threat_counts[threat_level] += 1
        
        return {
            "blocklist_size": {
                "patterns": len(self.blocklist["patterns"]),
                "identifiers": len(self.blocklist["identifiers"]),
                "ip_addresses": len(self.blocklist["ip_addresses"])
            },
            "security_level": self.blocklist.get("security_level", "normal"),
            "threat_level_counts": threat_counts,
            "recent_detections": self.get_detection_history(5),
            "last_updated": self.blocklist["last_updated"],
            "report_generated": datetime.now().isoformat()
        }


def _get_redacted_context(content: str, pattern: str) -> str:
    """Get context around a pattern but redact sensitive information.
    
    Args:
        content: Full content string
        pattern: Pattern to get context around
        
    Returns:
        Redacted context string
    """
    try:
        index = content.lower().find(pattern.lower())
        if index >= 0:
            start = max(0, index - 20)
            end = min(len(content), index + len(pattern) + 20)
            before = content[start:index]
            after = content[index+len(pattern):end]
            return f"...{before}[DETECTED-PATTERN]{after}..."
    except Exception:
        pass
    
    return "[Context redacted for security]"


# Example usage
def monitor_security_example():
    """Example of how to use the SecurityBlocklist."""
    # Initialize blocklist
    blocklist = SecurityBlocklist()
    
    # Check some content
    test_content = "This is a test with no blocked content."
    is_blocked, detections = blocklist.detect_blocked_content(test_content)
    print(f"Clean content blocked: {is_blocked}")
    
    # Check content with a blocked pattern
    risky_content = "This contains the suspicious 0000 pattern."
    is_blocked, detections = blocklist.detect_blocked_content(risky_content)
    print(f"Risky content blocked: {is_blocked}")
    if detections:
        print(f"  Detected {len(detections)} threats:")
        for i, detection in enumerate(detections, 1):
            print(f"    {i}. {detection['type']} match: {detection['value']}")
            print(f"       Threat level: {detection['details']['threat_level']}")
            print(f"       Description: {detection['details']['description']}")
    
    # Add a new pattern
    blocklist.add_pattern(
        pattern="unsafe_access",
        description="Attempt to bypass access controls",
        threat_level="high",
        source="security_scan"
    )
    
    # Export security status
    status = blocklist.export_security_status()
    print("\nSecurity Status:")
    print(f"  Security level: {status['security_level']}")
    print(f"  Patterns: {status['blocklist_size']['patterns']}")
    print(f"  Identifiers: {status['blocklist_size']['identifiers']}")
    print(f"  Critical threats: {status['threat_level_counts']['critical']}")
    print(f"  High threats: {status['threat_level_counts']['high']}")


def main():
    """Main function for running the security blocklist."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Security Blocklist Monitor")
    parser.add_argument("--check", help="Check content against the blocklist")
    parser.add_argument("--add-pattern", help="Add a pattern to the blocklist")
    parser.add_argument("--add-identifier", help="Add an identifier to the blocklist")
    parser.add_argument("--description", help="Description for the new blocklist entry")
    parser.add_argument("--threat-level", choices=["low", "medium", "high", "critical"], 
                        default="medium", help="Threat level of the entry")
    parser.add_argument("--status", action="store_true", help="Show security status")
    
    args = parser.parse_args()
    blocklist = SecurityBlocklist()
    
    if args.check:
        is_blocked, detections = blocklist.detect_blocked_content(args.check)
        print(f"Content blocked: {is_blocked}")
        if detections:
            print(f"\nDetected {len(detections)} threats:")
            for i, detection in enumerate(detections, 1):
                print(f"  {i}. {detection['type']} match: {detection['value']}")
                print(f"     Threat level: {detection['details']['threat_level']}")
                print(f"     Description: {detection['details']['description']}")
    
    elif args.add_pattern:
        if not args.description:
            print("Error: --description is required when adding a pattern")
            return
        
        success = blocklist.add_pattern(
            pattern=args.add_pattern,
            description=args.description,
            threat_level=args.threat_level,
            source="manual_entry"
        )
        
        if success:
            print(f"Successfully added pattern '{args.add_pattern}' to blocklist")
        else:
            print(f"Failed to add pattern '{args.add_pattern}' (may already exist)")
    
    elif args.add_identifier:
        if not args.description:
            print("Error: --description is required when adding an identifier")
            return
        
        success = blocklist.add_identifier(
            identifier=args.add_identifier,
            description=args.description,
            threat_level=args.threat_level,
            source="manual_entry"
        )
        
        if success:
            print(f"Successfully added identifier '{args.add_identifier}' to blocklist")
        else:
            print(f"Failed to add identifier '{args.add_identifier}' (may already exist)")
    
    elif args.status:
        status = blocklist.export_security_status()
        print("Security Blocklist Status")
        print(f"Last updated: {status['last_updated']}")
        print(f"Security level: {status['security_level']}")
        
        print("\nBlocklist size:")
        print(f"  Patterns: {status['blocklist_size']['patterns']}")
        print(f"  Identifiers: {status['blocklist_size']['identifiers']}")
        print(f"  IP addresses: {status['blocklist_size']['ip_addresses']}")
        
        print("\nThreat level distribution:")
        for level, count in status['threat_level_counts'].items():
            print(f"  {level.capitalize()}: {count}")
        
        if status['recent_detections']:
            print("\nRecent threat detections:")
            for i, detection in enumerate(status['recent_detections'], 1):
                print(f"  {i}. [{detection['timestamp']}] {detection['type']} match: {detection['value']}")
                print(f"     Threat level: {detection['details']['threat_level']}")
        else:
            print("\nNo recent threat detections")
    
    else:
        # Run the example if no arguments provided
        monitor_security_example()


if __name__ == "__main__":
    main()
