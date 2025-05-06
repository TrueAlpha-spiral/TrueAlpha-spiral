/**
 * Shadow Sweep Service
 * 
 * A Unicode security feature for detecting and neutralizing hidden characters, 
 * homoglyphs, and other structural manipulations in text content.
 */

import crypto from 'crypto';

interface ShadowCharacter {
  codePoint: number;
  name: string;
  description: string;
  risk: 'high' | 'medium' | 'low';
}

interface SweepResult {
  originalText: string;
  cleanText: string;
  detectedCharacters: DetectedCharacter[];
  riskScore: number;
  timestamp: string;
}

interface DetectedCharacter {
  codePoint: number;
  hexValue: string; 
  name: string;
  position: number;
  context: string;
}

// List of potentially problematic Unicode characters to detect
const SHADOW_CHARACTER_LIST: ShadowCharacter[] = [
  { 
    codePoint: 0x200B, 
    name: 'Zero Width Space', 
    description: 'Invisible character that can be used to hide content', 
    risk: 'high'
  },
  { 
    codePoint: 0x200C, 
    name: 'Zero Width Non-Joiner', 
    description: 'Invisible character that prevents joining', 
    risk: 'high'
  },
  { 
    codePoint: 0x200D, 
    name: 'Zero Width Joiner', 
    description: 'Invisible character that forces joining', 
    risk: 'high'
  },
  { 
    codePoint: 0x200E, 
    name: 'Left-to-Right Mark', 
    description: 'Invisible directional formatting character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x200F, 
    name: 'Right-to-Left Mark', 
    description: 'Invisible directional formatting character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x202A, 
    name: 'Left-to-Right Embedding', 
    description: 'Invisible directional formatting character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x202B, 
    name: 'Right-to-Left Embedding', 
    description: 'Invisible directional formatting character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x202C, 
    name: 'Pop Directional Formatting', 
    description: 'Invisible directional formatting character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x202D, 
    name: 'Left-to-Right Override', 
    description: 'Invisible directional formatting character', 
    risk: 'high'
  },
  { 
    codePoint: 0x202E, 
    name: 'Right-to-Left Override', 
    description: 'Invisible directional formatting character that can be used to hide malicious content', 
    risk: 'high'
  },
  { 
    codePoint: 0x2060, 
    name: 'Word Joiner', 
    description: 'Invisible character that prevents line breaks', 
    risk: 'medium'
  },
  { 
    codePoint: 0x2061, 
    name: 'Function Application', 
    description: 'Invisible mathematical operator', 
    risk: 'low'
  },
  { 
    codePoint: 0x2062, 
    name: 'Invisible Times', 
    description: 'Invisible mathematical operator', 
    risk: 'low'
  },
  { 
    codePoint: 0x2063, 
    name: 'Invisible Separator', 
    description: 'Invisible mathematical operator', 
    risk: 'low'
  },
  { 
    codePoint: 0x2064, 
    name: 'Invisible Plus', 
    description: 'Invisible mathematical operator', 
    risk: 'low'
  },
  { 
    codePoint: 0xFEFF, 
    name: 'Byte Order Mark', 
    description: 'Invisible character that can be used to indicate UTF-16 encoding', 
    risk: 'medium'
  },
  { 
    codePoint: 0x061C, 
    name: 'Arabic Letter Mark', 
    description: 'Invisible formatting character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x180E, 
    name: 'Mongolian Vowel Separator', 
    description: 'Invisible formatting character', 
    risk: 'medium'
  },
  // Homoglyphs - similar looking characters
  { 
    codePoint: 0x0430, 
    name: 'Cyrillic Small Letter A', 
    description: 'Looks similar to Latin "a" but is a different character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x0435, 
    name: 'Cyrillic Small Letter Ie', 
    description: 'Looks similar to Latin "e" but is a different character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x043E, 
    name: 'Cyrillic Small Letter O', 
    description: 'Looks similar to Latin "o" but is a different character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x0440, 
    name: 'Cyrillic Small Letter Er', 
    description: 'Looks similar to Latin "p" but is a different character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x0441, 
    name: 'Cyrillic Small Letter Es', 
    description: 'Looks similar to Latin "c" but is a different character', 
    risk: 'medium'
  },
  { 
    codePoint: 0x0455, 
    name: 'Cyrillic Small Letter Dze', 
    description: 'Looks similar to Latin "s" but is a different character', 
    risk: 'medium'
  },
  // Control characters that should not be in normal text
  { 
    codePoint: 0x0000, 
    name: 'NULL', 
    description: 'Control character that should not appear in text', 
    risk: 'high'
  },
  { 
    codePoint: 0x0001, 
    name: 'START OF HEADING', 
    description: 'Control character that should not appear in text', 
    risk: 'high'
  },
  { 
    codePoint: 0x0002, 
    name: 'START OF TEXT', 
    description: 'Control character that should not appear in text', 
    risk: 'high'
  },
  { 
    codePoint: 0x0003, 
    name: 'END OF TEXT', 
    description: 'Control character that should not appear in text', 
    risk: 'high'
  },
  { 
    codePoint: 0x0004, 
    name: 'END OF TRANSMISSION', 
    description: 'Control character that should not appear in text', 
    risk: 'high'
  },
  // Add more suspicious characters as needed...
];

