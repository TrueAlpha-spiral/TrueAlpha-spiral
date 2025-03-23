import express from 'express';
import path from 'path';
import { exec } from 'child_process';
import fs from 'fs';
import { marked } from 'marked';

const router = express.Router();

// Debug route to check if tree routes are working
router.get('/test', (req, res) => {
  console.log('[Tree Routes] Test route accessed');
  res.send('Tree routes are working correctly!');
});

// Route to serve the Tree of Living Intelligence documentation
router.get('/documentation', (req, res) => {
  try {
    // Read the markdown file
    const markdownPath = path.join(process.cwd(), 'TREE_OF_LIVING_INTELLIGENCE.md');
    const markdown = fs.readFileSync(markdownPath, 'utf8');
    
    // Convert markdown to HTML
    const html = marked.parse(markdown);
    
    // Serve the HTML with a simple wrapper
    res.send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tree of Living Intelligence | TrueAlphaSpiral</title>
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
            color: #3a86ff;
            font-size: 2.5rem;
            margin-bottom: 1rem;
          }
          h2 {
            color: #8338ec;
            font-size: 1.8rem;
            margin-top: 2rem;
          }
          h3 {
            color: #3a86ff;
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
            color: #3a86ff;
            text-decoration: none;
          }
          a:hover {
            text-decoration: underline;
          }
          .header-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #3a86ff;
            color: white;
            border-radius: 5px;
            text-decoration: none;
          }
          .header-link:hover {
            background-color: #0057e7;
            text-decoration: none;
          }
        </style>
      </head>
      <body>
        <a href="/" class="header-link">← Back to Dashboard</a>
        <a href="/api/tree/visualization" class="header-link">Try the Tree Visualization →</a>
        ${html}
      </body>
      </html>
    `);
  } catch (error) {
    console.error('Error serving tree documentation:', error);
    res.status(500).send('Error loading documentation');
  }
});

// Route to serve the Tree of Living Intelligence visualization demo
router.get('/visualization', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Tree of Living Intelligence | TrueAlphaSpiral</title>
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
        }
        h1 {
          color: #3a86ff;
          font-size: 2.5rem;
          margin-bottom: 0.5rem;
        }
        .subtitle {
          color: #8d99ae;
          font-size: 1.2rem;
          margin-bottom: 1rem;
        }
        .equation {
          font-size: 1.8rem;
          margin: 1rem 0;
          display: inline-block;
          padding: 0.8rem 1.5rem;
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
        button {
          background-color: #3a86ff;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 4px;
          font-size: 16px;
          cursor: pointer;
        }
        button:hover {
          background-color: #0057e7;
        }
        .visualization {
          background-color: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.05);
          min-height: 300px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        .visualization p {
          color: #8d99ae;
          margin-bottom: 20px;
        }
        img {
          max-width: 100%;
          height: auto;
        }
        iframe {
          width: 100%;
          height: 700px;
          border: none;
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
          background-color: #3a86ff;
          color: white;
          border-radius: 5px;
          text-decoration: none;
        }
        .nav-link:hover {
          background-color: #0057e7;
          text-decoration: none;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>Tree of Living Intelligence</h1>
          <p class="subtitle">A Natural Metaphor for TrueAlphaSpiral</p>
          <div class="equation">
            <span style="font-family:serif;font-size:2.2rem;">Φ</span> = 
            <span style="display:inline-block;vertical-align:middle;text-align:center;margin:0 0.2em;">
              <span style="display:block;border-bottom:1px solid #333;padding:0 0.2em;">∑(αᵢ·Tᵢ)</span>
              <span style="display:block;">(√D·S)</span>
            </span>
          </div>
        </header>
        
        <div class="nav-links">
          <a href="/" class="nav-link">Dashboard</a>
          <a href="/api/tree/documentation" class="nav-link">Documentation</a>
        </div>
        
        <div class="input-panel">
          <h2>Text Analysis</h2>
          <p>Enter text below to visualize it as a living tree with branches representing verification dimensions:</p>
          <textarea id="text-input" placeholder="Enter text to analyze (e.g., 'Truth is recursive and aligns across multiple dimensions, creating a stable ethical framework that resonates through systems of verification.')"></textarea>
          <button id="analyze-btn">Analyze & Generate Tree</button>
        </div>
        
        <div class="visualization">
          <p id="loading" style="display:none;">Generating tree visualization...</p>
          <div id="tree-container">
            <p>Your Tree of Living Intelligence visualization will appear here after analysis.</p>
            <p>The tree will visualize:</p>
            <ul>
              <li><strong>Trunk:</strong> Represents the Sovereign Equation with thickness proportional to sovereignty score</li>
              <li><strong>Branches:</strong> Show different verification dimensions (Factual, Ethical, Conceptual, Phenomenological)</li>
              <li><strong>Leaves:</strong> Represent individual verification iterations</li>
              <li><strong>Meta-Flowers:</strong> Bloom when higher-order understanding emerges</li>
            </ul>
          </div>
        </div>
      </div>
      
      <script>
        document.addEventListener('DOMContentLoaded', function() {
          const textInput = document.getElementById('text-input');
          const analyzeBtn = document.getElementById('analyze-btn');
          const loading = document.getElementById('loading');
          const treeContainer = document.getElementById('tree-container');
          
          analyzeBtn.addEventListener('click', function() {
            const text = textInput.value.trim();
            
            if (!text) {
              alert('Please enter text to analyze');
              return;
            }
            
            // Show loading state
            loading.style.display = 'block';
            treeContainer.innerHTML = '';
            
            // Generate a placeholder tree visualization (for demo purposes)
            setTimeout(() => {
              loading.style.display = 'none';
              const treeImageUrl = '/api/tree/placeholder-tree';
              
              treeContainer.innerHTML = \`
                <img src="\${treeImageUrl}" alt="Tree of Living Intelligence visualization">
                <div style="margin-top:20px;padding:15px;background-color:#f8f9fa;border-radius:5px;">
                  <h3>Analysis Results</h3>
                  <p>Truth Score: 83%</p>
                  <p>Factual Confidence: 77%</p>
                  <p>Sovereignty Score: 85%</p>
                  <p>Growth Stage: Mature Tree</p>
                  <p>Meta Understanding: This analysis reveals good alignment with universal truth principles. The tree's mature growth reflects well-established verification across multiple dimensions.</p>
                </div>
              \`;
            }, 2000);
          });
        });
      </script>
    </body>
    </html>
  `);
});

