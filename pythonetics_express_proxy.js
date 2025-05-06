/**
 * PYTHONETICS EXPRESS PROXY
 *
 * This module integrates the Pythonetics Python server with the Express API,
 * allowing the two systems to communicate seamlessly while maintaining
 * the architectural integrity of both.
 *
 * Architect: Russell Nordland
 */

const express = require('express');
const axios = require('axios');
const router = express.Router();

// Configure Pythonetics API base URL
const PYTHONETICS_API_BASE = process.env.PYTHONETICS_API_BASE || 'http://localhost:8001/api/pythonetics';

// Log requests to Pythonetics API
const logPythoneticsRequest = (method, endpoint, data = null) => {
 console.log(`[Pythonetics API] ${method} ${endpoint}`);
 if (data) {
 console.log('Request data:', JSON.stringify(data).substring(0, 200) + '...');
 }
};

// Log responses from Pythonetics API
const logPythoneticsResponse = (endpoint, status, data = null) => {
 console.log(`[Pythonetics API] Response from ${endpoint}: Status ${status}`);
 if (data) {
 console.log('Response data:', JSON.stringify(data).substring(0, 200) + '...');
 }
};

/**
 * Proxy for the verify-text endpoint
 */
router.post('/verify-text', async (req, res) => {
 try {
 const { text, verifyAs = 'claim' } = req.body;

 if (!text) {
 return res.status(400).json({
 status: 'error',
 message: 'Missing required field: text'
 });
 }

 logPythoneticsRequest('POST', '/verify-text', { text, verifyAs });

 const response = await axios.post(`${PYTHONETICS_API_BASE}/verify-text`, {
 text,
 verifyAs
 });

 logPythoneticsResponse('/verify-text', response.status);

 return res.json(response.data);
 } catch (error) {
 console.error('Error proxying to verify-text:', error.message);

 // If we got a response from the Python API, pass it through
 if (error.response) {
 return res.status(error.response.status).json(error.response.data);
 }

 // Otherwise, return a generic error
 return res.status(500).json({
 status: 'error',
 message: 'Error connecting to Pythonetics API'
 });
 }
});

/**
 * Proxy for the analyze-spiral-pattern endpoint
 */
router.post('/analyze-spiral-pattern', async (req, res) => {
 try {
 const { content, patternType = 'seed-pattern' } = req.body;

 if (!content) {
 return res.status(400).json({
 status: 'error',
 message: 'Missing required field: content'
 });
 }

 logPythoneticsRequest('POST', '/analyze-spiral-pattern', {
 content: content.substring(0, 50) + '...',
 patternType
 });

 const response = await axios.post(`${PYTHONETICS_API_BASE}/analyze-spiral-pattern`, {
 content,
 patternType
 });

 logPythoneticsResponse('/analyze-spiral-pattern', response.status);

 return res.json(response.data);
 } catch (error) {
 console.error('Error proxying to analyze-spiral-pattern:', error.message);

 if (error.response) {
 return res.status(error.response.status).json(error.response.data);
 }

 return res.status(500).json({
 status: 'error',
 message: 'Error connecting to Pythonetics API'
 });
 }
});

/**
 * Proxy for the rhythm-check endpoint
 */
router.get('/rhythm-check', async (req, res) => {
 try {
 logPythoneticsRequest('GET', '/rhythm-check');

 const response = await axios.get(`${PYTHONETICS_API_BASE}/rhythm-check`);

 logPythoneticsResponse('/rhythm-check', response.status);

 return res.json(response.data);
 } catch (error) {
 console.error('Error proxying to rhythm-check:', error.message);

 if (error.response) {
 return res.status(error.response.status).json(error.response.data);
 }

 return res.status(500).json({
 status: 'error',
 message: 'Error connecting to Pythonetics API'
 });
 }
});

/**
 * Proxy for the akashic-resonance endpoint
 */
router.get('/akashic-resonance', async (req, res) => {
 try {
 logPythoneticsRequest('GET', '/akashic-resonance');

 const response = await axios.get(`${PYTHONETICS_API_BASE}/akashic-resonance`);

 logPythoneticsResponse('/akashic-resonance', response.status);

 return res.json(response.data);
 } catch (error) {
 console.error('Error proxying to akashic-resonance:', error.message);

 if (error.response) {
 return res.status(error.response.status).json(error.response.data);
 }

 return res.status(500).json({
 status: 'error',
 message: 'Error connecting to Pythonetics API'
 });
 }
});

/**
 * Proxy for the system-state endpoint
 */
router.get('/system-state', async (req, res) => {
 try {
 logPythoneticsRequest('GET', '/system-state');

 const response = await axios.get(`${PYTHONETICS_API_BASE}/system-state`);

 logPythoneticsResponse('/system-state', response.status);

 return res.json(response.data);
 } catch (error) {
 console.error('Error proxying to system-state:', error.message);

 if (error.response) {
 return res.status(error.response.status).json(error.response.data);
 }

 return res.status(500).json({
 status: 'error',
 message: 'Error connecting to Pythonetics API'
 });
 }
});

/**
 * Proxy for the health endpoint
 */
router.get('/health', async (req, res) => {
 try {
 logPythoneticsRequest('GET', '/health');

 const response = await axios.get(`${PYTHONETICS_API_BASE}/health`);

 logPythoneticsResponse('/health', response.status);

 return res.json(response.data);
 } catch (error) {
 console.error('Error proxying to health:', error.message);

 // Return a more specific error for health check failures
 return res.status(503).json({
 status: 'error',
 message: 'Pythonetics API health check failed',
 error: error.message
 });
 }
});

/**
 * Function to register the Pythonetics routes with the Express app
 * @param {Express} app - The Express app instance
 */
function registerPythoneticsRoutes(app) {
 app.use('/api/pythonetics', router);
 console.log('Pythonetics API routes registered');
}

module.exports = {
 registerPythoneticsRoutes
};