/**
 * TrueAlphaSpiral Autostart Integration Script
 * This script is automatically executed during server startup to ensure
 * permanent integration between Python API and Express frontend.
 *
 * Architect: Russell Nordland
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

// Print header
console.log(`${colors.cyan}${colors.bright}======================================================================${colors.reset}`);
console.log(`${colors.cyan}${colors.bright} TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright} Autostart Integration - PERMANENT SOLUTION ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright} Architect: Russell Nordland ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright} Date: ${new Date().toISOString()} ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright}======================================================================${colors.reset}`);

// Check if resilient integration system is available
if (fs.existsSync('./resilient_integration_system.py')) {
 console.log(`${colors.green}Found resilient integration system script${colors.reset}`);

 // Make sure it's executable
 try {
 fs.chmodSync('./resilient_integration_system.py', 0o755);
 console.log(`${colors.green}Made resilient_integration_system.py executable${colors.reset}`);
 } catch (err) {
 console.error(`${colors.red}Failed to make script executable: ${err.message}${colors.reset}`);
 }

 // Start the resilient integration system
 console.log(`${colors.yellow}Starting resilient integration system...${colors.reset}`);

 // Check if already running
 const pidFile = './resilient_system.pid';
 let isRunning = false;

 if (fs.existsSync(pidFile)) {
 try {
 const pid = parseInt(fs.readFileSync(pidFile, 'utf8').trim());
 try {
 // Check if process is running
 process.kill(pid, 0);
 isRunning = true;
 console.log(`${colors.yellow}Resilient integration system already running with PID ${pid}${colors.reset}`);
 } catch (e) {
 // Process not running
 console.log(`${colors.yellow}Found stale PID file for resilient integration system${colors.reset}`);
 fs.unlinkSync(pidFile);
 }
 } catch (err) {
 console.error(`${colors.red}Error checking PID file: ${err.message}${colors.reset}`);
 }
 }

 // Start if not already running
 if (!isRunning) {
 const process = spawn('python', ['resilient_integration_system.py'], {
 detached: true,
 stdio: 'inherit'
 });

 process.unref();

 console.log(`${colors.green}Started resilient integration system with PID ${process.pid}${colors.reset}`);
 console.log(`${colors.green}System now permanently protected and integrated${colors.reset}`);
 }
} else {
 console.log(`${colors.red}Resilient integration system script not found${colors.reset}`);
 console.log(`${colors.yellow}Falling back to direct process execution${colors.reset}`);

 // Fallback to directly starting the Python API server
 if (fs.existsSync('./python_api_server.py')) {
 console.log(`${colors.green}Found Python API server script${colors.reset}`);

 // Start Python API server directly
 const pythonProcess = spawn('python', ['python_api_server.py', '--port', '8001'], {
 detached: true,
 stdio: 'inherit'
 });

 pythonProcess.unref();

 console.log(`${colors.green}Started Python API server with PID ${pythonProcess.pid}${colors.reset}`);
 console.log(`${colors.yellow}This is a fallback solution and does not include full protection${colors.reset}`);
 } else {
 console.log(`${colors.red}Python API server script not found${colors.reset}`);
 console.log(`${colors.red}Unable to establish integration${colors.reset}`);
 }
}

console.log(`${colors.cyan}${colors.bright}======================================================================${colors.reset}`);
console.log(`${colors.cyan}${colors.bright} Integration startup complete ${colors.reset}`);
console.log(`${colors.cyan}${colors.bright}======================================================================${colors.reset}`);
