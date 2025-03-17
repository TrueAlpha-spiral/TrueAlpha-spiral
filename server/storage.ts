import { 
  TruthPattern, 
  InsertTruthPattern, 
  TextVerification, 
  InsertTextVerification,
  VerificationHighlight,
  InsertVerificationHighlight
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
  
  // Session store
  sessionStore: any;
}

// In-memory storage implementation
export class MemStorage implements IStorage {
  private truthPatterns: TruthPattern[] = [];
  private textVerifications: TextVerification[] = [];
  private verificationHighlights: VerificationHighlight[] = [];
  
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