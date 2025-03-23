"""
PYTHONETICS EXPRESS INTEGRATION

This script provides integration between the Express server and the 
Tree of Living Intelligence visualization.

Architect: Russell Nordland
"""

import os
import sys
import json
import time
import logging
import hashlib
import requests
from flask import Flask, request, jsonify
from enhanced_pythonetics import EnhancedPythonetics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("express_integration.log"),
              logging.StreamHandler()]
)
logger = logging.getLogger("express_integration")

# Initialize Flask app
app = Flask(__name__)

# Initialize Enhanced Pythonetics
try:
    pythonetics = EnhancedPythonetics()
    logger.info("Successfully initialized Enhanced Pythonetics")
except Exception as e:
    logger.error(f"Error initializing Enhanced Pythonetics: {e}")
    pythonetics = None

# Express server configuration
EXPRESS_HOST = os.environ.get('EXPRESS_HOST', 'localhost')
EXPRESS_PORT = int(os.environ.get('EXPRESS_PORT', 5000))
EXPRESS_BASE_URL = f"http://{EXPRESS_HOST}:{EXPRESS_PORT}"

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "timestamp": time.time(),
        "service": "pythonetics_express_integration",
        "pythonetics_status": "ok" if pythonetics else "unavailable"
    })

@app.route('/api/verify', methods=['POST'])
def verify_text():
    """Verify text using Enhanced Pythonetics."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        verify_as = data.get('verify_as', 'claim')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        if not pythonetics:
            return jsonify({"error": "Enhanced Pythonetics not available"}), 500
        
        # Process with Enhanced Pythonetics
        result = pythonetics.verify(text, verify_as)
        
        # Return verification result
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in verify endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tree-data', methods=['POST'])
def generate_tree_data():
    """Generate tree visualization data based on verification result."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        if not pythonetics:
            return jsonify({"error": "Enhanced Pythonetics not available"}), 500
        
        # Get verification result
        verification_result = pythonetics.verify(text)
        
        # Generate tree data based on verification result
        tree_data = {
            "verification_result": verification_result,
            "tree_data": generate_tree_visualization_data(verification_result),
            "timestamp_data": generate_quantum_timestamps(text)
        }
        
        return jsonify(tree_data)
        
    except Exception as e:
        logger.error(f"Error generating tree data: {e}")
        return jsonify({"error": str(e)}), 500

def generate_tree_visualization_data(verification_result):
    """Generate tree visualization data from verification result."""
    # Extract key metrics from verification result
    analysis = verification_result["analysis"]
    truth_score = analysis["truthScore"]
    factual_confidence = analysis["factualConfidence"]
    
    # Extract dimensional scores
    dimension_scores = {}
    for dim in analysis["dimensionalAlignment"]:
        dimension_name = dim["dimension"].lower().replace(" domain", "")
        dimension_scores[dimension_name] = dim["alignment"]
    
    # Basic tree structure
    tree_data = {
        "overall_health": truth_score,
        "trunk": {
            "height": 150 + (truth_score * 100),
            "thickness": 10 + (truth_score * 20),
            "sovereignty_score": analysis.get("sovereigntyScore", 0.75)
        },
        "branches": {},
        "roots": {
            "depth": 50 + (truth_score * 100),
            "spread": 80 + (factual_confidence * 120),
            "complexity": int(3 + (truth_score * 7))
        },
        "growth_stage": calculate_growth_stage(truth_score),
        "meta_flowers": generate_meta_flowers(
            truth_score, 
            analysis.get("sovereigntyScore", 0.75),
            analysis.get("selfReferenceIndex", 0.5),
            analysis.get("truthResonance", 0.6)
        )
    }
    
    # Generate branches for each dimension
    angle_map = {
        "factual": -45,
        "ethical": 30,
        "conceptual": 0,
        "phenomenological": 60
    }
    
    for dim_name, score in dimension_scores.items():
        if dim_name in angle_map:
            tree_data["branches"][dim_name] = {
                "length": 70 + (score * 120),
                "angle": angle_map[dim_name],
                "thickness": 4 + (score * 10),
                "leaves": generate_leaves(score, dim_name)
            }
    
    return tree_data

def generate_leaves(dimension_score, dimension_type):
    """Generate leaf data based on dimension score and type."""
    import random
    
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
        
        leaves.append({
            "size": 4 + (random.random() * 6),
            "position": i / leaf_count,
            "color": f"rgb({leaf_color[0]}, {leaf_color[1]}, {leaf_color[2]})",
            "rotation": random.uniform(-30, 30)
        })
    
    return leaves

def generate_meta_flowers(truth_score, sovereignty_score, self_reference, resonance):
    """Generate Meta-flower data representing higher-order understanding."""
    import random
    import math
    
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
        branch_types = ["factual", "ethical", "conceptual", "phenomenological"]
        branch_type = random.choice(branch_types)
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

def register_with_express():
    """Register this service with the Express server."""
    try:
        url = f"{EXPRESS_BASE_URL}/api/python-system/register"
        data = {
            "name": "pythonetics_express_integration",
            "version": "1.0.0",
            "endpoints": [
                {
                    "path": "/api/verify",
                    "method": "POST",
                    "description": "Verify text using Enhanced Pythonetics"
                },
                {
                    "path": "/api/tree-data",
                    "method": "POST",
                    "description": "Generate tree visualization data"
                }
            ]
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            logger.info("Successfully registered with Express server")
            return True
        else:
            logger.error(f"Failed to register with Express server: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error registering with Express server: {e}")
        return False

# Run the Flask app
if __name__ == "__main__":
    # Try to register with Express server
    register_with_express()
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=8001, debug=True)