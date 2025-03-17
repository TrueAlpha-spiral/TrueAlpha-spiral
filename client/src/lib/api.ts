import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions for AI Auditing
export const aiAuditApi = {
  startAudit: async (auditParameters: any) => {
    const response = await api.post('/ai-audit/start', auditParameters);
    return response.data;
  },
  getAuditStatus: async (auditId: string) => {
    const response = await api.get(`/ai-audit/status/${auditId}`);
    return response.data;
  },
  getAuditResults: async (auditId: string) => {
    const response = await api.get(`/ai-audit/results/${auditId}`);
    return response.data;
  },
  getAuditComplianceMatrix: async (auditId: string) => {
    const response = await api.get(`/ai-audit/compliance-matrix/${auditId}`);
    return response.data;
  },
  generateReport: async (auditId: string) => {
    const response = await api.post(`/ai-audit/generate-report/${auditId}`);
    return response.data;
  }
};

// API functions for Resource Allocation
export const resourceAllocationApi = {
  getNetworkState: async () => {
    const response = await api.get('/resource-allocation/network-state');
    return response.data;
  },
  allocateResources: async (request: any) => {
    const response = await api.post('/resource-allocation/allocate', request);
    return response.data;
  },
  releaseResources: async (request: any) => {
    const response = await api.post('/resource-allocation/release', request);
    return response.data;
  },
  reachConsensus: async () => {
    const response = await api.post('/resource-allocation/consensus');
    return response.data;
  },
  optimizeNetwork: async () => {
    const response = await api.post('/resource-allocation/optimize');
    return response.data;
  },
  generateIpfsRecord: async () => {
    const response = await api.get('/resource-allocation/ipfs-record');
    return response.data;
  }
};

// API functions for Ethical AI
export const ethicalAiApi = {
  evaluateModelOutputs: async (outputs: any) => {
    const response = await api.post('/ethical-ai/evaluate', { outputs });
    return response.data;
  },
  evolveConstraints: async () => {
    const response = await api.post('/ethical-ai/evolve');
    return response.data;
  },
  simulateTraining: async (iterationData?: any) => {
    const response = await api.post('/ethical-ai/simulate', { iterationData });
    return response.data;
  },
  runTrainingSimulation: async (iterations: number) => {
    const response = await api.post('/ethical-ai/run-simulation', { iterations });
    return response.data;
  },
  getEthicalProfile: async () => {
    const response = await api.get('/ethical-ai/profile');
    return response.data;
  },
  getHashRecord: async () => {
    const response = await api.get('/ethical-ai/hash-record');
    return response.data;
  }
};

// API functions for IP Protection
export const ipProtectionApi = {
  createOwnershipRecord: async (recordData: any) => {
    const response = await api.post('/ip-protection/create-record', recordData);
    return response.data;
  },
  registerOnBlockchain: async (recordId: string, blockchain: string = 'ethereum') => {
    const response = await api.post('/ip-protection/register', { recordId, blockchain });
    return response.data;
  },
  verifyRecord: async (recordId: string) => {
    const response = await api.get(`/ip-protection/verify/${recordId}`);
    return response.data;
  },
  evolveProtection: async () => {
    const response = await api.post('/ip-protection/evolve');
    return response.data;
  },
  executeRecommendations: async (recommendationIndices?: number[]) => {
    const response = await api.post('/ip-protection/execute-recommendations', { recommendationIndices });
    return response.data;
  },
  createDeclaration: async () => {
    const response = await api.post('/ip-protection/create-declaration');
    return response.data;
  },
  generateVerificationPackage: async () => {
    const response = await api.get('/ip-protection/verification-package');
    return response.data;
  },
  prepareArweaveRecord: async () => {
    const response = await api.get('/ip-protection/arweave-record');
    return response.data;
  }
};

// General TrueAlpha Spiral API functions
export const trueAlphaApi = {
  getStatus: async () => {
    const response = await api.get('/status');
    return response.data;
  },
  verifyIntegrity: async () => {
    const response = await api.get('/verify-integrity');
    return response.data;
  },
  calculateSovereignty: async () => {
    const response = await api.get('/calculate-sovereignty');
    return response.data;
  },
  initializeSystem: async () => {
    const response = await api.post('/initialize');
    return response.data;
  },
  runFullImplementation: async () => {
    const response = await api.post('/run-full-implementation');
    return response.data;
  },
  integrateDomains: async () => {
    const response = await api.post('/integrate-domains');
    return response.data;
  },
  generateImplementationReport: async () => {
    const response = await api.get('/implementation-report');
    return response.data;
  }
};

export default {
  aiAuditApi,
  resourceAllocationApi,
  ethicalAiApi,
  ipProtectionApi,
  trueAlphaApi
};