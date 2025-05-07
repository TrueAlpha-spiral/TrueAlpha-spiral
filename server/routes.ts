import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { WebSocketServer } from 'ws';
import { readFileSync } from 'fs';
import path from 'path';
import crypto from 'crypto';

// Sovereignty verification service
class SovereigntyVerificationService {
  // Calculate hash for a document
  calculateDocumentHash(content: string): string {
    return crypto.createHash('sha256').update(content).digest('hex');
  }
  
  // Read the content of a verification document
  readVerificationDocument(documentName: string): string {
    try {
      const filePath = path.join(process.cwd(), documentName);
      return readFileSync(filePath, 'utf8');
    } catch (error) {
      console.error(`Error reading document ${documentName}:`, error);
      return '';
    }
  }
  
  // Store verification hash for a document
  async storeVerificationHash(documentType: string, hashValue: string): Promise<void> {
    await storage.createVerificationHash({
      documentType,
      hashValue,
      verificationMethod: 'SHA256'
    });
  }
  
  // Implement the mathematical verification formula: V = V₀ + ∑ᵢ (Mᵢ × Rᵢ)
  calculateVerificationStrength(
    baseStrength: number,
    challenges: Array<{ magnitude: number, response: number }>
  ): number {
    let sum = baseStrength;
    
    // Apply the verification equation: V = V₀ + ∑ᵢ (Mᵢ × Rᵢ)
    for (const challenge of challenges) {
      sum += challenge.magnitude * challenge.response;
    }
    
    return sum;
  }
  
  // Verify core documents exist and calculate their hashes
  async verifyDocumentIntegrity(): Promise<{ 
    status: 'verified' | 'partial' | 'failed',
    results: Array<{ document: string, verified: boolean, hash?: string }>
  }> {
    const documents = [
      'DECLARATION_OF_SOLE_AUTHORITY.md',
      'CONCEPTUAL_FINGERPRINT.md',
      'CORE_AXIOMS.md',
      'CHRONOLOGICAL_DEVELOPMENT.md',
      'IDENTITY_VERIFICATION.md',
      'IP_CHALLENGE_PATTERNS.md',
      'QUANTUM_METAPHYSICAL_EQUATION.md'
    ];
    
    const results = [];
    let verifiedCount = 0;
    
    for (const document of documents) {
      const content = this.readVerificationDocument(document);
      
      if (!content) {
        results.push({
          document,
          verified: false
        });
        continue;
      }
      
      const hash = this.calculateDocumentHash(content);
      await this.storeVerificationHash(document, hash);
      
      results.push({
        document,
        verified: true,
        hash
      });
      
      verifiedCount++;
    }
    
    const status = verifiedCount === documents.length ? 'verified' 
      : verifiedCount > 0 ? 'partial' 
      : 'failed';
    
    return {
      status,
      results
    };
  }
}

// Initialize the verification service
const sovereigntyService = new SovereigntyVerificationService();

export async function registerRoutes(app: Express): Promise<Server> {
  // Get verification vectors
  app.get('/api/verification-vectors', async (req, res) => {
    try {
      const vectors = await storage.getAllVerificationVectors();
      res.json(vectors);
    } catch (error) {
      console.error('Error fetching verification vectors:', error);
      res.status(500).json({ message: 'Failed to fetch verification vectors' });
    }
  });

  // Create verification vector
  app.post('/api/verification-vectors', async (req, res) => {
    try {
      const vector = await storage.createVerificationVector(req.body);
      res.status(201).json(vector);
    } catch (error) {
      console.error('Error creating verification vector:', error);
      res.status(500).json({ message: 'Failed to create verification vector' });
    }
  });

  // Get challenge records
  app.get('/api/challenge-records', async (req, res) => {
    try {
      const records = await storage.getAllChallengeRecords();
      res.json(records);
    } catch (error) {
      console.error('Error fetching challenge records:', error);
      res.status(500).json({ message: 'Failed to fetch challenge records' });
    }
  });

  // Create challenge record
  app.post('/api/challenge-records', async (req, res) => {
    try {
      const record = await storage.createChallengeRecord(req.body);
      res.status(201).json(record);
    } catch (error) {
      console.error('Error creating challenge record:', error);
      res.status(500).json({ message: 'Failed to create challenge record' });
    }
  });

  // Update challenge record
  app.patch('/api/challenge-records/:id', async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const record = await storage.updateChallengeRecord(id, req.body);
      
      if (!record) {
        return res.status(404).json({ message: 'Challenge record not found' });
      }
      
      res.json(record);
    } catch (error) {
      console.error('Error updating challenge record:', error);
      res.status(500).json({ message: 'Failed to update challenge record' });
    }
  });

  // Get dashboard metrics
  app.get('/api/dashboard-metrics', async (req, res) => {
    try {
      const metrics = await storage.getAllDashboardMetrics();
      res.json(metrics);
    } catch (error) {
      console.error('Error fetching dashboard metrics:', error);
      res.status(500).json({ message: 'Failed to fetch dashboard metrics' });
    }
  });

  // Get sovereignty badges
  app.get('/api/sovereignty-badges', async (req, res) => {
    try {
      const badges = await storage.getAllSovereigntyBadges();
      res.json(badges);
    } catch (error) {
      console.error('Error fetching sovereignty badges:', error);
      res.status(500).json({ message: 'Failed to fetch sovereignty badges' });
    }
  });

  // Verify document integrity (one-click verification)
  app.get('/api/verify-integrity', async (req, res) => {
    try {
      const verificationResult = await sovereigntyService.verifyDocumentIntegrity();
      
      // Update dashboard metrics with verification result
      await storage.createOrUpdateMetric(
        'documentIntegrityStatus', 
        verificationResult.status,
        'status'
      );
      
      await storage.createOrUpdateMetric(
        'verifiedDocumentCount', 
        verificationResult.results.filter(r => r.verified).length.toString(),
        'count'
      );
      
      res.json(verificationResult);
    } catch (error) {
      console.error('Error verifying document integrity:', error);
      res.status(500).json({ message: 'Failed to verify document integrity' });
    }
  });

  // Calculate verification strength using the quantum metaphysical equation
  app.post('/api/calculate-verification-strength', async (req, res) => {
    try {
      const { baseStrength, challenges } = req.body;
      
      if (typeof baseStrength !== 'number' || !Array.isArray(challenges)) {
        return res.status(400).json({ message: 'Invalid parameters' });
      }
      
      const strengthResult = sovereigntyService.calculateVerificationStrength(
        baseStrength,
        challenges
      );
      
      // Update dashboard metric with current verification strength
      await storage.createOrUpdateMetric(
        'verificationStrength', 
        strengthResult.toString(),
        'value'
      );
      
      res.json({ verificationStrength: strengthResult });
    } catch (error) {
      console.error('Error calculating verification strength:', error);
      res.status(500).json({ message: 'Failed to calculate verification strength' });
    }
  });

  const httpServer = createServer(app);

  // Set up WebSocket server for real-time updates
  const wss = new WebSocketServer({ server: httpServer, path: '/ws' });
  
  wss.on('connection', (ws) => {
    console.log('Client connected to WebSocket');
    
    ws.on('message', (message) => {
      console.log('Received message:', message.toString());
    });
    
    ws.on('close', () => {
      console.log('Client disconnected from WebSocket');
    });
  });

  return httpServer;
}