/**
 * Main routes configuration file
 */

const express = require('express');
const pythoneticsRoutes = require('./pythonetics');

const router = express.Router();

// System routes
router.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString()
  });
});

// Pythonetics routes
router.use('/pythonetics', pythoneticsRoutes);

module.exports = router;