import { 
  users, type User, type InsertUser,
  verificationVectors, type VerificationVector, type InsertVerificationVector,
  challengeRecords, type ChallengeRecord, type InsertChallengeRecord,
  verificationHashes, type VerificationHash, type InsertVerificationHash,
  dashboardMetrics, type DashboardMetric, type InsertDashboardMetric,
  sovereigntyBadges, type SovereigntyBadge, type InsertSovereigntyBadge
} from "@shared/schema";
import { db } from "./db";
import { eq } from "drizzle-orm";
import crypto from 'crypto';

// Interface for storage operations
export interface IStorage {
  // User operations
  getUser(id: string): Promise<User | undefined>;
  upsertUser(user: InsertUser): Promise<User>;
  
  // Verification vector operations
  getAllVerificationVectors(): Promise<VerificationVector[]>;
  getVerificationVector(id: number): Promise<VerificationVector | undefined>;
  createVerificationVector(vector: InsertVerificationVector): Promise<VerificationVector>;
  updateVerificationVector(id: number, vector: Partial<InsertVerificationVector>): Promise<VerificationVector | undefined>;
  
  // Challenge record operations
  getAllChallengeRecords(): Promise<ChallengeRecord[]>;
  getChallengeRecord(id: number): Promise<ChallengeRecord | undefined>;
  createChallengeRecord(record: InsertChallengeRecord): Promise<ChallengeRecord>;
  updateChallengeRecord(id: number, record: Partial<InsertChallengeRecord>): Promise<ChallengeRecord | undefined>;
  
  // Verification hash operations
  getAllVerificationHashes(): Promise<VerificationHash[]>;
  createVerificationHash(hash: InsertVerificationHash): Promise<VerificationHash>;
  verifyDocumentHash(documentType: string, content: string): Promise<boolean>;
  
  // Dashboard metric operations
  getAllDashboardMetrics(): Promise<DashboardMetric[]>;
  updateDashboardMetric(id: number, metric: Partial<InsertDashboardMetric>): Promise<DashboardMetric | undefined>;
  createOrUpdateMetric(metricName: string, metricValue: string, metricType: string): Promise<DashboardMetric>;
  
  // Sovereignty badge operations
  getAllSovereigntyBadges(): Promise<SovereigntyBadge[]>;
  getSovereigntyBadge(id: number): Promise<SovereigntyBadge | undefined>;
  createSovereigntyBadge(badge: InsertSovereigntyBadge): Promise<SovereigntyBadge>;
}

