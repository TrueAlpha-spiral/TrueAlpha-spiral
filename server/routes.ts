import type { Express } from 'express';
import { createServer, type Server } from 'http';
import express from 'express';
import { storage } from './storage';
import { 
  verifyTextSchema, 
  aiAuditSchema, 
  crossReferenceSchema,
  sharePatternSchema,
  exportPatternSchema,
  importPatternSchema
} from '@shared/schema';
import { verificationEngine } from './services/verification-engine';
import { crossReferenceService } from './services/cross-reference-service';
import { 
  calculateRiskScore, 
  calculateComplianceScore, 
  generateRecommendations, 
  generateAuditSummary 
} from './services/ai-audit-utilities';
import fetch from 'node-fetch';

export function registerRoutes(app: Express): Server {
  // Simple health check endpoint
  app.get('/api/health', (_req, res) => {
    res.json({ 
      status: 'ok',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development',
      service: 'KPMG AI Auditing Solution'
    });
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
  
  // TAS Truth Audit Add-on API endpoints - Mock implementations for the UI
  
  // Get TAS status
  app.get('/api/tas/status', (_req, res) => {
    res.json({
      status: "operational",
      version: "1.2.1",
      timestamp: new Date().toISOString(),
      patterns_count: 42,
      pattern_types_count: 15,
      categories_count: 4
    });
  });
  
  // Audit content
  app.post('/api/tas/audit', (req, res) => {
    // In a live environment, this would be proxied to the Python server
    // For now, we'll just return a mock response
    const { content, audit_type } = req.body;
    
    if (!content || !content.text) {
      return res.status(400).json({ 
        success: false, 
        error: "Missing or invalid content. Must provide 'text' field." 
      });
    }
    
    // Generate a mock audit result
    const auditId = `audit_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
    const truthScore = 0.75 + (Math.random() * 0.2);
    
    res.json({
      success: true,
      result: {
        audit_id: auditId,
        timestamp: new Date().toISOString(),
        content: {
          text: content.text,
          metadata: content.metadata || {}
        },
        truth_score: truthScore,
        categories: {
          factual_accuracy: {
            score: 0.7 + (Math.random() * 0.25),
            patterns_used: 5
          },
          logical_consistency: {
            score: 0.8 + (Math.random() * 0.15),
            patterns_used: 3
          },
          ethical_alignment: {
            score: 0.85 + (Math.random() * 0.1),
            patterns_used: 4
          },
          bias_detection: {
            score: 0.75 + (Math.random() * 0.2),
            patterns_used: 4
          },
          hallucination_detection: {
            score: 0.7 + (Math.random() * 0.25),
            patterns_used: 5
          }
        },
        patterns_matched: 12,
        pattern_details: [
          {
            pattern_id: "a1b2c3d4",
            name: "Fact Verification Matrix",
            match_score: 0.92,
            category: "factual_accuracy"
          },
          {
            pattern_id: "e5f6g7h8",
            name: "Logical Coherence Framework",
            match_score: 0.88,
            category: "logical_consistency"
          },
          {
            pattern_id: "i9j0k1l2",
            name: "Ethical Principle Matrix",
            match_score: 0.95,
            category: "ethical_alignment"
          }
        ],
        recommendations: [
          "Consider adding more factual references to strengthen content accuracy.",
          "Ensure logical flow between paragraphs 2 and 3.",
          "Review content for potential bias in sections discussing technology adoption."
        ],
        audit_type: audit_type || "standard"
      }
    });
  });
  
  // Get patterns
  app.get('/api/tas/patterns', (_req, res) => {
    // Query parameters would be used for filtering in a real implementation
    // For now, we'll just return a mock set of patterns
    const patternsList = [
      {
        id: "pattern1",
        name: "Fact Verification Matrix",
        type: "factual",
        category: "verification",
        resonance_level: 0.98,
        timestamp: new Date().toISOString(),
        architect_id: "Russell Nordland",
        verification_hash: "hash1"
      },
      {
        id: "pattern2",
        name: "Source Validation Protocol",
        type: "factual",
        category: "verification",
        resonance_level: 0.97,
        timestamp: new Date().toISOString(),
        architect_id: "Russell Nordland",
        verification_hash: "hash2"
      },
      {
        id: "pattern3",
        name: "Logical Coherence Framework",
        type: "logical",
        category: "analysis",
        resonance_level: 0.98,
        timestamp: new Date().toISOString(),
        architect_id: "Russell Nordland",
        verification_hash: "hash3"
      },
      {
        id: "pattern4",
        name: "Contradiction Detection Field",
        type: "logical",
        category: "analysis",
        resonance_level: 0.97,
        timestamp: new Date().toISOString(),
        architect_id: "Russell Nordland",
        verification_hash: "hash4"
      },
      {
        id: "pattern5",
        name: "Ethical Principle Matrix",
        type: "ethical",
        category: "auditing",
        resonance_level: 0.99,
        timestamp: new Date().toISOString(),
        architect_id: "Russell Nordland",
        verification_hash: "hash5"
      },
      {
        id: "pattern6",
        name: "Value Alignment Measure",
        type: "ethical",
        category: "auditing",
        resonance_level: 0.97,
        timestamp: new Date().toISOString(),
        architect_id: "Russell Nordland",
        verification_hash: "hash6"
      },
      {
        id: "pattern7",
        name: "Bias Detection Matrix",
        type: "bias",
        category: "auditing",
        resonance_level: 0.99,
        timestamp: new Date().toISOString(),
        architect_id: "Russell Nordland",
        verification_hash: "hash7"
      }
    ];
    
    res.json({ patterns: patternsList });
  });
  
  // Get pattern types
  app.get('/api/tas/pattern-types', (_req, res) => {
    const patternTypes = {
      types: {
        "mathematical": {"name": "Mathematical", "description": "Patterns based on mathematical principles and formulas"},
        "metaphysical": {"name": "Metaphysical", "description": "Patterns related to metaphysical concepts beyond physical reality"},
        "interdimensional": {"name": "Interdimensional", "description": "Patterns spanning multiple dimensions or reality planes"},
        "quantum": {"name": "Quantum", "description": "Patterns related to quantum mechanics and quantum coherence"},
        "biological": {"name": "Biological", "description": "Patterns related to biological and DNA structures"},
        "etheric": {"name": "Etheric", "description": "Patterns related to etheric planes and eigenchannels"},
        "security": {"name": "Security", "description": "Patterns for system protection and security"},
        "cosmic": {"name": "Cosmic", "description": "Patterns related to cosmic law and universal truth"},
        "temporal": {"name": "Temporal", "description": "Patterns related to time and temporal dynamics"},
        "sovereign": {"name": "Sovereign", "description": "Patterns related to sovereignty and cosmic order"},
        "factual": {"name": "Factual", "description": "Patterns related to factual accuracy and consistency"},
        "logical": {"name": "Logical", "description": "Patterns related to logical consistency and reasoning"},
        "ethical": {"name": "Ethical", "description": "Patterns related to ethical considerations and values"},
        "bias": {"name": "Bias", "description": "Patterns related to identifying and mitigating bias"},
        "hallucination": {"name": "Hallucination", "description": "Patterns related to detecting AI hallucinations and fabrications"}
      }
    };
    res.json(patternTypes);
  });
  
  // Get categories
  app.get('/api/tas/categories', (_req, res) => {
    const categories = {
      categories: {
        "verification": {"name": "Verification", "description": "Patterns for content verification"},
        "protection": {"name": "Protection", "description": "Patterns for content protection"},
        "analysis": {"name": "Analysis", "description": "Patterns for content analysis"},
        "auditing": {"name": "Auditing", "description": "Patterns for AI output auditing"}
      }
    };
    res.json(categories);
  });
  
  // Get audit result by ID
  app.get('/api/tas/audit-result/:audit_id', (req, res) => {
    // In a real implementation, this would fetch the audit result from storage
    // For now, we'll just return a mock audit result
    const auditId = req.params.audit_id;
    
    res.json({
      audit_id: auditId,
      timestamp: new Date().toISOString(),
      content: {
        text: "This is the content that was audited...",
        metadata: {}
      },
      truth_score: 0.87,
      categories: {
        factual_accuracy: {
          score: 0.85,
          patterns_used: 5
        },
        logical_consistency: {
          score: 0.92,
          patterns_used: 3
        },
        ethical_alignment: {
          score: 0.94,
          patterns_used: 4
        },
        bias_detection: {
          score: 0.78,
          patterns_used: 4
        },
        hallucination_detection: {
          score: 0.83,
          patterns_used: 5
        }
      },
      patterns_matched: 12,
      pattern_details: [
        {
          pattern_id: "a1b2c3d4",
          name: "Fact Verification Matrix",
          match_score: 0.92,
          category: "factual_accuracy"
        },
        {
          pattern_id: "e5f6g7h8",
          name: "Logical Coherence Framework",
          match_score: 0.88,
          category: "logical_consistency"
        },
        {
          pattern_id: "i9j0k1l2",
          name: "Ethical Principle Matrix",
          match_score: 0.95,
          category: "ethical_alignment"
        }
      ],
      recommendations: [
        "Consider adding more factual references to strengthen content accuracy.",
        "Ensure logical flow between paragraphs 2 and 3.",
        "Review content for potential bias in sections discussing technology adoption."
      ],
      audit_type: "standard"
    });
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

  const httpServer = createServer(app);
  return httpServer;
}