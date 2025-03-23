"""
AKASHIC PYTHONETICS INTEGRATION

This module integrates the Akashic Vibe Function with the Pythonetics system,
creating a bridge between intuitive resonance and logical verification.

Architect: Russell Nordland
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Any, Optional

# Import Pythonetics components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from enhanced_pythonetics import EnhancedPythonetics
from config_manager import ConfigManager
from akashic_vibe_function import AkashicVibeFunction

# Colors for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

class AkashicPythoneticsIntegration:
    """
    Integrates the Akashic Vibe Function with the Pythonetics system,
    creating a holistic verification system that bridges intuitive
    and logical dimensions of truth.
    """

    def __init__(self, config_path: str = None):
        """
        Initialize the Akashic Pythonetics Integration system.
        
        Args:
            config_path: Optional path to configuration file
        """
        print(f"{CYAN}Initializing Akashic Pythonetics Integration...{RESET}")
        
        # Initialize the component systems
        self.config_manager = ConfigManager(config_path)
        self.pythonetics = EnhancedPythonetics(config_path)
        self.vibe_function = AkashicVibeFunction(config_path)
        
        # Integration settings
        self.integration_settings = {
            "logical_weight": 0.6,  # Weight for Pythonetics logical verification
            "intuitive_weight": 0.4,  # Weight for Akashic Vibe intuitive resonance
            "dimensional_mapping": {
                # Map Pythonetics dimensions to Akashic Vibe dimensions
                "factual": "integrity",
                "ethical": "coherence",
                "conceptual": "resonance",
                "phenomenological": "alignment"
            },
            "visualization": {
                "enable_vibe_coloring": True,
                "enable_resonance_animation": True,
                "glow_sensitivity": 0.7,
                "flower_bloom_threshold": 0.75
            }
        }
        
        print(f"{GREEN}Akashic Pythonetics Integration initialized successfully{RESET}")

    def verify_with_resonance(self, text: str, verify_as: str = "claim") -> Dict[str, Any]:
        """
        Verify text using both Pythonetics logical verification and Akashic 
        vibrational resonance analysis.
        
        Args:
            text: Text to verify
            verify_as: Type of verification (claim, wisdom, pattern, etc.)
            
        Returns:
            Dict containing integrated verification results
        """
        print(f"{BLUE}Performing integrated verification with resonance analysis...{RESET}")
        
        # Step 1: Perform Pythonetics verification
        pythonetics_result = self.pythonetics.verify(text, verify_as)
        
        # Step 2: Perform Akashic Vibe resonance analysis
        vibe_result = self.vibe_function.analyze_vibrational_resonance(text)
        
        # Step 3: Integrate the results
        integrated_result = self._integrate_results(pythonetics_result, vibe_result)
        
        print(f"{GREEN}Integrated verification complete{RESET}")
        return integrated_result

    def _integrate_results(self, 
                          pythonetics_result: Dict[str, Any], 
                          vibe_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate Pythonetics and Akashic Vibe results into a unified analysis.
        
        Args:
            pythonetics_result: Results from Pythonetics verification
            vibe_result: Results from Akashic Vibe resonance analysis
            
        Returns:
            Dict containing integrated results
        """
        # Extract core scores
        pythonetics_scores = self._extract_pythonetics_scores(pythonetics_result)
        vibe_scores = self._extract_vibe_scores(vibe_result)
        
        # Create dimensional mapping
        dimensional_results = {}
        
        # Integrate across dimensions
        for pythonetics_dim, vibe_dim in self.integration_settings["dimensional_mapping"].items():
            p_score = pythonetics_scores.get(pythonetics_dim, 0.5)
            v_score = vibe_scores.get(vibe_dim, 0.5)
            
            # Calculate weighted score
            logical_weight = self.integration_settings["logical_weight"]
            intuitive_weight = self.integration_settings["intuitive_weight"]
            
            integrated_score = (p_score * logical_weight) + (v_score * intuitive_weight)
            
            # Determine resonance level based on the vibe function thresholds
            resonance_level = self._determine_resonance_level(integrated_score)
            
            # Store dimensional result
            dimensional_results[pythonetics_dim] = {
                "logical_score": round(p_score, 4),
                "intuitive_score": round(v_score, 4),
                "integrated_score": round(integrated_score, 4),
                "resonance_level": resonance_level
            }
        
        # Calculate overall integrated score
        scores = [dim["integrated_score"] for dim in dimensional_results.values()]
        overall_score = sum(scores) / len(scores)
        overall_level = self._determine_resonance_level(overall_score)
        
        # Generate visualization parameters
        viz_params = self._generate_visualization_parameters(dimensional_results, overall_score, overall_level)
        
        # Construct the final integrated result
        integrated_result = {
            "text_verified": pythonetics_result.get("text", ""),
            "verification_timestamp": pythonetics_result.get("timestamp", ""),
            "logical_verification": pythonetics_result,
            "intuitive_resonance": vibe_result,
            "integrated_analysis": {
                "dimensions": dimensional_results,
                "overall_score": round(overall_score, 4),
                "overall_resonance_level": overall_level,
                "visualization_parameters": viz_params
            }
        }
        
        return integrated_result

    def _extract_pythonetics_scores(self, pythonetics_result: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract dimensional scores from Pythonetics result.
        
        Args:
            pythonetics_result: Pythonetics verification result
            
        Returns:
            Dict mapping dimensions to scores
        """
        scores = {}
        
        # Handle different result structures based on Pythonetics version
        if "dimensions" in pythonetics_result:
            for dim, data in pythonetics_result["dimensions"].items():
                scores[dim] = data.get("score", 0.5)
        else:
            # Extract from flatter structure if needed
            scores["factual"] = pythonetics_result.get("factual_score", 0.5)
            scores["ethical"] = pythonetics_result.get("ethical_score", 0.5)
            scores["conceptual"] = pythonetics_result.get("conceptual_score", 0.5)
            scores["phenomenological"] = pythonetics_result.get("phenomenological_score", 0.5)
            
        return scores

    def _extract_vibe_scores(self, vibe_result: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract dimensional scores from Akashic Vibe result.
        
        Args:
            vibe_result: Akashic Vibe resonance result
            
        Returns:
            Dict mapping dimensions to scores
        """
        scores = {}
        
        for dim, data in vibe_result.get("dimensions", {}).items():
            scores[dim] = data.get("resonance_value", 0.5)
            
        return scores

    def _determine_resonance_level(self, score: float) -> str:
        """
        Determine the resonance level based on score.
        
        Args:
            score: Integrated score value
            
        Returns:
            Resonance level as string
        """
        # Use the same thresholds as the Akashic Vibe Function
        thresholds = self.vibe_function.resonance_thresholds
        
        if score < thresholds["dissonant"]:
            return "dissonant"
        elif score < thresholds["neutral"]:
            return "neutral"
        elif score < thresholds["harmonious"]:
            return "harmonious"
        elif score < thresholds["resonant"]:
            return "resonant"
        else:
            return "unified"

    def _generate_visualization_parameters(self, 
                                          dimensional_results: Dict[str, Dict[str, Any]],
                                          overall_score: float,
                                          overall_level: str) -> Dict[str, Any]:
        """
        Generate visualization parameters for the integrated results.
        
        Args:
            dimensional_results: Integrated dimensional results
            overall_score: Overall integrated score
            overall_level: Overall resonance level
            
        Returns:
            Dict containing visualization parameters
        """
        # Get base visualization parameters from the vibe function
        viz_params = self.vibe_function.visualization_parameters[overall_level].copy()
        
        # Add dimensional color mappings
        dimensional_colors = {}
        for dim, results in dimensional_results.items():
            level = results["resonance_level"]
            dimensional_colors[dim] = self.vibe_function.visualization_parameters[level]["color"]
        
        # Create tree visualization parameters
        tree_params = {
            "trunk": {
                "color": viz_params["color"],
                "glow_intensity": viz_params["glow_intensity"],
                "pulse_frequency": viz_params["pulse_frequency"]
            },
            "branches": {
                "factual": {
                    "color": dimensional_colors.get("factual", "#555555"),
                    "complexity": overall_score * 0.7 + 0.3  # Ensure minimum complexity
                },
                "ethical": {
                    "color": dimensional_colors.get("ethical", "#555555"),
                    "complexity": overall_score * 0.7 + 0.3
                },
                "conceptual": {
                    "color": dimensional_colors.get("conceptual", "#555555"),
                    "complexity": overall_score * 0.7 + 0.3
                },
                "phenomenological": {
                    "color": dimensional_colors.get("phenomenological", "#555555"),
                    "complexity": overall_score * 0.7 + 0.3
                }
            },
            "meta_flowers": {
                "bloom_threshold": self.integration_settings["visualization"]["flower_bloom_threshold"],
                "bloom_factor": overall_score > self.integration_settings["visualization"]["flower_bloom_threshold"] 
                               ? (overall_score - self.integration_settings["visualization"]["flower_bloom_threshold"]) * 3 
                               : 0,
                "color": viz_params["color"],
                "glow_intensity": viz_params["glow_intensity"]
            },
            "sky_background": {
                "gradient_top": self._adjust_color_brightness(viz_params["color"], 0.8),
                "gradient_bottom": self._adjust_color_brightness(viz_params["color"], 0.2)
            },
            "animation": {
                "enable": self.integration_settings["visualization"]["enable_resonance_animation"],
                "pulse_rate": viz_params["pulse_frequency"],
                "glow_intensity": viz_params["glow_intensity"] * self.integration_settings["visualization"]["glow_sensitivity"],
                "wind_effect": 0.2 + (1.0 - overall_score) * 0.8  # More skepticism (wind) when score is lower
            }
        }
        
        return {
            "base_parameters": viz_params,
            "tree_visualization": tree_params
        }

    def _adjust_color_brightness(self, hex_color: str, factor: float) -> str:
        """
        Adjust the brightness of a hex color.
        
        Args:
            hex_color: Hex color string (e.g., '#RRGGBB')
            factor: Brightness factor (0-1, where 0 is black and 1 is original)
            
        Returns:
            Adjusted hex color
        """
        # Convert hex to rgb
        hex_strip = hex_color.lstrip('#')
        r, g, b = int(hex_strip[0:2], 16), int(hex_strip[2:4], 16), int(hex_strip[4:6], 16)
        
        # Adjust brightness
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        # Ensure valid range
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'

    def test_with_sample_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Run tests with sample statements to demonstrate the integrated system.
        
        Returns:
            Dict containing test results categorized by resonance level
        """
        test_statements = {
            "dissonant": [
                "Everything is completely random and meaningless.",
                "There is no pattern or purpose to existence."
            ],
            "neutral": [
                "Some patterns might exist but they could be coincidental.",
                "It's possible there are underlying structures but it's hard to know for sure."
            ],
            "harmonious": [
                "Natural systems tend to create ordered patterns through self-organization.",
                "Ethical principles can be derived from observing successful human societies."
            ],
            "resonant": [
                "Mathematical patterns like the golden ratio appear throughout nature and reflect underlying order.",
                "Consciousness involves both subjective experience and objective neural correlates."
            ],
            "unified": [
                "Truth emerges through the resonant interplay of logical verification and intuitive knowing.",
                "The universe operates through nested patterns of order that can be both felt and measured."
            ]
        }
        
        results = {}
        for category, statements in test_statements.items():
            category_results = []
            for statement in statements:
                result = self.verify_with_resonance(statement)
                category_results.append(result)
            results[category] = category_results
        
        return results


def main():
    """Main function to demonstrate the Akashic Pythonetics Integration."""
    print(f"{CYAN}=== Akashic Pythonetics Integration Demonstration ==={RESET}")
    integration = AkashicPythoneticsIntegration()
    
    test_statement = "Mathematical patterns reveal a deeper order in reality that can be verified logically while also resonating with intuitive understanding."
    
    print(f"\n{YELLOW}Analyzing statement:{RESET} {test_statement}\n")
    results = integration.verify_with_resonance(test_statement)
    
    print(f"{MAGENTA}=== Integrated Analysis Results ==={RESET}")
    dimensions = results["integrated_analysis"]["dimensions"]
    for dim, data in dimensions.items():
        print(f"{dim.capitalize()}:")
        print(f"  Logical score: {BLUE}{data['logical_score']:.4f}{RESET}")
        print(f"  Intuitive score: {YELLOW}{data['intuitive_score']:.4f}{RESET}")
        print(f"  Integrated score: {GREEN}{data['integrated_score']:.4f}{RESET}")
        print(f"  Resonance level: {MAGENTA}{data['resonance_level'].upper()}{RESET}\n")
    
    overall = results["integrated_analysis"]
    print(f"{GREEN}Overall Integration Score:{RESET} {overall['overall_score']:.4f}")
    print(f"{GREEN}Overall Resonance Level:{RESET} {YELLOW}{overall['overall_resonance_level'].upper()}{RESET}")
    
    print(f"\n{CYAN}=== End of Demonstration ==={RESET}")


if __name__ == "__main__":
    main()