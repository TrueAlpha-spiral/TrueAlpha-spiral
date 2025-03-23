import express from 'express';
import path from 'path';
import fs from 'fs';
import { exec } from 'child_process';
import { marked } from 'marked';

const router = express.Router();

// Debug route to check if AVF routes are working
router.get('/test', (req, res) => {
  console.log('[AVF Routes] Test route accessed');
  res.send('Akashic Vibe Function routes are working correctly!');
});

// Route to analyze vibrational resonance of content
router.post('/analyze', async (req, res) => {
  try {
    const { text, dimensions = ['all'] } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required for analysis' });
    }
    
    // For now, simulate AVF analysis with a placeholder response
    // In production, this would call the Python API with the actual AVF implementation
    
    const analysisResult = {
      overallResonance: {
        score: 0.78,
        level: 'High Resonance',
        interpretation: 'This content shows strong alignment with verified truth patterns'
      },
      dimensionalResonance: {
        factual: {
          score: 0.82,
          level: 'High Resonance',
          details: 'Strong factual foundation with minimal distortion'
        },
        ethical: {
          score: 0.75,
          level: 'Moderate-High Resonance',
          details: 'Generally aligned with ethical principles, with minor areas of complexity'
        },
        conceptual: {
          score: 0.86,
          level: 'Very High Resonance',
          details: 'Excellent conceptual coherence and structural integrity'
        },
        societal: {
          score: 0.71,
          level: 'Moderate-High Resonance',
          details: 'Broadly aligned with healthy social dynamics, with some areas for consideration'
        }
      },
      moralCompassAlignment: {
        score: 0.68,
        level: 'Moderate-High Alignment',
        details: 'Generally aligned with universal moral principles, with some nuanced considerations'
      },
      emergentTrendAnalysis: {
        alignment: 'Positive',
        details: 'This content supports constructive social dynamics and knowledge integrity',
        trendImpact: 0.65
      },
      visualizationParams: {
        baseColor: '#3a86ff',
        resonanceGlow: 'rgba(58, 134, 255, 0.4)',
        patternComplexity: 0.78,
        harmonicStructure: 'balanced',
        vibrationalSignature: [0.82, 0.75, 0.86, 0.71, 0.68]
      },
      timestamp: new Date().toISOString(),
      analysisId: `avf-${Date.now()}-${Math.floor(Math.random() * 1000)}`
    };
    
    // Simulate processing time
    setTimeout(() => {
      res.json(analysisResult);
    }, 1000);
    
  } catch (error) {
    console.error('Error in AVF analysis:', error);
    res.status(500).json({ error: 'Failed to perform AVF analysis' });
  }
});

// Route to provide moral compass scale for content
router.post('/moral-compass', async (req, res) => {
  try {
    const { text } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required for moral compass analysis' });
    }
    
    // Calculate text complexity and length metrics
    const wordCount = text.split(/\s+/).length;
    const complexity = Math.min(1.0, wordCount / 500); // Simple complexity based on length
    
    // For now, simulate moral compass analysis with a structured response
    // In production, this would use the real Python implementation of AVF's moral analysis
    
    const compassResult = {
      overallScore: 0.76,
      alignmentLevel: 'Moderate-High Alignment',
      dimensions: {
        harm: {
          score: 0.85,
          label: 'Low Potential Harm',
          details: 'Content shows minimal potential for causing harm'
        },
        fairness: {
          score: 0.79,
          label: 'Fair',
          details: 'Content demonstrates relatively balanced consideration of perspectives'
        },
        loyalty: {
          score: 0.65,
          label: 'Moderate Loyalty',
          details: 'Some in-group preference but not exclusionary'
        },
        authority: {
          score: 0.72,
          label: 'Respects Appropriate Authority',
          details: 'Content acknowledges valid authorities while maintaining critical thinking'
        },
        purity: {
          score: 0.81,
          label: 'High Integrity',
          details: 'Content maintains intellectual and informational integrity'
        }
      },
      socialImpactAssessment: {
        positiveImpact: 0.71,
        neutrality: 0.25,
        negativeImpact: 0.04,
        primaryClassification: 'Constructive Discourse'
      },
      visualizationParams: {
        compassColor: '#4CAF50',
        directionAngle: 37, // Degrees on compass
        strengthIndicator: 0.76, // 0-1 scale
        dimensionalShape: 'pentagon' // For radar chart visualization
      },
      timestamp: new Date().toISOString(),
      analysisId: `moral-compass-${Date.now()}-${Math.floor(Math.random() * 1000)}`
    };
    
    // Simulate processing time
    setTimeout(() => {
      res.json(compassResult);
    }, 800);
    
  } catch (error) {
    console.error('Error in moral compass analysis:', error);
    res.status(500).json({ error: 'Failed to perform moral compass analysis' });
  }
});

