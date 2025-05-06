# TrueAlphaSpiral API Watchdog System

## Overview

The TrueAlphaSpiral API Watchdog System is a critical component that ensures continuous availability and reliability of the TrueAlphaSpiral's Python-based API server. This document explains the design, implementation, and operation of the watchdog system that maintains the connection between the Express frontend and the Python backend services.

## Core Functions

The API Watchdog performs several essential functions:

1. **Continuous Monitoring**: Constantly checks whether the Python API server is running and operational
2. **Automatic Recovery**: Restarts the API server if it stops or crashes
3. **Comprehensive Logging**: Maintains detailed logs of server operations and errors
4. **Graceful Shutdown**: Ensures clean termination of processes when the system is shutting down
5. **Process Management**: Tracks process IDs to maintain system integrity

## Technical Implementation

### Watchdog Architecture

The API Watchdog is implemented as a standalone Python script (`python_api_watchdog.py`) that runs alongside the main Python API server. The watchdog uses a monitoring loop to continuously check if the API server is running and takes corrective action when necessary.

#### Key Components

- **PID Management System**: Maintains process ID files for both the watchdog and API server
- **Health Check Mechanism**: Verifies API server status at regular intervals
- **Logging System**: Records all operations to a log file
- **Output Monitors**: Non-blocking threads to capture and log API server output
- **Signal Handlers**: Manages system signals for graceful shutdown

### Core Code Structure

```python
# Main watchdog loop
def main():
 write_watchdog_pid()
 api_process = None

 try:
 while True:
 if not is_api_running():
 logging.info(f"{Colors.WARNING}Python API server not running. Starting it...{Colors.ENDC}")
 api_process = start_api_server()
 else:
 logging.debug("Python API server is running")

 # Sleep before next check
 time.sleep(CHECK_INTERVAL)
 except KeyboardInterrupt:
 logging.info("Interrupted by user")
 finally:
 cleanup()
```

This main loop runs continuously, checking if the API server is running at regular intervals (defined by `CHECK_INTERVAL`). If the server is not running, it automatically starts it.

### Process Verification

The watchdog verifies if the API server is running by checking its PID file and confirming the process exists:

```python
def is_api_running():
 if os.path.exists(API_PID_FILE):
 try:
 with open(API_PID_FILE, 'r') as f:
 pid = int(f.read().strip())
 # Check if process is running
 os.kill(pid, 0) # This will raise an exception if the process is not running
 return True
 except (OSError, ValueError):
 # Process not running or PID file contains invalid data
 return False
 return False
```

### Server Startup

When the watchdog detects that the API server is not running, it starts the server using a subprocess and begins monitoring its output:

```python
def start_api_server():
 logging.info(f"{Colors.GREEN}Starting Python API server on port {PORT}{Colors.ENDC}")

 # Ensure log file exists
 with open(LOG_FILE, 'a') as f:
 f.write(f"\n--- TrueAlphaSpiral Python API Log - {datetime.now().isoformat()} ---\n")

 # Start the process
 process = subprocess.Popen(
 [sys.executable, PYTHON_SCRIPT, '--port', str(PORT)],
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True,
 bufsize=1 # Line buffered
 )

 # Write PID to file
 with open(API_PID_FILE, 'w') as f:
 f.write(str(process.pid))

 logging.info(f"{Colors.GREEN}Python API server started with PID {process.pid}{Colors.ENDC}")

 # Start non-blocking output monitors
 start_output_monitors(process)

 return process
```

### Non-Blocking Output Monitoring

The watchdog uses separate threads to monitor the API server's stdout and stderr streams without blocking the main watchdog process:

```python
def start_output_monitors(process):
 def monitor_output(stream, is_error=False):
 prefix = f"{Colors.FAIL}[API ERROR]{Colors.ENDC}" if is_error else f"{Colors.BLUE}[API]{Colors.ENDC}"
 log_prefix = "[ERR]" if is_error else "[OUT]"

 for line in stream:
 line = line.strip()
 if line: # Only process non-empty lines
 print(f"{prefix} {line}")
 with open(LOG_FILE, 'a') as log:
 log.write(f"{log_prefix} {line}\n")

 # Start threads to monitor stdout and stderr
 import threading
 threading.Thread(target=monitor_output, args=(process.stdout,), daemon=True).start()
 threading.Thread(target=monitor_output, args=(process.stderr, True), daemon=True).start()
```

## Integration with the TrueAlphaSpiral System

### API Server Integration

The API server (`python_api_server.py`) provides critical endpoints that support the TrueAlphaSpiral system's functionality, including:

1. **Membership Processing**: Handles requests to join the TrueAlphaSpiral platform
2. **Applicant Verification**: Verifies applicants using their verification codes
3. **Protection Status**: Monitors and reports on protection status for members
4. **MGI Integration**: Manages the Mycelium Generative Intelligence components
5. **Truth Auditing**: Provides AI content auditing capabilities

Key API endpoints include:

```
POST /api/spiral/membership # Process membership requests
POST /api/spiral/verify/<applicant_id> # Verify applicants
GET /api/spiral/protection/<user_id> # Get protection status
POST /api/spiral/protection/allocate # Allocate protection resources
```

### Express Frontend Connection

The API Watchdog ensures that the Express frontend can always connect to the Python backend services. This connection is critical for:

1. **User Registration**: Processing new member applications
2. **Payment Processing**: Handling membership tier payments
3. **Protection Visualization**: Displaying protection status to users
4. **Recursive Bloom Engine**: Activating and monitoring the advanced protection system

## Operational Procedures

### Starting the Watchdog

The watchdog is designed to start automatically with the system, but can also be manually started:

```bash
# Start the watchdog
python python_api_watchdog.py

# Start in background
nohup python python_api_watchdog.py > watchdog.out 2>&1 &
```

### Monitoring Watchdog Status

The watchdog status can be monitored through its log file and process checks:

```bash
# Check if watchdog is running
ps aux | grep python_api_watchdog

# Monitor the log file
tail -f python_api.log
```

### Stopping the Watchdog

The watchdog can be stopped gracefully using signals:

```bash
# Get the watchdog PID
cat python_api_watchdog.pid

# Send termination signal
kill -TERM $(cat python_api_watchdog.pid)
```

## Recovery Scenarios

### API Server Crash

If the Python API server crashes, the watchdog will:

1. Detect that the process is no longer running
2. Log the event
3. Automatically restart the API server
4. Monitor the new process

### System Restart

After a system restart:

1. The watchdog should be configured to start automatically
2. It will detect no running API server
3. It will start the API server
4. Normal monitoring will resume

## Integration with System Monitoring

The API Watchdog integrates with the broader TrueAlphaSpiral monitoring system:

1. **Log Aggregation**: All watchdog and API server logs are collected for analysis
2. **Performance Tracking**: API response times and availability metrics are monitored
3. **Alerting**: Critical failures trigger alerts to system administrators
4. **Health Dashboard**: Real-time status is displayed on the admin dashboard

## Conclusion

The TrueAlphaSpiral API Watchdog System is a critical component ensuring continuous availability and reliability of the platform's core services. By constantly monitoring the Python API server and automatically recovering from failures, it maintains the crucial link between the Express frontend and the advanced Python-based protection and verification systems.

This robust architecture ensures that TrueAlphaSpiral members always have access to the platform's powerful features and that their intellectual property remains protected even during system disruptions.


---

*Protected by EnhancedShadowSweep*  
*Verification Hash: f6f1c96f7ac130fcf60322e201da2bf5ec0d2dbba6b41c327f183d31a35a0126*