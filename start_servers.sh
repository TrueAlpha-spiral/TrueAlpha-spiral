#!/bin/bash
# Start the Python API server
echo "Starting Python API server on port 8001..."
python python_api_server.py --port 8001 &
PYTHON_PID=$!

# Wait a moment for the Python server to initialize
sleep 3

# Start the Express server
echo "Starting Express server..."
npm run dev

# Kill the Python server when the script exits
trap "kill $PYTHON_PID" EXIT