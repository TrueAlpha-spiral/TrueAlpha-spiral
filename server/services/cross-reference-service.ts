import { verificationEngine } from './verification-engine';
import { type VerificationResult, type TruthPattern, type CrossReferenceResult } from '@shared/schema';
import axios from 'axios';

// Define types for the analyzing results
interface SourceResult {
  truthScore?: number;
  verification_score?: number;
  highlights?: any[];
  originalText?: string;
}

interface Assessment {
  sourceId: string;
  type: 'factual' | 'speculative' | 'fabricated';
  confidence: number;
  message: string;
}

/**
 * CrossReferenceService provides methods to verify content against multiple
 * data sources and compare results to improve accuracy and confidence.
 */
export class CrossReferenceService {
  /**
   * List of available verification data sources
   * Each source has a different verification method
   */
  private dataSources = [
    {
      id: 'internal-patterns',
      name: 'Truth Pattern Analysis',
      description: 'Checks content against known truth patterns',
      priority: 1
    },
    {
      id: 'fact-database',
      name: 'Factual Database',
      description: 'Verifies against known facts',
      priority: 2
    },
    {
      id: 'python-analysis',
      name: 'Python Analysis Engine',
      description: 'Uses Python-based quantum echo verification',
      priority: 3
    }
  ];

  /**
   * Performs verification across multiple data sources and cross-references the results
   * to improve accuracy and confidence in the verification.
   */
  async crossVerifyContent(
    text: string,
    patterns: TruthPattern[],
    options: { 
      enabledSources?: string[],
      minConfidenceThreshold?: number,
      regulatoryFramework?: string
    } = {}
  ): Promise<CrossReferenceResult> {
    const startTime = Date.now();
    console.log("[CrossRef] Starting cross-reference verification");

    // Default options
    const {
      enabledSources = this.dataSources.map(source => source.id),
      minConfidenceThreshold = 0.8,
      regulatoryFramework = 'general'
    } = options;

    // Filter enabled data sources by priority
    const activeSources = this.dataSources
      .filter(source => enabledSources.includes(source.id))
      .sort((a, b) => a.priority - b.priority);

    console.log(`[CrossRef] Using sources: ${activeSources.map(s => s.name).join(', ')}`);

    // Store results from each source
    const sourceResults: Record<string, any> = {};
    const sourceVerificationScores: Record<string, number> = {};
    
    // Collect verification results from all sources
    for (const source of activeSources) {
      try {
        console.log(`[CrossRef] Verifying with source: ${source.name}`);
        const result = await this.verifyWithSource(source.id, text, patterns, regulatoryFramework);
        sourceResults[source.id] = result;
        
        // Extract verification score based on source type
        if (source.id === 'internal-patterns' || source.id === 'fact-database') {
          sourceVerificationScores[source.id] = (result as VerificationResult).truthScore;
        } else if (source.id === 'python-analysis') {
          sourceVerificationScores[source.id] = result.verification_score;
        }
      } catch (error) {
        console.error(`[CrossRef] Error verifying with source ${source.name}:`, error);
        // Continue with other sources
      }
    }

    // Cross-reference the results
    const crossReferenceAnalysis = this.analyzeResults(sourceResults, sourceVerificationScores);
    
    // Calculate confidence score across sources
    const confidenceScore = this.calculateConfidenceScore(sourceVerificationScores);
    
    // Determine verification status based on confidence threshold
    const verificationStatus = confidenceScore >= minConfidenceThreshold 
      ? 'verified' 
      : 'requires_review';

    // Generate reconciled result
    const reconciledResult = this.reconcileResults(sourceResults, crossReferenceAnalysis);
    
    return {
      originalText: text,
      confidenceScore,
      verificationStatus,
      sourceResults,
      crossReferenceAnalysis,
      reconciledResult,
      processingTimeMs: Date.now() - startTime
    };
  }

