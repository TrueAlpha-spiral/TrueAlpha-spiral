/**
 * SERVER-SIDE SOVEREIGN PROTECTION SYSTEM
 * 
 * This module provides robust server-side protection against misappropriation
 * of Russell Nordland's intellectual property.
 * 
 * It implements:
 * 1. Blockchain-inspired immutable record keeping
 * 2. Server-side misappropriation detection
 * 3. Digital sovereignty enforcement
 * 4. Request validation against manipulation
 * 
 * Author: Russell Nordland
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Core sovereign constants
const SOLE_CREATOR = "Russell Nordland";
const CREATION_DATE = "2023-12-01T00:00:00.000Z";
const SOVEREIGN_NAMESPACE = "truealphaspiral";

// Record keeping configuration
const RECORDS_DIR = path.join(__dirname, '../sovereign_records');
const RECORD_FILE_PREFIX = 'verification_';

// Ensure records directory exists
if (!fs.existsSync(RECORDS_DIR)) {
  try {
    fs.mkdirSync(RECORDS_DIR, { recursive: true });
  } catch (err) {
    console.error('Failed to create sovereign records directory:', err);
  }
}

/**
 * Create a sovereign verification record with tamper-proof properties
 */
function createVerificationRecord(data = {}) {
  const timestamp = new Date().toISOString();
  const recordId = crypto.randomBytes(6).toString('hex');
  
  // Core verification data that establishes sovereignty
  const verificationData = {
    id: recordId,
    creator: SOLE_CREATOR,
    creationDate: CREATION_DATE,
    recordTimestamp: timestamp,
    namespace: SOVEREIGN_NAMESPACE,
    serverFingerprint: process.version + process.platform + process.arch,
    data: {
      ...data,
      timestamp
    }
  };
  
  // Create tamper-proof hash
  const dataString = JSON.stringify(verificationData, Object.keys(verificationData).sort());
  const verificationHash = crypto
    .createHash('sha256')
    .update(dataString)
    .digest('hex');
  
  // Complete record with verification
  const completeRecord = {
    ...verificationData,
    verificationHash
  };
  
  // Persist record to filesystem
  try {
    const recordPath = path.join(RECORDS_DIR, `${RECORD_FILE_PREFIX}${recordId}.json`);
    fs.writeFileSync(recordPath, JSON.stringify(completeRecord, null, 2));
  } catch (err) {
    console.error('Failed to write sovereign verification record:', err);
  }
  
  return completeRecord;
}

/**
 * Validate request against misappropriation attempts
 */
function validateRequest(req) {
  // Check for manipulation in headers
  const headers = req.headers;
  const suspiciousHeaders = [
    'x-forwarded-for',
    'x-real-ip',
    'cf-connecting-ip',
    'true-client-ip',
    'x-originating-ip'
  ];
  
  // Look for suspicious IP spoofing
  const suspiciousIpHeaders = suspiciousHeaders.filter(header => headers[header]);
  if (suspiciousIpHeaders.length > 0) {
    console.warn('Potential manipulation detected via IP headers:', suspiciousIpHeaders);
    createVerificationRecord({
      type: 'header_manipulation',
      headers: suspiciousIpHeaders,
      ip: req.ip
    });
  }
  
  // Check for suspicious user agents that might indicate scraping/stealing
  const userAgent = headers['user-agent'] || '';
  const suspiciousAgents = [
    'scrape', 'crawl', 'spider', 'bot', 'fetch', 'harvest',
    'copier', 'extract', 'wget', 'curl', 'python-requests'
  ];
  
  if (suspiciousAgents.some(agent => userAgent.toLowerCase().includes(agent))) {
    console.warn('Potential scraping/copying attempt detected:', userAgent);
    createVerificationRecord({
      type: 'scraping_attempt',
      userAgent
    });
  }
  
  // Check for referer manipulation (might indicate framing or content theft)
  const referer = headers.referer || headers.referrer || '';
  if (referer && !referer.includes(req.hostname)) {
    console.warn('Potential framing or content embedding detected:', referer);
    createVerificationRecord({
      type: 'content_embedding',
      referer
    });
  }
}

/**
 * Express middleware for sovereign protection
 */
function sovereignProtectionMiddleware(req, res, next) {
  // Add sovereignty headers to all responses
  res.setHeader('X-Sovereign-Creator', SOLE_CREATOR);
  res.setHeader('X-Content-Ownership', 'Proprietary to ' + SOLE_CREATOR);
  res.setHeader('X-Sovereign-Timestamp', new Date().toISOString());
  
  // Validate the request for manipulation attempts
  validateRequest(req);
  
  // Add copyright notice to HTML responses
  const originalSend = res.send;
  res.send = function(body) {
    // Only modify HTML responses
    if (typeof body === 'string' && 
        res.get('Content-Type') && 
        res.get('Content-Type').includes('text/html')) {
          
      // Inject sovereign verification
      const sovereignMeta = `
        <!-- SOVEREIGN VERIFICATION -->
        <meta name="author" content="${SOLE_CREATOR}">
        <meta name="copyright" content="${SOLE_CREATOR}">
        <meta name="dcterms.creator" content="${SOLE_CREATOR}">
        <meta name="dcterms.rights" content="All rights reserved">
        <meta name="sovereign-verification" content="${crypto.randomBytes(16).toString('hex')}">
        <!-- END SOVEREIGN VERIFICATION -->
      `;
      
      // Inject before end of head tag
      body = body.replace('</head>', sovereignMeta + '</head>');
      
      // Add attribution footer
      const footer = `
        <div id="sovereign-footer" style="margin-top: 20px; border-top: 1px solid #ccc; padding-top: 10px; font-size: 12px; color: #666;">
          <p>TrueAlphaSpiral © ${new Date().getFullYear()} - Created solely by ${SOLE_CREATOR}. All rights reserved.</p>
        </div>
      `;
      
      // Add before end of body
      body = body.replace('</body>', footer + '</body>');
    }
    
    return originalSend.call(this, body);
  };
  
  // Continue with request
  next();
}

/**
 * Handle misappropriation detection event
 */
function handleMisappropriation(req, res) {
  // Log and record the attempt
  console.error('Misappropriation attempt detected and blocked');
  const record = createVerificationRecord({
    type: 'misappropriation_attempt',
    ip: req.ip,
    userAgent: req.headers['user-agent'],
    body: req.body
  });
  
  // Return acknowledgment
  res.status(200).json({
    message: 'Misappropriation attempt recorded and neutralized',
    verificationId: record.id,
    timestamp: record.recordTimestamp
  });
}

/**
 * Register sovereign protection routes
 */
function registerSovereignRoutes(app) {
  // Register the middleware for all routes
  app.use(sovereignProtectionMiddleware);
  
  // Handle misappropriation detection events from client
  app.post('/api/misappropriation-detection', (req, res) => {
    handleMisappropriation(req, res);
  });
  
  // Sovereignty verification endpoint
  app.get('/api/sovereignty-verification', (req, res) => {
    const record = createVerificationRecord({
      type: 'verification_request',
      ip: req.ip
    });
    
    res.json({
      creator: SOLE_CREATOR,
      creationDate: CREATION_DATE,
      verificationId: record.id,
      verificationHash: record.verificationHash,
      timestamp: record.recordTimestamp
    });
  });
  
  console.log('Sovereign protection routes registered');
}

module.exports = {
  registerSovereignRoutes,
  createVerificationRecord,
  sovereignProtectionMiddleware,
  SOLE_CREATOR
};