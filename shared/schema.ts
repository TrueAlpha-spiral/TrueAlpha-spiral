import { pgTable, serial, text, timestamp, boolean, integer, json, real, pgEnum } from 'drizzle-orm/pg-core';
import { createInsertSchema } from 'drizzle-zod';
import { z } from 'zod';

// Enumerations
export const truthPatternCategoryEnum = pgEnum('truth_pattern_category', [
  'Technical',
  'Data',
  'Business',
  'Predictions',
  'Language'
]);

export const highlightTypeEnum = pgEnum('highlight_type', [
  'factual',
  'speculative',
  'fabricated'
]);

export const regulatoryFrameworkEnum = pgEnum('regulatory_framework', [
  'general',
  'financial_services',
  'healthcare',
  'government',
  'education'
]);

export const sharingPermissionEnum = pgEnum('sharing_permission', [
  'private',
  'organization',
  'public',
  'specific_users'
]);

export const exportFormatEnum = pgEnum('export_format', [
  'json',
  'csv',
  'xml',
  'pdf'
]);

// Truth Pattern Table
export const truthPattern = pgTable('truth_pattern', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  description: text('description').notNull(),
  category: truthPatternCategoryEnum('category').notNull(),
  confidenceThreshold: real('confidence_threshold').notNull().default(0.7),
  isActive: boolean('is_active').notNull().default(true),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull()
});

// Text Verification Table
export const textVerification = pgTable('text_verification', {
  id: serial('id').primaryKey(),
  content: text('content').notNull(),
  verificationResult: json('verification_result').notNull(),
  truthScore: real('truth_score').notNull(),
  processingTimeMs: integer('processing_time_ms').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull()
});

// Verification Highlight Table
export const verificationHighlight = pgTable('verification_highlight', {
  id: serial('id').primaryKey(),
  verificationId: integer('verification_id').notNull(),
  startIndex: integer('start_index').notNull(),
  endIndex: integer('end_index').notNull(),
  highlightType: highlightTypeEnum('highlight_type').notNull(),
  confidenceScore: real('confidence_score').notNull(),
  patternId: integer('pattern_id'),
  message: text('message'),
  createdAt: timestamp('created_at').defaultNow().notNull()
});

