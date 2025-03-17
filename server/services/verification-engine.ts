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
    
    console.log("[DEBUG] Verifying text:", text);
    console.log("[DEBUG] Is question?", this.isQuestion(text));
    
    // First, check if this is a question or against known facts database
    // This applies to the entire text, not individual sentences
    const factCheck = this.checkAgainstKnownFacts(text);
    console.log("[DEBUG] factCheck result:", factCheck);
    
    if (factCheck) {
      console.log("[DEBUG] Using factCheck result with confidence:", factCheck.confidence);
      // We have a direct factual/speculative/fabricated determination
      const result: VerificationResult = {
        originalText: text,
        truthScore: factCheck.confidence,
        overallScore: factCheck.confidence,
        highlights: [{
          startIndex: 0,
          endIndex: text.length,
          type: factCheck.type,
          confidenceScore: factCheck.confidence,
          message: factCheck.message,
          patternName: factCheck.pattern.name
        }],
        processingTimeMs: Date.now() - startTime,
        summary: {
          factualCount: factCheck.type === 'factual' ? 1 : 0,
          speculativeCount: factCheck.type === 'speculative' ? 1 : 0,
          fabricatedCount: factCheck.type === 'fabricated' ? 1 : 0,
          totalSentences: 1
        }
      };
      
      return result;
    }
    
    // If not a known fact/question, proceed with normal pattern analysis
    
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
      
      // Check if this individual sentence is a question
      if (this.isQuestion(sentenceText)) {
        speculativeCount++;
        highlights.push({
          startIndex: index,
          endIndex: index + sentenceText.length,
          type: 'speculative',
          confidenceScore: 0.5,
          message: 'This is a question, not a factual statement.',
          patternName: 'Question Detection'
        });
        totalConfidence += 0.5;
        continue;
      }
      
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
    // We've already checked against known facts and questions in verifyText
    // so we don't need to do it here again
    
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
   * Checks text against a database of known facts
   */
  private checkAgainstKnownFacts(text: string): { pattern: TruthPattern; confidence: number; type: 'factual' | 'speculative' | 'fabricated'; message: string; } | null {
    // First, handle questions or speculative statements
    if (this.isQuestion(text)) {
      return {
        pattern: {
          id: 998, // Special ID for question handling
          name: "Question Detection",
          description: "Identifies questions that cannot be verified as fact",
          category: "Language",
          confidenceThreshold: 0.9,
          isActive: true,
          createdAt: new Date(),
          updatedAt: new Date()
        },
        confidence: 0.5, // Mid-range confidence (questions aren't factual or false)
        type: 'speculative',
        message: "This is a question, not a factual statement."
      };
    }

    // Basic fact database - in production this would connect to a real database or API
    const knownFalsehoods = [
      {
        pattern: /Elon Musk is the president/i,
        message: "Elon Musk is not the president of the United States."
      },
      {
        pattern: /\b(?:earth|world) is flat\b/i,
        message: "The Earth is not flat; it is an oblate spheroid."
      },
      {
        pattern: /\bhumans never (?:landed|went) (?:on|to) the moon\b/i,
        message: "Humans have landed on the moon; the first moon landing was in 1969."
      },
      {
        pattern: /\bvaccines cause autism\b/i,
        message: "Scientific consensus shows no link between vaccines and autism."
      },
      {
        pattern: /\bclimate change is (?:a hoax|not real|fake)\b/i,
        message: "Climate change is supported by scientific consensus."
      },
      // Add statements about current political figures and celebrities
      {
        pattern: /\b(?:Joe Biden|President Biden) is dead\b/i,
        message: "As of March 2025, Joe Biden is alive and serving as President of the United States."
      },
      {
        pattern: /\bDonald Trump is (?:the president|president)\b/i,
        message: "As of March 2025, Donald Trump is not the current president of the United States."
      },
      {
        pattern: /\bQueen Elizabeth is alive\b/i,
        message: "Queen Elizabeth II passed away on September 8, 2022."
      }
    ];
    
    // Check for falsehoods
    for (const falsehood of knownFalsehoods) {
      if (falsehood.pattern.test(text)) {
        return {
          pattern: {
            id: 999, // Special ID for fact checking
            name: "Fact Checking",
            description: "Verifies statements against known facts",
            category: "Data",
            confidenceThreshold: 0.9,
            isActive: true,
            createdAt: new Date(),
            updatedAt: new Date()
          },
          confidence: 0.1, // Very low confidence (high certainty of being false)
          type: 'fabricated',
          message: falsehood.message
        };
      }
    }
    
    return null;
  }
  
  /**
   * Detects if a text is a question
   */
  private isQuestion(text: string): boolean {
    // Check for question marks
    if (text.includes('?')) return true;
    
    // Check for common question starters
    const questionStarters = [
      /^(?:who|what|where|when|why|how|is|are|was|were|will|would|should|could|can|do|does|did|has|have|had)\b/i
    ];
    
    return questionStarters.some(pattern => pattern.test(text.trim()));
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