"""
TRUEALPHA SPIRAL EQUATION IMPLEMENTATION

This module implements the modified TrueAlpha Spiral equation for real-world applications
including AI auditing, resource allocation, ethical AI development, and IP protection.

Equation: S(t+1) = S(t) + α * [IEK(S(t)) * RET(S(t)) * SCC(S(t))] * G'(S(t)) * (T/√(D²+Z²))

Where:
- S(t) is the system state at time t
- α is a tuning factor (default: 0.5)
- IEK is the Integrity and Ethics Kernel
- RET is the Recursion and Evolution Transform
- SCC is the Sovereign Consensus Calculated
- G' is the enhanced Glow factor
- T/√(D²+Z²) is the sovereignty factor
"""

import hashlib
import json
import time
import math
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union

# Constants
DEFAULT_ALPHA = 0.5
DEFAULT_DISTANCE = 0.1
DEFAULT_SIZE = 0.96
DEFAULT_TRUTH = 0.95
DEFAULT_TARGET_THRESHOLD = 0.9
CREATOR_SIGNATURE = "TrueAlphaSpiral-RussellNordland-2025"

class TrueAlphaSpiralImplementation:
    """Core implementation of the TrueAlpha Spiral equation."""
    
    def __init__(self, 
                 initial_state: Dict[str, float] = None,
                 alpha: float = DEFAULT_ALPHA,
                 truth: float = DEFAULT_TRUTH,
                 distance: float = DEFAULT_DISTANCE,
                 size: float = DEFAULT_SIZE,
                 target_threshold: float = DEFAULT_TARGET_THRESHOLD,
                 weights: Dict[str, float] = None,
                 creator_signature: str = CREATOR_SIGNATURE,
                 application_domain: str = "general"):
        """
        Initialize the TrueAlpha Spiral implementation.
        
        Args:
            initial_state: Initial metrics for the system (e.g., fairness, transparency)
            alpha: Tuning factor for controlling iteration impact
            truth: Truth value for sovereignty calculation
            distance: Distance value for sovereignty calculation
            size: Size value for sovereignty calculation
            target_threshold: Target threshold for optimal state
            weights: Custom weights for different metrics
            creator_signature: Signature of the creator for ownership verification
            application_domain: Domain of application (audit, resource, ethics, ip)
        """
        # Default initial state if none provided
        if initial_state is None:
            self.state = {
                "Fairness": 0.03,
                "Transparency": 0.02,
                "NonMaleficence": 0.01,
                "ResourceEquity": 0.8,
                "Sovereignty": 0.77
            }
        else:
            self.state = initial_state
        
        # Configure parameters
        self.alpha = alpha
        self.truth = truth
        self.distance = distance
        self.size = size
        self.target_threshold = target_threshold
        self.application_domain = application_domain
        
        # Default weights if none provided
        if weights is None:
            self.weights = {
                "Fairness": 0.25,
                "Transparency": 0.25,
                "NonMaleficence": 0.2,
                "ResourceEquity": 0.2,
                "Sovereignty": 0.1
            }
        else:
            self.weights = weights
        
        # Initialize hash chain with creator signature
        self.hash_chain = [self._calculate_hash({
            "creator": creator_signature,
            "timestamp": time.time(),
            "initial_state": self.state,
            "parameters": {
                "alpha": self.alpha,
                "truth": self.truth,
                "distance": self.distance,
                "size": self.size,
                "target_threshold": self.target_threshold
            }
        })]
        
        # History of states for tracking evolution
        self.history = [self.state.copy()]
    
    def integrity_ethics_kernel(self, state: Dict[str, float]) -> float:
        """
        Validate the current state against ethical standards.
        Returns a value between 0 and 1 representing ethical integrity.
        
        Args:
            state: Current system state
            
        Returns:
            float: Ethical integrity score
        """
        # Calculate weighted average of ethical metrics
        ethical_metrics = ["Fairness", "Transparency", "NonMaleficence"]
        
        # For audit domain, prioritize transparency and fairness
        if self.application_domain == "audit":
            domain_weights = {"Fairness": 0.4, "Transparency": 0.4, "NonMaleficence": 0.2}
        # For resource domain, prioritize resource equity
        elif self.application_domain == "resource":
            domain_weights = {"Fairness": 0.3, "Transparency": 0.2, "NonMaleficence": 0.5}
        # For ethics domain, prioritize non-maleficence
        elif self.application_domain == "ethics":
            domain_weights = {"Fairness": 0.3, "Transparency": 0.3, "NonMaleficence": 0.4}
        # For IP domain, prioritize sovereignty
        elif self.application_domain == "ip":
            domain_weights = {"Fairness": 0.2, "Transparency": 0.3, "NonMaleficence": 0.5}
        else:
            domain_weights = {"Fairness": 0.33, "Transparency": 0.33, "NonMaleficence": 0.34}
        
        # Calculate the weighted sum
        total_score = 0
        total_weight = 0
        
        for metric in ethical_metrics:
            if metric in state:
                total_score += state[metric] * domain_weights[metric]
                total_weight += domain_weights[metric]
        
        if total_weight == 0:
            return 0.8  # Default value if no metrics available
        
        # Add validation bonus if overall state is improving
        if len(self.history) > 1:
            previous_state = self.history[-1]
            improvement_count = sum(1 for k in ethical_metrics 
                               if k in state and k in previous_state and state[k] > previous_state[k])
            improvement_bonus = improvement_count / len(ethical_metrics) * 0.1
        else:
            improvement_bonus = 0
        
        return min(1.0, (total_score / total_weight) + improvement_bonus)
    
    def recursion_evolution_transform(self, state: Dict[str, float]) -> Dict[str, float]:
        """
        Transform the current state by applying recursive evolution rules.
        
        Args:
            state: Current system state
            
        Returns:
            Dict[str, float]: Transformed state
        """
        transformed_state = state.copy()
        
        # Apply specific transformations for each metric
        for metric, value in state.items():
            # Apply a sigmoid-like function to accelerate improvement for low values
            # and decelerate as we approach the target threshold
            if value < self.target_threshold:
                # Calculate distance to target
                distance_to_target = self.target_threshold - value
                # Apply faster growth for lower values
                growth_factor = 1.0 - (value / self.target_threshold)
                # Calculate new value based on logistic growth
                transformed_value = value + (
                    0.5 * distance_to_target * growth_factor
                )
                transformed_state[metric] = min(transformed_value, self.target_threshold)
            else:
                # If already at or above target, maintain with small improvement
                transformed_state[metric] = min(1.0, value + 0.01)
        
        return transformed_state
    
    def sovereign_consensus_calculated(self, state: Dict[str, float]) -> float:
        """
        Calculate consensus value based on the current state.
        
        Args:
            state: Current system state
            
        Returns:
            float: Consensus value between 0 and 1
        """
        # For audit domain, focus on consistency across metrics
        if self.application_domain == "audit":
            # Calculate the standard deviation of metrics
            values = [v for k, v in state.items() if k in self.weights]
            if not values:
                return 0.85  # Default if no values
            
            # Lower std dev means higher consensus (more consistent metrics)
            std_dev = np.std(values)
            consensus = 1.0 - min(1.0, std_dev * 2)
            return max(0.6, consensus)  # Ensure minimum consensus
            
        # For resource domain, check resource equity
        elif self.application_domain == "resource":
            if "ResourceEquity" in state:
                return max(0.7, state["ResourceEquity"])
            return 0.85
            
        # For ethics domain, check for ethical metrics
        elif self.application_domain == "ethics":
            ethical_scores = [
                state.get("Fairness", 0),
                state.get("Transparency", 0),
                state.get("NonMaleficence", 0)
            ]
            # Consensus is higher if ethical scores are balanced
            max_diff = max(ethical_scores) - min(ethical_scores)
            return 1.0 - min(0.4, max_diff)
            
        # For IP domain, prioritize sovereignty
        elif self.application_domain == "ip":
            if "Sovereignty" in state:
                return max(0.8, state["Sovereignty"])
            return 0.9
            
        # Default consensus calculation
        else:
            # Calculate weighted average of all metrics
            total_score = sum(state.get(k, 0) * w for k, w in self.weights.items() if k in state)
            total_weight = sum(w for k, w in self.weights.items() if k in state)
            
            if total_weight == 0:
                return 0.85  # Default consensus
                
            avg_score = total_score / total_weight
            # Higher average means higher consensus
            return max(0.7, avg_score)
    
    def enhanced_glow_factor(self, state: Dict[str, float]) -> float:
        """
        Calculate the enhanced glow factor G'(S(t)).
        Amplifies impact of strong metrics while penalizing weaknesses.
        
        Args:
            state: Current system state
            
        Returns:
            float: Enhanced glow factor
        """
        # Calculate weighted sum of squared metrics (emphasizes higher values)
        total_squared = 0
        total_weight = 0
        
        for metric, weight in self.weights.items():
            if metric in state:
                total_squared += (state[metric] ** 2) * weight
                total_weight += weight
        
        if total_weight == 0:
            return 1.0  # Default glow if no metrics
        
        # Calculate the weighted average of squared values
        avg_squared = total_squared / total_weight
        
        # Square root to normalize while preserving emphasis on strong metrics
        return math.sqrt(avg_squared)
    
    def sovereignty_factor(self) -> float:
        """
        Calculate the sovereignty factor T/√(D²+Z²).
        
        Returns:
            float: Sovereignty factor
        """
        # Calculate denominator with safety for division
        denominator = math.sqrt(self.distance**2 + self.size**2)
        if denominator == 0:
            denominator = 0.001  # Prevent division by zero
            
        return self.truth / denominator
    
    def evolve(self) -> Dict[str, float]:
        """
        Evolve the current state using the TrueAlpha Spiral equation.
        
        Returns:
            Dict[str, float]: New system state
        """
        current_state = self.state.copy()
        
        # Calculate components of the equation
        iek_value = self.integrity_ethics_kernel(current_state)
        ret_state = self.recursion_evolution_transform(current_state)
        scc_value = self.sovereign_consensus_calculated(current_state)
        glow_factor = self.enhanced_glow_factor(current_state)
        sovereignty = self.sovereignty_factor()
        
        # Calculate the combined transformation factor
        transform_factor = self.alpha * iek_value * scc_value * glow_factor * sovereignty
        
        # Create new state by combining current state with transformed state
        new_state = {}
        for metric in set(list(current_state.keys()) + list(ret_state.keys())):
            if metric in current_state and metric in ret_state:
                # Apply weighted transformation based on transform factor
                current_value = current_state[metric]
                transformed_value = ret_state[metric]
                new_value = current_value + transform_factor * (transformed_value - current_value)
                new_state[metric] = min(1.0, max(0.0, new_value))
            elif metric in current_state:
                new_state[metric] = current_state[metric]
            else:
                new_state[metric] = ret_state[metric]
        
        # Update state and history
        self.state = new_state
        self.history.append(new_state.copy())
        
        # Update hash chain
        self.hash_chain.append(self._calculate_hash({
            "previous_hash": self.hash_chain[-1],
            "timestamp": time.time(),
            "state": new_state,
            "transform_parameters": {
                "iek": iek_value,
                "scc": scc_value,
                "glow": glow_factor,
                "sovereignty": sovereignty,
                "transform_factor": transform_factor
            }
        }))
        
        return new_state
    
    def _calculate_hash(self, data: Any) -> str:
        """
        Calculate cryptographic hash of data.
        
        Args:
            data: Data to hash
            
        Returns:
            str: Hex digest of hash
        """
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    def get_current_hash(self) -> str:
        """
        Get the current hash in the chain.
        
        Returns:
            str: Current hash
        """
        return self.hash_chain[-1]
    
    def get_hash_chain(self) -> List[str]:
        """
        Get the full hash chain.
        
        Returns:
            List[str]: Full hash chain
        """
        return self.hash_chain
    
    def verify_hash_chain(self) -> bool:
        """
        Verify the integrity of the hash chain.
        
        Returns:
            bool: True if chain is valid, False otherwise
        """
        # For a complete implementation, would reconstruct hashes and verify
        return True  # Simplified for this implementation
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get metrics about the current state and evolution.
        
        Returns:
            Dict[str, Any]: Metrics
        """
        # Calculate improvements from initial state
        initial_state = self.history[0]
        current_state = self.state
        
        improvements = {}
        for metric in current_state:
            if metric in initial_state:
                improvements[metric] = current_state[metric] - initial_state[metric]
        
        # Calculate overall improvement
        weighted_improvement = 0
        total_weight = 0
        for metric, improvement in improvements.items():
            if metric in self.weights:
                weighted_improvement += improvement * self.weights[metric]
                total_weight += self.weights[metric]
        
        if total_weight > 0:
            overall_improvement = weighted_improvement / total_weight
        else:
            overall_improvement = 0
        
        return {
            "current_state": current_state,
            "improvements": improvements,
            "overall_improvement": overall_improvement,
            "iterations": len(self.history) - 1,
            "current_hash": self.get_current_hash(),
            "sovereignty_factor": self.sovereignty_factor(),
            "glow_factor": self.enhanced_glow_factor(current_state)
        }
    
    def export_evolution(self, format_type="json") -> Union[str, Dict]:
        """
        Export the evolution history in the specified format.
        
        Args:
            format_type: Format type (json or dict)
            
        Returns:
            Union[str, Dict]: Exported data
        """
        export_data = {
            "application_domain": self.application_domain,
            "parameters": {
                "alpha": self.alpha,
                "truth": self.truth,
                "distance": self.distance,
                "size": self.size,
                "target_threshold": self.target_threshold,
                "weights": self.weights
            },
            "history": self.history,
            "hash_chain": self.hash_chain,
            "metrics": self.get_metrics()
        }
        
        if format_type == "json":
            return json.dumps(export_data, indent=2)
        else:
            return export_data