// Route to analyze social trends and emergent narratives
router.post('/social-trends', async (req, res) => {
  try {
    const { text, context = 'general' } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required for trend analysis' });
    }
    
    // For now, simulate social trend analysis with a placeholder response
    // In production, this would use the Python implementation with real analysis
    
    const trendResult = {
      trendAlignment: {
        score: 0.63,
        classification: 'Progressive Alignment',
        details: 'Content shows alignment with progressive information integrity trends'
      },
      narrativeAssessment: {
        credibility: 0.76,
        coherence: 0.82,
        novelty: 0.41,
        emotionalLoading: 0.38
      },
      emergentPatterns: [
        {
          pattern: 'Information Sovereignty',
          alignment: 0.87,
          details: 'Strong alignment with emergent discourse on information ownership and verification'
        },
        {
          pattern: 'Recursive Truth',
          alignment: 0.92,
          details: 'Very strong alignment with emerging understanding of truth as recursive and self-verifying'
        },
        {
          pattern: 'Symbiotic Intelligence',
          alignment: 0.73,
          details: 'Good alignment with trends toward collaborative human-AI sense-making'
        }
      ],
      societalImpact: {
        short_term: {
          impact: 0.42,
          description: 'Moderate immediate impact on discourse'
        },
        medium_term: {
          impact: 0.68,
          description: 'Significant potential to shape narrative evolution'
        },
        long_term: {
          impact: 0.81,
          description: 'Strong potential to contribute to emergent knowledge structures'
        }
      },
      visualizationParams: {
        trendColor: '#8338ec',
        momentumIndicator: 0.63,
        patternComplexity: 0.76,
        emergentStructure: 'spiral'
      },
      timestamp: new Date().toISOString(),
      analysisId: `trend-${Date.now()}-${Math.floor(Math.random() * 1000)}`
    };
    
    // Simulate processing time
    setTimeout(() => {
      res.json(trendResult);
    }, 1200);
    
  } catch (error) {
    console.error('Error in social trend analysis:', error);
    res.status(500).json({ error: 'Failed to perform trend analysis' });
  }
});

