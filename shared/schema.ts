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

// Types
export type TruthPattern = typeof truthPattern.$inferSelect;
export type InsertTruthPattern = typeof truthPattern.$inferInsert;

export type TextVerification = typeof textVerification.$inferSelect;
export type InsertTextVerification = typeof textVerification.$inferInsert;

export type VerificationHighlight = typeof verificationHighlight.$inferSelect;
export type InsertVerificationHighlight = typeof verificationHighlight.$inferInsert;

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

// Verification Request Schema
export const verifyTextSchema = z.object({
  content: z.string().min(10, "Text must be at least 10 characters long").max(10000, "Text cannot exceed 10,000 characters"),
  options: z.object({
    includeSummary: z.boolean().optional().default(true),
    sensitivityLevel: z.number().min(0).max(1).optional().default(0.7)
  }).optional().default({})
});

export type VerifyTextInput = z.infer<typeof verifyTextSchema>;