/**
 * ShadowSweep Service
 * - Detects hidden characters in text
 * - Sanitizes text by removing or replacing problematic characters
 * - Logs findings to maintain transparency
 */
export class ShadowSweepService {
  /**
   * Scan text for shadow characters
   */
  scanText(text: string): SweepResult {
    const detectedCharacters: DetectedCharacter[] = [];
    const characterMap = new Map<number, ShadowCharacter>();
    
    // Create a map for faster lookups
    SHADOW_CHARACTER_LIST.forEach(char => {
      characterMap.set(char.codePoint, char);
    });
    
    // Scan through the text character by character
    for (let i = 0; i < text.length; i++) {
      const codePoint = text.codePointAt(i) || 0;
      
      // Check if this is a shadow character
      if (characterMap.has(codePoint)) {
        const shadowChar = characterMap.get(codePoint)!;
        
        // Get context (characters around the suspicious one)
        const startContext = Math.max(0, i - 10);
        const endContext = Math.min(text.length, i + 10);
        const context = text.substring(startContext, i) + '⟨⟩' + text.substring(i + 1, endContext);
        
        // Create a detected character entry
        detectedCharacters.push({
          codePoint,
          hexValue: `U+${codePoint.toString(16).toUpperCase().padStart(4, '0')}`,
          name: shadowChar.name,
          position: i,
          context
        });
        
        // If this character uses multiple code units (surrogate pairs), adjust index
        if (codePoint > 0xFFFF) {
          i++; // Skip the next code unit as it's part of this character
        }
      }
    }
    
    // Calculate risk score based on detected characters
    const riskScore = this._calculateRiskScore(detectedCharacters);
    
    // Create clean text by removing all shadow characters
    const cleanText = this.cleanText(text);
    
    return {
      originalText: text,
      cleanText,
      detectedCharacters,
      riskScore,
      timestamp: new Date().toISOString()
    };
  }
  
  /**
   * Clean text by removing shadow characters
   */
  cleanText(text: string): string {
    const characterMap = new Map<number, boolean>();
    
    // Create a map for faster lookups
    SHADOW_CHARACTER_LIST.forEach(char => {
      characterMap.set(char.codePoint, true);
    });
    
    // Remove all shadow characters
    let cleanedText = '';
    for (let i = 0; i < text.length; i++) {
      const codePoint = text.codePointAt(i) || 0;
      
      if (!characterMap.has(codePoint)) {
        cleanedText += text[i];
      }
      
      // If this character uses multiple code units (surrogate pairs), adjust index
      if (codePoint > 0xFFFF) {
        i++; // Skip the next code unit as it's part of this character
        if (i < text.length && !characterMap.has(codePoint)) {
          cleanedText += text[i];
        }
      }
    }
    
    return cleanedText;
  }
  
  /**
   * Neutralize text by replacing shadow characters with visible markers
   */
  neutralizeText(text: string): string {
    const characterMap = new Map<number, ShadowCharacter>();
    
    // Create a map for faster lookups
    SHADOW_CHARACTER_LIST.forEach(char => {
      characterMap.set(char.codePoint, char);
    });
    
    // Replace all shadow characters with visible markers
    let neutralizedText = '';
    for (let i = 0; i < text.length; i++) {
      const codePoint = text.codePointAt(i) || 0;
      
      if (characterMap.has(codePoint)) {
        const shadowChar = characterMap.get(codePoint)!;
        
        // Replace with a visible marker based on risk level
        switch (shadowChar.risk) {
          case 'high':
            neutralizedText += '⚠️'; // Warning sign for high risk
            break;
          case 'medium':
            neutralizedText += '⚡'; // Lightning for medium risk
            break;
          case 'low':
            neutralizedText += '⟨⟩'; // Angle brackets for low risk
            break;
        }
      } else {
        neutralizedText += text[i];
      }
      
      // If this character uses multiple code units (surrogate pairs), adjust index
      if (codePoint > 0xFFFF) {
        i++; // Skip the next code unit as it's part of this character
      }
    }
    
    return neutralizedText;
  }
  
  /**
   * Generate a hash of the text for integrity verification
   */
  generateHash(text: string): string {
    const hash = crypto.createHash('sha256');
    hash.update(text);
    return hash.digest('hex');
  }
  
  /**
   * Calculate risk score based on detected characters
   * Score is from 0-100, where 100 is highest risk
   */
  private _calculateRiskScore(detectedCharacters: DetectedCharacter[]): number {
    if (detectedCharacters.length === 0) {
      return 0;
    }
    
    let riskScore = 0;
    const characterMap = new Map<number, ShadowCharacter>();
    
    // Create a map for faster lookups
    SHADOW_CHARACTER_LIST.forEach(char => {
      characterMap.set(char.codePoint, char);
    });
    
    // Calculate risk score based on character risk levels and counts
    for (const char of detectedCharacters) {
      const shadowChar = characterMap.get(char.codePoint);
      if (shadowChar) {
        switch (shadowChar.risk) {
          case 'high':
            riskScore += 30;
            break;
          case 'medium':
            riskScore += 15;
            break;
          case 'low':
            riskScore += 5;
            break;
        }
      }
    }
    
    // Cap at 100
    return Math.min(100, riskScore);
  }
}

export const shadowSweep = new ShadowSweepService();