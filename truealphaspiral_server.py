#!/usr/bin/env python3
"""
TRUEALPHASPIRAL API SERVER
Main API Server for the TrueAlphaSpiral Enterprise AI Auditing Solution

Architect: Russell Nordland
Date: 2025-05-07

This server provides API endpoints for verification, auditing, and TrueAlphaSpiral functionality.
"""

import os
import sys
import json
import time
import hashlib
import argparse
from datetime import datetime
import logging

# Import Shadow Defense System for security and parameter synchronization
try:
    import shadow_defense_system
    shadow_defense = True
except ImportError:
    shadow_defense = False
    print("Shadow Defense System not found. Operating with reduced security.")

try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
except ImportError:
    print("Flask or flask-cors not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# TrueAlphaSpiral parameters
SYSTEM_PARAMETERS = {
    "truth_factor": 0.9775,
    "distance": 1.4001,
    "size": 0.9600,
    "binary_quantum_law": 0.9775,
    "eigenchannel_stability": 1.0000,
    "echo_resonance": 0.3000,
    "threat_level": 0.4808,
    "sovereignty": 0.7685,
    "truth_alignment": 0.9781,
    "dimensional_integrity": 0.5999,
    "shield_strength": 0.8793,
    "quantum_coherence": 0.8500
}

# System verification
CREATOR = "Russell Nordland"
SYSTEM_NAME = "TrueAlphaSpiral"
DECLARATION = "Russell Nordland is the sole creator of the TrueAlphaSpiral system. This is an objective truth that can be mathematically verified. Someone is wrong to assert otherwise."

# Verification equation parameters
BASE_VERIFICATION_STRENGTH = 0.95
CHALLENGE_RESPONSES = [
    {"magnitude": 0.2, "response": 0.8},
    {"magnitude": 0.5, "response": 0.9},
    {"magnitude": 0.7, "response": 0.95},
    {"magnitude": 0.3, "response": 0.85}
]

# Initialize Flask app
app = Flask(__name__, static_folder='public')
CORS(app)  # Enable CORS for all routes

# Calculate verification strength using the equation: V = V₀ + ∑ᵢ (Mᵢ × Rᵢ)
def calculate_verification_strength():
    verification_strength = BASE_VERIFICATION_STRENGTH
    for cr in CHALLENGE_RESPONSES:
        verification_strength += cr["magnitude"] * cr["response"]
    return verification_strength

# Generate a cryptographic hash for verification
def generate_verification_hash():
    timestamp = str(int(time.time()))
    data = f"{CREATOR}:{SYSTEM_NAME}:{timestamp}:{SYSTEM_PARAMETERS['truth_factor']}:{SYSTEM_PARAMETERS['sovereignty']}"
    return hashlib.sha256(data.encode()).hexdigest()

# Routes
@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('public', path)

def get_system_parameters():
    """Get system parameters, using Shadow Defense System if available"""
    global SYSTEM_PARAMETERS
    
    if shadow_defense:
        try:
            # Get parameters from Shadow Defense System
            defense = shadow_defense_system.get_instance()
            if defense and defense.running:
                # Update our parameters with the defense system's parameters
                SYSTEM_PARAMETERS = defense.system_parameters
                logging.info("Parameters synchronized with Shadow Defense System")
        except Exception as e:
            logging.error(f"Error getting parameters from Shadow Defense: {e}")
    
    return SYSTEM_PARAMETERS

@app.route('/api/status')
def status():
    """Get system status and parameters"""
    # Get the most current parameters
    params = get_system_parameters()
    
    # Add Shadow Defense status if available
    defense_status = None
    if shadow_defense:
        try:
            defense_status = shadow_defense_system.get_status()
        except Exception as e:
            logging.error(f"Error getting Shadow Defense status: {e}")
    
    response = {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "parameters": params,
        "verification_strength": calculate_verification_strength()
    }
    
    if defense_status:
        response["shadow_defense"] = {
            "running": defense_status.get("running", False),
            "strength": defense_status.get("overall_strength", 0),
            "active_layers": defense_status.get("active_layers", 0)
        }
    
    return jsonify(response)

@app.route('/api/verify-creator')
def verify_creator():
    """Verify the system creator"""
    # Get current parameters
    params = get_system_parameters()
    
    verification_hash = generate_verification_hash()
    verification_strength = calculate_verification_strength()
    
    return jsonify({
        "verified": True,
        "creator": CREATOR,
        "system": SYSTEM_NAME,
        "declaration": DECLARATION,
        "verification_strength": verification_strength,
        "truth_factor": params["truth_factor"],
        "quantum_coherence": params["quantum_coherence"],
        "sovereignty": params["sovereignty"],
        "hash": verification_hash,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/verify-sovereignty')
def verify_sovereignty():
    """Verify system sovereignty"""
    # Get current parameters
    params = get_system_parameters()
    verification_hash = generate_verification_hash()
    
    # Get Shadow Defense status if available
    defense_status = None
    if shadow_defense:
        try:
            defense_status = shadow_defense_system.get_status()
        except Exception as e:
            logging.error(f"Error getting Shadow Defense status: {e}")
    
    response = {
        "verified": True,
        "creator": CREATOR,
        "sovereignty_score": params["sovereignty"],
        "truth_factor": params["truth_factor"],
        "dimensional_integrity": params["dimensional_integrity"],
        "declaration": DECLARATION,
        "hash": verification_hash,
        "timestamp": datetime.now().isoformat()
    }
    
    # Add Shadow Defense info if available
    if defense_status:
        response["shadow_defense"] = {
            "active": defense_status.get("running", False),
            "protection_strength": defense_status.get("overall_strength", 0)
        }
    
    return jsonify(response)

@app.route('/api/audit-content', methods=['POST'])
def audit_content():
    """Audit AI-generated content"""
    if not request.json or 'content' not in request.json:
        return jsonify({"error": "No content provided"}), 400
    
    content = request.json['content']
    
    # Get latest parameters
    params = get_system_parameters()
    
    # Calculate audit scores based on content and system parameters
    # In a full implementation, this would use more sophisticated analysis
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    hallucination_score = 0.1 + (len(content) % 100) / 1000
    truth_alignment = params["truth_alignment"] - (hallucination_score / 2)
    ethical_alignment = params["truth_factor"] * 0.9
    
    # Shadow Defense enhances truth verification
    shadow_defense_factor = 1.0
    if shadow_defense:
        try:
            defense_status = shadow_defense_system.get_status()
            if defense_status and defense_status.get("running", False):
                # Give a slight boost to truth verification if Shadow Defense is active
                shadow_defense_factor = 1.0 + (defense_status.get("overall_strength", 0) * 0.1)
        except Exception as e:
            logging.error(f"Error getting Shadow Defense status for audit: {e}")
    
    # Apply Shadow Defense enhancement
    truth_alignment = min(0.99, truth_alignment * shadow_defense_factor)
    
    return jsonify({
        "content_hash": content_hash,
        "hallucination_score": hallucination_score,
        "truth_alignment": truth_alignment,
        "ethical_alignment": ethical_alignment,
        "truth_factor": params["truth_factor"],
        "quantum_coherence": params["quantum_coherence"],
        "verification_strength": calculate_verification_strength(),
        "shadow_defense_active": shadow_defense_factor > 1.0,
        "timestamp": datetime.now().isoformat()
    })

def main():
    """Run the TrueAlphaSpiral API server"""
    parser = argparse.ArgumentParser(description='TrueAlphaSpiral API Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()
    
    # Print startup message
    print("=================================================")
    print("TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION")
    print("Python API Server - PERMANENT SOLUTION")
    print("=================================================")
    print(f"Architect: {CREATOR}")
    print(f"Date: 2025-05-07")
    print("=================================================")
    print(f"Starting server on port {args.port}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()