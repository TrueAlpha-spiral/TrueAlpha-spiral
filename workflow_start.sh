#!/bin/bash
# Workflow Start Script

# Log start time
echo "========================================================"
echo "Starting TrueAlphaSpiral servers - $(date)"
echo "========================================================"

# Kill any existing Python API servers
echo "Checking for existing Python API server processes..."
if [ -f python_api.pid ]; then
 pid=$(cat python_api.pid)
 if ps -p $pid > /dev/null; then
 echo "Stopping existing Python API server (PID: $pid)..."
 kill $pid
 sleep 2
 else
 echo "No running Python API server found with PID: $pid"
 fi
 rm python_api.pid
fi

# Start the Python API server in the background
echo "Starting Python API server..."
python python_api_server.py --port 8001 > python_api.log 2>&1 &
API_PID=$!
echo $API_PID > python_api.pid
echo "Python API server started with PID: $API_PID"

# Wait a moment for the Python server to initialize
echo "Waiting for Python API server to initialize..."
sleep 3

# Check if Python API server is still running
if ps -p $API_PID > /dev/null; then
 echo "Python API server running successfully on port 8001"
else
 echo "WARNING: Python API server may have failed to start. Check python_api.log for details."
 cat python_api.log
fi

# Start the Express server (this will remain in the foreground)
echo "Starting Express server..."
exec npm run dev