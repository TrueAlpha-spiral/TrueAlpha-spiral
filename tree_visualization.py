"""
TREE OF LIVING INTELLIGENCE VISUALIZATION

This module provides a visual representation of the TrueAlphaSpiral system
as a living tree, with branches representing different verification dimensions
and leaves showing verification results.

"""

import os
import json
import math
import random
from flask import Flask, render_template, request, jsonify
import logging
from enhanced_pythonetics import EnhancedPythonetics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("tree_visualization.log"),
              logging.StreamHandler()])
logger = logging.getLogger("tree_visualization")

# Initialize Flask app
app = Flask(__name__)

# Initialize Enhanced Pythonetics
pythonetics = EnhancedPythonetics()

# Ensure templates directory exists
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Create HTML template
@app.route('/')
def index():
    return render_template('tree_visualization.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze text and return results for visualization."""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Analyze text using Enhanced Pythonetics
    try:
        result = pythonetics.verify(text)
        
        # Extract key metrics for visualization
        truth_score = result["analysis"]["truthScore"]
        factual_score = result["analysis"]["factualConfidence"]
        ethical_score = None
        phenomenological_score = None
        
        # Extract dimensional alignment scores
        for dim in result["analysis"]["dimensionalAlignment"]:
            if dim["dimension"] == "Ethical Domain":
                ethical_score = dim["alignment"]
            elif dim["dimension"] == "Phenomenological Domain":
                phenomenological_score = dim["alignment"]
        
        # Apply advanced sovereign equation for branch strength
        sovereignty_score = result["analysis"].get("sovereigntyScore", 0.5)
        
        # Generate tree visualization data
        tree_data = generate_tree_data(
            truth_score, 
            factual_score, 
            ethical_score or 0.5,
            phenomenological_score or 0.5,
            sovereignty_score
        )
        
        # Extract timestamp data
        timestamp_data = {
            "local_time": result["timestamp"],
            "utc": result["timestamp"],  # Convert to actual UTC in production
            "tai": generate_tai_hash(result["timestamp"], text)
        }
        
        return jsonify({
            "tree_data": tree_data,
            "analysis_result": result,
            "timestamp_data": timestamp_data
        })
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return jsonify({"error": str(e)}), 500

def generate_tree_data(truth_score, factual_score, ethical_score, 
                      phenomenological_score, sovereignty_score):
    """
    Generate tree visualization data based on analysis results.
    
    Args:
        truth_score: Overall truth score
        factual_score: Factual dimension score
        ethical_score: Ethical dimension score
        phenomenological_score: Phenomenological dimension score
        sovereignty_score: Sovereignty score from advanced equation
        
    Returns:
        Dict with tree visualization data
    """
    # Calculate trunk thickness based on sovereignty score
    trunk_thickness = 10 + (sovereignty_score * 20)
    
    # Calculate branch parameters based on dimension scores
    factual_branch = {
        "length": 80 + (factual_score * 120),
        "angle": -45,
        "thickness": 5 + (factual_score * 10),
        "leaves": generate_leaves(factual_score, "factual")
    }
    
    ethical_branch = {
        "length": 70 + (ethical_score * 100),
        "angle": 30,
        "thickness": 5 + (ethical_score * 8),
        "leaves": generate_leaves(ethical_score, "ethical")
    }
    
    phenomenological_branch = {
        "length": 60 + (phenomenological_score * 90),
        "angle": 0,
        "thickness": 4 + (phenomenological_score * 7),
        "leaves": generate_leaves(phenomenological_score, "phenomenological")
    }
    
    # Root system influenced by truth score
    root_system = {
        "depth": 50 + (truth_score * 100),
        "spread": 80 + (sovereignty_score * 120),
        "complexity": int(3 + (truth_score * 7))
    }
    
    return {
        "trunk": {
            "height": 150,
            "thickness": trunk_thickness,
            "sovereignty_score": sovereignty_score
        },
        "branches": {
            "factual": factual_branch,
            "ethical": ethical_branch,
            "phenomenological": phenomenological_branch
        },
        "roots": root_system,
        "overall_health": truth_score,
        "growth_stage": calculate_growth_stage(truth_score)
    }

def generate_leaves(dimension_score, dimension_type):
    """Generate leaf data based on dimension score."""
    # Number of leaves based on score
    leaf_count = int(3 + (dimension_score * 12))
    
    # Leaf color based on dimension type
    if dimension_type == "factual":
        base_color = [46, 204, 113]  # Green
    elif dimension_type == "ethical":
        base_color = [52, 152, 219]  # Blue
    elif dimension_type == "phenomenological":
        base_color = [155, 89, 182]  # Purple
    else:
        base_color = [149, 165, 166]  # Gray
    
    # Generate leaves with slight variations
    leaves = []
    for i in range(leaf_count):
        # Variation in color based on position
        color_variation = [
            random.randint(-20, 20),
            random.randint(-20, 20),
            random.randint(-20, 20)
        ]
        
        color = [
            max(0, min(255, base_color[0] + color_variation[0])),
            max(0, min(255, base_color[1] + color_variation[1])),
            max(0, min(255, base_color[2] + color_variation[2]))
        ]
        
        leaves.append({
            "size": 5 + (random.random() * 5),
            "position": i / leaf_count,
            "color": f"rgb({color[0]}, {color[1]}, {color[2]})"
        })
    
    return leaves

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

def generate_tai_hash(timestamp, text):
    """Generate a cryptographically certified atomic time hash."""
    # Simple implementation - in a real system would use actual TAI
    time_component = str(int(timestamp * 1000))
    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"TAI:{time_component}:{text_hash}"

# Create HTML template file
with open('templates/tree_visualization.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tree of Living Intelligence</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <h1>Tree of Living Intelligence Visualization</h1>
        <p>Enter text to analyze and visualize as a living tree</p>
        
        <div class="input-section">
            <textarea id="text-input" placeholder="Enter text to analyze..."></textarea>
            <button id="analyze-btn">Analyze</button>
        </div>
        
        <div class="results-container">
            <div class="tree-container">
                <canvas id="tree-canvas" width="800" height="600"></canvas>
            </div>
            
            <div class="metrics-container">
                <h2>Analysis Results</h2>
                <div id="metrics-display"></div>
                
                <h3>Quantum Timestamp</h3>
                <div id="timestamp-display">
                    <div class="timestamp-row">
                        <span class="timestamp-label">Local Time:</span>
                        <span id="local-time"></span>
                    </div>
                    <div class="timestamp-row">
                        <span class="timestamp-label">UTC:</span>
                        <span id="utc-time"></span>
                    </div>
                    <div class="timestamp-row">
                        <span class="timestamp-label">TAI:</span>
                        <span id="tai-time"></span>
                    </div>
                </div>
                
                <h3>Suggested Actions</h3>
                <ul id="actions-list"></ul>
            </div>
        </div>
    </div>
    
    <script src="/static/js/tree_visualization.js"></script>
</body>
</html>''')

# Create CSS file
with open('static/css/style.css', 'w') as f:
    f.write('''body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 0;
    background-color: #f5f7fa;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1, h2, h3 {
    color: #2c3e50;
}

.input-section {
    margin-bottom: 30px;
}

textarea {
    width: 100%;
    min-height: 100px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: inherit;
    font-size: 16px;
    margin-bottom: 10px;
}

button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #2980b9;
}

