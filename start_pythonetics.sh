#!/bin/bash

# Start Pythonetics Python API Server
# This script starts the Pythonetics server and creates an interface
# between the Python implementation and the Node.js Express server

echo "Starting Pythonetics Server..."

# Kill any existing Pythonetics process
if [ -f pythonetics.pid ]; then
  pid=$(cat pythonetics.pid)
  if ps -p $pid > /dev/null; then
    echo "Killing existing Pythonetics process ($pid)"
    kill $pid
  fi
  rm pythonetics.pid
fi

# Start the Pythonetics server in the background
python pythonetics_server_integration.py > pythonetics.log 2>&1 &

# Save the process ID
echo $! > pythonetics.pid

echo "Pythonetics Server started with PID $(cat pythonetics.pid)"

# Start a watchdog process to monitor the server
# This will restart the server if it crashes
(
  while true; do
    if [ ! -f pythonetics.pid ]; then
      echo "Pythonetics PID file not found, exiting watchdog"
      exit 1
    fi
    
    pid=$(cat pythonetics.pid)
    if ! ps -p $pid > /dev/null; then
      echo "Pythonetics process ($pid) died, restarting..."
      python pythonetics_server_integration.py > pythonetics.log 2>&1 &
      echo $! > pythonetics.pid
      echo "Restarted Pythonetics with PID $(cat pythonetics.pid)"
    fi
    sleep 5
  done
) > pythonetics_watchdog.log 2>&1 &

# Save watchdog PID
echo $! > pythonetics_watchdog.pid

echo "Pythonetics watchdog started with PID $(cat pythonetics_watchdog.pid)"
echo "Pythonetics server is running at http://localhost:8001/api/pythonetics/health"