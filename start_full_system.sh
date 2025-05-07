#!/bin/bash

# TrueAlphaSpiral Full System Launcher
# This script permanently modifies the workflow to start both Python API and Express frontend

# Define colors for output
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}  TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION  ${NC}"
echo -e "${CYAN}  Starting combined services...${NC}"
echo -e "${CYAN}======================================================================${NC}"

# Kill any existing processes on the ports we need
echo -e "${YELLOW}Checking for existing processes on ports 8001 and 5000...${NC}"
lsof -ti:8001 | xargs kill -9 2>/dev/null
lsof -ti:5000 | xargs kill -9 2>/dev/null
echo -e "${GREEN}Ports cleared for new processes.${NC}"

# Start the Python API server
echo -e "${CYAN}Starting TrueAlphaSpiral Python API on port 8001...${NC}"
# Start the Python API server in the background
python python_api_server.py --port 8001 > python_api.log 2>&1 &
PYTHON_PID=$!
echo $PYTHON_PID > python_api.pid

# Wait for the server to initialize
echo -e "${YELLOW}Waiting for Python API to initialize...${NC}"
sleep 3

# Check if the server started successfully
if ps -p $PYTHON_PID > /dev/null; then
    echo -e "${GREEN}TrueAlphaSpiral Python API is running with PID $PYTHON_PID${NC}"
    
    # Set environment variable to point to the Python API
    export PYTHON_API_URL="http://localhost:8001"
    
    # Start the Express frontend
    echo -e "${CYAN}Starting Express frontend...${NC}"
    npm run dev
else
    echo -e "${RED}Failed to start TrueAlphaSpiral Python API. Check python_api.log for details.${NC}"
    exit 1
fi