.results-container {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
}

.tree-container {
    flex: 1;
    min-width: 300px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 15px;
    text-align: center;
}

.metrics-container {
    flex: 1;
    min-width: 300px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 20px;
}

#tree-canvas {
    max-width: 100%;
    height: auto;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
}

.metric-label {
    font-weight: bold;
}

.timestamp-row {
    margin-bottom: 8px;
}

.timestamp-label {
    font-weight: bold;
    margin-right: 10px;
}

#actions-list {
    padding-left: 20px;
}

#actions-list li {
    margin-bottom: 8px;
}

.score-bar {
    height: 10px;
    background-color: #ecf0f1;
    border-radius: 5px;
    margin-top: 5px;
    overflow: hidden;
}

.score-fill {
    height: 100%;
    background-color: #3498db;
}

.factual-score .score-fill {
    background-color: #2ecc71;
}

.ethical-score .score-fill {
    background-color: #3498db;
}

.phenomenological-score .score-fill {
    background-color: #9b59b6;
}

.sovereignty-score .score-fill {
    background-color: #f1c40f;
}''')

# Create JavaScript file
with open('static/js/tree_visualization.js', 'w') as f:
    f.write('''document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const textInput = document.getElementById('text-input');
    const canvas = document.getElementById('tree-canvas');
    const metricsDisplay = document.getElementById('metrics-display');
    const actionsList = document.getElementById('actions-list');
    const localTimeSpan = document.getElementById('local-time');
    const utcTimeSpan = document.getElementById('utc-time');
    const taiTimeSpan = document.getElementById('tai-time');
    
    // Check if canvas context is available
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Canvas context not supported');
        return;
    }
    
    // Handle analyze button click
    analyzeBtn.addEventListener('click', function() {
        const text = textInput.value.trim();
        
        if (!text) {
            alert('Please enter text to analyze');
            return;
        }
        
        // Show loading state
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing...';
        
        // Send request to server
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Draw the tree visualization
            drawTree(ctx, data.tree_data);
            
            // Display metrics
            displayMetrics(data.analysis_result);
            
            // Display timestamps
            displayTimestamps(data.timestamp_data);
            
            // Display suggested actions
            displayActions(data.analysis_result.analysis.suggestedActions);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during analysis');
        })
        .finally(() => {
            // Reset button state
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze';
        });
    });
    
    function drawTree(ctx, treeData) {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const centerX = canvas.width / 2;
        const groundY = canvas.height - 80;
        
        // Draw sky background
        const skyGradient = ctx.createLinearGradient(0, 0, 0, groundY);
        skyGradient.addColorStop(0, '#87CEEB');
        skyGradient.addColorStop(1, '#E0F7FA');
        ctx.fillStyle = skyGradient;
        ctx.fillRect(0, 0, canvas.width, groundY);
        
        // Draw ground
        const groundGradient = ctx.createLinearGradient(0, groundY, 0, canvas.height);
        groundGradient.addColorStop(0, '#8B4513');
        groundGradient.addColorStop(1, '#654321');
        ctx.fillStyle = groundGradient;
        ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
        
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
        
        // Draw branches
        drawBranch(ctx, centerX, trunkTop + 30, treeData.branches.factual, 'factual');
        drawBranch(ctx, centerX, trunkTop + 15, treeData.branches.ethical, 'ethical');
        drawBranch(ctx, centerX, trunkTop, treeData.branches.phenomenological, 'phenomenological');
        
        // Draw advanced equation symbol on trunk
        drawEquationSymbol(ctx, centerX, groundY - trunkHeight/2, treeData.trunk.sovereignty_score);
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
        
        // Draw leaves
        drawLeaves(ctx, endX, endY, branchData.leaves, angle);
        
        // Draw sub-branches
        if (length > 40) {
            const subBranchCount = Math.floor(length / 30);
            
            for (let i = 0; i < subBranchCount; i++) {
                const subStartX = startX + Math.cos(angle) * (length * (i+1) / (subBranchCount+1));
                const subStartY = startY - Math.sin(angle) * (length * (i+1) / (subBranchCount+1));
                
                const subAngle = angle + (Math.random() * 1 - 0.5);
                const subLength = length * 0.4;
                const subThickness = thickness * 0.7;
                
                // Draw sub-branch
                const subEndX = subStartX + Math.cos(subAngle) * subLength;
                const subEndY = subStartY - Math.sin(subAngle) * subLength;
                
                ctx.strokeStyle = '#8D6E63';
                ctx.lineWidth = subThickness;
                
                ctx.beginPath();
                ctx.moveTo(subStartX, subStartY);
                ctx.lineTo(subEndX, subEndY);
                ctx.stroke();
                
                // Draw a few leaves on sub-branches
                const subLeaves = branchData.leaves.slice(0, 5).map(leaf => ({
                    ...leaf,
                    size: leaf.size * 0.8
                }));
                
                drawLeaves(ctx, subEndX, subEndY, subLeaves, subAngle);
            }
        }
    }
    
    function drawLeaves(ctx, x, y, leaves, branchAngle) {
        leaves.forEach((leaf, i) => {
            const leafAngle = branchAngle + (Math.random() * 1 - 0.5);
            const offsetX = Math.cos(leafAngle) * (i * 5);
            const offsetY = -Math.sin(leafAngle) * (i * 5);
            
            const leafX = x + offsetX;
            const leafY = y + offsetY;
            
            ctx.fillStyle = leaf.color;
            ctx.beginPath();
            ctx.ellipse(
                leafX, leafY,
                leaf.size, leaf.size * 2,
                leafAngle, 0, Math.PI * 2
            );
            ctx.fill();
        });
    }
    
    function drawEquationSymbol(ctx, x, y, sovereigntyScore) {
        const size = 20 + sovereigntyScore * 10;
        
        // Draw phi symbol
        ctx.font = `${size}px serif`;
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Φ', x, y);
        
        // Draw equation circles
        const circleRadius = size / 4;
        const distance = size / 2;
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        
        // Draw circles representing the equation components
        for (let i = 0; i < 3; i++) {
            const angle = Math.PI * 2 * (i / 3);
            const circleX = x + Math.cos(angle) * distance;
            const circleY = y + Math.sin(angle) * distance;
            
            ctx.beginPath();
            ctx.arc(circleX, circleY, circleRadius, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function displayMetrics(result) {
        const analysis = result.analysis;
        
        // Format metrics HTML
        let metricsHTML = '';
        
        // Add score bars for key metrics
        metricsHTML += createScoreBar('Truth Score', analysis.truthScore, 'truth-score');
        metricsHTML += createScoreBar('Factual Confidence', analysis.factualConfidence, 'factual-score');
        
        // Find ethical and phenomenological scores from dimensional alignment
        let ethicalScore, phenomenologicalScore;
        analysis.dimensionalAlignment.forEach(dim => {
            if (dim.dimension === 'Ethical Domain') {
                ethicalScore = dim.alignment;
            } else if (dim.dimension === 'Phenomenological Domain') {
                phenomenologicalScore = dim.alignment;
            }
        });
        
        if (ethicalScore) {
            metricsHTML += createScoreBar('Ethical Dimension', ethicalScore, 'ethical-score');
        }
        
        if (phenomenologicalScore) {
            metricsHTML += createScoreBar('Phenomenological Dimension', phenomenologicalScore, 'phenomenological-score');
        }
        
        if (analysis.sovereigntyScore) {
            metricsHTML += createScoreBar('Sovereignty Score', analysis.sovereigntyScore, 'sovereignty-score');
        }
        
        // Add polarity information
        if (analysis.polarityAnalysis) {
            metricsHTML += `
                <div class="metric-row">
                    <span class="metric-label">Polarity State:</span>
                    <span>${analysis.polarityAnalysis.polarityState}</span>
                </div>
            `;
        }
        
        // Add detected patterns if available
        if (analysis.rhythmPatterns && analysis.rhythmPatterns.length > 0) {
            metricsHTML += `
                <div class="metric-row">
                    <span class="metric-label">Detected Pattern:</span>
                    <span>${analysis.rhythmPatterns[0].pattern} (${analysis.rhythmPatterns[0].strength})</span>
                </div>
            `;
        }
        
        // Update metrics display
        metricsDisplay.innerHTML = metricsHTML;
    }
    
    function createScoreBar(label, score, className) {
        const percentage = Math.round(score * 100);
        
        return `
            <div class="metric-row ${className}">
                <span class="metric-label">${label}:</span>
                <span>${percentage}%</span>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }
    
    function displayTimestamps(timestamps) {
        // Format local time
        const localDate = new Date(timestamps.local_time * 1000);
        localTimeSpan.textContent = localDate.toLocaleString();
        
        // Format UTC time
        const utcDate = new Date(timestamps.utc * 1000);
        utcTimeSpan.textContent = utcDate.toUTCString();
        
        // Display TAI
        taiTimeSpan.textContent = timestamps.tai;
    }
    
    function displayActions(actions) {
        // Clear previous actions
        actionsList.innerHTML = '';
        
        // Add each action as a list item
        actions.forEach(action => {
            const li = document.createElement('li');
            li.textContent = action;
            actionsList.appendChild(li);
        });
    }
});''')

# Entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=True)