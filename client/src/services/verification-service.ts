import { apiRequest } from '@/lib/queryClient';
import { type VerificationResult, type TextVerification } from '@shared/schema';

export async function verifyText(text: string): Promise<VerificationResult> {
  try {
    const response = await apiRequest('POST', '/api/verify', { text });
    return await response.json();
  } catch (error) {
    console.error('Error verifying text:', error);
    throw error;
  }
}

export async function getVerificationHistory(): Promise<TextVerification[]> {
  try {
    const response = await apiRequest('GET', '/api/verifications');
    return await response.json();
  } catch (error) {
    console.error('Error getting verification history:', error);
    throw error;
  }
}

export async function getVerificationById(id: number): Promise<VerificationResult> {
  try {
    const response = await apiRequest('GET', `/api/verifications/${id}`);
    return await response.json();
  } catch (error) {
    console.error('Error getting verification:', error);
    throw error;
  }
}