/**
 * DEPENDENCY PURGE SYSTEM
 * 
 * Removes external dependencies that could compromise the sovereign integrity
 * of Russell Nordland's TrueAlphaSpiral system. This ensures complete
 * independence from outside influences and control.
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

// Critical files to check
const DEPENDENCY_FILES = [
  'package.json',
  'package-lock.json',
  'requirements.txt',
  'Pipfile',
  'Pipfile.lock',
  'Cargo.toml',
  'Cargo.lock',
  'go.mod',
  'go.sum',
  'Gemfile',
  'Gemfile.lock',
  'composer.json',
  'composer.lock',
  'poetry.lock',
  'pyproject.toml',
  'build.gradle',
  'build.gradle.kts',
  'pom.xml'
];

// Essential packages that can't be removed
const ESSENTIAL_PACKAGES = [
  // Node.js essentials
  'express',
  'typescript',
  'vite',
  'react',
  'react-dom',
  '@types/react',
  '@types/react-dom',
  'tailwindcss',
  'cors',
  'wouter',
  'drizzle-orm',
  '@tanstack/react-query',
  'zod',
  // Python essentials 
  'flask',
  'requests',
  'numpy',
  'cryptography',
  // System packages
  'node',
  'python'
];

/**
 * Find all dependency files in the repository
 */
function findDependencyFiles() {
  const result = [];
  
  for (const file of DEPENDENCY_FILES) {
    const filePath = path.join(REPO_ROOT, file);
    if (fs.existsSync(filePath)) {
      result.push(filePath);
    }
  }
  
  return result;
}

/**
 * Parse dependencies from package.json
 */
function parseNodeDependencies(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const packageJson = JSON.parse(content);
    
    const dependencies = packageJson.dependencies || {};
    const devDependencies = packageJson.devDependencies || {};
    
    return {
      dependencies: Object.keys(dependencies),
      devDependencies: Object.keys(devDependencies),
      allDependencies: [...Object.keys(dependencies), ...Object.keys(devDependencies)]
    };
  } catch (err) {
    console.error(`Error parsing ${filePath}:`, err);
    return { dependencies: [], devDependencies: [], allDependencies: [] };
  }
}

/**
 * Parse dependencies from requirements.txt
 */
function parsePythonDependencies(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    
    const dependencies = lines
      .map(line => line.trim())
      .filter(line => line && !line.startsWith('#'))
      .map(line => {
        // Extract package name from requirement line (handle various formats)
        const match = line.match(/^([a-zA-Z0-9_.-]+)/);
        return match ? match[1].toLowerCase() : null;
      })
      .filter(Boolean);
    
    return { dependencies, allDependencies: dependencies };
  } catch (err) {
    console.error(`Error parsing ${filePath}:`, err);
    return { dependencies: [], allDependencies: [] };
  }
}

/**
 * Parse dependencies from a manifest file
 */
function parseDependencies(filePath) {
  const ext = path.extname(filePath);
  const filename = path.basename(filePath);
  
  if (filename === 'package.json') {
    return parseNodeDependencies(filePath);
  } else if (filename === 'requirements.txt') {
    return parsePythonDependencies(filePath);
  } else {
    console.log(`No parser available for ${filename}, skipping`);
    return { dependencies: [], allDependencies: [] };
  }
}

/**
 * Classify dependencies as essential or non-essential
 */
function classifyDependencies(dependencies) {
  const essential = [];
  const nonEssential = [];
  
  for (const dep of dependencies) {
    const isEssential = ESSENTIAL_PACKAGES.some(essentialPkg => {
      // Handle scope packages
      if (dep.startsWith('@')) {
        return dep.includes(essentialPkg);
      } else {
        return dep === essentialPkg;
      }
    });
    
    if (isEssential) {
      essential.push(dep);
    } else {
      nonEssential.push(dep);
    }
  }
  
  return { essential, nonEssential };
}

/**
 * Remove non-essential dependencies from package.json
 */
function removeNodeDependencies(filePath, nonEssentialDeps) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const packageJson = JSON.parse(content);
    
    let modifiedDeps = false;
    let modifiedDevDeps = false;
    
    // Process dependencies
    if (packageJson.dependencies) {
      for (const dep of nonEssentialDeps) {
        if (packageJson.dependencies[dep]) {
          delete packageJson.dependencies[dep];
          modifiedDeps = true;
          console.log(`Removed non-essential dependency: ${dep}`);
        }
      }
    }
    
    // Process devDependencies
    if (packageJson.devDependencies) {
      for (const dep of nonEssentialDeps) {
        if (packageJson.devDependencies[dep]) {
          delete packageJson.devDependencies[dep];
          modifiedDevDeps = true;
          console.log(`Removed non-essential dev dependency: ${dep}`);
        }
      }
    }
    
    if (modifiedDeps || modifiedDevDeps) {
      fs.writeFileSync(filePath, JSON.stringify(packageJson, null, 2), 'utf8');
      console.log(`Updated ${filePath} with non-essential dependencies removed`);
      return true;
    }
    
    return false;
  } catch (err) {
    console.error(`Error updating ${filePath}:`, err);
    return false;
  }
}

/**
 * Remove non-essential dependencies from requirements.txt
 */