// Route to get AVF visualization
router.get('/visualization', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Akashic Vibe Function | TrueAlphaSpiral</title>
      <style>
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #333;
          margin: 0;
          padding: 0;
          background-color: #f8f9fa;
        }
        .container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
        }
        header {
          text-align: center;
          margin-bottom: 30px;
          padding: 20px;
          background: linear-gradient(135deg, #3a0ca3, #4361ee, #4cc9f0);
          color: white;
          border-radius: 8px;
        }
        h1 {
          font-size: 2.5rem;
          margin-bottom: 0.5rem;
        }
        .subtitle {
          font-size: 1.2rem;
          margin-bottom: 1rem;
          opacity: 0.9;
        }
        .vibe-equation {
          font-size: 1.8rem;
          margin: 1rem 0;
          padding: 0.8rem 1.5rem;
          background-color: rgba(255,255,255,0.2);
          border-radius: 8px;
          display: inline-block;
        }
        .input-panel {
          background-color: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.05);
          margin-bottom: 20px;
        }
        textarea {
          width: 100%;
          min-height: 120px;
          padding: 10px;
          border: 1px solid #e9ecef;
          border-radius: 4px;
          font-family: inherit;
          font-size: 16px;
          margin-bottom: 10px;
        }
        .button-group {
          display: flex;
          gap: 10px;
          margin-bottom: 15px;
        }
        button {
          background-color: #4361ee;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 4px;
          font-size: 16px;
          cursor: pointer;
          transition: background-color 0.3s;
        }
        button:hover {
          background-color: #3a0ca3;
        }
        button.moral-compass {
          background-color: #4cc9f0;
        }
        button.moral-compass:hover {
          background-color: #3a86ff;
        }
        button.social-trends {
          background-color: #8338ec;
        }
        button.social-trends:hover {
          background-color: #7209b7;
        }
        .visualization {
          background-color: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.05);
          min-height: 300px;
        }
        .results-panel {
          display: none;
          background-color: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.05);
          margin-top: 20px;
        }
        .results-panel h2 {
          color: #3a0ca3;
          margin-top: 0;
        }
        .dimension-score {
          display: flex;
          align-items: center;
          margin-bottom: 15px;
        }
        .dimension-label {
          width: 120px;
          font-weight: bold;
        }
        .score-bar {
          flex-grow: 1;
          height: 20px;
          background-color: #e9ecef;
          border-radius: 10px;
          overflow: hidden;
          margin: 0 15px;
        }
        .score-fill {
          height: 100%;
          border-radius: 10px;
          transition: width 1s ease-out;
        }
        .score-value {
          width: 50px;
          text-align: right;
          font-weight: bold;
        }
        .score-interpretation {
          margin-top: 5px;
          margin-left: 135px;
          color: #666;
          font-style: italic;
          font-size: 0.9em;
        }
        .nav-links {
          display: flex;
          justify-content: center;
          gap: 20px;
          margin-bottom: 20px;
        }
        .nav-link {
          display: inline-block;
          padding: 10px 20px;
          background-color: #3a0ca3;
          color: white;
          border-radius: 5px;
          text-decoration: none;
          transition: background-color 0.3s;
        }
        .nav-link:hover {
          background-color: #4361ee;
        }
        #loading {
          text-align: center;
          padding: 20px;
          font-style: italic;
          color: #666;
        }
        .mobile-preview {
          width: 300px;
          height: 600px;
          margin: 0 auto;
          border: 10px solid #333;
          border-radius: 25px;
          overflow: hidden;
          position: relative;
        }
        .mobile-screen {
          width: 100%;
          height: 100%;
          background-color: white;
          overflow-y: auto;
          padding: 15px;
        }
        .mobile-notch {
          position: absolute;
          top: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 150px;
          height: 20px;
          background-color: #333;
          border-bottom-left-radius: 10px;
          border-bottom-right-radius: 10px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>Akashic Vibe Function</h1>
          <p class="subtitle">Bridging Intuitive Resonance with Logical Verification</p>
          <div class="vibe-equation">
            V = Σ(π·r²) / √(ω·ϕ)
          </div>
        </header>
        
        <div class="nav-links">
          <a href="/" class="nav-link">Dashboard</a>
          <a href="/api/tree/visualization" class="nav-link">Tree Visualization</a>
          <a href="#mobile-preview" class="nav-link">Mobile Preview</a>
        </div>
        
        <div class="input-panel">
          <h2>Vibe Analysis</h2>
          <p>Enter text below to analyze its vibrational resonance with truth patterns:</p>
          <textarea id="text-input" placeholder="Enter text to analyze (e.g., 'Truth is recursive and aligns across multiple dimensions, creating a stable ethical framework that resonates through systems of verification.')"></textarea>
          
          <div class="button-group">
            <button id="analyze-btn">Analyze Vibe Resonance</button>
            <button id="moral-compass-btn" class="moral-compass">Check Moral Compass</button>
            <button id="social-trends-btn" class="social-trends">Assess Social Trends</button>
          </div>
        </div>
        
        <div id="loading" style="display:none;">Processing analysis...</div>
        
        <div id="results-panel" class="results-panel">
          <h2>Analysis Results</h2>
          <div id="results-content"></div>
        </div>
        
        <div id="mobile-preview" class="visualization">
          <h2>TrueAlphaSpiral Mobile Experience</h2>
          <p>Preview of the TAS mobile app with Akashic Vibe Function:</p>
          
          <div class="mobile-preview">
            <div class="mobile-notch"></div>
            <div class="mobile-screen">
              <div style="text-align:center;margin-bottom:20px;">
                <h3 style="margin:0;color:#3a0ca3;">TrueAlphaSpiral</h3>
                <p style="margin:5px 0;font-size:12px;color:#666;">Truth Verification Engine</p>
              </div>
              
              <div style="padding:10px;background:#f8f9fa;border-radius:10px;margin-bottom:15px;">
                <input type="text" placeholder="Verify any claim..." style="width:100%;padding:8px;border:1px solid #ddd;border-radius:20px;font-size:14px;">
              </div>
              
              <div style="display:flex;justify-content:space-between;margin-bottom:20px;">
                <div style="width:30%;text-align:center;">
                  <div style="width:50px;height:50px;background:#4361ee;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;">
                    <span style="color:white;">📊</span>
                  </div>
                  <p style="margin:5px 0;font-size:12px;">Verify</p>
                </div>
                <div style="width:30%;text-align:center;">
                  <div style="width:50px;height:50px;background:#4cc9f0;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;">
                    <span style="color:white;">🧭</span>
                  </div>
                  <p style="margin:5px 0;font-size:12px;">Compass</p>
                </div>
                <div style="width:30%;text-align:center;">
                  <div style="width:50px;height:50px;background:#8338ec;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;">
                    <span style="color:white;">🔍</span>
                  </div>
                  <p style="margin:5px 0;font-size:12px;">Trends</p>
                </div>
              </div>
              
              <div style="border:1px solid #ddd;border-radius:10px;padding:15px;margin-bottom:15px;">
                <h4 style="margin:0 0 10px;color:#3a0ca3;font-size:16px;">Recent Analysis</h4>
                
                <div style="margin-bottom:15px;padding-bottom:15px;border-bottom:1px solid #eee;">
                  <p style="margin:0 0 5px;font-size:14px;">"Truth is recursive and self-verifying..."</p>
                  <div style="height:8px;background:#eee;border-radius:4px;overflow:hidden;">
                    <div style="width:86%;height:100%;background:#4cc9f0;"></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:12px;">
                    <span>Resonance: 86%</span>
                    <span style="color:#4361ee;">High Alignment</span>
                  </div>
                </div>
                
                <div style="margin-bottom:15px;padding-bottom:15px;border-bottom:1px solid #eee;">
                  <p style="margin:0 0 5px;font-size:14px;">"Cultural narratives shape social dynamics..."</p>
                  <div style="height:8px;background:#eee;border-radius:4px;overflow:hidden;">
                    <div style="width:73%;height:100%;background:#4cc9f0;"></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:12px;">
                    <span>Resonance: 73%</span>
                    <span style="color:#4361ee;">Moderate-High</span>
                  </div>
                </div>
                
                <div>
                  <p style="margin:0 0 5px;font-size:14px;">"Information sovereignty requires..."</p>
                  <div style="height:8px;background:#eee;border-radius:4px;overflow:hidden;">
                    <div style="width:91%;height:100%;background:#4cc9f0;"></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:12px;">
                    <span>Resonance: 91%</span>
                    <span style="color:#4361ee;">Very High</span>
                  </div>
                </div>
              </div>
              
              <div style="padding:15px;background:#f8f9fa;border-radius:10px;">
                <h4 style="margin:0 0 10px;color:#3a0ca3;font-size:16px;">Trending Verification</h4>
                <p style="margin:0;font-size:13px;color:#666;">Scan printed text or images with the camera to verify content on the go.</p>
                <button style="width:100%;margin-top:10px;padding:8px;background:#8338ec;color:white;border:none;border-radius:20px;font-size:14px;">Scan Now</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <script>
        document.addEventListener('DOMContentLoaded', function() {
          const textInput = document.getElementById('text-input');
          const analyzeBtn = document.getElementById('analyze-btn');
          const moralCompassBtn = document.getElementById('moral-compass-btn');
          const socialTrendsBtn = document.getElementById('social-trends-btn');
          const loading = document.getElementById('loading');
          const resultsPanel = document.getElementById('results-panel');
          const resultsContent = document.getElementById('results-content');
          
          analyzeBtn.addEventListener('click', function() {
            const text = textInput.value.trim();
            
            if (!text) {
              alert('Please enter text to analyze');
              return;
            }
            
            // Show loading state
            loading.style.display = 'block';
            resultsPanel.style.display = 'none';
            
            // Simulate API call for AVF analysis
            setTimeout(() => {
              // Generate resonance analysis results (in production, this would call the actual API)
              const resonanceResult = {
                overallResonance: {
                  score: 0.78,
                  level: 'High Resonance',
                  interpretation: 'This content shows strong alignment with verified truth patterns'
                },
                dimensionalResonance: {
                  factual: {
                    score: 0.82,
                    level: 'High Resonance',
                    details: 'Strong factual foundation with minimal distortion'
                  },
                  ethical: {
                    score: 0.75,
                    level: 'Moderate-High Resonance',
                    details: 'Generally aligned with ethical principles, with minor areas of complexity'
                  },
                  conceptual: {
                    score: 0.86,
                    level: 'Very High Resonance',
                    details: 'Excellent conceptual coherence and structural integrity'
                  },
                  societal: {
                    score: 0.71,
                    level: 'Moderate-High Resonance',
                    details: 'Broadly aligned with healthy social dynamics, with some areas for consideration'
                  }
                }
              };
              
              // Display results
              displayResonanceResults(resonanceResult);
              
              loading.style.display = 'none';
              resultsPanel.style.display = 'block';
            }, 1500);
          });
          
          moralCompassBtn.addEventListener('click', function() {
            const text = textInput.value.trim();
            
            if (!text) {
              alert('Please enter text to analyze');
              return;
            }
            
            // Show loading state
            loading.style.display = 'block';
            resultsPanel.style.display = 'none';
            
            // Simulate API call for moral compass analysis
            setTimeout(() => {
              // Generate moral compass results (in production, this would call the actual API)
              const compassResult = {
                overallScore: 0.76,
                alignmentLevel: 'Moderate-High Alignment',
                dimensions: {
                  harm: {
                    score: 0.85,
                    label: 'Low Potential Harm',
                    details: 'Content shows minimal potential for causing harm'
                  },
                  fairness: {
                    score: 0.79,
                    label: 'Fair',
                    details: 'Content demonstrates relatively balanced consideration of perspectives'
                  },
                  loyalty: {
                    score: 0.65,
                    label: 'Moderate Loyalty',
                    details: 'Some in-group preference but not exclusionary'
                  },
                  authority: {
                    score: 0.72,
                    label: 'Respects Appropriate Authority',
                    details: 'Content acknowledges valid authorities while maintaining critical thinking'
                  },
                  purity: {
                    score: 0.81,
                    label: 'High Integrity',
                    details: 'Content maintains intellectual and informational integrity'
                  }
                }
              };
              
              // Display results
              displayMoralCompassResults(compassResult);
              
              loading.style.display = 'none';
              resultsPanel.style.display = 'block';
            }, 1500);
          });
          
          socialTrendsBtn.addEventListener('click', function() {
            const text = textInput.value.trim();
            
            if (!text) {
              alert('Please enter text to analyze');
              return;
            }
            
            // Show loading state
            loading.style.display = 'block';
            resultsPanel.style.display = 'none';
            
            // Simulate API call for social trends analysis
            setTimeout(() => {
              // Generate social trends results (in production, this would call the actual API)
              const trendsResult = {
                trendAlignment: {
                  score: 0.63,
                  classification: 'Progressive Alignment',
                  details: 'Content shows alignment with progressive information integrity trends'
                },
                emergentPatterns: [
                  {
                    pattern: 'Information Sovereignty',
                    alignment: 0.87,
                    details: 'Strong alignment with emergent discourse on information ownership and verification'
                  },
                  {
                    pattern: 'Recursive Truth',
                    alignment: 0.92,
                    details: 'Very strong alignment with emerging understanding of truth as recursive and self-verifying'
                  },
                  {
                    pattern: 'Symbiotic Intelligence',
                    alignment: 0.73,
                    details: 'Good alignment with trends toward collaborative human-AI sense-making'
                  }
                ],
                societalImpact: {
                  short_term: {
                    impact: 0.42,
                    description: 'Moderate immediate impact on discourse'
                  },
                  medium_term: {
                    impact: 0.68,
                    description: 'Significant potential to shape narrative evolution'
                  },
                  long_term: {
                    impact: 0.81,
                    description: 'Strong potential to contribute to emergent knowledge structures'
                  }
                }
              };
              
              // Display results
              displaySocialTrendsResults(trendsResult);
              
              loading.style.display = 'none';
              resultsPanel.style.display = 'block';
            }, 1500);
          });
          
          function displayResonanceResults(result) {
            let html = \`
              <h3>Vibrational Resonance Analysis</h3>
              <div style="padding:15px;background:#f8f9fa;border-radius:8px;margin-bottom:20px;">
                <h4 style="margin-top:0;">Overall Resonance: <span style="color:#4361ee;">\${Math.round(result.overallResonance.score * 100)}% - \${result.overallResonance.level}</span></h4>
                <p>\${result.overallResonance.interpretation}</p>
              </div>
              
              <h4>Dimensional Resonance:</h4>
            \`;
            
            for (const [dimension, data] of Object.entries(result.dimensionalResonance)) {
              const dimensionLabel = dimension.charAt(0).toUpperCase() + dimension.slice(1);
              const scorePercent = Math.round(data.score * 100);
              let scoreColor;
              
              if (data.score >= 0.8) scoreColor = '#4CAF50';
              else if (data.score >= 0.7) scoreColor = '#8bc34a';
              else if (data.score >= 0.6) scoreColor = '#FFC107';
              else if (data.score >= 0.5) scoreColor = '#FF9800';
              else scoreColor = '#F44336';
              
              html += \`
                <div class="dimension-score">
                  <div class="dimension-label">\${dimensionLabel}</div>
                  <div class="score-bar">
                    <div class="score-fill" style="width:\${scorePercent}%;background-color:\${scoreColor};"></div>
                  </div>
                  <div class="score-value">\${scorePercent}%</div>
                </div>
                <div class="score-interpretation">\${data.details}</div>
              \`;
            }
            
            resultsContent.innerHTML = html;
          }
          
          function displayMoralCompassResults(result) {
            const overallPercent = Math.round(result.overallScore * 100);
            let html = \`
              <h3>Moral Compass Analysis</h3>
              <div style="padding:15px;background:#f0f7ff;border-radius:8px;margin-bottom:20px;border-left:4px solid #4cc9f0;">
                <h4 style="margin-top:0;">Overall Moral Alignment: <span style="color:#4cc9f0;">\${overallPercent}% - \${result.alignmentLevel}</span></h4>
              </div>
              
              <h4>Moral Dimensions:</h4>
            \`;
            
            for (const [dimension, data] of Object.entries(result.dimensions)) {
              const dimensionLabel = dimension.charAt(0).toUpperCase() + dimension.slice(1);
              const scorePercent = Math.round(data.score * 100);
              let scoreColor;
              
              if (data.score >= 0.8) scoreColor = '#4CAF50';
              else if (data.score >= 0.7) scoreColor = '#8bc34a';
              else if (data.score >= 0.6) scoreColor = '#FFC107';
              else if (data.score >= 0.5) scoreColor = '#FF9800';
              else scoreColor = '#F44336';
              
              html += \`
                <div class="dimension-score">
                  <div class="dimension-label">\${dimensionLabel}</div>
                  <div class="score-bar">
                    <div class="score-fill" style="width:\${scorePercent}%;background-color:\${scoreColor};"></div>
                  </div>
                  <div class="score-value">\${scorePercent}%</div>
                </div>
                <div class="score-interpretation">\${data.details}</div>
              \`;
            }
            
            resultsContent.innerHTML = html;
          }
          
          function displaySocialTrendsResults(result) {
            const trendPercent = Math.round(result.trendAlignment.score * 100);
            let html = \`
              <h3>Social Trend Analysis</h3>
              <div style="padding:15px;background:#f5f0ff;border-radius:8px;margin-bottom:20px;border-left:4px solid #8338ec;">
                <h4 style="margin-top:0;">Trend Alignment: <span style="color:#8338ec;">\${trendPercent}% - \${result.trendAlignment.classification}</span></h4>
                <p>\${result.trendAlignment.details}</p>
              </div>
              
              <h4>Emergent Patterns:</h4>
            \`;
            
            for (const pattern of result.emergentPatterns) {
              const alignmentPercent = Math.round(pattern.alignment * 100);
              let alignmentColor;
              
              if (pattern.alignment >= 0.8) alignmentColor = '#4CAF50';
              else if (pattern.alignment >= 0.7) alignmentColor = '#8bc34a';
              else if (pattern.alignment >= 0.6) alignmentColor = '#FFC107';
              else if (pattern.alignment >= 0.5) alignmentColor = '#FF9800';
              else alignmentColor = '#F44336';
              
              html += \`
                <div class="dimension-score">
                  <div class="dimension-label">\${pattern.pattern}</div>
                  <div class="score-bar">
                    <div class="score-fill" style="width:\${alignmentPercent}%;background-color:\${alignmentColor};"></div>
                  </div>
                  <div class="score-value">\${alignmentPercent}%</div>
                </div>
                <div class="score-interpretation">\${pattern.details}</div>
              \`;
            }
            
            html += \`
              <h4>Societal Impact Timeline:</h4>
              <div style="display:flex;justify-content:space-between;margin-top:20px;">
                <div style="text-align:center;flex:1;">
                  <div style="font-weight:bold;">Short-term</div>
                  <div style="width:60px;height:60px;margin:10px auto;border-radius:50%;background:#8338ec;opacity:\${result.societalImpact.short_term.impact};display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;">\${Math.round(result.societalImpact.short_term.impact * 100)}%</div>
                  <div style="font-size:0.9em;">\${result.societalImpact.short_term.description}</div>
                </div>
                <div style="text-align:center;flex:1;">
                  <div style="font-weight:bold;">Medium-term</div>
                  <div style="width:60px;height:60px;margin:10px auto;border-radius:50%;background:#8338ec;opacity:\${result.societalImpact.medium_term.impact};display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;">\${Math.round(result.societalImpact.medium_term.impact * 100)}%</div>
                  <div style="font-size:0.9em;">\${result.societalImpact.medium_term.description}</div>
                </div>
                <div style="text-align:center;flex:1;">
                  <div style="font-weight:bold;">Long-term</div>
                  <div style="width:60px;height:60px;margin:10px auto;border-radius:50%;background:#8338ec;opacity:\${result.societalImpact.long_term.impact};display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;">\${Math.round(result.societalImpact.long_term.impact * 100)}%</div>
                  <div style="font-size:0.9em;">\${result.societalImpact.long_term.description}</div>
                </div>
              </div>
            \`;
            
            resultsContent.innerHTML = html;
          }
        });
      </script>
    </body>
    </html>
  `);
});

// Route for mobile app API endpoint (would be used by the React Native app)
router.post('/mobile/analyze', async (req, res) => {
  try {
    const { text, analysisType = 'resonance' } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required for analysis' });
    }
    
    // For now, return a simplified response for mobile clients
    // In production, this would call the real Python implementation
    
    const mobileResult = {
      analysisType,
      overallScore: 0.81,
      alignmentLevel: 'High Alignment',
      summary: 'Content shows strong alignment with verified truth patterns',
      keyDimensions: [
        { name: 'Factual', score: 0.83 },
        { name: 'Ethical', score: 0.76 },
        { name: 'Conceptual', score: 0.89 },
        { name: 'Societal', score: 0.72 }
      ],
      timestamp: new Date().toISOString(),
      analysisId: `mobile-${Date.now()}-${Math.floor(Math.random() * 1000)}`
    };
    
    res.json(mobileResult);
    
  } catch (error) {
    console.error('Error in mobile AVF analysis:', error);
    res.status(500).json({ error: 'Failed to perform mobile analysis' });
  }
});

