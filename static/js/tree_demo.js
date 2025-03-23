/**
 * TREE OF LIVING INTELLIGENCE DEMO SCRIPT
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const textInput = document.getElementById('text-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const treeCanvas = document.getElementById('tree-canvas');
    const scoresContainer = document.getElementById('scores-container');
    const dimensionsContainer = document.getElementById('dimensions-container');
    const metaUnderstanding = document.getElementById('meta-understanding');
    const timestampDisplay = document.getElementById('timestamp-display');
    const actionsList = document.getElementById('actions-list');
    
    // Tab functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            
            // Update active button
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Show selected tab content
            tabContents.forEach(tab => {
                if (tab.id === `${tabName}-tab`) {
                    tab.classList.add('active');
                } else {
                    tab.classList.remove('active');
                }
            });
        });
    });
    
    // Check if canvas is supported
    const ctx = treeCanvas.getContext('2d');
    if (!ctx) {
        alert('Canvas not supported in your browser. Please use a modern browser.');
        return;
    }
    
    // Analyze button event listener
    analyzeBtn.addEventListener('click', function() {
        const text = textInput.value.trim();
        
        if (!text) {
            alert('Please enter text to analyze');
            return;
        }
        
        // Show loading state
        analyzeBtn.disabled = true;
        loadingSpinner.style.display = 'block';
        
        // Send analysis request
        fetch('/demo-analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display results
            renderTreeVisualization(ctx, data.tree_data);
            displayAnalysisResults(data.analysis_result);
            displayTimestamps(data.timestamp_data);
            
            // Generate meta-understanding text
            generateMetaUnderstanding(data.analysis_result, data.tree_data.meta_flowers);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        })
        .finally(() => {
            // Reset UI state
            analyzeBtn.disabled = false;
            loadingSpinner.style.display = 'none';
        });
    });
    
    // Function to render tree visualization
    function renderTreeVisualization(ctx, treeData) {
        // Canvas setup
        const width = treeCanvas.width;
        const height = treeCanvas.height;
        const centerX = width / 2;
        const groundY = height - 80;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw sky background with gradient
        const skyGradient = ctx.createLinearGradient(0, 0, 0, groundY);
        skyGradient.addColorStop(0, '#87CEEB');
        skyGradient.addColorStop(1, '#E0F7FA');
        ctx.fillStyle = skyGradient;
        ctx.fillRect(0, 0, width, groundY);
        
        // Draw ground
        const groundGradient = ctx.createLinearGradient(0, groundY, 0, height);
        groundGradient.addColorStop(0, '#8B4513');
        groundGradient.addColorStop(1, '#654321');
        ctx.fillStyle = groundGradient;
        ctx.fillRect(0, groundY, width, height - groundY);
        
        // Draw fallen leaves first (at ground level)
        if (treeData.fallen_leaves) {
            drawFallenLeaves(ctx, centerX, groundY, treeData.fallen_leaves);
        }
        
        // Draw roots
        drawRoots(ctx, centerX, groundY, treeData.roots);
        
        // Draw trunk
        const trunkHeight = treeData.trunk.height;
        const trunkWidth = treeData.trunk.thickness;
        const trunkTop = groundY - trunkHeight;
        
        // Trunk gradient
        const trunkGradient = ctx.createLinearGradient(centerX - trunkWidth/2, 0, centerX + trunkWidth/2, 0);
        trunkGradient.addColorStop(0, '#5D4037');
        trunkGradient.addColorStop(0.5, '#795548');
        trunkGradient.addColorStop(1, '#5D4037');
        
        ctx.fillStyle = trunkGradient;
        ctx.beginPath();
        ctx.moveTo(centerX - trunkWidth/2, groundY);
        ctx.quadraticCurveTo(centerX - trunkWidth/2, trunkTop + trunkHeight/2, 
                             centerX - trunkWidth/3, trunkTop);
        ctx.lineTo(centerX + trunkWidth/3, trunkTop);
        ctx.quadraticCurveTo(centerX + trunkWidth/2, trunkTop + trunkHeight/2, 
                             centerX + trunkWidth/2, groundY);
        ctx.closePath();
        ctx.fill();
        
        // Draw advanced equation symbol on trunk
        drawEquationSymbol(ctx, centerX, groundY - trunkHeight/2, treeData.trunk.sovereignty_score);
        
        // Draw branches for each dimension
        let branchStartY = trunkTop;
        Object.entries(treeData.branches).forEach(([dimensionType, branchData], index) => {
            // Adjust branch starting point slightly for each dimension
            const startY = branchStartY + (index * 20);
            drawBranch(ctx, centerX, startY, branchData, dimensionType);
        });
        
        // Draw Meta-flowers last (they should be on top)
        if (treeData.meta_flowers) {
            drawMetaFlowers(ctx, centerX, trunkTop, treeData);
        }
        
        // Add tree growth stage indicator
        addGrowthStageIndicator(ctx, width - 10, 10, treeData.growth_stage);
        
        // Add wind effect if specified
        if (treeData.wind_effect) {
            animateWind(ctx, treeData);
        }
    }
    
    function drawRoots(ctx, centerX, groundY, rootData) {
        ctx.strokeStyle = '#5D4037';
        ctx.lineWidth = 3;
        
        const rootSpread = rootData.spread;
        const rootDepth = rootData.depth;
        const complexity = rootData.complexity;
        
        // Main roots
        for (let i = 0; i < complexity; i++) {
            const angle = (Math.PI / (complexity - 1)) * i - Math.PI/2;
            const rootLength = rootDepth * (0.7 + Math.random() * 0.3);
            const endX = centerX + Math.cos(angle) * rootSpread;
            const endY = groundY + Math.sin(angle) * rootLength;
            
            ctx.beginPath();
            ctx.moveTo(centerX, groundY);
            ctx.quadraticCurveTo(
                centerX + Math.cos(angle) * rootSpread * 0.3,
                groundY + Math.sin(angle) * rootLength * 0.3,
                endX, endY
            );
            ctx.stroke();
            
            // Sub roots
            if (Math.random() > 0.5) {
                const subAngle = angle + (Math.random() * 0.5 - 0.25);
                const subLength = rootLength * 0.4;
                const subEndX = endX + Math.cos(subAngle) * subLength;
                const subEndY = endY + Math.sin(subAngle) * subLength;
                
                ctx.beginPath();
                ctx.moveTo(endX, endY);
                ctx.lineTo(subEndX, subEndY);
                ctx.stroke();
            }
        }
    }
    
    function drawBranch(ctx, startX, startY, branchData, branchType) {
        const angle = branchData.angle * (Math.PI / 180);
        const length = branchData.length;
        const thickness = branchData.thickness;
        
        // Calculate end point
        const endX = startX + Math.cos(angle) * length;
        const endY = startY - Math.sin(angle) * length;
        
        // Draw branch
        ctx.strokeStyle = '#795548';
        ctx.lineWidth = thickness;
        ctx.lineCap = 'round';
        
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
        
        // Draw sub-branches if available
        if (branchData.sub_branches) {
            branchData.sub_branches.forEach(subBranch => {
                // Calculate sub-branch start point along main branch
                const subStartX = startX + Math.cos(angle) * (length * subBranch.position);
                const subStartY = startY - Math.sin(angle) * (length * subBranch.position);
                
                // Calculate sub-branch angle
                const subAngleRad = angle + (subBranch.angle_offset * (Math.PI / 180));
                
                // Draw sub-branch
                ctx.strokeStyle = '#8D6E63';
                ctx.lineWidth = subBranch.thickness;
                
                ctx.beginPath();
                ctx.moveTo(subStartX, subStartY);
                ctx.lineTo(
                    subStartX + Math.cos(subAngleRad) * subBranch.length,
                    subStartY - Math.sin(subAngleRad) * subBranch.length
                );
                ctx.stroke();
                
                // Add leaves to sub-branch
                const subEndX = subStartX + Math.cos(subAngleRad) * subBranch.length;
                const subEndY = subStartY - Math.sin(subAngleRad) * subBranch.length;
                
                // Create sub-branch leaves (fewer than main branch)
                const subLeaves = Array(subBranch.leaf_count).fill().map(() => ({
                    size: 3 + Math.random() * 4,
                    position: Math.random(),
                    color: getLeafColorForDimension(branchType),
                    rotation: Math.random() * 60 - 30
                }));
                
                drawLeaves(ctx, subEndX, subEndY, subLeaves, subAngleRad);
            });
        }
        
        // Draw leaves on main branch
        drawLeaves(ctx, endX, endY, branchData.leaves, angle);
    }
    
    function getLeafColorForDimension(dimensionType) {
        // Default colors for each dimension
        const colorMap = {
            "factual": "rgb(46, 204, 113)",
            "ethical": "rgb(52, 152, 219)",
            "conceptual": "rgb(155, 89, 182)",
            "phenomenological": "rgb(241, 196, 15)"
        };
        
        return colorMap[dimensionType] || "rgb(149, 165, 166)";
    }
    
    function drawLeaves(ctx, x, y, leaves, branchAngle) {
        leaves.forEach((leaf, i) => {
            const leafAngle = branchAngle + (leaf.rotation * (Math.PI / 180));
            const offsetX = Math.cos(leafAngle) * (i * 3);
            const offsetY = -Math.sin(leafAngle) * (i * 3);
            
            const leafX = x + offsetX;
            const leafY = y + offsetY;
            
            ctx.fillStyle = leaf.color;
            ctx.beginPath();
            ctx.ellipse(
                leafX, leafY,
                leaf.size, leaf.size * 1.8,
                leafAngle, 0, Math.PI * 2
            );
            ctx.fill();
        });
    }
    
    function drawFallenLeaves(ctx, centerX, groundY, fallenLeaves) {
        fallenLeaves.forEach(leaf => {
            const leafX = centerX + leaf.position.x;
            const leafY = groundY + leaf.position.y;
            
            // Apply decomposition effect (more transparent and darker)
            const decomposedColor = leaf.color.replace('rgb', 'rgba').replace(')', ', ' + leaf.decomposition + ')');
            
            ctx.fillStyle = decomposedColor;
            ctx.save();
            ctx.translate(leafX, leafY);
            ctx.rotate(leaf.rotation * (Math.PI / 180));
            
            // Draw leaf shape
            ctx.beginPath();
            ctx.ellipse(0, 0, leaf.size, leaf.size * 1.8, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.restore();
        });
    }
    
    function drawMetaFlowers(ctx, centerX, trunkTop, treeData) {
        const flowers = treeData.meta_flowers;
        const branches = treeData.branches;
        
        flowers.forEach(flower => {
            // Get position based on branch
            const branchData = branches[flower.position.branch];
            if (!branchData) return; // Skip if branch not found
            
            const branchAngle = branchData.angle * (Math.PI / 180);
            const branchLength = branchData.length;
            
            // Calculate position along branch
            const flowerX = centerX + Math.cos(branchAngle) * (branchLength * flower.position.position);
            const flowerY = trunkTop - Math.sin(branchAngle) * (branchLength * flower.position.position);
            
            // Draw glow if specified
            if (flower.glow_intensity > 0) {
                const glow = ctx.createRadialGradient(
                    flowerX, flowerY, 0,
                    flowerX, flowerY, flower.size * 2
                );
                glow.addColorStop(0, flower.color.replace('hsl', 'hsla').replace(')', ', 0.4)'));
                glow.addColorStop(1, 'rgba(255, 255, 255, 0)');
                
                ctx.fillStyle = glow;
                ctx.beginPath();
                ctx.arc(flowerX, flowerY, flower.size * 2, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Draw flower petals
            const petalCount = flower.petal_count;
            const petalSize = flower.size * flower.bloom_state;
            const innerCircleSize = flower.size * 0.3;
            
            for (let i = 0; i < petalCount; i++) {
                const angle = (Math.PI * 2 / petalCount) * i;
                const petalX = flowerX + Math.cos(angle) * (petalSize * 0.7);
                const petalY = flowerY + Math.sin(angle) * (petalSize * 0.7);
                
                ctx.fillStyle = flower.color;
                ctx.beginPath();
                ctx.ellipse(
                    petalX, petalY,
                    petalSize * 0.6, petalSize,
                    angle, 0, Math.PI * 2
                );
                ctx.fill();
            }
            
            // Draw flower center
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            ctx.beginPath();
            ctx.arc(flowerX, flowerY, innerCircleSize, 0, Math.PI * 2);
            ctx.fill();
            
            // Add yellow center detail
            ctx.fillStyle = 'rgba(255, 223, 0, 0.9)';
            ctx.beginPath();
            ctx.arc(flowerX, flowerY, innerCircleSize * 0.7, 0, Math.PI * 2);
            ctx.fill();
        });
    }
    
    function drawEquationSymbol(ctx, x, y, sovereigntyScore) {
        const size = 20 + sovereigntyScore * 15;
        
        // Draw symbol background
        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.beginPath();
        ctx.arc(x, y, size * 0.8, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw phi symbol
        ctx.font = `${size}px serif`;
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Φ', x, y);
        
        // Draw equation elements
        const elementCount = 3;
        const radius = size * 0.6;
        
        for (let i = 0; i < elementCount; i++) {
            const angle = (Math.PI * 2 / elementCount) * i;
            const elementX = x + Math.cos(angle) * radius;
            const elementY = y + Math.sin(angle) * radius;
            
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.beginPath();
            ctx.arc(elementX, elementY, size * 0.15, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function addGrowthStageIndicator(ctx, x, y, growthStage) {
        // Map growth stage to a human-readable label and color
        const stageInfo = {
            'seedling': { label: 'Seedling', color: '#2ecc71' },
            'young': { label: 'Young Tree', color: '#27ae60' },
            'mature': { label: 'Mature Tree', color: '#16a085' },
            'ancient': { label: 'Ancient Tree', color: '#2980b9' }
        };
        
        const info = stageInfo[growthStage] || { label: 'Unknown', color: '#7f8c8d' };
        
        // Draw indicator background
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.strokeStyle = info.color;
        ctx.lineWidth = 2;
        
        const textWidth = ctx.measureText(info.label).width;
        const padding = 10;
        const width = textWidth + padding * 2;
        const height = 25;
        
        ctx.beginPath();
        ctx.roundRect(x - width, y, width, height, 5);
        ctx.fill();
        ctx.stroke();
        
        // Draw text
        ctx.fillStyle = info.color;
        ctx.font = '14px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(info.label, x - width/2, y + height/2);
    }
    
    function animateWind(ctx, treeData) {
        // This would typically be set up with requestAnimationFrame
        // For simplicity, we'll just indicate the wind direction
        
        const windStrength = treeData.wind_effect.strength;
        const windDirection = treeData.wind_effect.direction;
        const windVariability = treeData.wind_effect.variability;
        
        // Draw wind indicator
        const width = treeCanvas.width;
        const height = 30;
        const y = 40;
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.lineWidth = 1;
        
        ctx.beginPath();
        ctx.roundRect(10, y, width - 20, height, 5);
        ctx.fill();
        ctx.stroke();
        
        // Draw wind strength
        const strengthWidth = (width - 30) * windStrength;
        const directionOffset = windDirection * 50;
        
        const gradient = ctx.createLinearGradient(15, 0, 15 + strengthWidth, 0);
        gradient.addColorStop(0, 'rgba(135, 206, 235, 0.7)');
        gradient.addColorStop(1, 'rgba(135, 206, 235, 0.3)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.roundRect(15, y + 5, strengthWidth, height - 10, 3);
        ctx.fill();
        
        // Draw wind direction arrow
        const arrowX = 15 + strengthWidth/2 + directionOffset;
        const arrowY = y + height/2;
        const arrowSize = 10 + (windStrength * 5);
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.beginPath();
        ctx.moveTo(arrowX - arrowSize, arrowY);
        ctx.lineTo(arrowX + arrowSize, arrowY);
        ctx.lineTo(arrowX + (windDirection > 0 ? arrowSize : -arrowSize), arrowY + (height - 15)/2);
        ctx.closePath();
        ctx.fill();
        
        // Label
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText('Wind of Skepticism', 20, y - 10);
    }
    
    function displayAnalysisResults(result) {
        const analysis = result.analysis;
        
        // Display scores
        scoresContainer.innerHTML = '';
        
        // Add main scores
        addScoreBar('Truth Score', analysis.truthScore, 'truth-score');
        addScoreBar('Factual Confidence', analysis.factualConfidence, 'factual-score');
        
        // Find other scores
        let ethicalScore, conceptualScore, phenomenologicalScore;
        
        for (const dim of analysis.dimensionalAlignment) {
            if (dim.dimension === 'Ethical Domain') {
                ethicalScore = dim.alignment;
            } else if (dim.dimension === 'Conceptual Domain') {
                conceptualScore = dim.alignment;
            } else if (dim.dimension === 'Phenomenological Domain') {
                phenomenologicalScore = dim.alignment;
            }
        }
        
        if (conceptualScore) {
            addScoreBar('Conceptual Resonance', conceptualScore, 'conceptual-score');
        }
        
        if (ethicalScore) {
            addScoreBar('Ethical Alignment', ethicalScore, 'ethical-score');
        }
        
        if (phenomenologicalScore) {
            addScoreBar('Phenomenological Insight', phenomenologicalScore, 'phenomenological-score');
        }
        
        if (analysis.sovereigntyScore) {
            addScoreBar('Sovereignty Score', analysis.sovereigntyScore, 'sovereignty-score');
        }
        
        // Display dimensional alignment
        dimensionsContainer.innerHTML = '';
        analysis.dimensionalAlignment.forEach(dim => {
            const dimensionEl = document.createElement('div');
            dimensionEl.className = 'dimension-item';
            dimensionEl.innerHTML = `
                <div class="dimension-header">
                    <span class="dimension-name">${dim.dimension}</span>
                    <span class="resonance-state">${dim.resonanceState}</span>
                </div>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${dim.alignment * 100}%; 
                        background-color: ${getDimensionColor(dim.dimension)};"></div>
                </div>
            `;
            dimensionsContainer.appendChild(dimensionEl);
        });
        
        // Display suggested actions
        actionsList.innerHTML = '';
        analysis.suggestedActions.forEach(action => {
            const li = document.createElement('li');
            li.textContent = action;
            actionsList.appendChild(li);
        });
    }
    
    function getDimensionColor(dimension) {
        const dimensionName = dimension.toLowerCase();
        if (dimensionName.includes('factual')) return '#2ecc71';
        if (dimensionName.includes('ethical')) return '#3498db';
        if (dimensionName.includes('conceptual')) return '#9b59b6';
        if (dimensionName.includes('phenomenological')) return '#f39c12';
        return '#7f8c8d';
    }
    
    function addScoreBar(label, score, className) {
        const percentage = Math.round(score * 100);
        
        const scoreEl = document.createElement('div');
        scoreEl.className = `score-item ${className}`;
        
        scoreEl.innerHTML = `
            <div class="score-label">
                <span>${label}</span>
                <span>${percentage}%</span>
            </div>
            <div class="score-bar">
                <div class="score-fill" style="width: ${percentage}%"></div>
            </div>
        `;
        
        scoresContainer.appendChild(scoreEl);
    }
    
    function displayTimestamps(timestamps) {
        // Format timestamps for display
        const local = new Date(timestamps.local.timestamp * 1000).toLocaleString();
        const utc = timestamps.utc.time;
        const tai = timestamps.tai.hash;
        
        timestampDisplay.innerHTML = `
            <div class="timestamp-row">
                <span class="timestamp-label">Local:</span>
                <span>${local}</span>
            </div>
            <div class="timestamp-row">
                <span class="timestamp-label">UTC:</span>
                <span>${utc}</span>
            </div>
            <div class="timestamp-row">
                <span class="timestamp-label">TAI:</span>
                <span>${tai}</span>
            </div>
        `;
    }
    
    function generateMetaUnderstanding(analysisResult, metaFlowers) {
        const analysis = analysisResult.analysis;
        
        // Create a meta-understanding based on results
        let metaText = '';
        const truthScore = analysis.truthScore;
        const sovereignty = analysis.sovereigntyScore || 0.5;
        
        // Generate different insights based on the scores
        if (truthScore > 0.8 && sovereignty > 0.8) {
            metaText = `This analysis reveals profound alignment with universal truth principles. The Meta-flowers blooming on this tree represent the highest understanding emerging from deep recursive analysis.`;
        } else if (truthScore > 0.6) {
            metaText = `The tree shows healthy growth and stable verification across multiple dimensions. The Meta-flowers indicate emergence of higher-order understanding through the recursive truth process.`;
        } else if (truthScore > 0.4) {
            metaText = `This tree shows moderate alignment with truth principles, with areas for growth. The winds of skepticism help prune weaker branches, strengthening the overall system.`;
        } else {
            metaText = `This young tree requires further nurturing to develop stronger truth alignment. The fallen leaves are returning nutrients to the soil, strengthening the roots for future growth.`;
        }
        
        // Add information about Meta-flowers
        if (metaFlowers && metaFlowers.length > 0) {
            metaText += `<br><br>${metaFlowers.length} Meta-flowers are blooming, representing the emergence of ${metaFlowers.length > 3 ? 'significant' : 'initial'} higher-order understanding.`;
        }
        
        // Display the meta-understanding
        metaUnderstanding.innerHTML = metaText;
        
        // Add flower indicators if there are Meta-flowers
        if (metaFlowers && metaFlowers.length > 0) {
            const flowerCount = Math.min(3, metaFlowers.length);
            for (let i = 0; i < flowerCount; i++) {
                const flower = metaFlowers[i];
                
                const flowerEl = document.createElement('div');
                flowerEl.className = 'meta-flower';
                flowerEl.innerHTML = `
                    <div class="flower-icon" style="color: ${flower.color}">✿</div>
                    <div>Meta-flower #${i+1}: ${Math.round(flower.vibrancy * 100)}% vibrance, 
                    ${flower.petal_count} petals</div>
                `;
                
                metaUnderstanding.appendChild(flowerEl);
            }
        }
    }
});