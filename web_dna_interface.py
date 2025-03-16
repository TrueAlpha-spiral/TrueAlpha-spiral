#!/usr/bin/env python3
"""
WEB INTERFACE FOR QUANTUM DNA VISUALIZATION

This script provides a web interface for the Quantum DNA Visualization system,
allowing for real-time monitoring and visualization of recovered interstellar
DNA patterns and their implementation locations.

Architect: Russell Nordland
"""

import os
import sys
import json
import time
import threading
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, send_from_directory

# Import the Quantum DNA Visualizer
from quantum_dna_visualization import QuantumDNAVisualizer

# Constants
DEFAULT_PORT = 8084
DEFAULT_HOST = "0.0.0.0"
OUTPUT_DIR = "quantum_visualizations"
REFRESH_INTERVAL = 5  # seconds

# Create Flask app
app = Flask(__name__)

# Global visualizer instance
visualizer = None
visualization_thread = None
running = False

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum DNA Visualization System</title>
    <style>
        :root {
            --primary-color: #0a0047;
            --secondary-color: #3a008f;
            --accent-color: #9000ff;
            --glow-color: #00ffaa;
            --text-color: #ffffff;
            --background-color: #070014;
            --card-background: #110029;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
        }
        
        header {
            background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
            color: var(--text-color);
            text-align: center;
            padding: 2rem 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(144, 0, 255, 0.3);
        }
        
        .header-content {
            position: relative;
            z-index: 2;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #ffffff, #00ffaa);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        h2 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--glow-color);
        }
        
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .card {
            background-color: var(--card-background);
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .card h3 {
            font-size: 1.2rem;
            margin-bottom: 1rem;
            color: var(--accent-color);
        }
        
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        
        .stat-box {
            text-align: center;
            padding: 1rem;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--glow-color);
            margin: 0.5rem 0;
        }
        
        .visualization {
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .visualization-item {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        
        .visualization-item img {
            width: 100%;
            height: auto;
            display: block;
        }
        
        .controls {
            margin-top: 2rem;
            display: flex;
            gap: 1rem;
            justify-content: center;
        }
        
        button {
            background: linear-gradient(to right, var(--secondary-color), var(--accent-color));
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(144, 0, 255, 0.3);
        }
        
        #patterns-container {
            margin-top: 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }
        
        .pattern-card {
            background-color: var(--card-background);
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
            cursor: pointer;
        }
        
        .pattern-card:hover {
            transform: translateY(-5px);
        }
        
        .pattern-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .pattern-id {
            font-size: 0.8rem;
            opacity: 0.7;
        }
        
        .pattern-glow {
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--glow-color);
        }
        
        .pattern-source {
            margin-bottom: 0.5rem;
        }
        
        .pattern-image {
            width: 100%;
            height: 150px;
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;
            border-radius: 5px;
            margin-top: 0.5rem;
        }
        
        .pattern-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            margin-top: 0.5rem;
            opacity: 0.8;
        }
        
        #status-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: var(--primary-color);
            color: var(--text-color);
            padding: 0.5rem 2rem;
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
        }
        
        .status-item {
            display: flex;
            align-items: center;
        }
        
        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }
        
        .active {
            background-color: var(--glow-color);
            box-shadow: 0 0 10px var(--glow-color);
        }
        
        .inactive {
            background-color: #ff3860;
        }
        
        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
            
            .stats {
                grid-template-columns: 1fr;
            }
            
            .controls {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>Quantum DNA Visualization System</h1>
            <p>Track interstellar DNA patterns and glow signatures across the metaverse</p>
        </div>
    </header>
    
    <div class="container">
        <div class="dashboard">
            <div class="card">
                <h3>System Status</h3>
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-label">Patterns</div>
                        <div class="stat-value" id="patterns-count">0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Implementations</div>
                        <div class="stat-value" id="implementations-count">0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Average Glow</div>
                        <div class="stat-value" id="average-glow">0.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Sovereignty</div>
                        <div class="stat-value" id="sovereignty">0.7762</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>Controls</h3>
                <div class="controls">
                    <button id="register-pattern">Register New Pattern</button>
                    <button id="add-implementation">Add Implementation</button>
                    <button id="generate-report">Generate Report</button>
                </div>
            </div>
        </div>
        
        <div class="visualization">
            <h2>Global Implementation Map</h2>
            <div class="visualization-item">
                <img id="world-map" src="/visualization/world_map" alt="World Map" />
            </div>
            
            <h2>METAfloor Dimensional Resonance</h2>
            <div class="visualization-item">
                <img id="dimensional-resonance" src="/visualization/dimensional_resonance" alt="Dimensional Resonance" />
            </div>
            
            <h2>Glow History</h2>
            <div class="visualization-item">
                <img id="glow-history" src="/visualization/glow_history" alt="Glow History" />
            </div>
        </div>
        
        <h2>Active DNA Patterns</h2>
        <div id="patterns-container">
            <!-- Patterns will be added here dynamically -->
        </div>
    </div>
    
    <div id="status-bar">
        <div class="status-item">
            <div class="status-indicator active" id="system-status-indicator"></div>
            <span id="system-status">System Active</span>
        </div>
        <div class="status-item">
            <span id="timestamp">{{ timestamp }}</span>
        </div>
        <div class="status-item">
            <span id="alignment">Cosmic Alignment: <span id="alignment-value">0.9851</span></span>
        </div>
    </div>
    
    <script>
        // Initialize the dashboard
        document.addEventListener('DOMContentLoaded', function() {
            // Fetch initial data
            fetchDashboardData();
            
            // Set up auto-refresh
            setInterval(fetchDashboardData, {{ refresh_interval }} * 1000);
            
            // Set up buttons
            document.getElementById('register-pattern').addEventListener('click', function() {
                fetch('/api/register_pattern', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showNotification('New pattern registered: ' + data.pattern_id);
                            fetchDashboardData();
                        }
                    });
            });
            
            document.getElementById('add-implementation').addEventListener('click', function() {
                fetch('/api/add_implementation', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showNotification('New implementation added for pattern: ' + data.pattern_id);
                            fetchDashboardData();
                        } else {
                            showNotification('Failed to add implementation: No patterns available', 'error');
                        }
                    });
            });
            
            document.getElementById('generate-report').addEventListener('click', function() {
                fetch('/api/generate_report', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showNotification('Report generated');
                            window.open('/report/' + data.report_dir, '_blank');
                        }
                    });
            });
            
            // Update timestamp
            updateTimestamp();
            setInterval(updateTimestamp, 1000);
        });
        
        // Fetch dashboard data
        function fetchDashboardData() {
            fetch('/api/dashboard')
                .then(response => response.json())
                .then(data => {
                    // Update stats
                    document.getElementById('patterns-count').textContent = data.pattern_count;
                    document.getElementById('implementations-count').textContent = data.implementation_count;
                    document.getElementById('average-glow').textContent = data.average_glow.toFixed(2);
                    document.getElementById('alignment-value').textContent = data.cosmic_alignment.toFixed(4);
                    
                    // Update visualizations with cache busting
                    const timestamp = Date.now();
                    document.getElementById('world-map').src = '/visualization/world_map?' + timestamp;
                    document.getElementById('dimensional-resonance').src = '/visualization/dimensional_resonance?' + timestamp;
                    document.getElementById('glow-history').src = '/visualization/glow_history?' + timestamp;
                    
                    // Update patterns
                    updatePatterns(data.patterns);
                });
        }
        
        // Update patterns display
        function updatePatterns(patterns) {
            const container = document.getElementById('patterns-container');
            container.innerHTML = '';
            
            patterns.forEach(pattern => {
                const card = document.createElement('div');
                card.className = 'pattern-card';
                card.setAttribute('data-id', pattern.id);
                
                card.innerHTML = `
                    <div class="pattern-header">
                        <div class="pattern-id">${pattern.id}</div>
                        <div class="pattern-glow">${pattern.glow.toFixed(2)}</div>
                    </div>
                    <div class="pattern-source">Source: ${pattern.source}</div>
                    <div class="pattern-image" style="background-image: url('/visualization/pattern/${pattern.id}?${Date.now()}')"></div>
                    <div class="pattern-meta">
                        <div>Implementations: ${pattern.implementations}</div>
                        <div>Channel: ${pattern.channel}</div>
                    </div>
                `;
                
                card.addEventListener('click', function() {
                    window.open('/visualization/pattern/${pattern.id}', '_blank');
                });
                
                container.appendChild(card);
            });
        }
        
        // Update timestamp
        function updateTimestamp() {
            const now = new Date();
            const timestamp = now.toISOString().replace('T', ' ').substring(0, 19);
            document.getElementById('timestamp').textContent = timestamp;
        }
        
        // Show notification
        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = 'notification ' + type;
            notification.textContent = message;
            notification.style.position = 'fixed';
            notification.style.top = '20px';
            notification.style.right = '20px';
            notification.style.padding = '15px 25px';
            notification.style.background = type === 'success' ? '#00ffaa' : '#ff3860';
            notification.style.color = type === 'success' ? '#000' : '#fff';
            notification.style.borderRadius = '5px';
            notification.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.3)';
            notification.style.zIndex = '1000';
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            notification.style.transition = 'opacity 0.3s, transform 0.3s';
            
            document.body.appendChild(notification);
            
            // Animate in
            setTimeout(() => {
                notification.style.opacity = '1';
                notification.style.transform = 'translateY(0)';
            }, 10);
            
            // Remove after delay
            setTimeout(() => {
                notification.style.opacity = '0';
                notification.style.transform = 'translateY(-20px)';
                
                // Remove from DOM after animation
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 3000);
        }
    </script>
