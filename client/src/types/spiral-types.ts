export interface TruthPattern {
  id: number;
  name: string;
  type: string;
  icon: string;
  resonance_level: number;
}

export interface VerificationHash {
  id: number;
  hash_value: string;
  timestamp: string;
  user_id: number;
  related_file: string | null;
  verified: boolean;
}

export interface DimensionalPlane {
  id: string;
  size: number;
  rotation: number;
  color: string;
  animationDelay: string;
}

export interface SecurityModule {
  name: string;
  status: 'ACTIVE' | 'INACTIVE';
  value: number;
}

export interface EigenchannelValue {
  name: string;
  value: number;
}

export interface SovereignEquationParams {
  truth: number;
  distance: number;
  size: number;
}

export type VerificationLayer = {
  name: string;
  verified: boolean;
};
