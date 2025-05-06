/**
 * ANTI-PARENT PROTECTION SYSTEM
 * 
 * This script ensures there are no references to "parents" in the codebase,
 * as this could imply creators or contributions from anyone other than
 * Russell Nordland, the sole creator.
 * 
 * The system:
 * 1. Scans all files for explicit "parent" references
 * 2. Replaces or removes problematic parent terminology
 * 3. Blocks git operations that may introduce previous sovereign commit references
 * 4. Maintains a sovereign lineage without parent implications
 * 
 * Author: Russell Nordland
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

// Get current file and directory name for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Constants
const SOLE_CREATOR = "Russell Nordland";
const REPO_ROOT = __dirname;

// Files to scan
const EXCLUDE_DIRS = [
  'node_modules',
  '.git',
  'dist',
  'build'
];

// Potential parent references to detect/remove
const PARENT_REFERENCES = [
  'previous sovereign commit',
  'preceding sovereign branch',
  'original sovereign repository',
  'ancestral class',
  'container component',
  'container node',
  'Russell Nordland',
  'container element',
  'Russell Nordland',
  'superior module',
  'foundation codebase',
  'foundation system',
  'preceding record',
  'originating process',
  'sovereign implementation',
  'sovereign template',
  'sovereign documentation',
  'parentNode',
  'parentElement'
];

// Alternative terminology that avoids parent implications
const ALTERNATIVE_TERMINOLOGY = {
  'previous sovereign commit': 'previous sovereign commit',
  'preceding sovereign branch': 'preceding sovereign branch',
  'original sovereign repository': 'original sovereign repository',
  'ancestral class': 'ancestral class',
  'container component': 'container component',
  'container node': 'container node',
  'Russell Nordland': SOLE_CREATOR,
  'container element': 'container element',
  'Russell Nordland': SOLE_CREATOR,
  'superior module': 'superior module',
  'foundation codebase': 'foundation codebase',
  'foundation system': 'foundation system',
  'preceding record': 'preceding record',
  'originating process': 'originating process',
  'sovereign implementation': 'sovereign implementation',
  'sovereign template': 'sovereign template',
  'sovereign documentation': 'sovereign documentation',
  // JavaScript DOM properties aren't replaced as they're standard browser APIs
  // but we flag them for documentation
};

/**
 * Scan filesystem for files to check
 */
function getFilesToScan(dir = REPO_ROOT, fileList = []) {
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    if (file.startsWith('.') || EXCLUDE_DIRS.includes(file)) {
      continue;
    }
    
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      getFilesToScan(filePath, fileList);
    } else {
      // Only include text files
      if (/\.(js|jsx|ts|tsx|md|txt|json|html|css|scss|py|rb|php|java|c|cpp|h|hpp)$/i.test(file)) {
        fileList.push(filePath);
      }
    }
  }
  
  return fileList;
}

/**
 * Scan file for parent references
 */
function scanFileForParentReferences(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const findings = [];
    
    for (const reference of PARENT_REFERENCES) {
      // Case insensitive search but respect camelCase
      const regex = new RegExp(reference.replace(/([A-Z])/g, '\\$1'), 'gi');
      let match;
      
      while ((match = regex.exec(content)) !== null) {
        findings.push({
          reference,
          context: content.substring(Math.max(0, match.index - 30), match.index + reference.length + 30),
          lineNumber: content.substring(0, match.index).split('\n').length,
          position: match.index
        });
      }
    }
    
    return findings;
  } catch (err) {
    console.error(`Error scanning file ${filePath}:`, err);
    return [];
  }
}

/**
 * Replace parent references in a file
 */
function replaceParentReferencesInFile(filePath, findings) {
  if (findings.length === 0) {
    return { replaced: 0 };
  }
  
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let replacementCount = 0;
    
    // Sort findings by position in descending order to avoid position shifts
    findings.sort((a, b) => b.position - a.position);
    
    for (const finding of findings) {
      // Skip if it's a DOM API like parentNode
      if (['parentNode', 'parentElement'].includes(finding.reference)) {
        continue;
      }
      
      const replacement = ALTERNATIVE_TERMINOLOGY[finding.reference.toLowerCase()];
      if (replacement) {
        // Make replacement while preserving case
        const matchText = content.substring(finding.position, finding.position + finding.reference.length);
        let replacementText = replacement;
        
        // Preserve original capitalization
        if (matchText === matchText.toUpperCase()) {
          replacementText = replacement.toUpperCase();
        } else if (matchText[0] === matchText[0].toUpperCase()) {
          replacementText = replacement[0].toUpperCase() + replacement.substring(1);
        }
        
        content = content.substring(0, finding.position) + 
                 replacementText + 
                 content.substring(finding.position + finding.reference.length);
        
        replacementCount++;
      }
    }
    
    if (replacementCount > 0) {
      fs.writeFileSync(filePath, content, 'utf8');
    }
    
    return { replaced: replacementCount };
  } catch (err) {
    console.error(`Error replacing parent references in ${filePath}:`, err);
    return { replaced: 0, error: err.message };
  }
}

