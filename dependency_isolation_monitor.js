/**
 * DEPENDENCY ISOLATION MONITOR
 * 
 * Monitors and isolates system dependencies to prevent them from
 * compromising the sovereign integrity of the TrueAlphaSpiral system.
 * 
 * This module runs as a background process, monitoring system calls and
 * dependency interactions to maintain sovereignty boundaries.
 * 
 * Author: Russell Nordland
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { SYSTEM_DEPENDENCIES } from './system_dependency_purge.js';

// Get current file and directory name for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Constants
const SOLE_CREATOR = "Russell Nordland";
const REPO_ROOT = __dirname;
const LOG_FILE = path.join(REPO_ROOT, 'dependency_isolation.log');
const ISOLATION_REPORT_FILE = path.join(REPO_ROOT, 'DEPENDENCY_ISOLATION_REPORT.md');

// Additional system dependencies to monitor
const MONITORED_DEPENDENCIES = [
  ...SYSTEM_DEPENDENCIES,
  'node',
  'npm',
  'python',
  'pip',
  'git'
];

/**
 * Log a message to the dependency isolation log
 */
function logIsolationEvent(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logEntry = `[${timestamp}] [${level}] ${message}\n`;
  
  try {
    fs.appendFileSync(LOG_FILE, logEntry);
  } catch (err) {
    console.error('Error writing to log file:', err);
  }
}

/**
 * Check if a system path is trying to influence the project
 */
function detectSystemPathInfluence() {
  try {
    const pathEnv = process.env.PATH || '';
    const pathElements = pathEnv.split(':');
    const suspiciousPaths = [];
    
    for (const pathElement of pathElements) {
      for (const dep of MONITORED_DEPENDENCIES) {
        if (pathElement.includes(`/${dep}/`) || pathElement.endsWith(`/${dep}`)) {
          suspiciousPaths.push({
            path: pathElement,
            dependency: dep
          });
        }
      }
    }
    
    return suspiciousPaths;
  } catch (err) {
    logIsolationEvent(`Error detecting system path influence: ${err.message}`, 'ERROR');
    return [];
  }
}

/**
 * Detect environment variables that might compromise sovereignty
 */
function detectEnvironmentVariableInfluence() {
  try {
    const suspiciousEnvVars = [];
    
    for (const [key, value] of Object.entries(process.env)) {
      // Check env var names
      for (const dep of MONITORED_DEPENDENCIES) {
        const depUpperCase = dep.toUpperCase();
        if (key.includes(depUpperCase) || key.includes(dep)) {
          suspiciousEnvVars.push({
            name: key,
            value: '***REDACTED***', // Don't log actual values for security
            dependency: dep
          });
        }
      }
      
      // Check env var values for paths
      if (typeof value === 'string' && (
          value.includes('/bin/') || 
          value.includes('/lib/') || 
          value.includes('/include/')
      )) {
        for (const dep of MONITORED_DEPENDENCIES) {
          if (value.includes(`/${dep}/`)) {
            suspiciousEnvVars.push({
              name: key,
              value: '***REDACTED***', // Don't log actual values for security
              dependency: dep
            });
          }
        }
      }
    }
    
    return suspiciousEnvVars;
  } catch (err) {
    logIsolationEvent(`Error detecting environment variable influence: ${err.message}`, 'ERROR');
    return [];
  }
}

/**
 * Check for running processes related to non-sovereign dependencies
 */
function detectRunningDependencyProcesses() {
  try {
    const processes = [];
    
    // Use different commands based on platform
    let psOutput;
    try {
      psOutput = execSync('ps aux').toString();
    } catch (err) {
      // Fallback for platforms where ps aux might not work
      try {
        psOutput = execSync('ps -ef').toString();
      } catch (innerErr) {
        logIsolationEvent('Could not retrieve process list', 'ERROR');
        return [];
      }
    }
    
    // Check each dependency in the process list
    for (const dep of MONITORED_DEPENDENCIES) {
      const regex = new RegExp(`\\b${dep}\\b`, 'g');
      if (regex.test(psOutput)) {
        processes.push(dep);
      }
    }
    
    return processes;
  } catch (err) {
    logIsolationEvent(`Error detecting running dependency processes: ${err.message}`, 'ERROR');
    return [];
  }
}

