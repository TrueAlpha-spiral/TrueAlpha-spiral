import { Router } from 'express';
import { exec } from 'child_process';
import fs from 'fs';
import path from 'path';
import { promisify } from 'util';

const execAsync = promisify(exec);
const router = Router();

// Endpoint to test the AVF (Akashic Vibe Function)
router.get('/test', (req, res) => {
  res.json({
    status: 'success',
    message: 'AVF routes are working correctly!',
    timestamp: new Date().toISOString()
  });
});

// Endpoint to analyze text with the AVF
router.post('/analyze', async (req, res) => {
  try {
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({
        status: 'error',
        message: 'Text is required for analysis'
      });
    }
    
    // Call the Python script to analyze the text
    const scriptPath = path.join(process.cwd(), 'akashic_vibe_function.py');
    
    // Create a temporary file to store the text for analysis
    const tempFilePath = path.join(process.cwd(), 'temp_avf_input.json');
    fs.writeFileSync(tempFilePath, JSON.stringify({ text }));
    
    try {
      // Run the Python script with the input file
      const { stdout, stderr } = await execAsync(`python ${scriptPath} --analyze --input ${tempFilePath} --output-json`);
      
      if (stderr) {
        console.error('AVF Analysis Error:', stderr);
      }
      
      // Parse the output
      let result;
      try {
        result = JSON.parse(stdout);
      } catch (parseError) {
        console.error('Failed to parse AVF output:', parseError);
        result = { 
          status: 'partial_success',
          raw_output: stdout,
          message: 'Analysis completed but results could not be fully parsed'
        };
      }
      
      // Clean up
      if (fs.existsSync(tempFilePath)) {
        fs.unlinkSync(tempFilePath);
      }
      
      return res.json({
        status: 'success',
        result
      });
      
    } catch (execError) {
      console.error('Failed to execute AVF analysis:', execError);
      return res.status(500).json({
        status: 'error',
        message: 'Failed to execute AVF analysis',
        error: execError.message
      });
    }
  } catch (error) {
    console.error('AVF Analysis Error:', error);
    return res.status(500).json({
      status: 'error',
      message: 'An error occurred during AVF analysis',
      error: error.message
    });
  }
});

// Endpoint to integrate AVF with Pythonetics
router.post('/integrate', async (req, res) => {
  try {
    const { text, verifyAs } = req.body;
    
    if (!text) {
      return res.status(400).json({
        status: 'error',
        message: 'Text is required for integration'
      });
    }
    
    // Call the Python script to integrate AVF with Pythonetics
    const scriptPath = path.join(process.cwd(), 'akashic_pythonetics_integration.py');
    
    // Create a temporary file to store the input for integration
    const tempFilePath = path.join(process.cwd(), 'temp_avf_integration_input.json');
    fs.writeFileSync(tempFilePath, JSON.stringify({ 
      text, 
      verify_as: verifyAs || 'claim' 
    }));
    
    try {
      // Run the Python script with the input file
      const { stdout, stderr } = await execAsync(`python ${scriptPath} --integrate --input ${tempFilePath} --output-json`);
      
      if (stderr) {
        console.error('AVF Integration Error:', stderr);
      }
      
      // Parse the output
      let result;
      try {
        result = JSON.parse(stdout);
      } catch (parseError) {
        console.error('Failed to parse AVF integration output:', parseError);
        result = { 
          status: 'partial_success',
          raw_output: stdout,
          message: 'Integration completed but results could not be fully parsed'
        };
      }
      
      // Clean up
      if (fs.existsSync(tempFilePath)) {
        fs.unlinkSync(tempFilePath);
      }
      
      return res.json({
        status: 'success',
        result
      });
      
    } catch (execError) {
      console.error('Failed to execute AVF integration:', execError);
      return res.status(500).json({
        status: 'error',
        message: 'Failed to execute AVF integration',
        error: execError.message
      });
    }
  } catch (error) {
    console.error('AVF Integration Error:', error);
    return res.status(500).json({
      status: 'error',
      message: 'An error occurred during AVF integration',
      error: error.message
    });
  }
});

// Endpoint to get visualization parameters for the tree based on resonance
router.post('/tree-visualization', async (req, res) => {
  try {
    const { resonanceResults } = req.body;
    
    if (!resonanceResults) {
      return res.status(400).json({
        status: 'error',
        message: 'Resonance results are required for visualization'
      });
    }
    
    // Call the Python script to generate visualization parameters
    const scriptPath = path.join(process.cwd(), 'akashic_vibe_function.py');
    
    // Create a temporary file to store the resonance results
    const tempFilePath = path.join(process.cwd(), 'temp_avf_visualization_input.json');
    fs.writeFileSync(tempFilePath, JSON.stringify({ resonanceResults }));
    
    try {
      // Run the Python script with the input file
      const { stdout, stderr } = await execAsync(`python ${scriptPath} --visualize --input ${tempFilePath} --output-json`);
      
      if (stderr) {
        console.error('AVF Visualization Error:', stderr);
      }
      
      // Parse the output
      let visualizationParams;
      try {
        visualizationParams = JSON.parse(stdout);
      } catch (parseError) {
        console.error('Failed to parse AVF visualization output:', parseError);
        visualizationParams = { 
          status: 'partial_success',
          raw_output: stdout,
          message: 'Visualization parameters generation completed but results could not be fully parsed'
        };
      }
      
      // Clean up
      if (fs.existsSync(tempFilePath)) {
        fs.unlinkSync(tempFilePath);
      }
      
      return res.json({
        status: 'success',
        visualizationParams
      });
      
    } catch (execError) {
      console.error('Failed to generate AVF visualization parameters:', execError);
      return res.status(500).json({
        status: 'error',
        message: 'Failed to generate AVF visualization parameters',
        error: execError.message
      });
    }
  } catch (error) {
    console.error('AVF Visualization Error:', error);
    return res.status(500).json({
      status: 'error',
      message: 'An error occurred during AVF visualization parameters generation',
      error: error.message
    });
  }
});

export default router;