  /**
   * Performs cross-reference verification using verification result
   */
  async performCrossReferenceVerification(
    content: string,
    verificationResult: VerificationResult,
    options: {
      enabledSources?: string[],
      minConfidenceThreshold?: number,
      regulatoryFramework?: string
    } = {}
  ): Promise<CrossReferenceResult> {
    // Use the existing verification result as the internal-patterns source
    const sourceResults: Record<string, any> = {
      'internal-patterns': verificationResult
    };
    const sourceVerificationScores: Record<string, number> = {
      'internal-patterns': verificationResult.truthScore
    };
    
    // Get enabled sources excluding internal-patterns which we already have
    const { 
      enabledSources = this.dataSources.map(source => source.id),
      minConfidenceThreshold = 0.8,
      regulatoryFramework = 'general'
    } = options;
    
    const otherSources = this.dataSources
      .filter(source => source.id !== 'internal-patterns' && enabledSources.includes(source.id))
      .sort((a, b) => a.priority - b.priority);
    
    // Get results from other sources
    for (const source of otherSources) {
      try {
        console.log(`[CrossRef] Verifying with source: ${source.name}`);
        // Since we don't have patterns here, just pass an empty array
        const result = await this.verifyWithSource(source.id, content, [], regulatoryFramework);
        sourceResults[source.id] = result;
        
        // Extract verification score based on source type
        if (source.id === 'fact-database') {
          sourceVerificationScores[source.id] = (result as VerificationResult).truthScore;
        } else if (source.id === 'python-analysis') {
          sourceVerificationScores[source.id] = result.verification_score;
        }
      } catch (error) {
        console.error(`[CrossRef] Error verifying with source ${source.name}:`, error);
        // Continue with other sources
      }
    }
    
    // Cross-reference the results
    const crossReferenceAnalysis = this.analyzeResults(sourceResults, sourceVerificationScores);
    
    // Calculate confidence score across sources
    const confidenceScore = this.calculateConfidenceScore(sourceVerificationScores);
    
    // Determine verification status based on confidence threshold
    const verificationStatus = confidenceScore >= minConfidenceThreshold 
      ? 'verified' 
      : 'requires_review';
    
    // Generate reconciled result
    const reconciledResult = this.reconcileResults(sourceResults, crossReferenceAnalysis);
    
    return {
      originalText: content,
      confidenceScore,
      verificationStatus,
      sourceResults,
      crossReferenceAnalysis,
      reconciledResult,
      processingTimeMs: Date.now() - verificationResult.processingTimeMs
    };
  }

  /**
   * Verifies content using a specific data source
   */
  private async verifyWithSource(
    sourceId: string, 
    text: string, 
    patterns: TruthPattern[],
    regulatoryFramework: string
  ): Promise<any> {
    switch (sourceId) {
      case 'internal-patterns':
        return await verificationEngine.verifyText(text, patterns);
        
      case 'fact-database':
        // This would call a different verification method that focuses on facts
        // For now, we'll use the same engine but could be extended
        return await verificationEngine.verifyText(text, patterns);
        
      case 'python-analysis':
        try {
          // Call Python API for verification
          const response = await axios.post('/api/python-system/verify', {
            content: text,
            framework: regulatoryFramework
          });
          return response.data;
        } catch (error) {
          console.error('[CrossRef] Python API error:', error);
          throw new Error('Python verification failed');
        }
        
      default:
        throw new Error(`Unknown data source: ${sourceId}`);
    }
  }

  /**
   * Analyzes results from different sources and identifies discrepancies
   */
  private analyzeResults(
    sourceResults: Record<string, any>,
    sourceVerificationScores: Record<string, number>
  ): any {
    const discrepancies = [];
    const consistencies = [];
    
    // Compare scores across sources
    const scores = Object.values(sourceVerificationScores);
    const avgScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    const scoreVariance = Math.sqrt(
      scores.reduce((sum, score) => sum + Math.pow(score - avgScore, 2), 0) / scores.length
    );
    
    // Identify sentence-level discrepancies
    const sentenceAnalysis: Record<string, any> = {};
    
    // Check for results with highlights (sentence-level analysis)
    const resultsWithHighlights = Object.entries(sourceResults)
      .filter(([_, result]) => result.highlights && Array.isArray(result.highlights));
    
    if (resultsWithHighlights.length > 0) {
      // Build a map of sentences and their verification types across sources
      for (const [sourceId, result] of resultsWithHighlights) {
        for (const highlight of result.highlights) {
          const sentenceKey = `${highlight.startIndex}-${highlight.endIndex}`;
          if (!sentenceAnalysis[sentenceKey]) {
            sentenceAnalysis[sentenceKey] = {
              text: result.originalText.substring(highlight.startIndex, highlight.endIndex),
              assessments: []
            };
          }
          
          sentenceAnalysis[sentenceKey].assessments.push({
            sourceId,
            type: highlight.type as 'factual' | 'speculative' | 'fabricated',
            confidence: highlight.confidenceScore,
            message: highlight.message
          });
        }
      }
      
      // Analyze each sentence for discrepancies
      for (const [sentenceKey, analysis] of Object.entries(sentenceAnalysis)) {
        const types = analysis.assessments.map((a: Assessment) => a.type);
        
        // Check if all sources agree
        const allAgree = types.every((type: string) => type === types[0]);
        
        if (allAgree) {
          consistencies.push({
            sentence: analysis.text,
            agreedType: types[0] as 'factual' | 'speculative' | 'fabricated',
            sources: analysis.assessments.map((a: Assessment) => a.sourceId)
          });
        } else {
          discrepancies.push({
            sentence: analysis.text,
            assessments: analysis.assessments as Assessment[],
            recommendation: this.generateDiscrepancyRecommendation(analysis.assessments as Assessment[])
          });
        }
      }
    }
    
    return {
      scoreVariance,
      avgScore,
      discrepancies,
      consistencies,
      reliabilityScore: 1 - (scoreVariance / (avgScore > 0 ? avgScore : 1)),
      sentenceAnalysis: Object.values(sentenceAnalysis)
    };
  }

