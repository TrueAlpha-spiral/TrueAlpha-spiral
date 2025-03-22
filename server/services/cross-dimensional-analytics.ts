/**
 * Cross-Dimensional Analytics Service
 * 
 * This service provides analytical functions for the dimensional boundary simulation,
 * including concept drift analysis, integrity reporting, and entity metrics.
 */

import { storage } from '../storage';
import { v4 as uuidv4 } from 'uuid';

/**
 * Analyzes concept drift between dimensions
 * @param conceptId The concept identifier
 * @param sourceDimension The source dimension
 * @param targetDimension The target dimension 
 * @returns Analysis results
 */
export function analyzeConceptDrift(
  conceptId: string, 
  sourceDimension: string, 
  targetDimension: string
) {
  // Get the simulation state
  const simulation = storage.getDimensionalBoundarySimulation();
  
  if (!simulation) {
    return {
      status: 'error',
      message: 'No simulation running',
      timestamp: new Date().toISOString()
    };
  }
  
  // Find the dimensions
  const dimensions = simulation.dimensions || [];
  const sourceDim = dimensions.find(d => d.id === sourceDimension);
  const targetDim = dimensions.find(d => d.id === targetDimension);
  
  if (!sourceDim || !targetDim) {
    return {
      status: 'error',
      message: 'Source or target dimension not found',
      timestamp: new Date().toISOString()
    };
  }
  
  // Get all entities that crossed boundaries
  const entities = simulation.entities || [];
  const crossingEvents = simulation.crossingEvents || [];
  
  // Filter relevant events
  const relevantEvents = crossingEvents.filter(e => 
    e.fromDimension === sourceDimension && 
    e.toDimension === targetDimension
  );
  
  // Calculate concept drift metrics
  const driftIntensity = calculateDriftIntensity(sourceDim, targetDim);
  const semanticShift = calculateSemanticShift(relevantEvents);
  const truthPreservation = calculateTruthPreservation(
    sourceDim.integrity, 
    targetDim.integrity
  );
  
  // Generate analysis report
  return {
    status: 'success',
    analysisId: uuidv4(),
    conceptId,
    sourceDimension: {
      id: sourceDim.id,
      name: sourceDim.name,
      integrity: sourceDim.integrity
    },
    targetDimension: {
      id: targetDim.id,
      name: targetDim.name,
      integrity: targetDim.integrity
    },
    metrics: {
      driftIntensity,
      semanticShift,
      truthPreservation,
      crossingEventCount: relevantEvents.length,
      boundaryStrength: simulation.config?.boundaryStrength || 0.5,
      integrityDelta: targetDim.integrity - sourceDim.integrity
    },
    recommendations: generateRecommendations(
      driftIntensity, 
      semanticShift, 
      truthPreservation
    ),
    timestamp: new Date().toISOString()
  };
}

/**
 * Generates an integrity report for the current simulation
 * @returns Integrity report
 */
export function generateIntegrityReport() {
  const simulation = storage.getDimensionalBoundarySimulation();
  
  if (!simulation) {
    return {
      status: 'error',
      message: 'No simulation running',
      timestamp: new Date().toISOString()
    };
  }
  
  const dimensions = simulation.dimensions || [];
  const entities = simulation.entities || [];
  const crossingEvents = simulation.crossingEvents || [];
  
  // Calculate dimension integrity metrics
  const dimensionMetrics = dimensions.map(dim => ({
    id: dim.id,
    name: dim.name,
    currentIntegrity: dim.integrity,
    ruleCount: dim.rules?.length || 0,
    integrityTrend: calculateIntegrityTrend(dim.id, crossingEvents)
  }));
  
  // Calculate overall system integrity
  const systemIntegrity = calculateSystemIntegrity(dimensions);
  
  // Find dimension with lowest integrity
  const lowestIntegrityDimension = [...dimensions]
    .sort((a, b) => a.integrity - b.integrity)[0];
  
  // Calculate boundary strengths between dimensions
  const boundaryStrengths = calculateBoundaryStrengths(dimensions, crossingEvents);
  
  // Generate integrity report
  return {
    status: 'success',
    reportId: uuidv4(),
    systemIntegrity,
    dimensionCount: dimensions.length,
    entityCount: entities.length,
    crossingEventCount: crossingEvents.length,
    criticalDimension: lowestIntegrityDimension ? {
      id: lowestIntegrityDimension.id,
      name: lowestIntegrityDimension.name,
      integrity: lowestIntegrityDimension.integrity
    } : null,
    dimensionMetrics,
    boundaryStrengths,
    recommendations: generateIntegrityRecommendations(
      systemIntegrity,
      dimensionMetrics,
      boundaryStrengths
    ),
    timestamp: new Date().toISOString()
  };
}

/**
 * Provides metrics for entities in the simulation
 * @returns Entity metrics
 */