export class DatabaseStorage implements IStorage {
  // User operations
  async getUser(id: string): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user;
  }

  async upsertUser(userData: InsertUser): Promise<User> {
    const [user] = await db
      .insert(users)
      .values(userData)
      .onConflictDoUpdate({
        target: users.id,
        set: {
          ...userData,
          updatedAt: new Date(),
        },
      })
      .returning();
    return user;
  }
  
  // Verification vector operations
  async getAllVerificationVectors(): Promise<VerificationVector[]> {
    return await db.select().from(verificationVectors);
  }
  
  async getVerificationVector(id: number): Promise<VerificationVector | undefined> {
    const [vector] = await db.select().from(verificationVectors).where(eq(verificationVectors.id, id));
    return vector;
  }
  
  async createVerificationVector(vector: InsertVerificationVector): Promise<VerificationVector> {
    const [newVector] = await db.insert(verificationVectors).values(vector).returning();
    return newVector;
  }
  
  async updateVerificationVector(id: number, vector: Partial<InsertVerificationVector>): Promise<VerificationVector | undefined> {
    const [updatedVector] = await db
      .update(verificationVectors)
      .set({
        ...vector,
        updatedAt: new Date(),
      })
      .where(eq(verificationVectors.id, id))
      .returning();
    
    return updatedVector;
  }
  
  // Challenge record operations
  async getAllChallengeRecords(): Promise<ChallengeRecord[]> {
    return await db.select().from(challengeRecords);
  }
  
  async getChallengeRecord(id: number): Promise<ChallengeRecord | undefined> {
    const [record] = await db.select().from(challengeRecords).where(eq(challengeRecords.id, id));
    return record;
  }
  
  async createChallengeRecord(record: InsertChallengeRecord): Promise<ChallengeRecord> {
    const [newRecord] = await db.insert(challengeRecords).values(record).returning();
    return newRecord;
  }
  
  async updateChallengeRecord(id: number, record: Partial<InsertChallengeRecord>): Promise<ChallengeRecord | undefined> {
    const [updatedRecord] = await db
      .update(challengeRecords)
      .set({
        ...record,
        updatedAt: new Date(),
      })
      .where(eq(challengeRecords.id, id))
      .returning();
    
    return updatedRecord;
  }
  
  // Verification hash operations
  async getAllVerificationHashes(): Promise<VerificationHash[]> {
    return await db.select().from(verificationHashes);
  }
  
  async createVerificationHash(hash: InsertVerificationHash): Promise<VerificationHash> {
    const [newHash] = await db.insert(verificationHashes).values(hash).returning();
    return newHash;
  }
  
  async verifyDocumentHash(documentType: string, content: string): Promise<boolean> {
    // Calculate hash of the provided content
    const calculatedHash = crypto.createHash('sha256').update(content).digest('hex');
    
    // Find the stored hash for this document type
    const [storedHashRecord] = await db
      .select()
      .from(verificationHashes)
      .where(eq(verificationHashes.documentType, documentType));
    
    if (!storedHashRecord) {
      return false;
    }
    
    // Compare the hashes
    return calculatedHash === storedHashRecord.hashValue;
  }
  
  // Dashboard metric operations
  async getAllDashboardMetrics(): Promise<DashboardMetric[]> {
    return await db.select().from(dashboardMetrics);
  }
  
  async updateDashboardMetric(id: number, metric: Partial<InsertDashboardMetric>): Promise<DashboardMetric | undefined> {
    const [updatedMetric] = await db
      .update(dashboardMetrics)
      .set({
        ...metric,
        updatedAt: new Date(),
      })
      .where(eq(dashboardMetrics.id, id))
      .returning();
    
    return updatedMetric;
  }
  
  async createOrUpdateMetric(metricName: string, metricValue: string, metricType: string): Promise<DashboardMetric> {
    // Check if metric exists
    const [existingMetric] = await db
      .select()
      .from(dashboardMetrics)
      .where(eq(dashboardMetrics.metricName, metricName));
    
    if (existingMetric) {
      // Update existing metric
      const [updatedMetric] = await db
        .update(dashboardMetrics)
        .set({
          metricValue,
          updatedAt: new Date(),
        })
        .where(eq(dashboardMetrics.id, existingMetric.id))
        .returning();
      
      return updatedMetric;
    } else {
      // Create new metric
      const [newMetric] = await db
        .insert(dashboardMetrics)
        .values({
          metricName,
          metricValue,
          metricType,
          displayOrder: 1, // Default display order, will be updated by system
        })
        .returning();
      
      return newMetric;
    }
  }
  
  // Sovereignty badge operations
  async getAllSovereigntyBadges(): Promise<SovereigntyBadge[]> {
    return await db.select().from(sovereigntyBadges);
  }
  
  async getSovereigntyBadge(id: number): Promise<SovereigntyBadge | undefined> {
    const [badge] = await db.select().from(sovereigntyBadges).where(eq(sovereigntyBadges.id, id));
    return badge;
  }
  
  async createSovereigntyBadge(badge: InsertSovereigntyBadge): Promise<SovereigntyBadge> {
    const [newBadge] = await db.insert(sovereigntyBadges).values(badge).returning();
    return newBadge;
  }
}

export const storage = new DatabaseStorage();