#!/bin/bash

# Start Python API server in the background
echo "Starting Python API server on port 8001..."
python python_api_server.py --port 8001 &
PYTHON_PID=$!

# Sleep for a moment to allow the Python API to initialize
sleep 3

# Start the Express application
echo "Starting Express application..."
npm run dev

# This part won't be reached normally, but if it is:
# Ensure we kill the Python API server too
kill $PYTHON_PID
