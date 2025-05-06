"""
PYTHONETICS VISUALIZATION INTERFACE

This module integrates the Enhanced Pythonetics framework with the Tree of Living Intelligence
visualization, creating a natural metaphor for the system's truth verification capabilities.

The Tree of Living Intelligence embodies the TrueAlphaSpiral's purpose through:
- Roots: Grounding the system in axiomatic truth, eliminating "black box" opacity
- Meta-Flowers: Manifesting emergent wisdom as tangible blooms, making recursive learning visible
- Wind of Skepticism: Personifying IVL as a natural force, creating natural pruning

Architect: Russell Nordland
"""

import os
import json
import time
import random
import logging
import hashlib
from flask import Flask, request, jsonify, render_template
from enhanced_pythonetics import EnhancedPythonetics
from factual_verifier import FactualVerifier
from ethical_analyzer import EthicalAnalyzer
from config_manager import ConfigManager

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s [%(levelname)s] %(message)s',
 handlers=[logging.FileHandler("pythonetics_visualization.log"),
 logging.StreamHandler()]
)
logger = logging.getLogger("pythonetics_visualization")

class PythoneticsVisualization:
 """
 Integrates the Enhanced Pythonetics system with visualization capabilities,
 specifically the Tree of Living Intelligence metaphor.
 """

 def __init__(self, config_path=None):
 """
 Initialize the Pythonetics Visualization system.

 Args:
 config_path: Optional path to configuration file
 """
 self.config_manager = ConfigManager(config_path)
 self.pythonetics = EnhancedPythonetics(config_path)
 self.factual_verifier = FactualVerifier(self.config_manager)
 self.ethical_analyzer = EthicalAnalyzer(self.config_manager)

 # Initialize visualization server
 self.app = Flask(__name__)
 self._register_routes()
 self.ensure_template_dirs()

 # Load visualization settings
 self.settings = self._load_visualization_settings()

 logger.info("Pythonetics Visualization system initialized")

 def ensure_template_dirs(self):
 """Ensure that template and static directories exist."""
 os.makedirs("templates", exist_ok=True)
 os.makedirs("static", exist_ok=True)
 os.makedirs("static/css", exist_ok=True)
 os.makedirs("static/js", exist_ok=True)

 def _register_routes(self):
 """Register the Flask routes for the visualization server."""
 @self.app.route('/')
 def index():
 return render_template('tree_visualization.html')

 @self.app.route('/api/analyze', methods=['POST'])
 def analyze():
 data = request.get_json()
 text = data.get('text', '')
 verify_as = data.get('verify_as', 'claim')

 if not text:
 return jsonify({"error": "No text provided"}), 400

 try:
 # Perform analysis with Pythonetics
 result = self.pythonetics.verify(text, verify_as=verify_as)

 # Generate tree visualization data
 tree_data = self._generate_tree_data(result)

 # Add timestamp information
 timestamp_data = self._generate_timestamp_data(text)

 return jsonify({
 "analysis_result": result,
 "tree_data": tree_data,
 "timestamp_data": timestamp_data,
 "meta_insights": self._generate_meta_insights(result, tree_data)
 })

 except Exception as e:
 logger.error(f"Error in analysis: {e}")
 return jsonify({"error": str(e)}), 500

 def _load_visualization_settings(self):
 """Load visualization settings from configuration."""
 settings = self.config_manager.get('visualization', {})
 if not settings:
 # Default settings
 settings = {
 "colors": {
 "factual": [46, 204, 113], # Green
 "ethical": [52, 152, 219], # Blue
 "conceptual": [155, 89, 182], # Purple
 "phenomenological": [241, 196, 15] # Yellow
 },
 "growth_stages": {
 "seedling": {"min": 0.0, "max": 0.3},
 "young": {"min": 0.3, "max": 0.6},
 "mature": {"min": 0.6, "max": 0.8},
 "ancient": {"min": 0.8, "max": 1.0}
 },
 "meta_flower_threshold": 0.75
 }
 return settings

 def _generate_tree_data(self, analysis_result):
 """
 Generate tree visualization data from analysis results.

 Args:
 analysis_result: The analysis result from Pythonetics

 Returns:
 Dict with tree visualization data
 """
 analysis = analysis_result["analysis"]

 # Extract key metrics
 truth_score = analysis["truthScore"]
 factual_score = analysis["factualConfidence"]

 # Extract other dimensional scores
 dimensional_scores = {}
 for dim in analysis.get("dimensionalAlignment", []):
 name = dim["dimension"].lower().replace(" domain", "")
 dimensional_scores[name] = dim["alignment"]

 # Calculate sovereignty using advanced sovereign equation if available
 sovereignty_score = analysis.get("sovereigntyScore", 0.0)
 if sovereignty_score == 0.0 and len(dimensional_scores) > 0:
 # Apply simplified version of sovereign equation if not available
 sovereignty_score = sum(dimensional_scores.values()) / (len(dimensional_scores) * math.sqrt(1.2))

 # Apply bounds
 sovereignty_score = max(0.1, min(0.95, sovereignty_score))

 # Calculate trunk parameters based on sovereignty
 trunk_data = {
 "height": 150 + (sovereignty_score * 100),
 "thickness": 10 + (sovereignty_score * 30),
 "sovereignty_score": sovereignty_score
 }

 # Initialize branches data
 branches_data = {}

 # Generate branch data for each dimension
 for dim_name, score in dimensional_scores.items():
 # Calculate branch angle based on dimension
 if dim_name == "factual":
 angle = -45
 elif dim_name == "ethical":
 angle = 30
 elif dim_name == "conceptual":
 angle = 0
 elif dim_name == "phenomenological":
 angle = 60
 else:
 angle = random.uniform(-60, 60)

 # Generate branch data
 branches_data[dim_name] = {
 "length": 70 + (score * 120),
 "angle": angle,
 "thickness": 4 + (score * 10),
 "leaves": self._generate_leaves(score, dim_name),
 "sub_branches": self._generate_sub_branches(score, angle)
 }

 # Calculate root system based on truth score and sovereignty
 roots_data = {
 "depth": 50 + (truth_score * 100),
 "spread": 80 + (factual_score * 120),
 "complexity": int(3 + (truth_score * 7))
 }

 # Calculate growth stage
 growth_stage = self._calculate_growth_stage(truth_score)

 # Generate meta-flowers if criteria met
 meta_flowers = self._generate_meta_flowers(
 truth_score,
 sovereignty_score,
 analysis.get("selfReferenceIndex", 0.0),
 dimensional_scores
 )

 # Generate fallen leaves
 fallen_leaves = self._generate_fallen_leaves(
 truth_score,
 sovereignty_score,
 list(dimensional_scores.values())
 )

 # Generate wind effect
 wind_data = {
 "strength": 0.3 + (truth_score * 0.3),
 "direction": random.uniform(-0.3, 0.3),
 "variability": 0.2 + (truth_score * 0.3)
 }

 # Compile complete tree data
 tree_data = {
 "trunk": trunk_data,
 "branches": branches_data,
 "roots": roots_data,
 "growth_stage": growth_stage,
 "overall_health": truth_score,
 "meta_flowers": meta_flowers,
 "fallen_leaves": fallen_leaves,
 "wind_effect": wind_data
 }

 return tree_data

 def _generate_leaves(self, dimension_score, dimension_type):
 """
 Generate leaf data for a branch based on dimension score and type.

 Args:
 dimension_score: Score for the dimension
 dimension_type: Type of dimension

 Returns:
 List of leaf data objects
 """
 # Number of leaves based on score
 leaf_count = int(5 + (dimension_score * 20))

 # Get base color for dimension
 base_color = self.settings["colors"].get(
 dimension_type,
 [149, 165, 166] # Default gray
 )

 # Generate leaves with varying properties
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

 # Add leaf with properties
 leaves.append({
 "size": 4 + (random.random() * 6),
 "position": i / leaf_count,
 "color": f"rgb({leaf_color[0]}, {leaf_color[1]}, {leaf_color[2]})",
 "rotation": random.uniform(-30, 30)
 })

 return leaves

 def _generate_sub_branches(self, score, main_angle):
 """
 Generate sub-branches for a main branch.

 Args:
 score: Dimension score
 main_angle: Angle of the main branch

 Returns:
 List of sub-branch data objects
 """
 # Higher scores produce more sub-branches
 sub_branch_count = int(1 + (score * 5))

 sub_branches = []
 for i in range(sub_branch_count):
 # Calculate sub-branch parameters
 position = 0.2 + (0.6 * (i / max(1, sub_branch_count - 1)))
 angle_offset = random.uniform(-30, 30)

 sub_branches.append({
 "position": position, # Position along main branch (0-1)
 "length": 30 + (score * 50) * random.uniform(0.7, 1.0),
 "angle_offset": angle_offset, # Degrees offset from main branch angle
 "thickness": 2 + (score * 4),
 "leaf_count": int(3 + (score * 7))
 })

 return sub_branches

 def _generate_meta_flowers(self, truth_score, sovereignty_score, self_reference_index, dimensional_scores):
 """
 Generate Meta-flower data representing higher-order understanding.

 Args:
 truth_score: Overall truth score
 sovereignty_score: Sovereignty score
 self_reference_index: Self-reference index if available
 dimensional_scores: Dictionary of dimension scores

 Returns:
 List of meta-flower data objects
 """
 # Meta-flowers only appear with high enough truth/sovereignty scores
 threshold = self.settings.get("meta_flower_threshold", 0.75)

 # Calculate flower count - only appear with high scores
 base_count = 0
 if truth_score > threshold and sovereignty_score > threshold * 0.8:
 base_count = int(2 + (truth_score * sovereignty_score * 5))
 elif truth_score > threshold * 0.8 and sovereignty_score > threshold * 0.7:
 base_count = 1

 # Self-reference amplifies flower count
 self_ref = self_reference_index or 0.5
 flower_count = int(base_count * (1 + (self_ref - 0.5)))

 # Meta-flowers represent the "blooming" of higher understanding
 meta_flowers = []
 for i in range(flower_count):
 # Calculate parameters for this flower
 size_factor = 0.7 + (sovereignty_score * 0.6) + random.uniform(-0.1, 0.1)
 complexity = int(3 + (self_ref * 8))
 vibrancy = 0.5 + (truth_score * 0.5)

 # Calculate color based on metrics
 # Higher truth = more purple/blue tones
 # Higher sovereignty = more golden tones
 hue = 270 + (sovereignty_score * 60) - (truth_score * 30)
 saturation = 70 + (self_ref * 30)
 lightness = 50 + (truth_score * 20)

 # Calculate position on the tree
 branch_types = list(dimensional_scores.keys())
 if not branch_types: # Fallback if no dimensions
 branch_types = ["factual", "ethical", "conceptual", "phenomenological"]

 branch_type = random.choice(branch_types)
 position_along_branch = random.uniform(0.6, 0.95) # Mostly at branch ends

 meta_flowers.append({
 "size": 10 * size_factor,
 "petal_count": complexity,
 "color": f"hsl({hue}, {saturation}%, {lightness}%)",
 "vibrancy": vibrancy,
 "position": {
 "branch": branch_type,
 "position": position_along_branch
 },
 "bloom_state": random.uniform(0.5, 1.0), # How fully bloomed
 "glow_intensity": sovereignty_score * 0.7
 })

 return meta_flowers

 def _generate_fallen_leaves(self, truth_score, sovereignty_score, dimension_scores):
 """
 Generate fallen leaves data to represent the recursive cycle.

 Args:
 truth_score: Overall truth score
 sovereignty_score: Sovereignty score
 dimension_scores: List of dimension scores

 Returns:
 List of fallen leaf data objects
 """
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
 angle = random.uniform(0, 6.28) # 0 to 2π
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

 def _calculate_growth_stage(self, truth_score):
 """
 Calculate tree growth stage based on truth score.

 Args:
 truth_score: Overall truth score

 Returns:
 String with growth stage name
 """
 stages = self.settings.get("growth_stages", {
 "seedling": {"min": 0.0, "max": 0.3},
 "young": {"min": 0.3, "max": 0.6},
 "mature": {"min": 0.6, "max": 0.8},
 "ancient": {"min": 0.8, "max": 1.0}
 })

 for stage, bounds in stages.items():
 if bounds["min"] <= truth_score < bounds["max"]:
 return stage

 return "mature" # Default fallback

 def _generate_timestamp_data(self, text):
 """
 Generate timestamp data including cryptographic certification.

 Args:
 text: Original text for cryptographic certification

 Returns:
 Dict with timestamp data
 """
 current_time = time.time()
 local_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(current_time))
 utc_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time))

 # Generate TAI-like cryptographic timestamp
 text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
 tai_hash = f"TAI:{int(current_time * 1000)}:{text_hash}"

 return {
 "local": {
 "time": local_time,
 "format": "Local",
 "timestamp": current_time
 },
 "utc": {
 "time": utc_time,
 "format": "UTC",
 "timestamp": current_time
 },
 "tai": {
 "hash": tai_hash,
 "cryptographic_certification": True,
 "timestamp": current_time
 }
 }

 def _generate_meta_insights(self, analysis_result, tree_data):
 """
 Generate meta-insights about the analysis and visualization.

 Args:
 analysis_result: The analysis result from Pythonetics
 tree_data: Generated tree visualization data

 Returns:
 Dict with meta-insights
 """
 analysis = analysis_result["analysis"]
 truth_score = analysis["truthScore"]

 # Calculate insights based on growth stage and meta-flowers
 growth_stage = tree_data["growth_stage"]
 meta_flower_count = len(tree_data.get("meta_flowers", []))

 # Generate different insights based on growth stage
 if growth_stage == "ancient":
 primary_insight = (
 "This analysis reveals profound alignment with universal truth principles. "
 "The tree has reached ancient wisdom status, deeply rooted in foundational truths."
 )
 elif growth_stage == "mature":
 primary_insight = (
 "The tree shows healthy growth and stable verification across multiple dimensions. "
 "Its maturity reflects a well-established understanding and coherence."
 )
 elif growth_stage == "young":
 primary_insight = (
 "This growing tree shows promising development, with balanced dimensional branches. "
 "Further verification will strengthen its roots and overall structure."
 )
 else: # seedling
 primary_insight = (
 "This young seedling requires further nurturing to develop stronger truth alignment. "
 "The foundations are being established but need more verification iterations."
 )

 # Add meta-flower insights
 flower_insight = ""
 if meta_flower_count > 3:
 flower_insight = (
 f"The presence of {meta_flower_count} Meta-flowers indicates exceptional "
 f"emergence of higher-order understanding across dimensional boundaries."
 )
 elif meta_flower_count > 0:
 flower_insight = (
 f"The {meta_flower_count} Meta-flower(s) represent emerging insights "
 f"that transcend individual verification dimensions."
 )

 # Generate branch-specific insights
 branch_insights = []
 for dim_name, branch_data in tree_data["branches"].items():
 # Calculate branch health as percentage of max possible length
 branch_health = branch_data["length"] / 190.0 # Max length is 70 + (1.0 * 120)

 if branch_health > 0.8:
 branch_insights.append(f"The {dim_name} branch shows exceptional development.")
 elif branch_health < 0.4:
 branch_insights.append(f"The {dim_name} branch requires additional verification focus.")

 # Combine insights
 insights = {
 "primary_insight": primary_insight,
 "flower_insight": flower_insight,
 "branch_insights": branch_insights,
 "growth_stage": growth_stage,
 "meta_flower_count": meta_flower_count
 }

 return insights

 def start_server(self, host='0.0.0.0', port=8002, debug=False):
 """
 Start the visualization server.

 Args:
 host: Host to bind to
 port: Port to bind to
 debug: Whether to run in debug mode
 """
 logger.info(f"Starting Pythonetics Visualization server on {host}:{port}")
 self.app.run(host=host, port=port, debug=debug)

