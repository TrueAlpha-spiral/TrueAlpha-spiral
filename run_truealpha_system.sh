#!/bin/bash

# TrueAlphaSpiral System Launcher
# This script starts both the Python API server and the Express frontend

echo "======================================================================"
echo " TRUEALPHASPIRAL SYSTEM LAUNCHER "
echo " Architect: Russell Nordland "
echo " Date: $(date)"
echo "======================================================================"

# Define colors for output
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# Kill any existing processes on the ports we need
kill_existing_processes() {
 echo -e "${YELLOW}Checking for existing processes on ports 8001 and 5000...${NC}"
 lsof -ti:8001 | xargs kill -9 2>/dev/null
 lsof -ti:5000 | xargs kill -9 2>/dev/null
 echo -e "${GREEN}Ports cleared for new processes.${NC}"
}

# Start the Python API server
start_python_api() {
 echo -e "${CYAN}Starting TrueAlphaSpiral Python API on port 8001...${NC}"
 # Start the Python API server in the background
 python python_api_server.py --port 8001 > python_api.log 2>&1 &
 PYTHON_PID=$!
 echo $PYTHON_PID > python_api.pid

 # Wait for the server to initialize
 echo -e "${YELLOW}Waiting for Python API to initialize...${NC}"
 sleep 2

 # Check if the server started successfully
 if ps -p $PYTHON_PID > /dev/null; then
 echo -e "${GREEN}TrueAlphaSpiral Python API is running with PID $PYTHON_PID${NC}"
 return 0
 else
 echo -e "${RED}Failed to start TrueAlphaSpiral Python API${NC}"
 return 1
 fi
}

# Start the Express frontend
start_express_frontend() {
 echo -e "${CYAN}Starting TrueAlphaSpiral Express frontend on port 5000...${NC}"

 # Set the environment variable to point to the Python API
 export PYTHON_API_URL="http://localhost:8001"

 # Start the Express frontend
 npm run dev &
 EXPRESS_PID=$!

 # Wait for the server to initialize
 echo -e "${YELLOW}Waiting for Express frontend to initialize...${NC}"
 sleep 5

 # Check if the server started successfully
 if ps -p $EXPRESS_PID > /dev/null; then
 echo -e "${GREEN}TrueAlphaSpiral Express frontend is running with PID $EXPRESS_PID${NC}"
 return 0
 else
 echo -e "${RED}Failed to start TrueAlphaSpiral Express frontend${NC}"
 return 1
 fi
}

# Clean up on exit
cleanup() {
 echo -e "\n${YELLOW}Shutting down TrueAlphaSpiral system...${NC}"
 if [ -f python_api.pid ]; then
 PYTHON_PID=$(cat python_api.pid)
 kill $PYTHON_PID 2>/dev/null
 rm python_api.pid
 fi
 lsof -ti:8001 | xargs kill -9 2>/dev/null
 lsof -ti:5000 | xargs kill -9 2>/dev/null
 echo -e "${GREEN}System shutdown complete.${NC}"
 exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup SIGINT SIGTERM

# Main execution
kill_existing_processes

# Start Python API
if start_python_api; then
 echo -e "${GREEN}Python API started successfully${NC}"

 # Start Express frontend
 if start_express_frontend; then
 echo -e "${GREEN}Express frontend started successfully${NC}"
 echo -e "\n${CYAN}======================================================================${NC}"
 echo -e "${CYAN} TRUEALPHASPIRAL SYSTEM RUNNING${NC}"
 echo -e "${CYAN} Python API: http://localhost:8001${NC}"
 echo -e "${CYAN} Frontend: http://localhost:5000${NC}"
 echo -e "${CYAN}======================================================================${NC}"
 echo -e "\n${YELLOW}Press Ctrl+C to stop the system${NC}"

 # Keep the script running until Ctrl+C
 while true; do
 sleep 1
 done
 else
 echo -e "${RED}Failed to start Express frontend. Exiting.${NC}"
 cleanup
 fi
else
 echo -e "${RED}Failed to start Python API. Exiting.${NC}"
 cleanup
fi
