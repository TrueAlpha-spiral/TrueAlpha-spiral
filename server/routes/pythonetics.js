/**
 * Pythonetics Routes
 * 
 * This file contains routes for integrating with the Pythonetics system,
 * including routes for the Tree of Living Intelligence visualization.
 */

const express = require('express');
const axios = require('axios');
const router = express.Router();

// Configuration
const PYTHONETICS_API_PORT = process.env.PYTHONETICS_API_PORT || 8001;
const PYTHONETICS_API_HOST = process.env.PYTHONETICS_API_HOST || 'localhost';
const PYTHONETICS_API_BASE_URL = `http://${PYTHONETICS_API_HOST}:${PYTHONETICS_API_PORT}`;

const VISUALIZATION_PORT = process.env.VISUALIZATION_PORT || 8002;
const VISUALIZATION_HOST = process.env.VISUALIZATION_HOST || 'localhost';
const VISUALIZATION_BASE_URL = `http://${VISUALIZATION_HOST}:${VISUALIZATION_PORT}`;

// Cache for service status
let serviceStatus = {
  pythonetics: { status: 'unknown', lastChecked: 0 },
  visualization: { status: 'unknown', lastChecked: 0 }
};

/**
 * Check if the Pythonetics API is available
 */
async function checkPythoneticsApi() {
  const now = Date.now();
  
  // Only check if it's been more than 30 seconds since last check
  if (now - serviceStatus.pythonetics.lastChecked < 30000) {
    return serviceStatus.pythonetics.status === 'available';
  }
  
  try {
    const response = await axios.get(`${PYTHONETICS_API_BASE_URL}/api/health`, { timeout: 2000 });
    const available = response.status === 200;
    
    serviceStatus.pythonetics = {
      status: available ? 'available' : 'unavailable',
      lastChecked: now
    };
    
    return available;
  } catch (error) {
    console.error(`Error checking Pythonetics API: ${error.message}`);
    
    serviceStatus.pythonetics = {
      status: 'unavailable',
      lastChecked: now
    };
    
    return false;
  }
}

/**
 * Check if the Visualization service is available
 */
async function checkVisualizationService() {
  const now = Date.now();
  
  // Only check if it's been more than 30 seconds since last check
  if (now - serviceStatus.visualization.lastChecked < 30000) {
    return serviceStatus.visualization.status === 'available';
  }
  
  try {
    const response = await axios.get(`${VISUALIZATION_BASE_URL}/`, { timeout: 2000 });
    const available = response.status === 200;
    
    serviceStatus.visualization = {
      status: available ? 'available' : 'unavailable',
      lastChecked: now
    };
    
    return available;
  } catch (error) {
    console.error(`Error checking Visualization service: ${error.message}`);
    
    serviceStatus.visualization = {
      status: 'unavailable',
      lastChecked: now
    };
    
    return false;
  }
}

/**
 * Health check endpoint
 */
router.get('/health', async (req, res) => {
  const pythoneticsAvailable = await checkPythoneticsApi();
  const visualizationAvailable = await checkVisualizationService();
  
  res.json({
    status: 'ok',
    pythonetics: pythoneticsAvailable ? 'available' : 'unavailable',
    visualization: visualizationAvailable ? 'available' : 'unavailable',
    timestamp: new Date().toISOString()
  });
});

/**
 * Verify text with the Pythonetics API
 */
router.post('/verify', async (req, res) => {
  try {
    const pythoneticsAvailable = await checkPythoneticsApi();
    
    if (!pythoneticsAvailable) {
      return res.status(503).json({
        error: 'Pythonetics API unavailable',
        message: 'The Pythonetics API is currently unavailable. Please try again later.'
      });
    }
    
    const { text, verify_as = 'claim' } = req.body;
    
    if (!text) {
      return res.status(400).json({
        error: 'Missing text',
        message: 'Text to verify is required'
      });
    }
    
    // Forward request to Pythonetics API
    const response = await axios.post(`${PYTHONETICS_API_BASE_URL}/api/verify`, {
      text,
      verify_as
    });
    
    res.json(response.data);
  } catch (error) {
    console.error(`Error verifying text: ${error.message}`);
    
    res.status(500).json({
      error: 'Verification failed',
      message: error.message
    });
  }
});

/**
 * Generate tree visualization data
 */
router.post('/tree-data', async (req, res) => {
  try {
    const pythoneticsAvailable = await checkPythoneticsApi();
    
    if (!pythoneticsAvailable) {
      return res.status(503).json({
        error: 'Pythonetics API unavailable',
        message: 'The Pythonetics API is currently unavailable. Please try again later.'
      });
    }
    
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({
        error: 'Missing text',
        message: 'Text to analyze is required'
      });
    }
    
    // Forward request to Pythonetics API
    const response = await axios.post(`${PYTHONETICS_API_BASE_URL}/api/tree-data`, {
      text
    });
    
    res.json(response.data);
  } catch (error) {
    console.error(`Error generating tree data: ${error.message}`);
    
    res.status(500).json({
      error: 'Tree data generation failed',
      message: error.message
    });
  }
});

/**
 * Proxy for the visualization UI
 */
router.get('/visualization', async (req, res) => {
  try {
    const visualizationAvailable = await checkVisualizationService();
    
    if (!visualizationAvailable) {
      return res.send(`
        <html>
          <head>
            <title>Tree of Living Intelligence Visualization</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
                text-align: center;
              }
              h1 {
                color: #3498db;
              }
              .error-container {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 2rem;
                margin-top: 2rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
              }
              .icon {
                font-size: 3rem;
                margin-bottom: 1rem;
              }
            </style>
          </head>
          <body>
            <h1>Tree of Living Intelligence</h1>
            <div class="error-container">
              <div class="icon">🌱</div>
              <h2>Visualization Service Unavailable</h2>
              <p>The Tree of Living Intelligence visualization service is currently unavailable.</p>
              <p>Please start the visualization server using the <code>run_visualization.py</code> script.</p>
            </div>
          </body>
        </html>
      `);
    }
    
    // Redirect to visualization server
    res.redirect(`${VISUALIZATION_BASE_URL}/`);
  } catch (error) {
    console.error(`Error serving visualization: ${error.message}`);
    
    res.status(500).send(`
      <html>
        <head>
          <title>Error</title>
        </head>
        <body>
          <h1>Error</h1>
          <p>${error.message}</p>
        </body>
      </html>
    `);
  }
});

module.exports = router;