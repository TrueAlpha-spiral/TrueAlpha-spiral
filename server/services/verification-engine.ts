import { type VerificationResult, type TruthPattern } from '@shared/schema';

/**
 * VerificationEngine provides the core functionality for analyzing text
 * and detecting potentially fabricated or speculative content.
 */
export class VerificationEngine {
  /**
   * Analyzes text against a set of truth patterns to detect potentially
   * fabricated or speculative content.
   */
  async verifyText(
    text: string,
    patterns: TruthPattern[]
  ): Promise<VerificationResult> {
    const startTime = Date.now();
    
    // Preprocess the text
    const sentences = this.splitIntoSentences(text);
    
    // Initialize result structure
    const highlights: VerificationResult['highlights'] = [];
    let totalConfidence = 0;
    
    // Track summary statistics
    let factualCount = 0;
    let speculativeCount = 0;
    let fabricatedCount = 0;
    
    // Process each sentence
    for (const sentence of sentences) {
      const { index, text: sentenceText } = sentence;
      
      // Check against each pattern
      const patternResults = patterns
        .filter(p => p.isActive)
        .map(pattern => this.checkPattern(sentenceText, pattern))
        .filter(result => result !== null) as Array<{
          pattern: TruthPattern;
          confidence: number;
          type: 'factual' | 'speculative' | 'fabricated';
          message: string;
        }>;
      
      // If no patterns matched, consider it factual by default
      if (patternResults.length === 0) {
        factualCount++;
        highlights.push({
          startIndex: index,
          endIndex: index + sentenceText.length,
          type: 'factual',
          confidenceScore: 0.95,
          message: 'This content appears to be factual.',
          patternName: 'Default Factual'
        });
        totalConfidence += 0.95;
        continue;
      }
      
      // Get the most concerning result (lowest confidence = highest concern)
      const mostConcerningResult = patternResults.sort((a, b) => a.confidence - b.confidence)[0];
      
      // Add highlight based on the result
      highlights.push({
        startIndex: index,
        endIndex: index + sentenceText.length,
        type: mostConcerningResult.type,
        confidenceScore: mostConcerningResult.confidence,
        message: mostConcerningResult.message,
        patternName: mostConcerningResult.pattern.name
      });
      
      // Update statistics
      if (mostConcerningResult.type === 'factual') {
        factualCount++;
      } else if (mostConcerningResult.type === 'speculative') {
        speculativeCount++;
      } else {
        fabricatedCount++;
      }
      
      totalConfidence += mostConcerningResult.confidence;
    }
    
    // Calculate overall truth score (average confidence across all sentences)
    const truthScore = sentences.length > 0 ? totalConfidence / sentences.length : 1.0;
    
    // Calculate processing time
    const processingTimeMs = Date.now() - startTime;
    
    return {
      originalText: text,
      truthScore,
      overallScore: truthScore, // Same as truthScore for now
      highlights,
      processingTimeMs,
      summary: {
        factualCount,
        speculativeCount,
        fabricatedCount,
        totalSentences: sentences.length
      }
    };
  }
  
  /**
   * Checks a text fragment against a specific truth pattern.
   */
  private checkPattern(
    text: string,
    pattern: TruthPattern
  ): { pattern: TruthPattern; confidence: number; type: 'factual' | 'speculative' | 'fabricated'; message: string; } | null {
    // Pattern-specific detection logic
    let confidence = 1.0;
    let message = '';
    let type: 'factual' | 'speculative' | 'fabricated' = 'factual';
    
    switch (pattern.category) {
      case 'Technical':
        // Check for implementation claims
        if (pattern.name === 'Implementation Claims' && this.containsImplementationClaims(text)) {
          confidence = 0.6;
          message = 'This contains technical implementation claims that may be speculative.';
          type = confidence < pattern.confidenceThreshold ? 'fabricated' : 'speculative';
        }
        break;
        
      case 'Data':
        // Check for metrics and statistics
        if (pattern.name === 'Metrics & Statistics' && this.containsUncitedStatistics(text)) {
          confidence = 0.5;
          message = 'This contains metrics or statistics without proper citation.';
          type = confidence < pattern.confidenceThreshold ? 'fabricated' : 'speculative';
        }
        break;
        
      case 'Business':
        // Check for case studies
        if (pattern.name === 'Case Study Detection' && this.containsCaseStudy(text)) {
          confidence = 0.65;
          message = 'This contains case study examples that may be fabricated.';
          type = confidence < pattern.confidenceThreshold ? 'fabricated' : 'speculative';
        }
        break;
        
      case 'Predictions':
        // Check for future claims
        if (pattern.name === 'Speculative Future Claims' && this.containsFutureClaims(text)) {
          confidence = 0.7;
          message = 'This makes specific claims about future outcomes without proper qualification.';
          type = confidence < pattern.confidenceThreshold ? 'fabricated' : 'speculative';
        }
        break;
        
      case 'Language':
        // Check for hedging language
        if (pattern.name === 'Hedging Language' && this.containsHedgingLanguage(text)) {
          confidence = 0.75;
          message = 'This contains hedging language that indicates uncertainty.';
          type = confidence < pattern.confidenceThreshold ? 'fabricated' : 'speculative';
        }
        break;
    }
    
    // If detected pattern doesn't meet threshold, return result
    if (confidence < 1.0) {
      return { pattern, confidence, type, message };
    }
    
    // No match
    return null;
  }
  
