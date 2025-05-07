import {
  pgTable,
  text,
  varchar,
  timestamp,
  jsonb,
  index,
  serial,
  boolean
} from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// Session storage table for authentication
export const sessions = pgTable(
  "sessions",
  {
    sid: varchar("sid").primaryKey(),
    sess: jsonb("sess").notNull(),
    expire: timestamp("expire").notNull(),
  },
  (table) => [index("IDX_session_expire").on(table.expire)],
);

// User table
export const users = pgTable("users", {
  id: varchar("id").primaryKey().notNull(),
  username: varchar("username").unique().notNull(),
  email: varchar("email").unique(),
  firstName: varchar("first_name"),
  lastName: varchar("last_name"),
  bio: text("bio"),
  profileImageUrl: varchar("profile_image_url"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

// Verification vector table - stores verification vectors for sovereignty claims
export const verificationVectors = pgTable("verification_vectors", {
  id: serial("id").primaryKey(),
  name: varchar("name").notNull(),
  description: text("description").notNull(),
  type: varchar("type").notNull(), // conceptual, temporal, axiom, identity, etc.
  strength: varchar("strength").notNull(), // Low, Medium, High, Very High
  filePath: varchar("file_path"), // Reference to related file if applicable
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

// Challenge records table - catalogs challenges to sovereignty claims
export const challengeRecords = pgTable("challenge_records", {
  id: serial("id").primaryKey(),
  patternType: varchar("pattern_type").notNull(), // From IP_CHALLENGE_PATTERNS.md
  description: text("description").notNull(),
  response: text("response"),
  verificationStrengthBeforeChallenge: varchar("verification_strength_before").notNull(),
  verificationStrengthAfterChallenge: varchar("verification_strength_after").notNull(),
  paradoxicalReinforcementFactor: varchar("reinforcement_factor").notNull(),
  isResolved: boolean("is_resolved").default(false),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

// Verification hash records - stores cryptographic verification hashes
export const verificationHashes = pgTable("verification_hashes", {
  id: serial("id").primaryKey(),
  documentType: varchar("document_type").notNull(), // DECLARATION, CONCEPTUAL_FINGERPRINT, etc.
  hashValue: varchar("hash_value").notNull(),
  verificationMethod: varchar("verification_method").notNull(), // SHA256, TrueAlpha, etc.
  createdAt: timestamp("created_at").defaultNow(),
});

// Dashboard metrics - stores real-time metrics for the dashboard
export const dashboardMetrics = pgTable("dashboard_metrics", {
  id: serial("id").primaryKey(),
  metricName: varchar("metric_name").notNull(),
  metricValue: varchar("metric_value").notNull(),
  metricType: varchar("metric_type").notNull(), // percentage, count, value, etc.
  displayOrder: serial("display_order").notNull(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

// Sovereignty badges - records earned badges
export const sovereigntyBadges = pgTable("sovereignty_badges", {
  id: serial("id").primaryKey(),
  badgeName: varchar("badge_name").notNull(),
  description: text("description").notNull(),
  criteria: text("criteria").notNull(),
  visualPath: varchar("visual_path").notNull(),
  issuedAt: timestamp("issued_at").defaultNow(),
});

// Define insert types using drizzle-zod
export const insertUserSchema = createInsertSchema(users).omit({ 
  createdAt: true, 
  updatedAt: true 
});

export const insertVerificationVectorSchema = createInsertSchema(verificationVectors).omit({ 
  id: true, 
  createdAt: true, 
  updatedAt: true 
});

export const insertChallengeRecordSchema = createInsertSchema(challengeRecords).omit({ 
  id: true, 
  createdAt: true, 
  updatedAt: true 
});

export const insertVerificationHashSchema = createInsertSchema(verificationHashes).omit({ 
  id: true, 
  createdAt: true 
});

export const insertDashboardMetricSchema = createInsertSchema(dashboardMetrics).omit({ 
  id: true, 
  updatedAt: true 
});

export const insertSovereigntyBadgeSchema = createInsertSchema(sovereigntyBadges).omit({ 
  id: true, 
  issuedAt: true 
});

// Define select types
export type User = typeof users.$inferSelect;
export type VerificationVector = typeof verificationVectors.$inferSelect;
export type ChallengeRecord = typeof challengeRecords.$inferSelect;
export type VerificationHash = typeof verificationHashes.$inferSelect;
export type DashboardMetric = typeof dashboardMetrics.$inferSelect;
export type SovereigntyBadge = typeof sovereigntyBadges.$inferSelect;

// Define insert types
export type InsertUser = z.infer<typeof insertUserSchema>;
export type InsertVerificationVector = z.infer<typeof insertVerificationVectorSchema>;
export type InsertChallengeRecord = z.infer<typeof insertChallengeRecordSchema>;
export type InsertVerificationHash = z.infer<typeof insertVerificationHashSchema>;
export type InsertDashboardMetric = z.infer<typeof insertDashboardMetricSchema>;
export type InsertSovereigntyBadge = z.infer<typeof insertSovereigntyBadgeSchema>;