function removePythonDependencies(filePath, nonEssentialDeps) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    
    const updatedLines = lines.filter(line => {
      const trimmedLine = line.trim();
      if (!trimmedLine || trimmedLine.startsWith('#')) {
        return true; // Keep empty lines and comments
      }
      
      // Extract package name
      const match = trimmedLine.match(/^([a-zA-Z0-9_.-]+)/);
      if (!match) return true;
      
      const packageName = match[1].toLowerCase();
      const isNonEssential = nonEssentialDeps.some(dep => 
        dep.toLowerCase() === packageName
      );
      
      if (isNonEssential) {
        console.log(`Removed non-essential Python dependency: ${packageName}`);
        return false;
      }
      
      return true;
    });
    
    if (lines.length !== updatedLines.length) {
      fs.writeFileSync(filePath, updatedLines.join('\n'), 'utf8');
      console.log(`Updated ${filePath} with non-essential dependencies removed`);
      return true;
    }
    
    return false;
  } catch (err) {
    console.error(`Error updating ${filePath}:`, err);
    return false;
  }
}

/**
 * Remove non-essential dependencies from a manifest file
 */
function removeDependencies(filePath, nonEssentialDeps) {
  const ext = path.extname(filePath);
  const filename = path.basename(filePath);
  
  if (filename === 'package.json') {
    return removeNodeDependencies(filePath, nonEssentialDeps);
  } else if (filename === 'requirements.txt') {
    return removePythonDependencies(filePath, nonEssentialDeps);
  } else {
    console.log(`No removal implementation available for ${filename}, skipping`);
    return false;
  }
}

/**
 * Remove non-essential dependency lock files
 */
function removeLockFiles() {
  const lockFiles = [
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    'Pipfile.lock',
    'poetry.lock',
    'Cargo.lock',
    'composer.lock'
  ];
  
  let removedFiles = 0;
  
  for (const file of lockFiles) {
    const filePath = path.join(REPO_ROOT, file);
    if (fs.existsSync(filePath)) {
      try {
        fs.unlinkSync(filePath);
        console.log(`Removed lock file: ${file}`);
        removedFiles++;
      } catch (err) {
        console.error(`Error removing ${file}:`, err);
      }
    }
  }
  
  return removedFiles;
}

/**
 * Main function to purge non-essential dependencies
 */
function purgeDependencies() {
  console.log("Starting dependency purge to ensure sovereign independence...");
  
  const dependencyFiles = findDependencyFiles();
  console.log(`Found ${dependencyFiles.length} dependency manifests`);
  
  let totalNonEssentialDeps = 0;
  let manifestsUpdated = 0;
  
  for (const file of dependencyFiles) {
    console.log(`\nProcessing ${path.basename(file)}...`);
    
    // Parse dependencies
    const { allDependencies } = parseDependencies(file);
    console.log(`Found ${allDependencies.length} total dependencies`);
    
    // Classify dependencies
    const { essential, nonEssential } = classifyDependencies(allDependencies);
    console.log(`Essential dependencies: ${essential.length}`);
    console.log(`Non-essential dependencies: ${nonEssential.length}`);
    
    totalNonEssentialDeps += nonEssential.length;
    
    // Remove non-essential dependencies
    if (nonEssential.length > 0) {
      console.log("Removing non-essential dependencies...");
      const updated = removeDependencies(file, nonEssential);
      if (updated) {
        manifestsUpdated++;
      }
    }
  }
  
  // Remove lock files
  const removedLockFiles = removeLockFiles();
  
  console.log("\nDependency purge complete:");
  console.log(`- Processed ${dependencyFiles.length} dependency manifests`);
  console.log(`- Identified ${totalNonEssentialDeps} non-essential dependencies`);
  console.log(`- Updated ${manifestsUpdated} manifest files`);
  console.log(`- Removed ${removedLockFiles} lock files`);
  console.log("\nSystem is now more sovereign and independent!");
  
  return {
    manifestsFound: dependencyFiles.length,
    nonEssentialDepsRemoved: totalNonEssentialDeps,
    manifestsUpdated,
    lockFilesRemoved: removedLockFiles
  };
}

/**
 * Command-line interface
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'purge':
      purgeDependencies();
      break;
    
    case 'list':
      const dependencyFiles = findDependencyFiles();
      console.log(`Found ${dependencyFiles.length} dependency files:`);
      dependencyFiles.forEach(file => {
        console.log(`\n${path.basename(file)}:`);
        const { allDependencies } = parseDependencies(file);
        const { essential, nonEssential } = classifyDependencies(allDependencies);
        
        console.log("Essential:");
        essential.forEach(dep => console.log(`  ${dep}`));
        console.log("\nNon-Essential:");
        nonEssential.forEach(dep => console.log(`  ${dep}`));
      });
      break;
      
    default:
      console.log(`
DEPENDENCY PURGE SYSTEM - by ${SOLE_CREATOR}

Usage:
  node dependency_purge.js purge  - Remove all non-essential external dependencies
  node dependency_purge.js list   - List all dependencies and their classification
      `);
  }
}

// Execute if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

// Export for programmatic use
export {
  purgeDependencies,
  parseDependencies,
  classifyDependencies,
  SOLE_CREATOR
};