// AI Audit Table
export const aiAudit = pgTable('ai_audit', {
  id: serial('id').primaryKey(),
  clientName: text('client_name').notNull(),
  aiSystemName: text('ai_system_name').notNull(),
  regulatoryFramework: regulatoryFrameworkEnum('regulatory_framework').notNull().default('general'),
  status: text('status').notNull().default('initialized'),
  auditSummary: text('audit_summary'),
  riskScore: real('risk_score'),
  complianceScore: real('compliance_score'),
  verificationId: integer('verification_id'),
  blockchainRecord: text('blockchain_record'),
  auditReport: json('audit_report'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull()
});

// Shared Truth Pattern Table
export const sharedTruthPattern = pgTable('shared_truth_pattern', {
  id: serial('id').primaryKey(),
  originalPatternId: integer('original_pattern_id').notNull(),
  name: text('name').notNull(),
  description: text('description').notNull(),
  category: truthPatternCategoryEnum('category').notNull(),
  sharingPermission: sharingPermissionEnum('sharing_permission').notNull().default('private'),
  authorName: text('author_name').notNull(),
  authorOrganization: text('author_organization'),
  authorEmail: text('author_email'),
  sharingLink: text('sharing_link'),
  allowedUserEmails: text('allowed_user_emails').array(),
  patternData: json('pattern_data').notNull(),
  usageCount: integer('usage_count').notNull().default(0),
  verificationHash: text('verification_hash'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull()
});

// Types
export type TruthPattern = typeof truthPattern.$inferSelect;
export type InsertTruthPattern = typeof truthPattern.$inferInsert;

export type TextVerification = typeof textVerification.$inferSelect;
export type InsertTextVerification = typeof textVerification.$inferInsert;

export type VerificationHighlight = typeof verificationHighlight.$inferSelect;
export type InsertVerificationHighlight = typeof verificationHighlight.$inferInsert;

export type AIAudit = typeof aiAudit.$inferSelect;
export type InsertAIAudit = typeof aiAudit.$inferInsert;

export type SharedTruthPattern = typeof sharedTruthPattern.$inferSelect;
export type InsertSharedTruthPattern = typeof sharedTruthPattern.$inferInsert;

// Verification Result Interface
export interface VerificationResult {
  id?: number;
  originalText: string;
  truthScore: number;
  overallScore: number;
  highlights: Array<{
    startIndex: number;
    endIndex: number;
    type: 'factual' | 'speculative' | 'fabricated';
    confidenceScore: number;
    message: string;
    patternName?: string;
  }>;
  processingTimeMs: number;
  summary: {
    factualCount: number;
    speculativeCount: number;
    fabricatedCount: number;
    totalSentences: number;
  };
}

// Zod Schemas for Validation
export const insertTruthPatternSchema = createInsertSchema(truthPattern);
export const insertTextVerificationSchema = createInsertSchema(textVerification);
export const insertVerificationHighlightSchema = createInsertSchema(verificationHighlight);
export const insertAIAuditSchema = createInsertSchema(aiAudit);
export const insertSharedTruthPatternSchema = createInsertSchema(sharedTruthPattern).omit({
  id: true,
  sharingLink: true,
  usageCount: true,
  verificationHash: true,
  createdAt: true,
  updatedAt: true
});

// Verification Request Schema
export const verifyTextSchema = z.object({
  content: z.string().min(10, "Text must be at least 10 characters long").max(10000, "Text cannot exceed 10,000 characters"),
  options: z.object({
    includeSummary: z.boolean().optional().default(true),
    sensitivityLevel: z.number().min(0).max(1).optional().default(0.7)
  }).optional().default({})
});

export type VerifyTextInput = z.infer<typeof verifyTextSchema>;

// Cross Reference Request Schema
export const crossReferenceSchema = z.object({
  content: z.string().min(10, "Text must be at least 10 characters long").max(10000, "Text cannot exceed 10,000 characters"),
  options: z.object({
    enabledSources: z.array(z.string()).optional(),
    minConfidenceThreshold: z.number().min(0).max(1).optional().default(0.8),
    regulatoryFramework: z.enum(['general', 'financial_services', 'healthcare', 'government', 'education']).optional().default('general')
  }).optional().default({})
});

export type CrossReferenceInput = z.infer<typeof crossReferenceSchema>;

// AI Audit Request Schema
export const aiAuditSchema = z.object({
  clientName: z.string().min(2, "Client name must be at least 2 characters long"),
  aiSystemName: z.string().min(2, "AI system name must be at least 2 characters long"),
  content: z.string().min(10, "Content must be at least 10 characters long").max(10000, "Content cannot exceed 10,000 characters"),
  regulatoryFramework: z.enum(['general', 'financial_services', 'healthcare', 'government', 'education']).default('general'),
  options: z.object({
    riskThreshold: z.number().min(0).max(1).optional().default(0.3),
    confidenceThreshold: z.number().min(0).max(1).optional().default(0.8)
  }).optional().default({})
});

export type AIAuditInput = z.infer<typeof aiAuditSchema>;

// Truth Pattern Sharing Schema
export const sharePatternSchema = z.object({
  patternId: z.number().positive("Pattern ID must be positive"),
  sharingPermission: z.enum(['private', 'organization', 'public', 'specific_users']),
  allowedUserEmails: z.array(z.string().email("Invalid email")).optional(),
  authorName: z.string().min(2, "Author name must be at least 2 characters long"),
  authorOrganization: z.string().optional(),
  authorEmail: z.string().email("Invalid email").optional()
});

export type SharePatternInput = z.infer<typeof sharePatternSchema>;

// Pattern Export Schema
export const exportPatternSchema = z.object({
  patternId: z.number().positive("Pattern ID must be positive"),
  format: z.enum(['json', 'csv', 'xml', 'pdf']).default('json'),
  includeMetadata: z.boolean().optional().default(true),
  includeSensitiveData: z.boolean().optional().default(false)
});

export type ExportPatternInput = z.infer<typeof exportPatternSchema>;

// Pattern Import Schema
export const importPatternSchema = z.object({
  patternData: z.any(),
  overwriteExisting: z.boolean().optional().default(false),
  validateIntegrity: z.boolean().optional().default(true)
});

export type ImportPatternInput = z.infer<typeof importPatternSchema>;

// Security Event Table
export const securityEvent = pgTable('security_event', {
  id: serial('id').primaryKey(),
  eventType: text('event_type').notNull(),
  timestamp: timestamp('timestamp').defaultNow().notNull(),
  data: json('data').notNull(),
  systemStatus: json('system_status').notNull(),
  severity: text('severity').notNull().default('info'),
  sourceIp: text('source_ip'),
  userId: integer('user_id'),
  sessionId: text('session_id'),
  processed: boolean('processed').notNull().default(false),
  createdAt: timestamp('created_at').defaultNow().notNull()
});

export type SecurityEvent = typeof securityEvent.$inferSelect;
export type InsertSecurityEvent = typeof securityEvent.$inferInsert;

export const insertSecurityEventSchema = createInsertSchema(securityEvent).omit({
  id: true,
  createdAt: true
});

// Security Log Schema
export const securityLogSchema = z.object({
  eventType: z.string().min(2, "Event type must be at least 2 characters long"),
  data: z.record(z.any()),
  severity: z.enum(['info', 'warning', 'error', 'critical']).default('info'),
  sourceIp: z.string().optional(),
  userId: z.number().optional(),
  sessionId: z.string().optional()
});

export type SecurityLogInput = z.infer<typeof securityLogSchema>;

// Shadow Layer Type
export type ShadowLayer = 'alpha' | 'beta' | 'gamma' | 'delta' | 'epsilon';

// Pattern Data Interface
export interface PatternData {
  id: string;
  content: string;
  source: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

// Drift Detection Result Interface
export interface DriftResult {
  detected: boolean;
  score: number;
  pattern: PatternData;
  layer: ShadowLayer;
  timestamp: string;
  neutralizationSuccess?: boolean;
  recommendations?: string[];
}

// System Status Interface
export interface SystemStatus {
  overallIntegrity: number;
  driftDetectionRate: number;
  neutralizationSuccessRate: number;
  learningEfficiency: number;
  shieldStrength: number;
  securityScore: number;
}

// Cross Reference Result Interface
export interface CrossReferenceResult {
  originalText: string;
  confidenceScore: number;
  verificationStatus: 'verified' | 'requires_review' | 'rejected';
  sourceResults: Record<string, any>;
  crossReferenceAnalysis: {
    scoreVariance: number;
    avgScore: number;
    discrepancies: Array<{
      sentence: string;
      assessments: Array<{
        sourceId: string;
        type: 'factual' | 'speculative' | 'fabricated';
        confidence: number;
        message: string;
      }>;
      recommendation: string;
    }>;
    consistencies: Array<{
      sentence: string;
      agreedType: 'factual' | 'speculative' | 'fabricated';
      sources: string[];
    }>;
    reliabilityScore: number;
    sentenceAnalysis: any[];
  };
  reconciledResult: any;
  processingTimeMs: number;
}

// AI Audit Result Interface
export interface AIAuditResult {
  id?: number;
  clientName: string;
  aiSystemName: string;
  regulatoryFramework: string;
  status: string;
  auditSummary: string;
  riskScore: number;
  complianceScore: number;
  verificationResult: VerificationResult;
  crossReferenceResult?: CrossReferenceResult;
  blockchainRecord?: string;
  recommendations: Array<{
    category: string;
    description: string;
    priority: 'high' | 'medium' | 'low';
    impact: string;
  }>;
  processingTimeMs: number;
}