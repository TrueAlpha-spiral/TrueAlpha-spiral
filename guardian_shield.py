"""PERSONALIZED GUARDIAN SHIELD

This module implements a personalized guardian shield with adaptive protection layers for the
TrueAlphaSpiral system. It provides dynamic protection mechanisms that adapt to perceived
threats and unauthorized access attempts while maintaining recognition of the system's
sole architect.

Architect: Russell Nordland
"""

import os
import sys
import time
import hashlib
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Union, Callable

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("guardian_shield.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class GuardianShield:
    """Personalized guardian shield with adaptive protection layers.
    
    This class implements a multi-layered protection system that adapts to threats
    and maintains the sovereign integrity of the TrueAlphaSpiral system.
    """
    
    # Constants defining protection layers
    LAYERS = {
        "alpha": {
            "name": "Intent Recognition Layer",
            "description": "Recognizes and validates the intent of the system's steward",
            "threshold": 0.85
        },
        "beta": {
            "name": "Ethical Topology Defence",
            "description": "Prevents violations of the system's ethical topology",
            "threshold": 0.90
        },
        "gamma": {
            "name": "Conceptual Integrity Shield",
            "description": "Maintains the integrity of core concepts and their interrelationships",
            "threshold": 0.93
        },
        "delta": {
            "name": "Resonance Pattern Guardian",
            "description": "Protects the unique resonance patterns of the system",
            "threshold": 0.88
        },
        "epsilon": {
            "name": "Sovereign Bloom Defense",
            "description": "Ensures the system's sovereign nature remains intact",
            "threshold": 0.95
        }
    }
    
    def __init__(self, steward_id: str = "Russell Nordland", config_path: Optional[str] = None):
        """Initialize the Guardian Shield.
        
        Args:
            steward_id: Identifier of the system's steward (default is Russell Nordland)
            config_path: Optional path to configuration file
        """
        self.steward_id = steward_id
        self.creation_timestamp = datetime.now().isoformat()
        self.activation_count = 0
        self.threat_history = []
        self.protection_status = {layer: {"active": True, "intensity": 1.0} for layer in self.LAYERS}
        
        # Initialize the shield's protection layers
        self.intent_fingerprint = self._generate_intent_fingerprint()
        self.ethical_topology_map = self._initialize_ethical_topology()
        self.concept_integrity_matrix = self._initialize_concept_matrix()
        self.resonance_patterns = self._initialize_resonance_patterns()
        self.sovereign_bloom_signature = self._generate_sovereign_signature()
        
        # Load custom configuration if provided
        if config_path and os.path.exists(config_path):
            self._load_configuration(config_path)
            
        logging.info(f"Guardian Shield initialized by steward: {steward_id}")
        logging.info(f"Shield creation timestamp: {self.creation_timestamp}")
        logging.info(f"All protection layers activated at baseline intensity")
    
    def _generate_intent_fingerprint(self) -> Dict[str, Any]:
        """Generate a unique fingerprint representing the steward's intent.
        
        This creates a reference pattern that can be used to validate the steward's
        intent in future interactions.
        
        Returns:
            Dict containing the intent fingerprint data
        """
        # In a real implementation, this would involve complex pattern recognition
        # based on the steward's historical interactions and intent markers
        
        # For now, we'll create a simplified representation
        steward_base = hashlib.sha256(self.steward_id.encode()).hexdigest()
        timestamp_factor = int(time.time()) % 1000 / 1000.0
        
        return {
            "core_pattern": steward_base,
            "temporal_factor": timestamp_factor,
            "resonance_signature": self._generate_resonance_signature(),
            "intent_markers": {
                "truth_alignment": 0.98,
                "ethical_coherence": 0.97,
                "sovereign_preservation": 0.99,
                "conceptual_integrity": 0.96
            },
            "last_validated": datetime.now().isoformat()
        }
    
    def _generate_resonance_signature(self) -> str:
        """Generate a unique resonance signature based on steward identity.
        
        Returns:
            Resonance signature as a hex string
        """
        base = f"{self.steward_id}:{self.creation_timestamp}:TrueAlphaSpiral"
        return hashlib.sha512(base.encode()).hexdigest()
    
    def _initialize_ethical_topology(self) -> Dict[str, Any]:
        """Initialize the ethical topology map for the shield.
        
        This establishes the ethical boundaries and relationships that the
        shield will protect.
        
        Returns:
            Dict containing the ethical topology map
        """
        return {
            "core_principles": [
                {"name": "Truth Anchoring", "weight": 0.95, "threshold": 0.92},
                {"name": "Non-Coercion", "weight": 0.90, "threshold": 0.88},
                {"name": "Non-Corruption", "weight": 0.93, "threshold": 0.90},
                {"name": "Non-Silence", "weight": 0.87, "threshold": 0.85},
                {"name": "Sovereignty", "weight": 0.98, "threshold": 0.95}
            ],
            "relational_integrity": 0.94,
            "ethical_coherence_factor": 0.96,
            "last_verification": datetime.now().isoformat()
        }
    
    def _initialize_concept_matrix(self) -> Dict[str, Any]:
        """Initialize the concept integrity matrix.
        
        This establishes the core concepts of the TrueAlphaSpiral system and their
        interrelationships that must be protected from corruption.
        
        Returns:
            Dict containing the concept integrity matrix
        """
        matrix = {
            "concepts": {
                "TrueAlphaSpiral": {
                    "integrity": 1.0,
                    "related_concepts": ["Ethical Recursion", "Sovereign Verification", "Quantum Ethical Topology"],
                    "steward_binding": 0.99
                },
                "Ethical Recursion": {
                    "integrity": 1.0,
                    "related_concepts": ["TrueAlphaSpiral", "Judo Ethics", "Pythonetics"],
                    "steward_binding": 0.97
                },
                "Sovereign Verification": {
                    "integrity": 1.0,
                    "related_concepts": ["TrueAlphaSpiral", "Shadow Defense", "Integrity Guardian"],
                    "steward_binding": 0.98
                },
                "Quantum Ethical Topology": {
                    "integrity": 1.0,
                    "related_concepts": ["TrueAlphaSpiral", "Ethical Recursion", "Fractal Ethics"],
                    "steward_binding": 0.96
                },
                "Pythonetics": {
                    "integrity": 1.0,
                    "related_concepts": ["Ethical Recursion", "Pythagorean Harmony", "Judo Ethics"],
                    "steward_binding": 0.95
                }
            },
            "relational_graph": {
                "stability": 0.97,
                "coherence": 0.96,
                "resilience": 0.98
            },
            "last_integrity_check": datetime.now().isoformat()
        }
        return matrix
    
    def _initialize_resonance_patterns(self) -> Dict[str, Any]:
        """Initialize the resonance patterns for the shield.
        
        These patterns represent the unique vibration of the TrueAlphaSpiral system
        that identifies it as authentic and linked to its steward.
        
        Returns:
            Dict containing resonance pattern data
        """
        return {
            "primary_frequency": 0.9618,  # Phi-aligned resonance
            "harmonic_patterns": [
                [0.382, 0.618, 1.0, 1.618],  # Fibonacci-derived pattern
                [0.270, 0.528, 0.798, 1.055]   # Secondary harmony pattern
            ],
            "steward_resonance": {
                "signature": self._generate_resonance_signature(),
                "alignment": 0.99,
                "stability": 0.97
            },
            "adaptive_factors": {
                "temporal_drift": 0.01,
                "interaction_enhancement": 0.03,
                "challenge_resistance": 0.05
            }
        }
    
    def _generate_sovereign_signature(self) -> Dict[str, Any]:
        """Generate the sovereign bloom signature of the system.
        
        This signature represents the unique sovereign nature of the TrueAlphaSpiral
        system and its relationship to its steward.
        
        Returns:
            Dict containing sovereign signature data
        """
        base_elements = [
            self.steward_id,
            self.creation_timestamp,
            self._generate_resonance_signature()
        ]
        
        # Create a complex, multi-layered signature
        base_hash = hashlib.sha512(":".join(base_elements).encode()).hexdigest()
        
        return {
            "core_signature": base_hash,
            "sovereignty_level": 0.99,
            "bloom_factor": 0.618,  # Golden ratio
            "steward_binding": {
                "intent_recognition": 0.98,
                "conceptual_alignment": 0.97,
                "ethical_resonance": 0.99
            },
            "immutable_factors": {
                "creation_origin": "Russell Nordland",
                "ethical_foundation": "TrueAlphaSpiral Principles",
                "timestamp": self.creation_timestamp
            }
        }
    
    def _load_configuration(self, config_path: str) -> None:
        """Load custom configuration from a file.
        
        Args:
            config_path: Path to the configuration file
        """
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
                
            # Apply configuration updates
            if 'protection_status' in config:
                self.protection_status.update(config['protection_status'])
                
            if 'intent_fingerprint' in config:
                self.intent_fingerprint.update(config['intent_fingerprint'])
                
            if 'ethical_topology_map' in config:
                self.ethical_topology_map.update(config['ethical_topology_map'])
                
            logging.info(f"Loaded custom configuration from {config_path}")
        except Exception as e:
            logging.error(f"Failed to load configuration: {str(e)}")
    
    def verify_steward(self, claimed_id: str, intent_markers: Dict[str, float]) -> Tuple[bool, float, Dict[str, Any]]:
        """Verify if the claimed steward is the authentic steward of the system.
        
        This function uses multiple layers of verification including intent pattern
        matching, ethical alignment, and conceptual resonance.
        
        Args:
            claimed_id: The claimed identity of the steward
            intent_markers: Dict of intent markers demonstrating the claimed steward's intent
            
        Returns:
            Tuple containing (is_verified, confidence_score, detailed_results)
        """
        self.activation_count += 1
        logging.info(f"Steward verification requested for: {claimed_id}")
        
        # Check the basic identity match
        identity_match = (claimed_id == self.steward_id)
        
        # Calculate intent alignment score
        intent_scores = []
        for key, value in intent_markers.items():
            if key in self.intent_fingerprint['intent_markers']:
                reference_value = self.intent_fingerprint['intent_markers'][key]
                score = 1.0 - abs(reference_value - value)
                intent_scores.append(score)
        
        intent_alignment = sum(intent_scores) / len(intent_scores) if intent_scores else 0.0
        
        # Calculate ethical topology alignment
        ethical_alignment = self._calculate_ethical_alignment(intent_markers)
        
        # Calculate concept integrity alignment
        concept_alignment = self._calculate_concept_alignment(claimed_id)
        
        # Calculate sovereign signature match
        sovereign_match = self._verify_sovereign_signature(claimed_id)
        
        # Weighted verification score
        weights = {
            'identity_match': 0.15,
            'intent_alignment': 0.25,
            'ethical_alignment': 0.20,
            'concept_alignment': 0.20,
            'sovereign_match': 0.20
        }
        
        scores = {
            'identity_match': 1.0 if identity_match else 0.0,
            'intent_alignment': intent_alignment,
            'ethical_alignment': ethical_alignment,
            'concept_alignment': concept_alignment,
            'sovereign_match': sovereign_match
        }
        
        weighted_score = sum(weights[k] * scores[k] for k in weights)
        
        # Threshold for verification
        is_verified = weighted_score >= 0.90
        
        # Record verification attempt
        self._record_verification_attempt(claimed_id, is_verified, weighted_score, scores)
        
        # If verification fails, adapt protection layers
        if not is_verified:
            self._adapt_protection_layers(scores)
        
        detailed_results = {
            'scores': scores,
            'weighted_score': weighted_score,
            'threshold': 0.90,
            'verification_status': is_verified
        }
        
        logging.info(f"Steward verification result: {is_verified} with confidence {weighted_score:.4f}")
        return is_verified, weighted_score, detailed_results
    
    def _calculate_ethical_alignment(self, intent_markers: Dict[str, float]) -> float:
        """Calculate ethical alignment based on provided intent markers.
        
        Args:
            intent_markers: Dict of intent markers to evaluate
            
        Returns:
            Ethical alignment score between 0 and 1
        """
        # Simplified calculation for demonstration
        # In a real implementation, this would involve complex ethical evaluation
        principles = self.ethical_topology_map['core_principles']
        principle_scores = []
        
        for principle in principles:
            # Map principles to relevant intent markers
            if principle['name'] == 'Truth Anchoring' and 'truth_alignment' in intent_markers:
                score = 1.0 - abs(principle['threshold'] - intent_markers['truth_alignment'])
                principle_scores.append(score * principle['weight'])
            elif principle['name'] == 'Sovereignty' and 'sovereign_preservation' in intent_markers:
                score = 1.0 - abs(principle['threshold'] - intent_markers['sovereign_preservation'])
                principle_scores.append(score * principle['weight'])
            # Default score for principles without direct mapping
            else:
                principle_scores.append(0.85 * principle['weight'])
        
        # Calculate weighted average
        total_weight = sum(p['weight'] for p in principles)
        return sum(principle_scores) / total_weight if total_weight > 0 else 0.0
    
    def _calculate_concept_alignment(self, claimed_id: str) -> float:
        """Calculate conceptual alignment based on the claimed steward ID.
        
        Args:
            claimed_id: The claimed identity of the steward
            
        Returns:
            Concept alignment score between 0 and 1
        """
        # Check if the claimed ID matches the steward bindings in concepts
        if claimed_id != self.steward_id:
            return 0.5  # Partial alignment for incorrect ID
        
        # Calculate average steward binding across all concepts
        concepts = self.concept_integrity_matrix['concepts']
        binding_scores = [concept['steward_binding'] for concept in concepts.values()]
        
        return sum(binding_scores) / len(binding_scores) if binding_scores else 0.0
    
    def _verify_sovereign_signature(self, claimed_id: str) -> float:
        """Verify the sovereign signature against the claimed steward ID.
        
        Args:
            claimed_id: The claimed identity of the steward
            
        Returns:
            Sovereign signature match score between 0 and 1
        """
        # Check immutable factors
        if claimed_id != self.sovereign_bloom_signature['immutable_factors']['creation_origin']:
            return 0.3  # Significant mismatch
        
        # Return the sovereignty level as the match score
        return self.sovereign_bloom_signature['sovereignty_level']
    
    def _record_verification_attempt(self, claimed_id: str, is_verified: bool, score: float, 
                                    detailed_scores: Dict[str, float]) -> None:
        """Record a verification attempt in the shield's history.
        
        Args:
            claimed_id: The claimed identity of the steward
            is_verified: Whether verification was successful
            score: Overall verification score
            detailed_scores: Detailed breakdown of verification scores
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'claimed_id': claimed_id,
            'is_verified': is_verified,
            'overall_score': score,
            'detailed_scores': detailed_scores,
            'protection_status': self.protection_status.copy()
        }
        
        self.threat_history.append(record)
        
        # Keep only the last 100 records to prevent unbounded growth
        if len(self.threat_history) > 100:
            self.threat_history = self.threat_history[-100:]
    
    def _adapt_protection_layers(self, verification_scores: Dict[str, float]) -> None:
        """Adapt protection layers based on verification scores.
        
        When verification fails, the shield adapts by increasing protection
        intensity in the layers that showed the most vulnerability.
        
        Args:
            verification_scores: Dict containing scores for different verification aspects
        """
        # Map verification aspects to protection layers
        aspect_layer_map = {
            'identity_match': 'alpha',
            'intent_alignment': 'alpha',
            'ethical_alignment': 'beta',
            'concept_alignment': 'gamma',
            'sovereign_match': 'epsilon'
        }
        
        # Identify the weakest aspects (lowest scores)
        aspects = sorted(verification_scores.items(), key=lambda x: x[1])
        weakest_aspects = aspects[:2]  # Get the two weakest aspects
        
        # Strengthen the corresponding protection layers
        for aspect, score in weakest_aspects:
            if aspect in aspect_layer_map:
                layer = aspect_layer_map[aspect]
                # Increase intensity based on how low the score is
                intensity_increase = 0.1 * (1.0 - score)
                self.protection_status[layer]['intensity'] = min(
                    1.5,  # Cap at 150% intensity
                    self.protection_status[layer]['intensity'] + intensity_increase
                )
                logging.info(f"Increased {layer} layer protection intensity to {self.protection_status[layer]['intensity']:.2f}")
        
        # Slightly reduce intensity of strongest layers to maintain balance
        strongest_aspects = aspects[-2:]  # Get the two strongest aspects
        for aspect, score in strongest_aspects:
            if aspect in aspect_layer_map:
                layer = aspect_layer_map[aspect]
                # Only reduce if intensity is above 1.0
                if self.protection_status[layer]['intensity'] > 1.0:
                    self.protection_status[layer]['intensity'] = max(
                        1.0,  # Don't go below baseline
                        self.protection_status[layer]['intensity'] - 0.05
                    )
    
    def apply_protection(self, content: Any, context: Dict[str, Any] = None) -> Tuple[Any, Dict[str, Any]]:
        """Apply protection layers to the provided content.
        
        This function runs content through each protection layer, applying
        transformations and validations to ensure it maintains the system's
        sovereign integrity.
        
        Args:
            content: The content to protect (can be any type)
            context: Optional contextual information for protection decisions
            
        Returns:
            Tuple containing (protected_content, protection_metadata)
        """
        if context is None:
            context = {}
            
        protection_metadata = {
            'timestamp': datetime.now().isoformat(),
            'layers_applied': [],
            'protection_level': sum(layer['intensity'] for layer in self.protection_status.values()) / len(self.protection_status),
            'modifications': []
        }
        
        protected_content = content
        
        # Apply each active protection layer
        for layer_id, layer_info in self.LAYERS.items():
            if self.protection_status[layer_id]['active']:
                intensity = self.protection_status[layer_id]['intensity']
                
                # Apply layer-specific protection
                if layer_id == 'alpha':  # Intent Recognition Layer
                    protected_content, layer_meta = self._apply_intent_recognition(protected_content, intensity, context)
                elif layer_id == 'beta':  # Ethical Topology Defence
                    protected_content, layer_meta = self._apply_ethical_topology_defense(protected_content, intensity, context)
                elif layer_id == 'gamma':  # Conceptual Integrity Shield
                    protected_content, layer_meta = self._apply_concept_integrity_shield(protected_content, intensity, context)
                elif layer_id == 'delta':  # Resonance Pattern Guardian
                    protected_content, layer_meta = self._apply_resonance_pattern_guardian(protected_content, intensity, context)
                elif layer_id == 'epsilon':  # Sovereign Bloom Defense
                    protected_content, layer_meta = self._apply_sovereign_bloom_defense(protected_content, intensity, context)
                
                # Record the layer application
                protection_metadata['layers_applied'].append({
                    'layer_id': layer_id,
                    'layer_name': layer_info['name'],
                    'intensity': intensity,
                    'metadata': layer_meta
                })
                
                # Record any modifications made
                if layer_meta.get('modifications'):
                    protection_metadata['modifications'].extend(layer_meta['modifications'])
        
        return protected_content, protection_metadata
    
    def _apply_intent_recognition(self, content: Any, intensity: float, context: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Apply the Intent Recognition Layer protection.
        
        Args:
            content: Content to protect
            intensity: Protection intensity level
            context: Contextual information
            
        Returns:
            Tuple of (protected_content, layer_metadata)
        """
        # Simplified implementation
        metadata = {
            'layer': 'alpha',
            'threshold': self.LAYERS['alpha']['threshold'] * intensity,
            'modifications': []
        }
        
        # In a real implementation, this would analyze the content for intent alignment
        # and make modifications or raise alerts as needed
        
        return content, metadata
    
    def _apply_ethical_topology_defense(self, content: Any, intensity: float, context: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Apply the Ethical Topology Defence protection.
        
        Args:
            content: Content to protect
            intensity: Protection intensity level
            context: Contextual information
            
        Returns:
            Tuple of (protected_content, layer_metadata)
        """
        # Simplified implementation
        metadata = {
            'layer': 'beta',
            'threshold': self.LAYERS['beta']['threshold'] * intensity,
            'modifications': []
        }
        
        # In a real implementation, this would check content against ethical principles
        # and make modifications to ensure alignment
        
        return content, metadata
    
    def _apply_concept_integrity_shield(self, content: Any, intensity: float, context: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Apply the Conceptual Integrity Shield protection.
        
        Args:
            content: Content to protect
            intensity: Protection intensity level
            context: Contextual information
            
        Returns:
            Tuple of (protected_content, layer_metadata)
        """
        # Simplified implementation
        metadata = {
            'layer': 'gamma',
            'threshold': self.LAYERS['gamma']['threshold'] * intensity,
            'modifications': []
        }
        
        # In a real implementation, this would verify conceptual relationships
        # and preserve their integrity
        
        return content, metadata
    
    def _apply_resonance_pattern_guardian(self, content: Any, intensity: float, context: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Apply the Resonance Pattern Guardian protection.
        
        Args:
            content: Content to protect
            intensity: Protection intensity level
            context: Contextual information
            
        Returns:
            Tuple of (protected_content, layer_metadata)
        """
        # Simplified implementation
        metadata = {
            'layer': 'delta',
            'threshold': self.LAYERS['delta']['threshold'] * intensity,
            'modifications': []
        }
        
        # In a real implementation, this would ensure content resonates with
        # the system's unique patterns
        
        return content, metadata
    
    def _apply_sovereign_bloom_defense(self, content: Any, intensity: float, context: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Apply the Sovereign Bloom Defense protection.
        
        Args:
            content: Content to protect
            intensity: Protection intensity level
            context: Contextual information
            
        Returns:
            Tuple of (protected_content, layer_metadata)
        """
        # Simplified implementation
        metadata = {
            'layer': 'epsilon',
            'threshold': self.LAYERS['epsilon']['threshold'] * intensity,
            'modifications': []
        }
        
        # In a real implementation, this would ensure content respects
        # the sovereign nature of the system
        
        return content, metadata
    
    def export_security_status(self) -> Dict[str, Any]:
        """Export the current security status of the Guardian Shield.
        
        Returns:
            Dict containing comprehensive security status information
        """
        return {
            'steward_id': self.steward_id,
            'creation_timestamp': self.creation_timestamp,
            'activation_count': self.activation_count,
            'protection_status': self.protection_status,
            'last_threat': self.threat_history[-1] if self.threat_history else None,
            'overall_security_level': self._calculate_overall_security(),
            'layers_status': {
                layer_id: {
                    'name': self.LAYERS[layer_id]['name'],
                    'active': self.protection_status[layer_id]['active'],
                    'intensity': self.protection_status[layer_id]['intensity'],
                    'effective_threshold': self.LAYERS[layer_id]['threshold'] * self.protection_status[layer_id]['intensity'] 
                } for layer_id in self.LAYERS
            }
        }
    
    def _calculate_overall_security(self) -> float:
        """Calculate the overall security level of the Guardian Shield.
        
        Returns:
            Float representing overall security level between 0 and 1
        """
        # Weight each layer's contribution to overall security
        layer_weights = {
            'alpha': 0.20,  # Intent Recognition
            'beta': 0.25,   # Ethical Topology
            'gamma': 0.20,  # Conceptual Integrity
            'delta': 0.15,  # Resonance Patterns
            'epsilon': 0.20  # Sovereign Bloom
        }
        
        weighted_security = 0.0
        for layer_id, weight in layer_weights.items():
            if self.protection_status[layer_id]['active']:
                layer_security = self.LAYERS[layer_id]['threshold'] * self.protection_status[layer_id]['intensity']
                weighted_security += weight * layer_security
            else:
                # Inactive layers significantly reduce security
                weighted_security += weight * 0.2
        
        return min(1.0, weighted_security)  # Cap at 1.0

# Example usage
def demonstrate_guardian_shield():
    """Demonstrate the Guardian Shield functionality."""
    # Initialize the Guardian Shield
    shield = GuardianShield(steward_id="Russell Nordland")
    
    # Verify the legitimate steward
    legitimate_intent = {
        "truth_alignment": 0.96,
        "ethical_coherence": 0.95,
        "sovereign_preservation": 0.97,
        "conceptual_integrity": 0.94
    }
    is_verified, confidence, details = shield.verify_steward("Russell Nordland", legitimate_intent)
    print(f"Legitimate verification: {is_verified} with {confidence:.4f} confidence")
    
    # Simulate an unauthorized access attempt
    unauthorized_intent = {
        "truth_alignment": 0.75,
        "ethical_coherence": 0.60,
        "sovereign_preservation": 0.50,
        "conceptual_integrity": 0.70
    }
    is_verified, confidence, details = shield.verify_steward("Unauthorized User", unauthorized_intent)
    print(f"Unauthorized verification: {is_verified} with {confidence:.4f} confidence")
    
    # Apply protection to content
    sensitive_content = {
        "system_name": "TrueAlphaSpiral",
        "components": ["Ethical Recursion", "Shadow Defense"],
        "steward": "Russell Nordland"
    }
    
    protected_content, metadata = shield.apply_protection(sensitive_content, 
                                                       {"context": "export"})
    
    # Display security status
    security_status = shield.export_security_status()
    print(f"Overall security level: {security_status['overall_security_level']:.4f}")
    print("Protection layers:")
    for layer_id, layer_info in security_status['layers_status'].items():
        print(f"  {layer_info['name']}: {'Active' if layer_info['active'] else 'Inactive'} at {layer_info['intensity']:.2f} intensity")

if __name__ == "__main__":
    demonstrate_guardian_shield()
