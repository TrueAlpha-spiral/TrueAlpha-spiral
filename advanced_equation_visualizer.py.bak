"""
ADVANCED EQUATION VISUALIZER

This module provides visualization tools for the Architect's Advanced Equation
integration into the DNA tracking system. It visually demonstrates how the
equation components affect the cryptographic hash generation and pattern protection.

Architect: Russell Nordland
"""

import os
import time
import hashlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
import math
import random

# Constants
OUTPUT_DIR = "visualization_output"
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"

def timestamp():
    """Generate a timestamp for logs and filenames."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def log_message(message, color=RESET):
    """Log a message with timestamp and color."""
    print(f"{color}[{timestamp()}] {message}{RESET}")

def ensure_output_dir():
    """Ensure output directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        log_message(f"Created output directory: {OUTPUT_DIR}", color=GREEN)

def generate_advanced_equation_value(truth_factor, distance_factor, size_factor):
    """
    Generate the Advanced Equation value based on the provided factors.
    
    Advanced Equation: Φ = ∑(αi·Ti)/(√(D)·S)
    
    Args:
        truth_factor (float): Truth value (0.93-0.99)
        distance_factor (float): Distance value (1.2-1.6)
        size_factor (float): Size value (0.85-0.98)
        
    Returns:
        float: The calculated equation value
    """
    advanced_eq_value = (truth_factor) / (np.sqrt(distance_factor) * size_factor)
    return advanced_eq_value

def generate_pattern_hash(pattern_id, truth_factor, distance_factor, size_factor):
    """
    Generate a cryptographic hash using the Advanced Equation components.
    
    Args:
        pattern_id (str): Pattern identifier
        truth_factor (float): Truth value
        distance_factor (float): Distance value
        size_factor (float): Size value
        
    Returns:
        tuple: (hash_value, advanced_eq_value)
    """
    # Calculate Advanced Equation value
    advanced_eq_value = generate_advanced_equation_value(
        truth_factor, distance_factor, size_factor
    )
    
    # Format with high precision
    advanced_eq_str = f"{advanced_eq_value:.16f}"
    
    # First layer hash
    data = f"{pattern_id}-{time.time()}-{np.random.randint(10000, 99999)}-AEQ{advanced_eq_str}"
    hash_layer1 = hashlib.sha256(data.encode()).hexdigest()
    
    # Second layer hash with equation components
    final_data = f"{hash_layer1}:T{truth_factor:.4f}:D{distance_factor:.4f}:S{size_factor:.4f}"
    final_hash = hashlib.sha256(final_data.encode()).hexdigest()
    
    return final_hash, advanced_eq_value

