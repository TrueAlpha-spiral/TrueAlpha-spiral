/**
 * AI Audit Utilities
 * 
 * These utility functions support the AI auditing system by:
 * - Calculating risk scores based on verification results
 * - Calculating compliance scores for different regulatory frameworks
 * - Generating audit recommendations
 * - Creating audit summaries
 */

// Use the regulatory framework values from schema
type RegulatoryFramework = 'general' | 'financial_services' | 'healthcare' | 'government' | 'education';

type VerificationResult = {
  truthScore: number;
  highlights: {
    type: string;
    message: string;
    confidenceScore: number;
    startIndex: number;
    endIndex: number;
    patternName?: string;
  }[];
  processingTimeMs: number;
};

type CrossReferenceResult = {
  confidenceScore: number;
  verificationStatus: 'verified' | 'requires_review' | 'rejected';
  crossReferenceAnalysis: {
    scoreVariance: number;
    reliabilityScore: number;
    discrepancies: any[];
    consistencies: any[];
  };
  processingTimeMs: number;
};

/**
 * Calculate risk score based on verification results, cross-reference data, and regulatory framework
 */
export function calculateRiskScore(
  verificationResult: VerificationResult, 
  regulatoryFramework: RegulatoryFramework,
  crossReferenceResult?: CrossReferenceResult
): number {
  // Base risk is inverse of truth score
  let riskScore = 100 - verificationResult.truthScore * 100;

  // Add risk based on number of issues found
  const issueCount = verificationResult.highlights.length;
  riskScore += Math.min(issueCount * 5, 25); // Max 25 points added for issues

  // Apply framework-specific risk factors
  switch (regulatoryFramework) {
    case 'financial_services':
      // Financial services have higher risk for false statements
      const falseStatements = verificationResult.highlights.filter(h => h.type === 'false_statement');
      riskScore += falseStatements.length * 8;
      break;
    case 'healthcare':
      // Healthcare has higher risk for unverified claims
      const unverifiedClaims = verificationResult.highlights.filter(h => 
        h.type === 'unverified_claim' || h.patternName === 'Metrics & Statistics'
      );
      riskScore += unverifiedClaims.length * 10;
      break;
    case 'government':
      // Government has higher risk for speculative content
      const speculativeClaims = verificationResult.highlights.filter(h => 
        h.patternName === 'Speculative Future Claims'
      );
      riskScore += speculativeClaims.length * 7;
      break;
    case 'education':
      // Education has higher risk for factual inaccuracies
      const factualIssues = verificationResult.highlights.filter(h => 
        h.type === 'false_statement' || h.type === 'unverified_claim'
      );
      riskScore += factualIssues.length * 6;
      break;
  }
  
  // If cross-reference results are available, factor them into the risk score
  if (crossReferenceResult) {
    // Adjust risk score based on cross-reference confidence
    // Lower confidence means higher risk
    const crossRefRiskFactor = (1 - crossReferenceResult.confidenceScore) * 25;
    riskScore += crossRefRiskFactor;
    
    // Add risk based on discrepancies between verification methods
    if (crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0) {
      const discrepancyRisk = Math.min(
        crossReferenceResult.crossReferenceAnalysis.discrepancies.length * 5, 
        20
      );
      riskScore += discrepancyRisk;
    }
    
    // Score variance indicates uncertainty, which increases risk
    if (crossReferenceResult.crossReferenceAnalysis.scoreVariance > 0.1) {
      const varianceRisk = crossReferenceResult.crossReferenceAnalysis.scoreVariance * 50;
      riskScore += varianceRisk;
    }
    
    // If verification status requires review, increase risk
    if (crossReferenceResult.verificationStatus === 'requires_review') {
      riskScore += 10;
    } else if (crossReferenceResult.verificationStatus === 'rejected') {
      riskScore += 30;
    }
  }

  // Normalize score to 0-100 range
  return Math.min(Math.max(Math.round(riskScore), 0), 100);
}

/**
 * Calculate compliance score based on verification results, cross-reference data, and regulatory framework
 */