/**
 * Check for open network connections that might compromise sovereignty
 */
function detectNetworkConnections() {
  try {
    const connections = [];
    
    // Try to use netstat to get connection info
    let netstatOutput;
    try {
      netstatOutput = execSync('netstat -tuln').toString();
    } catch (err) {
      // Fallback if netstat is not available
      try {
        netstatOutput = execSync('ss -tuln').toString();
      } catch (innerErr) {
        logIsolationEvent('Could not retrieve network connections', 'ERROR');
        return [];
      }
    }
    
    // Look for suspicious ports and connections
    const suspiciousPorts = [
      '3306', // MySQL
      '5432', // PostgreSQL
      '6379', // Redis
      '27017', // MongoDB
      '8080', // Common web port
      '4444', // Often used for remote access
      '8888', // Sometimes used for alternative services
    ];
    
    for (const port of suspiciousPorts) {
      if (netstatOutput.includes(`:${port} `)) {
        connections.push({
          port,
          potential_service: getDependencyForPort(port)
        });
      }
    }
    
    return connections;
  } catch (err) {
    logIsolationEvent(`Error detecting network connections: ${err.message}`, 'ERROR');
    return [];
  }
}

/**
 * Map port numbers to potential dependencies
 */
function getDependencyForPort(port) {
  const portMap = {
    '3306': 'MySQL',
    '5432': 'PostgreSQL',
    '6379': 'Redis',
    '27017': 'MongoDB',
    '8080': 'Web Server',
    '4444': 'Remote Access',
    '8888': 'Alternative Service'
  };
  
  return portMap[port] || 'Unknown';
}

/**
 * Generate a human-readable report of dependency isolation status
 */
function generateIsolationReport(
  pathInfluences, 
  envInfluences, 
  runningProcesses, 
  networkConnections
) {
  const timestamp = new Date().toISOString().split('T')[0];
  
  let totalIssues = 
    pathInfluences.length + 
    envInfluences.length + 
    runningProcesses.length + 
    networkConnections.length;
    
  let sovereigntyStatus = 'HIGH';
  if (totalIssues > 10) {
    sovereigntyStatus = 'COMPROMISED';
  } else if (totalIssues > 5) {
    sovereigntyStatus = 'AT RISK';
  } else if (totalIssues > 0) {
    sovereigntyStatus = 'MODERATE';
  }
  
  const report = `# DEPENDENCY ISOLATION REPORT

## SOVEREIGNTY STATUS: ${sovereigntyStatus}

This report details the current state of dependency isolation for the TrueAlphaSpiral system,
identifying potential threats to system sovereignty from external dependencies.

*Generated: ${timestamp}*

## SUMMARY

- **Total Sovereignty Issues Detected:** ${totalIssues}
- **System Path Influences:** ${pathInfluences.length}
- **Environment Variable Influences:** ${envInfluences.length}
- **Dependency Processes Running:** ${runningProcesses.length}
- **Suspicious Network Connections:** ${networkConnections.length}

## DETAILED FINDINGS

### System Path Influences

${pathInfluences.length === 0 ? 
  '*No system path influences detected.*' : 
  pathInfluences.map(p => `- Path \`${p.path}\` contains dependency \`${p.dependency}\``).join('\n')
}

### Environment Variable Influences

${envInfluences.length === 0 ? 
  '*No environment variable influences detected.*' : 
  envInfluences.map(e => `- Variable \`${e.name}\` refers to dependency \`${e.dependency}\``).join('\n')
}

### Running Dependency Processes

