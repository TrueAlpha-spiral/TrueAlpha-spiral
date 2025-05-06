import { apiRequest } from "@/lib/queryClient";

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

export const shadowSweepService = {
  /**
   * Scan text for shadow characters
   */
  async scanText(text: string): Promise<SweepResult> {
    const response = await apiRequest("POST", "/api/shadow-sweep/scan", { text });
    const data = await response.json();
    return data;
  },

  /**
   * Clean text by removing shadow characters
   */
  async cleanText(text: string): Promise<CleanResult> {
    const response = await apiRequest("POST", "/api/shadow-sweep/clean", { text });
    const data = await response.json();
    return data;
  },

  /**
   * Neutralize text by replacing shadow characters with visible markers
   */
  async neutralizeText(text: string): Promise<NeutralizeResult> {
    const response = await apiRequest("POST", "/api/shadow-sweep/neutralize", { text });
    const data = await response.json();
    return data;
  }
};