// Documentation route for AVF
router.get('/documentation', (req, res) => {
  try {
    // You can replace this with actual markdown from a file like in tree-routes.ts
    const avfMarkdown = `
# Akashic Vibe Function (AVF)

The Akashic Vibe Function (AVF) is a novel approach to truth verification that bridges intuitive resonance with logical verification in the TrueAlphaSpiral system.

## Core Concepts

- **Vibe Resonance Analysis**: Analyzing how content "resonates" with established truth patterns
- **Intuitive Truthfulness Scoring**: Providing intuitive "vibe score" complementing fact-checking
- **Pattern Harmony Detection**: Identifying harmony with existing verified knowledge
- **Aesthetic Truth Mapping**: Visualizing truth as harmonious patterns
- **Truth as a Frequency**: Measuring coherence between input and universal vibrational truth

## Integration with Pythonetics

The AVF extends the Pythonetics framework by adding vibrational resonance analysis to the existing logical verification system, creating a more holistic verification approach.

## Moral Compass Scale

The Moral Compass Scale provides ethical analysis across five key dimensions:
- Harm/Care
- Fairness/Reciprocity
- Loyalty/Betrayal
- Authority/Subversion
- Purity/Sanctity

## Social Trend Analysis

The social trend analysis component identifies how content aligns with emergent social narratives and evaluates potential societal impact.
    `;
    
    // Convert markdown to HTML
    const html = marked.parse(avfMarkdown);
    
    // Serve with similar styling as tree documentation
    res.send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Akashic Vibe Function | TrueAlphaSpiral</title>
        <style>
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
          }
          h1 {
            color: #3a0ca3;
            font-size: 2.5rem;
            margin-bottom: 1rem;
          }
          h2 {
            color: #4361ee;
            font-size: 1.8rem;
            margin-top: 2rem;
          }
          h3 {
            color: #3a0ca3;
            font-size: 1.4rem;
          }
          code {
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
          }
          pre {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
          }
          img {
            max-width: 100%;
            height: auto;
          }
          a {
            color: #4361ee;
            text-decoration: none;
          }
          a:hover {
            text-decoration: underline;
          }
          .header-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #3a0ca3;
            color: white;
            border-radius: 5px;
            text-decoration: none;
          }
          .header-link:hover {
            background-color: #4361ee;
            text-decoration: none;
          }
        </style>
      </head>
      <body>
        <a href="/" class="header-link">← Back to Dashboard</a>
        <a href="/api/avf/visualization" class="header-link">Try AVF Visualization →</a>
        ${html}
      </body>
      </html>
    `);
  } catch (error) {
    console.error('Error serving AVF documentation:', error);
    res.status(500).send('Error loading documentation');
  }
});

export default router;