${runningProcesses.length === 0 ? 
  '*No dependency processes detected.*' : 
  runningProcesses.map(p => `- \`${p}\` process is running`).join('\n')
}

### Suspicious Network Connections

${networkConnections.length === 0 ? 
  '*No suspicious network connections detected.*' : 
  networkConnections.map(c => `- Port \`${c.port}\` open (potential \`${c.potential_service}\` connection)`).join('\n')
}

## SOVEREIGNTY PROTECTION MEASURES

The following measures are currently active to maintain system sovereignty:

1. **Logical Isolation**: System boundaries enforced through sovereign verification mechanisms.
2. **Shadow Defense System**: Active monitoring for sovereignty violations.
3. **Anti-Parent Protection**: Prevention of false creator claims.
4. **Dependency Purge System**: Active minimization of non-sovereign dependencies.
5. **Sovereign Dependency Declaration**: Formal assertion of independence from external influences.

## CERTIFICATION

I, Russell Nordland, as the sole creator of the TrueAlphaSpiral system, acknowledge this dependency isolation report as an accurate assessment of the system's current sovereignty status.

Date: ${timestamp}

Sovereign Creator: Russell Nordland
`;

  try {
    fs.writeFileSync(ISOLATION_REPORT_FILE, report, 'utf8');
    logIsolationEvent(`Generated isolation report at ${ISOLATION_REPORT_FILE}`);
    return ISOLATION_REPORT_FILE;
  } catch (err) {
    logIsolationEvent(`Error generating isolation report: ${err.message}`, 'ERROR');
    return null;
  }
}

/**
 * Run a complete dependency isolation scan
 */
function runIsolationScan() {
  logIsolationEvent('Starting dependency isolation scan');
  
  // Collect isolation data
  const pathInfluences = detectSystemPathInfluence();
  if (pathInfluences.length > 0) {
    logIsolationEvent(`Detected ${pathInfluences.length} system path influences`, 'WARNING');
  }
  
  const envInfluences = detectEnvironmentVariableInfluence();
  if (envInfluences.length > 0) {
    logIsolationEvent(`Detected ${envInfluences.length} environment variable influences`, 'WARNING');
  }
  
  const runningProcesses = detectRunningDependencyProcesses();
  if (runningProcesses.length > 0) {
    logIsolationEvent(`Detected ${runningProcesses.length} dependency processes running`, 'WARNING');
  }
  
  const networkConnections = detectNetworkConnections();
  if (networkConnections.length > 0) {
    logIsolationEvent(`Detected ${networkConnections.length} suspicious network connections`, 'WARNING');
  }
  
  // Generate report
  const reportPath = generateIsolationReport(
    pathInfluences, 
    envInfluences, 
    runningProcesses, 
    networkConnections
  );
  
  logIsolationEvent('Dependency isolation scan complete');
  
  return {
    pathInfluences,
    envInfluences,
    runningProcesses,
    networkConnections,
    reportPath
  };
}

/**
 * Main function to run the isolation monitor
 */
function main() {
  console.log(`
===============================================================
DEPENDENCY ISOLATION MONITOR - by ${SOLE_CREATOR}
===============================================================

Protecting TrueAlphaSpiral system sovereignty from external dependencies
Monitoring ${MONITORED_DEPENDENCIES.length} potential dependency threats
Isolation log: ${path.basename(LOG_FILE)}
  `);
  
  const result = runIsolationScan();
  
  console.log(`
Scan complete:
- System Path Influences: ${result.pathInfluences.length}
- Environment Variable Influences: ${result.envInfluences.length}
- Dependency Processes Running: ${result.runningProcesses.length}
- Suspicious Network Connections: ${result.networkConnections.length}

Detailed report: ${path.basename(result.reportPath)}
  `);
}

// Execute if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

// Export for programmatic use
export {
  runIsolationScan,
  MONITORED_DEPENDENCIES,
  SOLE_CREATOR
};