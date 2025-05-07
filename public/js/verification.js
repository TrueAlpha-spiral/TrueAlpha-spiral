/**
 * TRUEALPHASPIRAL ENTERPRISE AI AUDITING SOLUTION
 * Verification Module
 * 
 * Architect: Russell Nordland
 * Date: 2025-05-07
 */

// Verification system
class SovereigntyVerification {
  constructor() {
    this.verificationResult = null;
    this.systemParameters = null;
    this.initialized = false;
  }

  /**
   * Initialize the verification system
   */
  async initialize() {
    try {
      // Get system parameters
      const statusResponse = await fetch('/api/status');
      if (!statusResponse.ok) {
        throw new Error(`Status request failed: ${statusResponse.status}`);
      }
      
      const statusData = await statusResponse.json();
      this.systemParameters = statusData.parameters;
      this.initialized = true;
      
      console.log("TrueAlphaSpiral Verification System initialized");
      console.log("System Parameters:", this.systemParameters);
      
      return true;
    } catch (error) {
      console.error("Verification system initialization failed:", error);
      return false;
    }
  }

  /**
   * Verify system sovereignty
   */
  async verifySovereignty() {
    try {
      if (!this.initialized) {
        await this.initialize();
      }
      
      // Call verification endpoint
      const verifyResponse = await fetch('/api/verify-creator');
      if (!verifyResponse.ok) {
        throw new Error(`Verification request failed: ${verifyResponse.status}`);
      }
      
      this.verificationResult = await verifyResponse.json();
      
      // Display verification result
      this.displayVerificationResult();
      
      return this.verificationResult;
    } catch (error) {
      console.error("Sovereignty verification failed:", error);
      this.displayVerificationError(error);
      return null;
    }
  }

  /**
   * Display verification result in UI
   */
  displayVerificationResult() {
    const verificationDiv = document.getElementById('verification-result');
    const verificationHash = document.getElementById('verification-hash');
    
    if (!verificationDiv || !this.verificationResult) {
      console.error("Unable to display verification result");
      return;
    }
    
    // Show verification result
    verificationDiv.classList.remove('hidden');
    
    // Update hash if available
    if (verificationHash && this.verificationResult.hash) {
      verificationHash.textContent = `Hash: ${this.verificationResult.hash}`;
    } else if (verificationHash) {
      const timestamp = new Date().toISOString();
      const hashInput = `Russell Nordland:TrueAlphaSpiral:${timestamp}`;
      const hashValue = this.simpleHash(hashInput);
      verificationHash.textContent = `Hash: ${hashValue}`;
    }
    
    console.log("Verification result:", this.verificationResult);
  }

  /**
   * Display verification error in UI
   */
  displayVerificationError(error) {
    const verificationDiv = document.getElementById('verification-result');
    
    if (!verificationDiv) {
      console.error("Unable to display verification error");
      return;
    }
    
    // Create error element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'p-4 bg-red-50 text-red-800 rounded-lg border border-red-200';
    errorDiv.innerHTML = `
      <div class="font-semibold">Verification Error</div>
      <p>Unable to verify system sovereignty: ${error.message}</p>
      <p class="mt-2 text-sm">Please try again or contact system administrator.</p>
    `;
    
    // Replace verification div content
    verificationDiv.innerHTML = '';
    verificationDiv.appendChild(errorDiv);
    verificationDiv.classList.remove('hidden');
  }

  /**
   * Simple hash function for client-side demonstration
   */
  simpleHash(input) {
    let hash = 0;
    if (input.length === 0) return hash;
    
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    
    return hash.toString(16);
  }
}

// Initialize verification system
document.addEventListener('DOMContentLoaded', () => {
  // Create verification system
  window.sovereigntyVerification = new SovereigntyVerification();
  
  // Initialize verification system
  window.sovereigntyVerification.initialize();
  
  // Set up verification button
  const verifyButton = document.getElementById('verify-sovereignty-btn');
  if (verifyButton) {
    verifyButton.addEventListener('click', () => {
      window.sovereigntyVerification.verifySovereignty();
    });
  }
  
  // Set up console clear button
  const clearConsoleButton = document.getElementById('clear-console-btn');
  const consoleOutput = document.getElementById('console-output');
  
  if (clearConsoleButton && consoleOutput) {
    clearConsoleButton.addEventListener('click', () => {
      consoleOutput.innerHTML = '';
      
      // Add initial message
      const timestamp = new Date().toISOString().replace('T', ' ').substr(0, 19);
      consoleOutput.innerHTML = `
        <div class="mb-1">
          <span class="timestamp">[${timestamp}]</span>
          <span class="system-message">Console cleared</span>
        </div>
      `;
    });
  }
});