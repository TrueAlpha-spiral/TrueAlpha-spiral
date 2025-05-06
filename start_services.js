/**
 * Combined Service Starter for TrueAlphaSpiral Enterprise AI Auditing Solution
 * This is used by the package.json scripts to start both the Python API and Express server
 */

const concurrently = require('concurrently');

// Set up command and options for Python API server
const pythonApiCommand = {
 command: 'python python_api_server.py --port 8001',
 name: 'python-api',
 prefixColor: 'magenta',
 env: { PYTHONUNBUFFERED: '1' } // Ensure Python output is not buffered
};

// Set up command and options for Express server
const expressCommand = {
 command: 'tsx server/index.ts',
 name: 'express',
 prefixColor: 'blue',
 env: { PYTHON_API_URL: 'http://localhost:8001' } // Set environment variable for Python API URL
};

// Define the terminal header
console.log('\x1b[36m%s\x1b[0m', '======================================================================');
console.log('\x1b[36m%s\x1b[0m', ' TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION ');
console.log('\x1b[36m%s\x1b[0m', ' Starting combined services...');
console.log('\x1b[36m%s\x1b[0m', '======================================================================');

// Start both services with concurrently
concurrently(
 [pythonApiCommand, expressCommand],
 {
 prefix: 'name',
 killOthers: ['failure', 'success'], // Kill other processes if one dies
 restartTries: 3, // Try restarting dead processes up to 3 times
 restartDelay: 1000, // Wait 1 second before restarting
 }
).then(
 () => console.log('\x1b[32m%s\x1b[0m', 'All processes complete.'),
 (err) => console.error('\x1b[31m%s\x1b[0m', `Error: ${err}`)
);
