import React, { useEffect, useRef } from 'react';
import { MedicalTestCase } from '../test-suite-types';

interface SelfReflexivityRadarProps {
  testCase: MedicalTestCase;
}

export const SelfReflexivityRadar: React.FC<SelfReflexivityRadarProps> = ({ testCase }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Draw the self-reflexivity radar visualization
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
    
    // Get pathway data
    const pathways = testCase.expectedAnalysis.cyberneticMeta.selfReflexivityPathways;
    
    // Calculate dimensions
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const maxRadius = Math.min(width, height) / 2 - 30;
    
    // Draw circular grid
    ctx.strokeStyle = 'rgba(161, 161, 170, 0.15)'; // Zinc-400 with low opacity
    ctx.lineWidth = 1;
    
    for (let i = 1; i <= 5; i++) {
      const radius = maxRadius * (i / 5);
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.stroke();
    }
    
    // Draw axis labels (20%, 40%, etc.)
    ctx.font = '10px sans-serif';
    ctx.fillStyle = 'var(--muted-foreground)';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    for (let i = 1; i <= 5; i++) {
      const value = (i / 5) * 100;
      const radius = maxRadius * (i / 5);
      ctx.fillText(`${value}%`, centerX, centerY - radius - 10);
    }
    
    // Calculate angles for each pathway
    const angleStep = (Math.PI * 2) / pathways.length;
    
    // Draw axis lines
    ctx.beginPath();
    pathways.forEach((_, i) => {
      const angle = i * angleStep;
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(
        centerX + Math.cos(angle) * maxRadius, 
        centerY + Math.sin(angle) * maxRadius
      );
    });
    ctx.stroke();
    
    // Draw pathway labels
    ctx.font = 'bold 12px sans-serif';
    ctx.fillStyle = 'var(--foreground)';
    
    pathways.forEach((pathway, i) => {
      const angle = i * angleStep;
      const labelRadius = maxRadius + 20;
      const x = centerX + Math.cos(angle) * labelRadius;
      const y = centerY + Math.sin(angle) * labelRadius;
      
      // Adjust text alignment based on position
      if (angle === 0) {
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
      } else if (angle === Math.PI) {
        ctx.textAlign = 'right';
        ctx.textBaseline = 'middle';
      } else if (angle < Math.PI) {
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
      } else {
        ctx.textAlign = 'right';
        ctx.textBaseline = 'top';
      }
      
      ctx.fillText(pathway.path, x, y);
    });
    
    // Draw data points and connect them
    ctx.beginPath();
    pathways.forEach((pathway, i) => {
      const angle = i * angleStep;
      const radius = maxRadius * pathway.confidence;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    
    // Close the path by connecting to the first point
    if (pathways.length > 0) {
      const firstAngle = 0;
      const firstRadius = maxRadius * pathways[0].confidence;
      const firstX = centerX + Math.cos(firstAngle) * firstRadius;
      const firstY = centerY + Math.sin(firstAngle) * firstRadius;
      ctx.lineTo(firstX, firstY);
    }
    
    // Fill the shape
    ctx.fillStyle = 'rgba(16, 185, 129, 0.1)'; // Emerald-500 with low opacity
    ctx.fill();
    
    // Draw stroke around the shape
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.8)'; // Emerald-500 with high opacity
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw data points
    pathways.forEach((pathway, i) => {
      const angle = i * angleStep;
      const radius = maxRadius * pathway.confidence;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(16, 185, 129, 0.8)'; // Emerald-500 with high opacity
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 1;
      ctx.stroke();
      
      // Draw confidence percentage
      ctx.font = 'bold 10px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${Math.round(pathway.confidence * 100)}%`, x, y);
    });
    
    // Draw title
    ctx.font = 'bold 14px sans-serif';
    ctx.fillStyle = 'var(--foreground)';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    ctx.fillText('Self-Reflexivity Pathways', centerX, 10);
    
    // Draw subtitle
    ctx.font = '12px sans-serif';
    ctx.fillStyle = 'var(--muted-foreground)';
    ctx.fillText('Confidence Levels', centerX, 30);
    
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