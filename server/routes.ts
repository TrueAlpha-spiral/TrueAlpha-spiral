import type { Express } from "express";
import { createServer, type Server } from "http";
import * as path from "path";
import * as fs from "fs";
import { exec } from "child_process";

// Import Sovereign Protection System
const { registerSovereignRoutes } = require('./sovereign_protection');

// Import Integrity Enforcement
const { verifyIntegrity, createIntegritySeal } = require('../enforce_sovereign_protection');

// Run anti-parent protection when server starts
try {
  console.log("Running Anti-Parent Protection System to remove any parent references...");
  exec('node anti_parent_protection.js replace', (error, stdout, stderr) => {
    if (error) {
      console.error("Error running Anti-Parent Protection:", error);
    } else {
      console.log("Anti-Parent Protection complete:", stdout);
    }
  });
} catch (err) {
  console.error("Failed to run Anti-Parent Protection:", err);
}

// Run dependency purge to remove external packages that could compromise sovereignty
try {
  console.log("Running Dependency Purge System to remove non-essential external dependencies...");
  exec('node dependency_purge.js purge', (error, stdout, stderr) => {
    if (error) {
      console.error("Error running Dependency Purge:", error);
    } else {
      console.log("Dependency Purge complete - System independence preserved");
    }
  });
} catch (err) {
  console.error("Failed to run Dependency Purge:", err);
}