  /**
   * Splits text into sentences with their starting indices.
   */
  private splitIntoSentences(text: string): Array<{ index: number; text: string }> {
    const sentenceRegex = /[^.!?]+[.!?]+/g;
    const sentences: Array<{ index: number; text: string }> = [];
    
    let match;
    while ((match = sentenceRegex.exec(text)) !== null) {
      sentences.push({
        index: match.index,
        text: match[0].trim()
      });
    }
    
    // Handle text without punctuation or remaining text
    if (sentences.length === 0 || (sentences.length > 0 && 
        sentences[sentences.length - 1].index + sentences[sentences.length - 1].text.length < text.length)) {
      const lastEnd = sentences.length > 0 
        ? sentences[sentences.length - 1].index + sentences[sentences.length - 1].text.length 
        : 0;
      
      if (lastEnd < text.length) {
        const remainingText = text.substring(lastEnd).trim();
        if (remainingText.length > 0) {
          sentences.push({
            index: lastEnd,
            text: remainingText
          });
        }
      }
    }
    
    return sentences;
  }
  
  // Pattern detection helper methods
  
  private containsImplementationClaims(text: string): boolean {
    const implementationKeywords = [
      'implements', 'implemented', 'implementation', 'algorithm',
      'framework', 'architecture', 'system design', 'module',
      'component', 'integrates', 'integrated', 'built-in'
    ];
    
    return this.containsAnyKeywords(text, implementationKeywords);
  }
  
  private containsUncitedStatistics(text: string): boolean {
    // Check for numbers and percentages without citations
    const hasNumbers = /\d+%|\d+\s*percent|\d+\.\d+|\b\d{2,}\b/.test(text);
    const hasCitation = /\[\d+\]|\(\d{4}\)|cited by|according to|reference|study|research shows/.test(text.toLowerCase());
    
    return hasNumbers && !hasCitation;
  }
  
  private containsCaseStudy(text: string): boolean {
    const caseStudyKeywords = [
      'case study', 'example', 'for instance', 'for example',
      'customer', 'client', 'organization', 'company', 'business',
      'experienced', 'achieved', 'resulted in', 'leading to'
    ];
    
    return this.containsAnyKeywords(text, caseStudyKeywords);
  }
  
  private containsFutureClaims(text: string): boolean {
    const futureKeywords = [
      'will', 'going to', 'future', 'predict', 'projected',
      'forecast', 'expected to', 'anticipated', 'upcoming',
      'soon', 'plan to', 'intend to', 'in the coming'
    ];
    
    return this.containsAnyKeywords(text, futureKeywords);
  }
  
  private containsHedgingLanguage(text: string): boolean {
    const hedgingKeywords = [
      'may', 'might', 'could', 'possibly', 'perhaps',
      'potential', 'sometimes', 'often', 'usually', 'typically',
      'generally', 'likely', 'unlikely', 'probably', 'approximately',
      'around', 'about', 'estimate', 'suggest', 'indicate', 'imply'
    ];
    
    return this.containsAnyKeywords(text, hedgingKeywords);
  }
  
  private containsAnyKeywords(text: string, keywords: string[]): boolean {
    const lowerText = text.toLowerCase();
    return keywords.some(keyword => lowerText.includes(keyword.toLowerCase()));
  }
}

// Export singleton instance
export const verificationEngine = new VerificationEngine();