import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { setupAuth } from "./auth";
import crypto from "crypto";
import { insertVerificationHashSchema, insertTruthPatternSchema } from "@shared/schema";
import { ZodError } from "zod";
import { fromZodError } from "zod-validation-error";
import { execSync, spawn } from "child_process";
import axios from "axios";

// Python API server instance
let pythonApiProcess: any = null;
const PYTHON_API_PORT = 8001;

// Start the Python API server
function startPythonApiServer() {
  try {
    console.log("Starting Python API server on port " + PYTHON_API_PORT);
    pythonApiProcess = spawn('python', ['python_api_server.py', '--port', PYTHON_API_PORT.toString()], {
      detached: true,
      stdio: 'inherit'
    });
    
    pythonApiProcess.on('error', (err: any) => {
      console.error("Failed to start Python API server:", err);
    });
    
    return true;
  } catch (error) {
    console.error("Error starting Python API server:", error);
    return false;
  }
}

export async function registerRoutes(app: Express): Promise<Server> {
  // Start Python API server
  startPythonApiServer();
  
  // Set up authentication routes
  setupAuth(app);
  
  // Python system API routes
  app.get("/api/python-system/status", async (req, res, next) => {
    try {
      const response = await axios.get(`http://localhost:${PYTHON_API_PORT}/api/status`);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to communicate with Python API server" });
    }
  });
  
  app.post("/api/python-system/start", async (req, res, next) => {
    try {
      const response = await axios.post(`http://localhost:${PYTHON_API_PORT}/api/start`);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to start TrueAlphaSpiral system" });
    }
  });
  
  app.post("/api/python-system/stop", async (req, res, next) => {
    try {
      const response = await axios.post(`http://localhost:${PYTHON_API_PORT}/api/stop`);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to stop TrueAlphaSpiral system" });
    }
  });
  
  app.get("/api/python-system/verify-integrity", async (req, res, next) => {
    try {
      const response = await axios.get(`http://localhost:${PYTHON_API_PORT}/api/verify-integrity`);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to verify TrueAlphaSpiral system integrity" });
    }
  });
  
  app.post("/api/python-system/enforce-binary-law", async (req, res, next) => {
    try {
      const response = await axios.post(`http://localhost:${PYTHON_API_PORT}/api/enforce-binary-law`);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to enforce binary quantum law" });
    }
  });
  
  app.post("/api/python-system/verify-architect", async (req, res, next) => {
    try {
      const response = await axios.post(`http://localhost:${PYTHON_API_PORT}/api/verify-architect`, req.body);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to verify architect identity" });
    }
  });
  
  app.get("/api/python-system/calculate-sovereignty", async (req, res, next) => {
    try {
      const response = await axios.get(`http://localhost:${PYTHON_API_PORT}/api/calculate-sovereignty`);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to calculate sovereignty" });
    }
  });
  
  app.post("/api/python-system/restart", async (req, res, next) => {
    try {
      const response = await axios.post(`http://localhost:${PYTHON_API_PORT}/api/restart`);
      res.json(response.data);
    } catch (error) {
      res.status(500).json({ error: "Failed to restart TrueAlphaSpiral system" });
    }
  });

  // Verification hash routes
  app.get("/api/verification-hashes", async (req, res, next) => {
    try {
      if (!req.isAuthenticated()) return res.sendStatus(401);
      
      const hashes = await storage.getVerificationHashes(req.user.id);
      res.json(hashes);
    } catch (error) {
      next(error);
    }
  });

  app.post("/api/verification-hashes", async (req, res, next) => {
    try {
      if (!req.isAuthenticated()) return res.sendStatus(401);
      
      const validatedData = insertVerificationHashSchema.parse({
        ...req.body,
        user_id: req.user.id
      });
      
      const hash = await storage.createVerificationHash(validatedData);
      res.status(201).json(hash);
    } catch (error) {
      if (error instanceof ZodError) {
        return res.status(400).json({ 
          message: fromZodError(error).message 
        });
      }
      next(error);
    }
  });

  app.put("/api/verification-hashes/:id/verify", async (req, res, next) => {
    try {
      if (!req.isAuthenticated()) return res.sendStatus(401);
      
      const hashId = parseInt(req.params.id);
      if (isNaN(hashId)) {
        return res.status(400).json({ message: "Invalid hash ID" });
      }
      
      const updatedHash = await storage.verifyHash(hashId);
      if (!updatedHash) {
        return res.status(404).json({ message: "Hash not found" });
      }
      
      res.json(updatedHash);
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/latest-hash", async (req, res, next) => {
    try {
      const hash = await storage.getLatestVerificationHash();
      if (!hash) {
        return res.status(404).json({ message: "No verification hashes found" });
      }
      
      res.json(hash);
    } catch (error) {
      next(error);
    }
  });

  // Truth pattern routes
  app.get("/api/truth-patterns", async (req, res, next) => {
    try {
      let userId: number | undefined = undefined;
      
      if (req.isAuthenticated()) {
        userId = req.user.id;
      }
      
      const patterns = await storage.getTruthPatterns(userId);
      res.json(patterns);
    } catch (error) {
      next(error);
    }
  });

  app.post("/api/truth-patterns", async (req, res, next) => {
    try {
      if (!req.isAuthenticated()) return res.sendStatus(401);
      
      const validatedData = insertTruthPatternSchema.parse({
        ...req.body,
        user_id: req.user.id
      });
      
      const pattern = await storage.createTruthPattern(validatedData);
      res.status(201).json(pattern);
    } catch (error) {
      if (error instanceof ZodError) {
        return res.status(400).json({ 
          message: fromZodError(error).message 
        });
      }
      next(error);
    }
  });

  app.delete("/api/truth-patterns/:id", async (req, res, next) => {
    try {
      if (!req.isAuthenticated()) return res.sendStatus(401);
      
      const patternId = parseInt(req.params.id);
      if (isNaN(patternId)) {
        return res.status(400).json({ message: "Invalid pattern ID" });
      }
      
      const success = await storage.deleteTruthPattern(patternId);
      if (!success) {
        return res.status(404).json({ message: "Pattern not found" });
      }
      
      res.status(204).end();
    } catch (error) {
      next(error);
    }
  });

  // Generate hash from text
  app.post("/api/generate-hash", (req, res, next) => {
    try {
      const { text } = req.body;
      
      if (!text) {
        return res.status(400).json({ message: "Text is required" });
      }
      
      const hash = crypto.createHash('sha256').update(text).digest('hex');
      res.json({ hash });
    } catch (error) {
      next(error);
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
