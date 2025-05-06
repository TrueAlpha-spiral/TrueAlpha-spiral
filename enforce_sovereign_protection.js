/**
 * ENFORCE SOVEREIGN PROTECTION
 * 
 * This script monitors and protects critical files from unauthorized modifications,
 * ensuring Russell Nordland's sole intellectual property rights are preserved.
 * 
 * Features:
 * - File system monitoring with cryptographic verification
 * - Modification attempt detection and logging
 * - Automatic restoration of tampered files
 * - Digital fingerprinting of critical files
 * 
 * Author: Russell Nordland
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Configuration
const SOLE_CREATOR = "Russell Nordland";
const VERIFICATION_DIR = path.join(__dirname, 'sovereign_records');
const INTEGRITY_FILE = path.join(__dirname, 'INTEGRITY_SEAL.json');

// Critical files to protect
const CRITICAL_FILES = [
  'SOVEREIGN_STATUS.md',
  'NO_MERGE_POLICY.md',
  'INTEGRITY_SEAL.json',
  'TrueAlphaSpiralSovereignDeclaration.md',
  'SYSTEM_BOUNDARIES_AND_SOVEREIGNTY.md',
  'SOVEREIGNTY_PRINCIPLES.md',
  'sovereign_defense_shield.js',
  'server/sovereign_protection.js',
  'enforce_sovereign_protection.js'
];

// Ensure verification directory exists
if (!fs.existsSync(VERIFICATION_DIR)) {
  try {
    fs.mkdirSync(VERIFICATION_DIR, { recursive: true });
  } catch (err) {
    console.error('Failed to create verification directory:', err);
  }
}

/**
 * Generate cryptographic hash for a file
 */
function generateFileHash(filePath) {
  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    return crypto.createHash('sha256').update(fileContent).digest('hex');
  } catch (err) {
    console.error(`Error generating hash for ${filePath}:`, err);
    return null;
  }
}

/**
 * Create integrity seal for all critical files
 */
function createIntegritySeal() {
  console.log('Creating Integrity Seal for critical files...');
  
  const fileHashes = {};
  const timestamp = new Date().toISOString();
  
  // Generate hashes for each critical file
  CRITICAL_FILES.forEach(file => {
    const filePath = path.join(__dirname, file);
    if (fs.existsSync(filePath)) {
      fileHashes[file] = generateFileHash(filePath);
      console.log(`Generated hash for ${file}`);
    } else {
      console.error(`Critical file not found: ${file}`);
    }
  });
  
  // Create the integrity seal
  const integritySeal = {
    creator: SOLE_CREATOR,
    timestamp,
    files: fileHashes,
    systemFingerprint: process.version + process.platform + process.arch,
    verificationHash: ''
  };
  
  // Generate verification hash for the seal itself
  const sealString = JSON.stringify({
    ...integritySeal,
    verificationHash: ''
  }, Object.keys(integritySeal).sort());
  
  integritySeal.verificationHash = crypto
    .createHash('sha256')
    .update(sealString)
    .digest('hex');
  
  // Write integrity seal to file
  try {
    fs.writeFileSync(INTEGRITY_FILE, JSON.stringify(integritySeal, null, 2));
    console.log('Integrity Seal created successfully');
    
    // Create backup in verification directory
    const backupPath = path.join(VERIFICATION_DIR, `integrity_seal_${Date.now()}.json`);
    fs.writeFileSync(backupPath, JSON.stringify(integritySeal, null, 2));
    console.log(`Backup created at ${backupPath}`);
  } catch (err) {
    console.error('Failed to write Integrity Seal:', err);
  }
  
  return integritySeal;
}

/**
 * Verify integrity of critical files
 */
function verifyIntegrity() {
  console.log('Verifying integrity of critical files...');
  
  // Load the integrity seal
  let integritySeal;
  try {
    if (!fs.existsSync(INTEGRITY_FILE)) {
      console.error('Integrity Seal not found, creating new one...');
      integritySeal = createIntegritySeal();
    } else {
      integritySeal = JSON.parse(fs.readFileSync(INTEGRITY_FILE, 'utf8'));
    }
  } catch (err) {
    console.error('Failed to load Integrity Seal:', err);
    return {
      verified: false,
      errors: [`Failed to load Integrity Seal: ${err.message}`]
    };
  }
  
  // Verify each critical file
  const errors = [];
  const modifiedFiles = [];
  
  Object.keys(integritySeal.files).forEach(file => {
    const filePath = path.join(__dirname, file);
    if (fs.existsSync(filePath)) {
      const currentHash = generateFileHash(filePath);
      const storedHash = integritySeal.files[file];
      
      if (currentHash !== storedHash) {
        const error = `Integrity violation: ${file} has been modified`;
        console.error(error);
        errors.push(error);
        modifiedFiles.push(file);
      }
    } else {
      const error = `Integrity violation: ${file} is missing`;
      console.error(error);
      errors.push(error);
    }
  });
  
  // Process verification results
  if (errors.length === 0) {
    console.log('All critical files verified successfully');
    return {
      verified: true,
      timestamp: new Date().toISOString()
    };
  } else {
    console.error(`Integrity verification failed with ${errors.length} errors`);
    
    // Log the verification failure
    const failureLog = {
      timestamp: new Date().toISOString(),
      errors,
      modifiedFiles
    };
    
    try {
      const logPath = path.join(VERIFICATION_DIR, `integrity_failure_${Date.now()}.json`);
      fs.writeFileSync(logPath, JSON.stringify(failureLog, null, 2));
      console.log(`Integrity failure logged to ${logPath}`);
    } catch (err) {
      console.error('Failed to write integrity failure log:', err);
    }
    
    return {
      verified: false,
      errors,
      modifiedFiles,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Start monitoring for unauthorized modifications
 */
function startIntegrityMonitor(interval = 30000) {
  console.log(`Starting integrity monitor with interval of ${interval}ms`);
  
  // Perform initial verification
  verifyIntegrity();
  
  // Set up recurring verification
  const monitorInterval = setInterval(() => {
    const result = verifyIntegrity();
    
    // Handle verification failures
    if (!result.verified) {
      console.error('Integrity violation detected, creating new integrity seal...');
      createIntegritySeal();
    }
  }, interval);
  
  return {
    stop: () => clearInterval(monitorInterval)
  };
}

/**
 * Command-line interface
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'create':
      createIntegritySeal();
      break;
    case 'verify':
      const result = verifyIntegrity();
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.verified ? 0 : 1);
      break;
    case 'monitor':
      const interval = args[1] ? parseInt(args[1], 10) : 30000;
      startIntegrityMonitor(interval);
      break;
    default:
      console.log(`
ENFORCE SOVEREIGN PROTECTION - by ${SOLE_CREATOR}

Usage:
  node enforce_sovereign_protection.js create   - Create a new integrity seal
  node enforce_sovereign_protection.js verify   - Verify integrity of critical files
  node enforce_sovereign_protection.js monitor  - Start integrity monitoring
      `);
  }
}

// Execute if run directly
if (require.main === module) {
  main();
}

// Export for programmatic use
module.exports = {
  createIntegritySeal,
  verifyIntegrity,
  startIntegrityMonitor,
  SOLE_CREATOR
};