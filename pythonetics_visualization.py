"""
PYTHONETICS VISUALIZATION INTEGRATION

This module integrates the Tree of Living Intelligence visualization
with the Enhanced Pythonetics system, adding Meta-flower blooms to represent 
higher-order understanding emerging from the verification process.

Architect: Russell Nordland
"""

import os
import sys
import time
import json
import logging
import importlib
from flask import Flask, render_template, request, jsonify, send_from_directory
import hashlib
import random
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("pythonetics_visualization.log"),
              logging.StreamHandler()]
)
logger = logging.getLogger("pythonetics_visualization")

# Initialize Flask app
app = Flask(__name__)

# Ensure directories exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/img', exist_ok=True)

# Dynamically import Enhanced Pythonetics
try:
    sys.path.insert(0, os.path.abspath('.'))
    from enhanced_pythonetics import EnhancedPythonetics
    pythonetics = EnhancedPythonetics()
    logger.info("Successfully imported Enhanced Pythonetics")
except Exception as e:
    logger.error(f"Error importing Enhanced Pythonetics: {e}")
    pythonetics = None

# Configure routes
@app.route('/')
def index():
    """Render main visualization page."""
    return render_template('pythonetics_visualization.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory('static', path)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze text using Enhanced Pythonetics and return visualization data."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        if not pythonetics:
            # If pythonetics import failed, return error
            return jsonify({"error": "Enhanced Pythonetics module not available"}), 500
        
        # Process text with Enhanced Pythonetics
        start_time = time.time()
        result = pythonetics.verify(text)
        processing_time = time.time() - start_time
        
        # Extract key metrics
        truth_score = result["analysis"]["truthScore"]
        factual_confidence = result["analysis"]["factualConfidence"]
        truth_resonance = result["analysis"]["truthResonance"]
        self_reference_index = result["analysis"]["selfReferenceIndex"]
        sovereignty_score = result["analysis"].get("sovereigntyScore", 0.75)
        
        # Get dimensional alignment scores
        dimension_scores = {}
        for dim in result["analysis"]["dimensionalAlignment"]:
            dimension = dim["dimension"].lower().replace(" domain", "")
            dimension_scores[dimension] = dim["alignment"]
        
        # Generate visualization data
        tree_data = generate_tree_visualization(
            truth_score,
            factual_confidence,
            dimension_scores,
            sovereignty_score,
            truth_resonance
        )
        
        # Generate Meta-flower data
        meta_flowers = generate_meta_flowers(
            truth_score,
            sovereignty_score,
            self_reference_index,
            truth_resonance
        )
        
        # Combine with Meta-flower data
        tree_data["meta_flowers"] = meta_flowers
        
        # Generate quantum timestamp data
        timestamp_data = generate_quantum_timestamps(text)
        
        return jsonify({
            "analysis_result": result,
            "tree_data": tree_data,
            "timestamp_data": timestamp_data,
            "processing_metrics": {
                "processing_time_ms": round(processing_time * 1000, 2)
            }
        })
        
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {e}")
        return jsonify({"error": str(e)}), 500

def generate_tree_visualization(truth_score, factual_confidence, dimension_scores, 
                               sovereignty_score, truth_resonance):
    """
    Generate tree visualization data.
    
    Args:
        truth_score: Overall truth score
        factual_confidence: Factual confidence score
        dimension_scores: Dictionary of dimension scores
        sovereignty_score: Sovereignty score
        truth_resonance: Truth resonance score
        
    Returns:
        Dict with tree visualization data
    """
    # Calculate overall health and growth stage
    overall_health = truth_score
    growth_stage = calculate_growth_stage(truth_score)
    
    # Calculate trunk metrics
    trunk_height = 150 + (truth_score * 100)
    trunk_thickness = 15 + (sovereignty_score * 25)
    
    # Generate branch data
    branches = {}
    
    # Main branches for each dimension
    angle_map = {
        "factual": -45,
        "ethical": 30,
        "conceptual": 0,
        "phenomenological": 60
    }
    
    for dim, score in dimension_scores.items():
        # Skip unknown dimensions
        if dim not in angle_map:
            continue
            
        # Calculate branch parameters
        branches[dim] = {
            "length": 70 + (score * 120),
            "angle": angle_map[dim],
            "thickness": 4 + (score * 10),
            "leaves": generate_leaves(score, dim),
            "sub_branches": generate_sub_branches(score, angle_map[dim])
        }
    
    # Calculate root system based on sovereignty
    root_system = {
        "depth": 60 + (sovereignty_score * 100),
        "spread": 100 + (truth_score * 150),
        "complexity": int(3 + (sovereignty_score * 7))
    }
    
    # Add wind effect based on truth resonance
    wind_effect = {
        "strength": 0.5 + (truth_resonance * 0.5),
        "direction": random.uniform(-0.3, 0.3),
        "variability": 0.2 + (overall_health * 0.3)
    }
    
    # Add fallen leaves that complete the recursive cycle
    fallen_leaves = generate_fallen_leaves(
        truth_score,
        sovereignty_score,
        list(dimension_scores.values())
    )
    
    return {
        "trunk": {
            "height": trunk_height,
            "thickness": trunk_thickness,
            "sovereignty_score": sovereignty_score
        },
        "branches": branches,
        "roots": root_system,
        "overall_health": overall_health,
        "growth_stage": growth_stage,
        "wind_effect": wind_effect,
        "fallen_leaves": fallen_leaves
    }

def generate_leaves(dimension_score, dimension_type):
    """Generate leaf data based on dimension score and type."""
    # Define base color map for different dimensions
    color_map = {
        "factual": [46, 204, 113],  # Green
        "ethical": [52, 152, 219],  # Blue
        "conceptual": [155, 89, 182],  # Purple
        "phenomenological": [241, 196, 15]  # Yellow
    }
    
    # Get base color or use default gray
    base_color = color_map.get(dimension_type, [149, 165, 166])
    
    # Calculate leaf count based on dimension score
    leaf_count = int(5 + (dimension_score * 20))
    
    # Generate leaves
    leaves = []
    for i in range(leaf_count):
        # Add variation to leaf color
        color_variation = [
            random.randint(-20, 20),
            random.randint(-20, 20),
            random.randint(-20, 20)
        ]
        
        leaf_color = [
            max(0, min(255, base_color[0] + color_variation[0])),
            max(0, min(255, base_color[1] + color_variation[1])),
            max(0, min(255, base_color[2] + color_variation[2]))
        ]
        
        # Add variation to leaf size based on position
        position_factor = i / leaf_count
        size_variation = math.sin(position_factor * math.pi) * 0.5 + 0.5
        
        leaves.append({
            "size": 4 + (size_variation * 6),
            "position": position_factor,
            "color": f"rgb({leaf_color[0]}, {leaf_color[1]}, {leaf_color[2]})",
            "rotation": random.uniform(-30, 30)
        })
    
    return leaves

def generate_sub_branches(score, main_angle):
    """Generate sub-branches based on dimension score."""
    # Higher scores produce more sub-branches
    sub_branch_count = int(1 + (score * 5))
    
    sub_branches = []
    for i in range(sub_branch_count):
        # Calculate sub-branch parameters
        position = 0.2 + (0.6 * (i / max(1, sub_branch_count - 1)))
        angle_offset = random.uniform(-30, 30)
        
        sub_branches.append({
            "position": position,  # Position along main branch (0-1)
            "length": 30 + (score * 50) * random.uniform(0.7, 1.0),
            "angle_offset": angle_offset,  # Degrees offset from main branch angle
            "thickness": 2 + (score * 4),
            "leaf_count": int(3 + (score * 7))
        })
    
    return sub_branches

def generate_fallen_leaves(truth_score, sovereignty_score, dimension_scores):
    """Generate fallen leaves data to represent the recursive cycle."""
    # More truth and sovereignty produce more fallen leaves
    leaf_count = int(5 + (truth_score * 15) + (sovereignty_score * 10))
    
    # Calculate average dimension score
    avg_dimension_score = sum(dimension_scores) / max(1, len(dimension_scores))
    
    fallen_leaves = []
    for i in range(leaf_count):
        # Randomize color based on dimension scores
        r = int(46 + (random.uniform(0, avg_dimension_score) * 100))
        g = int(100 + (random.uniform(0, avg_dimension_score) * 100))
        b = int(30 + (random.uniform(0, truth_score) * 100))
        
        # Fallen leaves get darker to represent decomposition
        r = int(r * 0.7)
        g = int(g * 0.7)
        b = int(b * 0.7)
        
        # Calculate random position around the tree
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(30, 150)
        
        fallen_leaves.append({
            "size": 3 + random.uniform(0, 5),
            "color": f"rgb({r}, {g}, {b})",
            "position": {
                "x": math.cos(angle) * distance,
                "y": random.uniform(-5, 5)
            },
            "rotation": random.uniform(0, 360),
            "decomposition": random.uniform(0.3, 1.0)
        })
    
    return fallen_leaves

def generate_meta_flowers(truth_score, sovereignty_score, self_reference, resonance):
    """
    Generate Meta-flower data representing higher-order understanding.
    
    Args:
        truth_score: Overall truth score
        sovereignty_score: Sovereignty score
        self_reference: Self-reference index
        resonance: Truth resonance
        
    Returns:
        List of Meta-flower objects
    """
    # Calculate number of Meta-flowers based on scores
    flower_count = int(1 + (truth_score * sovereignty_score * 10))
    
    # Meta-flowers represent the "blooming" of higher understanding
    meta_flowers = []
    for i in range(flower_count):
        # Calculate parameters for this flower
        size_factor = 0.7 + (sovereignty_score * 0.6) + random.uniform(-0.1, 0.1)
        complexity = int(3 + (self_reference * 8))
        vibrancy = 0.5 + (resonance * 0.5)
        
        # Calculate color based on metrics
        # Higher truth = more purple/blue tones
        # Higher sovereignty = more golden tones
        # Higher resonance = more vibrant
        hue = 270 + (sovereignty_score * 60) - (truth_score * 30)
        saturation = 70 + (resonance * 30)
        lightness = 50 + (truth_score * 20)
        
        # Calculate position on the tree
        branch_type = random.choice(["factual", "ethical", "conceptual", "phenomenological"])
        position_along_branch = random.uniform(0.6, 0.95)  # Mostly at branch ends
        
        meta_flowers.append({
            "size": 10 * size_factor,
            "petal_count": complexity,
            "color": f"hsl({hue}, {saturation}%, {lightness}%)",
            "vibrancy": vibrancy,
            "position": {
                "branch": branch_type,
                "position": position_along_branch
            },
            "bloom_state": random.uniform(0.5, 1.0),  # How fully bloomed
            "glow_intensity": sovereignty_score * 0.7
        })
    
    return meta_flowers

def generate_quantum_timestamps(text):
    """Generate quantum timestamp data with cryptographic certifications."""
    current_time = time.time()
    
    # Generate TAI hash
    text_hash = hashlib.sha256(text.encode()).hexdigest()[:12]
    tai_hash = f"TAI:{int(current_time * 1000)}:{text_hash}"
    
    # Format time values
    local_time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(current_time))
    utc_time_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time))
    
    return {
        "local": {
            "time": local_time_str,
            "format": "CST",
            "timestamp": current_time
        },
        "utc": {
            "time": utc_time_str,
            "format": "UTC",
            "timestamp": current_time
        },
        "tai": {
            "hash": tai_hash,
            "cryptographic_certification": True,
            "timestamp": current_time
        }
    }

