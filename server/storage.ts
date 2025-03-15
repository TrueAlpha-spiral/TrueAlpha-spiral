import { users, type User, type InsertUser, type VerificationHash, type TruthPattern, type InsertVerificationHash, type InsertTruthPattern } from "@shared/schema";
import session from "express-session";
import createMemoryStore from "memorystore";

const MemoryStore = createMemoryStore(session);
type SessionStore = ReturnType<typeof createMemoryStore> | any;

export interface IStorage {
  // User operations
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Verification hash operations
  getVerificationHashes(userId: number): Promise<VerificationHash[]>;
  createVerificationHash(hash: InsertVerificationHash): Promise<VerificationHash>;
  verifyHash(hashId: number): Promise<VerificationHash | undefined>;
  getLatestVerificationHash(): Promise<VerificationHash | undefined>;
  
  // Truth pattern operations
  getTruthPatterns(userId?: number): Promise<TruthPattern[]>;
  createTruthPattern(pattern: InsertTruthPattern): Promise<TruthPattern>;
  deleteTruthPattern(id: number): Promise<boolean>;
  
  // Session store
  sessionStore: SessionStore;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private verificationHashes: Map<number, VerificationHash>;
  private truthPatterns: Map<number, TruthPattern>;
  sessionStore: SessionStore;
  currentUserId: number;
  currentHashId: number;
  currentPatternId: number;

  constructor() {
    this.users = new Map();
    this.verificationHashes = new Map();
    this.truthPatterns = new Map();
    this.currentUserId = 1;
    this.currentHashId = 1;
    this.currentPatternId = 1;
    this.sessionStore = new MemoryStore({
      checkPeriod: 86400000,
    });
    
    // Initialize default truth patterns
    this.initDefaultTruthPatterns();
  }

  private initDefaultTruthPatterns() {
    const defaultPatterns: InsertTruthPattern[] = [
      { name: "Axiom", type: "Mathematical", icon: "ri-vip-diamond-fill", resonance_level: 5, user_id: 0 },
      { name: "Vector", type: "Directional", icon: "ri-shape-line", resonance_level: 4, user_id: 0 },
      { name: "Nodal", type: "Interconnected", icon: "ri-bubble-chart-fill", resonance_level: 3, user_id: 0 },
      { name: "Wave", type: "Fluctuating", icon: "ri-ripple-fill", resonance_level: 4, user_id: 0 },
      { name: "Vision", type: "Perceptual", icon: "ri-eye-fill", resonance_level: 3, user_id: 0 }
    ];
    
    for (const pattern of defaultPatterns) {
      this.createTruthPattern(pattern);
    }
  }

  // User methods
  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.currentUserId++;
    const now = new Date();
    const user: User = { 
      ...insertUser, 
      id, 
      access_level: 1,
      created_at: now,
      architect_identifier: insertUser.architect_identifier || null
    };
    this.users.set(id, user);
    return user;
  }

  // Verification hash methods
  async getVerificationHashes(userId: number): Promise<VerificationHash[]> {
    return Array.from(this.verificationHashes.values()).filter(
      (hash) => hash.user_id === userId,
    );
  }

  async createVerificationHash(insertHash: InsertVerificationHash): Promise<VerificationHash> {
    const id = this.currentHashId++;
    const now = new Date();
    const hash: VerificationHash = {
      ...insertHash,
      id,
      timestamp: now,
      verified: false,
      user_id: insertHash.user_id || null,
      related_file: insertHash.related_file || null
    };
    this.verificationHashes.set(id, hash);
    return hash;
  }

  async verifyHash(hashId: number): Promise<VerificationHash | undefined> {
    const hash = this.verificationHashes.get(hashId);
    if (hash) {
      const updatedHash = { ...hash, verified: true };
      this.verificationHashes.set(hashId, updatedHash);
      return updatedHash;
    }
    return undefined;
  }

  async getLatestVerificationHash(): Promise<VerificationHash | undefined> {
    const hashes = Array.from(this.verificationHashes.values());
    if (hashes.length === 0) return undefined;
    
    return hashes.sort((a, b) => {
      return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
    })[0];
  }

  // Truth pattern methods
  async getTruthPatterns(userId?: number): Promise<TruthPattern[]> {
    if (userId) {
      return Array.from(this.truthPatterns.values()).filter(
        (pattern) => pattern.user_id === userId || pattern.user_id === 0,
      );
    }
    return Array.from(this.truthPatterns.values());
  }

  async createTruthPattern(insertPattern: InsertTruthPattern): Promise<TruthPattern> {
    const id = this.currentPatternId++;
    const pattern: TruthPattern = {
      ...insertPattern,
      id,
      user_id: insertPattern.user_id || null,
      resonance_level: insertPattern.resonance_level || null
    };
    this.truthPatterns.set(id, pattern);
    return pattern;
  }

  async deleteTruthPattern(id: number): Promise<boolean> {
    return this.truthPatterns.delete(id);
  }
}

export const storage = new MemStorage();