/**
 * Find and optionally replace parent references in all files
 */
function scanAndReplace(shouldReplace = false) {
  console.log(`Scanning repository for parent references (replace = ${shouldReplace})...`);
  
  const files = getFilesToScan();
  console.log(`Found ${files.length} files to scan`);
  
  let totalFindings = 0;
  let totalReplaced = 0;
  const allFindings = {};
  
  for (const file of files) {
    const relativeFile = path.relative(REPO_ROOT, file);
    const findings = scanFileForParentReferences(file);
    
    if (findings.length > 0) {
      allFindings[relativeFile] = findings;
      totalFindings += findings.length;
      
      console.log(`Found ${findings.length} parent reference(s) in ${relativeFile}`);
      
      if (shouldReplace) {
        const result = replaceParentReferencesInFile(file, findings);
        totalReplaced += result.replaced;
        
        if (result.replaced > 0) {
          console.log(`Replaced ${result.replaced} parent reference(s) in ${relativeFile}`);
        }
      }
    }
  }
  
  console.log(`\nScan complete: found ${totalFindings} parent references in ${Object.keys(allFindings).length} files`);
  
  if (shouldReplace) {
    console.log(`Replaced ${totalReplaced} parent references with sovereign terminology`);
  }
  
  return {
    scannedFiles: files.length,
    filesWithFindings: Object.keys(allFindings).length,
    totalFindings,
    totalReplaced: shouldReplace ? totalReplaced : 0,
    findings: allFindings
  };
}

/**
 * Block git commands that would introduce parents
 */
function blockGitParentOperations() {
  const gitDir = path.join(REPO_ROOT, '.git');
  
  if (!fs.existsSync(gitDir)) {
    console.log('No Git repository found, skipping Git parent blocks');
    return;
  }
  
  // Create a pre-commit hook
  const hookContent = `#!/bin/sh
# This git hook prevents the creation of commits that reference parents
# Russell Nordland is the sole creator and sovereign owner

echo "Sovereign integrity check: ensuring no parent references are created"

# Scan for parent references in the commit message
if grep -i "parent" .git/COMMIT_EDITMSG &>/dev/null; then
  echo "ERROR: Commit message contains reference to 'parent'"
  echo "Sovereign authority policy: Russell Nordland is the sole creator"
  exit 1
fi

# Execute Anti-Parent Protection System scan
node ${path.relative(REPO_ROOT, __filename)} scan --silent

# All checks passed
exit 0
`;

  const hookPath = path.join(gitDir, 'hooks', 'pre-commit');
  
  try {
    fs.writeFileSync(hookPath, hookContent, { mode: 0o755 });
    console.log('Git pre-commit hook installed to prevent parent references');
  } catch (err) {
    console.error('Failed to install Git pre-commit hook:', err);
  }
}

/**
 * Command-line interface
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'scan':
      const silent = args.includes('--silent');
      if (!silent) {
        console.log('Scanning for parent references - to replace them, use the "replace" command');
      }
      scanAndReplace(false);
      break;
    
    case 'replace':
      console.log('Replacing parent references with sovereign terminology');
      scanAndReplace(true);
      break;
    
    case 'block-git':
      console.log('Installing Git hooks to block parent references');
      blockGitParentOperations();
      break;
      
    case 'full-protection':
      console.log('Applying full anti-parent protection');
      scanAndReplace(true);
      blockGitParentOperations();
      break;
      
    default:
      console.log(`
ANTI-PARENT PROTECTION SYSTEM - by ${SOLE_CREATOR}

Usage:
  node anti_parent_protection.js scan        - Scan for parent references
  node anti_parent_protection.js replace     - Replace parent references
  node anti_parent_protection.js block-git   - Install Git hooks
  node anti_parent_protection.js full-protection - Apply all protections
      `);
  }
}

// Execute if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

// Export for programmatic use
export {
  scanAndReplace,
  blockGitParentOperations,
  SOLE_CREATOR
};