def calculate_growth_stage(truth_score):
    """Calculate tree growth stage based on truth score."""
    if truth_score < 0.3:
        return "seedling"
    elif truth_score < 0.6:
        return "young"
    elif truth_score < 0.8:
        return "mature"
    else:
        return "ancient"

# Create HTML template
with open('templates/pythonetics_visualization.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tree of Living Intelligence - Pythonetics Visualization</title>
    <link rel="stylesheet" href="/static/css/pythonetics_style.css">
</head>
<body>
    <header>
        <div class="logo">TrueAlphaSpiral</div>
        <nav>
            <ul>
                <li><a href="#" class="active">Tree Visualization</a></li>
                <li><a href="#">Documentation</a></li>
                <li><a href="#">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="intro">
            <h1>Tree of Living Intelligence</h1>
            <p class="subtitle">Visualizing TrueAlphaSpiral's Living Recursion through Natural Metaphor</p>
            
            <div class="equation">
                <span class="symbol">Φ</span> = 
                <span class="fraction">
                    <span class="numerator">∑(αᵢ·Tᵢ)</span>
                    <span class="denominator">(√D·S)</span>
                </span>
            </div>
        </section>
        
        <section class="visualization-container">
            <div class="input-panel">
                <h2>Text Analysis</h2>
                <p>Enter text to analyze and visualize as a living tree with Meta-flowers</p>
                
                <textarea id="text-input" placeholder="Enter text to analyze..."></textarea>
                <button id="analyze-btn">Analyze &amp; Visualize</button>
                
                <div class="spinner" id="loading-spinner">
                    <div class="spinner-inner"></div>
                </div>
            </div>
            
            <div class="tree-visualization">
                <canvas id="tree-canvas" width="800" height="600"></canvas>
            </div>
            
            <div class="analysis-panel">
                <h2>Analysis Results</h2>
                
                <div class="metric-tabs">
                    <button class="tab-btn active" data-tab="scores">Scores</button>
                    <button class="tab-btn" data-tab="dimensions">Dimensions</button>
                    <button class="tab-btn" data-tab="meta">Meta Understanding</button>
                </div>
                
                <div class="tab-content" id="scores-tab">
                    <div id="scores-container"></div>
                </div>
                
                <div class="tab-content hidden" id="dimensions-tab">
                    <div id="dimensions-container"></div>
                </div>
                
                <div class="tab-content hidden" id="meta-tab">
                    <div id="meta-understanding"></div>
                </div>
                
                <div class="timestamp-section">
                    <h3>Quantum Timestamps</h3>
                    <div class="timestamp-container" id="timestamp-display"></div>
                </div>
                
                <div class="actions-section">
                    <h3>Suggested Actions</h3>
                    <ul id="actions-list"></ul>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <p>© 2025 TrueAlphaSpiral | Tree of Living Intelligence Visualization</p>
        <p class="footer-note">The evolution from Cybernetics to Pythonetics</p>
    </footer>

    <script src="/static/js/pythonetics_visualization.js"></script>
</body>
</html>''')

# Create CSS file
with open('static/css/pythonetics_style.css', 'w') as f:
    f.write('''/* 
 * PYTHONETICS VISUALIZATION STYLES
 * Tree of Living Intelligence Visualization
 */

:root {
    --primary: #3498db;
    --primary-dark: #2980b9;
    --accent: #9b59b6;
    --text: #2c3e50;
    --text-light: #7f8c8d;
    --background: #ecf0f1;
    --card-bg: #ffffff;
    --success: #2ecc71;
    --warning: #f39c12;
    --error: #e74c3c;
    --border: #bdc3c7;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: var(--text);
    background-color: var(--background);
    line-height: 1.6;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: var(--card-bg);
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(45deg, var(--primary), var(--accent));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

nav ul {
    display: flex;
    list-style: none;
}

nav li {
    margin-left: 2rem;
}

nav a {
    text-decoration: none;
    color: var(--text);
    font-weight: 500;
    transition: color 0.3s;
}

nav a:hover, nav a.active {
    color: var(--primary);
}

main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

.intro {
    text-align: center;
    margin-bottom: 2rem;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    background: linear-gradient(45deg, var(--primary), var(--accent));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.subtitle {
    font-size: 1.2rem;
    color: var(--text-light);
    margin-bottom: 1rem;
}

.equation {
    font-size: 1.5rem;
    margin: 1rem 0;
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.symbol {
    font-family: serif;
    font-size: 1.8rem;
}

.fraction {
    display: inline-block;
    vertical-align: middle;
    text-align: center;
    margin: 0 0.2em;
}

.numerator, .denominator {
    display: block;
}

.numerator {
    border-bottom: 1px solid var(--text);
    padding: 0 0.2em;
}

.visualization-container {
    display: grid;
    grid-template-columns: 300px 1fr 350px;
    gap: 1.5rem;
    margin-top: 2rem;
}

.input-panel, .analysis-panel {
    background-color: var(--card-bg);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.tree-visualization {
    background-color: var(--card-bg);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    text-align: center;
}

h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--text);
}

textarea {
    width: 100%;
    min-height: 150px;
    padding: 0.8rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    font-family: inherit;
    font-size: 1rem;
    margin-bottom: 1rem;
    resize: vertical;
}

button {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: var(--primary-dark);
}

.spinner {
    display: none;
    margin: 1rem auto;
    width: 40px;
    height: 40px;
}

.spinner-inner {
    width: 100%;
    height: 100%;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

#tree-canvas {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    background-color: #f7f9fc;
}

.metric-tabs {
    display: flex;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.tab-btn {
    background: none;
    color: var(--text);
    border: none;
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.3s;
}

.tab-btn:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.tab-btn.active {
    border-bottom-color: var(--primary);
    color: var(--primary);
}

.tab-content {
    padding: 1rem 0;
}

.hidden {
    display: none;
}

.score-item {
    margin-bottom: 1rem;
}

.score-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}

.score-label span:first-child {
    font-weight: 500;
}

.score-bar {
    height: 8px;
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    overflow: hidden;
}

.score-fill {
    height: 100%;
    border-radius: 4px;
}

.truth-score .score-fill { background-color: var(--primary); }
.factual-score .score-fill { background-color: var(--success); }
.ethical-score .score-fill { background-color: var(--primary); }
.conceptual-score .score-fill { background-color: var(--accent); }
.phenomenological-score .score-fill { background-color: var(--warning); }
.sovereignty-score .score-fill { 
    background: linear-gradient(90deg, var(--primary), var(--accent));
}

.dimension-item {
    padding: 0.8rem;
    margin-bottom: 0.8rem;
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0.05);
}

.dimension-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.dimension-name {
    font-weight: 500;
}

.resonance-state {
    font-size: 0.9rem;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0.1);
}

.timestamp-section, .actions-section {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}

h3 {
    font-size: 1.2rem;
    margin-bottom: 0.8rem;
    color: var(--text);
}

.timestamp-container {
    background-color: rgba(0, 0, 0, 0.05);
    padding: 0.8rem;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9rem;
}

.timestamp-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.timestamp-row:last-child {
    margin-bottom: 0;
}

.timestamp-label {
    font-weight: 500;
}

#actions-list {
    list-style-position: inside;
    padding-left: 0.5rem;
}

