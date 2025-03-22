import React, { useEffect, useRef } from 'react';
import { MedicalTestCase } from '../test-suite-types';

interface MetaFloorExplorerProps {
  testCase: MedicalTestCase;
}

export const MetaFloorExplorer: React.FC<MetaFloorExplorerProps> = ({ testCase }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Draw the meta floor explorer visualization
  useEffect(() => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas dimensions to match its display size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Get meta floor data
    const nodes = testCase.expectedAnalysis.cyberneticMeta.metaFloorNodes;
    const connections = testCase.expectedAnalysis.cyberneticMeta.metaFloorConnections;
    
    // Build node map for easier lookups
    const nodeMap = nodes.reduce((map, node) => {
      map[node.id] = node;
      return map;
    }, {} as Record<string, typeof nodes[0]>);
    
    // Calculate dimensions
    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;
    
    // Node positioning and rendering constants
    const nodeRadius = 20;
    const nodeTypes: Record<string, { color: string, label: string }> = {
      fact: { color: 'rgba(16, 185, 129, 0.8)', label: 'F' },      // Emerald for facts
      reference: { color: 'rgba(79, 70, 229, 0.8)', label: 'R' },  // Indigo for references
      rule: { color: 'rgba(245, 158, 11, 0.8)', label: 'RL' },     // Amber for rules
      concept: { color: 'rgba(236, 72, 153, 0.8)', label: 'C' }    // Pink for concepts
    };
    
    // Create a force-directed layout
    // This is a simplified version, a real implementation would iteratively solve the forces
    const nodePositions: Record<string, {x: number, y: number}> = {};
    
    // Initial positioning in a grid-like pattern
    const cols = Math.ceil(Math.sqrt(nodes.length));
    const rows = Math.ceil(nodes.length / cols);
    const cellWidth = (width - padding * 2) / cols;
    const cellHeight = (height - padding * 2) / rows;
    
    nodes.forEach((node, i) => {
      const row = Math.floor(i / cols);
      const col = i % cols;
      nodePositions[node.id] = {
        x: padding + col * cellWidth + cellWidth/2 + (Math.random() * 20 - 10),
        y: padding + row * cellHeight + cellHeight/2 + (Math.random() * 20 - 10)
      };
    });
    
    // Function to draw a connection between nodes
    const drawConnection = (source: string, target: string, strength: number) => {
      const sourcePos = nodePositions[source];
      const targetPos = nodePositions[target];
      
      if (!sourcePos || !targetPos) return;
      
      const gradient = ctx.createLinearGradient(
        sourcePos.x, 
        sourcePos.y, 
        targetPos.x, 
        targetPos.y
      );
      
      const sourceNode = nodeMap[source];
      const targetNode = nodeMap[target];
      const sourceType = nodeTypes[sourceNode.type];
      const targetType = nodeTypes[targetNode.type];
      
      gradient.addColorStop(0, sourceType.color);
      gradient.addColorStop(1, targetType.color);
      
      ctx.beginPath();
      ctx.moveTo(sourcePos.x, sourcePos.y);
      ctx.lineTo(targetPos.x, targetPos.y);
      ctx.strokeStyle = gradient;
      ctx.lineWidth = Math.max(1, strength * 5);
      ctx.stroke();
      
      // Draw strength label
      const midX = (sourcePos.x + targetPos.x) / 2;
      const midY = (sourcePos.y + targetPos.y) / 2;
      
      ctx.font = 'bold 10px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Add a small background to make the text more readable
      const strengthText = `${Math.round(strength * 100)}%`;
      const textWidth = ctx.measureText(strengthText).width;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.fillRect(midX - textWidth/2 - 2, midY - 7, textWidth + 4, 14);
      
      ctx.fillStyle = 'var(--foreground)';
      ctx.fillText(strengthText, midX, midY);
    };
    
    // Function to draw a node
    const drawNode = (node: typeof nodes[0]) => {
      const pos = nodePositions[node.id];
      if (!pos) return;
      
      const typeInfo = nodeTypes[node.type];
      
      // Draw node background
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, nodeRadius, 0, Math.PI * 2);
      ctx.fillStyle = typeInfo.color;
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Draw node type label
      ctx.font = 'bold 12px sans-serif';
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(typeInfo.label, pos.x, pos.y);
      
      // Draw node name
      ctx.font = '12px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Truncate long names
      let displayName = node.name;
      if (displayName.length > 15) {
        displayName = displayName.substring(0, 13) + '...';
      }
      
      ctx.fillText(displayName, pos.x, pos.y + nodeRadius + 15);
      
      // Draw confidence
      ctx.font = 'bold 10px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      
      const confidenceText = `${Math.round(node.confidence * 100)}%`;
      ctx.fillText(confidenceText, pos.x, pos.y + nodeRadius + 30);
    };
    
    // Draw connections first (so they are behind nodes)
    connections.forEach(connection => {
      drawConnection(connection.source, connection.target, connection.strength);
    });
    
    // Draw nodes on top
    nodes.forEach(node => {
      drawNode(node);
    });
    
    // Draw legend
    const legendX = width - 140;
    const legendY = 30;
    const legendSpacing = 25;
    
    // Draw legend title
    ctx.font = 'bold 14px sans-serif';
    ctx.fillStyle = 'var(--foreground)';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText('Node Types', legendX, legendY);
    
    // Draw legend items
    Object.entries(nodeTypes).forEach(([type, info], i) => {
      const y = legendY + 30 + i * legendSpacing;
      
      // Draw legend dot
      ctx.beginPath();
      ctx.arc(legendX + 10, y, 8, 0, Math.PI * 2);
      ctx.fillStyle = info.color;
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 1;
      ctx.stroke();
      
      // Draw legend text
      ctx.font = '12px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(type.charAt(0).toUpperCase() + type.slice(1), legendX + 25, y);
    });
    
    // Draw title
    ctx.font = 'bold 16px sans-serif';
    ctx.fillStyle = 'var(--foreground)';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText('MetaFloor Knowledge Map', 20, 20);
    
    // Draw stats
    ctx.font = '12px sans-serif';
    ctx.fillStyle = 'var(--muted-foreground)';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText(`Nodes: ${nodes.length} | Connections: ${connections.length}`, 20, 45);
    
  }, [testCase]);

  return (
    <div className="w-full h-full">
      <canvas
        ref={canvasRef}
        className="w-full h-full"
      />
    </div>
  );
};