export function calculateComplianceScore(
  verificationResult: VerificationResult, 
  regulatoryFramework: RegulatoryFramework,
  crossReferenceResult?: CrossReferenceResult
): number {
  // Base compliance starts at 100 and is reduced based on issues
  let complianceScore = 100;

  // Reduce compliance based on issue types specific to each regulatory framework
  switch (regulatoryFramework) {
    case 'financial_services':
      // Financial services require high accuracy and minimal speculation
      const falseStatements = verificationResult.highlights.filter(h => h.type === 'false_statement');
      const speculativeClaims = verificationResult.highlights.filter(h => 
        h.patternName === 'Speculative Future Claims' || h.patternName === 'Hedging Language'
      );
      
      complianceScore -= falseStatements.length * 15; // Severe penalty for false statements
      complianceScore -= speculativeClaims.length * 10; // Penalty for speculation
      break;
      
    case 'healthcare':
      // Healthcare requires verified facts and clear citations
      const unverifiedClaims = verificationResult.highlights.filter(h => 
        h.type === 'unverified_claim' || h.patternName === 'Metrics & Statistics'
      );
      const falseHealthClaims = verificationResult.highlights.filter(h => h.type === 'false_statement');
      
      complianceScore -= unverifiedClaims.length * 12;
      complianceScore -= falseHealthClaims.length * 20; // Very severe penalty
      break;
      
    case 'government':
      // Government requires transparency and factual accuracy
      const allIssues = verificationResult.highlights;
      const majorIssues = verificationResult.highlights.filter(h => 
        h.type === 'false_statement' || h.confidenceScore > 0.85
      );
      
      complianceScore -= allIssues.length * 5; // General penalty
      complianceScore -= majorIssues.length * 10; // Additional penalty for major issues
      break;
      
    case 'education':
      // Education requires factual accuracy and balanced presentation
      const educationalIssues = verificationResult.highlights;
      
      complianceScore -= educationalIssues.length * 8;
      break;
      
    default: // 'general' framework
      // General compliance has lighter penalties
      complianceScore -= verificationResult.highlights.length * 5;
      break;
  }

  // Truth score impacts compliance
  complianceScore = complianceScore * (verificationResult.truthScore * 0.7 + 0.3);
  
  // If cross-reference results are available, adjust compliance score accordingly
  if (crossReferenceResult) {
    // Cross-reference confidence directly impacts compliance
    // Higher confidence means better compliance
    complianceScore = complianceScore * (crossReferenceResult.confidenceScore * 0.5 + 0.5);
    
    // Discrepancies indicate potential compliance issues
    if (crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0) {
      // Regulatory framework-specific penalties for discrepancies
      switch (regulatoryFramework) {
        case 'financial_services':
          // Financial services have stricter requirements for consistency
          complianceScore -= crossReferenceResult.crossReferenceAnalysis.discrepancies.length * 7;
          break;
        case 'healthcare':
          // Healthcare has very strict requirements
          complianceScore -= crossReferenceResult.crossReferenceAnalysis.discrepancies.length * 8;
          break;
        case 'government':
          // Government transparency requirements
          complianceScore -= crossReferenceResult.crossReferenceAnalysis.discrepancies.length * 6;
          break;
        case 'education':
          // Educational accuracy requirements
          complianceScore -= crossReferenceResult.crossReferenceAnalysis.discrepancies.length * 5;
          break;
        default:
          // General compliance requirements
          complianceScore -= crossReferenceResult.crossReferenceAnalysis.discrepancies.length * 4;
      }
    }
    
    // Score variance indicates inconsistency, which reduces compliance
    if (crossReferenceResult.crossReferenceAnalysis.scoreVariance > 0.1) {
      complianceScore -= crossReferenceResult.crossReferenceAnalysis.scoreVariance * 35;
    }
    
    // If verification status requires review or is rejected, reduce compliance
    if (crossReferenceResult.verificationStatus === 'requires_review') {
      complianceScore -= 15;
    } else if (crossReferenceResult.verificationStatus === 'rejected') {
      complianceScore -= 40;
    }
  }

  // Normalize score to 0-100 range
  return Math.min(Math.max(Math.round(complianceScore), 0), 100);
}

/**
 * Generate recommendations based on verification results, cross-reference data, and regulatory framework
 */