export function getEntityMetrics() {
  const simulation = storage.getDimensionalBoundarySimulation();
  
  if (!simulation) {
    return {
      status: 'error',
      message: 'No simulation running',
      timestamp: new Date().toISOString()
    };
  }
  
  const entities = simulation.entities || [];
  const crossingEvents = simulation.crossingEvents || [];
  
  // Calculate metrics for each entity
  const entityMetrics = entities.map(entity => {
    const entityEvents = crossingEvents.filter(e => e.entityId === entity.id);
    const successfulCrossings = entityEvents.filter(e => e.success).length;
    const failedCrossings = entityEvents.filter(e => !e.success).length;
    
    const integrityImpact = entityEvents.reduce((sum, e) => 
      sum + (e.integrityImpact || 0), 0);
    
    const currentDimension = entity.currentPosition?.dimension;
    
    return {
      id: entity.id,
      name: entity.name,
      status: entity.status,
      currentDimension,
      crossingAttempts: entityEvents.length,
      successfulCrossings,
      failedCrossings,
      successRate: entityEvents.length > 0 
        ? successfulCrossings / entityEvents.length 
        : 0,
      integrityImpact,
      anomalyCount: entityEvents.reduce((sum, e) => 
        sum + (e.anomalies?.length || 0), 0)
    };
  });
  
  // Calculate overall entity performance metrics
  const totalCrossings = crossingEvents.length;
  const successfulCrossings = crossingEvents.filter(e => e.success).length;
  const overallSuccessRate = totalCrossings > 0 
    ? successfulCrossings / totalCrossings 
    : 0;
  
  // Identify most successful and least successful entities
  const sortedBySuccess = [...entityMetrics]
    .sort((a, b) => b.successRate - a.successRate);
  
  const mostSuccessful = sortedBySuccess[0];
  const leastSuccessful = sortedBySuccess[sortedBySuccess.length - 1];
  
  return {
    status: 'success',
    metricsId: uuidv4(),
    entityCount: entities.length,
    totalCrossings,
    successfulCrossings,
    overallSuccessRate,
    mostSuccessful: mostSuccessful ? {
      id: mostSuccessful.id,
      name: mostSuccessful.name,
      successRate: mostSuccessful.successRate
    } : null,
    leastSuccessful: leastSuccessful ? {
      id: leastSuccessful.id,
      name: leastSuccessful.name,
      successRate: leastSuccessful.successRate
    } : null,
    entityMetrics,
    simulationSpeed: simulation.config?.speed || 1,
    recommendations: generateEntityRecommendations(
      entityMetrics,
      overallSuccessRate,
      simulation.config?.boundaryStrength || 0.5
    ),
    timestamp: new Date().toISOString()
  };
}

// Helper functions

/**
 * Calculates the intensity of concept drift between dimensions
 */
function calculateDriftIntensity(sourceDim: any, targetDim: any) {
  // Base calculation on integrity difference and rule differences
  const integrityDifference = Math.abs(sourceDim.integrity - targetDim.integrity);
  
  // Calculate rule difference (simplified)
  const sourceRules = sourceDim.rules || [];
  const targetRules = targetDim.rules || [];
  const ruleDifference = Math.abs(sourceRules.length - targetRules.length) / 
    Math.max(sourceRules.length, targetRules.length, 1);
  
  // Combined drift intensity on a scale of 0-1
  return Math.min(0.8 * integrityDifference + 0.2 * ruleDifference, 1);
}

/**
 * Calculates semantic shift based on crossing events
 */
function calculateSemanticShift(events: any[]) {
  if (events.length === 0) return 0;
  
  // Calculate based on integrity impacts of events
  const totalImpact = events.reduce((sum, e) => 
    sum + Math.abs(e.integrityImpact || 0), 0);
  
  // Normalize to 0-1 scale
  return Math.min(totalImpact / (events.length * 0.5), 1);
}

/**
 * Calculates truth preservation between dimensions
 */
function calculateTruthPreservation(sourceIntegrity: number, targetIntegrity: number) {
  // Higher value means better truth preservation
  const baseTruthPreservation = 1 - Math.abs(sourceIntegrity - targetIntegrity);
  
  // Adjust for low integrity dimensions
  const minIntegrity = Math.min(sourceIntegrity, targetIntegrity);
  const adjustment = minIntegrity * 0.2;
  
  return Math.max(Math.min(baseTruthPreservation + adjustment, 1), 0);
}

/**
 * Generates recommendations based on drift analysis
 */
function generateRecommendations(
  driftIntensity: number, 
  semanticShift: number, 
  truthPreservation: number
) {
  const recommendations = [];
  
  if (driftIntensity > 0.7) {
    recommendations.push(
      "High concept drift detected. Consider strengthening dimensional boundaries."
    );
  }
  
  if (semanticShift > 0.6) {
    recommendations.push(
      "Significant semantic shift observed. Implement more robust conceptual validation."
    );
  }
  
  if (truthPreservation < 0.4) {
    recommendations.push(
      "Truth preservation critically low. Add additional truth anchoring mechanisms."
    );
  }
  
  if (recommendations.length === 0) {
    recommendations.push(
      "Concept drift within acceptable parameters. Continue monitoring."
    );
  }
  
  return recommendations;
}

/**
 * Calculates integrity trend for a dimension
 */
