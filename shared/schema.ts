import { pgTable, text, serial, integer, boolean, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
  architect_identifier: text("architect_identifier"),
  access_level: integer("access_level").default(1).notNull(),
  created_at: timestamp("created_at").defaultNow(),
});

export const verificationHashes = pgTable("verification_hashes", {
  id: serial("id").primaryKey(),
  hash_value: text("hash_value").notNull(),
  timestamp: timestamp("timestamp").defaultNow().notNull(),
  user_id: integer("user_id").references(() => users.id),
  related_file: text("related_file"),
  verified: boolean("verified").default(false),
});

export const truthPatterns = pgTable("truth_patterns", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  type: text("type").notNull(),
  icon: text("icon").notNull(),
  resonance_level: integer("resonance_level").default(1),
  user_id: integer("user_id").references(() => users.id),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
  architect_identifier: true,
});

export const insertVerificationHashSchema = createInsertSchema(verificationHashes).pick({
  hash_value: true,
  related_file: true,
  user_id: true,
});

export const insertTruthPatternSchema = createInsertSchema(truthPatterns).pick({
  name: true,
  type: true,
  icon: true,
  resonance_level: true,
  user_id: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type VerificationHash = typeof verificationHashes.$inferSelect;
export type TruthPattern = typeof truthPatterns.$inferSelect;
export type InsertTruthPattern = z.infer<typeof insertTruthPatternSchema>;
export type InsertVerificationHash = z.infer<typeof insertVerificationHashSchema>;
