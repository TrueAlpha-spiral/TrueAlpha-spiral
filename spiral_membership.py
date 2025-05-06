"""  
SPIRAL MEMBERSHIP SYSTEM

This module implements the TrueAlphaSpiral membership system that allows
individuals to join the spiral in accordance with defined stewardship principles.
It follows the human-centric design with intention verification and ethical alignment.

Architect: Russell Nordland
"""

import uuid
import time
import json
import hashlib
import base64
from datetime import datetime
import os
import logging

# ANSI color codes for terminal output
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("spiral_membership.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SpiralMembership")

class SpiralMembership:
    """Implements the TrueAlphaSpiral membership system allowing individuals to join the spiral."""
    
    def __init__(self):
        """Initialize the Spiral Membership system."""
        self.members = {}
        self.pending_members = {}
        self.payment_records = {}
        self.alignment_thresholds = {
            "intent": 0.75,  # Minimum intent score required
            "ethical": 0.80,  # Minimum ethical alignment score
            "resonance": 0.70,  # Minimum resonance with core principles
            "sovereignty": 0.85  # Minimum sovereignty respect score
        }
        self.payment_tiers = {
            "basic": {
                "name": "Basic Access",
                "amount": 15.00,
                "description": "Basic access to join the spiral",
                "currency": "USD"
            },
            "contributor": {
                "name": "Contributor Access",
                "amount": 45.00,
                "description": "Enhanced access with contributor privileges",
                "currency": "USD"
            },
            "guardian": {
                "name": "Guardian Access",
                "amount": 99.00,
                "description": "Premium access with guardian capabilities",
                "currency": "USD"
            }
        }
        self.membership_levels = {
            "observer": {
                "name": "Observer",
                "description": "Initial level that allows viewing public spiral information",
                "access_level": 1,
                "requirements": {
                    "intent": 0.60,
                    "ethical": 0.70,
                    "time_in_system": 0  # Days
                }
            },
            "contributor": {
                "name": "Contributor",
                "description": "Can contribute data and feedback to the spiral",
                "access_level": 2,
                "requirements": {
                    "intent": 0.75,
                    "ethical": 0.80,
                    "time_in_system": 7  # Days
                }
            },
            "resonator": {
                "name": "Resonator",
                "description": "Can participate in collective resonance activities",
                "access_level": 3,
                "requirements": {
                    "intent": 0.85,
                    "ethical": 0.85,
                    "time_in_system": 30  # Days
                }
            },
            "guardian": {
                "name": "Guardian",
                "description": "Helps protect the integrity of the spiral",
                "access_level": 4,
                "requirements": {
                    "intent": 0.90,
                    "ethical": 0.90,
                    "time_in_system": 90  # Days
                }
            }
        }
        self.steward_id = None  # Will be set during initialization
        self.membership_storage_path = "membership_data.json"
        self.initialized = False
        
        logger.info("Spiral Membership system created")
    
    def initialize(self, steward_id=None, steward_name="Russell Nordland"):
        """Initialize the membership system with the steward."""
        self.steward_id = steward_id or str(uuid.uuid4())
        self.steward_name = steward_name
        
        # Create the steward record
        steward_record = {
            "id": self.steward_id,
            "name": steward_name,
            "role": "steward",
            "level": "founder",
            "join_date": datetime.now().isoformat(),
            "auth_hash": self._generate_auth_hash(self.steward_id),
            "intent_score": 1.0,
            "ethical_score": 1.0,
            "resonance_score": 1.0,
            "sovereignty_score": 1.0,
            "activities": [],
            "approved_by": "origin"
        }
        
        # Store the steward record
        self.members[self.steward_id] = steward_record
        
        # Load any existing membership data
        self._load_membership_data()
        
        self.initialized = True
        logger.info(f"Spiral Membership system initialized with steward: {steward_name}")
        return True
    
    def request_membership(self, applicant_data):
        """Process a request to join the TrueAlphaSpiral."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Validate required fields
        required_fields = ["name", "email", "intent_statement"]
        for field in required_fields:
            if field not in applicant_data:
                return {"success": False, "error": f"Missing required field: {field}"}
        
        # Generate a unique applicant ID
        applicant_id = str(uuid.uuid4())
        
        # Analyze the applicant's intent
        intent_analysis = self._analyze_intent(applicant_data.get("intent_statement", ""))
        
        # Create a pending member record
        pending_record = {
            "id": applicant_id,
            "name": applicant_data.get("name"),
            "email": applicant_data.get("email"),
            "request_date": datetime.now().isoformat(),
            "intent_statement": applicant_data.get("intent_statement"),
            "intent_score": intent_analysis.get("intent_score", 0),
            "ethical_score": intent_analysis.get("ethical_score", 0),
            "resonance_score": intent_analysis.get("resonance_score", 0),
            "sovereignty_score": intent_analysis.get("sovereignty_score", 0),
            "verification_code": self._generate_verification_code(),
            "status": "pending",
            "level": "observer",  # Default starting level
            "notes": intent_analysis.get("notes", [])
        }
        
        # Check if the applicant meets the threshold requirements
        meets_threshold = self._check_threshold_requirements(pending_record)
        if meets_threshold:
            pending_record["status"] = "verification_needed"
        else:
            pending_record["status"] = "review_needed"
            pending_record["notes"].append("Application requires steward review due to below-threshold scores")
        
        # Store the pending application
        self.pending_members[applicant_id] = pending_record
        
        # Save updated membership data
        self._save_membership_data()
        
        # Prepare the response
        response = {
            "success": True,
            "applicant_id": applicant_id,
            "verification_needed": pending_record["status"] == "verification_needed",
            "status": pending_record["status"],
            "message": "Your membership request has been received and is being processed.",
            "payment_required": True,
            "payment_tiers": self.payment_tiers
        }
        
        if pending_record["status"] == "verification_needed":
            response["verification_code"] = pending_record["verification_code"]
            response["message"] = "Please complete verification and payment to confirm your request."
        
        logger.info(f"New membership request from {applicant_data.get('name')} with ID {applicant_id}")
        return response
    
    def verify_applicant(self, applicant_id, verification_code):
        """Verify an applicant using their verification code."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Check if the applicant exists
        if applicant_id not in self.pending_members:
            return {"success": False, "error": "Applicant not found"}
        
        pending_record = self.pending_members[applicant_id]
        
        # Check if verification is needed
        if pending_record["status"] != "verification_needed":
            return {"success": False, "error": "Verification not required for this application"}
        
        # Verify the code
        if pending_record["verification_code"] != verification_code:
            return {"success": False, "error": "Invalid verification code"}
        
        # Update the application status
        pending_record["status"] = "verified"
        pending_record["verification_date"] = datetime.now().isoformat()
        
        # Save updated membership data
        self._save_membership_data()
        
        logger.info(f"Applicant {applicant_id} verified successfully")
        return {
            "success": True,
            "message": "Verification successful. Your membership request will be reviewed by the steward."
        }
    
    def approve_applicant(self, applicant_id, approved_by, level="observer", notes=None):
        """Approve an applicant for membership."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Check if the applicant exists
        if applicant_id not in self.pending_members:
            return {"success": False, "error": "Applicant not found"}
        
        pending_record = self.pending_members[applicant_id]
        
        # Check if the application is ready for approval
        valid_statuses = ["verified", "review_needed", "ready_for_approval"]
        if pending_record["status"] not in valid_statuses:
            return {
                "success": False, 
                "error": f"Application cannot be approved at this time. Current status: {pending_record['status']}"
            }
        
        # Check if payment has been received
        has_paid = "payment_status" in pending_record and pending_record["payment_status"] == "paid"
        # Allow the steward to override payment requirement (this will be checked in the API layer)
        override_payment = False
        
        if not has_paid and not override_payment and approved_by != "Russell Nordland":
            return {
                "success": False,
                "error": "Payment is required before approval. Use override_payment=true to bypass (steward only)."
            }
        
        # Validate the level
        if level not in self.membership_levels:
            return {"success": False, "error": f"Invalid membership level: {level}"}
        
        # Create a member record from the pending application
        member_record = {
            "id": applicant_id,
            "name": pending_record["name"],
            "email": pending_record["email"],
            "role": "member",
            "level": level,
            "join_date": datetime.now().isoformat(),
            "request_date": pending_record["request_date"],
            "auth_hash": self._generate_auth_hash(applicant_id),
            "intent_score": pending_record["intent_score"],
            "ethical_score": pending_record["ethical_score"],
            "resonance_score": pending_record["resonance_score"],
            "sovereignty_score": pending_record["sovereignty_score"],
            "activities": [],
            "approved_by": approved_by,
            "notes": pending_record.get("notes", [])
        }
        
        # Add approval notes
        if notes:
            member_record["notes"].append(f"Approval note: {notes}")
        
        # Add the new member
        self.members[applicant_id] = member_record
        
        # Remove from pending applications
        del self.pending_members[applicant_id]
        
        # Save updated membership data
        self._save_membership_data()
        
        logger.info(f"Applicant {applicant_id} approved as {level} by {approved_by}")
        return {
            "success": True,
            "member_id": applicant_id,
            "level": level,
            "message": f"Applicant has been approved as a {self.membership_levels[level]['name']}"
        }
    
    def reject_applicant(self, applicant_id, rejected_by, reason=None):
        """Reject an applicant for membership."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Check if the applicant exists
        if applicant_id not in self.pending_members:
            return {"success": False, "error": "Applicant not found"}
        
        # Record the rejection
        pending_record = self.pending_members[applicant_id]
        pending_record["status"] = "rejected"
        pending_record["rejection_date"] = datetime.now().isoformat()
        pending_record["rejected_by"] = rejected_by
        if reason:
            pending_record["rejection_reason"] = reason
        
        # Save updated membership data
        self._save_membership_data()
        
        logger.info(f"Applicant {applicant_id} rejected by {rejected_by}")
        return {
            "success": True,
            "message": "Applicant has been rejected"
        }
    
    def get_member(self, member_id):
        """Get a member's information."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return None
        
        return self.members.get(member_id)
    
    def get_all_members(self, include_sensitive=False):
        """Get all members (optionally filtering sensitive information)."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return []
        
        if include_sensitive:
            return list(self.members.values())
        
        # Filter out sensitive information
        filtered_members = []
        for member in self.members.values():
            filtered_member = {
                "id": member["id"],
                "name": member["name"],
                "role": member["role"],
                "level": member["level"],
                "join_date": member["join_date"]
            }
            filtered_members.append(filtered_member)
        
        return filtered_members
    
    def get_pending_applications(self):
        """Get all pending membership applications."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return []
        
        return list(self.pending_members.values())
    
    def authenticate_member(self, member_id, auth_hash):
        """Authenticate a member using their auth hash."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return False
        
        member = self.members.get(member_id)
        if not member:
            return False
        
        return member["auth_hash"] == auth_hash
    
    def record_member_activity(self, member_id, activity_type, details=None):
        """Record an activity performed by a member."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return False
        
        member = self.members.get(member_id)
        if not member:
            return False
        
        # Create activity record
        activity = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "details": details or {}
        }
        
        # Add to member's activities
        member["activities"].append(activity)
        
        # Save updated membership data
        self._save_membership_data()
        
        return True
    
    def update_member_level(self, member_id, new_level, updated_by, reason=None):
        """Update a member's level."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Validate level
        if new_level not in self.membership_levels:
            return {"success": False, "error": f"Invalid level: {new_level}"}
        
        # Check if member exists
        member = self.members.get(member_id)
        if not member:
            return {"success": False, "error": "Member not found"}
        
        # Record the change
        old_level = member["level"]
        member["level"] = new_level
        
        # Record the activity
        activity = {
            "timestamp": datetime.now().isoformat(),
            "type": "level_change",
            "details": {
                "old_level": old_level,
                "new_level": new_level,
                "updated_by": updated_by,
                "reason": reason
            }
        }
        member["activities"].append(activity)
        
        # Save updated membership data
        self._save_membership_data()
        
        logger.info(f"Member {member_id} level updated from {old_level} to {new_level} by {updated_by}")
        return {
            "success": True,
            "message": f"Member level updated from {old_level} to {new_level}"
        }
    
    def _analyze_intent(self, intent_statement):
        """Analyze an applicant's intent statement.
        
        In a full implementation, this would use sophisticated analysis,
        possibly connected to the TrueAlphaSpiral ethical analysis system.
        
        This simplified version uses basic metrics for demonstration.
        """
        # Basic checks for demonstration
        intent_score = 0.70  # Base score
        ethical_score = 0.75
        resonance_score = 0.70
        sovereignty_score = 0.80
        notes = []
        
        # Check for minimum length
        if len(intent_statement) < 50:
            intent_score -= 0.20
            notes.append("Intent statement is too short for proper analysis")
        elif len(intent_statement) > 500:
            intent_score += 0.05
            notes.append("Detailed intent statement provided")
        
        # Check for key phrase presence
        key_phrases = [
            "ethical", "alignment", "truth", "collaboration", "sovereign", 
            "spiral", "recursive", "integrity", "steward", "TrueAlphaSpiral"
        ]
        
        lower_statement = intent_statement.lower()
        phrase_count = sum(1 for phrase in key_phrases if phrase.lower() in lower_statement)
        
        if phrase_count >= 5:
            resonance_score += 0.15
            notes.append("Strong resonance with TrueAlphaSpiral terminology")
        elif phrase_count >= 3:
            resonance_score += 0.05
            notes.append("Some resonance with TrueAlphaSpiral terminology")
        
        # Check for respect of sovereignty
        sovereignty_phrases = ["steward", "russell", "nordland", "sovereign", "author", "creator"]
        sov_count = sum(1 for phrase in sovereignty_phrases if phrase.lower() in lower_statement)
        
        if sov_count >= 2:
            sovereignty_score += 0.10
            notes.append("Acknowledges sovereignty concepts")
        
        # Note: In a full implementation, this would use proper NLP and the 
        # TrueAlphaSpiral ethical analysis system for a more detailed analysis
        
        return {
            "intent_score": min(1.0, intent_score),
            "ethical_score": min(1.0, ethical_score),
            "resonance_score": min(1.0, resonance_score),
            "sovereignty_score": min(1.0, sovereignty_score),
            "notes": notes
        }
    
    def _check_threshold_requirements(self, applicant_record):
        """Check if an applicant meets the threshold requirements."""
        intent_threshold = self.alignment_thresholds["intent"]
        ethical_threshold = self.alignment_thresholds["ethical"]
        resonance_threshold = self.alignment_thresholds["resonance"]
        sovereignty_threshold = self.alignment_thresholds["sovereignty"]
        
        return (
            applicant_record["intent_score"] >= intent_threshold and
            applicant_record["ethical_score"] >= ethical_threshold and
            applicant_record["resonance_score"] >= resonance_threshold and
            applicant_record["sovereignty_score"] >= sovereignty_threshold
        )
    
    def _generate_verification_code(self):
        """Generate a verification code for applicants."""
        # Create a random code for email verification
        random_bytes = os.urandom(16)
        return base64.b64encode(random_bytes).decode('utf-8')[:12]
    
    def _generate_auth_hash(self, user_id):
        """Generate an authentication hash for a user."""
        # In a production system, this would use better security practices
        timestamp = str(int(time.time()))
        random_component = os.urandom(8).hex()
        auth_string = f"{user_id}:{timestamp}:{random_component}:TrueAlphaSpiral"
        return hashlib.sha256(auth_string.encode()).hexdigest()
    
    def record_payment(self, applicant_id, payment_data):
        """Record a payment from an applicant."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Check if the applicant exists
        if applicant_id not in self.pending_members and applicant_id not in self.members:
            return {"success": False, "error": "Applicant or member not found"}
        
        # Validate payment data
        required_fields = ["payment_id", "amount", "currency", "payment_date", "tier"]
        for field in required_fields:
            if field not in payment_data:
                return {"success": False, "error": f"Missing payment field: {field}"}
        
        # Verify payment tier exists
        tier = payment_data.get("tier")
        if tier not in self.payment_tiers:
            return {"success": False, "error": f"Invalid payment tier: {tier}"}
        
        # Create payment record
        payment_record = {
            "id": payment_data.get("payment_id"),
            "applicant_id": applicant_id,
            "tier": tier,
            "amount": payment_data.get("amount"),
            "currency": payment_data.get("currency"),
            "payment_date": payment_data.get("payment_date"),
            "status": "completed",
            "payment_method": payment_data.get("payment_method", "unknown"),
            "notes": payment_data.get("notes", [])
        }
        
        # Store the payment record
        self.payment_records[payment_record["id"]] = payment_record
        
        # Update applicant status if pending
        if applicant_id in self.pending_members:
            pending_record = self.pending_members[applicant_id]
            pending_record["payment_status"] = "paid"
            pending_record["payment_id"] = payment_record["id"]
            pending_record["payment_tier"] = tier
            pending_record["notes"].append(f"Payment received: {payment_data.get('amount')} {payment_data.get('currency')} for {self.payment_tiers[tier]['name']}")
            
            # If already verified, mark as ready for approval
            if pending_record["status"] == "verified":
                pending_record["status"] = "ready_for_approval"
        
        # Update member status if already a member (renewal or upgrade)
        elif applicant_id in self.members:
            member_record = self.members[applicant_id]
            if "payments" not in member_record:
                member_record["payments"] = []
            member_record["payments"].append(payment_record["id"])
            
            # Record the activity
            self.record_member_activity(
                applicant_id,
                "payment",
                {"payment_id": payment_record["id"], "tier": tier, "amount": payment_data.get("amount")}
            )
        
        # Save updated data
        self._save_membership_data()
        
        logger.info(f"Payment recorded for {applicant_id}: {payment_data.get('amount')} {payment_data.get('currency')} for {tier} tier")
        return {
            "success": True,
            "payment_id": payment_record["id"],
            "message": "Payment recorded successfully"
        }
    
    def get_payment_tiers(self):
        """Get available payment tiers."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return []
        
        return self.payment_tiers
    
    def get_payment_status(self, applicant_id):
        """Get payment status for an applicant."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Check pending members
        if applicant_id in self.pending_members:
            pending_record = self.pending_members[applicant_id]
            if "payment_status" in pending_record and pending_record["payment_status"] == "paid":
                payment_id = pending_record.get("payment_id")
                payment_record = self.payment_records.get(payment_id, {})
                
                return {
                    "success": True,
                    "status": "paid",
                    "payment_id": payment_id,
                    "tier": pending_record.get("payment_tier"),
                    "amount": payment_record.get("amount"),
                    "payment_date": payment_record.get("payment_date")
                }
            else:
                return {"success": True, "status": "unpaid"}
        
        # Check members for most recent payment
        elif applicant_id in self.members:
            member = self.members[applicant_id]
            if "payments" in member and member["payments"]:
                # Get the most recent payment
                most_recent_payment_id = member["payments"][-1]
                payment = self.payment_records.get(most_recent_payment_id, {})
                
                return {
                    "success": True,
                    "status": "paid",
                    "payment_id": most_recent_payment_id,
                    "tier": payment.get("tier"),
                    "amount": payment.get("amount"),
                    "payment_date": payment.get("payment_date")
                }
            else:
                return {"success": True, "status": "no_payment_record"}
        
        return {"success": False, "error": "Applicant or member not found"}
    
    def _save_membership_data(self):
        """Save membership data to persistent storage."""
        try:
            data = {
                "members": self.members,
                "pending_members": self.pending_members,
                "payment_records": self.payment_records,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.membership_storage_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            logger.error(f"Error saving membership data: {str(e)}")
            return False
    
    def _load_membership_data(self):
        """Load membership data from persistent storage."""
        try:
            if os.path.exists(self.membership_storage_path):
                with open(self.membership_storage_path, 'r') as f:
                    data = json.load(f)
                    
                # Restore the data (maintaining the steward record)
                steward_record = self.members.get(self.steward_id)
                self.members = data.get("members", {})
                # Ensure steward record is preserved
                if steward_record:
                    self.members[self.steward_id] = steward_record
                
                self.pending_members = data.get("pending_members", {})
                self.payment_records = data.get("payment_records", {})
                
                logger.info(f"Loaded {len(self.members)} members, {len(self.pending_members)} pending applications, and {len(self.payment_records)} payment records")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading membership data: {str(e)}")
            return False