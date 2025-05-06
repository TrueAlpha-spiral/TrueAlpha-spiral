"""
RUN DNA VISUALIZATION

This script runs the quantum DNA visualization system, connecting it to
the double helix scaffold framework to visualize interstellar DNA patterns.

Architect: Russell Nordland
"""

import os
from double_helix_framework import DoubleHelixScaffold
from quantum_dna_visualization import QuantumDNAVisualizer
from quantum_dna_retrieval import QuantumDNARetrieval

def main():
 """Run the DNA visualization system."""
 print("\n=== QUANTUM DNA VISUALIZATION SYSTEM ===\n")

 # Initialize the double helix scaffold
 print("Initializing Double Helix Scaffold Framework...")
 scaffold = DoubleHelixScaffold()
 scaffold.initialize()

 # Initialize the DNA retrieval system if available
 dna_retrieval = None
 try:
 print("Initializing Quantum DNA Retrieval System...")
 dna_retrieval = QuantumDNARetrieval()
 dna_retrieval.initialize()

 # Connect scaffold to retrieval system
 print("Connecting scaffold to DNA retrieval system...")
 scaffold.connect_to_dna_retrieval(dna_retrieval)

 except Exception as e:
 print(f"Warning: Could not initialize DNA retrieval system: {str(e)}")
 print("Continuing with manually created helices...")

 # Create output directory
 output_dir = "visualization_output"
 if not os.path.exists(output_dir):
 os.makedirs(output_dir)
 print(f"Created output directory: {output_dir}")

 # Create quantum DNA helix
 print("\nCreating Quantum DNA Helix...")
 quantum_helix = scaffold.create_helix("quantum-dna")
 if not quantum_helix:
 print("Failed to create quantum DNA helix. Exiting.")
 return

 # Create spiral eigensystem helix
 print("\nCreating Spiral Eigensystem Helix...")
 spiral_helix = scaffold.create_helix("spiral-eigensystem")
 if not spiral_helix:
 print("Failed to create spiral eigensystem helix. Continuing with quantum helix only.")
 spiral_helix = None

 # Create truth resonant helix
 print("\nCreating Truth Resonant Helix...")
 truth_helix = scaffold.create_helix("truth-resonant")
 if not truth_helix:
 print("Failed to create truth resonant helix. Continuing with other helices.")
 truth_helix = None

 # Apply scaffold templates
 print("\nApplying scaffold templates...")
 enhanced_quantum_helix = scaffold.apply_scaffold_template(quantum_helix["helix_id"], "quantum-enhancement")

 # Apply templates to other helices if they exist
 enhanced_spiral_helix = None
 enhanced_truth_helix = None
 if spiral_helix:
 enhanced_spiral_helix = scaffold.apply_scaffold_template(spiral_helix["helix_id"], "eigensystem-reinforcement")
 if truth_helix:
 enhanced_truth_helix = scaffold.apply_scaffold_template(truth_helix["helix_id"], "truth-amplification")

 # Generate quantum bindings
 print("\nGenerating quantum bindings...")
 scaffold.generate_quantum_bindings(quantum_helix["helix_id"])
 if spiral_helix:
 scaffold.generate_quantum_bindings(spiral_helix["helix_id"])
 if truth_helix:
 scaffold.generate_quantum_bindings(truth_helix["helix_id"])

 # Merge helices
 merged_helix = None
 if spiral_helix:
 print("\nMerging helices...")
 merged_helix = scaffold.merge_helices(quantum_helix["helix_id"], spiral_helix["helix_id"], "quantum-fusion")

 # Initialize visualizer
 print("\nInitializing Quantum DNA Visualizer...")
 visualizer = QuantumDNAVisualizer()
 visualizer.initialize()

 # Connect to scaffold framework
 print("Connecting visualizer to scaffold framework...")
 visualizer.connect_helix_framework(scaffold)

 # Generate visualizations
 print("\nGenerating visualizations...")

 # Terminal visualizations
 print("\n1. Terminal Visualizations:")
 print("\n=== Quantum DNA Helix ===")
 visualizer.visualize_helix(quantum_helix["helix_id"], "terminal")

 if spiral_helix:
 print("\n=== Spiral Eigensystem Helix ===")
 visualizer.visualize_helix(spiral_helix["helix_id"], "terminal")

 if truth_helix:
 print("\n=== Truth Resonant Helix ===")
 visualizer.visualize_helix(truth_helix["helix_id"], "terminal")

 if merged_helix:
 print("\n=== Merged Helix ===")
 visualizer.visualize_helix(merged_helix["helix_id"], "terminal")

 # Generate HTML visualizations
 print("\n2. Generating HTML Visualizations...")

 visualizer.visualize_helix(
 quantum_helix["helix_id"],
 "html",
 os.path.join(output_dir, "quantum_helix.html")
 )

 if spiral_helix:
 visualizer.visualize_helix(
 spiral_helix["helix_id"],
 "html",
 os.path.join(output_dir, "spiral_helix.html")
 )

 if truth_helix:
 visualizer.visualize_helix(
 truth_helix["helix_id"],
 "html",
 os.path.join(output_dir, "truth_helix.html")
 )

 if merged_helix:
 visualizer.visualize_helix(
 merged_helix["helix_id"],
 "html",
 os.path.join(output_dir, "merged_helix.html")
 )

 # Generate scaffold visualizations
 print("\n3. Generating Scaffold Visualizations...")

 visualizer.generate_scaffold_visualization(
 quantum_helix["helix_id"],
 "html",
 os.path.join(output_dir, "quantum_scaffold.html")
 )

 if spiral_helix:
 visualizer.generate_scaffold_visualization(
 spiral_helix["helix_id"],
 "html",
 os.path.join(output_dir, "spiral_scaffold.html")
 )

 if truth_helix:
 visualizer.generate_scaffold_visualization(
 truth_helix["helix_id"],
 "html",
 os.path.join(output_dir, "truth_scaffold.html")
 )

 # Generate comparison visualizations
 print("\n4. Generating Comparison Visualizations...")

 if spiral_helix:
 visualizer.generate_comparison_visualization(
 quantum_helix["helix_id"],
 spiral_helix["helix_id"],
 "html",
 os.path.join(output_dir, "quantum_vs_spiral.html")
 )

 if truth_helix:
 visualizer.generate_comparison_visualization(
 quantum_helix["helix_id"],
 truth_helix["helix_id"],
 "html",
 os.path.join(output_dir, "quantum_vs_truth.html")
 )

 if spiral_helix and truth_helix:
 visualizer.generate_comparison_visualization(
 spiral_helix["helix_id"],
 truth_helix["helix_id"],
 "html",
 os.path.join(output_dir, "spiral_vs_truth.html")
 )

 if merged_helix:
 visualizer.generate_comparison_visualization(
 merged_helix["helix_id"],
 quantum_helix["helix_id"],
 "html",
 os.path.join(output_dir, "merged_vs_quantum.html")
 )

 # Summary of output files
 print("\n=== Visualization Complete ===")
 print(f"Output files available in: {output_dir}/")

 # List generated files
 files = os.listdir(output_dir)
 for i, file in enumerate(files):
 if file.endswith(".html"):
 print(f" {i+1}. {file}")

 print("\nThe HTML files provide interactive visualizations of the quantum DNA helices.")
 print("Each visualization includes detailed information about the helix structure,")
 print("scaffold points, quantum bindings, and complementary strand pairings.")

if __name__ == "__main__":
 main()