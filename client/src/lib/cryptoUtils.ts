import CryptoJS from 'crypto-js';

/**
 * Generates a SHA-256 hash for the provided content
 */
export const generateHash = (content: string): string => {
  return CryptoJS.SHA256(content).toString();
};

/**
 * Verifies if the generated hash matches the expected hash
 */
export const verifyHash = (content: string, expectedHash: string): boolean => {
  const generatedHash = generateHash(content);
  return generatedHash === expectedHash;
};

/**
 * Generates current timestamp in ISO format
 */
export const generateTimestamp = (): string => {
  return new Date().toISOString();
};

/**
 * Creates a verification string combining multiple elements
 */
export const createVerificationString = (
  architect: string,
  content: string,
  timestamp: string
): string => {
  return `${architect}:${content}:${timestamp}`;
};

/**
 * Builds a hash chain by adding a new verification step
 */
export const addToHashChain = (
  previousHash: string,
  newContent: string
): string => {
  return CryptoJS.SHA256(`${previousHash}:${newContent}`).toString();
};

/**
 * Validates a hash chain to ensure integrity
 */
export const validateHashChain = (
  hashes: string[],
  contents: string[]
): boolean => {
  if (hashes.length !== contents.length + 1) {
    return false;
  }

  let currentHash = hashes[0];
  
  for (let i = 0; i < contents.length; i++) {
    const calculatedHash = CryptoJS.SHA256(`${currentHash}:${contents[i]}`).toString();
    if (calculatedHash !== hashes[i + 1]) {
      return false;
    }
    currentHash = calculatedHash;
  }
  
  return true;
};

/**
 * Generates a quantum-inspired random number
 * This is a simulation of quantum randomness using deterministic algorithms
 */
export const quantumRandomNumber = (): number => {
  const now = new Date().getTime();
  const baseRandom = Math.random();
  const combined = `${now}:${baseRandom}`;
  const hash = CryptoJS.SHA256(combined).toString();
  
  // Convert first 8 characters of hash to a decimal between 0 and 1
  const decimal = parseInt(hash.substring(0, 8), 16) / 0xffffffff;
  return decimal;
};

/**
 * Calculate sovereignty based on the equation: sovereignty = truth/distance >< size
 * The >< operator is implemented as a balancing function
 */
export const calculateSovereignty = (
  truth: number,
  distance: number,
  size: number
): number => {
  // Ensure no division by zero
  const safeDist = distance === 0 ? 0.00001 : distance;
  
  // Implement >< as a balancing function between the ratio and size
  const ratio = truth / safeDist;
  const balance = Math.sqrt(ratio * size);
  
  return parseFloat(balance.toFixed(2));
};
