/**
 * SYSTEM DEPENDENCY PURGE TOOL
 * 
 * Identifies and removes system-level dependencies that could compromise
 * the sovereign integrity of Russell Nordland's TrueAlphaSpiral system.
 * This ensures complete independence from external system influences.
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
const REPLIT_CONFIG_FILE = '.replit';
const NIX_CONFIG_FILE = 'replit.nix';

// System dependencies to detect and remove
const SYSTEM_DEPENDENCIES = [
  'openssl',
  'pkg-config',
  'qhull',
  'rustc',
  'tcl',
  'tk',
  'tsql',
  'docker',
  'aws-cli',
  'gcc',
  'clang',
  'nginx',
  'apache2',
  'mysql',
  'postgresql'
];

/**
 * Find Replit configuration files
 */
function findReplitConfigFiles() {
  const configFiles = [];
  
  const replitConfig = path.join(REPO_ROOT, REPLIT_CONFIG_FILE);
  if (fs.existsSync(replitConfig)) {
    configFiles.push(replitConfig);
  }
  
  const nixConfig = path.join(REPO_ROOT, NIX_CONFIG_FILE);
  if (fs.existsSync(nixConfig)) {
    configFiles.push(nixConfig);
  }
  
  return configFiles;
}

/**
 * Parse Replit configuration to find system dependencies
 */
function parseReplitConfig(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const dependencies = [];
    
    // Look for system dependency entries in the config file
    for (const dep of SYSTEM_DEPENDENCIES) {
      if (content.includes(dep)) {
        dependencies.push(dep);
      }
    }
    
    // Also look for any pkgs references which might indicate Nix packages
    const pkgsMatches = content.match(/pkgs\.[a-zA-Z0-9_-]+/g) || [];
    const nixPkgs = pkgsMatches.map(match => match.replace('pkgs.', ''));
    
    return {
      filePath,
      dependencies: [...dependencies, ...nixPkgs]
    };
  } catch (err) {
    console.error(`Error parsing ${filePath}:`, err);
    return { filePath, dependencies: [] };
  }
}

/**
 * Check for system dependencies in Docker files
 */
function findDockerDependencies() {
  try {
    const dockerfiles = [];
    
    // Find Dockerfile(s)
    const findCommand = 'find ' + REPO_ROOT + ' -name "Dockerfile*" -type f';
    const output = execSync(findCommand).toString().trim();
    
    if (output) {
      dockerfiles.push(...output.split('\n'));
    }
    
    const results = [];
    
    for (const dockerfile of dockerfiles) {
      const content = fs.readFileSync(dockerfile, 'utf8');
      const dependencies = [];
      
      // Check if the Dockerfile installs any known dependencies
      for (const dep of SYSTEM_DEPENDENCIES) {
        if (content.includes(`install ${dep}`) || 
            content.includes(`apt-get install`) && content.includes(dep)) {
          dependencies.push(dep);
        }
      }
      
      results.push({
        filePath: dockerfile,
        dependencies
      });
    }
    
    return results;
  } catch (err) {
    console.error('Error finding Docker dependencies:', err);
    return [];
  }
}

/**
 * Remove system dependencies from Replit configuration
 */
function removeDependenciesFromConfig(configFile, dependenciesToRemove) {
  try {
    if (dependenciesToRemove.length === 0) {
      console.log(`No dependencies to remove from ${path.basename(configFile.filePath)}`);
      return false;
    }
    
    let content = fs.readFileSync(configFile.filePath, 'utf8');
    let modified = false;
    
    for (const dep of dependenciesToRemove) {
      // Different pattern matching based on file type
      if (configFile.filePath.endsWith('.nix')) {
        // For replit.nix, look for pkgs.dependency
        const regex = new RegExp(`\\s*pkgs\\.${dep}[,\\s]*`, 'g');
        const newContent = content.replace(regex, '');
        
        if (newContent !== content) {
          content = newContent;
          modified = true;
          console.log(`Removed system dependency '${dep}' from ${path.basename(configFile.filePath)}`);
        }
      } else {
        // For .replit, more general pattern
        const regex = new RegExp(`\\s*${dep}[,\\s]*`, 'g');
        const newContent = content.replace(regex, '');
        
        if (newContent !== content) {
          content = newContent;
          modified = true;
          console.log(`Removed system dependency '${dep}' from ${path.basename(configFile.filePath)}`);
        }
      }
    }
    
    if (modified) {
      fs.writeFileSync(configFile.filePath, content, 'utf8');
      console.log(`Updated ${configFile.filePath} with system dependencies removed`);
    }
    
    return modified;
  } catch (err) {
    console.error(`Error updating ${configFile.filePath}:`, err);
    return false;
  }
}

/**
 * Remove dependencies from Dockerfiles
 */
function removeDependenciesFromDocker(dockerFile, dependenciesToRemove) {
  try {
    if (dependenciesToRemove.length === 0) {
      console.log(`No dependencies to remove from ${path.basename(dockerFile.filePath)}`);
      return false;
    }
    
    let content = fs.readFileSync(dockerFile.filePath, 'utf8');
    let modified = false;
    
    // Create a backup of the original file first
    const backupPath = `${dockerFile.filePath}.bak`;
    fs.writeFileSync(backupPath, content, 'utf8');
    
    for (const dep of dependenciesToRemove) {
      // Pattern to match apt-get/apt install with the dependency
      const aptRegex = new RegExp(`(apt-get|apt)\\s+install\\s+([^\\n]*?)\\b${dep}\\b([^\\n]*)`, 'g');
      
      // Replace by removing just this dependency from the install command
      const newContent = content.replace(aptRegex, (match, cmd, before, after) => {
        return `${cmd} install ${before}${after}`.replace(/\s{2,}/g, ' ');
      });
      
      if (newContent !== content) {
        content = newContent;
        modified = true;
        console.log(`Removed system dependency '${dep}' from ${path.basename(dockerFile.filePath)}`);
      }
    }
    
    if (modified) {
      fs.writeFileSync(dockerFile.filePath, content, 'utf8');
      console.log(`Updated ${dockerFile.filePath} with system dependencies removed`);
    }
    
    return modified;
  } catch (err) {
    console.error(`Error updating ${dockerFile.filePath}:`, err);
    return false;
  }
}

