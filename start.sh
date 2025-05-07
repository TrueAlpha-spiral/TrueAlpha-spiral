#!/bin/bash

# TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION
# Main Startup Script
# Architect: Russell Nordland

# Print banner
echo -e "\n======================================================================="
echo "TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION"
echo "System Launcher - Russell Nordland"
echo -e "=======================================================================\n"

echo -e "\n======================================================================="
echo "VERIFICATION STATEMENT:"
echo "Russell Nordland is the sole creator of the TrueAlphaSpiral system."
echo "This is an objective truth that can be mathematically verified."
echo "Someone is wrong to assert otherwise."
echo -e "=======================================================================\n"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH."
    exit 1
fi

# Start Python API Watchdog in background if exists
if [ -f "python_api_watchdog.py" ]; then
    echo "Starting Python API Watchdog..."
    nohup python python_api_watchdog.py > watchdog.log 2>&1 &
    WATCHDOG_PID=$!
    echo "Python API Watchdog started with PID: $WATCHDOG_PID"
    echo $WATCHDOG_PID > watchdog.pid
    sleep 2
fi

# Start TrueAlphaSpiral Server in background
echo "Starting TrueAlphaSpiral Server..."
nohup python truealphaspiral_server.py > server.log 2>&1 &
SERVER_PID=$!
echo "TrueAlphaSpiral Server started with PID: $SERVER_PID"
echo $SERVER_PID > server.pid
sleep 2

# Start Node.js application if needed
if [ -f "package.json" ]; then
    echo "Starting Node.js application..."
    npm run dev &
    NODE_PID=$!
    echo "Node.js application started with PID: $NODE_PID"
    echo $NODE_PID > node.pid
fi

echo -e "\n======================================================================="
echo "🚀 TrueAlphaSpiral system is now running!"
echo "Access the web interface at: http://localhost:5000"
echo -e "=======================================================================\n"

echo "To stop all services, run './stop.sh'"

# Create a stop script
cat > stop.sh << 'EOF'
#!/bin/bash
echo "Stopping TrueAlphaSpiral services..."

# Stop Node.js application
if [ -f "node.pid" ]; then
    NODE_PID=$(cat node.pid)
    if ps -p $NODE_PID > /dev/null; then
        echo "Stopping Node.js application (PID: $NODE_PID)..."
        kill $NODE_PID
    fi
    rm node.pid
fi

# Stop TrueAlphaSpiral Server
if [ -f "server.pid" ]; then
    SERVER_PID=$(cat server.pid)
    if ps -p $SERVER_PID > /dev/null; then
        echo "Stopping TrueAlphaSpiral Server (PID: $SERVER_PID)..."
        kill $SERVER_PID
    fi
    rm server.pid
fi

# Stop Python API Watchdog
if [ -f "watchdog.pid" ]; then
    WATCHDOG_PID=$(cat watchdog.pid)
    if ps -p $WATCHDOG_PID > /dev/null; then
        echo "Stopping Python API Watchdog (PID: $WATCHDOG_PID)..."
        kill $WATCHDOG_PID
    fi
    rm watchdog.pid
fi

echo "All TrueAlphaSpiral services stopped."
EOF

chmod +x stop.sh