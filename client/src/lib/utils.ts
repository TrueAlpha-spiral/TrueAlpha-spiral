import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines class names with tailwind-merge to handle conflicting classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}