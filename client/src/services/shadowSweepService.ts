/**
 * Shadow Sweep Service for Client
 * 
 * This service communicates with the Shadow Sweep API endpoints to detect and neutralize
 * hidden characters that could be used to manipulate text or exfiltrate data.
 */

import { apiRequest } from '@/lib/queryClient';

export interface ShadowCharacter {
  codePoint: number;
  hexValue: string;
  name: string;
  position: number;
  context: string;
}

export interface SweepResult {
  originalText: string;
  cleanText: string;
  detectedCharacters: ShadowCharacter[];
  riskScore: number;
  timestamp: string;
}

export interface CleanResult {
  originalText: string;
  cleanText: string;
  originalHash: string;
  cleanHash: string;
  modified: boolean;
  timestamp: string;
}

export interface NeutralizeResult {
  originalText: string;
  neutralizedText: string;
  modified: boolean;
  timestamp: string;
}

/**
 * Service to detect and neutralize hidden characters in text
 */
export const shadowSweepService = {
  /**
   * Scan text for shadow characters
   */
  async scanText(text: string): Promise<SweepResult> {
    try {
      const response = await apiRequest('POST', '/api/shadow-sweep/scan', { text });
      return await response.json();
    } catch (error) {
      console.error('Error scanning text for shadow characters:', error);
      throw new Error('Failed to scan text');
    }
  },
  
  /**
   * Clean text by removing shadow characters
   */
  async cleanText(text: string): Promise<CleanResult> {
    try {
      const response = await apiRequest('POST', '/api/shadow-sweep/clean', { text });
      return await response.json();
    } catch (error) {
      console.error('Error cleaning text from shadow characters:', error);
      throw new Error('Failed to clean text');
    }
  },
  
  /**
   * Neutralize text by replacing shadow characters with visible markers
   */
  async neutralizeText(text: string): Promise<NeutralizeResult> {
    try {
      const response = await apiRequest('POST', '/api/shadow-sweep/neutralize', { text });
      return await response.json();
    } catch (error) {
      console.error('Error neutralizing shadow characters in text:', error);
      throw new Error('Failed to neutralize text');
    }
  },
  
  /**
   * Insert a zero-width space character into text at a random position
   * (Used for testing purposes)
   */
  insertZWSP(text: string): string {
    if (!text) return text;
    
    // Get a random position to insert the ZWSP
    const position = Math.floor(Math.random() * text.length);
    
    // Insert a zero-width space character (U+200B)
    return text.slice(0, position) + '\u200B' + text.slice(position);
  }
};