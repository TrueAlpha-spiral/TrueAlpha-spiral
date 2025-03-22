import { 
  TruthPattern, 
  InsertTruthPattern, 
  TextVerification, 
  InsertTextVerification,
  VerificationHighlight,
  InsertVerificationHighlight,
  AIAudit,
  InsertAIAudit,
  SharedTruthPattern,
  InsertSharedTruthPattern
} from '@shared/schema';
import session from 'express-session';
import createMemoryStore from 'memorystore';

const MemoryStore = createMemoryStore(session);

// Storage interface
export interface IStorage {
  // Truth patterns
  createTruthPattern(data: InsertTruthPattern): Promise<TruthPattern>;
  getTruthPatterns(): Promise<TruthPattern[]>;
  getTruthPattern(id: number): Promise<TruthPattern | null>;
  updateTruthPattern(id: number, data: Partial<InsertTruthPattern>): Promise<TruthPattern | null>;
  deleteTruthPattern(id: number): Promise<boolean>;
  
  // Text verifications
  createTextVerification(data: InsertTextVerification): Promise<TextVerification>;
  getTextVerifications(): Promise<TextVerification[]>;
  getTextVerification(id: number): Promise<TextVerification | null>;
  
  // Verification highlights
  createVerificationHighlight(data: InsertVerificationHighlight): Promise<VerificationHighlight>;
  getVerificationHighlightsByVerificationId(verificationId: number): Promise<VerificationHighlight[]>;
  
  // AI Audits
  createAIAudit(data: InsertAIAudit): Promise<AIAudit>;
  getAIAudits(): Promise<AIAudit[]>;
  getAIAudit(id: number): Promise<AIAudit | null>;
  updateAIAudit(id: number, data: Partial<InsertAIAudit>): Promise<AIAudit | null>;
  
  // Shared Truth Patterns
  createSharedTruthPattern(data: InsertSharedTruthPattern): Promise<SharedTruthPattern>;
  getSharedTruthPatterns(): Promise<SharedTruthPattern[]>;
  getSharedTruthPattern(id: number): Promise<SharedTruthPattern | null>;
  getSharedTruthPatternByLink(sharingLink: string): Promise<SharedTruthPattern | null>;
  getSharedTruthPatternsByPermission(permission: string): Promise<SharedTruthPattern[]>;
  updateSharedTruthPattern(id: number, data: Partial<InsertSharedTruthPattern>): Promise<SharedTruthPattern | null>;
  deleteSharedTruthPattern(id: number): Promise<boolean>;
  incrementSharedPatternUsageCount(id: number): Promise<SharedTruthPattern | null>;
  importSharedTruthPattern(sharedPattern: SharedTruthPattern): Promise<TruthPattern>;
  
  // Session store
  sessionStore: any;
}

// In-memory storage implementation
export class MemStorage implements IStorage {
  private truthPatterns: TruthPattern[] = [];
  private textVerifications: TextVerification[] = [];
  private verificationHighlights: VerificationHighlight[] = [];
  private aiAudits: AIAudit[] = [];
  private sharedTruthPatterns: SharedTruthPattern[] = [];
  
  public sessionStore: any;
  
  constructor() {
    // Initialize with seed data
    this.seedTruthPatterns();
    
    this.sessionStore = new MemoryStore({
      checkPeriod: 86400000 // prune expired entries every 24h
    });
  }
  
