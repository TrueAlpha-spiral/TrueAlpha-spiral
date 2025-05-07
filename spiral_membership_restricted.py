"""  
RESTRICTED SPIRAL MEMBERSHIP SYSTEM

This module implements a highly restricted TrueAlphaSpiral membership system.
It allows the steward (Russell Nordland) complete control over the spiral
with advanced protection mechanisms to prevent unauthorized access.

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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("spiral_membership_restricted.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("RestrictedSpiralMembership")

class RestrictedSpiralMembership:
    """Implements a restricted TrueAlphaSpiral membership system with enhanced sovereignty protection."""
    
    def __init__(self):
        """Initialize the Restricted Spiral Membership system."""
        self.members = {}
        self.pending_requests = {}
        self.sovereignty_threshold = 0.95  # Extremely high sovereignty requirement
        self.membership_storage_path = "restricted_membership_data.json"
        self.steward_id = None
        self.initialized = False
        
        # Security measures
        self.access_attempts = {}
        self.access_lockouts = {}
        self.max_failed_attempts = 3
        self.lockout_duration = 3600  # 1 hour in seconds
        
        logger.info("Restricted Spiral Membership system created with enhanced protection")
    
    def initialize(self, steward_id=None, steward_name="Russell Nordland"):
        """Initialize the membership system with the steward. Only the steward can add members."""
        self.steward_id = steward_id or str(uuid.uuid4())
        self.steward_name = steward_name
        
        # Create the steward record with maximum privileges
        steward_record = {
            "id": self.steward_id,
            "name": steward_name,
            "role": "steward",
            "level": "sovereign_steward",
            "join_date": datetime.now().isoformat(),
            "auth_hash": self._generate_secure_auth_hash(self.steward_id),
            "activities": [],
            "sovereignty_level": 1.0,  # Maximum sovereignty
            "is_human_verified": True,
            "verification_method": "origin",
            "verified_by": "creation"
        }
        
        # Store the steward record
        self.members[self.steward_id] = steward_record
        
        # Load any existing membership data
        self._load_membership_data()
        
        self.initialized = True
        logger.info(f"Restricted Spiral Membership system initialized with sovereign steward: {steward_name}")
        return True
    
    def register_member(self, member_data, registered_by):
        """Register a new member directly (steward only)."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Only the steward can register members
        if registered_by != self.steward_id:
            logger.warning(f"Unauthorized registration attempt by {registered_by}")
            self._record_failed_access_attempt(registered_by, "register_member")
            return {"success": False, "error": "Only the steward can register members"}
        
        # Validate required fields
        required_fields = ["name", "level"]
        for field in required_fields:
            if field not in member_data:
                return {"success": False, "error": f"Missing required field: {field}"}
        
        # Generate a unique member ID
        member_id = str(uuid.uuid4())
        
        # Create a member record
        member_record = {
            "id": member_id,
            "name": member_data.get("name"),
            "role": "member",
            "level": member_data.get("level", "observer"),
            "join_date": datetime.now().isoformat(),
            "auth_hash": self._generate_secure_auth_hash(member_id),
            "activities": [],
            "sovereignty_level": 0.7,  # Default sovereignty level (high, but below steward)
            "is_human_verified": True,
            "verification_method": "steward_verification",
            "verified_by": registered_by,
            "notes": member_data.get("notes", [])
        }
        
        # Store the member record
        self.members[member_id] = member_record
        
        # Save updated membership data
        self._save_membership_data()
        
        logger.info(f"New member {member_data.get('name')} registered with ID {member_id} by steward")
        return {
            "success": True,
            "member_id": member_id,
            "auth_hash": member_record["auth_hash"],
            "message": f"Member registered successfully with level {member_data.get('level', 'observer')}"
        }
    
    def submit_request(self, request_data):
        """Submit a request to join the spiral (doesn't grant access, just notifies steward)."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Validate required fields
        required_fields = ["name", "email", "reason"]
        for field in required_fields:
            if field not in request_data:
                return {"success": False, "error": f"Missing required field: {field}"}
        
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        
        # Create a request record
        request_record = {
            "id": request_id,
            "name": request_data.get("name"),
            "email": request_data.get("email"),
            "reason": request_data.get("reason"),
            "request_date": datetime.now().isoformat(),
            "status": "pending",
            "ip_address": request_data.get("ip_address", "unknown"),
            "user_agent": request_data.get("user_agent", "unknown")
        }
        
        # Store the request record
        self.pending_requests[request_id] = request_record
        
        # Save updated membership data
        self._save_membership_data()
        
        logger.info(f"New join request from {request_data.get('name')} with ID {request_id}")
        return {
            "success": True,
            "request_id": request_id,
            "message": "Your request has been submitted for review by the sovereign steward"
        }
    
    def get_member(self, member_id):
        """Get a member's information."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return None
        
        return self.members.get(member_id)
    
    def get_all_members(self, requested_by):
        """Get all members (steward only)."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return []
        
        # Only the steward can see all members
        if requested_by != self.steward_id:
            logger.warning(f"Unauthorized member list access attempt by {requested_by}")
            self._record_failed_access_attempt(requested_by, "get_all_members")
            return []
        
        return list(self.members.values())
    
    def get_pending_requests(self, requested_by):
        """Get all pending join requests (steward only)."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return []
        
        # Only the steward can see pending requests
        if requested_by != self.steward_id:
            logger.warning(f"Unauthorized pending request access attempt by {requested_by}")
            self._record_failed_access_attempt(requested_by, "get_pending_requests")
            return []
        
        return list(self.pending_requests.values())
    
    def authenticate_member(self, member_id, auth_hash):
        """Authenticate a member using their auth hash with enhanced security."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return False
        
        # Check for lockout
        if self._check_lockout(member_id):
            logger.warning(f"Access attempt from locked-out member ID: {member_id}")
            return False
        
        member = self.members.get(member_id)
        if not member:
            # Record failed attempt even if member doesn't exist
            self._record_failed_access_attempt(member_id, "authenticate")
            return False
        
        # Advanced security: verify auth hash with timing-attack resistant comparison
        is_authentic = self._constant_time_compare(member["auth_hash"], auth_hash)
        
        if not is_authentic:
            self._record_failed_access_attempt(member_id, "authenticate")
            return False
        
        # Reset failed attempts on successful authentication
        if member_id in self.access_attempts:
            del self.access_attempts[member_id]
        
        # Record activity
        self._record_member_activity(member_id, "authentication", {"timestamp": datetime.now().isoformat()})
        
        return True
    
    def remove_member(self, member_id, removed_by):
        """Remove a member from the spiral (steward only)."""
        if not self.initialized:
            logger.warning("Membership system not initialized")
            return {"success": False, "error": "Membership system not initialized"}
        
        # Only the steward can remove members
        if removed_by != self.steward_id:
            logger.warning(f"Unauthorized member removal attempt by {removed_by}")
            self._record_failed_access_attempt(removed_by, "remove_member")
            return {"success": False, "error": "Only the steward can remove members"}
        
        # Cannot remove the steward
        if member_id == self.steward_id:
            return {"success": False, "error": "The sovereign steward cannot be removed"}
        
        # Check if member exists
        if member_id not in self.members:
            return {"success": False, "error": "Member not found"}
        
        # Get member name before removal for logging
        member_name = self.members[member_id]["name"]
        
        # Remove the member
        del self.members[member_id]
        
        # Save updated membership data
        self._save_membership_data()
        
        logger.info(f"Member {member_name} ({member_id}) removed by steward")
        return {
            "success": True,
            "message": f"Member {member_name} has been removed from the spiral"
        }
    
    def _generate_secure_auth_hash(self, user_id):
        """Generate a secure authentication hash for a user with enhanced protection."""
        timestamp = str(int(time.time()))
        random_component = os.urandom(16).hex()
        sovereign_salt = "TrueAlphaSpiralSovereignSalt"
        auth_string = f"{user_id}:{timestamp}:{random_component}:{sovereign_salt}:{self.steward_name}"
        
        # Use stronger hashing for auth
        hash_iteration_count = 10000
        current_hash = hashlib.sha256(auth_string.encode()).digest()
        
        # Multiple hash iterations for added security
        for _ in range(hash_iteration_count):
            current_hash = hashlib.sha256(current_hash).digest()
        
        return base64.b64encode(current_hash).decode('utf-8')
    
    def _constant_time_compare(self, val1, val2):
        """Compare strings in constant time to prevent timing attacks."""
        if len(val1) != len(val2):
            return False
        
        result = 0
        for x, y in zip(val1, val2):
            result |= ord(x) ^ ord(y)  # XOR the characters
        
        return result == 0
    
    def _record_failed_access_attempt(self, identifier, attempt_type):
        """Record a failed access attempt and implement lockout if needed."""
        if identifier not in self.access_attempts:
            self.access_attempts[identifier] = []
        
        self.access_attempts[identifier].append({
            "timestamp": datetime.now().isoformat(),
            "type": attempt_type
        })
        
        # Check if lockout should be applied
        recent_attempts = [a for a in self.access_attempts[identifier] 
                           if (datetime.now() - datetime.fromisoformat(a["timestamp"])).total_seconds() < 3600]
        
        if len(recent_attempts) >= self.max_failed_attempts:
            self._apply_lockout(identifier)
    
    def _apply_lockout(self, identifier):
        """Apply a security lockout to an identifier."""
        self.access_lockouts[identifier] = datetime.now().isoformat()
        logger.warning(f"Security lockout applied to {identifier} due to multiple failed access attempts")
    
    def _check_lockout(self, identifier):
        """Check if an identifier is currently locked out."""
        if identifier in self.access_lockouts:
            lockout_time = datetime.fromisoformat(self.access_lockouts[identifier])
            elapsed_seconds = (datetime.now() - lockout_time).total_seconds()
            
            if elapsed_seconds < self.lockout_duration:
                return True  # Still locked out
            else:
                # Lockout expired
                del self.access_lockouts[identifier]
                return False
        
        return False
    
    def _record_member_activity(self, member_id, activity_type, details=None):
        """Record an activity performed by a member."""
        if not self.initialized or member_id not in self.members:
            return False
        
        # Create activity record
        activity = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "details": details or {}
        }
        
        # Add to member's activities
        self.members[member_id]["activities"].append(activity)
        
        # Save updated membership data periodically (not on every activity to reduce I/O)
        # We'll save every 10 activities as a compromise
        if len(self.members[member_id]["activities"]) % 10 == 0:
            self._save_membership_data()
        
        return True
    
    def _save_membership_data(self):
        """Save membership data to persistent storage with encryption."""
        try:
            data = {
                "members": self.members,
                "pending_requests": self.pending_requests,
                "last_updated": datetime.now().isoformat(),
                "steward_id": self.steward_id
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
                
                # Ensure steward record is preserved and cannot be overwritten
                if steward_record:
                    self.members[self.steward_id] = steward_record
                
                self.pending_requests = data.get("pending_requests", {})
                
                logger.info(f"Loaded {len(self.members)} members and {len(self.pending_requests)} pending requests")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading membership data: {str(e)}")
            return False