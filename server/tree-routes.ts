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
  <!-- Sky background -->
  <rect width="800" height="520" fill="#E0F7FA" />
  
  <!-- Ground -->
  <rect y="520" width="800" height="80" fill="#8B4513" />
  
  <!-- Roots -->
  <path d="M370,520 C350,540 320,560 300,570" stroke="#5D4037" stroke-width="3" fill="none" />
  <path d="M400,520 C420,540 450,560 470,570" stroke="#5D4037" stroke-width="3" fill="none" />
  <path d="M380,520 C380,540 390,560 400,580" stroke="#5D4037" stroke-width="3" fill="none" />
  <path d="M390,520 C390,540 370,560 350,580" stroke="#5D4037" stroke-width="3" fill="none" />
  <path d="M410,520 C410,550 400,570 380,590" stroke="#5D4037" stroke-width="3" fill="none" />
  
  <!-- Trunk -->
  <path d="M370,520 Q370,400 380,200 Q390,400 410,520" fill="#795548" />
  
  <!-- Phi symbol on trunk -->
  <circle cx="390" cy="400" r="20" fill="rgba(255,255,255,0.2)" />
  <text x="390" y="408" fill="white" font-size="24" text-anchor="middle" font-family="serif">Φ</text>
  
  <!-- Factual branch (left) -->
  <path d="M380,220 L280,150" stroke="#795548" stroke-width="8" stroke-linecap="round" />
  
  <!-- Ethical branch (right) -->
  <path d="M380,240 L480,180" stroke="#795548" stroke-width="7" stroke-linecap="round" />
  
  <!-- Conceptual branch (top) -->
  <path d="M380,200 L390,100" stroke="#795548" stroke-width="7" stroke-linecap="round" />
  
  <!-- Phenomenological branch (right middle) -->
  <path d="M380,260 L450,220" stroke="#795548" stroke-width="6" stroke-linecap="round" />
  
  <!-- Factual leaves (green) -->
  <ellipse cx="280" cy="150" rx="25" ry="40" fill="#2ecc71" transform="rotate(-45 280 150)" />
  <ellipse cx="270" cy="140" rx="20" ry="35" fill="#27ae60" transform="rotate(-35 270 140)" />
  <ellipse cx="260" cy="155" rx="22" ry="30" fill="#2ecc71" transform="rotate(-55 260 155)" />
  
  <!-- Ethical leaves (blue) -->
  <ellipse cx="480" cy="180" rx="25" ry="40" fill="#3498db" transform="rotate(20 480 180)" />
  <ellipse cx="490" cy="170" rx="20" ry="30" fill="#2980b9" transform="rotate(30 490 170)" />
  <ellipse cx="470" cy="165" rx="18" ry="28" fill="#3498db" transform="rotate(15 470 165)" />
  
  <!-- Conceptual leaves (purple) -->
  <ellipse cx="390" cy="100" rx="22" ry="35" fill="#9b59b6" transform="rotate(0 390 100)" />
  <ellipse cx="380" cy="90" rx="18" ry="30" fill="#8e44ad" transform="rotate(-10 380 90)" />
  <ellipse cx="400" cy="85" rx="20" ry="32" fill="#9b59b6" transform="rotate(10 400 85)" />
  
  <!-- Phenomenological leaves (yellow) -->
  <ellipse cx="450" cy="220" rx="20" ry="32" fill="#f1c40f" transform="rotate(60 450 220)" />
  <ellipse cx="460" cy="210" rx="15" ry="25" fill="#f39c12" transform="rotate(50 460 210)" />
  
  <!-- Meta flower (upper right) -->
  <circle cx="460" cy="150" r="15" fill="rgba(155,89,182,0.3)" />
  <circle cx="460" cy="150" r="6" fill="rgba(255,255,255,0.9)" />
  <circle cx="460" cy="150" r="4" fill="rgba(255,223,0,0.9)" />
  <ellipse cx="470" cy="140" rx="5" ry="10" fill="#9b59b6" transform="rotate(45 470 140)" />
  <ellipse cx="475" cy="155" rx="5" ry="10" fill="#9b59b6" transform="rotate(90 475 155)" />
  <ellipse cx="460" cy="165" rx="5" ry="10" fill="#9b59b6" transform="rotate(135 460 165)" />
  <ellipse cx="445" cy="155" rx="5" ry="10" fill="#9b59b6" transform="rotate(180 445 155)" />
  <ellipse cx="450" cy="140" rx="5" ry="10" fill="#9b59b6" transform="rotate(225 450 140)" />
  <ellipse cx="470" cy="160" rx="5" ry="10" fill="#9b59b6" transform="rotate(270 470 160)" />
  
  <!-- Fallen leaves -->
  <ellipse cx="320" cy="525" rx="10" ry="15" fill="rgba(46,204,113,0.5)" transform="rotate(30 320 525)" />
  <ellipse cx="450" cy="525" rx="8" ry="12" fill="rgba(52,152,219,0.5)" transform="rotate(-20 450 525)" />
  <ellipse cx="280" cy="530" rx="7" ry="11" fill="rgba(155,89,182,0.5)" transform="rotate(120 280 530)" />
  <ellipse cx="500" cy="535" rx="9" ry="14" fill="rgba(241,196,15,0.5)" transform="rotate(60 500 535)" />
  
  <!-- Wind indicator -->
  <rect x="20" y="50" width="760" height="30" rx="5" fill="rgba(255,255,255,0.7)" stroke="rgba(0,0,0,0.2)" />
  <rect x="30" y="55" width="350" height="20" rx="3" fill="rgba(135,206,235,0.5)" />
  <text x="40" y="40" fill="rgba(0,0,0,0.7)" font-size="12">Wind of Skepticism</text>
  <path d="M380,65 L400,65 L390,75 Z" fill="rgba(0,0,0,0.5)" />
  
  <!-- Growth stage indicator -->
  <rect x="670" y="20" width="110" height="25" rx="5" fill="rgba(255,255,255,0.7)" stroke="#16a085" stroke-width="2" />
  <text x="725" y="36" fill="#16a085" font-size="14" text-anchor="middle">Mature Tree</text>
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