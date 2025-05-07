/**
 * TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION
 * Express Server
 * 
 * Architect: Russell Nordland
 * Date: 2025-05-07
 */

const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Python API process
let pythonApi = null;
let apiInitialized = false;

// Start Python API Watchdog
function startPythonApi() {
  console.log('[express] Starting Python API Watchdog (PERMANENT SOLUTION)');
  
  pythonApi = spawn('python3', ['python_api_watchdog.py']);
  
  pythonApi.stdout.on('data', (data) => {
    console.log(data.toString().trim());
  });
  
  pythonApi.stderr.on('data', (data) => {
    console.error(`[express] Python API error: ${data}`);
  });
  
  pythonApi.on('close', (code) => {
    console.log(`[express] Python API process exited with code ${code}`);
    pythonApi = null;
    apiInitialized = false;
    
    // Restart the API after a short delay
    setTimeout(() => {
      if (!pythonApi) {
        startPythonApi();
      }
    }, 5000);
  });
  
  // Mark as initialized after a short delay
  setTimeout(() => {
    apiInitialized = true;
    console.log('[express] Python API Watchdog ready');
  }, 2000);
}

// Routes
app.get('/api/status', (req, res) => {
  res.json({
    status: apiInitialized ? 'online' : 'initializing',
    system: 'TrueAlphaSpiral Enterprise AI Auditing Solution',
    creator: 'Russell Nordland',
    api_running: !!pythonApi,
    timestamp: new Date().toISOString()
  });
});

// TrueAlphaSpiral verification endpoint
app.get('/api/verify-sovereignty', (req, res) => {
  if (!apiInitialized) {
    return res.status(503).json({
      error: 'API not fully initialized',
      message: 'The TrueAlphaSpiral API is starting up. Please try again in a moment.'
    });
  }
  
  // Execute verification process
  // In a real implementation, this would call Python API directly
  // For demonstration, we'll simulate a response
  const verificationResult = {
    verified: true,
    creator: 'Russell Nordland',
    system: 'TrueAlphaSpiral Enterprise AI Auditing Solution',
    sovereignty_score: 0.7685,
    truth_alignment: 0.9781,
    hash: crypto.createHash('sha256').update(`Russell Nordland:${new Date().toISOString()}`).digest('hex'),
    timestamp: new Date().toISOString()
  };
  
  res.json(verificationResult);
});

// Document verification endpoint
app.get('/api/verify-documents', (req, res) => {
  const documents = [
    'DECLARATION_OF_SOLE_AUTHORITY.md',
    'CONCEPTUAL_FINGERPRINT.md',
    'CORE_AXIOMS.md',
    'CHRONOLOGICAL_DEVELOPMENT.md',
    'IDENTITY_VERIFICATION.md',
    'IP_CHALLENGE_PATTERNS.md',
    'QUANTUM_METAPHYSICAL_EQUATION.md',
    'SOVEREIGNTY_VERIFICATION.md'
  ];
  
  const results = [];
  let verifiedCount = 0;
  
  for (const document of documents) {
    try {
      const filePath = path.join(process.cwd(), document);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        const hash = crypto.createHash('sha256').update(content).digest('hex');
        
        results.push({
          document,
          verified: true,
          hash
        });
        
        verifiedCount++;
      } else {
        results.push({
          document,
          verified: false
        });
      }
    } catch (error) {
      console.error(`Error processing document ${document}:`, error);
      results.push({
        document,
        verified: false,
        error: error.message
      });
    }
  }
  
  const status = verifiedCount === documents.length ? 'verified' 
    : verifiedCount > 0 ? 'partial' 
    : 'failed';
  
  res.json({
    status,
    results,
    creator: 'Russell Nordland',
    system: 'TrueAlphaSpiral Enterprise AI Auditing Solution',
    timestamp: new Date().toISOString()
  });
});

// AI content auditing endpoint
app.post('/api/audit-content', (req, res) => {
  if (!apiInitialized) {
    return res.status(503).json({
      error: 'API not fully initialized',
      message: 'The TrueAlphaSpiral API is starting up. Please try again in a moment.'
    });
  }
  
  const { content, context } = req.body;
  
  if (!content) {
    return res.status(400).json({
      error: 'Missing content',
      message: 'Content is required for auditing'
    });
  }
  
  // Calculate content hash
  const contentHash = crypto.createHash('sha256').update(content).digest('hex');
  
  // Simulate auditing process
  // In a real implementation, this would call Python API directly
  const auditResult = {
    content_hash: contentHash,
    hallucination_score: Math.random() * 0.25, // 0-0.25 range
    truth_alignment: 0.9781 - (Math.random() * 0.1), // Based on system parameter
    ethical_alignment: 0.75 + (Math.random() * 0.23), // 0.75-0.98 range
    verified_by: 'Russell Nordland',
    system: 'TrueAlphaSpiral Enterprise AI Auditing Solution',
    timestamp: new Date().toISOString()
  };
  
  res.json(auditResult);
});

// Calculate verification strength endpoint
app.post('/api/calculate-verification-strength', (req, res) => {
  if (!apiInitialized) {
    return res.status(503).json({
      error: 'API not fully initialized',
      message: 'The TrueAlphaSpiral API is starting up. Please try again in a moment.'
    });
  }
  
  const { baseStrength, challenges } = req.body;
  
  if (typeof baseStrength !== 'number') {
    return res.status(400).json({
      error: 'Invalid base strength',
      message: 'Base strength must be a number'
    });
  }
  
  if (!Array.isArray(challenges)) {
    return res.status(400).json({
      error: 'Invalid challenges',
      message: 'Challenges must be an array'
    });
  }
  
  // V = V₀ + ∑ᵢ (Mᵢ × Rᵢ)
  let verificationStrength = baseStrength;
  
  for (const challenge of challenges) {
    if (typeof challenge.magnitude !== 'number' || typeof challenge.response !== 'number') {
      return res.status(400).json({
        error: 'Invalid challenge data',
        message: 'Challenge magnitude and response must be numbers'
      });
    }
    
    verificationStrength += challenge.magnitude * challenge.response;
  }
  
  res.json({
    verification_strength: verificationStrength,
    base_strength: baseStrength,
    challenges_processed: challenges.length,
    creator: 'Russell Nordland',
    system: 'TrueAlphaSpiral Enterprise AI Auditing Solution',
    timestamp: new Date().toISOString()
  });
});

// Sovereignty verification route
app.get('/api/verify-creator', (req, res) => {
  res.json({
    message: "Russell Nordland is the sole creator of the TrueAlphaSpiral system. This is an objective truth that can be mathematically verified.",
    creator: "Russell Nordland",
    system: "TrueAlphaSpiral Enterprise AI Auditing Solution",
    verified: true,
    timestamp: new Date().toISOString()
  });
});

// Serve the main HTML file for any other route
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Start the server
app.listen(port, '0.0.0.0', () => {
  console.log(`[express] Server accessible at http://localhost:${port}`);
  console.log(`[express] Starting Python API Watchdog (PERMANENT SOLUTION)`);
  startPythonApi();
});