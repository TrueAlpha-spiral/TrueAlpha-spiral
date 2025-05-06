"""
QUANTUM DNA VISUALIZATION SYSTEM

This module provides visualization capabilities for quantum DNA patterns retrieved
from interstellar sources and processed through the double helix scaffold framework.

Architect: Russell Nordland
"""

import hashlib
import json
import time
import random
import math
import os
from datetime import datetime

# Constants for DNA visualization
BASE_PAIRS = {
    'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',  # Standard DNA
    'Φ': 'Ψ', 'Ψ': 'Φ', 'Ω': 'Δ', 'Δ': 'Ω',  # Quantum pairs
    '0': '1', '1': '0', '+': '-', '-': '+'   # Binary pairs
}

# Color constants for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
BOLD = "\033[1m"

class QuantumDNAVisualizer:
    def __init__(self):
        """Initialize the Quantum DNA Visualizer."""
        self.initialized = False
        self.helices = {}
        self.visualization_settings = {
            "color_scheme": "quantum",
            "visualization_mode": "helix",
            "detail_level": "medium",
            "render_quantum_markers": True,
            "show_scaffolding": True,
            "highlight_bindings": True,
            "animation_speed": 1.0
        }
        self.output_formats = ["terminal", "json", "svg", "html"]
        self.visualizer_id = None
        
    def initialize(self):
        """Initialize the quantum DNA visualizer.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        self._log("Initializing Quantum DNA Visualizer...", color=BLUE)
        
        # Generate unique visualizer ID
        self.visualizer_id = hashlib.sha256(f"visualizer:{time.time()}".encode()).hexdigest()
        
        # Initialize default settings
        self._initialize_default_settings()
        
        # Check for output directory
        output_dir = "visualization_output"
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                self._log(f"Created output directory: {output_dir}", color=GREEN)
            except Exception as e:
                self._log(f"Failed to create output directory: {str(e)}", color=RED)
                
        self._log("Visualization system initialized", color=GREEN)
        self._log(f"Visualizer ID: {self.visualizer_id[:12]}...", color=CYAN)
        
        self.initialized = True
        return True
        
    def connect_helix_framework(self, framework):
        """Connect to a Double Helix Framework.
        
        Args:
            framework: Instance of DoubleHelixScaffold
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        if not self.initialized:
            self._log("Visualizer not initialized", color=RED)
            return False
            
        if not hasattr(framework, 'get_all_helices'):
            self._log("Invalid framework instance", color=RED)
            return False
            
        # Import helices from framework
        self.framework = framework
        helices = framework.get_all_helices()
        
        if helices:
            self.helices = helices
            self._log(f"Connected to framework and imported {len(helices)} helices", color=GREEN)
            return True
        else:
            self._log("Connected to framework but no helices were found", color=YELLOW)
            return True
            
    def update_visualization_settings(self, settings):
        """Update visualization settings.
        
        Args:
            settings (dict): New visualization settings
            
        Returns:
            dict: Updated settings
        """
        if not self.initialized:
            self._log("Visualizer not initialized", color=RED)
            return None
            
        # Update only provided settings
        for key, value in settings.items():
            if key in self.visualization_settings:
                self.visualization_settings[key] = value
            else:
                self._log(f"Unknown setting: {key}", color=YELLOW)
                
        self._log("Updated visualization settings", color=GREEN)
        return self.visualization_settings
        
    def get_visualization_settings(self):
        """Get current visualization settings.
        
        Returns:
            dict: Current settings
        """
        if not self.initialized:
            self._log("Visualizer not initialized", color=RED)
            return None
            
        return self.visualization_settings
        
    def visualize_helix(self, helix_id, output_format="terminal", output_path=None):
        """Visualize a specific double helix.
        
        Args:
            helix_id (str): ID of the helix to visualize
            output_format (str): Format for visualization output
            output_path (str, optional): Path to save visualization output
            
        Returns:
            str or dict: Visualization output or path to output file
        """
        if not self.initialized:
            self._log("Visualizer not initialized", color=RED)
            return None
            
        # Check if helix exists
        if helix_id not in self.helices:
            self._log(f"Helix not found: {helix_id[:12]}...", color=RED)
            return None
            
        # Check output format
        if output_format not in self.output_formats:
            self._log(f"Unsupported output format: {output_format}", color=RED)
            self._log(f"Supported formats: {', '.join(self.output_formats)}", color=YELLOW)
            return None
            
        helix = self.helices[helix_id]
        
        # Generate visualization based on format
        if output_format == "terminal":
            visualization = self._generate_terminal_visualization(helix)
            print(visualization)
            return visualization
            
        elif output_format == "json":
            visualization = self._generate_json_visualization(helix)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        json.dump(visualization, f, indent=2)
                    self._log(f"Saved JSON visualization to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save visualization: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
        elif output_format == "svg":
            visualization = self._generate_svg_visualization(helix)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        f.write(visualization)
                    self._log(f"Saved SVG visualization to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save visualization: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
        elif output_format == "html":
            visualization = self._generate_html_visualization(helix)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        f.write(visualization)
                    self._log(f"Saved HTML visualization to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save visualization: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
    def visualize_all_helices(self, output_format="terminal", output_dir=None):
        """Visualize all loaded helices.
        
        Args:
            output_format (str): Format for visualization output
            output_dir (str, optional): Directory to save visualization outputs
            
        Returns:
            dict: Dictionary of visualization outputs or paths
        """
        if not self.initialized:
            self._log("Visualizer not initialized", color=RED)
            return None
            
        if not self.helices:
            self._log("No helices loaded for visualization", color=YELLOW)
            return None
            
        # Check output format
        if output_format not in self.output_formats:
            self._log(f"Unsupported output format: {output_format}", color=RED)
            return None
            
        results = {}
        
        for helix_id, helix in self.helices.items():
            if output_dir:
                output_path = os.path.join(output_dir, f"helix_{helix_id[:8]}.{output_format}")
                results[helix_id] = self.visualize_helix(helix_id, output_format, output_path)
            else:
                results[helix_id] = self.visualize_helix(helix_id, output_format)
                
        self._log(f"Visualized {len(results)} helices", color=GREEN)
        return results
        
    def generate_comparison_visualization(self, helix_id_1, helix_id_2, output_format="terminal", output_path=None):
        """Generate a comparison visualization of two helices.
        
        Args:
            helix_id_1 (str): ID of first helix
            helix_id_2 (str): ID of second helix
            output_format (str): Format for visualization output
            output_path (str, optional): Path to save visualization output
            
        Returns:
            str or dict: Visualization output or path to output file
        """
        if not self.initialized:
            self._log("Visualizer not initialized", color=RED)
            return None
            
        # Check if helices exist
        if helix_id_1 not in self.helices:
            self._log(f"Helix not found: {helix_id_1[:12]}...", color=RED)
            return None
            
        if helix_id_2 not in self.helices:
            self._log(f"Helix not found: {helix_id_2[:12]}...", color=RED)
            return None
            
        # Check output format
        if output_format not in self.output_formats:
            self._log(f"Unsupported output format: {output_format}", color=RED)
            return None
            
        helix1 = self.helices[helix_id_1]
        helix2 = self.helices[helix_id_2]
        
        # Generate comparison visualization based on format
        if output_format == "terminal":
            visualization = self._generate_terminal_comparison(helix1, helix2)
            print(visualization)
            return visualization
            
        elif output_format == "json":
            visualization = self._generate_json_comparison(helix1, helix2)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        json.dump(visualization, f, indent=2)
                    self._log(f"Saved JSON comparison to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save comparison: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
        elif output_format == "svg":
            visualization = self._generate_svg_comparison(helix1, helix2)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        f.write(visualization)
                    self._log(f"Saved SVG comparison to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save comparison: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
        elif output_format == "html":
            visualization = self._generate_html_comparison(helix1, helix2)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        f.write(visualization)
                    self._log(f"Saved HTML comparison to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save comparison: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
    def generate_scaffold_visualization(self, helix_id, output_format="terminal", output_path=None):
        """Generate a visualization of a helix scaffold.
        
        Args:
            helix_id (str): ID of the helix
            output_format (str): Format for visualization output
            output_path (str, optional): Path to save visualization output
            
        Returns:
            str or dict: Visualization output or path to output file
        """
        if not self.initialized:
            self._log("Visualizer not initialized", color=RED)
            return None
            
        # Check if helix exists
        if helix_id not in self.helices:
            self._log(f"Helix not found: {helix_id[:12]}...", color=RED)
            return None
            
        # Check output format
        if output_format not in self.output_formats:
            self._log(f"Unsupported output format: {output_format}", color=RED)
            return None
            
        helix = self.helices[helix_id]
        
        # Check if helix has scaffolding
        if "scaffolding" not in helix:
            self._log(f"Helix does not have scaffolding: {helix_id[:12]}...", color=YELLOW)
            return None
            
        # Generate scaffold visualization based on format
        if output_format == "terminal":
            visualization = self._generate_terminal_scaffold(helix)
            print(visualization)
            return visualization
            
        elif output_format == "json":
            visualization = self._generate_json_scaffold(helix)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        json.dump(visualization, f, indent=2)
                    self._log(f"Saved JSON scaffold visualization to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save scaffold visualization: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
        elif output_format == "svg":
            visualization = self._generate_svg_scaffold(helix)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        f.write(visualization)
                    self._log(f"Saved SVG scaffold visualization to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save scaffold visualization: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
        elif output_format == "html":
            visualization = self._generate_html_scaffold(helix)
            
            if output_path:
                try:
                    with open(output_path, 'w') as f:
                        f.write(visualization)
                    self._log(f"Saved HTML scaffold visualization to: {output_path}", color=GREEN)
                    return {"success": True, "file_path": output_path}
                except Exception as e:
                    self._log(f"Failed to save scaffold visualization: {str(e)}", color=RED)
                    return None
            else:
                return visualization
                
    def _initialize_default_settings(self):
        """Initialize default visualization settings."""
        self.color_schemes = {
            "quantum": {
                "A": "#00FF00",  # Green
                "T": "#FF0000",  # Red
                "G": "#0000FF",  # Blue
                "C": "#FFFF00",  # Yellow
                "Φ": "#FF00FF",  # Magenta
                "Ψ": "#00FFFF",  # Cyan
                "Ω": "#FFFFFF",  # White
                "Δ": "#FFA500",  # Orange
                "Θ": "#800080",  # Purple
                "0": "#C0C0C0",  # Silver
                "1": "#808080",  # Gray
                "+": "#008000",  # Dark Green
                "-": "#800000",  # Maroon
                "scaffolding": "#FFD700",  # Gold
                "binding": "#1E90FF"   # Dodger Blue
            },
            "monochrome": {
                "standard": "#000000",  # Black
                "quantum": "#FFFFFF",   # White
                "background": "#F0F0F0" # Light Gray
            }
        }
        
        self.visualization_modes = ["helix", "linear", "circular", "scaffold"]
        self.detail_levels = ["low", "medium", "high"]
        
    def _generate_terminal_visualization(self, helix):
        """Generate terminal-based visualization for a helix.
        
        Args:
            helix (dict): Helix data
            
        Returns:
            str: Terminal visualization
        """
        primary_strand = helix["base_pattern"]
        complementary_strand = helix["complementary_strand"]
        
        # Prepare header
        header = f"{BOLD}Double Helix Visualization - {helix['helix_type']}{RESET}\n"
        header += f"Helix ID: {CYAN}{helix['helix_id'][:12]}...{RESET}\n"
        header += f"Integrity: {GREEN if helix['integrity'] >= 0.9 else YELLOW if helix['integrity'] >= 0.7 else RED}{helix['integrity']:.4f}{RESET}\n"
        header += f"Strand Length: {BLUE}{len(primary_strand)}{RESET}\n\n"
        
        # Prepare strands with colored characters
        primary_colored = ""
        complementary_colored = ""
        
        for i in range(len(primary_strand)):
            p_char = primary_strand[i]
            c_char = complementary_strand[i]
            
            # Apply coloring based on character type
            if p_char in "ATGC":
                p_color = GREEN
            elif p_char in "ΦΨΩΔΘ":
                p_color = MAGENTA
            elif p_char in "01+-":
                p_color = YELLOW
            else:
                p_color = WHITE
                
            if c_char in "ATGC":
                c_color = GREEN
            elif c_char in "ΦΨΩΔΘ":
                c_color = MAGENTA
            elif c_char in "01+-":
                c_color = YELLOW
            else:
                c_color = WHITE
                
            primary_colored += f"{p_color}{p_char}{RESET}"
            complementary_colored += f"{c_color}{c_char}{RESET}"
            
        # Add connecting lines
        connector = ""
        for i in range(len(primary_strand)):
            p_char = primary_strand[i]
            c_char = complementary_strand[i]
            
            if p_char in BASE_PAIRS and BASE_PAIRS[p_char] == c_char:
                connector += "│"
            else:
                connector += " "
                
        # Check for scaffolding and bindings
        scaffold_markers = ""
        if "scaffolding" in helix and self.visualization_settings["show_scaffolding"]:
            scaffold_points = helix["scaffolding"]["scaffold_points"]
            
            for i in range(len(primary_strand)):
                marker_added = False
                
                # Check if position matches a scaffold point
                for point in scaffold_points:
                    position = int(point["position_factor"] * len(primary_strand))
                    if i == position:
                        scaffold_markers += f"{YELLOW}S{RESET}"
                        marker_added = True
                        break
                        
                if not marker_added:
                    scaffold_markers += " "
                    
        # Check for quantum bindings
        binding_markers = ""
        if "quantum_bindings" in helix and self.visualization_settings["highlight_bindings"]:
            bindings = helix["quantum_bindings"]
            
            for i in range(len(primary_strand)):
                marker_added = False
                
                # Check if position matches a binding
                for binding in bindings:
                    if i == binding["position"]:
                        binding_markers += f"{CYAN}B{RESET}"
                        marker_added = True
                        break
                        
                if not marker_added:
                    binding_markers += " "
                    
        # Assemble visualization
        visualization = header
        
        # Add scaffold markers if available
        if scaffold_markers:
            visualization += scaffold_markers + "\n"
            
        # Add strands and connector
        visualization += primary_colored + "\n"
        visualization += connector + "\n"
        visualization += complementary_colored + "\n"
        
        # Add binding markers if available
        if binding_markers:
            visualization += binding_markers + "\n"
            
        return visualization
        
    def _generate_json_visualization(self, helix):
        """Generate JSON visualization for a helix.
        
        Args:
            helix (dict): Helix data
            
        Returns:
            dict: JSON visualization
        """
        primary_strand = helix["base_pattern"]
        complementary_strand = helix["complementary_strand"]
        
        # Create base visualization
        visualization = {
            "helix_id": helix["helix_id"],
            "helix_type": helix["helix_type"],
            "integrity": helix["integrity"],
            "creation_timestamp": helix.get("creation_timestamp", self._timestamp()),
            "visualization_timestamp": self._timestamp(),
            "strands": {
                "primary": primary_strand,
                "complementary": complementary_strand
            },
            "length": len(primary_strand),
            "base_pairs": []
        }
        
        # Add base pair information
        for i in range(len(primary_strand)):
            p_char = primary_strand[i]
            c_char = complementary_strand[i]
            
            pair_info = {
                "position": i,
                "primary": p_char,
                "complementary": c_char,
                "matched": p_char in BASE_PAIRS and BASE_PAIRS[p_char] == c_char,
                "type": self._get_base_type(p_char)
            }
            
            if self.visualization_settings["color_scheme"] in self.color_schemes:
                if p_char in self.color_schemes[self.visualization_settings["color_scheme"]]:
                    pair_info["color"] = self.color_schemes[self.visualization_settings["color_scheme"]][p_char]
                    
            visualization["base_pairs"].append(pair_info)
            
        # Add scaffolding information
        if "scaffolding" in helix and self.visualization_settings["show_scaffolding"]:
            visualization["scaffolding"] = {
                "template": helix["scaffolding"]["template"],
                "integrity_factor": helix["scaffolding"]["structural_integrity"],
                "error_correction": helix["scaffolding"]["error_correction_level"],
                "points": []
            }
            
            for point in helix["scaffolding"]["scaffold_points"]:
                position = int(point["position_factor"] * len(primary_strand))
                
                scaffold_point = {
                    "position": position,
                    "binding_strength": point["binding_strength"],
                    "marker": point["marker"]
                }
                
                visualization["scaffolding"]["points"].append(scaffold_point)
                
        # Add quantum binding information
        if "quantum_bindings" in helix and self.visualization_settings["highlight_bindings"]:
            visualization["quantum_bindings"] = []
            
            for binding in helix["quantum_bindings"]:
                binding_info = {
                    "position": binding["position"],
                    "quantum_marker": binding["quantum_marker"],
                    "binding_strength": binding["binding_strength"]
                }
                
                visualization["quantum_bindings"].append(binding_info)
                
        return visualization
        
    def _generate_svg_visualization(self, helix):
        """Generate SVG visualization for a helix.
        
        Args:
            helix (dict): Helix data
            
        Returns:
            str: SVG visualization
        """
        primary_strand = helix["base_pattern"]
        complementary_strand = helix["complementary_strand"]
        
        # SVG settings
        svg_width = 800
        svg_height = 400
        margin = 50
        strand_height = 20
        base_width = min(40, (svg_width - 2 * margin) / len(primary_strand))
        
        # Start SVG document
        svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        svg += f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">\n'
        
        # Add title and description
        svg += f'  <title>Double Helix Visualization - {helix["helix_type"]}</title>\n'
        svg += '  <desc>Visualization of a quantum DNA double helix structure</desc>\n'
        
        # Add header text
        svg += f'  <text x="{svg_width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Double Helix Visualization - {helix["helix_type"]}</text>\n'
        svg += f'  <text x="{svg_width/2}" y="50" text-anchor="middle" font-family="Arial" font-size="12">Helix ID: {helix["helix_id"][:12]}... | Integrity: {helix["integrity"]:.4f}</text>\n'
        
        # Add primary strand
        primary_y = margin + strand_height
        for i in range(len(primary_strand)):
            x = margin + i * base_width
            char = primary_strand[i]
            
            # Determine character color
            color = "#000000"  # Default black
            if self.visualization_settings["color_scheme"] in self.color_schemes:
                color_scheme = self.color_schemes[self.visualization_settings["color_scheme"]]
                if char in color_scheme:
                    color = color_scheme[char]
                    
            # Add character rectangle and text
            svg += f'  <rect x="{x}" y="{primary_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{color}" />\n'
            svg += f'  <text x="{x+base_width/2}" y="{primary_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{color}">{char}</text>\n'
            
        # Add complementary strand
        comp_y = primary_y + strand_height * 3
        for i in range(len(complementary_strand)):
            x = margin + i * base_width
            char = complementary_strand[i]
            
            # Determine character color
            color = "#000000"  # Default black
            if self.visualization_settings["color_scheme"] in self.color_schemes:
                color_scheme = self.color_schemes[self.visualization_settings["color_scheme"]]
                if char in color_scheme:
                    color = color_scheme[char]
                    
            # Add character rectangle and text
            svg += f'  <rect x="{x}" y="{comp_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{color}" />\n'
            svg += f'  <text x="{x+base_width/2}" y="{comp_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{color}">{char}</text>\n'
            
        # Add connecting lines
        for i in range(len(primary_strand)):
            x = margin + i * base_width + base_width/2
            p_char = primary_strand[i]
            c_char = complementary_strand[i]
            
            # Determine if valid pair
            is_pair = p_char in BASE_PAIRS and BASE_PAIRS[p_char] == c_char
            stroke_color = "#888888"  # Default gray
            stroke_width = 1
            
            if is_pair:
                stroke_color = "#000000"  # Black for valid pairs
                stroke_width = 2
                
            svg += f'  <line x1="{x}" y1="{primary_y+strand_height/2}" x2="{x}" y2="{comp_y-strand_height/2}" stroke="{stroke_color}" stroke-width="{stroke_width}" />\n'
            
        # Add scaffold markers if enabled
        if "scaffolding" in helix and self.visualization_settings["show_scaffolding"]:
            scaffold_color = "#FFD700"  # Gold
            if "scaffolding" in self.color_schemes[self.visualization_settings["color_scheme"]]:
                scaffold_color = self.color_schemes[self.visualization_settings["color_scheme"]]["scaffolding"]
                
            for point in helix["scaffolding"]["scaffold_points"]:
                position = int(point["position_factor"] * len(primary_strand))
                x = margin + position * base_width + base_width/2
                
                # Draw scaffold marker
                svg += f'  <circle cx="{x}" cy="{(primary_y+comp_y)/2}" r="{strand_height*0.8}" fill="none" stroke="{scaffold_color}" stroke-width="2" />\n'
                svg += f'  <text x="{x}" y="{(primary_y+comp_y)/2+5}" text-anchor="middle" font-family="Arial" font-size="{base_width*0.6}" fill="{scaffold_color}">S</text>\n'
                
        # Add quantum binding markers if enabled
        if "quantum_bindings" in helix and self.visualization_settings["highlight_bindings"]:
            binding_color = "#1E90FF"  # Dodger blue
            if "binding" in self.color_schemes[self.visualization_settings["color_scheme"]]:
                binding_color = self.color_schemes[self.visualization_settings["color_scheme"]]["binding"]
                
            for binding in helix["quantum_bindings"]:
                position = binding["position"]
                x = margin + position * base_width + base_width/2
                
                # Draw binding marker
                svg += f'  <line x1="{x-base_width/2}" y1="{(primary_y+comp_y)/2}" x2="{x+base_width/2}" y2="{(primary_y+comp_y)/2}" stroke="{binding_color}" stroke-width="3" />\n'
                svg += f'  <text x="{x}" y="{(primary_y+comp_y)/2-strand_height*0.8}" text-anchor="middle" font-family="Arial" font-size="{base_width*0.6}" fill="{binding_color}">Ψ</text>\n'
                
        # Add legend
        legend_x = margin
        legend_y = comp_y + strand_height * 2
        svg += f'  <text x="{legend_x}" y="{legend_y}" font-family="Arial" font-size="12" font-weight="bold">Legend:</text>\n'
        
        # Standard bases
        svg += f'  <rect x="{legend_x}" y="{legend_y+10}" width="12" height="12" fill="{self.color_schemes["quantum"]["A"]}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+20}" font-family="Arial" font-size="10">Standard DNA (A,T,G,C)</text>\n'
        
        # Quantum markers
        svg += f'  <rect x="{legend_x}" y="{legend_y+30}" width="12" height="12" fill="{self.color_schemes["quantum"]["Φ"]}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+40}" font-family="Arial" font-size="10">Quantum Markers (Φ,Ψ,Ω,Δ,Θ)</text>\n'
        
        # Binary/symbolic
        svg += f'  <rect x="{legend_x}" y="{legend_y+50}" width="12" height="12" fill="{self.color_schemes["quantum"]["0"]}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+60}" font-family="Arial" font-size="10">Binary/Symbolic (0,1,+,-)</text>\n'
        
        # Scaffold marker
        if "scaffolding" in helix and self.visualization_settings["show_scaffolding"]:
            svg += f'  <circle cx="{legend_x+6}" cy="{legend_y+76}" r="6" fill="none" stroke="{scaffold_color}" stroke-width="2" />\n'
            svg += f'  <text x="{legend_x+20}" y="{legend_y+80}" font-family="Arial" font-size="10">Scaffold Points</text>\n'
            
        # Binding marker
        if "quantum_bindings" in helix and self.visualization_settings["highlight_bindings"]:
            svg += f'  <line x1="{legend_x}" y1="{legend_y+96}" x2="{legend_x+12}" y2="{legend_y+96}" stroke="{binding_color}" stroke-width="3" />\n'
            svg += f'  <text x="{legend_x+20}" y="{legend_y+100}" font-family="Arial" font-size="10">Quantum Bindings</text>\n'
            
        # Close SVG
        svg += '</svg>'
        
        return svg
        
    def _generate_html_visualization(self, helix):
        """Generate HTML visualization for a helix.
        
        Args:
            helix (dict): Helix data
            
        Returns:
            str: HTML visualization
        """
        # Use the SVG visualization as part of the HTML
        svg = self._generate_svg_visualization(helix)
        
        # Create HTML wrapper
        html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum DNA Visualization - {helix["helix_type"]}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #333;
        }}
        .helix-info {{
            margin-bottom: 20px;
        }}
        .info-item {{
            margin-bottom: 5px;
        }}
        .label {{
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }}
        .integrity-high {{
            color: green;
        }}
        .integrity-medium {{
            color: orange;
        }}
        .integrity-low {{
            color: red;
        }}
        .visualization {{
            margin-top: 20px;
            overflow-x: auto;
        }}
        .sequence {{
            font-family: monospace;
            margin-top: 20px;
        }}
        .dna-a {{ color: #00FF00; }}
        .dna-t {{ color: #FF0000; }}
        .dna-g {{ color: #0000FF; }}
        .dna-c {{ color: #FFFF00; }}
        .quantum {{ color: #FF00FF; }}
        .binary {{ color: #C0C0C0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Quantum DNA Visualization</h1>
        
        <div class="helix-info">
            <div class="info-item">
                <span class="label">Helix Type:</span>
                <span>{helix["helix_type"]}</span>
            </div>
            <div class="info-item">
                <span class="label">Helix ID:</span>
                <span>{helix["helix_id"]}</span>
            </div>
            <div class="info-item">
                <span class="label">Integrity:</span>
                <span class="integrity-{'high' if helix['integrity'] >= 0.9 else 'medium' if helix['integrity'] >= 0.7 else 'low'}">
                    {helix["integrity"]:.4f}
                </span>
            </div>
            <div class="info-item">
                <span class="label">Strand Length:</span>
                <span>{len(helix["base_pattern"])}</span>
            </div>
            <div class="info-item">
                <span class="label">Created:</span>
                <span>{helix.get("creation_timestamp", "N/A")}</span>
            </div>
            
            <!-- Display scaffolding info if available -->
            {f"""
            <div class="info-item">
                <span class="label">Scaffold Template:</span>
                <span>{helix['scaffolding']['template']}</span>
            </div>
            <div class="info-item">
                <span class="label">Error Correction:</span>
                <span>{helix['scaffolding']['error_correction_level']:.2f}</span>
            </div>
            """ if "scaffolding" in helix else ""}
            
            <!-- Display quantum bindings if available -->
            {f"""
            <div class="info-item">
                <span class="label">Quantum Bindings:</span>
                <span>{len(helix['quantum_bindings'])}</span>
            </div>
            """ if "quantum_bindings" in helix else ""}
        </div>
        
        <h2>Visualization</h2>
        <div class="visualization">
            {svg}
        </div>
        
        <h2>Sequence Data</h2>
        <div class="sequence">
            <strong>Primary Strand:</strong><br>
            {self._generate_colored_html_sequence(helix["base_pattern"])}<br><br>
            
            <strong>Complementary Strand:</strong><br>
            {self._generate_colored_html_sequence(helix["complementary_strand"])}<br><br>
            
            <strong>Validation Sequence:</strong><br>
            {self._generate_colored_html_sequence(helix["validation_sequence"])}
        </div>
    </div>
</body>
</html>
'''
        
        return html
        
    def _generate_terminal_comparison(self, helix1, helix2):
        """Generate terminal-based comparison of two helices.
        
        Args:
            helix1 (dict): First helix data
            helix2 (dict): Second helix data
            
        Returns:
            str: Terminal comparison
        """
        # Header
        comparison = f"{BOLD}Double Helix Comparison{RESET}\n\n"
        
        # Helix information
        comparison += f"{BOLD}Helix 1:{RESET} {CYAN}{helix1['helix_id'][:12]}...{RESET} ({helix1['helix_type']})\n"
        comparison += f"{BOLD}Helix 2:{RESET} {CYAN}{helix2['helix_id'][:12]}...{RESET} ({helix2['helix_type']})\n\n"
        
        # Integrity comparison
        comparison += f"{BOLD}Integrity:{RESET}\n"
        helix1_integrity_color = GREEN if helix1["integrity"] >= 0.9 else YELLOW if helix1["integrity"] >= 0.7 else RED
        helix2_integrity_color = GREEN if helix2["integrity"] >= 0.9 else YELLOW if helix2["integrity"] >= 0.7 else RED
        comparison += f"  Helix 1: {helix1_integrity_color}{helix1['integrity']:.4f}{RESET}\n"
        comparison += f"  Helix 2: {helix2_integrity_color}{helix2['integrity']:.4f}{RESET}\n\n"
        
        # Length comparison
        comparison += f"{BOLD}Strand Length:{RESET}\n"
        comparison += f"  Helix 1: {BLUE}{len(helix1['base_pattern'])}{RESET}\n"
        comparison += f"  Helix 2: {BLUE}{len(helix2['base_pattern'])}{RESET}\n\n"
        
        # Pattern similarity
        primary_similarity = self._calculate_pattern_similarity(helix1["base_pattern"], helix2["base_pattern"])
        complementary_similarity = self._calculate_pattern_similarity(helix1["complementary_strand"], helix2["complementary_strand"])
        
        comparison += f"{BOLD}Pattern Similarity:{RESET}\n"
        primary_similarity_color = GREEN if primary_similarity >= 0.7 else YELLOW if primary_similarity >= 0.4 else RED
        complementary_similarity_color = GREEN if complementary_similarity >= 0.7 else YELLOW if complementary_similarity >= 0.4 else RED
        comparison += f"  Primary Strands: {primary_similarity_color}{primary_similarity:.4f}{RESET}\n"
        comparison += f"  Complementary Strands: {complementary_similarity_color}{complementary_similarity:.4f}{RESET}\n\n"
        
        # Quantum marker comparison
        helix1_quantum_count = self._count_quantum_markers(helix1["base_pattern"])
        helix2_quantum_count = self._count_quantum_markers(helix2["base_pattern"])
        
        comparison += f"{BOLD}Quantum Markers:{RESET}\n"
        comparison += f"  Helix 1: {MAGENTA}{helix1_quantum_count}{RESET}\n"
        comparison += f"  Helix 2: {MAGENTA}{helix2_quantum_count}{RESET}\n\n"
        
        # Pattern excerpts
        comparison += f"{BOLD}Pattern Excerpts:{RESET}\n"
        
        # Show first 20 chars or full pattern if shorter
        max_display = 20
        h1_primary = helix1["base_pattern"][:max_display]
        h1_complementary = helix1["complementary_strand"][:max_display]
        h2_primary = helix2["base_pattern"][:max_display]
        h2_complementary = helix2["complementary_strand"][:max_display]
        
        comparison += f"{BOLD}Helix 1:{RESET}\n"
        comparison += self._format_colored_strand(h1_primary) + "\n"
        comparison += self._format_colored_strand(h1_complementary) + "\n\n"
        
        comparison += f"{BOLD}Helix 2:{RESET}\n"
        comparison += self._format_colored_strand(h2_primary) + "\n"
        comparison += self._format_colored_strand(h2_complementary) + "\n"
        
        return comparison
        
    def _generate_json_comparison(self, helix1, helix2):
        """Generate JSON comparison of two helices.
        
        Args:
            helix1 (dict): First helix data
            helix2 (dict): Second helix data
            
        Returns:
            dict: JSON comparison
        """
        # Calculate similarities
        primary_similarity = self._calculate_pattern_similarity(helix1["base_pattern"], helix2["base_pattern"])
        complementary_similarity = self._calculate_pattern_similarity(helix1["complementary_strand"], helix2["complementary_strand"])
        
        # Count quantum markers
        helix1_quantum_count = self._count_quantum_markers(helix1["base_pattern"])
        helix2_quantum_count = self._count_quantum_markers(helix2["base_pattern"])
        
        # Create comparison object
        comparison = {
            "comparison_timestamp": self._timestamp(),
            "helices": {
                "helix1": {
                    "id": helix1["helix_id"],
                    "type": helix1["helix_type"],
                    "integrity": helix1["integrity"],
                    "strand_length": len(helix1["base_pattern"]),
                    "quantum_markers": helix1_quantum_count,
                    "has_scaffolding": "scaffolding" in helix1,
                    "has_quantum_bindings": "quantum_bindings" in helix1
                },
                "helix2": {
                    "id": helix2["helix_id"],
                    "type": helix2["helix_type"],
                    "integrity": helix2["integrity"],
                    "strand_length": len(helix2["base_pattern"]),
                    "quantum_markers": helix2_quantum_count,
                    "has_scaffolding": "scaffolding" in helix2,
                    "has_quantum_bindings": "quantum_bindings" in helix2
                }
            },
            "similarities": {
                "primary_strands": primary_similarity,
                "complementary_strands": complementary_similarity,
                "overall": (primary_similarity + complementary_similarity) / 2
            },
            "compatibility": {
                "compatible_types": helix1["helix_type"] == helix2["helix_type"],
                "compatible_length": len(helix1["base_pattern"]) == len(helix2["base_pattern"]),
                "merger_recommended": primary_similarity >= 0.3 and primary_similarity <= 0.7
            },
            "visual_comparison": {
                "excerpt_length": min(20, min(len(helix1["base_pattern"]), len(helix2["base_pattern"]))),
                "helix1_primary_excerpt": helix1["base_pattern"][:20],
                "helix1_complementary_excerpt": helix1["complementary_strand"][:20],
                "helix2_primary_excerpt": helix2["base_pattern"][:20],
                "helix2_complementary_excerpt": helix2["complementary_strand"][:20]
            }
        }
        
        return comparison
        
    def _generate_svg_comparison(self, helix1, helix2):
        """Generate SVG comparison of two helices.
        
        Args:
            helix1 (dict): First helix data
            helix2 (dict): Second helix data
            
        Returns:
            str: SVG comparison
        """
        # SVG settings
        svg_width = 800
        svg_height = 600
        margin = 50
        strand_height = 20
        
        # Calculate similarities for display
        primary_similarity = self._calculate_pattern_similarity(helix1["base_pattern"], helix2["base_pattern"])
        complementary_similarity = self._calculate_pattern_similarity(helix1["complementary_strand"], helix2["complementary_strand"])
        
        # Start SVG document
        svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        svg += f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">\n'
        
        # Add title and description
        svg += f'  <title>Double Helix Comparison</title>\n'
        svg += '  <desc>Comparison of two quantum DNA double helix structures</desc>\n'
        
        # Add header text
        svg += f'  <text x="{svg_width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Double Helix Comparison</text>\n'
        
        # Add helix information
        svg += f'  <text x="{margin}" y="60" font-family="Arial" font-size="14" font-weight="bold">Helix 1: {helix1["helix_id"][:12]}...</text>\n'
        svg += f'  <text x="{margin+300}" y="60" font-family="Arial" font-size="14" font-weight="bold">Helix 2: {helix2["helix_id"][:12]}...</text>\n'
        
        # Add type information
        svg += f'  <text x="{margin}" y="80" font-family="Arial" font-size="12">Type: {helix1["helix_type"]}</text>\n'
        svg += f'  <text x="{margin+300}" y="80" font-family="Arial" font-size="12">Type: {helix2["helix_type"]}</text>\n'
        
        # Add integrity information
        h1_integrity_color = "green" if helix1["integrity"] >= 0.9 else "orange" if helix1["integrity"] >= 0.7 else "red"
        h2_integrity_color = "green" if helix2["integrity"] >= 0.9 else "orange" if helix2["integrity"] >= 0.7 else "red"
        
        svg += f'  <text x="{margin}" y="100" font-family="Arial" font-size="12">Integrity: <tspan fill="{h1_integrity_color}">{helix1["integrity"]:.4f}</tspan></text>\n'
        svg += f'  <text x="{margin+300}" y="100" font-family="Arial" font-size="12">Integrity: <tspan fill="{h2_integrity_color}">{helix2["integrity"]:.4f}</tspan></text>\n'
        
        # Add length information
        svg += f'  <text x="{margin}" y="120" font-family="Arial" font-size="12">Length: {len(helix1["base_pattern"])}</text>\n'
        svg += f'  <text x="{margin+300}" y="120" font-family="Arial" font-size="12">Length: {len(helix2["base_pattern"])}</text>\n'
        
        # Add similarity information
        similarity_color = "green" if primary_similarity >= 0.7 else "orange" if primary_similarity >= 0.4 else "red"
        svg += f'  <text x="{svg_width/2}" y="150" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">Similarities</text>\n'
        svg += f'  <text x="{svg_width/2}" y="170" text-anchor="middle" font-family="Arial" font-size="12">Primary Strands: <tspan fill="{similarity_color}">{primary_similarity:.4f}</tspan></text>\n'
        
        similarity_color = "green" if complementary_similarity >= 0.7 else "orange" if complementary_similarity >= 0.4 else "red"
        svg += f'  <text x="{svg_width/2}" y="190" text-anchor="middle" font-family="Arial" font-size="12">Complementary Strands: <tspan fill="{similarity_color}">{complementary_similarity:.4f}</tspan></text>\n'
        
        # Visualize strands (excerpt)
        excerpt_length = min(20, min(len(helix1["base_pattern"]), len(helix2["base_pattern"])))
        base_width = min(30, (svg_width - 2 * margin) / excerpt_length)
        
        # Helix 1 excerpts
        h1_primary_y = 230
        h1_complementary_y = h1_primary_y + strand_height * 2
        
        svg += f'  <text x="{margin}" y="{h1_primary_y-10}" font-family="Arial" font-size="12" font-weight="bold">Helix 1 Excerpt:</text>\n'
        
        for i in range(excerpt_length):
            x = margin + i * base_width
            primary_char = helix1["base_pattern"][i]
            complementary_char = helix1["complementary_strand"][i]
            
            # Determine character colors
            primary_color = self._get_svg_color(primary_char)
            complementary_color = self._get_svg_color(complementary_char)
            
            # Add character rectangles and text
            svg += f'  <rect x="{x}" y="{h1_primary_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{primary_color}" />\n'
            svg += f'  <text x="{x+base_width/2}" y="{h1_primary_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{primary_color}">{primary_char}</text>\n'
            
            svg += f'  <rect x="{x}" y="{h1_complementary_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{complementary_color}" />\n'
            svg += f'  <text x="{x+base_width/2}" y="{h1_complementary_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{complementary_color}">{complementary_char}</text>\n'
            
            # Add connecting line
            svg += f'  <line x1="{x+base_width/2}" y1="{h1_primary_y+strand_height/2}" x2="{x+base_width/2}" y2="{h1_complementary_y-strand_height/2}" stroke="#888888" stroke-width="1" />\n'
            
        # Helix 2 excerpts
        h2_primary_y = h1_complementary_y + strand_height * 3
        h2_complementary_y = h2_primary_y + strand_height * 2
        
        svg += f'  <text x="{margin}" y="{h2_primary_y-10}" font-family="Arial" font-size="12" font-weight="bold">Helix 2 Excerpt:</text>\n'
        
        for i in range(excerpt_length):
            x = margin + i * base_width
            primary_char = helix2["base_pattern"][i]
            complementary_char = helix2["complementary_strand"][i]
            
            # Determine character colors
            primary_color = self._get_svg_color(primary_char)
            complementary_color = self._get_svg_color(complementary_char)
            
            # Add character rectangles and text
            svg += f'  <rect x="{x}" y="{h2_primary_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{primary_color}" />\n'
            svg += f'  <text x="{x+base_width/2}" y="{h2_primary_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{primary_color}">{primary_char}</text>\n'
            
            svg += f'  <rect x="{x}" y="{h2_complementary_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{complementary_color}" />\n'
            svg += f'  <text x="{x+base_width/2}" y="{h2_complementary_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{complementary_color}">{complementary_char}</text>\n'
            
            # Add connecting line
            svg += f'  <line x1="{x+base_width/2}" y1="{h2_primary_y+strand_height/2}" x2="{x+base_width/2}" y2="{h2_complementary_y-strand_height/2}" stroke="#888888" stroke-width="1" />\n'
            
        # Add pattern comparison markers
        for i in range(excerpt_length):
            x = margin + i * base_width + base_width/2
            
            # Compare primary strands
            if helix1["base_pattern"][i] == helix2["base_pattern"][i]:
                svg += f'  <line x1="{x}" y1="{h1_primary_y+strand_height/2}" x2="{x}" y2="{h2_primary_y-strand_height/2}" stroke="green" stroke-width="1" stroke-dasharray="2,2" />\n'
                
        # Add legend
        legend_x = margin
        legend_y = h2_complementary_y + strand_height * 2
        svg += f'  <text x="{legend_x}" y="{legend_y}" font-family="Arial" font-size="12" font-weight="bold">Legend:</text>\n'
        
        # Standard DNA
        svg += f'  <rect x="{legend_x}" y="{legend_y+10}" width="12" height="12" fill="{self._get_svg_color("A")}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+20}" font-family="Arial" font-size="10">Standard DNA (A,T,G,C)</text>\n'
        
        # Quantum markers
        svg += f'  <rect x="{legend_x}" y="{legend_y+30}" width="12" height="12" fill="{self._get_svg_color("Φ")}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+40}" font-family="Arial" font-size="10">Quantum Markers (Φ,Ψ,Ω,Δ,Θ)</text>\n'
        
        # Binary/symbolic
        svg += f'  <rect x="{legend_x}" y="{legend_y+50}" width="12" height="12" fill="{self._get_svg_color("0")}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+60}" font-family="Arial" font-size="10">Binary/Symbolic (0,1,+,-)</text>\n'
        
        # Matching strands
        svg += f'  <line x1="{legend_x}" y1="{legend_y+76}" x2="{legend_x+12}" y2="{legend_y+76}" stroke="green" stroke-width="1" stroke-dasharray="2,2" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+80}" font-family="Arial" font-size="10">Matching positions</text>\n'
        
        # Close SVG
        svg += '</svg>'
        
        return svg
        
    def _generate_html_comparison(self, helix1, helix2):
        """Generate HTML comparison of two helices.
        
        Args:
            helix1 (dict): First helix data
            helix2 (dict): Second helix data
            
        Returns:
            str: HTML comparison
        """
        # Use the SVG comparison as part of the HTML
        svg = self._generate_svg_comparison(helix1, helix2)
        
        # Calculate similarities
        primary_similarity = self._calculate_pattern_similarity(helix1["base_pattern"], helix2["base_pattern"])
        complementary_similarity = self._calculate_pattern_similarity(helix1["complementary_strand"], helix2["complementary_strand"])
        overall_similarity = (primary_similarity + complementary_similarity) / 2
        
        # Create HTML wrapper
        html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum DNA Helix Comparison</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #333;
        }}
        .comparison-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .helix-info {{
            padding: 15px;
            border-radius: 6px;
            background-color: #f5f5f5;
        }}
        .info-item {{
            margin-bottom: 5px;
        }}
        .label {{
            font-weight: bold;
            display: inline-block;
            width: 100px;
        }}
        .integrity-high {{
            color: green;
        }}
        .integrity-medium {{
            color: orange;
        }}
        .integrity-low {{
            color: red;
        }}
        .similarity-high {{
            color: green;
        }}
        .similarity-medium {{
            color: orange;
        }}
        .similarity-low {{
            color: red;
        }}
        .similarity-section {{
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        .visualization {{
            margin-top: 20px;
            overflow-x: auto;
        }}
        .sequence {{
            font-family: monospace;
            margin-top: 20px;
        }}
        .dna-a {{ color: #00FF00; }}
        .dna-t {{ color: #FF0000; }}
        .dna-g {{ color: #0000FF; }}
        .dna-c {{ color: #FFFF00; }}
        .quantum {{ color: #FF00FF; }}
        .binary {{ color: #C0C0C0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Quantum DNA Helix Comparison</h1>
        
        <div class="comparison-grid">
            <div class="helix-info">
                <h2>Helix 1</h2>
                <div class="info-item">
                    <span class="label">ID:</span>
                    <span>{helix1["helix_id"][:12]}...</span>
                </div>
                <div class="info-item">
                    <span class="label">Type:</span>
                    <span>{helix1["helix_type"]}</span>
                </div>
                <div class="info-item">
                    <span class="label">Integrity:</span>
                    <span class="integrity-{'high' if helix1['integrity'] >= 0.9 else 'medium' if helix1['integrity'] >= 0.7 else 'low'}">
                        {helix1["integrity"]:.4f}
                    </span>
                </div>
                <div class="info-item">
                    <span class="label">Length:</span>
                    <span>{len(helix1["base_pattern"])}</span>
                </div>
                <div class="info-item">
                    <span class="label">Q-Markers:</span>
                    <span>{self._count_quantum_markers(helix1["base_pattern"])}</span>
                </div>
            </div>
            
            <div class="helix-info">
                <h2>Helix 2</h2>
                <div class="info-item">
                    <span class="label">ID:</span>
                    <span>{helix2["helix_id"][:12]}...</span>
                </div>
                <div class="info-item">
                    <span class="label">Type:</span>
                    <span>{helix2["helix_type"]}</span>
                </div>
                <div class="info-item">
                    <span class="label">Integrity:</span>
                    <span class="integrity-{'high' if helix2['integrity'] >= 0.9 else 'medium' if helix2['integrity'] >= 0.7 else 'low'}">
                        {helix2["integrity"]:.4f}
                    </span>
                </div>
                <div class="info-item">
                    <span class="label">Length:</span>
                    <span>{len(helix2["base_pattern"])}</span>
                </div>
                <div class="info-item">
                    <span class="label">Q-Markers:</span>
                    <span>{self._count_quantum_markers(helix2["base_pattern"])}</span>
                </div>
            </div>
        </div>
        
        <div class="similarity-section">
            <h2>Similarity Analysis</h2>
            <div class="info-item">
                <span class="label">Primary:</span>
                <span class="similarity-{'high' if primary_similarity >= 0.7 else 'medium' if primary_similarity >= 0.4 else 'low'}">
                    {primary_similarity:.4f}
                </span>
            </div>
            <div class="info-item">
                <span class="label">Complementary:</span>
                <span class="similarity-{'high' if complementary_similarity >= 0.7 else 'medium' if complementary_similarity >= 0.4 else 'low'}">
                    {complementary_similarity:.4f}
                </span>
            </div>
            <div class="info-item">
                <span class="label">Overall:</span>
                <span class="similarity-{'high' if overall_similarity >= 0.7 else 'medium' if overall_similarity >= 0.4 else 'low'}">
                    {overall_similarity:.4f}
                </span>
            </div>
            <div class="info-item">
                <span class="label">Compatible:</span>
                <span style="color: {'green' if helix1['helix_type'] == helix2['helix_type'] else 'red'}">
                    {helix1["helix_type"] == helix2["helix_type"]}
                </span>
            </div>
            <div class="info-item">
                <span class="label">Merger Recommended:</span>
                <span style="color: {'green' if 0.3 <= primary_similarity <= 0.7 else 'red'}">
                    {0.3 <= primary_similarity <= 0.7}
                </span>
            </div>
        </div>
        
        <h2>Visual Comparison</h2>
        <div class="visualization">
            {svg}
        </div>
        
        <h2>Sequence Data</h2>
        <div class="comparison-grid">
            <div class="sequence">
                <h3>Helix 1</h3>
                <div><strong>Primary:</strong><br>
                {self._generate_colored_html_sequence(helix1["base_pattern"][:30])}</div>
                <div><strong>Complementary:</strong><br>
                {self._generate_colored_html_sequence(helix1["complementary_strand"][:30])}</div>
            </div>
            
            <div class="sequence">
                <h3>Helix 2</h3>
                <div><strong>Primary:</strong><br>
                {self._generate_colored_html_sequence(helix2["base_pattern"][:30])}</div>
                <div><strong>Complementary:</strong><br>
                {self._generate_colored_html_sequence(helix2["complementary_strand"][:30])}</div>
            </div>
        </div>
    </div>
</body>
</html>
'''
        
        return html
        
    def _generate_terminal_scaffold(self, helix):
        """Generate terminal-based visualization for a helix scaffold.
        
        Args:
            helix (dict): Helix data with scaffolding
            
        Returns:
            str: Terminal scaffold visualization
        """
        primary_strand = helix["base_pattern"]
        complementary_strand = helix["complementary_strand"]
        scaffolding = helix["scaffolding"]
        
        # Prepare header
        header = f"{BOLD}Helix Scaffold Visualization{RESET}\n"
        header += f"Helix ID: {CYAN}{helix['helix_id'][:12]}...{RESET}\n"
        header += f"Scaffold Template: {YELLOW}{scaffolding['template']}{RESET}\n"
        header += f"Integrity Factor: {GREEN}{scaffolding['structural_integrity']:.2f}{RESET}\n"
        header += f"Error Correction: {BLUE}{scaffolding['error_correction_level']:.2f}{RESET}\n\n"
        
        # Create a visual representation of the scaffolded helix
        visualization = header
        
        # Prepare scaffold point positions
        scaffold_positions = []
        for point in scaffolding["scaffold_points"]:
            position = int(point["position_factor"] * len(primary_strand))
            scaffold_positions.append(position)
            
        # Create scaffold markers line
        scaffold_line = ""
        for i in range(len(primary_strand)):
            if i in scaffold_positions:
                scaffold_line += f"{YELLOW}S{RESET}"
            else:
                scaffold_line += " "
                
        # Add scaffold line
        visualization += scaffold_line + "\n"
        
        # Add primary strand with coloring
        primary_colored = ""
        for i, char in enumerate(primary_strand):
            if i in scaffold_positions:
                primary_colored += f"{YELLOW}{char}{RESET}"
            elif char in "ATGC":
                primary_colored += f"{GREEN}{char}{RESET}"
            elif char in "ΦΨΩΔΘ":
                primary_colored += f"{MAGENTA}{char}{RESET}"
            else:
                primary_colored += f"{WHITE}{char}{RESET}"
                
        visualization += primary_colored + "\n"
        
        # Add connecting lines
        connector = ""
        for i in range(len(primary_strand)):
            if i in scaffold_positions:
                connector += f"{YELLOW}|{RESET}"
            elif primary_strand[i] in BASE_PAIRS and BASE_PAIRS[primary_strand[i]] == complementary_strand[i]:
                connector += "│"
            else:
                connector += " "
                
        visualization += connector + "\n"
        
        # Add complementary strand with coloring
        complementary_colored = ""
        for i, char in enumerate(complementary_strand):
            if i in scaffold_positions:
                complementary_colored += f"{YELLOW}{char}{RESET}"
            elif char in "ATGC":
                complementary_colored += f"{GREEN}{char}{RESET}"
            elif char in "ΦΨΩΔΘ":
                complementary_colored += f"{MAGENTA}{char}{RESET}"
            else:
                complementary_colored += f"{WHITE}{char}{RESET}"
                
        visualization += complementary_colored + "\n"
        
        # Add scaffold description
        visualization += f"\n{BOLD}Scaffold Points:{RESET}\n"
        for i, point in enumerate(scaffolding["scaffold_points"]):
            position = int(point["position_factor"] * len(primary_strand))
            visualization += f"  {i+1}. Position {position} ({point['position_factor']:.2f}) - Marker: {YELLOW}{point['marker']}{RESET}, Strength: {point['binding_strength']:.2f}\n"
            
        # Add note about error correction
        if scaffolding["error_correction_level"] > 0.5:
            visualization += f"\n{BOLD}Error Correction Active:{RESET} {GREEN}Yes{RESET} (Level: {scaffolding['error_correction_level']:.2f})\n"
        else:
            visualization += f"\n{BOLD}Error Correction Active:{RESET} {RED}No{RESET} (Level: {scaffolding['error_correction_level']:.2f})\n"
            
        return visualization
        
    def _generate_json_scaffold(self, helix):
        """Generate JSON visualization for a helix scaffold.
        
        Args:
            helix (dict): Helix data with scaffolding
            
        Returns:
            dict: JSON scaffold visualization
        """
        scaffolding = helix["scaffolding"]
        
        # Create base visualization
        visualization = {
            "helix_id": helix["helix_id"],
            "helix_type": helix["helix_type"],
            "visualization_timestamp": self._timestamp(),
            "scaffold": {
                "template": scaffolding["template"],
                "integrity_factor": scaffolding["structural_integrity"],
                "error_correction_level": scaffolding["error_correction_level"],
                "scaffold_points": []
            },
            "strands": {
                "primary": helix["base_pattern"],
                "complementary": helix["complementary_strand"]
            }
        }
        
        # Add scaffold points
        for point in scaffolding["scaffold_points"]:
            position = int(point["position_factor"] * len(helix["base_pattern"]))
            
            point_info = {
                "position": position,
                "position_factor": point["position_factor"],
                "binding_strength": point["binding_strength"],
                "marker": point["marker"],
                "primary_base": helix["base_pattern"][position] if position < len(helix["base_pattern"]) else None,
                "complementary_base": helix["complementary_strand"][position] if position < len(helix["complementary_strand"]) else None
            }
            
            visualization["scaffold"]["scaffold_points"].append(point_info)
            
        # Add strand modifications if present
        if "strand_modifications" in scaffolding:
            visualization["scaffold"]["strand_modifications"] = scaffolding["strand_modifications"]
            
        return visualization
        
    def _generate_svg_scaffold(self, helix):
        """Generate SVG visualization for a helix scaffold.
        
        Args:
            helix (dict): Helix data with scaffolding
            
        Returns:
            str: SVG scaffold visualization
        """
        primary_strand = helix["base_pattern"]
        complementary_strand = helix["complementary_strand"]
        scaffolding = helix["scaffolding"]
        
        # SVG settings
        svg_width = 800
        svg_height = 500
        margin = 50
        strand_height = 20
        base_width = min(40, (svg_width - 2 * margin) / len(primary_strand))
        
        # Prepare scaffold point positions
        scaffold_positions = []
        for point in scaffolding["scaffold_points"]:
            position = int(point["position_factor"] * len(primary_strand))
            scaffold_positions.append(position)
            
        # Start SVG document
        svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        svg += f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">\n'
        
        # Add title and description
        svg += f'  <title>Helix Scaffold Visualization</title>\n'
        svg += '  <desc>Visualization of a scaffolded quantum DNA double helix structure</desc>\n'
        
        # Add style definitions
        svg += '  <defs>\n'
        svg += '    <linearGradient id="scaffoldGradient" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        svg += '      <stop offset="0%" style="stop-color:#FFD700;stop-opacity:0.7" />\n'
        svg += '      <stop offset="100%" style="stop-color:#FFA500;stop-opacity:0.7" />\n'
        svg += '    </linearGradient>\n'
        svg += '  </defs>\n'
        
        # Add header text
        svg += f'  <text x="{svg_width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Helix Scaffold Visualization</text>\n'
        svg += f'  <text x="{svg_width/2}" y="50" text-anchor="middle" font-family="Arial" font-size="12">Helix ID: {helix["helix_id"][:12]}... | Template: {scaffolding["template"]}</text>\n'
        svg += f'  <text x="{svg_width/2}" y="70" text-anchor="middle" font-family="Arial" font-size="12">Integrity Factor: {scaffolding["structural_integrity"]:.2f} | Error Correction: {scaffolding["error_correction_level"]:.2f}</text>\n'
        
        # Add primary strand
        primary_y = margin + strand_height * 2
        for i in range(len(primary_strand)):
            x = margin + i * base_width
            char = primary_strand[i]
            
            # Determine character color
            color = self._get_svg_color(char)
            
            # Add character rectangle and text
            if i in scaffold_positions:
                # Use gradient for scaffold points
                svg += f'  <rect x="{x}" y="{primary_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="url(#scaffoldGradient)" stroke="orange" stroke-width="2" />\n'
            else:
                svg += f'  <rect x="{x}" y="{primary_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{color}" />\n'
                
            svg += f'  <text x="{x+base_width/2}" y="{primary_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{color}">{char}</text>\n'
            
        # Add complementary strand
        comp_y = primary_y + strand_height * 3
        for i in range(len(complementary_strand)):
            x = margin + i * base_width
            char = complementary_strand[i]
            
            # Determine character color
            color = self._get_svg_color(char)
            
            # Add character rectangle and text
            if i in scaffold_positions:
                # Use gradient for scaffold points
                svg += f'  <rect x="{x}" y="{comp_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="url(#scaffoldGradient)" stroke="orange" stroke-width="2" />\n'
            else:
                svg += f'  <rect x="{x}" y="{comp_y-strand_height/2}" width="{base_width}" height="{strand_height}" fill="white" stroke="{color}" />\n'
                
            svg += f'  <text x="{x+base_width/2}" y="{comp_y+5}" text-anchor="middle" font-family="monospace" font-size="{base_width*0.7}" fill="{color}">{char}</text>\n'
            
        # Add connecting lines
        for i in range(len(primary_strand)):
            x = margin + i * base_width + base_width/2
            
            if i in scaffold_positions:
                # Add enhanced scaffold connector
                svg += f'  <line x1="{x}" y1="{primary_y+strand_height/2}" x2="{x}" y2="{comp_y-strand_height/2}" stroke="orange" stroke-width="2" stroke-dasharray="3,2" />\n'
            else:
                # Add standard connector
                svg += f'  <line x1="{x}" y1="{primary_y+strand_height/2}" x2="{x}" y2="{comp_y-strand_height/2}" stroke="#888888" stroke-width="1" />\n'
                
        # Add scaffold point markers
        for point in scaffolding["scaffold_points"]:
            position = int(point["position_factor"] * len(primary_strand))
            x = margin + position * base_width + base_width/2
            
            # Draw scaffold marker
            svg += f'  <circle cx="{x}" cy="{(primary_y+comp_y)/2}" r="{strand_height*0.8}" fill="none" stroke="orange" stroke-width="2" />\n'
            svg += f'  <text x="{x}" y="{(primary_y+comp_y)/2+5}" text-anchor="middle" font-family="Arial" font-size="{base_width*0.6}" fill="orange">S</text>\n'
            
        # Add scaffold details
        details_y = comp_y + strand_height * 3
        svg += f'  <text x="{margin}" y="{details_y}" font-family="Arial" font-size="14" font-weight="bold">Scaffold Points:</text>\n'
        
        for i, point in enumerate(scaffolding["scaffold_points"]):
            position = int(point["position_factor"] * len(primary_strand))
            detail_text = f"Position {position} ({point['position_factor']:.2f}) - Marker: {point['marker']}, Strength: {point['binding_strength']:.2f}"
            svg += f'  <text x="{margin+20}" y="{details_y + 20*(i+1)}" font-family="Arial" font-size="12">{i+1}. {detail_text}</text>\n'
            
        # Add legend
        legend_x = svg_width - margin - 200
        legend_y = details_y
        svg += f'  <text x="{legend_x}" y="{legend_y}" font-family="Arial" font-size="14" font-weight="bold">Legend:</text>\n'
        
        # Scaffold point
        svg += f'  <rect x="{legend_x}" y="{legend_y+10}" width="12" height="12" fill="url(#scaffoldGradient)" stroke="orange" stroke-width="2" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+20}" font-family="Arial" font-size="12">Scaffold Point</text>\n'
        
        # Scaffold connector
        svg += f'  <line x1="{legend_x}" y1="{legend_y+36}" x2="{legend_x+12}" y2="{legend_y+36}" stroke="orange" stroke-width="2" stroke-dasharray="3,2" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+40}" font-family="Arial" font-size="12">Scaffold Connector</text>\n'
        
        # Standard DNA
        svg += f'  <rect x="{legend_x}" y="{legend_y+50}" width="12" height="12" fill="white" stroke="{self._get_svg_color("A")}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+60}" font-family="Arial" font-size="12">Standard DNA</text>\n'
        
        # Quantum marker
        phi_color = "#AA00AA"  # Default magenta for quantum markers
        if self.visualization_settings["color_scheme"] in self.color_schemes:
            if "Φ" in self.color_schemes[self.visualization_settings["color_scheme"]]:
                phi_color = self.color_schemes[self.visualization_settings["color_scheme"]]["Φ"]
        svg += f'  <rect x="{legend_x}" y="{legend_y+70}" width="12" height="12" fill="white" stroke="{phi_color}" />\n'
        svg += f'  <text x="{legend_x+20}" y="{legend_y+80}" font-family="Arial" font-size="12">Quantum Marker</text>\n'
        
        # Close SVG
        svg += '</svg>'
        
        return svg
        
    def _generate_html_scaffold(self, helix):
        """Generate HTML visualization for a helix scaffold.
        
        Args:
            helix (dict): Helix data with scaffolding
            
        Returns:
            str: HTML scaffold visualization
        """
        # Use the SVG scaffold as part of the HTML
        svg = self._generate_svg_scaffold(helix)
        
        # Create HTML wrapper
        html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum DNA Scaffold Visualization</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #333;
        }}
        .helix-info {{
            margin-bottom: 20px;
        }}
        .info-item {{
            margin-bottom: 5px;
        }}
        .label {{
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }}
        .integrity-high {{
            color: green;
        }}
        .integrity-medium {{
            color: orange;
        }}
        .integrity-low {{
            color: red;
        }}
        .scaffold-info {{
            background-color: #fff8e1;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 4px solid #ffd700;
        }}
        .scaffold-point {{
            margin-bottom: 10px;
            padding-left: 20px;
        }}
        .visualization {{
            margin-top: 20px;
            overflow-x: auto;
        }}
        .sequence {{
            font-family: monospace;
            margin-top: 20px;
        }}
        .scaffold-marker {{
            background-color: #fff8e1;
            border: 1px solid #ffd700;
        }}
        .dna-a {{ color: #00FF00; }}
        .dna-t {{ color: #FF0000; }}
        .dna-g {{ color: #0000FF; }}
        .dna-c {{ color: #FFFF00; }}
        .quantum {{ color: #FF00FF; }}
        .binary {{ color: #C0C0C0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Quantum DNA Scaffold Visualization</h1>
        
        <div class="helix-info">
            <div class="info-item">
                <span class="label">Helix Type:</span>
                <span>{helix["helix_type"]}</span>
            </div>
            <div class="info-item">
                <span class="label">Helix ID:</span>
                <span>{helix["helix_id"]}</span>
            </div>
            <div class="info-item">
                <span class="label">Integrity:</span>
                <span class="integrity-{'high' if helix['integrity'] >= 0.9 else 'medium' if helix['integrity'] >= 0.7 else 'low'}">
                    {helix["integrity"]:.4f}
                </span>
            </div>
            <div class="info-item">
                <span class="label">Strand Length:</span>
                <span>{len(helix["base_pattern"])}</span>
            </div>
        </div>
        
        <div class="scaffold-info">
            <h2>Scaffold Information</h2>
            <div class="info-item">
                <span class="label">Template:</span>
                <span>{helix["scaffolding"]["template"]}</span>
            </div>
            <div class="info-item">
                <span class="label">Integrity Factor:</span>
                <span>{helix["scaffolding"]["structural_integrity"]:.2f}</span>
            </div>
            <div class="info-item">
                <span class="label">Error Correction:</span>
                <span>{helix["scaffolding"]["error_correction_level"]:.2f}</span>
            </div>
            
            <h3>Scaffold Points</h3>
            {"""
            """.join([f"""
            <div class="scaffold-point">
                <strong>Point {i+1}:</strong> Position {int(point["position_factor"] * len(helix["base_pattern"]))} 
                ({point["position_factor"]:.2f}) - Marker: {point["marker"]}, 
                Strength: {point["binding_strength"]:.2f}
            </div>
            """ for i, point in enumerate(helix["scaffolding"]["scaffold_points"])])}
        </div>
        
        <h2>Visualization</h2>
        <div class="visualization">
            {svg}
        </div>
        
        <h2>Sequence Data with Scaffold Highlights</h2>
        <div class="sequence">
            <strong>Primary Strand:</strong><br>
            {self._generate_scaffolded_html_sequence(helix["base_pattern"], helix["scaffolding"]["scaffold_points"], len(helix["base_pattern"]))}<br><br>
            
            <strong>Complementary Strand:</strong><br>
            {self._generate_scaffolded_html_sequence(helix["complementary_strand"], helix["scaffolding"]["scaffold_points"], len(helix["base_pattern"]))}<br><br>
        </div>
    </div>
</body>
</html>
'''
        
        return html
        
    def _calculate_pattern_similarity(self, pattern1, pattern2):
        """Calculate similarity between two patterns.
        
        Args:
            pattern1 (str): First pattern
            pattern2 (str): Second pattern
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        # Find shorter pattern
        min_length = min(len(pattern1), len(pattern2))
        
        if min_length == 0:
            return 0.0
            
        # Count matching characters
        matches = 0
        for i in range(min_length):
            if pattern1[i] == pattern2[i]:
                matches += 1
                
        # Return similarity as match ratio
        return matches / min_length
        
    def _count_quantum_markers(self, pattern):
        """Count quantum markers in a pattern.
        
        Args:
            pattern (str): Pattern to analyze
            
        Returns:
            int: Number of quantum markers
        """
        return sum(1 for char in pattern if char in "ΦΨΩΔΘ")
        
    def _get_base_type(self, char):
        """Get the type of a base character.
        
        Args:
            char (str): Character to check
            
        Returns:
            str: Character type
        """
        if char in "ATGC":
            return "standard-dna"
        elif char in "ΦΨΩΔΘ":
            return "quantum-marker"
        elif char in "01+-":
            return "binary-symbolic"
        else:
            return "unknown"
            
    def _format_colored_strand(self, strand):
        """Format a strand with colored characters for terminal display.
        
        Args:
            strand (str): Strand to format
            
        Returns:
            str: Formatted strand with color codes
        """
        result = ""
        for char in strand:
            if char in "ATGC":
                result += f"{GREEN}{char}{RESET}"
            elif char in "ΦΨΩΔΘ":
                result += f"{MAGENTA}{char}{RESET}"
            elif char in "01+-":
                result += f"{YELLOW}{char}{RESET}"
            else:
                result += f"{WHITE}{char}{RESET}"
                
        return result
        
    def _get_svg_color(self, char):
        """Get SVG color for a character based on current color scheme.
        
        Args:
            char (str): Character to get color for
            
        Returns:
            str: Color hex code
        """
        if self.visualization_settings["color_scheme"] in self.color_schemes:
            color_scheme = self.color_schemes[self.visualization_settings["color_scheme"]]
            if char in color_scheme:
                return color_scheme[char]
                
        if char in "ATGC":
            return "#00AA00"  # Green
        elif char in "ΦΨΩΔΘ":
            return "#AA00AA"  # Magenta
        elif char in "01+-":
            return "#AAAA00"  # Yellow
        else:
            return "#000000"  # Black
            
    def _generate_colored_html_sequence(self, sequence):
        """Generate sequence with colored spans for HTML display.
        
        Args:
            sequence (str): Sequence to format
            
        Returns:
            str: HTML formatted sequence
        """
        result = ""
        for char in sequence:
            if char in "ATGC":
                result += f'<span class="dna-{char.lower()}">{char}</span>'
            elif char in "ΦΨΩΔΘ":
                result += f'<span class="quantum">{char}</span>'
            elif char in "01+-":
                result += f'<span class="binary">{char}</span>'
            else:
                result += char
                
        return result
        
    def _generate_scaffolded_html_sequence(self, sequence, scaffold_points, total_length):
        """Generate sequence with scaffold highlights for HTML display.
        
        Args:
            sequence (str): Sequence to format
            scaffold_points (list): List of scaffold point dictionaries
            total_length (int): Total length of sequence
            
        Returns:
            str: HTML formatted sequence with scaffold highlights
        """
        # Determine scaffold positions
        scaffold_positions = []
        for point in scaffold_points:
            position = int(point["position_factor"] * total_length)
            scaffold_positions.append(position)
            
        # Generate HTML
        result = ""
        for i, char in enumerate(sequence):
            if i in scaffold_positions:
                # Apply scaffold marker style
                result += f'<span class="scaffold-marker">'
                
            if char in "ATGC":
                result += f'<span class="dna-{char.lower()}">{char}</span>'
            elif char in "ΦΨΩΔΘ":
                result += f'<span class="quantum">{char}</span>'
            elif char in "01+-":
                result += f'<span class="binary">{char}</span>'
            else:
                result += char
                
            if i in scaffold_positions:
                result += f'</span>'
                
        return result
        
    def _log(self, message, color=RESET, level="INFO"):
        """Log a message with timestamp and color.
        
        Args:
            message (str): Message to log
            color (str, optional): Color code. Defaults to RESET.
            level (str, optional): Log level. Defaults to "INFO".
        """
        timestamp = self._timestamp()
        formatted_message = f"{timestamp} - DNAVisualizer - {level} - {message}"
        print(f"{color}{formatted_message}{RESET}")
        
    def _timestamp(self):
        """Generate a timestamp for logs and records.
        
        Returns:
            str: Current timestamp as string
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def main():
    """Run the Quantum DNA Visualizer as a standalone module."""
    from double_helix_framework import DoubleHelixScaffold
    
    # Initialize scaffold framework
    scaffold = DoubleHelixScaffold()
    scaffold.initialize()
    
    # Create a quantum DNA helix
    print(f"\n{BOLD}{MAGENTA}Creating Quantum DNA Helix:{RESET}")
    helix = scaffold.create_helix("quantum-dna")
    
    if helix:
        # Apply scaffold template
        enhanced_helix = scaffold.apply_scaffold_template(helix["helix_id"], "quantum-enhancement")
        
        # Generate quantum bindings
        scaffold.generate_quantum_bindings(helix["helix_id"])
        
        # Initialize visualizer
        visualizer = QuantumDNAVisualizer()
        visualizer.initialize()
        
        # Connect to scaffold framework
        visualizer.connect_helix_framework(scaffold)
        
        # Visualize helix
        print(f"\n{BOLD}{MAGENTA}Visualizing Helix:{RESET}")
        visualizer.visualize_helix(helix["helix_id"], "terminal")
        
        # Create output directory if it doesn't exist
        output_dir = "visualization_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Generate HTML visualization
        html_path = os.path.join(output_dir, "helix_visualization.html")
        result = visualizer.visualize_helix(helix["helix_id"], "html", html_path)
        
        if isinstance(result, dict) and result.get("success"):
            print(f"\n{GREEN}Saved HTML visualization to: {html_path}{RESET}")
            
        # Generate scaffold visualization
        if enhanced_helix:
            print(f"\n{BOLD}{MAGENTA}Visualizing Scaffold:{RESET}")
            visualizer.generate_scaffold_visualization(enhanced_helix["helix_id"], "terminal")
            
            # Generate HTML scaffold visualization
            html_path = os.path.join(output_dir, "scaffold_visualization.html")
            result = visualizer.generate_scaffold_visualization(enhanced_helix["helix_id"], "html", html_path)
            
            if isinstance(result, dict) and result.get("success"):
                print(f"\n{GREEN}Saved HTML scaffold visualization to: {html_path}{RESET}")
                
        # Create a second helix for comparison
        print(f"\n{BOLD}{MAGENTA}Creating Second Helix for Comparison:{RESET}")
        helix2 = scaffold.create_helix("quantum-dna")
        
        if helix2:
            # Generate comparison visualization
            print(f"\n{BOLD}{MAGENTA}Visualizing Comparison:{RESET}")
            visualizer.generate_comparison_visualization(helix["helix_id"], helix2["helix_id"], "terminal")
            
            # Generate HTML comparison visualization
            html_path = os.path.join(output_dir, "comparison_visualization.html")
            result = visualizer.generate_comparison_visualization(helix["helix_id"], helix2["helix_id"], "html", html_path)
            
            if isinstance(result, dict) and result.get("success"):
                print(f"\n{GREEN}Saved HTML comparison visualization to: {html_path}{RESET}")


if __name__ == "__main__":
    main()