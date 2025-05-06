#!/bin/bash

# Kill any existing Python API server process
pkill -f "python python_api_server.py" || true
pkill -f "python3 python_api_server.py" || true

# Make sure we're not trying to start while another is running
sleep 1

# Start the Python API server in the background with improved robustness
nohup python python_api_server.py --port 8001 > python_api.log 2>&1 &
PYTHON_PID=$!

# Save the PID to a file
echo $PYTHON_PID > python_api.pid

echo "Python API server started on port 8001 with PID $PYTHON_PID"

# Monitor the process for 5 seconds to make sure it doesn't terminate immediately
sleep 5
if ps -p $PYTHON_PID > /dev/null; then
 echo "Python API server is running successfully after 5 seconds."
 echo "Logs available in python_api.log"

 # Set up a watchdog process that will restart the server if it fails
 (
 while true; do
 # Check if the process is still running
 if ! ps -p $PYTHON_PID > /dev/null; then
 echo "$(date): Python API server crashed, restarting..." >> python_api_watchdog.log
 # Restart the server
 nohup python python_api_server.py --port 8001 > python_api.log 2>&1 &
 PYTHON_PID=$!
 echo $PYTHON_PID > python_api.pid
 echo "$(date): Restarted with PID $PYTHON_PID" >> python_api_watchdog.log
 fi
 # Check every 30 seconds
 sleep 30
 done
 ) &

 # Save the watchdog PID
 echo $! > python_api_watchdog.pid
 echo "Watchdog process started with PID $(cat python_api_watchdog.pid)"
else
 echo "ERROR: Python API server failed to start or terminated immediately."
 echo "Check python_api.log for errors."
 cat python_api.log
fi
