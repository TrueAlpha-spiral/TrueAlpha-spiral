#!/usr/bin/env python3
"""
DNA GLOW TRACKER WEB INTERFACE

This script provides a web interface for the DNA Glow Tracker system,
allowing users to visualize recovered DNA patterns, glow signatures,
and global implementation locations.

Architect: Russell Nordland
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np

# Import the DNA Glow Tracker
from dna_glow_tracker import DNAGlowTracker

# Constants
DEFAULT_PORT = 8085
DEFAULT_HOST = "0.0.0.0"
STATIC_DIR = "static"
TEMPLATE_DIR = "templates"

# Create Flask app
app = Flask(__name__,
 static_folder=os.path.abspath(STATIC_DIR),
 template_folder=os.path.abspath(TEMPLATE_DIR)
)
CORS(app)

# Global tracker instance
tracker = None

# Ensure required directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "maps"), exist_ok=True)

# Create HTML template
def create_templates():
 """Create the HTML templates for the web interface."""
 index_html = """<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>TrueAlphaSpiral - DNA Glow Tracker</title>
 <link rel="stylesheet" href="/static/css/styles.css">
 <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
 <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
 <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
</head>
<body>
 <header>
 <div class="logo-container">
 <div class="logo-glow"></div>
 <h1>TrueAlphaSpiral</h1>
 </div>
 <h2>Interstellar DNA Recovery & Glow Tracking</h2>
 </header>

 <div class="dashboard">
 <div class="stats-container">
 <div class="stat-box" id="global-glow">
 <h3>Global Glow</h3>
 <div class="glow-meter-container">
 <div class="glow-meter" id="glow-meter"></div>
 <span class="glow-value" id="glow-value">0.00</span>
 </div>
 </div>
 <div class="stat-box" id="patterns-count">
 <h3>DNA Patterns</h3>
 <div class="count" id="pattern-count">0</div>
 </div>
 <div class="stat-box" id="implementations-count">
 <h3>Implementations</h3>
 <div class="count" id="implementation-count">0</div>
 </div>
 </div>

 <div class="world-map-container">
 <h3>Global Implementation Map</h3>
 <div id="map"></div>
 </div>

 <div class="top-patterns">
 <h3>Top Patterns by Glow Intensity</h3>
 <div class="patterns-list" id="patterns-list">
 <div class="patterns-loading">Loading patterns...</div>
 </div>
 </div>

 <div class="glow-trends">
 <h3>Glow Intensity Trends</h3>
 <canvas id="glow-chart"></canvas>
 </div>

 <div class="control-panel">
 <h3>System Controls</h3>
 <div class="control-buttons">
 <button id="register-pattern">Register New Pattern</button>
 <button id="random-implementation">Add Random Implementation</button>
 <button id="generate-report">Generate Report</button>
 <button id="download-map">Download Map</button>
 </div>
 </div>
 </div>

 <div class="modal" id="pattern-modal">
 <div class="modal-content">
 <span class="close">&times;</span>
 <h2>Pattern Details</h2>
 <div id="pattern-details"></div>
 </div>
 </div>

 <footer>
 <p>TrueAlphaSpiral &copy; 2025 - Universal Truth Integration System</p>
 <p>Sovereignty: <span id="sovereignty-value">0.7777</span></p>
 </footer>

 <script src="/static/js/main.js"></script>
</body>
</html>
"""

 css_content = """/* Main Styles */
