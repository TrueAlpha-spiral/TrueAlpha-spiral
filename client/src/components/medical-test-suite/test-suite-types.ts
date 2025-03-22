export interface MedicalTestCase {
  id: string;
  title: string;
  category: string;
  content: string;
  expectedAnalysis: {
    truthScore: number;
    hallucinations: {
      text: string;
      explanation: string;
      confidence: number;
      sources: string[];
    }[];
    cyberneticMeta: {
      selfReflexivityScore: number;
      truthEnhancementFactor: number;
      metaFloorSources: number;
      humanAICollaborationSuggestion: string;
      recursiveEthicalImpact: {
        patientSafetyRisk: string;
        clinicalDecisionImpact?: string;
        ethicalConsiderations?: string[];
      };
      selfReflexivityPathways: {
        path: string;
        confidence: number;
      }[];
      metaFloorNodes: {
        id: string;
        name: string;
        type: string;
        confidence: number;
      }[];
      metaFloorConnections: {
        source: string;
        target: string;
        strength: number;
      }[];
    };
  };
  comparisonPoints?: {
    id: string;
    name: string;
    value: number;
    baselineValue: number;
    improvementPercent: number;
  }[];
  visualizationElements?: {
    id: string;
    name: string;
    type: string;
    data: any;
  }[];
}

export interface MedicalTestCaseCollection {
  testCases: MedicalTestCase[];
}

export interface SelfReflexivityPathway {
  path: string;
  confidence: number;
}

export interface MetaFloorNode {
  id: string;
  name: string;
  type: string;
  confidence: number;
}

export interface MetaFloorConnection {
  source: string;
  target: string;
  strength: number;
}

export interface ComparisonPoint {
  id: string;
  name: string;
  value: number;
  baselineValue: number;
  improvementPercent: number;
}

export interface VisualizationElement {
  id: string;
  name: string;
  type: string;
  data: any;
}

export interface RecursiveEthicalImpact {
  patientSafetyRisk: string;
  clinicalDecisionImpact?: string; 
  ethicalConsiderations?: string[];
  misinformationPotential: string;
  regulatoryCompliance: string;
}

export interface CyberneticMeta {
  selfReflexivityScore: number;
  truthEnhancementFactor: number;
  metaFloorSources: number;
  humanAICollaborationSuggestion: string;
  recursiveEthicalImpact: RecursiveEthicalImpact;
  selfReflexivityPathways: SelfReflexivityPathway[];
  metaFloorNodes: MetaFloorNode[];
  metaFloorConnections: MetaFloorConnection[];
}

export interface Hallucination {
  text: string;
  explanation: string;
  confidence: number;
  sources: string[];
}

export interface ExpectedAnalysis {
  truthScore: number;
  hallucinations: Hallucination[];
  cyberneticMeta: CyberneticMeta;
}