</body>
</html>
"""

def initialize():
    """Initialize the system."""
    global visualizer
    visualizer = QuantumDNAVisualizer()
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize with some patterns
    register_initial_patterns()
    
    print(f"Quantum DNA Visualization system initialized")
    return visualizer

def register_initial_patterns(count=3):
    """Register some initial patterns."""
    global visualizer
    
    patterns = []
    for i in range(count):
        pattern_id = visualizer.register_pattern()
        patterns.append(pattern_id)
        
        # Add some implementations
        for _ in range(2):
            visualizer.add_implementation(pattern_id)
    
    return patterns

def visualization_loop():
    """Run the visualization loop in a background thread."""
    global visualizer, running
    
    while running:
        try:
            # Generate visualizations
            visualizer.visualize_world_map(os.path.join(OUTPUT_DIR, "world_map.png"))
            visualizer.visualize_dimensional_resonance(os.path.join(OUTPUT_DIR, "dimensional_resonance.png"))
            visualizer.visualize_glow_history(os.path.join(OUTPUT_DIR, "glow_history.png"))
            
            # Generate pattern visualizations
            for pattern_id in visualizer.dna_patterns:
                visualizer.visualize_pattern_glow(
                    pattern_id, 
                    os.path.join(OUTPUT_DIR, f"pattern_{pattern_id}.png")
                )
            
            # Sleep for a bit
            time.sleep(REFRESH_INTERVAL)
        except Exception as e:
            print(f"Error in visualization loop: {e}")
            time.sleep(1)


# Flask routes
@app.route('/')
def index():
    """Render the main page."""
    return render_template_string(
        HTML_TEMPLATE, 
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        refresh_interval=REFRESH_INTERVAL
    )

@app.route('/visualization/<visualization_type>')
def get_visualization(visualization_type):
    """Get a visualization image."""
    if visualization_type == 'world_map':
        return send_from_directory(OUTPUT_DIR, "world_map.png")
    elif visualization_type == 'dimensional_resonance':
        return send_from_directory(OUTPUT_DIR, "dimensional_resonance.png")
    elif visualization_type == 'glow_history':
        return send_from_directory(OUTPUT_DIR, "glow_history.png")
    else:
        return "Visualization not found", 404

@app.route('/visualization/pattern/<pattern_id>')
def get_pattern_visualization(pattern_id):
    """Get a pattern visualization image."""
    return send_from_directory(OUTPUT_DIR, f"pattern_{pattern_id}.png")

@app.route('/api/dashboard')
def get_dashboard_data():
    """Get dashboard data."""
    global visualizer
    
    if not visualizer:
        return jsonify({"error": "Visualizer not initialized"}), 500
    
    patterns = []
    for pattern_id, pattern in visualizer.dna_patterns.items():
        patterns.append({
            "id": pattern_id,
            "source": pattern["stellar_source"]["name"],
            "glow": visualizer.glow_factors.get(pattern_id, 0.0),
            "implementations": len(pattern["implementations"]),
            "channel": pattern["channel_type"]
        })
    
    # Sort patterns by glow factor
    patterns.sort(key=lambda p: p["glow"], reverse=True)
    
    implementation_count = sum(len(p["implementations"]) for p in visualizer.dna_patterns.values())
    
    # Calculate average glow
    average_glow = 0.0
    if visualizer.glow_factors:
        average_glow = sum(visualizer.glow_factors.values()) / len(visualizer.glow_factors)
    
    # Get cosmic alignment from TrueAlphaSpiral
    cosmic_alignment = 0.9851  # Default from system logs
    
    return jsonify({
        "pattern_count": len(visualizer.dna_patterns),
        "implementation_count": implementation_count,
        "average_glow": average_glow,
        "patterns": patterns,
        "cosmic_alignment": cosmic_alignment
    })

@app.route('/api/register_pattern', methods=['POST'])
def register_pattern():
    """Register a new pattern."""
    global visualizer
    
    if not visualizer:
        return jsonify({"error": "Visualizer not initialized"}), 500
    
    pattern_id = visualizer.register_pattern()
    
    return jsonify({
        "success": True,
        "pattern_id": pattern_id
    })

@app.route('/api/add_implementation', methods=['POST'])
def add_implementation():
    """Add a new implementation."""
    global visualizer
    
    if not visualizer:
        return jsonify({"error": "Visualizer not initialized"}), 500
    
    if not visualizer.dna_patterns:
        return jsonify({
            "success": False,
            "message": "No patterns available"
        })
    
    # Get a random pattern
    import random
    pattern_id = random.choice(list(visualizer.dna_patterns.keys()))
    
    # Add an implementation
    visualizer.add_implementation(pattern_id)
    
    return jsonify({
        "success": True,
        "pattern_id": pattern_id
    })

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """Generate a comprehensive report."""
    global visualizer
    
    if not visualizer:
        return jsonify({"error": "Visualizer not initialized"}), 500
    
    report_dir = visualizer.generate_comprehensive_report()
    
    return jsonify({
        "success": True,
        "report_dir": os.path.basename(report_dir)
    })

@app.route('/report/<path:report_path>')
def get_report(report_path):
    """Get a report file."""
    # Determine if we're looking at a directory or file
    full_path = os.path.join(OUTPUT_DIR, report_path)
    
    if os.path.isdir(full_path):
        # If it's a directory, list the files
        files = os.listdir(full_path)
        html = "<html><head><title>Report Files</title></head><body>"
        html += f"<h1>Report: {report_path}</h1>"
        html += "<ul>"
        
        for file in files:
            file_path = os.path.join(report_path, file)
            html += f"<li><a href='/report/{file_path}'>{file}</a></li>"
        
        html += "</ul></body></html>"
        return html
    else:
        # If it's a file, serve it
        return send_from_directory(OUTPUT_DIR, report_path)

def main():
    """Run the web interface."""
    global visualizer, visualization_thread, running
    
    import argparse
    parser = argparse.ArgumentParser(description="Quantum DNA Visualization Web Interface")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to run the server on")
    parser.add_argument("--host", type=str, default=DEFAULT_HOST, help="Host to run the server on")
    
    args = parser.parse_args()
    
    # Initialize the system
    visualizer = initialize()
    
    # Start the visualization thread
    running = True
    visualization_thread = threading.Thread(target=visualization_loop)
    visualization_thread.daemon = True
    visualization_thread.start()
    
    try:
        # Run the Flask app
        app.run(host=args.host, port=args.port, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        running = False
        if visualization_thread:
            visualization_thread.join(timeout=1)
        print("Web interface shutdown")

if __name__ == "__main__":
    main()