  /**
   * Calculates an overall confidence score based on multiple sources
   */
  private calculateConfidenceScore(sourceVerificationScores: Record<string, number>): number {
    // Weighted average based on source priority
    let totalScore = 0;
    let totalWeight = 0;
    
    for (const [sourceId, score] of Object.entries(sourceVerificationScores)) {
      const source = this.dataSources.find(s => s.id === sourceId);
      if (source) {
        // Higher priority (lower number) gets higher weight
        const weight = 1 / source.priority;
        totalScore += score * weight;
        totalWeight += weight;
      }
    }
    
    return totalWeight > 0 ? totalScore / totalWeight : 0;
  }

  /**
   * Generates a recommendation for a sentence with discrepancies
   */
  private generateDiscrepancyRecommendation(assessments: Assessment[]): string {
    // Count how many of each type
    const typeCounts = assessments.reduce((counts, assessment) => {
      counts[assessment.type] = (counts[assessment.type] || 0) + 1;
      return counts;
    }, {} as Record<string, number>);
    
    // Get type with highest count
    const sortedTypeCounts = Object.entries(typeCounts)
      .sort((a: [string, number], b: [string, number]) => b[1] - a[1]);
    
    if (sortedTypeCounts.length === 0) {
      return 'Unable to determine consensus. Review manually.';
    }
    
    const mostCommonType = sortedTypeCounts[0][0];
    const totalAssessments = assessments.length;
    const majorityCount = sortedTypeCounts[0][1];
    const majorityPercentage = (majorityCount / totalAssessments) * 100;
    
    // Generate recommendation based on the level of agreement
    if (majorityPercentage >= 75) {
      // Strong consensus
      if (mostCommonType === 'factual') {
        return 'High consensus that this is factual content (75%+ agreement).';
      } else if (mostCommonType === 'speculative') {
        return 'High consensus that this is speculative content. Consider rephrasing with qualifying language.';
      } else {
        return 'High consensus that this content may be fabricated. High priority for review or removal.';
      }
    } else if (majorityPercentage >= 50) {
      // Moderate consensus
      if (mostCommonType === 'factual') {
        return 'Moderate consensus that this is factual, but verify with additional sources if critical.';
      } else if (mostCommonType === 'speculative') {
        return 'Moderate consensus that this is speculative content. Consider adding qualifying language.';
      } else {
        return 'Moderate consensus that this content may be fabricated. Review recommended.';
      }
    } else {
      // Low consensus
      return 'Low consensus between verification sources. Multiple perspectives detected. Review manually.';
    }
  }

  /**
   * Reconciles results from multiple sources into a single result
   */
  private reconcileResults(
    sourceResults: Record<string, any>,
    crossReferenceAnalysis: any
  ): any {
    // Use the most conservative approach - if any source marks as fabricated, 
    // treat as fabricated, etc.
    const conservativeTruthScore = Math.min(
      ...Object.values(sourceResults)
        .filter(result => result.truthScore !== undefined)
        .map(result => result.truthScore)
    );
    
    // Start with the first result's highlights as a base
    const firstResultKey = Object.keys(sourceResults)[0];
    if (!firstResultKey || !sourceResults[firstResultKey]) {
      return { error: "No results available to reconcile" };
    }
    
    const baseResult = sourceResults[firstResultKey];
    
    // Modify highlights based on cross-reference analysis
    const modifiedHighlights = [...(baseResult.highlights || [])];
    
    // Update highlights for sentences with discrepancies
    for (const discrepancy of crossReferenceAnalysis.discrepancies) {
      // Find the highlight for this sentence
      const highlightIndex = modifiedHighlights.findIndex(h => 
        baseResult.originalText.substring(h.startIndex, h.endIndex) === discrepancy.sentence
      );
      
      if (highlightIndex >= 0) {
        // Update the highlight with the recommendation
        modifiedHighlights[highlightIndex] = {
          ...modifiedHighlights[highlightIndex],
          message: `[Cross-Reference] ${discrepancy.recommendation}`,
          crossReferenced: true
        };
      }
    }
    
    return {
      originalText: baseResult.originalText,
      truthScore: conservativeTruthScore,
      overallScore: crossReferenceAnalysis.reliabilityScore,
      highlights: modifiedHighlights,
      processingTimeMs: baseResult.processingTimeMs,
      summary: baseResult.summary,
      crossReferenceSummary: {
        reliabilityScore: crossReferenceAnalysis.reliabilityScore,
        discrepancyCount: crossReferenceAnalysis.discrepancies.length,
        consistencyCount: crossReferenceAnalysis.consistencies.length
      }
    };
  }
}

// Export a singleton instance
export const crossReferenceService = new CrossReferenceService();