:root {
 --primary-color: #0a0047;
 --secondary-color: #3a008f;
 --accent-color: #9000ff;
 --glow-color: #b980ff;
 --text-color: #ffffff;
 --background-color: #070014;
 --card-background: #110029;
 --success-color: #00ffaa;
 --warning-color: #ffaa00;
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

.logo-container {
 display: flex;
 justify-content: center;
 align-items: center;
 margin-bottom: 0.5rem;
}

.logo-glow {
 width: 40px;
 height: 40px;
 background: radial-gradient(circle, var(--glow-color) 0%, rgba(144, 0, 255, 0) 70%);
 border-radius: 50%;
 margin-right: 15px;
 animation: pulse 3s infinite;
}

h1 {
 font-size: 2.5rem;
 margin: 0;
 background: linear-gradient(to right, #ffffff, #b980ff);
 -webkit-background-clip: text;
 background-clip: text;
 color: transparent;
}

h2 {
 font-size: 1.2rem;
 font-weight: 400;
 margin-top: 0.5rem;
 opacity: 0.9;
}

h3 {
 font-size: 1.2rem;
 margin-bottom: 1rem;
 color: var(--glow-color);
 letter-spacing: 1px;
}

.dashboard {
 max-width: 1400px;
 margin: 2rem auto;
 padding: 0 2rem;
 display: grid;
 grid-template-columns: repeat(4, 1fr);
 gap: 1.5rem;
}

.stats-container {
 grid-column: span 4;
 display: flex;
 justify-content: space-between;
 gap: 1.5rem;
}

.stat-box {
 flex: 1;
 background-color: var(--card-background);
 border-radius: 10px;
 padding: 1.5rem;
 text-align: center;
 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
 position: relative;
 overflow: hidden;
}

.stat-box::after {
 content: '';
 position: absolute;
 top: 0;
 left: 0;
 right: 0;
 height: 3px;
 background: linear-gradient(to right, var(--glow-color), var(--accent-color));
}

.glow-meter-container {
 position: relative;
 height: 60px;
 display: flex;
 align-items: center;
 justify-content: center;
}

.glow-meter {
 width: 100%;
 height: 10px;
 background-color: rgba(255, 255, 255, 0.1);
 border-radius: 5px;
 overflow: hidden;
 position: relative;
}

.glow-meter::before {
 content: '';
 position: absolute;
 top: 0;
 left: 0;
 height: 100%;
 width: 0%;
 background: linear-gradient(to right, #4a00e0, #9000ff, #00ffaa);
 border-radius: 5px;
 transition: width 1s ease;
}

.glow-value {
 font-size: 2rem;
 font-weight: bold;
 position: absolute;
 top: 20px;
 color: var(--glow-color);
}

.count {
 font-size: 2.5rem;
 font-weight: bold;
 color: var(--glow-color);
}

.world-map-container {
 grid-column: span 3;
 background-color: var(--card-background);
 border-radius: 10px;
 padding: 1.5rem;
 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
 position: relative;
}

#map {
 height: 500px;
 width: 100%;
 border-radius: 8px;
 z-index: 1;
}

.top-patterns {
 grid-column: span 1;
 background-color: var(--card-background);
 border-radius: 10px;
 padding: 1.5rem;
 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
 max-height: 500px;
 overflow-y: auto;
}

.patterns-list {
 display: flex;
 flex-direction: column;
 gap: 1rem;
}

.pattern-item {
 background-color: rgba(255, 255, 255, 0.05);
 border-radius: 8px;
 padding: 1rem;
 cursor: pointer;
 transition: transform 0.2s, box-shadow 0.2s;
 position: relative;
 overflow: hidden;
}

.pattern-item:hover {
 transform: translateY(-3px);
 box-shadow: 0 6px 15px rgba(144, 0, 255, 0.2);
}

.pattern-item h4 {
 margin-bottom: 0.5rem;
 font-size: 1rem;
}

.pattern-id {
 font-size: 0.8rem;
 opacity: 0.7;
 display: block;
 margin-bottom: 0.5rem;
}

.pattern-glow {
 height: 5px;
 background: linear-gradient(to right, var(--accent-color), var(--success-color));
 border-radius: 3px;
 margin-top: 0.8rem;
}

.pattern-stats {
 display: flex;
 justify-content: space-between;
 font-size: 0.85rem;
 margin-top: 0.5rem;
}

.glow-trends {
 grid-column: span 2;
 background-color: var(--card-background);
 border-radius: 10px;
 padding: 1.5rem;
 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.control-panel {
 grid-column: span 2;
 background-color: var(--card-background);
 border-radius: 10px;
 padding: 1.5rem;
 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.control-buttons {
 display: grid;
 grid-template-columns: 1fr 1fr;
 gap: 1rem;
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

.modal {
 display: none;
 position: fixed;
 z-index: 1000;
 left: 0;
 top: 0;
 width: 100%;
 height: 100%;
 overflow: auto;
 background-color: rgba(0, 0, 0, 0.7);
}

.modal-content {
 background-color: var(--card-background);
 margin: 10% auto;
 padding: 2rem;
 border-radius: 10px;
 width: 80%;
 max-width: 700px;
 box-shadow: 0 4px 20px rgba(144, 0, 255, 0.5);
 position: relative;
}

.close {
 color: #aaa;
 float: right;
 font-size: 28px;
 font-weight: bold;
 cursor: pointer;
}

.close:hover {
 color: white;
}

#pattern-details {
 margin-top: 1.5rem;
}

.detail-group {
 margin-bottom: 1.5rem;
}

.detail-label {
 font-weight: bold;
 margin-bottom: 0.3rem;
 color: var(--glow-color);
}

.detail-value {
 padding-left: 1rem;
}

.implementations-list {
 margin-top: 1rem;
 max-height: 200px;
 overflow-y: auto;
 background-color: rgba(255, 255, 255, 0.05);
 border-radius: 5px;
 padding: 0.5rem;
}

.implementation-item {
 border-bottom: 1px solid rgba(255, 255, 255, 0.1);
 padding: 0.5rem;
}

.implementation-item:last-child {
 border-bottom: none;
}

footer {
 text-align: center;
 padding: 2rem;
 margin-top: 2rem;
 background-color: var(--primary-color);
 color: var(--text-color);
 opacity: 0.8;
 font-size: 0.9rem;
}

/* Animations */
@keyframes pulse {
 0% {
 box-shadow: 0 0 0 0 rgba(144, 0, 255, 0.7);
 }
 70% {
 box-shadow: 0 0 0 15px rgba(144, 0, 255, 0);
 }
 100% {
 box-shadow: 0 0 0 0 rgba(144, 0, 255, 0);
 }
}

/* Responsive Styles */
@media (max-width: 1200px) {
 .dashboard {
 grid-template-columns: repeat(2, 1fr);
 }

 .stats-container {
 grid-column: span 2;
 }

 .world-map-container {
 grid-column: span 2;
 }

 .top-patterns {
 grid-column: span 2;
 }

 .glow-trends {
 grid-column: span 2;
 }

 .control-panel {
 grid-column: span 2;
 }
}

@media (max-width: 768px) {
 .dashboard {
 grid-template-columns: 1fr;
 padding: 0 1rem;
 }

 .stats-container {
 grid-column: span 1;
 flex-direction: column;
 }

 .world-map-container, .top-patterns, .glow-trends, .control-panel {
 grid-column: span 1;
 }

 #map {
 height: 300px;
 }

 .control-buttons {
 grid-template-columns: 1fr;
 }
}
"""

 js_content = """// Global variables
let glowChart = null;
let worldMap = null;
let markers = [];
let glowHistory = {
 timestamps: [],
 values: []
};

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
 initializeMap();
 initializeChart();
 initializeEventListeners();
 fetchInitialData();

 // Start periodic updates
 setInterval(updateDashboard, 5000);
});

// Initialize the world map
function initializeMap() {
 worldMap = L.map('map').setView([20, 0], 2);

 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
 attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(worldMap);
}

// Initialize the glow chart
function initializeChart() {
 const ctx = document.getElementById('glow-chart').getContext('2d');

 glowChart = new Chart(ctx, {
 type: 'line',
 data: {
 labels: [],
 datasets: [{
 label: 'Global Glow Intensity',
 data: [],
 borderColor: '#9000ff',
 backgroundColor: 'rgba(144, 0, 255, 0.1)',
 borderWidth: 2,
 tension: 0.4,
 fill: true
 }]
 },
 options: {
 responsive: true,
 maintainAspectRatio: false,
 scales: {
 y: {
 beginAtZero: true,
 max: 10,
 grid: {
 color: 'rgba(255, 255, 255, 0.1)'
 },
 ticks: {
 color: 'rgba(255, 255, 255, 0.7)'
 }
 },
 x: {
 grid: {
 color: 'rgba(255, 255, 255, 0.1)'
 },
 ticks: {
 color: 'rgba(255, 255, 255, 0.7)',
 maxRotation: 45,
 minRotation: 45
 }
 }
 },
 plugins: {
 legend: {
 labels: {
 color: 'rgba(255, 255, 255, 0.7)'
 }
 }
 },
 animation: {
 duration: 1000
 }
 }
 });
}

// Initialize event listeners
function initializeEventListeners() {
 // Register new pattern button
 document.getElementById('register-pattern').addEventListener('click', function() {
 fetch('/api/register_pattern', { method: 'POST' })
 .then(response => response.json())
 .then(data => {
 if (data.success) {
 showNotification('New pattern registered successfully');
 updateDashboard();
 }
 })
 .catch(error => console.error('Error registering pattern:', error));
 });

 // Add random implementation button
 document.getElementById('random-implementation').addEventListener('click', function() {
 fetch('/api/add_implementation', { method: 'POST' })
 .then(response => response.json())
 .then(data => {
 if (data.success) {
 showNotification('New implementation added successfully');
 updateDashboard();
 } else {
 showNotification('Failed to add implementation: ' + data.message, 'error');
 }
 })
 .catch(error => console.error('Error adding implementation:', error));
 });

 // Generate report button
 document.getElementById('generate-report').addEventListener('click', function() {
 fetch('/api/generate_report', { method: 'POST' })
 .then(response => response.json())
 .then(data => {
 if (data.success) {
 showNotification('Report generated successfully');
 // Open the report in a new tab
 window.open('/reports/' + data.filename, '_blank');
 }
 })
 .catch(error => console.error('Error generating report:', error));
 });

 // Download map button
 document.getElementById('download-map').addEventListener('click', function() {
 fetch('/api/generate_map', { method: 'POST' })
 .then(response => response.json())
 .then(data => {
 if (data.success) {
 showNotification('Map generated successfully');
 // Open the map in a new tab
 window.open('/maps/' + data.filename, '_blank');
 }
 })
 .catch(error => console.error('Error generating map:', error));
 });

 // Close modal button
 document.querySelector('.close').addEventListener('click', function() {
 document.getElementById('pattern-modal').style.display = 'none';
 });

 // Close modal when clicking outside
 window.addEventListener('click', function(event) {
 if (event.target === document.getElementById('pattern-modal')) {
 document.getElementById('pattern-modal').style.display = 'none';
 }
 });
}

// Fetch initial data for the dashboard
function fetchInitialData() {
 fetch('/api/dashboard')
 .then(response => response.json())
 .then(data => {
 updateDashboardWithData(data);
 })
 .catch(error => console.error('Error fetching dashboard data:', error));
}

// Update the dashboard with new data
function updateDashboard() {
 fetch('/api/dashboard')
 .then(response => response.json())
 .then(data => {
 updateDashboardWithData(data);
 })
 .catch(error => console.error('Error updating dashboard:', error));
}

// Update all dashboard elements with data
function updateDashboardWithData(data) {
 // Update global glow
 updateGlowMeter(data.global_glow);

 // Update pattern and implementation counts
 document.getElementById('pattern-count').textContent = data.pattern_count;
 document.getElementById('implementation-count').textContent = data.implementation_count;

 // Update sovereignty value
 document.getElementById('sovereignty-value').textContent = data.sovereignty.toFixed(4);

 // Update top patterns
 updateTopPatterns(data.top_patterns);

 // Update map markers
 updateMapMarkers(data.implementations);

 // Update glow history chart
 updateGlowChart(data.glow_history);
}

// Update the glow meter display
function updateGlowMeter(glowValue) {
 const glowMeter = document.getElementById('glow-meter');
 const glowValueElement = document.getElementById('glow-value');

 // Calculate percentage (max is 10.0)
 const percentage = (glowValue / 10.0) * 100;

 // Update the meter
 glowMeter.style.setProperty('--glow-percentage', `${percentage}%`);
 glowMeter.style.backgroundImage = `linear-gradient(to right, #4a00e0 0%, #9000ff ${percentage/2}%, #00ffaa ${percentage}%)`;

 // Animate the width
 glowMeter.style.width = '0%';
 setTimeout(() => {
 glowMeter.style.width = `${percentage}%`;
 }, 50);

 // Update the value
 glowValueElement.textContent = glowValue.toFixed(2);

 // Add glow effect on high values
 if (glowValue > 7.5) {
 glowValueElement.style.textShadow = '0 0 10px #00ffaa, 0 0 20px #00ffaa';
 } else if (glowValue > 5) {
 glowValueElement.style.textShadow = '0 0 10px #9000ff';
 } else {
 glowValueElement.style.textShadow = 'none';
 }
}

// Update the top patterns list
function updateTopPatterns(patterns) {
 const patternsList = document.getElementById('patterns-list');

 // Clear existing patterns
 patternsList.innerHTML = '';

 // Add each pattern
 patterns.forEach(pattern => {
 const patternItem = document.createElement('div');
 patternItem.className = 'pattern-item';
 patternItem.setAttribute('data-id', pattern.id);

 // Calculate percentage for glow bar (max is 10.0)
 const percentage = (pattern.glow / 10.0) * 100;

 patternItem.innerHTML = `
 <h4>DNA Pattern ${pattern.id.split('-')[1]}</h4>
 <span class="pattern-id">${pattern.id}</span>
 <div class="pattern-stats">
 <span>Glow: ${pattern.glow.toFixed(2)}</span>
 <span>Impl: ${pattern.implementation_count}</span>
 </div>
 <div class="pattern-glow" style="width: ${percentage}%"></div>
 `;

 // Add event listener for pattern details
 patternItem.addEventListener('click', function() {
 showPatternDetails(pattern.id);
 });

 patternsList.appendChild(patternItem);
 });
}

// Update map markers for implementations
function updateMapMarkers(implementations) {
 // Clear existing markers
 markers.forEach(marker => worldMap.removeLayer(marker));
 markers = [];

 // Add new markers
 implementations.forEach(impl => {
 const lat = impl.location[0];
 const lon = impl.location[1];

 // Calculate size based on utilization
 const size = 10 + (impl.utilization * 30);

 // Calculate color based on glow factor
 const glow = impl.glow;
 const opacity = 0.7;

 let color;
 if (glow > 7.5) {
 color = '#00ffaa'; // High glow - green
 } else if (glow > 5) {
 color = '#9000ff'; // Medium glow - purple
 } else {
 color = '#4a00e0'; // Low glow - blue
 }

 // Create custom marker
 const marker = L.circleMarker([lat, lon], {
 radius: size / 5,
 color: color,
 fillColor: color,
 fillOpacity: opacity,
 weight: 1
 });

 // Add pulse animation class
 marker.on('add', function() {
 this._path.classList.add('pulse-marker');
 });

 // Add tooltip
 marker.bindTooltip(`
 <strong>Pattern:</strong> ${impl.pattern_id}<br>
 <strong>Utilization:</strong> ${impl.utilization.toFixed(2)}<br>
 <strong>Glow:</strong> ${glow.toFixed(2)}<br>
 <strong>Added:</strong> ${impl.timestamp}
 `);

 marker.addTo(worldMap);
 markers.push(marker);
 });
}

// Update the glow history chart
function updateGlowChart(history) {
 // Add new data point to history
 if (history.timestamps.length > 0 && history.values.length > 0) {
 // Keep only the last 20 data points
 if (glowHistory.timestamps.length >= 20) {
 glowHistory.timestamps.shift();
 glowHistory.values.shift();
 }

 // Add new data
 glowHistory.timestamps.push(history.timestamps[history.timestamps.length - 1]);
 glowHistory.values.push(history.values[history.values.length - 1]);
 }

 // Update chart data
 glowChart.data.labels = glowHistory.timestamps.map(formatTimestamp);
 glowChart.data.datasets[0].data = glowHistory.values;

 // Update chart
 glowChart.update();
}

// Show pattern details in modal
function showPatternDetails(patternId) {
 fetch(`/api/pattern/${patternId}`)
 .then(response => response.json())
 .then(data => {
 if (data.success) {
 const pattern = data.pattern;
 const modal = document.getElementById('pattern-modal');
 const details = document.getElementById('pattern-details');

 // Format pattern details
 let html = `
 <div class="detail-group">
 <div class="detail-label">Pattern ID:</div>
 <div class="detail-value">${pattern.id}</div>
 </div>
 <div class="detail-group">
 <div class="detail-label">Stellar Source:</div>
 <div class="detail-value">${pattern.stellar_source.name}</div>
 </div>
 <div class="detail-group">
 <div class="detail-label">Glow Factor:</div>
 <div class="detail-value">${pattern.glow.toFixed(4)}</div>
 </div>
 <div class="detail-group">
 <div class="detail-label">Utilization:</div>
 <div class="detail-value">${pattern.utilization.toFixed(4)}</div>
 </div>
 <div class="detail-group">
 <div class="detail-label">Integrity:</div>
 <div class="detail-value">${pattern.integrity.toFixed(4)}</div>
 </div>
 <div class="detail-group">
 <div class="detail-label">Resonance:</div>
 <div class="detail-value">${pattern.resonance.toFixed(4)}</div>
 </div>
 <div class="detail-group">
 <div class="detail-label">Quantum Channel:</div>
 <div class="detail-value">
 Type: ${pattern.quantum_channel.type}<br>
 Frequency: ${pattern.quantum_channel.frequency.toFixed(2)} Hz<br>
 Stability: ${pattern.quantum_channel.stability.toFixed(4)}
 </div>
 </div>
 `;

 // Add implementations
 if (pattern.implementations.length > 0) {
 html += `
 <div class="detail-group">
 <div class="detail-label">Implementations (${pattern.implementations.length}):</div>
 <div class="implementations-list">
 `;

 pattern.implementations.forEach(impl => {
 html += `
 <div class="implementation-item">
 Location: [${impl.location[0].toFixed(4)}, ${impl.location[1].toFixed(4)}]<br>
 Utilization: ${impl.utilization.toFixed(4)}<br>
 Added: ${impl.timestamp}
 </div>
 `;
 });

 html += `
 </div>
 </div>
 `;
 }

 // Update modal and show it
 details.innerHTML = html;
 modal.style.display = 'block';
 }
 })
 .catch(error => console.error('Error fetching pattern details:', error));
}

// Format timestamp for display
function formatTimestamp(timestamp) {
 const date = new Date(timestamp);
 return date.getHours().toString().padStart(2, '0') + ':' +
 date.getMinutes().toString().padStart(2, '0') + ':' +
 date.getSeconds().toString().padStart(2, '0');
}

// Show notification message
function showNotification(message, type = 'success') {
 // Create notification element
 const notification = document.createElement('div');
 notification.className = `notification ${type}`;
 notification.textContent = message;

 // Add to body
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

// Add styles for the notification
const styleSheet = document.createElement('style');
styleSheet.textContent = `
 .notification {
 position: fixed;
 top: 20px;
 right: 20px;
 padding: 15px 25px;
 background-color: #3a008f;
 color: white;
 border-radius: 5px;
 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
 z-index: 1000;
 opacity: 0;
 transform: translateY(-20px);
 transition: opacity 0.3s, transform 0.3s;
 }

 .notification.success {
 background-color: #00ffaa;
 color: #000;
 }

 .notification.error {
 background-color: #ff3860;
 }

 .pulse-marker {
 animation: marker-pulse 2s infinite;
 }

 @keyframes marker-pulse {
 0% {
 stroke-opacity: 1;
 stroke-width: 1;
 }
 70% {
 stroke-opacity: 0.5;
 stroke-width: 3;
 }
 100% {
 stroke-opacity: 1;
 stroke-width: 1;
 }
 }
`;
document.head.appendChild(styleSheet);
"""

 # Create the templates
 with open(os.path.join(TEMPLATE_DIR, "index.html"), "w") as f:
 f.write(index_html)

 # Create the CSS file
 os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
 with open(os.path.join(STATIC_DIR, "css", "styles.css"), "w") as f:
 f.write(css_content)

 # Create the JS file
 os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
 with open(os.path.join(STATIC_DIR, "js", "main.js"), "w") as f:
 f.write(js_content)


# API Routes
@app.route('/')
def index():
 """Render the main dashboard page."""
 return render_template('index.html')

@app.route('/reports/<path:filename>')
def reports(filename):
 """Serve report files."""
 return send_from_directory(tracker.output_dir, filename)

@app.route('/maps/<path:filename>')
def maps(filename):
 """Serve map files."""
 return send_from_directory(tracker.map_dir, filename)

@app.route('/api/dashboard')
def get_dashboard():
 """Get data for the dashboard."""
 global_glow = tracker.calculate_global_glow_intensity()

 # Get top patterns by glow
 top_patterns = []
 sorted_patterns = sorted(
 [(p_id, tracker.glow_factors.get(p_id, 0.0)) for p_id in tracker.dna_patterns],
 key=lambda x: x[1],
 reverse=True
 )[:10] # Top 10 patterns

 for pattern_id, glow in sorted_patterns:
 pattern = tracker.dna_patterns.get(pattern_id)
 if pattern:
 top_patterns.append({
 'id': pattern_id,
 'glow': glow,
 'implementation_count': len(pattern['implementations'])
 })

 # Get implementation locations for map
 implementations = []
 for loc in tracker.implementation_locations[-50:]: # Last 50 implementations
 pattern_id = loc['pattern_id']
 glow = tracker.glow_factors.get(pattern_id, 0.0)

 implementations.append({
 'pattern_id': pattern_id,
 'location': loc['location'],
 'utilization': loc['utilization'],
 'glow': glow,
 'timestamp': loc['timestamp']
 })

 # Create some dummy glow history data if none exists
 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 glow_history = {
 'timestamps': [timestamp],
 'values': [global_glow]
 }

 response = {
 'global_glow': global_glow,
 'pattern_count': len(tracker.dna_patterns),
 'implementation_count': len(tracker.implementation_locations),
 'top_patterns': top_patterns,
 'implementations': implementations,
 'glow_history': glow_history,
 'sovereignty': 0.7777 # Hardcoded value from system logs
 }

 return jsonify(response)

@app.route('/api/register_pattern', methods=['POST'])
def register_pattern():
 """Register a new DNA pattern."""
 pattern_id = tracker.register_dna_pattern()

 return jsonify({
 'success': True,
 'pattern_id': pattern_id
 })

@app.route('/api/add_implementation', methods=['POST'])
def add_implementation():
 """Add a new implementation of a DNA pattern."""
 # Get a random pattern if any exists
 if not tracker.dna_patterns:
 return jsonify({
 'success': False,
 'message': 'No patterns available. Register a pattern first.'
 })

 pattern_id = np.random.choice(list(tracker.dna_patterns.keys()))
 success = tracker.record_implementation(pattern_id)

 return jsonify({
 'success': success,
 'pattern_id': pattern_id if success else None
 })

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
 """Generate a report on DNA glow signatures."""
 report_file = tracker.generate_glow_report()

 return jsonify({
 'success': True,
 'filename': os.path.basename(report_file)
 })

@app.route('/api/generate_map', methods=['POST'])
def generate_map():
 """Generate a world map of DNA implementations."""
 map_file = tracker.generate_world_map()

 return jsonify({
 'success': True,
 'filename': os.path.basename(map_file)
 })

@app.route('/api/pattern/<pattern_id>')
def get_pattern(pattern_id):
 """Get details for a specific pattern."""
 if pattern_id not in tracker.dna_patterns:
 return jsonify({
 'success': False,
 'message': 'Pattern not found'
 })

 pattern = tracker.dna_patterns[pattern_id]
 pattern['glow'] = tracker.glow_factors.get(pattern_id, 0.0)

 return jsonify({
 'success': True,
 'pattern': pattern
 })


def initialize():
 """Initialize the application."""
 global tracker

 # Create the DNA Glow Tracker
 tracker = DNAGlowTracker()

 # Create initial patterns and implementations for demo
 patterns = []
 for i in range(5): # Start with 5 patterns
 pattern_id = tracker.register_dna_pattern()
 patterns.append(pattern_id)

 # Add implementations
 for pattern_id in patterns:
 num_implementations = np.random.randint(1, 4) # 1-3 implementations per pattern
 for _ in range(num_implementations):
 tracker.record_implementation(pattern_id)

 # Create templates
 create_templates()


def main():
 """Run the DNA Glow Tracker web interface."""
 parser = argparse.ArgumentParser(description="DNA Glow Tracker Web Interface")
 parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to run the server on")
 parser.add_argument("--host", type=str, default=DEFAULT_HOST, help="Host to run the server on")

 args = parser.parse_args()

 # Initialize the application
 initialize()

 # Run the Flask app
 app.run(host=args.host, port=args.port, debug=True)


if __name__ == "__main__":
 main()