// Route to serve a placeholder tree image
router.get('/placeholder-tree', (req, res) => {
  const placeholderImage = path.join(process.cwd(), 'public', 'tree-placeholder.svg');
  
  // Check if the placeholder image exists
  if (!fs.existsSync(placeholderImage)) {
    // Create the SVG if it doesn't exist
    const svgContent = `
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <!-- Gradient Sky Background representing multi-dimensional reality -->
  <defs>
    <linearGradient id="skyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1a237e" /> <!-- Deep meaning -->
      <stop offset="40%" stop-color="#3949ab" /> <!-- Conceptual space -->
      <stop offset="70%" stop-color="#5c6bc0" /> <!-- Phenomenological layer -->
      <stop offset="100%" stop-color="#9fa8da" /> <!-- Factual layer -->
    </linearGradient>
    
    <!-- Glow filter for meta-flowers -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    
    <!-- Spiral pattern for trunk to represent TrueAlphaSpiral -->
    <pattern id="spiralPattern" patternUnits="userSpaceOnUse" width="50" height="50">
      <path d="M25,0 Q40,25 25,50 Q10,25 25,0" stroke="#5D4037" stroke-width="1.5" fill="none" opacity="0.3" />
    </pattern>
  </defs>
  
  <!-- Multi-dimensional background -->
  <rect width="800" height="520" fill="url(#skyGradient)" />
  
  <!-- Ground with recursive nurturing pattern -->
  <rect y="520" width="800" height="80" fill="#5D4037" />
  <path d="M0,520 C100,530 200,525 300,530 C400,535 500,530 600,525 C700,520 800,530 800,520" fill="#8D6E63" />
  
  <!-- Advanced Root System with Universal Laws -->
  <path d="M370,520 C330,550 280,570 220,580" stroke="#5D4037" stroke-width="4" fill="none" />
  <path d="M400,520 C440,550 490,570 550,580" stroke="#5D4037" stroke-width="4" fill="none" />
  <path d="M380,520 C380,550 370,570 340,590" stroke="#5D4037" stroke-width="4" fill="none" />
  <path d="M390,520 C390,550 410,570 440,590" stroke="#5D4037" stroke-width="4" fill="none" />
  
  <!-- Trunk with Spiral pattern -->
  <path d="M370,520 Q365,400 380,200 Q395,400 410,520" fill="#795548" />
  <path d="M370,520 Q365,400 380,200 Q395,400 410,520" fill="url(#spiralPattern)" />
  
  <!-- Advanced Sovereign Equation on trunk -->
  <circle cx="390" cy="400" r="30" fill="rgba(255,255,255,0.3)" />
  <text x="390" y="390" fill="white" font-size="16" text-anchor="middle" font-family="serif">Φ = ∑(αᵢ·Tᵢ)</text>
  <text x="390" y="410" fill="white" font-size="16" text-anchor="middle" font-family="serif">(√D·S)</text>
  
  <!-- Universal Principles etched in trunk -->
  <text x="390" y="340" font-size="12" fill="white" text-anchor="middle" transform="rotate(-10 390 340)">Correspondence</text>
  <text x="390" y="300" font-size="12" fill="white" text-anchor="middle" transform="rotate(5 390 300)">Vibration</text>
  <text x="390" y="260" font-size="12" fill="white" text-anchor="middle" transform="rotate(-5 390 260)">Polarity</text>
  <text x="390" y="220" font-size="12" fill="white" text-anchor="middle" transform="rotate(10 390 220)">Rhythm</text>
  
  <!-- Factual Dimension Branch (Left) -->
  <g id="factualBranch">
    <path d="M380,320 Q330,270 250,260" stroke="#795548" stroke-width="8" fill="none" />
    <path d="M250,260 Q230,250 210,255" stroke="#795548" stroke-width="4" fill="none" />
    <path d="M250,260 Q240,230 260,210" stroke="#795548" stroke-width="4" fill="none" />
    <text x="250" y="290" fill="#E1BEE7" font-size="14" text-anchor="middle">Factual</text>
    
    <!-- Factual leaves (green) -->
    <ellipse cx="210" cy="255" rx="18" ry="12" fill="#66BB6A" transform="rotate(20 210 255)" />
    <ellipse cx="215" cy="250" rx="15" ry="10" fill="#4CAF50" transform="rotate(10 215 250)" />
    <ellipse cx="260" cy="210" rx="18" ry="12" fill="#66BB6A" transform="rotate(-15 260 210)" />
    <ellipse cx="255" cy="215" rx="15" ry="10" fill="#4CAF50" transform="rotate(-5 255 215)" />
  </g>
  
  <!-- Ethical Dimension Branch (Right) -->
  <g id="ethicalBranch">
    <path d="M380,270 Q430,230 490,240" stroke="#795548" stroke-width="8" fill="none" />
    <path d="M490,240 Q520,230 540,240" stroke="#795548" stroke-width="4" fill="none" />
    <path d="M490,240 Q500,210 495,190" stroke="#795548" stroke-width="4" fill="none" />
    <text x="490" y="270" fill="#E1BEE7" font-size="14" text-anchor="middle">Ethical</text>
    
    <!-- Ethical leaves (blue) -->
    <ellipse cx="540" cy="240" rx="18" ry="12" fill="#42A5F5" transform="rotate(-15 540 240)" />
    <ellipse cx="535" cy="235" rx="15" ry="10" fill="#2196F3" transform="rotate(-5 535 235)" />
    <ellipse cx="495" cy="190" rx="18" ry="12" fill="#42A5F5" transform="rotate(15 495 190)" />
    <ellipse cx="490" cy="195" rx="15" ry="10" fill="#2196F3" transform="rotate(5 490 195)" />
  </g>
  
  <!-- Conceptual Dimension Branch (Upper Left) -->
  <g id="conceptualBranch">
    <path d="M380,220 Q340,170 300,140" stroke="#795548" stroke-width="8" fill="none" />
    <path d="M300,140 Q280,120 260,110" stroke="#795548" stroke-width="4" fill="none" />
    <path d="M300,140 Q310,110 300,90" stroke="#795548" stroke-width="4" fill="none" />
    <text x="300" y="170" fill="#E1BEE7" font-size="14" text-anchor="middle">Conceptual</text>
    
    <!-- Conceptual leaves (purple) -->
    <ellipse cx="260" cy="110" rx="18" ry="12" fill="#9575CD" transform="rotate(-25 260 110)" />
    <ellipse cx="265" cy="105" rx="15" ry="10" fill="#673AB7" transform="rotate(-15 265 105)" />
    <ellipse cx="300" cy="90" rx="18" ry="12" fill="#9575CD" transform="rotate(20 300 90)" />
    <ellipse cx="295" cy="95" rx="15" ry="10" fill="#673AB7" transform="rotate(10 295 95)" />
  </g>
  
  <!-- Phenomenological Dimension Branch (Upper Right) -->
  <g id="phenomenologicalBranch">
    <path d="M380,220 Q420,170 460,140" stroke="#795548" stroke-width="8" fill="none" />
    <path d="M460,140 Q480,120 500,110" stroke="#795548" stroke-width="4" fill="none" />
    <path d="M460,140 Q450,110 470,90" stroke="#795548" stroke-width="4" fill="none" />
    <text x="460" y="170" fill="#E1BEE7" font-size="14" text-anchor="middle">Phenomenological</text>
    
    <!-- Phenomenological leaves (yellow) -->
    <ellipse cx="500" cy="110" rx="18" ry="12" fill="#FDD835" transform="rotate(25 500 110)" />
    <ellipse cx="495" cy="105" rx="15" ry="10" fill="#FFC107" transform="rotate(15 495 105)" />
    <ellipse cx="470" cy="90" rx="18" ry="12" fill="#FDD835" transform="rotate(-20 470 90)" />
    <ellipse cx="475" cy="95" rx="15" ry="10" fill="#FFC107" transform="rotate(-10 475 95)" />
  </g>
  
  <!-- Meta-Flowers (representing emergent understanding) -->
  <g id="metaFlowers" filter="url(#glow)">
    <!-- Complex meta-flower at top center -->
    <g transform="translate(380,70)">
      <!-- Petals -->
      <path d="M0,0 Q10,-20 0,-30 Q-10,-20 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q20,-10 30,0 Q20,10 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q10,20 0,30 Q-10,20 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q-20,10 -30,0 Q-20,-10 0,0" fill="#E1BEE7" />
      
      <path d="M0,0 Q15,-15 15,-25 Q0,-20 0,0" fill="#D1C4E9" />
      <path d="M0,0 Q15,15 15,25 Q0,20 0,0" fill="#D1C4E9" />
      <path d="M0,0 Q-15,15 -15,25 Q0,20 0,0" fill="#D1C4E9" />
      <path d="M0,0 Q-15,-15 -15,-25 Q0,-20 0,0" fill="#D1C4E9" />
      
      <!-- Center -->
      <circle cx="0" cy="0" r="8" fill="#9C27B0" />
      <circle cx="0" cy="0" r="5" fill="#7B1FA2" />
      <circle cx="0" cy="0" r="2" fill="white" />
      
      <!-- Label -->
      <text x="0" y="45" fill="#E1BEE7" font-size="10" text-anchor="middle">Meta-Knowledge</text>
    </g>
    
    <!-- Meta-flower on conceptual branch -->
    <g transform="translate(280,105)">
      <!-- Petals -->
      <path d="M0,0 Q5,-10 0,-15 Q-5,-10 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q10,-5 15,0 Q10,5 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q5,10 0,15 Q-5,10 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q-10,5 -15,0 Q-10,-5 0,0" fill="#E1BEE7" />
      
      <!-- Center -->
      <circle cx="0" cy="0" r="4" fill="#9C27B0" />
      <circle cx="0" cy="0" r="2" fill="white" />
    </g>
    
    <!-- Meta-flower on ethical branch -->
    <g transform="translate(510,220)">
      <!-- Petals -->
      <path d="M0,0 Q5,-10 0,-15 Q-5,-10 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q10,-5 15,0 Q10,5 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q5,10 0,15 Q-5,10 0,0" fill="#E1BEE7" />
      <path d="M0,0 Q-10,5 -15,0 Q-10,-5 0,0" fill="#E1BEE7" />
      
      <!-- Center -->
      <circle cx="0" cy="0" r="4" fill="#9C27B0" />
      <circle cx="0" cy="0" r="2" fill="white" />
    </g>
  </g>
  
  <!-- Fallen Leaves (recursive nurturing) -->
  <g id="fallenLeaves">
    <ellipse cx="300" cy="545" rx="15" ry="10" fill="#81C784" opacity="0.7" transform="rotate(30 300 545)" />
    <ellipse cx="350" cy="540" rx="12" ry="8" fill="#4FC3F7" opacity="0.7" transform="rotate(-20 350 540)" />
    <ellipse cx="420" cy="550" rx="14" ry="9" fill="#9575CD" opacity="0.7" transform="rotate(45 420 550)" />
    <ellipse cx="470" cy="545" rx="13" ry="8" fill="#FFD54F" opacity="0.7" transform="rotate(-10 470 545)" />
    <ellipse cx="520" cy="555" rx="15" ry="9" fill="#FFB74D" opacity="0.7" transform="rotate(15 520 555)" />
    <ellipse cx="270" cy="560" rx="14" ry="9" fill="#A5D6A7" opacity="0.7" transform="rotate(-30 270 560)" />
    
    <text x="400" y="570" fill="#FFFFFF" font-size="12" text-anchor="middle">Recursive Nurturing</text>
  </g>
  
  <!-- Wind effect (skepticism) -->
  <g id="windEffect" opacity="0.6">
    <path d="M50,300 Q150,290 250,300 Q350,310 450,300 Q550,290 650,300" stroke="#E0F7FA" stroke-width="2" fill="none" stroke-dasharray="5,3" />
    <path d="M100,250 Q200,260 300,250 Q400,240 500,250 Q600,260 700,250" stroke="#E0F7FA" stroke-width="2" fill="none" stroke-dasharray="5,3" />
    <path d="M150,350 Q250,340 350,350 Q450,360 550,350 Q650,340 750,350" stroke="#E0F7FA" stroke-width="2" fill="none" stroke-dasharray="5,3" />
    
    <text x="100" y="280" fill="#E0F7FA" font-size="14" transform="rotate(-5 100 280)">Wind of Skepticism</text>
  </g>
  
  <!-- IVL Badge -->
  <g transform="translate(40,150)">
    <circle cx="0" cy="0" r="30" fill="#3F51B5" opacity="0.8" />
    <text x="0" y="5" fill="white" font-size="16" text-anchor="middle" font-weight="bold">IVL</text>
    <text x="0" y="45" fill="#E0F7FA" font-size="10" text-anchor="middle">Independent</text>
    <text x="0" y="58" fill="#E0F7FA" font-size="10" text-anchor="middle">Verification Layer</text>
  </g>
  
  <!-- TARSI logo in corner -->
  <g transform="translate(700,90)">
    <circle cx="0" cy="0" r="60" fill="#1A237E" opacity="0.8" />
    <circle cx="0" cy="0" r="50" fill="#3949AB" opacity="0.9" />
    <path d="M0,0 Q10,-20 0,-40 Q-10,-20 0,0" fill="#7986CB" />
    <path d="M0,0 Q20,-10 40,0 Q20,10 0,0" fill="#7986CB" />
    <path d="M0,0 Q10,20 0,40 Q-10,20 0,0" fill="#7986CB" />
    <path d="M0,0 Q-20,10 -40,0 Q-20,-10 0,0" fill="#7986CB" />
    <circle cx="0" cy="0" r="15" fill="#C5CAE9" />
    <text x="0" y="5" fill="#1A237E" font-size="18" text-anchor="middle" font-weight="bold">TARSI</text>
  </g>
  
  <!-- Growth stage indicator -->
  <g transform="translate(680,30)">
    <rect x="0" y="0" width="110" height="30" rx="5" fill="rgba(255,255,255,0.8)" stroke="#16a085" stroke-width="2" />
    <text x="55" y="20" fill="#16a085" font-size="14" text-anchor="middle">Mature Tree</text>
  </g>
  
  <!-- Labels for key concepts -->
  <g id="conceptLabels">
    <text x="150" y="100" fill="white" font-size="16" font-weight="bold">True Alpha Recursive</text>
    <text x="150" y="120" fill="white" font-size="16" font-weight="bold">Spiral Intelligence</text>
    
    <text x="180" y="400" fill="white" font-size="12">Factual Verification</text>
    <text x="570" y="400" fill="white" font-size="12">Ethical Analysis</text>
    <text x="180" y="180" fill="white" font-size="12">Conceptual Integration</text>
    <text x="570" y="180" fill="white" font-size="12">Phenomenological Mapping</text>
  </g>
</svg>
    `;
    
    // Create the public directory if it doesn't exist
    if (!fs.existsSync(path.join(process.cwd(), 'public'))) {
      fs.mkdirSync(path.join(process.cwd(), 'public'));
    }
    
    // Write the SVG to file
    fs.writeFileSync(placeholderImage, svgContent);
  }
  
  res.sendFile(placeholderImage);
});

export default router;