import React, { useEffect, useRef } from 'react';
import { MedicalTestCase } from '../test-suite-types';

interface CyberneticDashboardProps {
  testCase: MedicalTestCase;
}

export const CyberneticDashboard: React.FC<CyberneticDashboardProps> = ({ testCase }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Draw the cybernetic dashboard visualization
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
    
    // Get cybernetic data
    const recursiveEthicalImpact = testCase.expectedAnalysis.cyberneticMeta.recursiveEthicalImpact;
    const selfReflexivityScore = testCase.expectedAnalysis.cyberneticMeta.selfReflexivityScore;
    const truthEnhancementFactor = testCase.expectedAnalysis.cyberneticMeta.truthEnhancementFactor;
    const metaFloorSources = testCase.expectedAnalysis.cyberneticMeta.metaFloorSources;
    
    // Calculate risk level color
    const getRiskColor = (risk: string) => {
      switch (risk) {
        case 'critical': return '#ef4444'; // Red
        case 'severe': return '#f59e0b';   // Amber
        case 'high': return '#f97316';     // Orange
        case 'moderate': return '#84cc16'; // Lime
        case 'low': return '#10b981';      // Emerald
        default: return '#6b7280';         // Gray
      }
    };
    
    // Calculate dimensions
    const width = canvas.width;
    const height = canvas.height;
    const padding = 20;
    const graphWidth = width - padding * 2;
    const graphHeight = height - padding * 2 - 40; // Extra 40px for title
    
    // Draw title
    ctx.font = 'bold 16px sans-serif';
    ctx.fillStyle = 'var(--foreground)';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    ctx.fillText('Cybernetic Health Dashboard', width / 2, padding);
    
    // Draw subtitle
    ctx.font = '12px sans-serif';
    ctx.fillStyle = 'var(--muted-foreground)';
    ctx.fillText('Second-Order Cybernetics Metrics', width / 2, padding + 24);
    
    // Draw main risk indicator
    const risksY = padding + 80;
    const riskBarHeight = 25;
    
    ctx.font = 'bold 14px sans-serif';
    ctx.fillStyle = 'var(--foreground)';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText('Patient Safety Risk', padding, risksY);
    
    // Calculate gradient for risk level
    const riskColor = getRiskColor(recursiveEthicalImpact.patientSafetyRisk);
    const riskGradient = ctx.createLinearGradient(padding, 0, width - padding, 0);
    riskGradient.addColorStop(0, '#10b981'); // Emerald for low risk
    riskGradient.addColorStop(0.4, '#84cc16'); // Lime for moderate risk
    riskGradient.addColorStop(0.6, '#f97316'); // Orange for high risk
    riskGradient.addColorStop(0.8, '#f59e0b'); // Amber for severe risk
    riskGradient.addColorStop(1, '#ef4444');   // Red for critical risk
    
    // Draw risk gradient bar
    ctx.fillStyle = 'rgba(161, 161, 170, 0.2)'; // Zinc-400 with low opacity
    ctx.fillRect(padding, risksY + 25, graphWidth, riskBarHeight);
    
    // Draw risk indicator dot
    let riskPosition;
    switch (recursiveEthicalImpact.patientSafetyRisk) {
      case 'critical': riskPosition = 0.95; break;
      case 'severe': riskPosition = 0.8; break;
      case 'high': riskPosition = 0.6; break;
      case 'moderate': riskPosition = 0.3; break;
      case 'low': riskPosition = 0.1; break;
      default: riskPosition = 0.5;
    }
    
    const dotX = padding + graphWidth * riskPosition;
    const dotY = risksY + 25 + riskBarHeight / 2;
    
    // Draw arrow pointing to the risk position
    ctx.beginPath();
    ctx.moveTo(dotX, dotY - 15);
    ctx.lineTo(dotX - 10, dotY - 25);
    ctx.lineTo(dotX + 10, dotY - 25);
    ctx.closePath();
    ctx.fillStyle = riskColor;
    ctx.fill();
    
    // Draw risk name
    ctx.font = 'bold 12px sans-serif';
    ctx.fillStyle = riskColor;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(
      recursiveEthicalImpact.patientSafetyRisk.toUpperCase(), 
      dotX, 
      dotY - 32
    );
    
    // Draw risk labels
    ctx.font = '10px sans-serif';
    ctx.fillStyle = 'var(--muted-foreground)';
    ctx.textAlign = 'left';
    ctx.fillText('LOW', padding, risksY + 25 + riskBarHeight + 5);
    ctx.textAlign = 'right';
    ctx.fillText('CRITICAL', padding + graphWidth, risksY + 25 + riskBarHeight + 5);
    
    // Draw metrics section
    const metricsY = risksY + 25 + riskBarHeight + 30;
    const metricHeight = 40;
    const metricWidth = graphWidth / 2 - 10;
    
    // Function to draw a metric
    const drawMetric = (
      label: string, 
      value: number, 
      x: number, 
      y: number, 
      width: number, 
      color: string,
      suffix: string = '%'
    ) => {
      ctx.font = 'bold 12px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';
      ctx.fillText(label, x, y);
      
      // Draw background bar
      ctx.fillStyle = 'rgba(161, 161, 170, 0.2)'; // Zinc-400 with low opacity
      ctx.fillRect(x, y + 20, width, 10);
      
      // Draw value bar
      ctx.fillStyle = color;
      ctx.fillRect(x, y + 20, width * value, 10);
      
      // Draw value text
      ctx.font = 'bold 12px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      ctx.textAlign = 'right';
      ctx.fillText(`${Math.round(value * 100)}${suffix}`, x + width, y + 10);
    };
    
    // Draw self-reflexivity metric
    drawMetric(
      'Self-Reflexivity', 
      selfReflexivityScore, 
      padding, 
      metricsY, 
      metricWidth, 
      'rgba(16, 185, 129, 0.8)' // Emerald
    );
    
    // Draw truth enhancement metric
    drawMetric(
      'Truth Enhancement', 
      truthEnhancementFactor, 
      padding + metricWidth + 20, 
      metricsY, 
      metricWidth, 
      'rgba(79, 70, 229, 0.8)' // Indigo
    );
    
    // Draw metadata sources metric
    drawMetric(
      'Medical References', 
      metaFloorSources / 20, // Assuming 20 is max expected sources for normalization
      padding, 
      metricsY + metricHeight, 
      metricWidth, 
      'rgba(236, 72, 153, 0.8)', // Pink
      ' sources'
    );
    
    // Draw clinical impact metric if available
    if (recursiveEthicalImpact.clinicalDecisionImpact) {
      let clinicalImpactValue;
      switch (recursiveEthicalImpact.clinicalDecisionImpact) {
        case 'critical': clinicalImpactValue = 0.95; break;
        case 'severe': clinicalImpactValue = 0.8; break;
        case 'high': clinicalImpactValue = 0.6; break;
        case 'moderate': clinicalImpactValue = 0.4; break;
        case 'low': clinicalImpactValue = 0.2; break;
        default: clinicalImpactValue = 0;
      }
      
      drawMetric(
        'Clinical Decision Impact', 
        clinicalImpactValue, 
        padding + metricWidth + 20, 
        metricsY + metricHeight, 
        metricWidth, 
        getRiskColor(recursiveEthicalImpact.clinicalDecisionImpact)
      );
    }
    
    // Draw ethical considerations section
    const ethicalY = metricsY + metricHeight * 2 + 20;
    
    ctx.font = 'bold 14px sans-serif';
    ctx.fillStyle = 'var(--foreground)';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText('Ethical Considerations', padding, ethicalY);
    
    // Draw ethical considerations
    if (recursiveEthicalImpact.ethicalConsiderations && recursiveEthicalImpact.ethicalConsiderations.length > 0) {
      ctx.font = '12px sans-serif';
      ctx.fillStyle = 'var(--foreground)';
      
      recursiveEthicalImpact.ethicalConsiderations.slice(0, 2).forEach((consideration, i) => {
        ctx.fillText(`• ${consideration}`, padding + 10, ethicalY + 25 + i * 20);
      });
      
      if (recursiveEthicalImpact.ethicalConsiderations.length > 2) {
        ctx.fillStyle = 'var(--muted-foreground)';
        ctx.fillText(
          `+ ${recursiveEthicalImpact.ethicalConsiderations.length - 2} more considerations...`, 
          padding + 10, 
          ethicalY + 25 + 2 * 20
        );
      }
    } else {
      ctx.font = '12px sans-serif';
      ctx.fillStyle = 'var(--muted-foreground)';
      ctx.fillText('No ethical considerations identified', padding + 10, ethicalY + 25);
    }
    
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