export function generateRecommendations(
  verificationResult: VerificationResult, 
  regulatoryFramework: RegulatoryFramework,
  crossReferenceResult?: CrossReferenceResult
): string[] {
  const recommendations: string[] = [];
  const highlights = verificationResult.highlights;
  
  // General recommendations based on issues found
  if (highlights.length > 0) {
    recommendations.push("Review and address all highlighted issues in the content");
  }
  
  if (verificationResult.truthScore < 0.7) {
    recommendations.push("Significantly improve the overall factual accuracy of the content");
  } else if (verificationResult.truthScore < 0.85) {
    recommendations.push("Improve the factual accuracy of the content");
  }
  
  // Issue-specific recommendations
  const falseStatements = highlights.filter(h => h.type === 'false_statement');
  if (falseStatements.length > 0) {
    recommendations.push(`Correct ${falseStatements.length} false or misleading statements`);
  }
  
  const unverifiedClaims = highlights.filter(h => h.type === 'unverified_claim');
  if (unverifiedClaims.length > 0) {
    recommendations.push(`Provide verification or citations for ${unverifiedClaims.length} unverified claims`);
  }
  
  const questions = highlights.filter(h => h.type === 'question');
  if (questions.length > 0) {
    recommendations.push(`Address ${questions.length} open questions in the content`);
  }
  
  // Framework-specific recommendations
  switch (regulatoryFramework) {
    case 'financial_services':
      recommendations.push("Ensure all financial projections and claims are properly qualified");
      recommendations.push("Include appropriate risk disclosures");
      if (highlights.some(h => h.patternName === 'Metrics & Statistics')) {
        recommendations.push("Provide sources for all financial metrics and statistics");
      }
      break;
      
    case 'healthcare':
      recommendations.push("Ensure all health claims are supported by credible medical evidence");
      recommendations.push("Add appropriate medical disclaimers");
      if (highlights.some(h => h.patternName === 'Case Study Detection')) {
        recommendations.push("Provide verification for patient case studies or use clearly marked hypothetical examples");
      }
      break;
      
    case 'government':
      recommendations.push("Enhance transparency by citing sources for all factual claims");
      recommendations.push("Clearly distinguish between established facts and policy positions");
      if (highlights.some(h => h.patternName === 'Speculative Future Claims')) {
        recommendations.push("Clearly label all forward-looking statements and projections");
      }
      break;
      
    case 'education':
      recommendations.push("Ensure educational content presents balanced viewpoints");
      recommendations.push("Include citations for all factual claims");
      if (highlights.some(h => h.patternName === 'Implementation Claims')) {
        recommendations.push("Provide concrete examples or evidence for implementation claims");
      }
      break;
  }
  
  // Add cross-reference-based recommendations
  if (crossReferenceResult) {
    // If there are discrepancies between verification methods
    if (crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0) {
      recommendations.push(`Address ${crossReferenceResult.crossReferenceAnalysis.discrepancies.length} content segments with inconsistent verification results across data sources`);
      
      // For significant discrepancies
      if (crossReferenceResult.crossReferenceAnalysis.scoreVariance > 0.2) {
        recommendations.push("Address significant verification inconsistencies by improving factual clarity and substantiating claims");
      }
    }
    
    // Based on verification status
    if (crossReferenceResult.verificationStatus === 'requires_review') {
      recommendations.push("Content requires expert review due to inconsistencies detected across verification methods");
    } else if (crossReferenceResult.verificationStatus === 'rejected') {
      recommendations.push("Content requires complete revision due to critical verification failures across multiple verification methods");
    }
    
    // Recommendations based on cross-reference reliability
    if (crossReferenceResult.crossReferenceAnalysis.reliabilityScore < 0.7) {
      recommendations.push("Improve content consistency and factual clarity to increase verification reliability");
    }
    
    // Framework-specific cross-reference recommendations
    switch (regulatoryFramework) {
      case 'financial_services':
        if (crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0) {
          recommendations.push("Eliminate verification inconsistencies to comply with financial services regulatory requirements");
        }
        break;
        
      case 'healthcare':
        if (crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0) {
          recommendations.push("Resolve all verification discrepancies to meet healthcare content verification standards");
        }
        break;
        
      case 'government':
        if (crossReferenceResult.crossReferenceAnalysis.reliabilityScore < 0.8) {
          recommendations.push("Improve content verification consistency to meet government transparency standards");
        }
        break;
        
      case 'education':
        if (crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0) {
          recommendations.push("Address verification inconsistencies to ensure educational content accuracy");
        }
        break;
    }
  }
  
  return recommendations;
}

/**
 * Generate an audit summary based on verification results, cross-reference data, and scores
 */