function calculateIntegrityTrend(dimensionId: string, events: any[]) {
  const relevantEvents = events.filter(e => 
    e.fromDimension === dimensionId || e.toDimension === dimensionId
  );
  
  if (relevantEvents.length === 0) return 0;
  
  // Calculate net integrity impact
  const netImpact = relevantEvents.reduce((sum, e) => {
    // Negative impact when leaving, positive when entering
    const multiplier = e.toDimension === dimensionId ? 1 : -1;
    return sum + (multiplier * (e.integrityImpact || 0));
  }, 0);
  
  // Normalize to a scale from -1 to 1
  return Math.max(Math.min(netImpact / (relevantEvents.length * 0.5), 1), -1);
}

/**
 * Calculates overall system integrity
 */
function calculateSystemIntegrity(dimensions: any[]) {
  if (dimensions.length === 0) return 0;
  
  // Weighted average of all dimension integrities
  const totalIntegrity = dimensions.reduce((sum, dim) => 
    sum + dim.integrity, 0);
  
  return totalIntegrity / dimensions.length;
}

/**
 * Calculates boundary strengths between dimensions
 */
function calculateBoundaryStrengths(dimensions: any[], events: any[]) {
  const boundaries = [];
  
  // For each pair of dimensions
  for (let i = 0; i < dimensions.length; i++) {
    for (let j = i + 1; j < dimensions.length; j++) {
      const dim1 = dimensions[i];
      const dim2 = dimensions[j];
      
      // Find crossing events between these dimensions
      const crossings = events.filter(e => 
        (e.fromDimension === dim1.id && e.toDimension === dim2.id) ||
        (e.fromDimension === dim2.id && e.toDimension === dim1.id)
      );
      
      if (crossings.length > 0) {
        // Calculate success rate of crossings
        const successfulCrossings = crossings.filter(e => e.success).length;
        const successRate = successfulCrossings / crossings.length;
        
        // Boundary strength is inverse of success rate
        const strength = 1 - successRate;
        
        boundaries.push({
          dimension1: {
            id: dim1.id,
            name: dim1.name
          },
          dimension2: {
            id: dim2.id,
            name: dim2.name
          },
          strength,
          crossingCount: crossings.length,
          successRate
        });
      }
    }
  }
  
  return boundaries;
}

/**
 * Generates recommendations for integrity improvement
 */
function generateIntegrityRecommendations(
  systemIntegrity: number,
  dimensionMetrics: any[],
  boundaryStrengths: any[]
) {
  const recommendations = [];
  
  if (systemIntegrity < 0.5) {
    recommendations.push(
      "System integrity below critical threshold. Consider rebalancing dimensional properties."
    );
  }
  
  // Find dimensions with negative integrity trends
  const decliningDimensions = dimensionMetrics
    .filter(d => d.integrityTrend < -0.3)
    .map(d => d.name);
  
  if (decliningDimensions.length > 0) {
    recommendations.push(
      `Declining integrity detected in dimensions: ${decliningDimensions.join(", ")}. Strengthen boundary controls.`
    );
  }
  
  // Find weak boundaries
  const weakBoundaries = boundaryStrengths
    .filter(b => b.strength < 0.3 && b.crossingCount > 2)
    .map(b => `${b.dimension1.name}-${b.dimension2.name}`);
  
  if (weakBoundaries.length > 0) {
    recommendations.push(
      `Weak boundaries detected between: ${weakBoundaries.join(", ")}. Consider increasing boundary strength.`
    );
  }
  
  if (recommendations.length === 0) {
    recommendations.push(
      "System integrity within acceptable parameters. Continue monitoring."
    );
  }
  
  return recommendations;
}

/**
 * Generates recommendations for entity management
 */
function generateEntityRecommendations(
  entityMetrics: any[],
  overallSuccessRate: number,
  boundaryStrength: number
) {
  const recommendations = [];
  
  if (overallSuccessRate < 0.3) {
    recommendations.push(
      "Low crossing success rate. Consider decreasing boundary strength or increasing entity resilience."
    );
  } else if (overallSuccessRate > 0.8 && boundaryStrength < 0.7) {
    recommendations.push(
      "High crossing success rate. Consider increasing boundary strength to maintain dimensional integrity."
    );
  }
  
  // Find entities with high anomaly counts
  const highAnomalyEntities = entityMetrics
    .filter(e => e.anomalyCount > 3)
    .map(e => e.name);
  
  if (highAnomalyEntities.length > 0) {
    recommendations.push(
      `High anomaly counts detected in entities: ${highAnomalyEntities.join(", ")}. Consider entity recalibration.`
    );
  }
  
  // Find entities with high negative integrity impact
  const highImpactEntities = entityMetrics
    .filter(e => e.integrityImpact < -2)
    .map(e => e.name);
  
  if (highImpactEntities.length > 0) {
    recommendations.push(
      `Negative integrity impact from entities: ${highImpactEntities.join(", ")}. Consider restricting dimensional access.`
    );
  }
  
  if (recommendations.length === 0) {
    recommendations.push(
      "Entity performance within acceptable parameters. Continue monitoring."
    );
  }
  
  return recommendations;
}