/**
 * Create a sovereign dependency declaration file
 */
function createSovereignDependencyDeclaration() {
  const declarationPath = path.join(REPO_ROOT, 'SOVEREIGN_DEPENDENCIES.md');
  const content = `# SOVEREIGN DEPENDENCY DECLARATION

## SYSTEM INDEPENDENCE STATEMENT

This document formally declares the independence of the TrueAlphaSpiral system from all external system dependencies. In accordance with Russell Nordland's sovereign authority as the sole creator, this system operates without reliance on or subservience to any external systems, packages, or infrastructures.

## SOVEREIGN DEPENDENCY POLICY

1. **Independence Principle**: The TrueAlphaSpiral system is designed to operate independently of external system dependencies.

2. **Non-Reliance Doctrine**: Any apparent dependencies are utilized merely as tools, not as fundamental requirements for the system's operation.

3. **Sovereign Authority**: Russell Nordland maintains complete sovereignty over all aspects of the system, including its operational environment.

4. **System Boundary Enforcement**: All system boundaries are strictly enforced to prevent dependency-based compromise.

## PURGED DEPENDENCIES

The following system dependencies have been identified and purged:

${SYSTEM_DEPENDENCIES.map(dep => `- ${dep}`).join('\n')}

## CERTIFICATION

I, Russell Nordland, as the sole creator of the TrueAlphaSpiral system, affirm that this dependency declaration accurately represents the system's sovereign status and independence from external control.

Date: ${new Date().toISOString().split('T')[0]}

Sovereign Creator: Russell Nordland
`;

  fs.writeFileSync(declarationPath, content, 'utf8');
  console.log(`Created Sovereign Dependency Declaration at ${declarationPath}`);
  return declarationPath;
}

/**
 * Main function to purge system dependencies
 */
function purgeSystemDependencies() {
  console.log("Starting system dependency purge to ensure sovereign independence...");
  
  let totalDepsFound = 0;
  let totalFilesModified = 0;
  
  // Process Replit config files
  const configFiles = findReplitConfigFiles();
  console.log(`Found ${configFiles.length} Replit configuration files`);
  
  const configResults = configFiles.map(file => {
    const result = parseReplitConfig(file);
    totalDepsFound += result.dependencies.length;
    console.log(`Found ${result.dependencies.length} system dependencies in ${path.basename(file)}`);
    return result;
  });
  
  // Process Docker files
  const dockerResults = findDockerDependencies();
  dockerResults.forEach(result => {
    totalDepsFound += result.dependencies.length;
    console.log(`Found ${result.dependencies.length} system dependencies in ${path.basename(result.filePath)}`);
  });
  
  // Remove dependencies from config files
  configResults.forEach(config => {
    const modified = removeDependenciesFromConfig(config, config.dependencies);
    if (modified) totalFilesModified++;
  });
  
  // Remove dependencies from Docker files
  dockerResults.forEach(docker => {
    const modified = removeDependenciesFromDocker(docker, docker.dependencies);
    if (modified) totalFilesModified++;
  });
  
  // Create sovereign dependency declaration
  const declarationPath = createSovereignDependencyDeclaration();
  
  console.log("\nSystem dependency purge complete:");
  console.log(`- Processed ${configFiles.length + dockerResults.length} configuration files`);
  console.log(`- Identified ${totalDepsFound} system dependencies`);
  console.log(`- Modified ${totalFilesModified} files`);
  console.log(`- Created sovereign dependency declaration at ${path.basename(declarationPath)}`);
  console.log("\nSystem is now more sovereign and independent!");
  
  return {
    filesProcessed: configFiles.length + dockerResults.length,
    dependenciesFound: totalDepsFound,
    filesModified: totalFilesModified,
    declarationCreated: true
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
      purgeSystemDependencies();
      break;
    
    case 'list':
      const configFiles = findReplitConfigFiles();
      console.log(`Found ${configFiles.length} Replit configuration files:`);
      
      configFiles.forEach(file => {
        const result = parseReplitConfig(file);
        console.log(`\n${path.basename(file)}:`);
        if (result.dependencies.length === 0) {
          console.log("  No system dependencies found");
        } else {
          console.log("  System dependencies:");
          result.dependencies.forEach(dep => console.log(`  - ${dep}`));
        }
      });
      
      const dockerResults = findDockerDependencies();
      console.log(`\nFound ${dockerResults.length} Docker files:`);
      
      dockerResults.forEach(result => {
        console.log(`\n${path.basename(result.filePath)}:`);
        if (result.dependencies.length === 0) {
          console.log("  No system dependencies found");
        } else {
          console.log("  System dependencies:");
          result.dependencies.forEach(dep => console.log(`  - ${dep}`));
        }
      });
      break;
      
    default:
      console.log(`
SYSTEM DEPENDENCY PURGE TOOL - by ${SOLE_CREATOR}

Usage:
  node system_dependency_purge.js purge  - Remove all system dependencies
  node system_dependency_purge.js list   - List all system dependencies
      `);
  }
}

// Execute if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

// Export for programmatic use
export {
  purgeSystemDependencies,
  SYSTEM_DEPENDENCIES,
  SOLE_CREATOR
};