#!/bin/bash

# TrueAlphaSpiral API Server Launcher
# Author: Russell Nordland

echo "======================================================"
echo "   STARTING TRUE ALPHA SPIRAL API SERVER"
echo "======================================================"

# Ensure proper permissions
chmod +x python_api_server.py

# Start the API server
python python_api_server.py