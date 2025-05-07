#!/usr/bin/env node

/**
 * TrueAlphaSpiral Combined Server Launcher
 * This script starts both the Python API server and the Express frontend
 */

const { spawn } = require('child_process');
const process = require('process');

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

// Kill any existing processes on ports we need
const killExistingProcesses = () => {
  console.log(`${colors.yellow}Checking for existing processes on ports 8001 and 5000...${colors.reset}`);
  try {
    // Note: This won't work on Windows, but Replit is Linux-based
    spawn('bash', ['-c', 'lsof -ti:8001 | xargs kill -9 2>/dev/null']);
    spawn('bash', ['-c', 'lsof -ti:5000 | xargs kill -9 2>/dev/null']);
    console.log(`${colors.green}Ports cleared for new processes.${colors.reset}`);
  } catch (error) {
    console.log(`${colors.yellow}Error clearing ports: ${error.message}${colors.reset}`);
  }
};

// Start the Python API server
const startPythonApi = () => {
  console.log(`${colors.cyan}Starting TrueAlphaSpiral Python API on port 8001...${colors.reset}`);
  
  // Use spawn to keep the process running and capture output
  const pythonProcess = spawn('python', ['python_api_server.py', '--port', '8001'], {
    stdio: 'pipe',
    detached: false
  });
  
  // Set up output handling with prefixes to distinguish sources
  pythonProcess.stdout.on('data', (data) => {
    const lines = data.toString().trim().split('\n');
    lines.forEach(line => {
      if (line.trim()) {
        console.log(`${colors.magenta}[Python API] ${colors.reset}${line}`);
      }
    });
  });
  
  pythonProcess.stderr.on('data', (data) => {
    const lines = data.toString().trim().split('\n');
    lines.forEach(line => {
      if (line.trim()) {
        console.log(`${colors.red}[Python API ERROR] ${colors.reset}${line}`);
      }
    });
  });
  
  pythonProcess.on('error', (error) => {
    console.log(`${colors.red}Failed to start Python API: ${error.message}${colors.reset}`);
  });
  
  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.log(`${colors.red}Python API process exited with code ${code}${colors.reset}`);
    }
  });
  
  return pythonProcess;
};

// Start the Express frontend
const startExpressFrontend = () => {
  console.log(`${colors.cyan}Starting TrueAlphaSpiral Express frontend...${colors.reset}`);
  
  // Set environment variable to point to the Python API
  const env = { ...process.env, PYTHON_API_URL: 'http://localhost:8001' };
  
  // Use npm run dev to start the Express server
  const expressProcess = spawn('npm', ['run', 'dev'], {
    stdio: 'pipe',
    env,
    detached: false
  });
  
  // Set up output handling with prefixes
  expressProcess.stdout.on('data', (data) => {
    const lines = data.toString().trim().split('\n');
    lines.forEach(line => {
      if (line.trim()) {
        console.log(`${colors.blue}[Express] ${colors.reset}${line}`);
      }
    });
  });
  
  expressProcess.stderr.on('data', (data) => {
    const lines = data.toString().trim().split('\n');
    lines.forEach(line => {
      if (line.trim()) {
        console.log(`${colors.red}[Express ERROR] ${colors.reset}${line}`);
      }
    });
  });
  
  expressProcess.on('error', (error) => {
    console.log(`${colors.red}Failed to start Express: ${error.message}${colors.reset}`);
  });
  
  expressProcess.on('close', (code) => {
    if (code !== 0) {
      console.log(`${colors.red}Express process exited with code ${code}${colors.reset}`);
    }
  });
  
  return expressProcess;
};

// Main function to start everything
const main = async () => {
  console.log(`${colors.bright}${colors.cyan}======================================================================${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}  TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION  ${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}  Architect: Russell Nordland  ${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}  Date: ${new Date().toISOString()}  ${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}======================================================================${colors.reset}`);
  
  // Kill any existing processes
  killExistingProcesses();
  
  // Start Python API server
  const pythonProcess = startPythonApi();
  
  // Wait for Python API to initialize before starting Express
  console.log(`${colors.yellow}Waiting for Python API to initialize...${colors.reset}`);
  await new Promise(resolve => setTimeout(resolve, 3000)); // Wait 3 seconds
  
  // Start Express frontend
  const expressProcess = startExpressFrontend();
  
  // Set up cleanup on exit
  const cleanup = () => {
    console.log(`\n${colors.yellow}Shutting down TrueAlphaSpiral system...${colors.reset}`);
    if (pythonProcess) {
      pythonProcess.kill();
    }
    if (expressProcess) {
      expressProcess.kill();
    }
    
    // Force kill any processes still on our ports
    try {
      spawn('bash', ['-c', 'lsof -ti:8001 | xargs kill -9 2>/dev/null']);
      spawn('bash', ['-c', 'lsof -ti:5000 | xargs kill -9 2>/dev/null']);
    } catch {}
    
    console.log(`${colors.green}System shutdown complete.${colors.reset}`);
    process.exit(0);
  };
  
  // Set up signal handlers
  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
};

// Run the main function
main().catch(error => {
  console.error(`${colors.red}Error in main: ${error.stack || error.message || error}${colors.reset}`);
  process.exit(1);
});
