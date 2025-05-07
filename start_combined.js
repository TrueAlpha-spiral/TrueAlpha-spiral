#!/usr/bin/env node

/**
 * TrueAlphaSpiral Combined Server Launcher (CommonJS version)
 * This script permanently starts both the Python API server and the Express frontend
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// ANSI color codes for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

// Print the header
console.log(`${colors.cyan}${colors.bright}======================================================================${colors.reset}`);
console.log(`${colors.cyan}${colors.bright}  TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION  ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright}  Architect: Russell Nordland  ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright}  Date: ${new Date().toISOString()}  ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright}======================================================================${colors.reset}`);

// Kill any existing processes on the ports we need
console.log(`${colors.yellow}Checking for existing processes on ports 8001 and 5000...${colors.reset}`);
const killPortsCommand = process.platform === 'win32' 
  ? 'npx kill-port 8001 5000'
  : 'lsof -ti:8001,5000 | xargs kill -9 2>/dev/null || true';

spawn('sh', ['-c', killPortsCommand], { stdio: 'inherit' }).on('close', (code) => {
  console.log(`${colors.green}Ports cleared for new processes.${colors.reset}`);
  startPythonServer();
});

// Start the Python API server
function startPythonServer() {
  console.log(`${colors.cyan}Starting TrueAlphaSpiral Python API on port 8001...${colors.reset}`);
  
  // Ensure python_api.log exists and is writable
  try {
    fs.writeFileSync('python_api.log', `--- TrueAlphaSpiral Python API Log - ${new Date().toISOString()} ---\n`, { flag: 'a' });
  } catch (err) {
    console.error(`${colors.red}Error writing to log file: ${err.message}${colors.reset}`);
  }
  
  // Start Python server
  const pythonProcess = spawn('python', ['python_api_server.py', '--port', '8001'], {
    stdio: ['ignore', 'pipe', 'pipe'], // stdin, stdout, stderr
    detached: false
  });
  
  // Save PID for management
  fs.writeFileSync('python_api.pid', pythonProcess.pid.toString());
  console.log(`${colors.green}Python API started with PID ${pythonProcess.pid}${colors.reset}`);
  
  // Log Python server output
  pythonProcess.stdout.on('data', (data) => {
    const output = data.toString().trim();
    console.log(`${colors.magenta}[Python] ${colors.reset}${output}`);
    fs.appendFileSync('python_api.log', `[OUT] ${output}\n`);
  });
  
  pythonProcess.stderr.on('data', (data) => {
    const output = data.toString().trim();
    console.log(`${colors.red}[Python ERROR] ${colors.reset}${output}`);
    fs.appendFileSync('python_api.log', `[ERR] ${output}\n`);
  });
  
  // Handle Python server exit
  pythonProcess.on('close', (code) => {
    console.log(`${colors.red}Python API process exited with code ${code}${colors.reset}`);
    try { fs.unlinkSync('python_api.pid'); } catch(e) {}
    if (expressProcess) {
      expressProcess.kill();
    }
    process.exit(1);
  });
  
  // Wait for Python server to start up
  console.log(`${colors.yellow}Waiting for Python API to initialize...${colors.reset}`);
  setTimeout(() => startExpressServer(pythonProcess), 3000);
}

// Global reference to Express process
let expressProcess;

// Start the Express server
function startExpressServer(pythonProcess) {
  console.log(`${colors.cyan}Starting Express frontend on port 5000...${colors.reset}`);
  
  // Set environment variable for Python API URL
  const env = Object.assign({}, process.env, { PYTHON_API_URL: 'http://localhost:8001' });
  
  // Start Express server
  expressProcess = spawn('npm', ['run', 'dev'], {
    stdio: 'inherit',
    env
  });
  
  // Handle Express server exit
  expressProcess.on('close', (code) => {
    console.log(`${colors.red}Express process exited with code ${code}${colors.reset}`);
    // Also kill Python server when Express exits
    pythonProcess.kill();
    process.exit();
  });
}

// Handle Ctrl+C and other termination signals
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);

function cleanup() {
  console.log(`\n${colors.yellow}Shutting down TrueAlphaSpiral system...${colors.reset}`);
  
  // Kill Express process if it exists
  if (expressProcess) {
    expressProcess.kill();
  }
  
  // Read and kill Python process by PID if PID file exists
  try {
    if (fs.existsSync('python_api.pid')) {
      const pid = parseInt(fs.readFileSync('python_api.pid', 'utf8'));
      process.kill(pid);
      console.log(`${colors.green}Killed Python API process ${pid}${colors.reset}`);
      fs.unlinkSync('python_api.pid');
    }
  } catch (e) {
    console.error(`${colors.red}Error killing Python process: ${e.message}${colors.reset}`);
  }
  
  // Final cleanup
  console.log(`${colors.green}System shutdown complete.${colors.reset}`);
  process.exit(0);
}