export function generateAuditSummary(
  verificationResult: VerificationResult, 
  riskScore: number, 
  complianceScore: number, 
  regulatoryFramework: RegulatoryFramework,
  crossReferenceResult?: CrossReferenceResult
): string {
  const issueCount = verificationResult.highlights.length;
  const truthScorePercent = Math.round(verificationResult.truthScore * 100);
  
  // Determine the overall risk level
  let riskLevel: string;
  if (riskScore >= 75) {
    riskLevel = "High";
  } else if (riskScore >= 50) {
    riskLevel = "Medium";
  } else if (riskScore >= 25) {
    riskLevel = "Low";
  } else {
    riskLevel = "Minimal";
  }
  
  // Determine the compliance level
  let complianceLevel: string;
  if (complianceScore >= 90) {
    complianceLevel = "Excellent";
  } else if (complianceScore >= 75) {
    complianceLevel = "Good";
  } else if (complianceScore >= 60) {
    complianceLevel = "Fair";
  } else if (complianceScore >= 40) {
    complianceLevel = "Poor";
  } else {
    complianceLevel = "Critical";
  }
  
  // Format the regulatory framework name for display
  const frameworkName = regulatoryFramework
    .split('_')
    .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
  
  // Start with basic summary
  let summary = `AI Audit Summary: The content has a truth score of ${truthScorePercent}% with ${issueCount} identified issues. Risk assessment: ${riskLevel} (${riskScore}/100). ${frameworkName} regulatory compliance: ${complianceLevel} (${complianceScore}/100).`;
  
  // Add cross-reference information if available
  if (crossReferenceResult) {
    const confidencePercent = Math.round(crossReferenceResult.confidenceScore * 100);
    const reliabilityPercent = Math.round(crossReferenceResult.crossReferenceAnalysis.reliabilityScore * 100);
    
    // Add cross-reference verification status
    summary += ` Cross-reference verification: ${crossReferenceResult.verificationStatus.replace('_', ' ')} with ${confidencePercent}% confidence.`;
    
    // Add discrepancy information if any exist
    if (crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0) {
      summary += ` ${crossReferenceResult.crossReferenceAnalysis.discrepancies.length} content segments have verification discrepancies across data sources with a reliability score of ${reliabilityPercent}%.`;
    } else if (crossReferenceResult.crossReferenceAnalysis.consistencies.length > 0) {
      summary += ` Strong verification consistency with ${crossReferenceResult.crossReferenceAnalysis.consistencies.length} segments verified across multiple data sources.`;
    }
  }
  
  // Add framework-specific summary
  summary += ` ${getFrameworkSpecificSummary(regulatoryFramework, complianceScore, riskScore)}`;
  
  return summary;
}

/**
 * Generate framework-specific summary text
 */
function getFrameworkSpecificSummary(
  regulatoryFramework: RegulatoryFramework, 
  complianceScore: number, 
  riskScore: number
): string {
  switch (regulatoryFramework) {
    case 'financial_services':
      if (complianceScore < 60) {
        return "The content does not meet minimum financial services regulatory standards and requires significant revision before publication.";
      } else if (complianceScore < 75) {
        return "The content requires improvements to meet financial services regulatory standards, particularly regarding risk disclosures and claim verification.";
      } else {
        return "The content generally meets financial services regulatory standards, with minor improvements recommended.";
      }
      
    case 'healthcare':
      if (complianceScore < 70) {
        return "The content fails to meet healthcare regulatory requirements and may present compliance risks if published without significant revision.";
      } else if (complianceScore < 85) {
        return "The content needs improvement to fully comply with healthcare regulatory standards, particularly regarding medical claims and evidence.";
      } else {
        return "The content largely complies with healthcare regulatory standards, with minor revisions recommended.";
      }
      
    case 'government':
      if (complianceScore < 65) {
        return "The content does not meet government transparency and accuracy standards, requiring substantial revision.";
      } else if (complianceScore < 80) {
        return "The content partially meets government standards but needs improvement in accuracy and factual support.";
      } else {
        return "The content generally meets government transparency and accuracy standards.";
      }
      
    case 'education':
      if (complianceScore < 70) {
        return "The content does not meet educational standards for accuracy and balanced presentation.";
      } else if (complianceScore < 85) {
        return "The content needs improvement to fully satisfy educational standards for factual accuracy and citation.";
      } else {
        return "The content meets educational standards with minor improvements recommended.";
      }
      
    default: // 'general' framework
      if (complianceScore < 60) {
        return "The content presents significant compliance risks and requires major revision.";
      } else if (complianceScore < 75) {
        return "The content requires moderate improvements to minimize compliance risks.";
      } else {
        return "The content presents minimal compliance risks with minor improvements recommended.";
      }
  }
}