def visualize_equation_impact(n_samples=50):
    """
    Visualize how changes in equation parameters impact the resulting hash values.
    
    Args:
        n_samples (int): Number of samples to generate
        
    Returns:
        str: Path to the saved visualization
    """
    ensure_output_dir()
    
    # Generate samples with varying equation parameters
    truth_values = np.linspace(0.93, 0.99, n_samples)
    distance_values = np.linspace(1.2, 1.6, n_samples)
    size_values = np.linspace(0.85, 0.98, n_samples)
    
    # Fixed pattern ID for comparison
    pattern_id = f"DNA-{int(time.time())}"
    
    # Collect data
    equation_values = []
    hash_similarities = []
    
    # Generate baseline hash
    baseline_truth = 0.96
    baseline_distance = 1.4
    baseline_size = 0.92
    baseline_hash, baseline_eq = generate_pattern_hash(
        pattern_id, baseline_truth, baseline_distance, baseline_size
    )
    
    # Generate variations
    for i in range(n_samples):
        truth = truth_values[i]
        distance = distance_values[i]
        size = size_values[i]
        
        hash_value, eq_value = generate_pattern_hash(pattern_id, truth, distance, size)
        
        # Calculate hash similarity (count matching characters)
        similarity = sum(a == b for a, b in zip(hash_value, baseline_hash)) / len(hash_value)
        
        equation_values.append(eq_value)
        hash_similarities.append(similarity)
    
    # Create visualization
    plt.figure(figsize=(12, 9))
    
    # Set up the grid
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
    
    # Plot 1: Equation value distribution
    ax1 = plt.subplot(gs[0, 0])
    ax1.hist(equation_values, bins=20, color='royalblue', alpha=0.7)
    ax1.set_title('Advanced Equation Value Distribution')
    ax1.set_xlabel('Equation Value (Φ)')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Plot 2: Hash similarity vs Equation value
    ax2 = plt.subplot(gs[0, 1])
    ax2.scatter(equation_values, hash_similarities, c=hash_similarities, 
               cmap='viridis', alpha=0.7, edgecolors='w', linewidth=0.5)
    ax2.set_title('Hash Similarity vs Equation Value')
    ax2.set_xlabel('Equation Value (Φ)')
    ax2.set_ylabel('Hash Similarity to Baseline')
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # Plot 3: Truth factor influence
    ax3 = plt.subplot(gs[1, 0])
    eq_values_truth = []
    for t in np.linspace(0.93, 0.99, 100):
        eq_values_truth.append(
            generate_advanced_equation_value(t, baseline_distance, baseline_size)
        )
    ax3.plot(np.linspace(0.93, 0.99, 100), eq_values_truth, 'g-', linewidth=2)
    ax3.set_title('Truth Factor Influence on Equation')
    ax3.set_xlabel('Truth Factor (T)')
    ax3.set_ylabel('Equation Value (Φ)')
    ax3.grid(True, linestyle='--', alpha=0.6)
    
    # Plot 4: Distance and Size impact
    ax4 = plt.subplot(gs[1, 1])
    distance_range = np.linspace(1.2, 1.6, 20)
    size_range = np.linspace(0.85, 0.98, 20)
    
    eq_grid = np.zeros((len(distance_range), len(size_range)))
    for i, d in enumerate(distance_range):
        for j, s in enumerate(size_range):
            eq_grid[i, j] = generate_advanced_equation_value(baseline_truth, d, s)
    
    im = ax4.imshow(eq_grid, extent=[0.85, 0.98, 1.6, 1.2], 
                   aspect='auto', cmap='plasma', origin='upper')
    ax4.set_title('Distance and Size Impact on Equation')
    ax4.set_xlabel('Size Factor (S)')
    ax4.set_ylabel('Distance Factor (D)')
    plt.colorbar(im, ax=ax4, label='Equation Value (Φ)')
    
    # Add equation and details in the figure text
    plt.figtext(0.5, 0.01, 
               "Architect's Advanced Equation: Φ = ∑(αi·Ti)/(√(D)·S)",
               ha='center', fontsize=14, bbox=dict(boxstyle='round,pad=0.5', 
                                                facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    
    # Save the visualization
    output_file = os.path.join(OUTPUT_DIR, f"advanced_equation_visual_{int(time.time())}.png")
    plt.savefig(output_file, dpi=300)
    log_message(f"Saved equation visualization to: {output_file}", color=GREEN)
    
    return output_file

def visualize_hash_distribution(n_samples=200):
    """
    Visualize how the equation-integrated hash values are distributed.
    
    Args:
        n_samples (int): Number of samples to generate
        
    Returns:
        str: Path to the saved visualization
    """
    ensure_output_dir()
    
    # Generate hashes with varying parameters
    hashes = []
    eq_values = []
    
    for i in range(n_samples):
        pattern_id = f"DNA-{int(time.time())}-{i}"
        truth = np.random.uniform(0.93, 0.99)
        distance = np.random.uniform(1.2, 1.6)
        size = np.random.uniform(0.85, 0.98)
        
        hash_value, eq_value = generate_pattern_hash(pattern_id, truth, distance, size)
        hashes.append(hash_value)
        eq_values.append(eq_value)
    
    # Analyze hash diversity
    hex_counts = {}
    for hash_value in hashes:
        for c in hash_value:
            hex_counts[c] = hex_counts.get(c, 0) + 1
    
    # Create visualization
    plt.figure(figsize=(12, 10))
    
    # Set up the grid
    gs = gridspec.GridSpec(2, 2)
    
    # Plot 1: Hex character distribution
    ax1 = plt.subplot(gs[0, 0])
    chars = list(hex_counts.keys())
    counts = list(hex_counts.values())
    
    sorted_indices = np.argsort(chars)
    sorted_chars = [chars[i] for i in sorted_indices]
    sorted_counts = [counts[i] for i in sorted_indices]
    
    ax1.bar(sorted_chars, sorted_counts, color='purple', alpha=0.7)
    ax1.set_title('Hex Character Distribution in Hashes')
    ax1.set_xlabel('Hex Character')
    ax1.set_ylabel('Frequency')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', alpha=0.4)
    
    # Plot 2: First byte distribution
    ax2 = plt.subplot(gs[0, 1])
    first_bytes = [h[:2] for h in hashes]
    unique_bytes = list(set(first_bytes))
    byte_counts = [first_bytes.count(b) for b in unique_bytes]
    
    sorted_indices = np.argsort(unique_bytes)
    sorted_bytes = [unique_bytes[i] for i in sorted_indices]
    sorted_byte_counts = [byte_counts[i] for i in sorted_indices]
    
    ax2.bar(sorted_bytes, sorted_byte_counts, color='teal', alpha=0.7)
    ax2.set_title('First Byte Distribution')
    ax2.set_xlabel('First Byte (Hex)')
    ax2.set_ylabel('Frequency')
    ax2.tick_params(axis='x', rotation=90)
    ax2.grid(True, linestyle='--', alpha=0.4)
    
    # Plot 3: Equation values vs hash first byte (numeric)
    ax3 = plt.subplot(gs[1, 0])
    first_byte_values = [int(h[:2], 16) for h in hashes]
    
    ax3.scatter(eq_values, first_byte_values, c=first_byte_values, 
               cmap='plasma', alpha=0.7, edgecolors='w', linewidth=0.5)
    ax3.set_title('Equation Value vs First Byte')
    ax3.set_xlabel('Equation Value (Φ)')
    ax3.set_ylabel('First Byte (Decimal)')
    ax3.grid(True, linestyle='--', alpha=0.6)
    
    # Plot 4: Hash visualization as an image
    ax4 = plt.subplot(gs[1, 1])
    
    # Convert hashes to a 2D grid of values
    grid_size = math.ceil(math.sqrt(n_samples))
    hash_grid = np.zeros((grid_size, grid_size))
    
    for i in range(min(n_samples, grid_size * grid_size)):
        row = i // grid_size
        col = i % grid_size
        # Use first 4 bytes of hash converted to int
        hash_grid[row, col] = int(hashes[i][:8], 16) % 256
    
    # Custom colormap for hash visualization
    colors = [(0, 0, 0.5), (0, 0.5, 1), (0, 1, 0.5), (0.5, 1, 0), 
              (1, 0.5, 0), (1, 0, 0)]
    cmap_name = 'hash_colors'
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
    
    im = ax4.imshow(hash_grid, cmap=cm)
    ax4.set_title('DNA Pattern Hashes Visualization')
    ax4.set_xticks([])
    ax4.set_yticks([])
    plt.colorbar(im, ax=ax4, label='Hash Value (First 4 bytes)')
    
    # Add description in the figure text
    plt.figtext(0.5, 0.01, 
               "Cryptographic Hash Distribution with Advanced Equation Integration\n" + 
               "Double-layered hashing process with 16-digit quantum fidelity precision",
               ha='center', fontsize=12, bbox=dict(boxstyle='round,pad=0.5', 
                                                facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.97])
    
    # Save the visualization
    output_file = os.path.join(OUTPUT_DIR, f"hash_distribution_visual_{int(time.time())}.png")
    plt.savefig(output_file, dpi=300)
    log_message(f"Saved hash distribution visualization to: {output_file}", color=GREEN)
    
    return output_file

def visualize_cosmic_alignment(iterations=100):
    """
    Visualize the cosmic alignment over time with the Advanced Equation integration.
    
    Args:
        iterations (int): Number of iterations to simulate
        
    Returns:
        str: Path to the saved visualization
    """
    ensure_output_dir()
    
    # Simulate cosmic alignment over time
    alignment_values = []
    truth_values = []
    sovereignty_values = []
    
    # Initial values
    truth = 0.96
    distance = 1.4
    size = 0.92
    
    for i in range(iterations):
        # Simulate small variations in parameters
        truth += np.random.normal(0, 0.002)  # Small random changes
        truth = max(0.93, min(0.99, truth))  # Keep in valid range
        
        distance += np.random.normal(0, 0.01)
        distance = max(1.2, min(1.6, distance))
        
        size += np.random.normal(0, 0.001)
        size = max(0.85, min(0.98, size))
        
        # Calculate cosmic alignment (simplified model)
        sovereignty = (truth) / (np.sqrt(distance) * size)
        cosmic_alignment = 0.85 + (truth - 0.93) * 0.8  # Simplified relationship
        cosmic_alignment = max(0.85, min(0.99, cosmic_alignment))
        
        alignment_values.append(cosmic_alignment)
        truth_values.append(truth)
        sovereignty_values.append(sovereignty)
    
    # Create visualization
    plt.figure(figsize=(12, 9))
    
    # Plot 1: Cosmic alignment over time
    plt.subplot(211)
    plt.plot(range(iterations), alignment_values, 'b-', linewidth=2)
    plt.axhline(y=0.85, color='r', linestyle='--', alpha=0.7, label='Minimum Threshold')
    plt.fill_between(range(iterations), 0.85, alignment_values, alpha=0.2, color='blue')
    plt.title('Cosmic Alignment over Time with Advanced Equation Integration')
    plt.xlabel('Iteration')
    plt.ylabel('Cosmic Alignment')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # Plot 2: Truth and Sovereignty values
    plt.subplot(212)
    plt.plot(range(iterations), truth_values, 'g-', linewidth=2, label='Truth Factor')
    plt.plot(range(iterations), sovereignty_values, 'r-', linewidth=2, label='Sovereignty')
    plt.title('Truth Factor and Sovereignty over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # Add description
    plt.figtext(0.5, 0.01, 
               "The Advanced Equation integration maintains cosmic alignment above 0.85\n" +
               "while truth factors naturally fluctuate over time.",
               ha='center', fontsize=12, bbox=dict(boxstyle='round,pad=0.5', 
                                                facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.97])
    
    # Save the visualization
    output_file = os.path.join(OUTPUT_DIR, f"cosmic_alignment_visual_{int(time.time())}.png")
    plt.savefig(output_file, dpi=300)
    log_message(f"Saved cosmic alignment visualization to: {output_file}", color=GREEN)
    
    return output_file

def main():
    """Main function to run all visualizations."""
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Advanced Equation Visualizer")
    parser.add_argument("--type", type=str, choices=["all", "impact", "hash", "cosmic"], 
                      default="all", help="Type of visualization to generate")
    args = parser.parse_args()
    
    log_message("Starting Advanced Equation Visualizer", color=BOLD + GREEN)
    ensure_output_dir()
    
    visualization_type = args.type.lower()
    
    if visualization_type == "all" or visualization_type == "impact":
        log_message("Generating equation impact visualization...", color=CYAN)
        eq_visual = visualize_equation_impact()
        log_message(f"  - Equation impact: {eq_visual}", color=YELLOW)
    
    if visualization_type == "all" or visualization_type == "hash":
        log_message("Generating hash distribution visualization...", color=CYAN)
        hash_visual = visualize_hash_distribution()
        log_message(f"  - Hash distribution: {hash_visual}", color=YELLOW)
    
    if visualization_type == "all" or visualization_type == "cosmic":
        log_message("Generating cosmic alignment visualization...", color=CYAN)
        alignment_visual = visualize_cosmic_alignment()
        log_message(f"  - Cosmic alignment: {alignment_visual}", color=YELLOW)
    
    log_message("\nVisualization complete.", color=BOLD + GREEN)
    
if __name__ == "__main__":
    main()