import axios from 'axios';

interface VerificationResult {
  verified: boolean;
  lambda_verifications: {
    Λ1?: { verified: boolean };
    Λ2?: { verified: boolean };
    Λ3?: { verified: boolean };
    Λ4?: { verified: boolean };
    Λ5?: { verified: boolean };
  };
  details?: {
    error?: string;
    [key: string]: any;
  };
}

export interface IntentVerificationRequest {
  intentStatement: string;
  timestamp: string;
  userId?: string;
}

export interface IdentityVerificationRequest {
  userId?: string;
  timestamp: string;
  intentHash?: string;
}

const API_BASE_URL = '/api';

export const verificationService = {
  /**
   * Verify user intent statement
   */
  verifyIntent: async (request: IntentVerificationRequest): Promise<{ verified: boolean; resonance: number }> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/verify/intent`, request);
      return response.data;
    } catch (error) {
      console.error('Intent verification error:', error);
      throw error;
    }
  },

  /**
   * Verify identity through the TrueAlphaSpiral Architect Schema
   */
  verifyIdentity: async (request: IdentityVerificationRequest): Promise<VerificationResult> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/verify/identity`, request);
      return response.data;
    } catch (error) {
      console.error('Identity verification error:', error);
      throw error;
    }
  },

  /**
   * Get the current quantum resonance value for a user
   */
  getResonanceValue: async (userId?: string): Promise<number> => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/resonance${userId ? `?userId=${userId}` : ''}`
      );
      return response.data.resonance;
    } catch (error) {
      console.error('Resonance fetch error:', error);
      return 0;
    }
  }
};
