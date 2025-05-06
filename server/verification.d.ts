export function verifyIntent(intentStatement: string): {
  verified: boolean;
  resonance: number;
  intentHash?: string;
};

export function verifyIdentity(request: {
  userId?: string;
  timestamp: string;
  intentHash?: string;
}): Promise<{
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
}>;

export function getResonanceValue(userId?: string): number;