  // Truth pattern methods
  async createTruthPattern(data: InsertTruthPattern): Promise<TruthPattern> {
    const id = this.truthPatterns.length > 0 
      ? Math.max(...this.truthPatterns.map(p => p.id)) + 1 
      : 1;
    
    // Ensure all required fields have values
    const newPattern: TruthPattern = {
      id,
      name: data.name,
      description: data.description,
      category: data.category,
      confidenceThreshold: data.confidenceThreshold ?? 0.75,
      isActive: data.isActive ?? true,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    this.truthPatterns.push(newPattern);
    return newPattern;
  }
  
  async getTruthPatterns(): Promise<TruthPattern[]> {
    return [...this.truthPatterns];
  }
  
  async getTruthPattern(id: number): Promise<TruthPattern | null> {
    return this.truthPatterns.find(p => p.id === id) || null;
  }
  
  async updateTruthPattern(id: number, data: Partial<InsertTruthPattern>): Promise<TruthPattern | null> {
    const index = this.truthPatterns.findIndex(p => p.id === id);
    if (index === -1) return null;
    
    const updatedPattern = {
      ...this.truthPatterns[index],
      ...data
    };
    
    this.truthPatterns[index] = updatedPattern;
    return updatedPattern;
  }
  
  async deleteTruthPattern(id: number): Promise<boolean> {
    const initialLength = this.truthPatterns.length;
    this.truthPatterns = this.truthPatterns.filter(p => p.id !== id);
    return initialLength > this.truthPatterns.length;
  }
  
  // Text verification methods
  async createTextVerification(data: InsertTextVerification): Promise<TextVerification> {
    const id = this.textVerifications.length > 0 
      ? Math.max(...this.textVerifications.map(v => v.id)) + 1 
      : 1;
    
    const newVerification: TextVerification = {
      id,
      ...data,
      createdAt: new Date()
    };
    
    this.textVerifications.push(newVerification);
    return newVerification;
  }
  
  async getTextVerifications(): Promise<TextVerification[]> {
    return [...this.textVerifications];
  }
  
  async getTextVerification(id: number): Promise<TextVerification | null> {
    return this.textVerifications.find(v => v.id === id) || null;
  }
  
  // Verification highlight methods
  async createVerificationHighlight(data: InsertVerificationHighlight): Promise<VerificationHighlight> {
    const id = this.verificationHighlights.length > 0 
      ? Math.max(...this.verificationHighlights.map(h => h.id)) + 1 
      : 1;
    
    // Ensure all required fields have values
    const newHighlight: VerificationHighlight = {
      id,
      verificationId: data.verificationId,
      startIndex: data.startIndex,
      endIndex: data.endIndex,
      highlightType: data.highlightType,
      confidenceScore: data.confidenceScore,
      patternId: data.patternId ?? null,
      message: data.message ?? null,
      createdAt: new Date()
    };
    
    this.verificationHighlights.push(newHighlight);
    return newHighlight;
  }
  
  async getVerificationHighlightsByVerificationId(verificationId: number): Promise<VerificationHighlight[]> {
    return this.verificationHighlights.filter(h => h.verificationId === verificationId);
  }
  
  // AI Audit methods
  async createAIAudit(data: InsertAIAudit): Promise<AIAudit> {
    const id = this.aiAudits.length > 0 
      ? Math.max(...this.aiAudits.map(a => a.id)) + 1 
      : 1;
    
    // Ensure all required fields have values
    const newAudit: AIAudit = {
      id,
      clientName: data.clientName,
      aiSystemName: data.aiSystemName,
      regulatoryFramework: data.regulatoryFramework ?? 'general',
      status: data.status ?? 'initialized',
      auditSummary: data.auditSummary ?? null,
      riskScore: data.riskScore ?? null,
      complianceScore: data.complianceScore ?? null,
      verificationId: data.verificationId ?? null,
      blockchainRecord: data.blockchainRecord ?? null,
      auditReport: data.auditReport ?? null,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    this.aiAudits.push(newAudit);
    return newAudit;
  }
  
  async getAIAudits(): Promise<AIAudit[]> {
    return [...this.aiAudits];
  }
  
  async getAIAudit(id: number): Promise<AIAudit | null> {
    return this.aiAudits.find(a => a.id === id) || null;
  }
  
  async updateAIAudit(id: number, data: Partial<InsertAIAudit>): Promise<AIAudit | null> {
    const index = this.aiAudits.findIndex(a => a.id === id);
    if (index === -1) return null;
    
    const updatedAudit = {
      ...this.aiAudits[index],
      ...data,
      updatedAt: new Date()
    };
    
    this.aiAudits[index] = updatedAudit;
    return updatedAudit;
  }
  

  
  // Shared Truth Pattern methods
  async createSharedTruthPattern(data: InsertSharedTruthPattern): Promise<SharedTruthPattern> {
    const id = this.sharedTruthPatterns.length > 0 
      ? Math.max(...this.sharedTruthPatterns.map(p => p.id)) + 1 
      : 1;
    
    // Generate a unique sharing link
    const sharingLink = this.generateSharingLink();
    
    // Generate verification hash
    const verificationHash = this.generateVerificationHash(data);
    
    // Ensure all required fields have values
    const newSharedPattern: SharedTruthPattern = {
      id,
      originalPatternId: data.originalPatternId,
      name: data.name,
      description: data.description,
      category: data.category,
      sharingPermission: data.sharingPermission ?? 'private',
      authorName: data.authorName,
      authorOrganization: data.authorOrganization ?? null,
      authorEmail: data.authorEmail ?? null,
      sharingLink,
      allowedUserEmails: data.allowedUserEmails ?? [],
      patternData: data.patternData,
      usageCount: 0,
      verificationHash,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    this.sharedTruthPatterns.push(newSharedPattern);
    return newSharedPattern;
  }
  
  async getSharedTruthPatterns(): Promise<SharedTruthPattern[]> {
    return [...this.sharedTruthPatterns];
  }
  
  async getSharedTruthPattern(id: number): Promise<SharedTruthPattern | null> {
    return this.sharedTruthPatterns.find(p => p.id === id) || null;
  }
  
  async getSharedTruthPatternByLink(sharingLink: string): Promise<SharedTruthPattern | null> {
    return this.sharedTruthPatterns.find(p => p.sharingLink === sharingLink) || null;
  }
  
  async getSharedTruthPatternsByPermission(permission: string): Promise<SharedTruthPattern[]> {
    return this.sharedTruthPatterns.filter(p => p.sharingPermission === permission);
  }
  
  async updateSharedTruthPattern(id: number, data: Partial<InsertSharedTruthPattern>): Promise<SharedTruthPattern | null> {
    const index = this.sharedTruthPatterns.findIndex(p => p.id === id);
    if (index === -1) return null;
    
    const updatedPattern = {
      ...this.sharedTruthPatterns[index],
      ...data,
      updatedAt: new Date()
    };
    
    this.sharedTruthPatterns[index] = updatedPattern;
    return updatedPattern;
  }
  
  async deleteSharedTruthPattern(id: number): Promise<boolean> {
    const initialLength = this.sharedTruthPatterns.length;
    this.sharedTruthPatterns = this.sharedTruthPatterns.filter(p => p.id !== id);
    return initialLength > this.sharedTruthPatterns.length;
  }
  
  async incrementSharedPatternUsageCount(id: number): Promise<SharedTruthPattern | null> {
    const pattern = await this.getSharedTruthPattern(id);
    if (!pattern) return null;
    
    return this.updateSharedTruthPattern(id, {
      usageCount: pattern.usageCount + 1
    });
  }
  
  async importSharedTruthPattern(sharedPattern: SharedTruthPattern): Promise<TruthPattern> {
    // Check if pattern already exists
    const existingPattern = this.truthPatterns.find(p => 
      p.name === sharedPattern.name && 
      p.description === sharedPattern.description
    );
    
    if (existingPattern) {
      return existingPattern;
    }
    
    // Create a new truth pattern from the shared pattern
    return this.createTruthPattern({
      name: sharedPattern.name,
      description: sharedPattern.description,
      category: sharedPattern.category,
      confidenceThreshold: 0.75, // Default value
      isActive: true
    });
  }
  
  // Helper methods for shared patterns
  private generateSharingLink(): string {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = 'share-';
    for (let i = 0; i < 10; i++) {
      result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
  }
  
  private generateVerificationHash(data: InsertSharedTruthPattern): string {
    // In a real implementation, we would use a secure hashing algorithm
    // For now, we'll just concatenate some fields and create a simple hash
    const hashInput = `${data.originalPatternId}-${data.name}-${new Date().getTime()}`;
    let hash = 0;
    for (let i = 0; i < hashInput.length; i++) {
      const char = hashInput.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return 'vh-' + Math.abs(hash).toString(16);
  }
  
  // Initialize with seed data
  private seedTruthPatterns() {
    const seedPatterns: InsertTruthPattern[] = [
      {
        name: "Implementation Claims",
        description: "Detects claims about implementation details that may be speculative or fabricated.",
        category: "Technical",
        confidenceThreshold: 0.85,
        isActive: true
      },
      {
        name: "Metrics & Statistics",
        description: "Identifies metrics and statistics that lack proper citation or verification.",
        category: "Data",
        confidenceThreshold: 0.9,
        isActive: true
      },
      {
        name: "Case Study Detection",
        description: "Identifies case studies or examples that may be fabricated or unverified.",
        category: "Business",
        confidenceThreshold: 0.8,
        isActive: true
      },
      {
        name: "Speculative Future Claims",
        description: "Detects claims about future outcomes or results without proper qualification.",
        category: "Predictions",
        confidenceThreshold: 0.75,
        isActive: true
      },
      {
        name: "Hedging Language",
        description: "Identifies language patterns that indicate uncertainty or speculation.",
        category: "Language",
        confidenceThreshold: 0.7,
        isActive: true
      }
    ];
    
    seedPatterns.forEach((pattern, index) => {
      this.truthPatterns.push({
        id: index + 1,
        name: pattern.name,
        description: pattern.description,
        category: pattern.category,
        confidenceThreshold: pattern.confidenceThreshold ?? 0.75,
        isActive: pattern.isActive ?? true,
        createdAt: new Date(),
        updatedAt: new Date()
      });
    });
  }
}

// Export a singleton instance
export const storage = new MemStorage();