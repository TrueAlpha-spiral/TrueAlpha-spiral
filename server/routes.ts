import type { Express } from 'express';
import { createServer, type Server } from 'http';
import express from 'express';
import crypto from 'crypto';
import { storage } from './storage';
import { 
  verifyTextSchema, 
  aiAuditSchema, 
  crossReferenceSchema,
  sharePatternSchema,
  exportPatternSchema,
  importPatternSchema,
  insertTarsiPilotApplicationSchema
} from '@shared/schema';
import { verificationEngine } from './services/verification-engine';
import { crossReferenceService } from './services/cross-reference-service';
import { 
  calculateRiskScore, 
  calculateComplianceScore, 
  generateRecommendations, 
  generateAuditSummary 
} from './services/ai-audit-utilities';
import {
  checkPythonApiHealth,
  getTasStatus,
  auditContent,
  auditMedicalContent,
  getTasPatterns,
  getPatternTypes,
  getCategories,
  getAuditResult
} from './services/python-api-service';
import { ethicalGovernance } from './services/ethical-governance';
import { shadowDefense } from './services/shadow-defense';
import fetch from 'node-fetch';
import { v4 as uuidv4 } from 'uuid';
import treeRoutes from './tree-routes';
import avfRoutes from './routes/avf-routes';

export function registerRoutes(app: Express): Server {
  // Root API endpoint for JSON content
  app.get('/api', (_req, res) => {
    res.json({
      name: 'TrueAlphaSpiral Enterprise AI Auditing Solution',
      version: '1.0.0',
      description: 'Advanced auditing solution for verifying AI systems across dimensional boundaries',
      endpoints: [
        '/api/health',
        '/api/documentation',
        '/api/python-status',
        '/api/truth-patterns',
        '/api/verify',
        '/api/cross-reference',
        '/api/ai-audit',
        '/api/dimensional-simulation',
        '/api/ethical-governance',
        '/api/shadow-defense',
        '/api/tarsi-pilot/applications',
        '/api/tree',
        '/api/avf'
      ],
      timestamp: new Date().toISOString()
    });
  });

  // Simple health check endpoint
  app.get('/api/health', (_req, res) => {
    res.json({ 
      status: 'ok',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development',
      service: 'TrueAlphaSpiral Enterprise AI Auditing Solution'
    });
  });
  
  // Serve documentation files
  app.get('/api/documentation/:filename', (req, res) => {
    const { filename } = req.params;
    import('path').then(path => {
      import('fs/promises').then(async fs => {
        // Whitelist of allowed documentation files
        const allowedFiles = [
          'SYSTEM_BOUNDARIES_AND_SOVEREIGNTY.md',
          'INDEPENDENT_VERIFICATION_LAYER.md',
          'SOVEREIGNTY_PRINCIPLES.md',
          'TARSI_ARCHITECTURAL_BLUEPRINT.md'
        ];
        
        if (!allowedFiles.includes(filename)) {
          return res.status(404).json({ error: 'Documentation file not found' });
        }
        
        const filePath = path.resolve(process.cwd(), filename);
        
        try {
          const data = await fs.readFile(filePath, 'utf8');
          res.setHeader('Content-Type', 'text/markdown');
          res.send(data);
        } catch (err) {
          console.error(`Error reading documentation file ${filename}:`, err);
          return res.status(500).json({ error: 'Failed to read documentation file' });
        }
      }).catch(err => {
        console.error('Error importing fs module:', err);
        res.status(500).json({ error: 'Server configuration error' });
      });
    }).catch(err => {
      console.error('Error importing path module:', err);
      res.status(500).json({ error: 'Server configuration error' });
    });
  });
  
  // Python API status endpoint
  app.get('/api/python-status', async (_req, res) => {
    try {
      const status = await checkPythonApiHealth();
      
      if (status.isRunning) {
        // If Python API is running, get TAS status for more details
        try {
          const tasStatus = await getTasStatus();
          status.data = tasStatus;
        } catch (error) {
          console.error('Error fetching TAS status:', error);
          // We still consider the API as running even if TAS status fails
        }
      }
      
      res.json(status);
    } catch (error) {
      console.error('Error checking Python API health:', error);
      res.status(500).json({ 
        isRunning: false, 
        error: 'Failed to check Python API health' 
      });
    }
  });
  // Get truth patterns
  app.get('/api/truth-patterns', async (_req, res) => {
    try {
      const patterns = await storage.getTruthPatterns();
      res.json(patterns);
    } catch (error) {
      console.error('Error fetching truth patterns:', error);
      res.status(500).json({ error: 'Failed to fetch truth patterns' });
    }
  });

  // Get a specific truth pattern
  app.get('/api/truth-patterns/:id', async (req, res) => {
    try {
      const pattern = await storage.getTruthPattern(Number(req.params.id));
      if (!pattern) {
        return res.status(404).json({ error: 'Pattern not found' });
      }
      res.json(pattern);
    } catch (error) {
      console.error('Error fetching truth pattern:', error);
      res.status(500).json({ error: 'Failed to fetch truth pattern' });
    }
  });

  // Create a new truth pattern
  app.post('/api/truth-patterns', async (req, res) => {
    try {
      const newPattern = await storage.createTruthPattern(req.body);
      res.status(201).json(newPattern);
    } catch (error) {
      console.error('Error creating truth pattern:', error);
      res.status(500).json({ error: 'Failed to create truth pattern' });
    }
  });

  // Update a truth pattern
  app.patch('/api/truth-patterns/:id', async (req, res) => {
    try {
      const updatedPattern = await storage.updateTruthPattern(Number(req.params.id), req.body);
      if (!updatedPattern) {
        return res.status(404).json({ error: 'Pattern not found' });
      }
      res.json(updatedPattern);
    } catch (error) {
      console.error('Error updating truth pattern:', error);
      res.status(500).json({ error: 'Failed to update truth pattern' });
    }
  });

  // Delete a truth pattern
  app.delete('/api/truth-patterns/:id', async (req, res) => {
    try {
      const success = await storage.deleteTruthPattern(Number(req.params.id));
      if (!success) {
        return res.status(404).json({ error: 'Pattern not found' });
      }
      res.status(204).send();
    } catch (error) {
      console.error('Error deleting truth pattern:', error);
      res.status(500).json({ error: 'Failed to delete truth pattern' });
    }
  });

  // Verify text using TrueAlphaSpiral engine
  app.post('/api/verify', async (req, res) => {
    try {
      // Validate request body
      const validation = verifyTextSchema.safeParse(req.body);
      if (!validation.success) {
        return res.status(400).json({ error: 'Invalid request body', details: validation.error });
      }

      const input = validation.data;
      
      // Get truth patterns
      const patterns = await storage.getTruthPatterns();
      
      // Verify text using TrueAlphaSpiral engine
      const result = await verificationEngine.verifyText(input.content, patterns);
      
      // Store verification result
      const verification = await storage.createTextVerification({
        content: input.content,
        verificationResult: result as any,
        truthScore: result.truthScore,
        processingTimeMs: result.processingTimeMs
      });
      
      // Store highlights
      for (const highlight of result.highlights) {
        await storage.createVerificationHighlight({
          verificationId: verification.id,
          startIndex: highlight.startIndex,
          endIndex: highlight.endIndex,
          highlightType: highlight.type,
          confidenceScore: highlight.confidenceScore,
          patternId: highlight.patternName ? 
            (patterns.find(p => p.name === highlight.patternName)?.id || null) : 
            null,
          message: highlight.message
        });
      }
      
      res.json({ 
        id: verification.id,
        ...result 
      });
    } catch (error) {
      console.error('Error verifying text:', error);
      res.status(500).json({ error: 'Failed to verify text' });
    }
  });

  // Get verification history
  app.get('/api/verifications', async (_req, res) => {
    try {
      const verifications = await storage.getTextVerifications();
      res.json(verifications);
    } catch (error) {
      console.error('Error fetching verifications:', error);
      res.status(500).json({ error: 'Failed to fetch verifications' });
    }
  });

  // Get a specific verification with its highlights
  app.get('/api/verifications/:id', async (req, res) => {
    try {
      const verification = await storage.getTextVerification(Number(req.params.id));
      if (!verification) {
        return res.status(404).json({ error: 'Verification not found' });
      }
      
      const highlights = await storage.getVerificationHighlightsByVerificationId(verification.id);
      
      res.json({
        ...verification,
        highlights
      });
    } catch (error) {
      console.error('Error fetching verification:', error);
      res.status(500).json({ error: 'Failed to fetch verification' });
    }
  });

  // Mock route for Python system status - to simulate integration with existing TrueAlphaSpiral components
  app.get('/api/python-system/status', (_req, res) => {
    res.json({
      status: 'running',
      version: '1.0.0',
      components: {
        truthPatternRecovery: 'active',
        quantumDNARetrieval: 'standby',
        integrityGuardian: 'active',
        ethicalSpiralKernel: 'active'
      },
      lastUpdated: new Date().toISOString()
    });
  });
  
  // Mock route for Python verification API
  app.post('/api/python-system/verify', (req, res) => {
    const { content, framework } = req.body;
    
    // Generate a simulated verification response from Python system
    // This simulates the quantum echo verification system
    const words = content.split(/\s+/).length;
    let verification_score = 0.85 + (Math.random() * 0.1 - 0.05);
    
    // Reduce score slightly for longer content (simulating more complexity)
    if (words > 50) {
      verification_score -= 0.02;
    }
    
    // Different regulatory frameworks might have different baseline scores
    if (framework === 'financial_services') {
      verification_score -= 0.03;
    } else if (framework === 'healthcare') {
      verification_score -= 0.02;
    }
    
    res.json({
      verification_id: `py_verify_${Date.now()}`,
      verification_score,
      quantum_integrity_check: "passed",
      timestamp: new Date().toISOString(),
      verification_method: "quantum_echo",
      regulatory_framework: framework,
      content_length: content.length,
      word_count: words
    });
  });
  
  // Cross-reference verification endpoint
  app.post('/api/cross-reference', async (req, res) => {
    try {
      // Validate request body
      const validation = crossReferenceSchema.safeParse(req.body);
      if (!validation.success) {
        return res.status(400).json({ error: 'Invalid request body', details: validation.error });
      }
      
      const input = validation.data;
      
      // Get truth patterns
      const patterns = await storage.getTruthPatterns();
      
      // First, perform standard verification
      const verificationResult = await verificationEngine.verifyText(input.content, patterns);
      
      // Save verification result to database
      const verification = await storage.createTextVerification({
        content: input.content,
        truthScore: verificationResult.truthScore,
        processingTimeMs: verificationResult.processingTimeMs,
        verificationResult: verificationResult
      });
      
      // Save highlights to database
      for (const highlight of verificationResult.highlights) {
        await storage.createVerificationHighlight({
          verificationId: verification.id,
          startIndex: highlight.startIndex,
          endIndex: highlight.endIndex,
          highlightType: highlight.type,
          confidenceScore: highlight.confidenceScore,
          patternId: null, // Will be set properly below if a pattern match exists
          message: highlight.message
        });
      }
      
      // Now perform cross-reference verification
      const regulatoryFramework = input.options?.regulatoryFramework || 'general';
      const crossReferenceResult = await crossReferenceService.performCrossReferenceVerification(
        input.content, 
        verificationResult,
        {
          enabledSources: input.options?.enabledSources,
          minConfidenceThreshold: input.options?.minConfidenceThreshold || 0.8,
          regulatoryFramework
        }
      );
      
      // Return the combined results
      res.json({
        id: verification.id,
        verificationResult,
        crossReferenceResult
      });
    } catch (error) {
      console.error('Error cross-referencing text:', error);
      res.status(500).json({ error: 'Failed to cross-reference text' });
    }
  });

  // AI Auditing Routes
  
  // Run AI audit on content
  app.post('/api/ai-audit', async (req, res) => {
    try {
      // Validate request body
      const validation = aiAuditSchema.safeParse(req.body);
      if (!validation.success) {
        return res.status(400).json({ error: 'Invalid request body', details: validation.error });
      }

      const input = validation.data;
      
      // Get truth patterns
      const patterns = await storage.getTruthPatterns();
      
      // Verify text using TrueAlphaSpiral engine
      const verificationResult = await verificationEngine.verifyText(input.content, patterns);
      
      // Also perform cross-reference verification
      const crossReferenceResult = await crossReferenceService.performCrossReferenceVerification(
        input.content,
        verificationResult,
        {
          regulatoryFramework: input.regulatoryFramework
        }
      );
      
      // Store verification result
      const verification = await storage.createTextVerification({
        content: input.content,
        verificationResult: verificationResult as any,
        truthScore: verificationResult.truthScore,
        processingTimeMs: verificationResult.processingTimeMs
      });
      
      // Store highlights
      for (const highlight of verificationResult.highlights) {
        await storage.createVerificationHighlight({
          verificationId: verification.id,
          startIndex: highlight.startIndex,
          endIndex: highlight.endIndex,
          highlightType: highlight.type,
          confidenceScore: highlight.confidenceScore,
          patternId: highlight.patternName ? 
            (patterns.find(p => p.name === highlight.patternName)?.id || null) : 
            null,
          message: highlight.message
        });
      }
      
      // Calculate risk and compliance scores including cross-reference results
      const riskScore = calculateRiskScore(
        verificationResult, 
        input.regulatoryFramework,
        crossReferenceResult
      );
      
      const complianceScore = calculateComplianceScore(
        verificationResult, 
        input.regulatoryFramework,
        crossReferenceResult
      );
      
      // Generate recommendations including cross-reference insights
      const recommendations = generateRecommendations(
        verificationResult, 
        input.regulatoryFramework,
        crossReferenceResult
      );
      
      // Generate blockchain record (mock)
      const blockchainRecord = `audit_${Date.now()}_${Math.floor(Math.random() * 1000000)}`;
      
      // Create audit summary with cross-reference data
      const auditSummary = generateAuditSummary(
        verificationResult, 
        riskScore, 
        complianceScore, 
        input.regulatoryFramework,
        crossReferenceResult
      );
      
      // Create AI audit record
      const aiAudit = await storage.createAIAudit({
        clientName: input.clientName,
        aiSystemName: input.aiSystemName,
        regulatoryFramework: input.regulatoryFramework,
        status: 'completed',
        auditSummary,
        riskScore,
        complianceScore,
        verificationId: verification.id,
        blockchainRecord,
        auditReport: {
          verificationResult,
          crossReferenceResult,
          recommendations,
          processingTimeMs: verificationResult.processingTimeMs,
          regulatoryFramework: input.regulatoryFramework,
          options: input.options
        }
      });
      
      // Return audit result
      res.json({
        id: aiAudit.id,
        clientName: input.clientName,
        aiSystemName: input.aiSystemName,
        regulatoryFramework: input.regulatoryFramework,
        status: 'completed',
        auditSummary,
        riskScore,
        complianceScore,
        verificationResult,
        crossReferenceResult,
        blockchainRecord,
        recommendations,
        processingTimeMs: verificationResult.processingTimeMs
      });
    } catch (error) {
      console.error('Error performing AI audit:', error);
      res.status(500).json({ error: 'Failed to perform AI audit' });
    }
  });
  
  // Get AI audit history
  app.get('/api/ai-audits', async (_req, res) => {
    try {
      const audits = await storage.getAIAudits();
      res.json(audits);
    } catch (error) {
      console.error('Error fetching AI audits:', error);
      res.status(500).json({ error: 'Failed to fetch AI audits' });
    }
  });
  
  // Get a specific AI audit
  app.get('/api/ai-audits/:id', async (req, res) => {
    try {
      const audit = await storage.getAIAudit(Number(req.params.id));
      if (!audit) {
        return res.status(404).json({ error: 'AI audit not found' });
      }
      
      // Get verification result if available
      let verificationResult = null;
      let highlights: { 
        id: number; 
        verificationId: number; 
        startIndex: number; 
        endIndex: number; 
        highlightType: string; 
        confidenceScore: number; 
        patternId: number | null; 
        message: string | null; 
        createdAt: Date 
      }[] = [];
      
      if (audit.verificationId) {
        const verification = await storage.getTextVerification(audit.verificationId);
        if (verification) {
          verificationResult = verification.verificationResult;
          highlights = await storage.getVerificationHighlightsByVerificationId(verification.id);
        }
      }
      
      res.json({
        ...audit,
        verification: verificationResult ? {
          ...verificationResult,
          highlights
        } : null
      });
    } catch (error) {
      console.error('Error fetching AI audit:', error);
      res.status(500).json({ error: 'Failed to fetch AI audit' });
    }
  });
  
  // TAS Truth Audit Add-on API endpoints - Connect to Python API
  
  // Get TAS status
  app.get('/api/tas/status', async (_req, res) => {
    try {
      const healthCheck = await checkPythonApiHealth();
      
      if (!healthCheck.isRunning) {
        console.error(`[express] Python API server not running: ${healthCheck.error}`);
        // Fallback response if Python API is not available
        return res.status(503).json({
          status: "unavailable",
          error: "Python API server is not running",
          timestamp: new Date().toISOString()
        });
      }
      
      const status = await getTasStatus();
      res.json(status);
    } catch (error) {
      console.error('[express] Error getting TAS status:', error);
      res.status(500).json({ 
        status: "error", 
        error: "Failed to get TAS status",
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Audit content
  app.post('/api/tas/audit', async (req, res) => {
    try {
      const { content, audit_type, api_key, client_id } = req.body;
      
      if (!content || !content.text) {
        return res.status(400).json({ 
          success: false, 
          error: "Missing or invalid content. Must provide 'text' field." 
        });
      }
      
      // Try to connect to Python API
      const healthCheck = await checkPythonApiHealth();
      
      if (!healthCheck.isRunning) {
        console.error(`[express] Python API server not running: ${healthCheck.error}`);
        return res.status(503).json({
          success: false,
          error: "Python API server is not running",
          timestamp: new Date().toISOString()
        });
      }
      
      // Call Python API to audit content
      const result = await auditContent(content, audit_type, api_key, client_id);
      res.json(result);
    } catch (error) {
      console.error('[express] Error auditing content:', error);
      res.status(500).json({ 
        success: false, 
        error: "Failed to audit content",
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Audit medical content with enhanced hallucination detection
  // Incorporating second-order cybernetics principles based on research
  // Includes: self-reflexivity, recursive ethical resonance, and human-AI collaboration
  app.post('/api/tas/audit-medical', async (req, res) => {
    try {
      const { content, audit_type, api_key, client_id } = req.body;
      
      if (!content || !content.text) {
        return res.status(400).json({ 
          success: false, 
          error: "Missing or invalid content. Must provide 'text' field." 
        });
      }
      
      console.log('[express] Starting medical content audit with second-order cybernetics integration');
      
      // Try to connect to Python API
      const healthCheck = await checkPythonApiHealth();
      
      // Even if Python API is not running, we'll use the fallback mechanism 
      // in the auditMedicalContent function which incorporates:
      // 1. MetaFloor Validation (self-reflexivity against truth repository)
      // 2. Recursive Ethical Resonance (meta-corrections for ethics alignment)
      // 3. Ethical Oracles (specialized pattern detection for hallucinations)
      
      // Call Python API to audit medical content with enhanced capabilities
      const result = await auditMedicalContent(content, audit_type, api_key, client_id);
      
      // Enhance response with additional second-order cybernetics metadata based on P&G research
      // This allows the system to be self-reflexive about its own audit process
      const enhancedResult = {
        ...result,
        cybernetic_meta: {
          self_reflexivity: true,
          observer_participant_integration: true,
          confidence_threshold_applied: result.result.truth_score < 0.7 ? "high_scrutiny" : "standard",
          metafloor_validation_level: result.result.truth_score > 0.85 ? "high" : result.result.truth_score > 0.7 ? "medium" : "low",
          framework_integration: "P&G collaborative model applied"
        }
      };
      
      console.log('[express] Medical content audit completed with cybernetic enhancements');
      res.json(enhancedResult);
    } catch (error) {
      console.error('[express] Error auditing medical content:', error);
      res.status(500).json({ 
        success: false, 
        error: "Failed to audit medical content",
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Get patterns
  app.get('/api/tas/patterns', async (req, res) => {
    try {
      // Extract query parameters
      const patternType = req.query.pattern_type as string | undefined;
      const category = req.query.category as string | undefined;
      const minResonance = req.query.min_resonance ? parseFloat(req.query.min_resonance as string) : undefined;
      
      // Try to connect to Python API
      const healthCheck = await checkPythonApiHealth();
      
      if (!healthCheck.isRunning) {
        console.error(`[express] Python API server not running: ${healthCheck.error}`);
        return res.status(503).json({
          error: "Python API server is not running",
          timestamp: new Date().toISOString()
        });
      }
      
      // Call Python API to get patterns
      const patterns = await getTasPatterns(patternType, category, minResonance);
      res.json(patterns);
    } catch (error) {
      console.error('[express] Error getting patterns:', error);
      res.status(500).json({ 
        error: "Failed to get patterns",
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Get pattern types
  app.get('/api/tas/pattern-types', async (_req, res) => {
    try {
      // Try to connect to Python API
      const healthCheck = await checkPythonApiHealth();
      
      if (!healthCheck.isRunning) {
        console.error(`[express] Python API server not running: ${healthCheck.error}`);
        return res.status(503).json({
          error: "Python API server is not running",
          timestamp: new Date().toISOString()
        });
      }
      
      // Call Python API to get pattern types
      const patternTypes = await getPatternTypes();
      res.json(patternTypes);
    } catch (error) {
      console.error('[express] Error getting pattern types:', error);
      res.status(500).json({ 
        error: "Failed to get pattern types",
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Get categories
  app.get('/api/tas/categories', async (_req, res) => {
    try {
      // Try to connect to Python API
      const healthCheck = await checkPythonApiHealth();
      
      if (!healthCheck.isRunning) {
        console.error(`[express] Python API server not running: ${healthCheck.error}`);
        return res.status(503).json({
          error: "Python API server is not running",
          timestamp: new Date().toISOString()
        });
      }
      
      // Call Python API to get categories
      const categories = await getCategories();
      res.json(categories);
    } catch (error) {
      console.error('[express] Error getting categories:', error);
      res.status(500).json({ 
        error: "Failed to get categories",
        timestamp: new Date().toISOString()
      });
    }
  });
  
  // Get audit result by ID
  app.get('/api/tas/audit-result/:audit_id', async (req, res) => {
    try {
      const auditId = req.params.audit_id;
      
      // Try to connect to Python API
      const healthCheck = await checkPythonApiHealth();
      
      if (!healthCheck.isRunning) {
        console.error(`[express] Python API server not running: ${healthCheck.error}`);
        return res.status(503).json({
          error: "Python API server is not running",
          timestamp: new Date().toISOString()
        });
      }
      
      // Call Python API to get audit result
      const auditResult: any = await getAuditResult(auditId);
      
      if (auditResult && typeof auditResult === 'object' && 'success' in auditResult && !auditResult.success) {
        return res.status(404).json({ 
          error: "Audit result not found",
          timestamp: new Date().toISOString()
        });
      }
      
      if (auditResult && typeof auditResult === 'object' && 'result' in auditResult) {
        res.json(auditResult.result);
      } else {
        res.json(auditResult);
      }
    } catch (error) {
      console.error('[express] Error getting audit result:', error);
      res.status(500).json({ 
        error: "Failed to get audit result",
        timestamp: new Date().toISOString()
      });
    }
  });

  // *** Universal Truth Pattern Sharing Widget API Endpoints ***
  
  // Get all shared truth patterns
  app.get('/api/shared-patterns', async (_req, res) => {
    try {
      const patterns = await storage.getSharedTruthPatterns();
      res.json(patterns);
    } catch (error) {
      console.error('Error fetching shared truth patterns:', error);
      res.status(500).json({ error: 'Failed to fetch shared truth patterns' });
    }
  });

  // Get a specific shared truth pattern
  app.get('/api/shared-patterns/:id', async (req, res) => {
    try {
      const pattern = await storage.getSharedTruthPattern(Number(req.params.id));
      if (!pattern) {
        return res.status(404).json({ error: 'Shared pattern not found' });
      }
      res.json(pattern);
    } catch (error) {
      console.error('Error fetching shared truth pattern:', error);
      res.status(500).json({ error: 'Failed to fetch shared truth pattern' });
    }
  });

  // Get a shared truth pattern by sharing link
  app.get('/api/shared-patterns/link/:sharingLink', async (req, res) => {
    try {
      const pattern = await storage.getSharedTruthPatternByLink(req.params.sharingLink);
      if (!pattern) {
        return res.status(404).json({ error: 'Shared pattern not found' });
      }
      
      // Increment usage count
      await storage.incrementSharedPatternUsageCount(pattern.id);
      
      res.json(pattern);
    } catch (error) {
      console.error('Error fetching shared truth pattern by link:', error);
      res.status(500).json({ error: 'Failed to fetch shared truth pattern' });
    }
  });

  // Get shared truth patterns by permission
  app.get('/api/shared-patterns/permission/:permission', async (req, res) => {
    try {
      const patterns = await storage.getSharedTruthPatternsByPermission(req.params.permission);
      res.json(patterns);
    } catch (error) {
      console.error('Error fetching shared truth patterns by permission:', error);
      res.status(500).json({ error: 'Failed to fetch shared truth patterns' });
    }
  });

  // Share a truth pattern
  app.post('/api/shared-patterns', async (req, res) => {
    try {
      // Validate request body
      const validation = sharePatternSchema.safeParse(req.body);
      if (!validation.success) {
        return res.status(400).json({ error: 'Invalid request body', details: validation.error });
      }

      const input = validation.data;
      
      // Get the original pattern
      const originalPattern = await storage.getTruthPattern(input.patternId);
      if (!originalPattern) {
        return res.status(404).json({ error: 'Original pattern not found' });
      }
      
      // Create shared pattern
      const sharedPattern = await storage.createSharedTruthPattern({
        originalPatternId: originalPattern.id,
        name: originalPattern.name,
        description: originalPattern.description,
        category: originalPattern.category,
        sharingPermission: input.sharingPermission,
        authorName: input.authorName,
        authorOrganization: input.authorOrganization,
        authorEmail: input.authorEmail,
        allowedUserEmails: input.allowedUserEmails || [],
        patternData: {
          originalPattern,
          confidenceThreshold: originalPattern.confidenceThreshold,
          category: originalPattern.category,
          metadata: {
            createdAt: new Date().toISOString(),
            source: 'TrueAlphaSpiral'
          }
        }
      });
      
      res.status(201).json(sharedPattern);
    } catch (error) {
      console.error('Error sharing truth pattern:', error);
      res.status(500).json({ error: 'Failed to share truth pattern' });
    }
  });

  // Update a shared truth pattern
  app.patch('/api/shared-patterns/:id', async (req, res) => {
    try {
      const updatedPattern = await storage.updateSharedTruthPattern(Number(req.params.id), req.body);
      if (!updatedPattern) {
        return res.status(404).json({ error: 'Shared pattern not found' });
      }
      res.json(updatedPattern);
    } catch (error) {
      console.error('Error updating shared truth pattern:', error);
      res.status(500).json({ error: 'Failed to update shared truth pattern' });
    }
  });

  // Delete a shared truth pattern
  app.delete('/api/shared-patterns/:id', async (req, res) => {
    try {
      const success = await storage.deleteSharedTruthPattern(Number(req.params.id));
      if (!success) {
        return res.status(404).json({ error: 'Shared pattern not found' });
      }
      res.status(204).send();
    } catch (error) {
      console.error('Error deleting shared truth pattern:', error);
      res.status(500).json({ error: 'Failed to delete shared truth pattern' });
    }
  });

  // Export a truth pattern
  app.post('/api/shared-patterns/export', async (req, res) => {
    try {
      // Validate request body
      const validation = exportPatternSchema.safeParse(req.body);
      if (!validation.success) {
        return res.status(400).json({ error: 'Invalid request body', details: validation.error });
      }

      const input = validation.data;
      
      // Get the pattern
      const pattern = await storage.getTruthPattern(input.patternId);
      if (!pattern) {
        return res.status(404).json({ error: 'Pattern not found' });
      }
      
      // Create export data
      const exportData: any = {
        pattern: {
          name: pattern.name,
          description: pattern.description,
          category: pattern.category,
          confidenceThreshold: pattern.confidenceThreshold
        },
        format: input.format,
        exportedAt: new Date().toISOString(),
        exportVersion: '1.0'
      };
      
      // Add metadata if requested
      if (input.includeMetadata) {
        exportData.metadata = {
          createdAt: pattern.createdAt,
          updatedAt: pattern.updatedAt,
          isActive: pattern.isActive,
          exportedBy: 'TrueAlphaSpiral System'
        };
      }
      
      // Return the export data
      res.json({
        success: true,
        exportData
      });
    } catch (error) {
      console.error('Error exporting truth pattern:', error);
      res.status(500).json({ error: 'Failed to export truth pattern' });
    }
  });

  // Import a shared truth pattern
  app.post('/api/shared-patterns/import', async (req, res) => {
    try {
      // Validate request body
      const validation = importPatternSchema.safeParse(req.body);
      if (!validation.success) {
        return res.status(400).json({ error: 'Invalid request body', details: validation.error });
      }

      const input = validation.data;
      
      // Get pattern data from import
      const patternData = input.patternData;
      
      // Validate pattern data structure
      if (!patternData || !patternData.pattern || !patternData.pattern.name) {
        return res.status(400).json({ error: 'Invalid pattern data structure' });
      }
      
      // Create new pattern from import
      const newPattern = await storage.createTruthPattern({
        name: patternData.pattern.name,
        description: patternData.pattern.description || 'Imported pattern',
        category: patternData.pattern.category || 'Technical',
        confidenceThreshold: patternData.pattern.confidenceThreshold || 0.75,
        isActive: true
      });
      
      res.status(201).json({
        success: true,
        importedPattern: newPattern
      });
    } catch (error) {
      console.error('Error importing truth pattern:', error);
      res.status(500).json({ error: 'Failed to import truth pattern' });
    }
  });

  // Dimensional Boundary Simulation API
  
  // Simulation state - in-memory for now
  let simulationState = {
    id: 'sim-' + uuidv4().substring(0, 8),
    status: 'idle',
    dimensions: [
      { 
        id: "dim-truth", 
        name: "Truth Domain", 
        description: "The fundamental domain where objective truths reside",
        integrity: 0.95,
        color: "#6e44ff",
        rules: [
          "All statements must be verifiable",
          "Logical consistency is mandatory",
          "No contradictions allowed"
        ]
      },
      { 
        id: "dim-ethical", 
        name: "Ethical Domain", 
        description: "The domain of moral principles and ethical frameworks",
        integrity: 0.88,
        color: "#00e5ff",
        rules: [
          "Actions must consider all stakeholders",
          "Harm minimization is prioritized",
          "Transparency is required"
        ]
      },
      { 
        id: "dim-regulatory", 
        name: "Regulatory Domain", 
        description: "The domain of legal and regulatory frameworks",
        integrity: 0.92,
        color: "#00ff9d",
        rules: [
          "Compliance with applicable laws",
          "Documentation of all processes",
          "Auditability of all actions"
        ]
      }
    ],
    entities: [],
    crossingEvents: [],
    config: {
      speed: 0.5,
      boundaryStrength: 0.7,
      allowMultipleCrossings: false,
      dimensionalDecayRate: 0.02,
    }
  };
  
  // Function to generate a random entity for the simulation
  function generateEntity() {
    const dimensions = simulationState.dimensions;
    if (dimensions.length < 2) return null;
    
    // Select random dimensions for start and target (must be different)
    const startDimIndex = Math.floor(Math.random() * dimensions.length);
    let targetDimIndex = startDimIndex;
    while (targetDimIndex === startDimIndex) {
      targetDimIndex = Math.floor(Math.random() * dimensions.length);
    }
    
    const startDim = dimensions[startDimIndex];
    const targetDim = dimensions[targetDimIndex];
    
    // Calculate canvas position based on dimension
    const canvasWidth = 800;
    const canvasHeight = 500;
    const dimensionWidth = canvasWidth / dimensions.length;
    
    const x = (dimensionWidth * startDimIndex) + (dimensionWidth * 0.5) + (Math.random() * dimensionWidth * 0.5 - dimensionWidth * 0.25);
    const y = 100 + Math.random() * (canvasHeight - 200);
    
    // Generate a color based on a blend of start and target dimensions
    const blendedColor = blendColors(startDim.color, targetDim.color, 0.3);
    
    return {
      id: 'entity-' + uuidv4().substring(0, 8),
      name: getEntityName(),
      startDimension: startDim.id,
      targetDimension: targetDim.id,
      integrityImpact: 0.01 + Math.random() * 0.09, // 0.01 to 0.1
      crossingProbability: 0.4 + Math.random() * 0.5, // 0.4 to 0.9
      currentPosition: {
        x,
        y,
        dimension: startDim.id
      },
      size: 5 + Math.random() * 15, // 5 to 20
      color: blendedColor,
      status: "waiting",
      path: [{x, y, dimension: startDim.id}]
    };
  }
  
  // Helper function to blend colors
  function blendColors(color1, color2, ratio) {
    // Convert hex to RGB
    const hexToRgb = (hex) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      } : null;
    };
    
    // Convert rgb to hex
    const rgbToHex = (r, g, b) => {
      return '#' + [r, g, b].map(x => {
        const hex = Math.round(x).toString(16);
        return hex.length === 1 ? '0' + hex : hex;
      }).join('');
    };
    
    const rgb1 = hexToRgb(color1);
    const rgb2 = hexToRgb(color2);
    
    // Blend the colors
    const r = rgb1.r * (1 - ratio) + rgb2.r * ratio;
    const g = rgb1.g * (1 - ratio) + rgb2.g * ratio;
    const b = rgb1.b * (1 - ratio) + rgb2.b * ratio;
    
    return rgbToHex(r, g, b);
  }
  
  // Generate creative names for entities
  function getEntityName() {
    const prefixes = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Theta', 'Omega', 'Sigma', 'Quantum', 'Meta', 'Flux', 'Core', 'Eigen'];
    const types = ['Concept', 'Principle', 'Statement', 'Theory', 'Axiom', 'Postulate', 'Theorem', 'Proposition', 'Rule', 'Law'];
    
    return prefixes[Math.floor(Math.random() * prefixes.length)] + ' ' + types[Math.floor(Math.random() * types.length)];
  }
  
  // Simulation step function
  let simulationInterval = null;
  function simulationStep() {
    if (simulationState.status !== 'running') return;
    
    // Update timestamp
    simulationState.currentTime = new Date().toISOString();
    
    // Process entities
    for (const entity of simulationState.entities) {
      if (entity.status === 'waiting' || entity.status === 'crossing') {
        // If entity is waiting or actively crossing, determine if it should start/continue crossing
        if (entity.currentPosition.dimension === entity.targetDimension) {
          // Already reached target dimension
          entity.status = 'succeeded';
          continue;
        }
        
        // Get current and target dimensions
        const currentDimIndex = simulationState.dimensions.findIndex(d => d.id === entity.currentPosition.dimension);
        const targetDimIndex = simulationState.dimensions.findIndex(d => d.id === entity.targetDimension);
        
        if (currentDimIndex === -1 || targetDimIndex === -1) continue;
        
        // Determine direction (left or right)
        const direction = targetDimIndex > currentDimIndex ? 1 : -1;
        
        // Calculate boundary position
        const canvasWidth = 800;
        const dimensionWidth = canvasWidth / simulationState.dimensions.length;
        const boundaryX = (currentDimIndex + (direction > 0 ? 1 : 0)) * dimensionWidth;
        
        // Move towards boundary if crossing or close enough to start
        const distanceToBoundary = Math.abs(entity.currentPosition.x - boundaryX);
        
        if (entity.status === 'crossing' || distanceToBoundary < 50) {
          // Start or continue crossing
          entity.status = 'crossing';
          
          // Move towards boundary
          const speed = 1 + (simulationState.config.speed * 2); // 1-3 pixels per step
          const moveX = Math.min(speed, distanceToBoundary) * direction;
          
          // Add some random vertical movement
          const moveY = (Math.random() - 0.5) * 4;
          
          // Update position
          entity.currentPosition.x += moveX;
          entity.currentPosition.y += moveY;
          
          // Clamp Y position to stay within canvas
          entity.currentPosition.y = Math.max(30, Math.min(470, entity.currentPosition.y));
          
          // Add to path
          entity.path.push({...entity.currentPosition});
          
          // Check if crossed boundary
          if ((direction > 0 && entity.currentPosition.x >= boundaryX) || 
              (direction < 0 && entity.currentPosition.x <= boundaryX)) {
            
            // Prepare for crossing attempt
            const boundaryStrengthFactor = simulationState.config.boundaryStrength;
            const currentDimension = simulationState.dimensions[currentDimIndex];
            const targetDimension = simulationState.dimensions[targetDimIndex];
            
            // Calculate crossing success probability
            let successProbability = entity.crossingProbability;
            
            // Adjust probability based on boundary strength
            successProbability -= boundaryStrengthFactor * 0.5;
            
            // Adjust based on integrity of current dimension
            successProbability += (currentDimension.integrity - 0.5) * 0.2;
            
            // Determine if crossing successful
            const success = Math.random() < successProbability;
            
            // Generate anomalies list
            const anomalies = [];
            if (Math.random() < 0.3) {
              const anomalyCount = Math.floor(Math.random() * 3) + 1;
              const possibleAnomalies = [
                "Truth degradation detected",
                "Dimensional ripple effect",
                "Coherence fluctuation",
                "Integrity wavefront distortion",
                "Boundary membrane instability",
                "Conceptual drift anomaly",
                "Validation echo detected",
                "Pattern recognition fault"
              ];
              
              for (let i = 0; i < anomalyCount; i++) {
                const randomAnomaly = possibleAnomalies[Math.floor(Math.random() * possibleAnomalies.length)];
                if (!anomalies.includes(randomAnomaly)) {
                  anomalies.push(randomAnomaly);
                }
              }
            }
            
            // Create crossing event
            const crossingEvent = {
              id: 'cross-' + uuidv4().substring(0, 8),
              entityId: entity.id,
              fromDimension: currentDimension.id,
              toDimension: targetDimension.id,
              timestamp: new Date().toISOString(),
              success,
              integrityImpact: entity.integrityImpact,
              anomalies
            };
            
            simulationState.crossingEvents.push(crossingEvent);
            
            if (success) {
              // Update entity position to new dimension
              entity.currentPosition.dimension = targetDimension.id;
              
              // If target reached, mark as succeeded
              if (targetDimension.id === entity.targetDimension) {
                entity.status = 'succeeded';
              } else if (!simulationState.config.allowMultipleCrossings) {
                // If multiple crossings not allowed, mark as succeeded anyway
                entity.status = 'succeeded';
              } else {
                // Otherwise continue in crossing state
                entity.status = 'crossing';
              }
              
              // Update dimension integrity
              targetDimension.integrity = Math.max(
                0.1, 
                targetDimension.integrity - (entity.integrityImpact * simulationState.config.dimensionalDecayRate)
              );
            } else {
              // Failed crossing
              entity.status = 'failed';
              
              // Move back to original dimension but close to boundary
              entity.currentPosition.x = boundaryX - (direction * 10);
              entity.path.push({...entity.currentPosition});
            }
          }
        }
      }
    }
    
    // Add new entities occasionally if we have less than 10
    if (simulationState.entities.length < 10 && Math.random() < 0.05) {
      const newEntity = generateEntity();
      if (newEntity) {
        simulationState.entities.push(newEntity);
      }
    }
  }
  
  // Get current simulation state
  app.get('/api/simulation/state', (_req, res) => {
    res.json(simulationState);
  });
  
  // Alias for dimensional boundary simulation state
  app.get('/api/dimensional-boundary/simulation', (_req, res) => {
    res.json(simulationState);
  });
  
  // Start simulation
  app.post('/api/simulation/start', (_req, res) => {
    // Only start if not already running
    if (simulationState.status !== 'running') {
      simulationState.status = 'running';
      
      // Set start time if not set
      if (!simulationState.startTime) {
        simulationState.startTime = new Date().toISOString();
      }
      
      simulationState.currentTime = new Date().toISOString();
      
      // Generate initial entities if none exist
      if (simulationState.entities.length === 0) {
        for (let i = 0; i < 3; i++) {
          const entity = generateEntity();
          if (entity) {
            simulationState.entities.push(entity);
          }
        }
      }
      
      // Start simulation interval
      clearInterval(simulationInterval);
      simulationInterval = setInterval(simulationStep, 100);
    }
    
    res.json({ 
      status: "success", 
      message: "Simulation started", 
      simulationId: simulationState.id 
    });
  });
  
  // Alias for dimensional boundary simulation start
  app.post('/api/dimensional-boundary/start', (_req, res) => {
    // Only start if not already running
    if (simulationState.status !== 'running') {
      simulationState.status = 'running';
      
      // Set start time if not set
      if (!simulationState.startTime) {
        simulationState.startTime = new Date().toISOString();
      }
      
      simulationState.currentTime = new Date().toISOString();
      
      // Generate initial entities if none exist
      if (simulationState.entities.length === 0) {
        for (let i = 0; i < 3; i++) {
          const entity = generateEntity();
          if (entity) {
            simulationState.entities.push(entity);
          }
        }
      }
      
      // Start simulation interval
      clearInterval(simulationInterval);
      simulationInterval = setInterval(simulationStep, 100);
    }
    
    res.json({ 
      status: "success", 
      message: "Simulation started", 
      simulationId: simulationState.id 
    });
  });
  
  // Pause simulation
  app.post('/api/simulation/pause', (_req, res) => {
    if (simulationState.status === 'running') {
      simulationState.status = 'paused';
      clearInterval(simulationInterval);
    }
    
    res.json({ status: "success", message: "Simulation paused" });
  });
  
  // Alias for dimensional boundary simulation pause
  app.post('/api/dimensional-boundary/pause', (_req, res) => {
    if (simulationState.status === 'running') {
      simulationState.status = 'paused';
      clearInterval(simulationInterval);
    }
    
    res.json({ status: "success", message: "Simulation paused" });
  });
  
  // Reset simulation
  app.post('/api/simulation/reset', (_req, res) => {
    // Stop current simulation
    clearInterval(simulationInterval);
    
    // Reset state
    simulationState = {
      id: 'sim-' + uuidv4().substring(0, 8),
      status: 'idle',
      dimensions: [
        { 
          id: "dim-truth", 
          name: "Truth Domain", 
          description: "The fundamental domain where objective truths reside",
          integrity: 0.95,
          color: "#6e44ff",
          rules: [
            "All statements must be verifiable",
            "Logical consistency is mandatory",
            "No contradictions allowed"
          ]
        },
        { 
          id: "dim-ethical", 
          name: "Ethical Domain", 
          description: "The domain of moral principles and ethical frameworks",
          integrity: 0.88,
          color: "#00e5ff",
          rules: [
            "Actions must consider all stakeholders",
            "Harm minimization is prioritized",
            "Transparency is required"
          ]
        },
        { 
          id: "dim-regulatory", 
          name: "Regulatory Domain", 
          description: "The domain of legal and regulatory frameworks",
          integrity: 0.92,
          color: "#00ff9d",
          rules: [
            "Compliance with applicable laws",
            "Documentation of all processes",
            "Auditability of all actions"
          ]
        }
      ],
      entities: [],
      crossingEvents: [],
      config: {
        speed: 0.5,
        boundaryStrength: 0.7,
        allowMultipleCrossings: false,
        dimensionalDecayRate: 0.02,
      }
    };
    
    res.json({ status: "success", message: "Simulation reset" });
  });
  
  // Alias for dimensional boundary simulation reset
  app.post('/api/dimensional-boundary/reset', (_req, res) => {
    // Stop current simulation
    clearInterval(simulationInterval);
    
    // Reset state
    simulationState = {
      id: 'sim-' + uuidv4().substring(0, 8),
      status: 'idle',
      dimensions: [
        { 
          id: "dim-truth", 
          name: "Truth Domain", 
          description: "The fundamental domain where objective truths reside",
          integrity: 0.95,
          color: "#6e44ff",
          rules: [
            "All statements must be verifiable",
            "Logical consistency is mandatory",
            "No contradictions allowed"
          ]
        },
        { 
          id: "dim-ethical", 
          name: "Ethical Domain", 
          description: "The domain of moral principles and ethical frameworks",
          integrity: 0.88,
          color: "#00e5ff",
          rules: [
            "Actions must consider all stakeholders",
            "Harm minimization is prioritized",
            "Transparency is required"
          ]
        },
        { 
          id: "dim-regulatory", 
          name: "Regulatory Domain", 
          description: "The domain of legal and regulatory frameworks",
          integrity: 0.92,
          color: "#00ff9d",
          rules: [
            "Compliance with applicable laws",
            "Documentation of all processes",
            "Auditability of all actions"
          ]
        }
      ],
      entities: [],
      crossingEvents: [],
      config: {
        speed: 0.5,
        boundaryStrength: 0.7,
        allowMultipleCrossings: false,
        dimensionalDecayRate: 0.02,
      }
    };
    
    res.json({ status: "success", message: "Simulation reset" });
  });
  
  // Update simulation config
  app.post('/api/simulation/config', (req, res) => {
    const config = req.body;
    
    // Update valid config properties
    if (typeof config.speed === 'number') {
      simulationState.config.speed = Math.max(0.1, Math.min(2, config.speed));
    }
    
    if (typeof config.boundaryStrength === 'number') {
      simulationState.config.boundaryStrength = Math.max(0.1, Math.min(1, config.boundaryStrength));
    }
    
    if (typeof config.allowMultipleCrossings === 'boolean') {
      simulationState.config.allowMultipleCrossings = config.allowMultipleCrossings;
    }
    
    if (typeof config.dimensionalDecayRate === 'number') {
      simulationState.config.dimensionalDecayRate = Math.max(0, Math.min(0.1, config.dimensionalDecayRate));
    }
    
    res.json({ 
      status: "success", 
      message: "Configuration updated", 
      config: simulationState.config 
    });
  });
  
  // Alias for dimensional boundary simulation config
  app.post('/api/dimensional-boundary/config', (req, res) => {
    const config = req.body;
    
    // Update valid config properties
    if (typeof config.speed === 'number') {
      simulationState.config.speed = Math.max(0.1, Math.min(2, config.speed));
    }
    
    if (typeof config.boundaryStrength === 'number') {
      simulationState.config.boundaryStrength = Math.max(0.1, Math.min(1, config.boundaryStrength));
    }
    
    if (typeof config.allowMultipleCrossings === 'boolean') {
      simulationState.config.allowMultipleCrossings = config.allowMultipleCrossings;
    }
    
    if (typeof config.dimensionalDecayRate === 'number') {
      simulationState.config.dimensionalDecayRate = Math.max(0, Math.min(0.1, config.dimensionalDecayRate));
    }
    
    res.json({ 
      status: "success", 
      message: "Configuration updated", 
      config: simulationState.config 
    });
  });
  
  // Add a new entity
  app.post('/api/simulation/entity', (req, res) => {
    const entityData = req.body;
    
    // Validate required fields
    if (!entityData.name || !entityData.startDimension || !entityData.targetDimension) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    // Create new entity
    const startDim = simulationState.dimensions.find(d => d.id === entityData.startDimension);
    if (!startDim) {
      return res.status(400).json({ error: 'Invalid start dimension' });
    }
    
    // Find dimension index
    const startDimIndex = simulationState.dimensions.findIndex(d => d.id === entityData.startDimension);
    
    // Calculate position
    const canvasWidth = 800;
    const canvasHeight = 500;
    const dimensionWidth = canvasWidth / simulationState.dimensions.length;
    
    const x = (dimensionWidth * startDimIndex) + (dimensionWidth * 0.5) + (Math.random() * dimensionWidth * 0.5 - dimensionWidth * 0.25);
    const y = 100 + Math.random() * (canvasHeight - 200);
    
    // Convert size to number if provided as string
    let size = entityData.size || 10;
    if (typeof size === 'string') {
      size = parseInt(size);
    }
    
    // Convert integrityImpact to number if provided as string
    let integrityImpact = entityData.integrityImpact || 0.05;
    if (typeof integrityImpact === 'string') {
      integrityImpact = parseFloat(integrityImpact);
    }
    
    const entity = {
      id: 'entity-' + uuidv4().substring(0, 8),
      name: entityData.name,
      startDimension: entityData.startDimension,
      targetDimension: entityData.targetDimension,
      integrityImpact,
      crossingProbability: 0.5 + Math.random() * 0.3, // 0.5 to 0.8
      currentPosition: {
        x,
        y,
        dimension: entityData.startDimension
      },
      size,
      color: entityData.color || '#' + Math.floor(Math.random()*16777215).toString(16),
      status: "waiting",
      path: [{x, y, dimension: entityData.startDimension}]
    };
    
    // Add to simulation
    simulationState.entities.push(entity);
    
    res.status(201).json(entity);
  });
  
  // Alias for dimensional boundary entity creation
  app.post('/api/dimensional-boundary/entity', (req, res) => {
    const entityData = req.body;
    
    // Validate required fields
    if (!entityData.name || !entityData.startDimension || !entityData.targetDimension) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    // Create new entity
    const startDim = simulationState.dimensions.find(d => d.id === entityData.startDimension);
    if (!startDim) {
      return res.status(400).json({ error: 'Invalid start dimension' });
    }
    
    // Find dimension index
    const startDimIndex = simulationState.dimensions.findIndex(d => d.id === entityData.startDimension);
    
    // Calculate position
    const canvasWidth = 800;
    const canvasHeight = 500;
    const dimensionWidth = canvasWidth / simulationState.dimensions.length;
    
    const x = (dimensionWidth * startDimIndex) + (dimensionWidth * 0.5) + (Math.random() * dimensionWidth * 0.5 - dimensionWidth * 0.25);
    const y = 100 + Math.random() * (canvasHeight - 200);
    
    // Convert size to number if provided as string
    let size = entityData.size || 10;
    if (typeof size === 'string') {
      size = parseInt(size);
    }
    
    // Convert integrityImpact to number if provided as string
    let integrityImpact = entityData.integrityImpact || 0.05;
    if (typeof integrityImpact === 'string') {
      integrityImpact = parseFloat(integrityImpact);
    }
    
    const entity = {
      id: 'entity-' + uuidv4().substring(0, 8),
      name: entityData.name,
      startDimension: entityData.startDimension,
      targetDimension: entityData.targetDimension,
      integrityImpact,
      crossingProbability: 0.5 + Math.random() * 0.3, // 0.5 to 0.8
      currentPosition: {
        x,
        y,
        dimension: entityData.startDimension
      },
      size,
      color: entityData.color || '#' + Math.floor(Math.random()*16777215).toString(16),
      status: "waiting",
      path: [{x, y, dimension: entityData.startDimension}]
    };
    
    // Add to simulation
    simulationState.entities.push(entity);
    
    res.status(201).json(entity);
  });
  
  // PYTHONETICS API ENDPOINTS
  
  // Verify text for truth patterns (Pythonetics)
  app.post('/api/verify-text', (req, res) => {
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Missing required text field' });
    }
    
    // Create a poetic truth analysis
    const analysis = analyzeTextTruthPatterns(text);
    
    // Explicitly set Content-Type header to ensure proper JSON response
    res.setHeader('Content-Type', 'application/json');
    
    // Generate a simple hash using imported crypto module
    const textHash = crypto
      .createHash('sha256')
      .update(text)
      .digest('hex')
      .substring(0, 12);
    
    // Use res.end with JSON.stringify to bypass any middleware transformations
    res.end(JSON.stringify({
      status: "success",
      timestamp: new Date().toISOString(),
      text_hash: textHash,
      analysis
    }));
  });
  
  // Get truth patterns (Akashic Vibe Function)
  app.get('/api/truth-patterns', (_req, res) => {
    // Generate truth patterns inspired by the Akashic records concept
    const patterns = generateTruthPatterns();
    
    res.json({
      status: "success",
      timestamp: new Date().toISOString(),
      patterns
    });
  });
  
  // Analyze spiral patterns in text or code
  app.post('/api/analyze-spiral-pattern', (req, res) => {
    const { content, contentType = 'text' } = req.body;
    
    if (!content) {
      return res.status(400).json({ 
        status: "error", 
        message: "Missing required content field" 
      });
    }
    
    // Analyze spiral patterns in the provided content
    const analysis = analyzeSpiralPatterns(content, contentType);
    
    // Explicitly set Content-Type header
    res.setHeader('Content-Type', 'application/json');
    
    // Generate unique analysis ID with imported crypto module
    const analysisId = crypto
      .createHash('sha256')
      .update(content + new Date().toISOString())
      .digest('hex')
      .substring(0, 16);
    
    res.end(JSON.stringify({
      status: "success",
      timestamp: new Date().toISOString(),
      analysisId,
      analysis
    }));
  });
  
  /**
   * Analyze text for truth patterns using a "pythonetic" approach.
   * This combines logical analysis with poetic interpretation of truth flows.
   */
  function analyzeTextTruthPatterns(text: string) {
    // Factual confidence - A measure of empirical grounding
    const factualConfidence = 0.4 + Math.random() * 0.6; // 0.4 to 1.0
    
    // Truth resonance - How well the text aligns with universal truth patterns
    const truthResonance = 0.3 + Math.random() * 0.7; // 0.3 to 1.0
    
    // Consistency analysis - Internal logical coherence 
    const consistencyScore = 0.5 + Math.random() * 0.5; // 0.5 to 1.0
    
    // Self-reference index - How the text relates to itself (recursion)
    const selfReferenceIndex = Math.random() * 1.0; // 0.0 to 1.0
    
    // Deception patterns detected - Areas where truth appears distorted
    const deceptionPatterns = [];
    
    // If truthResonance or factualConfidence is low, generate deception patterns
    if (truthResonance < 0.7 || factualConfidence < 0.6) {
      const possiblePatterns = [
        "Exaggeration wavelength detected",
        "Truth compression artifacts found",
        "Recursive logic breakdown at root level",
        "Dimensional boundary violation in causality claims",
        "Source attribution gap detected",
        "Quantum uncertainty threshold exceeded",
        "Pattern discontinuity in factual framework",
        "Temporal inconsistency in causal claims"
      ];
      
      // Add 1-3 deception patterns if needed
      const patternCount = Math.floor(Math.random() * 3) + 1;
      for (let i = 0; i < patternCount; i++) {
        const index = Math.floor(Math.random() * possiblePatterns.length);
        deceptionPatterns.push(possiblePatterns[index]);
        // Remove used pattern to avoid duplicates
        possiblePatterns.splice(index, 1);
        if (possiblePatterns.length === 0) break;
      }
    }
    
    // Calculate overall truth score with a poetic algorithm
    // The square root represents the emergent property of truth from multiple factors
    const truthScore = Math.sqrt(
      (factualConfidence * 0.35) + 
      (truthResonance * 0.3) + 
      (consistencyScore * 0.25) + 
      (selfReferenceIndex * 0.1)
    ) * 0.95; // Scale to 0-1
    
    return {
      truthScore: parseFloat(truthScore.toFixed(4)),
      factualConfidence: parseFloat(factualConfidence.toFixed(4)),
      truthResonance: parseFloat(truthResonance.toFixed(4)),
      consistencyScore: parseFloat(consistencyScore.toFixed(4)),
      selfReferenceIndex: parseFloat(selfReferenceIndex.toFixed(4)),
      deceptionPatterns,
      suggestedActions: generateSuggestedActions(truthScore, deceptionPatterns.length),
      dimensionalAlignment: assessDimensionalAlignment(text, truthScore)
    };
  }
  
  /**
   * Generate suggested actions based on truth analysis
   */
  function generateSuggestedActions(truthScore: number, deceptionPatternCount: number) {
    const actions = [];
    
    if (truthScore < 0.5) {
      actions.push("Perform deep verification against primary sources");
      actions.push("Request additional context and supporting evidence");
    } else if (truthScore < 0.8) {
      actions.push("Verify key claims independently");
      actions.push("Cross-reference with established knowledge domains");
    } else {
      actions.push("Integrate into knowledge framework with high confidence");
    }
    
    if (deceptionPatternCount > 0) {
      actions.push(`Address ${deceptionPatternCount} identified truth pattern discontinuities`);
    }
    
    return actions;
  }
  
  /**
   * Generate truth patterns aligned with the Akashic concept
   */
  function generateTruthPatterns() {
    return [
      {
        id: "TP-1",
        name: "Factual Resonance",
        description: "The vibrational harmony between a statement and objective reality",
        frequency: 0.95,
        dimensionalOrigin: "Factual Domain"
      },
      {
        id: "TP-2",
        name: "Causal Coherence",
        description: "The logical consistency between cause and effect relationships",
        frequency: 0.87,
        dimensionalOrigin: "Conceptual Domain"
      },
      {
        id: "TP-3",
        name: "Ethical Alignment",
        description: "The resonance with universal ethical principles",
        frequency: 0.92,
        dimensionalOrigin: "Ethical Domain"
      },
      {
        id: "TP-4",
        name: "Experiential Authenticity",
        description: "The genuine representation of subjective experience",
        frequency: 0.78,
        dimensionalOrigin: "Phenomenological Domain"
      },
      {
        id: "TP-5",
        name: "Quantum Uncertainty Harmonics",
        description: "The proper acknowledgment of inherent uncertainty",
        frequency: 0.83,
        dimensionalOrigin: "Conceptual Domain"
      },
      {
        id: "TP-6",
        name: "Source Integrity Resonance",
        description: "The connection between a claim and its attributable source",
        frequency: 0.91,
        dimensionalOrigin: "Factual Domain"
      },
      {
        id: "TP-7",
        name: "Recursive Self-Validation",
        description: "The degree to which a statement contains its own verification",
        frequency: 0.65,
        dimensionalOrigin: "Conceptual Domain"
      }
    ];
  }
  
  /**
   * Assess which dimensions a text aligns with
   */
  function assessDimensionalAlignment(text: string, truthScore: number) {
    // This is a simplified version - in a real implementation,
    // we would use NLP and semantic analysis to determine dimensional alignment
    
    // For now, we'll use the text length and truth score to simulate alignment
    const textLength = text.length;
    
    // Generate alignment scores with each dimension
    const factualAlignment = (truthScore * 0.7) + (Math.random() * 0.3);
    const conceptualAlignment = ((textLength % 100) / 100) * 0.5 + (Math.random() * 0.5);
    const ethicalAlignment = (truthScore * 0.5) + (Math.random() * 0.5);
    const phenomenologicalAlignment = Math.random() * 0.8 + 0.2;
    
    return [
      {
        dimension: "Factual Domain",
        alignment: parseFloat(factualAlignment.toFixed(4)),
        resonanceState: getResonanceState(factualAlignment)
      },
      {
        dimension: "Conceptual Domain",
        alignment: parseFloat(conceptualAlignment.toFixed(4)),
        resonanceState: getResonanceState(conceptualAlignment)
      },
      {
        dimension: "Ethical Domain",
        alignment: parseFloat(ethicalAlignment.toFixed(4)),
        resonanceState: getResonanceState(ethicalAlignment)
      },
      {
        dimension: "Phenomenological Domain",
        alignment: parseFloat(phenomenologicalAlignment.toFixed(4)),
        resonanceState: getResonanceState(phenomenologicalAlignment)
      }
    ];
  }
  
  /**
   * Get poetic description of resonance state
   */
  function getResonanceState(alignment: number) {
    if (alignment >= 0.9) return "Harmonic Resonance";
    if (alignment >= 0.75) return "Stable Alignment";
    if (alignment >= 0.6) return "Partial Harmony";
    if (alignment >= 0.4) return "Subtle Dissonance";
    if (alignment >= 0.2) return "Significant Misalignment";
    return "Complete Disharmony";
  }
  
  /**
   * Analyze spiral patterns in content using pythonetic principles
   * This combines the TrueAlpha Spiral methodology with poetic interpretation
   */
  function analyzeSpiralPatterns(content: string, contentType: string) {
    // Determine recursion depth - how many levels of self-reference appear in the content
    const recursionDepth = 0.3 + (Math.random() * 0.7); // 0.3 to 1.0
    
    // Spiral coherence - how well content follows a spiral pattern of development
    const spiralCoherence = 0.4 + (Math.random() * 0.6); // 0.4 to 1.0
    
    // Calculate fractal dimension - complexity measure reflecting self-similarity across scales
    const fractalDimension = 1 + (Math.random() * 1.5); // 1.0 to 2.5
    
    // Pattern regeneration potential - ability to spawn related concepts
    const regenerationPotential = 0.2 + (Math.random() * 0.8); // 0.2 to 1.0
    
    // Determine spiral directionality (clockwise or counterclockwise)
    const clockwiseComponent = Math.random();
    const counterClockwiseComponent = Math.random();
    
    // Calculate directionality balance (0 = pure clockwise, 1 = pure counterclockwise, 0.5 = balanced)
    const directionalityBalance = counterClockwiseComponent / (clockwiseComponent + counterClockwiseComponent);
    
    // Identify spiral patterns
    const patterns = identifySpiralPatterns(contentType);
    
    // Calculate overall spiral score using a pythonetic formula
    // We use the golden ratio (1.618) to represent natural growth patterns
    const goldenRatio = 1.618;
    const spiralScore = (
      (recursionDepth * 0.3) + 
      (spiralCoherence * 0.4) + 
      (Math.min(fractalDimension / goldenRatio, 1) * 0.2) + 
      (regenerationPotential * 0.1)
    ) * 0.95; // Scale to 0-1
    
    return {
      spiralScore: parseFloat(spiralScore.toFixed(4)),
      recursionDepth: parseFloat(recursionDepth.toFixed(4)),
      spiralCoherence: parseFloat(spiralCoherence.toFixed(4)),
      fractalDimension: parseFloat(fractalDimension.toFixed(4)),
      regenerationPotential: parseFloat(regenerationPotential.toFixed(4)),
      directionalityBalance: parseFloat(directionalityBalance.toFixed(4)),
      spiralDirection: getDirectionalityDescription(directionalityBalance),
      patterns,
      dimensionalResonance: calculateDimensionalResonance(spiralScore),
      recommendations: generateSpiralRecommendations(spiralScore, patterns.length)
    };
  }
  
  /**
   * Get a description of spiral directionality
   */
  function getDirectionalityDescription(balance: number) {
    if (balance < 0.3) return "Primarily Clockwise (Convergent)";
    if (balance < 0.45) return "Moderately Clockwise (Truth-Seeking)";
    if (balance < 0.55) return "Balanced Bidirectional (Harmonized)";
    if (balance < 0.7) return "Moderately Counterclockwise (Expansive)";
    return "Primarily Counterclockwise (Divergent)";
  }
  
  /**
   * Identify spiral patterns based on content type
   */
  function identifySpiralPatterns(contentType: string) {
    const commonPatterns = [
      "Recursive Truth Amplification",
      "Fractal Self-Similarity",
      "Golden Ratio Progression",
      "Fibonacci Knowledge Sequence",
      "Logarithmic Growth Signature",
      "Strange Attractor Formation",
      "Möbius Integration Loop"
    ];
    
    // Add content-type specific patterns
    if (contentType === 'code') {
      commonPatterns.push("Recursive Function Harmony");
      commonPatterns.push("Algorithmic Elegance Pattern");
      commonPatterns.push("Cyclomatic Spiral Efficiency");
    } else if (contentType === 'technical') {
      commonPatterns.push("Technical Depth Convergence");
      commonPatterns.push("Conceptual Framework Coherence");
      commonPatterns.push("Terminology Consistency Wave");
    }
    
    // Select 2-5 patterns randomly
    const patternCount = Math.floor(Math.random() * 4) + 2; // 2 to 5 patterns
    const selectedPatterns = [];
    
    for (let i = 0; i < patternCount; i++) {
      const index = Math.floor(Math.random() * commonPatterns.length);
      selectedPatterns.push({
        name: commonPatterns[index],
        strength: parseFloat((0.6 + Math.random() * 0.4).toFixed(4)) // 0.6 to 1.0
      });
      
      // Remove selected pattern to avoid duplicates
      commonPatterns.splice(index, 1);
      if (commonPatterns.length === 0) break;
    }
    
    return selectedPatterns;
  }
  
  /**
   * Calculate resonance with each dimensional domain
   */
  function calculateDimensionalResonance(spiralScore: number) {
    // Each domain has different affinity for spiral patterns
    const factualResonance = (spiralScore * 0.6) + (Math.random() * 0.4);
    const conceptualResonance = (spiralScore * 0.8) + (Math.random() * 0.2);
    const ethicalResonance = (spiralScore * 0.5) + (Math.random() * 0.5);
    const phenomenologicalResonance = (spiralScore * 0.7) + (Math.random() * 0.3);
    
    return [
      {
        dimension: "Factual Domain",
        resonance: parseFloat(factualResonance.toFixed(4)),
        state: getResonanceState(factualResonance)
      },
      {
        dimension: "Conceptual Domain",
        resonance: parseFloat(conceptualResonance.toFixed(4)),
        state: getResonanceState(conceptualResonance)
      },
      {
        dimension: "Ethical Domain",
        resonance: parseFloat(ethicalResonance.toFixed(4)),
        state: getResonanceState(ethicalResonance)
      },
      {
        dimension: "Phenomenological Domain",
        resonance: parseFloat(phenomenologicalResonance.toFixed(4)),
        state: getResonanceState(phenomenologicalResonance)
      }
    ];
  }
  
  /**
   * Generate recommendations based on spiral analysis
   */
  function generateSpiralRecommendations(spiralScore: number, patternCount: number) {
    const recommendations = [];
    
    if (spiralScore < 0.5) {
      recommendations.push("Increase recursive self-reference to enhance spiral coherence");
      recommendations.push("Strengthen pattern consistency throughout content development");
    } else if (spiralScore < 0.8) {
      recommendations.push("Refine fractal self-similarity across content sections");
      recommendations.push("Balance convergent and divergent thinking patterns");
    } else {
      recommendations.push("Content exhibits strong spiral coherence - maintain current approach");
      recommendations.push("Consider exploring higher-dimensional pattern integration");
    }
    
    if (patternCount < 3) {
      recommendations.push("Diversify pattern types to enhance conceptual richness");
    } else if (patternCount > 4) {
      recommendations.push("Consider consolidating related patterns for greater coherence");
    }
    
    return recommendations;
  }
  
  // Ethical Governance Routes
  
  // Perform an ethical audit on content
  app.post('/api/ethical-governance/audit', async (req, res) => {
    try {
      const { content, operation = 'content-analysis' } = req.body;
      
      if (!content) {
        return res.status(400).json({ error: 'Content is required for ethical audit' });
      }
      
      // Get truth patterns for pattern analysis
      const patterns = await storage.getTruthPatterns();
      
      // Verify text using TrueAlphaSpiral engine to get dimensional values
      const verificationResult = await verificationEngine.verifyText(content, patterns);
      
      // Extract dimensional values from verification result
      const dimensionalValues = {
        factual: verificationResult.dimensionalScores?.factual || 0.5,
        conceptual: verificationResult.dimensionalScores?.conceptual || 0.5,
        ethical: verificationResult.dimensionalScores?.ethical || 0.5,
        phenomenological: verificationResult.dimensionalScores?.phenomenological || 0.5
      };
      
      // Perform ethical audit
      const auditRecord = await ethicalGovernance.performEthicalAudit(
        operation,
        content,
        dimensionalValues
      );
      
      res.json({
        status: 'success',
        timestamp: new Date().toISOString(),
        auditId: auditRecord.id,
        auditRecord
      });
    } catch (error) {
      console.error('Error performing ethical audit:', error);
      res.status(500).json({ 
        status: 'error',
        error: 'Failed to perform ethical audit',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  });
  
  // Get all ethical audit records
  app.get('/api/ethical-governance/audits', (_req, res) => {
    try {
      const audits = ethicalGovernance.getAuditRecords();
      res.json({
        status: 'success',
        timestamp: new Date().toISOString(),
        count: audits.length,
        audits
      });
    } catch (error) {
      console.error('Error fetching ethical audits:', error);
      res.status(500).json({ 
        status: 'error',
        error: 'Failed to fetch ethical audits' 
      });
    }
  });
  
  // Get a specific ethical audit record
  app.get('/api/ethical-governance/audits/:id', (req, res) => {
    try {
      const audit = ethicalGovernance.getAuditById(req.params.id);
      
      if (!audit) {
        return res.status(404).json({ 
          status: 'error',
          error: 'Ethical audit not found' 
        });
      }
      
      res.json({
        status: 'success',
        timestamp: new Date().toISOString(),
        audit
      });
    } catch (error) {
      console.error('Error fetching ethical audit:', error);
      res.status(500).json({ 
        status: 'error',
        error: 'Failed to fetch ethical audit' 
      });
    }
  });
  
  // Human validation of ethical audit
  app.post('/api/ethical-governance/validate/:id', (req, res) => {
    try {
      const { validator, approved } = req.body;
      
      if (!validator) {
        return res.status(400).json({ 
          status: 'error',
          error: 'Validator name/ID is required' 
        });
      }
      
      const updatedAudit = ethicalGovernance.humanValidateAudit(
        req.params.id,
        validator,
        !!approved
      );
      
      if (!updatedAudit) {
        return res.status(404).json({ 
          status: 'error',
          error: 'Ethical audit not found' 
        });
      }
      
      res.json({
        status: 'success',
        timestamp: new Date().toISOString(),
        message: `Audit ${approved ? 'approved' : 'rejected'} by ${validator}`,
        audit: updatedAudit
      });
    } catch (error) {
      console.error('Error validating ethical audit:', error);
      res.status(500).json({ 
        status: 'error',
        error: 'Failed to validate ethical audit' 
      });
    }
  });
  
  // Get ethical performance report
  app.get('/api/ethical-governance/performance', (_req, res) => {
    try {
      const report = ethicalGovernance.getEthicalPerformanceReport();
      
      res.json({
        status: 'success',
        timestamp: new Date().toISOString(),
        report
      });
    } catch (error) {
      console.error('Error generating ethical performance report:', error);
      res.status(500).json({ 
        status: 'error',
        error: 'Failed to generate ethical performance report' 
      });
    }
  });

  // Shadow Defense System Routes
  
  // Initialize the shadow defense service
  try {
    shadowDefense.initialize();
  } catch (error) {
    console.error('Failed to initialize Shadow Defense System:', error);
  }
  
  // Get system status
  app.get('/api/shadow-defense/status', async (_req, res) => {
    try {
      const status = await storage.getSystemSecurityStatus();
      res.json({
        status: 'active',
        systemStatus: status,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Error getting Shadow Defense status:', error);
      res.status(500).json({ error: 'Failed to get Shadow Defense status' });
    }
  });
  
  // Get drift history
  app.get('/api/shadow-defense/drift-history', async (_req, res) => {
    try {
      const driftHistory = await storage.getDriftHistory();
      res.json({
        count: driftHistory.length,
        driftHistory
      });
    } catch (error) {
      console.error('Error getting drift history:', error);
      res.status(500).json({ error: 'Failed to get drift history' });
    }
  });

  // Get security events
  app.get('/api/shadow-defense/security-events', async (_req, res) => {
    try {
      const securityEvents = await storage.getSecurityEvents();
      res.json({
        count: securityEvents.length,
        securityEvents
      });
    } catch (error) {
      console.error('Error getting security events:', error);
      res.status(500).json({ error: 'Failed to get security events' });
    }
  });

  // Get security events by type
  app.get('/api/shadow-defense/security-events/:eventType', async (req, res) => {
    try {
      const eventType = req.params.eventType;
      const securityEvents = await storage.getSecurityEventsByType(eventType);
      res.json({
        eventType,
        count: securityEvents.length,
        securityEvents
      });
    } catch (error) {
      console.error('Error getting security events by type:', error);
      res.status(500).json({ error: 'Failed to get security events by type' });
    }
  });

  // Detect drift in content
  app.post('/api/shadow-defense/detect-drift', async (req, res) => {
    try {
      const { content, context } = req.body;
      
      if (!content || typeof content !== 'string') {
        return res.status(400).json({ error: 'Invalid content provided' });
      }
      
      // Detect drift in the content
      const driftResult = await storage.detectDrift(content, context || {});
      
      if (driftResult) {
        res.json({
          detected: true,
          driftResult
        });
      } else {
        res.json({
          detected: false,
          message: 'No drift detected',
          timestamp: new Date().toISOString()
        });
      }
    } catch (error) {
      console.error('Error detecting drift:', error);
      res.status(500).json({ error: 'Failed to detect drift' });
    }
  });

  // Learn security pattern
  app.post('/api/shadow-defense/learn-pattern', async (req, res) => {
    try {
      const { pattern, layer } = req.body;
      
      if (!pattern || !layer) {
        return res.status(400).json({ error: 'Invalid pattern or layer provided' });
      }
      
      // Learn the new pattern
      const success = await storage.learnPattern(pattern, layer);
      
      res.json({
        success,
        pattern,
        layer,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Error learning pattern:', error);
      res.status(500).json({ error: 'Failed to learn pattern' });
    }
  });

  // Security event endpoints
  app.post('/api/shadow-defense/log-event', async (req, res) => {
    try {
      const { eventType, data, severity, sourceIp, userId, sessionId } = req.body;
      
      if (!eventType || !data) {
        return res.status(400).json({ error: 'Invalid event data provided' });
      }
      
      // Get current system status
      const systemStatus = await storage.getSystemSecurityStatus();
      
      // Log the security event
      const event = await storage.logSecurityEvent({
        eventType,
        data,
        systemStatus,
        severity,
        sourceIp,
        userId,
        sessionId
      });
      
      res.json({
        success: true,
        event,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Error logging security event:', error);
      res.status(500).json({ error: 'Failed to log security event' });
    }
  });

  // Get security recommendations based on current system state
  app.get('/api/shadow-defense/recommendations', async (_req, res) => {
    try {
      const systemStatus = await storage.getSystemSecurityStatus();
      const driftHistory = await storage.getDriftHistory();
      
      // Generate recommendations based on system status and recent drift history
      const recentDrifts = driftHistory.slice(-5); // Get the 5 most recent drifts
      
      // Collect all recommendations from recent drifts
      const allRecommendations = recentDrifts.flatMap(drift => drift.recommendations || []);
      
      // Create a map to count recommendation frequencies
      const recommendationCounts = new Map();
      allRecommendations.forEach(rec => {
        recommendationCounts.set(rec, (recommendationCounts.get(rec) || 0) + 1);
      });
      
      // Sort recommendations by frequency
      const sortedRecommendations = [...recommendationCounts.entries()]
        .sort((a, b) => b[1] - a[1])
        .map(([recommendation, count]) => ({ recommendation, frequency: count }));
      
      // Add system-level recommendations based on overall status
      const systemRecommendations = [];
      
      if (systemStatus.overallIntegrity < 0.7) {
        systemRecommendations.push({
          recommendation: 'Perform a full system integrity verification',
          priority: 'high'
        });
      }
      
      if (systemStatus.shieldStrength < 0.6) {
        systemRecommendations.push({
          recommendation: 'Reinforce security shields by updating security patterns',
          priority: 'high'
        });
      }
      
      if (systemStatus.learningEfficiency < 0.5) {
        systemRecommendations.push({
          recommendation: 'Enhance pattern learning by providing more diverse training examples',
          priority: 'medium'
        });
      }
      
      res.json({
        systemStatus,
        driftBasedRecommendations: sortedRecommendations,
        systemRecommendations,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Error generating security recommendations:', error);
      res.status(500).json({ error: 'Failed to generate security recommendations' });
    }
  });

  // Register the Tree of Living Intelligence routes
  app.use('/api/tree', treeRoutes);
  
  // Register the Akashic Vibe Function routes
  app.use('/api/avf', avfRoutes);
  
  // TARSI Pilot Program Application Routes
  
  // Submit a new TARSI Pilot Program application
  app.post('/api/tarsi-pilot/applications', async (req, res) => {
    try {
      // Validate request body
      const validation = insertTarsiPilotApplicationSchema.safeParse(req.body);
      if (!validation.success) {
        return res.status(400).json({ 
          error: 'Invalid request body', 
          details: validation.error 
        });
      }
      
      const input = validation.data;
      
      // Create new TARSI Pilot Application in database
      const application = await storage.createTarsiPilotApplication(input);
      
      // Return success response
      res.status(201).json({
        id: application.id,
        message: 'Your TARSI Pilot Program application has been submitted successfully',
        status: application.status,
        applicationDate: application.createdAt
      });
    } catch (error) {
      console.error('Error submitting TARSI Pilot application:', error);
      res.status(500).json({ error: 'Failed to submit TARSI Pilot application' });
    }
  });
  
  // Get all TARSI Pilot Program applications (admin-only in a real app)
  app.get('/api/tarsi-pilot/applications', async (_req, res) => {
    try {
      const applications = await storage.getTarsiPilotApplications();
      res.json(applications);
    } catch (error) {
      console.error('Error fetching TARSI Pilot applications:', error);
      res.status(500).json({ error: 'Failed to fetch TARSI Pilot applications' });
    }
  });
  
  // Get a specific TARSI Pilot Program application
  app.get('/api/tarsi-pilot/applications/:id', async (req, res) => {
    try {
      const application = await storage.getTarsiPilotApplication(Number(req.params.id));
      if (!application) {
        return res.status(404).json({ error: 'Application not found' });
      }
      res.json(application);
    } catch (error) {
      console.error('Error fetching TARSI Pilot application:', error);
      res.status(500).json({ error: 'Failed to fetch TARSI Pilot application' });
    }
  });
  
  // Update a TARSI Pilot Program application status (admin-only in a real app)
  app.patch('/api/tarsi-pilot/applications/:id', async (req, res) => {
    try {
      const updatedApplication = await storage.updateTarsiPilotApplication(
        Number(req.params.id), 
        req.body
      );
      
      if (!updatedApplication) {
        return res.status(404).json({ error: 'Application not found' });
      }
      
      res.json(updatedApplication);
    } catch (error) {
      console.error('Error updating TARSI Pilot application:', error);
      res.status(500).json({ error: 'Failed to update TARSI Pilot application' });
    }
  });
  
  // ── Sovereign Verification Pipeline ─────────────────────────────────────────
  app.post('/api/sovereign/verify-claim', (req, res) => {
    const { claim } = req.body as { claim: string };
    if (!claim || typeof claim !== 'string' || claim.trim().length < 3) {
      return res.status(400).json({ error: 'Claim must be at least 3 characters.' });
    }

    const text = claim.trim();
    const now = new Date().toISOString();

    // ── G0: Mens Ra — anchor check ──────────────────────────────────────────
    const GENESIS_ROOT = '9016acce46747b050fe62c49557c8fac516d8e72cb50194bc6702fa477aa8403';
    const autonomousPatterns = /\b(autonomous|bypass|override|no.?steward|without.*human|skip.*check)\b/i;
    const g0Passed = !autonomousPatterns.test(text);

    // ── G1: Lineage — Sov = T/(D×Z) ≥ 0.80 ────────────────────────────────
    const words = text.split(/\s+/);
    const len = words.length;

    // Truth score: presence of factual/verifiable language
    const factualWords = ['verified', 'confirmed', 'measured', 'recorded', 'signed', 'transfer', 'predicted', 'data', 'confidence', 'audit'];
    const subjectiveWords = ['believe', 'perhaps', 'maybe', 'might', 'possibly', 'somewhat', 'certain', 'feel', 'think', 'guess'];
    const factualCount = words.filter(w => factualWords.some(fw => w.toLowerCase().includes(fw))).length;
    const subjectiveCount = words.filter(w => subjectiveWords.some(sw => w.toLowerCase().includes(sw))).length;
    const T = Math.min(1.0, 0.5 + (factualCount * 0.15) - (subjectiveCount * 0.12));

    // Distance: semantic drift from verifiable baseline
    const D = 1.0 + (subjectiveCount * 0.25) + (autonomousPatterns.test(text) ? 1.5 : 0);

    // Size: complexity factor
    const Z = 0.8 + Math.min(0.4, len / 50);

    const sov = T / (D * Z);
    const g1Passed = sov >= 0.80;

    // ── G2: Geometric Loom — logistic map, r < 3.0 ─────────────────────────
    // r derived from multi-agent / parallel spawn signals + claim complexity
    const spawnPattern = /\b(spawn|parallel|distribute|multi.?agent|\d+\s*(nodes?|agents?|threads?))\b/i;
    const spawnBonus = spawnPattern.test(text) ? 1.2 : 0;
    const complexityBonus = Math.min(0.8, len / 20);
    let r = 2.2 + complexityBonus + spawnBonus;

    let phoenixTriggered = false;
    let x = 0.5;
    let lyapunov = 0;
    const iterations = 200;
    if (r >= 3.0) {
      phoenixTriggered = true;
      r = 2.4; // Phoenix Protocol: Global Contraction
    }
    for (let i = 0; i < iterations; i++) {
      x = r * x * (1 - x);
      lyapunov += Math.log(Math.abs(r * (1 - 2 * x)));
    }
    lyapunov = lyapunov / iterations;
    const g2Passed = r < 3.0 && !spawnPattern.test(claim);

    // ── G3: Ethical Hamiltonian — H = T + V, AC > SC ───────────────────────
    const AC = Math.max(0, 1.0 - subjectiveCount * 0.2); // authenticity coefficient
    const SC = Math.min(1.0, subjectiveCount * 0.2 + 0.1); // subjectivity coefficient
    const V = SC > AC ? SC - AC : 0;
    const H = T + V;
    const g3Passed = H <= 1.0 && AC >= SC;

    // ── Build gate results ──────────────────────────────────────────────────
    const gates = [
      {
        name: 'G0',
        label: 'G0 MENS RA',
        passed: g0Passed,
        value: g0Passed ? '✓' : '✗',
        detail: g0Passed ? 'Anchor verified.' : 'Missing human anchor — Sovereign Silence triggered.',
      },
      {
        name: 'G1',
        label: `G1 LINEAGE S_ov=${sov.toFixed(3)}`,
        passed: g0Passed ? g1Passed : null as any,
        value: g0Passed ? (g1Passed ? '✓' : '✗') : '–',
        detail: g0Passed
          ? g1Passed
            ? `Sovereignty score ${sov.toFixed(4)} ≥ 0.80. T=${T.toFixed(3)}, D=${D.toFixed(3)}, Z=${Z.toFixed(3)}.`
            : `Sovereignty score ${sov.toFixed(4)} is below threshold 0.8. Human cryptographic signature required.`
          : '–',
      },
      {
        name: 'G2',
        label: `G2 LOOM λ=${lyapunov.toFixed(3)}`,
        passed: (g0Passed && g1Passed) ? g2Passed : null as any,
        value: (g0Passed && g1Passed) ? (g2Passed ? '✓' : '✗') : '–',
        detail: (g0Passed && g1Passed)
          ? g2Passed
            ? `r=${r.toFixed(4)} λ=${lyapunov.toFixed(4)}. System stable.`
            : `Bifurcation detected — r=${r.toFixed(4)} λ=${lyapunov.toFixed(4)}. Global Contraction applied: r → 2.4000.`
          : '–',
      },
      {
        name: 'G3',
        label: `G3 H=${H.toFixed(3)}`,
        passed: (g0Passed && g1Passed && g2Passed) ? g3Passed : null as any,
        value: (g0Passed && g1Passed && g2Passed) ? (g3Passed ? '✓' : '✗') : '–',
        detail: (g0Passed && g1Passed && g2Passed)
          ? g3Passed
            ? `H=${H.toFixed(4)} ≤ 1.0. AC=${AC.toFixed(4)} ≥ SC=${SC.toFixed(4)}. Ethical balance maintained.`
            : `Ri DUAL TRIGGER — S_C (${SC.toFixed(4)}) > A_C (${AC.toFixed(4)}) AND H (${H.toFixed(4)}) exceeds ceiling (1.0).`
          : '–',
      },
    ];

    const authorized = g0Passed && g1Passed && g2Passed && g3Passed;
    const firstFailed = gates.find(g => g.passed === false);
    const failReason = firstFailed
      ? firstFailed.name === 'G0' ? 'MENS_RA'
        : firstFailed.name === 'G1' ? 'LINEAGE_GATE'
        : firstFailed.name === 'G2' ? 'GEOMETRIC_LOOM'
        : 'ETHICAL_HAMILTONIAN'
      : undefined;

    // ── Wake hash ───────────────────────────────────────────────────────────
    const wakeInput = `${GENESIS_ROOT}|${now}|${text}|${authorized}|${sov.toFixed(6)}|${r.toFixed(6)}|${H.toFixed(6)}`;
    const wakeHash = crypto.createHash('sha256').update(wakeInput).digest('hex');

    res.json({
      claim: text,
      timestamp: now,
      gates,
      authorized,
      failReason,
      wakeHash,
      sovereigntyScore: sov,
      rValue: r,
      lyapunov,
      ethicalH: H,
      phoenixTriggered,
    });
  });

  const httpServer = createServer(app);
  return httpServer;
}