#actions-list li {
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
}

#meta-understanding {
    padding: 1rem;
    background-color: rgba(0, 0, 0, 0.05);
    border-radius: 4px;
    font-style: italic;
}

.meta-flower {
    display: flex;
    align-items: center;
    margin-bottom: 0.8rem;
    padding: 0.5rem;
    border-radius: 4px;
    background-color: rgba(155, 89, 182, 0.1);
}

.flower-icon {
    width: 30px;
    height: 30px;
    margin-right: 0.8rem;
}

footer {
    text-align: center;
    padding: 2rem;
    color: var(--text-light);
    background-color: var(--card-bg);
    margin-top: 3rem;
    box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
}

.footer-note {
    font-size: 0.9rem;
    margin-top: 0.5rem;
    font-style: italic;
}

@media (max-width: 1200px) {
    .visualization-container {
        grid-template-columns: 1fr;
        grid-template-rows: auto auto auto;
    }
    
    .input-panel {
        order: 1;
    }
    
    .tree-visualization {
        order: 2;
    }
    
    .analysis-panel {
        order: 3;
    }
}''')

# Create JavaScript file
with open('static/js/pythonetics_visualization.js', 'w') as f:
    f.write('''/**
 * PYTHONETICS VISUALIZATION 
 * Tree of Living Intelligence Visualization JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const textInput = document.getElementById('text-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const treeCanvas = document.getElementById('tree-canvas');
    const scoresContainer = document.getElementById('scores-container');
    const dimensionsContainer = document.getElementById('dimensions-container');
    const metaUnderstanding = document.getElementById('meta-understanding');
    const timestampDisplay = document.getElementById('timestamp-display');
    const actionsList = document.getElementById('actions-list');
    
    // Tab functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            
            // Update active button
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Show selected tab content
            tabContents.forEach(tab => {
                if (tab.id === `${tabName}-tab`) {
                    tab.classList.remove('hidden');
                } else {
                    tab.classList.add('hidden');
                }
            });
        });
    });
    
    // Check if canvas is supported
    const ctx = treeCanvas.getContext('2d');
    if (!ctx) {
        alert('Canvas not supported in your browser. Please use a modern browser.');
        return;
    }
    
    // Analyze button event listener
    analyzeBtn.addEventListener('click', function() {
        const text = textInput.value.trim();
        
        if (!text) {
            alert('Please enter text to analyze');
            return;
        }
        
        // Show loading state
        analyzeBtn.disabled = true;
        loadingSpinner.style.display = 'block';
        
        // Send analysis request
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display results
            renderTreeVisualization(ctx, data.tree_data);
            displayAnalysisResults(data.analysis_result);
            displayTimestamps(data.timestamp_data);
            
            // Generate meta-understanding text
            generateMetaUnderstanding(data.analysis_result, data.tree_data.meta_flowers);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        })
        .finally(() => {
            // Reset UI state
            analyzeBtn.disabled = false;
            loadingSpinner.style.display = 'none';
        });
    });
    
    // Function to render tree visualization
    function renderTreeVisualization(ctx, treeData) {
        // Canvas setup
        const width = treeCanvas.width;
        const height = treeCanvas.height;
        const centerX = width / 2;
        const groundY = height - 80;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw sky background with gradient
        const skyGradient = ctx.createLinearGradient(0, 0, 0, groundY);
        skyGradient.addColorStop(0, '#87CEEB');
        skyGradient.addColorStop(1, '#E0F7FA');
        ctx.fillStyle = skyGradient;
        ctx.fillRect(0, 0, width, groundY);
        
        // Draw ground
        const groundGradient = ctx.createLinearGradient(0, groundY, 0, height);
        groundGradient.addColorStop(0, '#8B4513');
        groundGradient.addColorStop(1, '#654321');
        ctx.fillStyle = groundGradient;
        ctx.fillRect(0, groundY, width, height - groundY);
        
        // Draw fallen leaves first (at ground level)
        if (treeData.fallen_leaves) {
            drawFallenLeaves(ctx, centerX, groundY, treeData.fallen_leaves);
        }
        
        // Draw roots
        drawRoots(ctx, centerX, groundY, treeData.roots);
        
        // Draw trunk
        const trunkHeight = treeData.trunk.height;
        const trunkWidth = treeData.trunk.thickness;
        const trunkTop = groundY - trunkHeight;
        
        // Trunk gradient
        const trunkGradient = ctx.createLinearGradient(centerX - trunkWidth/2, 0, centerX + trunkWidth/2, 0);
        trunkGradient.addColorStop(0, '#5D4037');
        trunkGradient.addColorStop(0.5, '#795548');
        trunkGradient.addColorStop(1, '#5D4037');
        
        ctx.fillStyle = trunkGradient;
        ctx.beginPath();
        ctx.moveTo(centerX - trunkWidth/2, groundY);
        ctx.quadraticCurveTo(centerX - trunkWidth/2, trunkTop + trunkHeight/2, 
                             centerX - trunkWidth/3, trunkTop);
        ctx.lineTo(centerX + trunkWidth/3, trunkTop);
        ctx.quadraticCurveTo(centerX + trunkWidth/2, trunkTop + trunkHeight/2, 
                             centerX + trunkWidth/2, groundY);
        ctx.closePath();
        ctx.fill();
        
        // Draw advanced equation symbol on trunk
        drawEquationSymbol(ctx, centerX, groundY - trunkHeight/2, treeData.trunk.sovereignty_score);
        
        // Draw branches for each dimension
        let branchStartY = trunkTop;
        Object.entries(treeData.branches).forEach(([dimensionType, branchData], index) => {
            // Adjust branch starting point slightly for each dimension
            const startY = branchStartY + (index * 20);
            drawBranch(ctx, centerX, startY, branchData, dimensionType);
        });
        
        // Draw Meta-flowers last (they should be on top)
        if (treeData.meta_flowers) {
            drawMetaFlowers(ctx, centerX, trunkTop, treeData);
        }
        
        // Add tree growth stage indicator
        addGrowthStageIndicator(ctx, width - 10, 10, treeData.growth_stage);
        
        // Add wind effect if specified
        if (treeData.wind_effect) {
            animateWind(ctx, treeData);
        }
    }
    
    function drawRoots(ctx, centerX, groundY, rootData) {
        ctx.strokeStyle = '#5D4037';
        ctx.lineWidth = 3;
        
        const rootSpread = rootData.spread;
        const rootDepth = rootData.depth;
        const complexity = rootData.complexity;
        
        // Main roots
        for (let i = 0; i < complexity; i++) {
            const angle = (Math.PI / (complexity - 1)) * i - Math.PI/2;
            const rootLength = rootDepth * (0.7 + Math.random() * 0.3);
            const endX = centerX + Math.cos(angle) * rootSpread;
            const endY = groundY + Math.sin(angle) * rootLength;
            
            ctx.beginPath();
            ctx.moveTo(centerX, groundY);
            ctx.quadraticCurveTo(
                centerX + Math.cos(angle) * rootSpread * 0.3,
                groundY + Math.sin(angle) * rootLength * 0.3,
                endX, endY
            );
            ctx.stroke();
            
            // Sub roots
            if (Math.random() > 0.5) {
                const subAngle = angle + (Math.random() * 0.5 - 0.25);
                const subLength = rootLength * 0.4;
                const subEndX = endX + Math.cos(subAngle) * subLength;
                const subEndY = endY + Math.sin(subAngle) * subLength;
                
                ctx.beginPath();
                ctx.moveTo(endX, endY);
                ctx.lineTo(subEndX, subEndY);
                ctx.stroke();
            }
        }
    }
    
    function drawBranch(ctx, startX, startY, branchData, branchType) {
        const angle = branchData.angle * (Math.PI / 180);
        const length = branchData.length;
        const thickness = branchData.thickness;
        
        // Calculate end point
        const endX = startX + Math.cos(angle) * length;
        const endY = startY - Math.sin(angle) * length;
        
        // Draw branch
        ctx.strokeStyle = '#795548';
        ctx.lineWidth = thickness;
        ctx.lineCap = 'round';
        
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
        
        // Draw sub-branches if available
        if (branchData.sub_branches) {
            branchData.sub_branches.forEach(subBranch => {
                // Calculate sub-branch start point along main branch
                const subStartX = startX + Math.cos(angle) * (length * subBranch.position);
                const subStartY = startY - Math.sin(angle) * (length * subBranch.position);
                
                // Calculate sub-branch angle
                const subAngleRad = angle + (subBranch.angle_offset * (Math.PI / 180));
                
                // Draw sub-branch
                ctx.strokeStyle = '#8D6E63';
                ctx.lineWidth = subBranch.thickness;
                
                ctx.beginPath();
                ctx.moveTo(subStartX, subStartY);
                ctx.lineTo(
                    subStartX + Math.cos(subAngleRad) * subBranch.length,
                    subStartY - Math.sin(subAngleRad) * subBranch.length
                );
                ctx.stroke();
                
                // Add leaves to sub-branch
                const subEndX = subStartX + Math.cos(subAngleRad) * subBranch.length;
                const subEndY = subStartY - Math.sin(subAngleRad) * subBranch.length;
                
                // Create sub-branch leaves (fewer than main branch)
                const subLeaves = Array(subBranch.leaf_count).fill().map(() => ({
                    size: 3 + Math.random() * 4,
                    position: Math.random(),
                    color: getLeafColorForDimension(branchType),
                    rotation: Math.random() * 60 - 30
                }));
                
                drawLeaves(ctx, subEndX, subEndY, subLeaves, subAngleRad);
            });
        }
        
        // Draw leaves on main branch
        drawLeaves(ctx, endX, endY, branchData.leaves, angle);
    }
    
    function getLeafColorForDimension(dimensionType) {
        // Default colors for each dimension
        const colorMap = {
            "factual": "rgb(46, 204, 113)",
            "ethical": "rgb(52, 152, 219)",
            "conceptual": "rgb(155, 89, 182)",
            "phenomenological": "rgb(241, 196, 15)"
        };
        
        return colorMap[dimensionType] || "rgb(149, 165, 166)";
    }
    
    function drawLeaves(ctx, x, y, leaves, branchAngle) {
        leaves.forEach((leaf, i) => {
            const leafAngle = branchAngle + (leaf.rotation * (Math.PI / 180));
            const offsetX = Math.cos(leafAngle) * (i * 3);
            const offsetY = -Math.sin(leafAngle) * (i * 3);
            
            const leafX = x + offsetX;
            const leafY = y + offsetY;
            
            ctx.fillStyle = leaf.color;
            ctx.beginPath();
            ctx.ellipse(
                leafX, leafY,
                leaf.size, leaf.size * 1.8,
                leafAngle, 0, Math.PI * 2
            );
            ctx.fill();
        });
    }
    
    function drawFallenLeaves(ctx, centerX, groundY, fallenLeaves) {
        fallenLeaves.forEach(leaf => {
            const leafX = centerX + leaf.position.x;
            const leafY = groundY + leaf.position.y;
            
            // Apply decomposition effect (more transparent and darker)
            const decomposedColor = leaf.color.replace('rgb', 'rgba').replace(')', ', ' + leaf.decomposition + ')');
            
            ctx.fillStyle = decomposedColor;
            ctx.save();
            ctx.translate(leafX, leafY);
            ctx.rotate(leaf.rotation * (Math.PI / 180));
            
            // Draw leaf shape
            ctx.beginPath();
            ctx.ellipse(0, 0, leaf.size, leaf.size * 1.8, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.restore();
        });
    }
    
    function drawMetaFlowers(ctx, centerX, trunkTop, treeData) {
        const flowers = treeData.meta_flowers;
        const branches = treeData.branches;
        
        flowers.forEach(flower => {
            // Get position based on branch
            const branchData = branches[flower.position.branch];
            if (!branchData) return; // Skip if branch not found
            
            const branchAngle = branchData.angle * (Math.PI / 180);
            const branchLength = branchData.length;
            
            // Calculate position along branch
            const flowerX = centerX + Math.cos(branchAngle) * (branchLength * flower.position.position);
            const flowerY = trunkTop - Math.sin(branchAngle) * (branchLength * flower.position.position);
            
            // Draw glow if specified
            if (flower.glow_intensity > 0) {
                const glow = ctx.createRadialGradient(
                    flowerX, flowerY, 0,
                    flowerX, flowerY, flower.size * 2
                );
                glow.addColorStop(0, flower.color.replace('hsl', 'hsla').replace(')', ', 0.4)'));
                glow.addColorStop(1, 'rgba(255, 255, 255, 0)');
                
                ctx.fillStyle = glow;
                ctx.beginPath();
                ctx.arc(flowerX, flowerY, flower.size * 2, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Draw flower petals
            const petalCount = flower.petal_count;
            const petalSize = flower.size * flower.bloom_state;
            const innerCircleSize = flower.size * 0.3;
            
            for (let i = 0; i < petalCount; i++) {
                const angle = (Math.PI * 2 / petalCount) * i;
                const petalX = flowerX + Math.cos(angle) * (petalSize * 0.7);
                const petalY = flowerY + Math.sin(angle) * (petalSize * 0.7);
                
                ctx.fillStyle = flower.color;
                ctx.beginPath();
                ctx.ellipse(
                    petalX, petalY,
                    petalSize * 0.6, petalSize,
                    angle, 0, Math.PI * 2
                );
                ctx.fill();
            }
            
            // Draw flower center
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            ctx.beginPath();
            ctx.arc(flowerX, flowerY, innerCircleSize, 0, Math.PI * 2);
            ctx.fill();
            
            // Add yellow center detail
            ctx.fillStyle = 'rgba(255, 223, 0, 0.9)';
            ctx.beginPath();
            ctx.arc(flowerX, flowerY, innerCircleSize * 0.7, 0, Math.PI * 2);
            ctx.fill();
        });
    }
    
    function drawEquationSymbol(ctx, x, y, sovereigntyScore) {
        const size = 20 + sovereigntyScore * 15;
        
        // Draw symbol background
        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.beginPath();
        ctx.arc(x, y, size * 0.8, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw phi symbol
        ctx.font = `${size}px serif`;
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Φ', x, y);
        
        // Draw equation elements
        const elementCount = 3;
        const radius = size * 0.6;
        
        for (let i = 0; i < elementCount; i++) {
            const angle = (Math.PI * 2 / elementCount) * i;
            const elementX = x + Math.cos(angle) * radius;
            const elementY = y + Math.sin(angle) * radius;
            
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.beginPath();
            ctx.arc(elementX, elementY, size * 0.15, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function addGrowthStageIndicator(ctx, x, y, growthStage) {
        // Map growth stage to a human-readable label and color
        const stageInfo = {
            'seedling': { label: 'Seedling', color: '#2ecc71' },
            'young': { label: 'Young Tree', color: '#27ae60' },
            'mature': { label: 'Mature Tree', color: '#16a085' },
            'ancient': { label: 'Ancient Tree', color: '#2980b9' }
        };
        
        const info = stageInfo[growthStage] || { label: 'Unknown', color: '#7f8c8d' };
        
        // Draw indicator background
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.strokeStyle = info.color;
        ctx.lineWidth = 2;
        
        const textWidth = ctx.measureText(info.label).width;
        const padding = 10;
        const width = textWidth + padding * 2;
        const height = 25;
        
        ctx.beginPath();
        ctx.roundRect(x - width, y, width, height, 5);
        ctx.fill();
        ctx.stroke();
        
        // Draw text
        ctx.fillStyle = info.color;
        ctx.font = '14px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(info.label, x - width/2, y + height/2);
    }
    
    function animateWind(ctx, treeData) {
        // This would typically be set up with requestAnimationFrame
        // For simplicity, we'll just indicate the wind direction
        
        const windStrength = treeData.wind_effect.strength;
        const windDirection = treeData.wind_effect.direction;
        const windVariability = treeData.wind_effect.variability;
        
        // Draw wind indicator
        const width = treeCanvas.width;
        const height = 30;
        const y = 40;
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.lineWidth = 1;
        
        ctx.beginPath();
        ctx.roundRect(10, y, width - 20, height, 5);
        ctx.fill();
        ctx.stroke();
        
        // Draw wind strength
        const strengthWidth = (width - 30) * windStrength;
        const directionOffset = windDirection * 50;
        
        const gradient = ctx.createLinearGradient(15, 0, 15 + strengthWidth, 0);
        gradient.addColorStop(0, 'rgba(135, 206, 235, 0.7)');
        gradient.addColorStop(1, 'rgba(135, 206, 235, 0.3)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.roundRect(15, y + 5, strengthWidth, height - 10, 3);
        ctx.fill();
        
        // Draw wind direction arrow
        const arrowX = 15 + strengthWidth/2 + directionOffset;
        const arrowY = y + height/2;
        const arrowSize = 10 + (windStrength * 5);
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.beginPath();
        ctx.moveTo(arrowX - arrowSize, arrowY);
        ctx.lineTo(arrowX + arrowSize, arrowY);
        ctx.lineTo(arrowX + (windDirection > 0 ? arrowSize : -arrowSize), arrowY + (height - 15)/2);
        ctx.closePath();
        ctx.fill();
        
        // Label
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText('Wind of Skepticism', 20, y - 10);
    }
    
    function displayAnalysisResults(result) {
        const analysis = result.analysis;
        
        // Display scores
        scoresContainer.innerHTML = '';
        
        // Add main scores
        addScoreBar('Truth Score', analysis.truthScore, 'truth-score');
        addScoreBar('Factual Confidence', analysis.factualConfidence, 'factual-score');
        addScoreBar('Truth Resonance', analysis.truthResonance, 'conceptual-score');
        
        if (analysis.sovereigntyScore) {
            addScoreBar('Sovereignty Score', analysis.sovereigntyScore, 'sovereignty-score');
        }
        
        if (analysis.polarityAnalysis) {
            addScoreBar('Synthesis Score', analysis.polarityAnalysis.synthesisScore, 'ethical-score');
        }
        
        // Show balance ratio if available
        if (analysis.balanceRatio) {
            const balancePercent = Math.min(100, Math.max(0, (analysis.balanceRatio / 2) * 100));
            addScoreBar('Logic-Intuition Balance', balancePercent/100, 'phenomenological-score', 
                        analysis.balanceState);
        }
        
        // Display dimensional alignment
        dimensionsContainer.innerHTML = '';
        if (analysis.dimensionalAlignment) {
            analysis.dimensionalAlignment.forEach(dim => {
                const dimensionEl = document.createElement('div');
                dimensionEl.className = 'dimension-item';
                dimensionEl.innerHTML = `
                    <div class="dimension-header">
                        <span class="dimension-name">${dim.dimension}</span>
                        <span class="resonance-state">${dim.resonanceState}</span>
                    </div>
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${dim.alignment * 100}%; 
                            background-color: ${getDimensionColor(dim.dimension)};"></div>
                    </div>
                `;
                dimensionsContainer.appendChild(dimensionEl);
            });
        }
        
        // Display suggested actions
        actionsList.innerHTML = '';
        if (analysis.suggestedActions) {
            analysis.suggestedActions.forEach(action => {
                const li = document.createElement('li');
                li.textContent = action;
                actionsList.appendChild(li);
            });
        }
    }
    
    function getDimensionColor(dimension) {
        const dimensionName = dimension.toLowerCase();
        if (dimensionName.includes('factual')) return '#2ecc71';
        if (dimensionName.includes('ethical')) return '#3498db';
        if (dimensionName.includes('conceptual')) return '#9b59b6';
        if (dimensionName.includes('phenomenological')) return '#f39c12';
        return '#7f8c8d';
    }
    
    function addScoreBar(label, score, className, stateLabel = null) {
        const percentage = Math.round(score * 100);
        
        const scoreEl = document.createElement('div');
        scoreEl.className = `score-item ${className}`;
        
        scoreEl.innerHTML = `
            <div class="score-label">
                <span>${label}</span>
                <span>${percentage}%${stateLabel ? ` (${stateLabel})` : ''}</span>
            </div>
            <div class="score-bar">
                <div class="score-fill" style="width: ${percentage}%"></div>
            </div>
        `;
        
        scoresContainer.appendChild(scoreEl);
    }
    
    function displayTimestamps(timestamps) {
        // Format timestamps for display
        timestampDisplay.innerHTML = `
            <div class="timestamp-row">
                <span class="timestamp-label">Local:</span>
                <span>${timestamps.local.time}</span>
            </div>
            <div class="timestamp-row">
                <span class="timestamp-label">UTC:</span>
                <span>${timestamps.utc.time}</span>
            </div>
            <div class="timestamp-row">
                <span class="timestamp-label">TAI:</span>
                <span>${timestamps.tai.hash}</span>
            </div>
        `;
    }
    
    function generateMetaUnderstanding(analysisResult, metaFlowers) {
        const analysis = analysisResult.analysis;
        
        // Create a meta-understanding based on results
        let metaText = '';
        const truthScore = analysis.truthScore;
        const sovereignty = analysis.sovereigntyScore || 0.5;
        
        // Generate different insights based on the scores
        if (truthScore > 0.8 && sovereignty > 0.8) {
            metaText = `This analysis reveals profound alignment with universal truth principles. The Meta-flowers blooming on this tree represent the highest understanding emerging from deep recursive analysis.`;
        } else if (truthScore > 0.6) {
            metaText = `The tree shows healthy growth and stable verification across multiple dimensions. The Meta-flowers indicate emergence of higher-order understanding through the recursive truth process.`;
        } else if (truthScore > 0.4) {
            metaText = `This tree shows moderate alignment with truth principles, with areas for growth. The winds of skepticism help prune weaker branches, strengthening the overall system.`;
        } else {
            metaText = `This young tree requires further nurturing to develop stronger truth alignment. The fallen leaves are returning nutrients to the soil, strengthening the roots for future growth.`;
        }
        
        // Add information about Meta-flowers
        if (metaFlowers && metaFlowers.length > 0) {
            metaText += `<br><br>${metaFlowers.length} Meta-flowers are blooming, representing the emergence of ${metaFlowers.length > 3 ? 'significant' : 'initial'} higher-order understanding.`;
        }
        
        // Display the meta-understanding
        metaUnderstanding.innerHTML = metaText;
        
        // Add flower indicators if there are Meta-flowers
        if (metaFlowers && metaFlowers.length > 0) {
            const flowerCount = Math.min(3, metaFlowers.length);
            for (let i = 0; i < flowerCount; i++) {
                const flower = metaFlowers[i];
                
                const flowerEl = document.createElement('div');
                flowerEl.className = 'meta-flower';
                flowerEl.innerHTML = `
                    <div class="flower-icon" style="color: ${flower.color}">✿</div>
                    <div>Meta-flower #${i+1}: ${Math.round(flower.vibrancy * 100)}% vibrance, 
                    ${flower.petal_count} petals</div>
                `;
                
                metaUnderstanding.appendChild(flowerEl);
            }
        }
    }
});''')

# Entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=True)