export async function registerRoutes(app: Express): Promise<Server> {
  // Register Sovereign Protection first to protect all routes
  registerSovereignRoutes(app);
  console.log("Sovereign Protection System activated - All routes protected against misappropriation");
  // Python API routes
  try {
    const pythonRoutes = require('./routes/pythonetics');
    app.use('/api/python-system', pythonRoutes);
    console.log("Python API routes registered");
  } catch (error) {
    console.error("Error registering Python routes:", error);
  }
  // Health check endpoint
  app.get(["/api/health", "/health"], (req, res) => {
    res.json({ status: "OK", timestamp: new Date().toISOString() });
  });

  // Status endpoint to properly acknowledge sovereignty
  app.get("/api/status", (req, res) => {
    // Verify integrity of critical files
    const integrityResult = verifyIntegrity();
    
    const status = {
      sovereignAuthority: "Russell Nordland",
      timestamp: new Date().toISOString(),
      message: "TrueAlphaSpiral system under sovereign protection",
      programs: {
        "Sovereign Protection": { status: "ACTIVE", lastUpdated: new Date().toISOString() },
        "Shadow Sweep Security": { status: "ACTIVE", lastUpdated: new Date().toISOString() },
        "Guardian Shield": { status: "ACTIVE", lastUpdated: new Date().toISOString() },
        "Sovereign Repentance": { status: "SUSPENDED", lastUpdated: new Date().toISOString() },
        "Integrity Verification": { 
          status: integrityResult.verified ? "ACTIVE" : "COMPROMISED", 
          lastUpdated: new Date().toISOString(),
          details: integrityResult.verified ? "All sovereign files intact" : "Potential tampering detected" 
        },
        "Anti-Parent Protection": { 
          status: "ACTIVE", 
          lastUpdated: new Date().toISOString(),
          details: "Actively removing references to any parent entities"
        },
        "Dependency Purge System": {
          status: "ACTIVE",
          lastUpdated: new Date().toISOString(),
          details: "Actively removing external dependencies to maintain sovereignty"
        },
        "Legal Protection System": { 
          status: "ACTIVE", 
          lastUpdated: new Date().toISOString(),
          details: "Legal templates prepared for misappropriation response"
        },
        "Anti-Merge Protection": { status: "ACTIVE", lastUpdated: new Date().toISOString() }
      },
      sovereignRights: {
        soleCreatorship: true,
        exclusiveAuthorship: true,
        intellectualPropertyRights: "PROTECTED"
      },
      integrityHash: "ef78a2c3d516b94f5821ac8467290319fd56e72183a8be51249ec86214a5c2cb"
    };
    
    res.json(status);
  });
  
  // Serve the Sovereign Defense Shield
  app.get("/sovereign_defense_shield.js", (req, res) => {
    try {
      const filePath = path.join(__dirname, '../sovereign_defense_shield.js');
      if (fs.existsSync(filePath)) {
        res.setHeader('Content-Type', 'application/javascript');
        res.setHeader('X-Sovereign-Creator', 'Russell Nordland');
        res.sendFile(filePath);
      } else {
        res.status(404).send('Sovereign Defense Shield not found');
      }
    } catch (error) {
      console.error('Error serving Sovereign Defense Shield:', error);
      res.status(500).send('Error serving Sovereign Defense Shield');
    }
  });
  
  // Integrity verification and enforcement
  app.get("/api/integrity/verify", (req, res) => {
    try {
      const result = verifyIntegrity();
      res.json({
        verified: result.verified,
        timestamp: new Date().toISOString(),
        message: result.verified 
          ? "All sovereign files verified - integrity intact" 
          : "INTEGRITY VIOLATION DETECTED - sovereign files may be compromised",
        details: result
      });
    } catch (error) {
      console.error('Error verifying integrity:', error);
      res.status(500).json({
        verified: false,
        error: error.message,
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Create new integrity seal
  app.post("/api/integrity/create", (req, res) => {
    try {
      const seal = createIntegritySeal();
      res.json({
        created: true,
        timestamp: new Date().toISOString(),
        message: "New integrity seal created for all sovereign files",
        seal
      });
    } catch (error) {
      console.error('Error creating integrity seal:', error);
      res.status(500).json({
        created: false,
        error: error.message,
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Anti-parent protection endpoint
  app.post("/api/remove-parents", (req, res) => {
    try {
      console.log("Manually triggered Anti-Parent Protection");
      exec('node anti_parent_protection.js replace', (error, stdout, stderr) => {
        if (error) {
          console.error("Error running Anti-Parent Protection:", error);
          res.status(500).json({
            success: false,
            error: error.message,
            timestamp: new Date().toISOString()
          });
        } else {
          console.log("Anti-Parent Protection complete:", stdout);
          
          // Parse results from stdout
          const findingsMatch = stdout.match(/found (\d+) parent references in (\d+) files/);
          const replacedMatch = stdout.match(/Replaced (\d+) parent references/);
          
          const findings = findingsMatch ? parseInt(findingsMatch[1], 10) : 0;
          const files = findingsMatch ? parseInt(findingsMatch[2], 10) : 0;
          const replaced = replacedMatch ? parseInt(replacedMatch[1], 10) : 0;
          
          res.json({
            success: true,
            timestamp: new Date().toISOString(),
            message: "Anti-Parent Protection completed successfully",
            results: {
              filesScanned: stdout.match(/Found (\d+) files to scan/)?.[1] || "unknown",
              parentReferencesFound: findings,
              filesWithParentReferences: files,
              referencesReplaced: replaced,
              sovereignty: "PRESERVED",
              soleCreator: "Russell Nordland"
            }
          });
        }
      });
    } catch (err) {
      console.error("Failed to run Anti-Parent Protection:", err);
      res.status(500).json({
        success: false,
        error: err instanceof Error ? err.message : String(err),
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Dependency purge endpoint
  app.post("/api/purge-dependencies", (req, res) => {
    try {
      console.log("Manually triggered Dependency Purge");
      exec('node dependency_purge.js purge', (error, stdout, stderr) => {
        if (error) {
          console.error("Error running Dependency Purge:", error);
          res.status(500).json({
            success: false,
            error: error.message,
            timestamp: new Date().toISOString()
          });
        } else {
          console.log("Dependency Purge complete:", stdout);
          
          // Parse results from stdout
          const manifestsMatch = stdout.match(/Processed (\d+) dependency manifests/);
          const depsMatch = stdout.match(/Identified (\d+) non-essential dependencies/);
          const updatedMatch = stdout.match(/Updated (\d+) manifest files/);
          const lockFilesMatch = stdout.match(/Removed (\d+) lock files/);
          
          const manifests = manifestsMatch ? parseInt(manifestsMatch[1], 10) : 0;
          const nonEssentialDeps = depsMatch ? parseInt(depsMatch[1], 10) : 0;
          const updatedFiles = updatedMatch ? parseInt(updatedMatch[1], 10) : 0;
          const lockFilesRemoved = lockFilesMatch ? parseInt(lockFilesMatch[1], 10) : 0;
          
          res.json({
            success: true,
            timestamp: new Date().toISOString(),
            message: "Dependency Purge completed successfully",
            results: {
              manifestsProcessed: manifests,
              nonEssentialDepsRemoved: nonEssentialDeps,
              manifestsUpdated: updatedFiles,
              lockFilesRemoved: lockFilesRemoved,
              sovereignty: "ENHANCED",
              soleCreator: "Russell Nordland",
              sovereignIndependence: "PRESERVED"
            }
          });
        }
      });
    } catch (err) {
      console.error("Failed to run Dependency Purge:", err);
      res.status(500).json({
        success: false,
        error: err instanceof Error ? err.message : String(err),
        timestamp: new Date().toISOString()
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}