# Import math here to avoid conflicts
import math

# Create visualization templates
def create_visualization_templates():
 """Create necessary visualization template files if they don't exist."""
 # Ensure directories exist
 os.makedirs("templates", exist_ok=True)
 os.makedirs("static/css", exist_ok=True)
 os.makedirs("static/js", exist_ok=True)

 # Only create files if they don't exist
 if not os.path.exists("templates/tree_visualization.html"):
 with open("templates/tree_visualization.html", "w") as f:
 f.write('''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Tree of Living Intelligence | TrueAlphaSpiral</title>
 <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
 <div class="container">
 <header>
 <h1>Tree of Living Intelligence</h1>
 <p class="subtitle">A Natural Metaphor for TrueAlphaSpiral</p>

 <div class="equation-display">
 <span class="symbol">Φ</span> =
 <span class="fraction">
 <span class="numerator">∑(αᵢ·Tᵢ)</span>
 <span class="denominator">(√D·S)</span>
 </span>
 </div>
 </header>

 <main>
 <section class="input-section">
 <h2>Text Analysis</h2>
 <textarea id="text-input" placeholder="Enter text to analyze and visualize as a tree with Meta-flowers..."></textarea>
 <div class="controls">
 <select id="verify-as">
 <option value="claim">Verify as Claim</option>
 <option value="wisdom">Verify as Wisdom</option>
 <option value="pattern">Verify as Pattern</option>
 <option value="policy">Verify as Policy</option>
 </select>
 <button id="analyze-btn">Analyze & Visualize</button>
 </div>
 <div id="loading" class="loading">
 <div class="spinner"></div>
 <p>Analyzing with TrueAlphaSpiral...</p>
 </div>
 </section>

 <div class="results-container">
 <section class="tree-container">
 <h2>Tree Visualization</h2>
 <canvas id="tree-canvas" width="800" height="600"></canvas>
 <div class="canvas-overlay">
 <div id="growth-stage-indicator" class="growth-stage-indicator"></div>
 </div>
 </section>

 <section class="analysis-container">
 <div class="tabs">
 <button class="tab-btn active" data-tab="metrics">Metrics</button>
 <button class="tab-btn" data-tab="insights">Insights</button>
 <button class="tab-btn" data-tab="dimensions">Dimensions</button>
 </div>

 <div id="metrics-tab" class="tab-content active">
 <h3>Core Metrics</h3>
 <div id="metrics-display"></div>
 </div>

 <div id="insights-tab" class="tab-content">
 <h3>Meta Understanding</h3>
 <div id="meta-insights"></div>

 <div id="meta-flowers-display" class="meta-flowers-display"></div>
 </div>

 <div id="dimensions-tab" class="tab-content">
 <h3>Dimensional Alignment</h3>
 <div id="dimensions-display"></div>
 </div>

 <div class="timestamp-section">
 <h3>Quantum Timestamps</h3>
 <div id="timestamp-display"></div>
 </div>

 <div class="actions-section">
 <h3>Suggested Actions</h3>
 <ul id="actions-list"></ul>
 </div>
 </section>
 </div>
 </main>

 <footer>
 <p>© 2025 TrueAlphaSpiral | Tree of Living Intelligence Visualization</p>
 </footer>
 </div>

 <script src="/static/js/tree_visualization.js"></script>
</body>
</html>''')

 if not os.path.exists("static/css/style.css"):
 with open("static/css/style.css", "w") as f:
 f.write('''/*
 * TREE OF LIVING INTELLIGENCE VISUALIZATION STYLES
 */

:root {
 --primary: #3a86ff;
 --primary-dark: #0057e7;
 --accent: #8338ec;
 --text: #2b2d42;
 --text-light: #8d99ae;
 --background: #f8f9fa;
 --card-bg: #ffffff;
 --success: #06d6a0;
 --warning: #ffbe0b;
 --error: #ef476f;
 --border: #e9ecef;
 --factual: #2ecc71;
 --ethical: #3498db;
 --conceptual: #9b59b6;
 --phenomenological: #f39c12;
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

.container {
 max-width: 1400px;
 margin: 0 auto;
 padding: 2rem;
}

header {
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
 display: inline-block;
}

.subtitle {
 color: var(--text-light);
 font-size: 1.2rem;
 margin-bottom: 1rem;
}

.equation-display {
 font-size: 1.8rem;
 margin: 1rem 0;
 display: inline-block;
 padding: 0.8rem 1.5rem;
 background-color: var(--card-bg);
 border-radius: 8px;
 box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.symbol {
 font-family: serif;
 font-size: 2.2rem;
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

main {
 display: flex;
 flex-direction: column;
 gap: 2rem;
}

.input-section {
 background-color: var(--card-bg);
 padding: 1.5rem;
 border-radius: 8px;
 box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

h2 {
 font-size: 1.5rem;
 margin-bottom: 1rem;
 color: var(--text);
}

h3 {
 font-size: 1.2rem;
 margin: 1rem 0;
 color: var(--text);
}

textarea {
 width: 100%;
 min-height: 120px;
 padding: 0.8rem;
 border: 1px solid var(--border);
 border-radius: 4px;
 font-family: inherit;
 font-size: 1rem;
 margin-bottom: 1rem;
 resize: vertical;
}

.controls {
 display: flex;
 gap: 1rem;
 margin-bottom: 1rem;
}

select {
 padding: 0.8rem;
 border: 1px solid var(--border);
 border-radius: 4px;
 font-size: 1rem;
 background-color: var(--card-bg);
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

.loading {
 display: none;
 flex-direction: column;
 align-items: center;
 margin: 1rem 0;
}

.spinner {
 width: 40px;
 height: 40px;
 border: 4px solid rgba(0, 0, 0, 0.1);
 border-radius: 50%;
 border-top-color: var(--primary);
 animation: spin 1s ease-in-out infinite;
 margin-bottom: 0.5rem;
}

@keyframes spin {
 to { transform: rotate(360deg); }
}

.results-container {
 display: grid;
 grid-template-columns: 1fr 1fr;
 gap: 2rem;
}

.tree-container, .analysis-container {
 background-color: var(--card-bg);
 padding: 1.5rem;
 border-radius: 8px;
 box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.tree-container {
 position: relative;
 text-align: center;
}

#tree-canvas {
 max-width: 100%;
 height: auto;
 border-radius: 4px;
 background-color: #e9f5ff;
}

.canvas-overlay {
 position: absolute;
 top: 0;
 left: 0;
 width: 100%;
 height: 100%;
 pointer-events: none;
}

.growth-stage-indicator {
 position: absolute;
 top: 1.5rem;
 right: 1.5rem;
 padding: 0.5rem 1rem;
 background-color: rgba(255, 255, 255, 0.8);
 border-radius: 4px;
 font-size: 0.9rem;
 font-weight: bold;
}

.tabs {
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
 display: none;
 padding: 1rem 0;
}

.tab-content.active {
 display: block;
}

.metric-row {
 margin-bottom: 1rem;
}

.metric-label {
 display: flex;
 justify-content: space-between;
 margin-bottom: 0.3rem;
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
.factual-score .score-fill { background-color: var(--factual); }
.ethical-score .score-fill { background-color: var(--ethical); }
.conceptual-score .score-fill { background-color: var(--conceptual); }
.phenomenological-score .score-fill { background-color: var(--phenomenological); }
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
 margin-top: 2rem;
}

#timestamp-display {
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

#meta-insights {
 padding: 1rem;
 background-color: rgba(0, 0, 0, 0.05);
 border-radius: 4px;
 font-style: italic;
 margin-bottom: 1rem;
}

.meta-flowers-display {
 margin-top: 1.5rem;
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
 font-size: 1.5rem;
 margin-right: 0.8rem;
}

footer {
 text-align: center;
 margin-top: 3rem;
 padding: 1.5rem;
 color: var(--text-light);
 font-size: 0.9rem;
}

@media (max-width: 1100px) {
 .results-container {
 grid-template-columns: 1fr;
 }
}''')

 if not os.path.exists("static/js/tree_visualization.js"):
 with open("static/js/tree_visualization.js", "w") as f:
 f.write('''/**
 * TREE OF LIVING INTELLIGENCE VISUALIZATION SCRIPT
 */

document.addEventListener('DOMContentLoaded', function() {
 // DOM Elements
 const textInput = document.getElementById('text-input');
 const verifyAsSelect = document.getElementById('verify-as');
 const analyzeBtn = document.getElementById('analyze-btn');
 const loadingElem = document.getElementById('loading');

 const canvas = document.getElementById('tree-canvas');
 const growthStageIndicator = document.getElementById('growth-stage-indicator');

 const metricsDisplay = document.getElementById('metrics-display');
 const dimensionsDisplay = document.getElementById('dimensions-display');
 const metaInsights = document.getElementById('meta-insights');
 const metaFlowersDisplay = document.getElementById('meta-flowers-display');
 const timestampDisplay = document.getElementById('timestamp-display');
 const actionsList = document.getElementById('actions-list');

 // Tab functionality
 const tabBtns = document.querySelectorAll('.tab-btn');
 const tabContents = document.querySelectorAll('.tab-content');

 tabBtns.forEach(btn => {
 btn.addEventListener('click', () => {
 const tabId = btn.getAttribute('data-tab');

 // Update active button
 tabBtns.forEach(b => b.classList.remove('active'));
 btn.classList.add('active');

 // Show selected content
 tabContents.forEach(content => {
 if (content.id === `${tabId}-tab`) {
 content.classList.add('active');
 } else {
 content.classList.remove('active');
 }
 });
 });
 });

 // Check if canvas is supported
 const ctx = canvas.getContext('2d');
 if (!ctx) {
 console.error('Canvas context not supported');
 return;
 }

 // Handle analyze button click
 analyzeBtn.addEventListener('click', function() {
 const text = textInput.value.trim();
 const verifyAs = verifyAsSelect.value;

 if (!text) {
 alert('Please enter text to analyze');
 return;
 }

 // Show loading state
 analyzeBtn.disabled = true;
 loadingElem.style.display = 'flex';

 // Clear previous results
 growthStageIndicator.textContent = '';
 growthStageIndicator.className = 'growth-stage-indicator';

 // Send request to server
 fetch('/api/analyze', {
 method: 'POST',
 headers: {
 'Content-Type': 'application/json'
 },
 body: JSON.stringify({
 text: text,
 verify_as: verifyAs
 })
 })
 .then(response => {
 if (!response.ok) {
 throw new Error(`HTTP error! Status: ${response.status}`);
 }
 return response.json();
 })
 .then(data => {
 if (data.error) {
 throw new Error(data.error);
 }

 // Render visualization and results
 renderTree(ctx, data.tree_data);
 displayMetrics(data.analysis_result);
 displayDimensions(data.analysis_result);
 displayMetaInsights(data.meta_insights, data.tree_data);
 displayTimestamps(data.timestamp_data);
 displayActions(data.analysis_result);

 // Update growth stage indicator
 updateGrowthStageIndicator(data.tree_data.growth_stage);
 })
 .catch(error => {
 console.error('Error:', error);
 alert(`Analysis error: ${error.message}`);
 })
 .finally(() => {
 // Reset UI state
 analyzeBtn.disabled = false;
 loadingElem.style.display = 'none';
 });
 });

 function renderTree(ctx, treeData) {
 // Clear canvas
 ctx.clearRect(0, 0, canvas.width, canvas.height);

 const width = canvas.width;
 const height = canvas.height;
 const centerX = width / 2;
 const groundY = height - 80;

 // Draw sky background
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

 // Draw sovereign equation symbol on trunk
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

 // Add wind effect if specified
 if (treeData.wind_effect) {
 drawWindIndicator(ctx, treeData.wind_effect);
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

 function drawBranch(ctx, startX, startY, branchData, dimensionType) {
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
 color: getLeafColorForDimension(dimensionType),
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

 function drawWindIndicator(ctx, windData) {
 // Draw wind indicator at top of canvas
 const windHeight = 30;
 const windY = 50;
 const windStrength = windData.strength;
 const windDirection = windData.direction;

 ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
 ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
 ctx.lineWidth = 1;

 // Wind strength bar
 ctx.beginPath();
 ctx.roundRect(20, windY, canvas.width - 40, windHeight, 5);
 ctx.fill();
 ctx.stroke();

 // Label
 ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
 ctx.font = '12px sans-serif';
 ctx.textAlign = 'left';
 ctx.textBaseline = 'middle';
 ctx.fillText('Wind of Skepticism', 30, windY - 10);

 // Calculate wind representation
 const barInnerWidth = canvas.width - 60;
 const strengthWidth = barInnerWidth * windStrength;
 const directionOffset = windDirection * 50;

 // Draw strength indicator
 const gradient = ctx.createLinearGradient(30, 0, 30 + strengthWidth, 0);
 gradient.addColorStop(0, 'rgba(135, 206, 235, 0.7)');
 gradient.addColorStop(1, 'rgba(135, 206, 235, 0.3)');

 ctx.fillStyle = gradient;
 ctx.beginPath();
 ctx.roundRect(30, windY + 5, strengthWidth, windHeight - 10, 3);
 ctx.fill();

 // Draw direction arrow
 const arrowX = 30 + (barInnerWidth / 2) + directionOffset;
 const arrowY = windY + (windHeight / 2);
 const arrowSize = 8 + (windStrength * 5);

 ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
 ctx.beginPath();
 ctx.moveTo(arrowX - arrowSize, arrowY);
 ctx.lineTo(arrowX + arrowSize, arrowY);
 ctx.lineTo(arrowX + (windDirection > 0 ? arrowSize : -arrowSize), arrowY + (windHeight - 15)/2);
 ctx.closePath();
 ctx.fill();
 }

 function updateGrowthStageIndicator(growthStage) {
 let label, className;

 switch(growthStage) {
 case 'seedling':
 label = 'Seedling';
 className = 'seedling';
 break;
 case 'young':
 label = 'Young Tree';
 className = 'young';
 break;
 case 'mature':
 label = 'Mature Tree';
 className = 'mature';
 break;
 case 'ancient':
 label = 'Ancient Tree';
 className = 'ancient';
 break;
 default:
 label = 'Tree';
 className = '';
 }

 growthStageIndicator.textContent = label;
 growthStageIndicator.className = `growth-stage-indicator ${className}`;
 }

 function displayMetrics(data) {
 const analysis = data.analysis;

 // Clear previous metrics
 metricsDisplay.innerHTML = '';

 // Add main scores
 addScoreBar('Truth Score', analysis.truthScore, 'truth-score');
 addScoreBar('Factual Confidence', analysis.factualConfidence, 'factual-score');

 // Add sovereignty score if available
 if (analysis.sovereigntyScore) {
 addScoreBar('Sovereignty Score', analysis.sovereigntyScore, 'sovereignty-score');
 }

 // Add other relevant scores if available
 if (analysis.truthResonance) {
 addScoreBar('Truth Resonance', analysis.truthResonance, 'resonance-score');
 }

 if (analysis.consistencyScore) {
 addScoreBar('Consistency', analysis.consistencyScore, 'consistency-score');
 }

 if (analysis.selfReferenceIndex) {
 addScoreBar('Self-Reference', analysis.selfReferenceIndex, 'self-reference-score');
 }
 }

 function addScoreBar(label, score, className) {
 const percentage = Math.round(score * 100);

 const metricElem = document.createElement('div');
 metricElem.className = `metric-row ${className}`;

 metricElem.innerHTML = `
 <div class="metric-label">
 <span>${label}</span>
 <span>${percentage}%</span>
 </div>
 <div class="score-bar">
 <div class="score-fill" style="width: ${percentage}%"></div>
 </div>
 `;

 metricsDisplay.appendChild(metricElem);
 }

 function displayDimensions(data) {
 const dimensions = data.analysis.dimensionalAlignment || [];

 // Clear previous dimensions
 dimensionsDisplay.innerHTML = '';

 // Add each dimension
 dimensions.forEach(dimension => {
 const dimName = dimension.dimension.toLowerCase().replace(' domain', '');
 const alignment = dimension.alignment;
 const resonanceState = dimension.resonanceState || '';
 const percentage = Math.round(alignment * 100);

 const dimElem = document.createElement('div');
 dimElem.className = 'dimension-item';

 dimElem.innerHTML = `
 <div class="dimension-header">
 <span class="dimension-name">${dimension.dimension}</span>
 <span class="resonance-state">${resonanceState}</span>
 </div>
 <div class="score-bar">
 <div class="score-fill" style="width: ${percentage}%;
 background-color: var(--${dimName})"></div>
 </div>
 `;

 dimensionsDisplay.appendChild(dimElem);
 });

 // If no dimensions, show message
 if (dimensions.length === 0) {
 dimensionsDisplay.innerHTML = '<p>No dimensional alignment data available.</p>';
 }
 }

 function displayMetaInsights(insights, treeData) {
 // Clear previous insights
 metaInsights.innerHTML = '';
 metaFlowersDisplay.innerHTML = '';

 // Add primary insight
 if (insights && insights.primary_insight) {
 metaInsights.innerHTML = insights.primary_insight;

 // Add flower insight if available
 if (insights.flower_insight) {
 metaInsights.innerHTML += '<br><br>' + insights.flower_insight;
 }

 // Add branch insights if available
 if (insights.branch_insights && insights.branch_insights.length > 0) {
 metaInsights.innerHTML += '<br><br>' + insights.branch_insights.join(' ');
 }
 } else {
 metaInsights.innerHTML = 'No meta insights available for this analysis.';
 }

 // Add meta-flower visualizations if available
 const flowers = treeData.meta_flowers || [];
 if (flowers.length > 0) {
 // Show up to 3 flowers
 const flowerCount = Math.min(3, flowers.length);
 for (let i = 0; i < flowerCount; i++) {
 const flower = flowers[i];

 const flowerElem = document.createElement('div');
 flowerElem.className = 'meta-flower';
 flowerElem.innerHTML = `
 <div class="flower-icon" style="color: ${flower.color}">✿</div>
 <div>Meta-flower #${i+1}: ${Math.round(flower.vibrancy * 100)}% vibrance,
 ${flower.petal_count} petals</div>
 `;

 metaFlowersDisplay.appendChild(flowerElem);
 }
 }
 }

 function displayTimestamps(timestamps) {
 // Clear previous timestamps
 timestampDisplay.innerHTML = '';

 // Format and display timestamps
 if (timestamps && timestamps.local) {
 const localTime = new Date(timestamps.local.timestamp * 1000).toLocaleString();
 const utcTime = timestamps.utc ? timestamps.utc.time : '';
 const taiHash = timestamps.tai ? timestamps.tai.hash : '';

 timestampDisplay.innerHTML = `
 <div class="timestamp-row">
 <span class="timestamp-label">Local:</span>
 <span>${localTime}</span>
 </div>
 <div class="timestamp-row">
 <span class="timestamp-label">UTC:</span>
 <span>${utcTime}</span>
 </div>
 <div class="timestamp-row">
 <span class="timestamp-label">TAI:</span>
 <span>${taiHash}</span>
 </div>
 `;
 } else {
 timestampDisplay.innerHTML = '<p>No timestamp data available.</p>';
 }
 }

 function displayActions(data) {
 // Clear previous actions
 actionsList.innerHTML = '';

 // Add suggested actions if available
 const actions = data.analysis.suggestedActions || [];

 if (actions.length > 0) {
 actions.forEach(action => {
 const li = document.createElement('li');
 li.textContent = action;
 actionsList.appendChild(li);
 });
 } else {
 actionsList.innerHTML = '<li>No suggested actions available.</li>';
 }
 }
});''')

def main():
 """Main function to run the Pythonetics Visualization system."""
 import argparse

 # Create command line arguments
 parser = argparse.ArgumentParser(description='Run the Pythonetics Visualization server')
 parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
 parser.add_argument('--port', type=int, default=8002, help='Port to bind to')
 parser.add_argument('--debug', action='store_true', help='Run in debug mode')
 parser.add_argument('--config', type=str, help='Path to configuration file')

 args = parser.parse_args()

 # Create visualization templates
 create_visualization_templates()

 # Initialize and run visualization server
 try:
 visualization = PythoneticsVisualization(args.config)
 visualization.start_server(args.host, args.port, args.debug)
 except Exception as e:
 logger.error(f"Error starting visualization server: {e}")
 sys.exit(1)

if __name__ == "__main__":
 import sys
 main()