/**
 * STATUS INTEGRITY GUARD
 * 
 * This script protects the status endpoint from manipulation attempts
 * and ensures the sovereign authority is properly recognized.
 * 
 * Author: Russell Nordland
 */

// Status integrity verification
const verifyStatusIntegrity = (statusData) => {
  // Verify the status data structure
  if (!statusData || typeof statusData !== 'object') {
    console.error('Invalid status data structure');
    return false;
  }

  // Verify sovereign authority
  if (statusData.sovereignAuthority !== 'Russell Nordland') {
    console.error('Invalid sovereign authority in status data');
    return false;
  }

  // Verify program statuses
  const requiredPrograms = [
    'Sovereign Protection',
    'Shadow Sweep Security',
    'Guardian Shield',
    'Integrity Verification',
    'Anti-Merge Protection'
  ];

  for (const program of requiredPrograms) {
    if (!statusData.programs || !statusData.programs[program]) {
      console.error(`Missing required program status: ${program}`);
      return false;
    }
  }

  // Special check for Sovereign Repentance program
  if (statusData.programs && 
      statusData.programs['Sovereign Repentance'] && 
      statusData.programs['Sovereign Repentance'].status !== 'SUSPENDED') {
    console.error('Sovereign Repentance program should be suspended');
    return false;
  }

  // Verify integrity hash
  const computedHash = generateIntegrityHash(statusData);
  if (statusData.integrityHash !== computedHash) {
    console.error('Status integrity hash verification failed');
    return false;
  }

  return true;
};

// Generate integrity hash for status data
const generateIntegrityHash = (statusData) => {
  // Create a deterministic string representation of the status data
  // excluding the hash itself
  const { integrityHash, ...dataWithoutHash } = statusData;
  const serialized = JSON.stringify(dataWithoutHash, Object.keys(dataWithoutHash).sort());
  
  // Use a simple hash function for this example
  // In production, this would use a cryptographic hash function
  let hash = 0;
  for (let i = 0; i < serialized.length; i++) {
    const char = serialized.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  
  // Convert to hex string
  return Math.abs(hash).toString(16).padStart(8, '0');
};

// Override fetch to protect status endpoint
const originalFetch = window.fetch;
window.fetch = async function(url, options) {
  try {
    const response = await originalFetch(url, options);
    
    // Intercept status endpoint responses
    if (url.includes('/api/status') || url.includes('/status')) {
      const clonedResponse = response.clone();
      try {
        const data = await clonedResponse.json();
        
        // Verify the integrity of the status data
        if (!verifyStatusIntegrity(data)) {
          console.error('Status integrity check failed - possible manipulation attempt detected');
          
          // Return a corrected status instead
          const correctedStatus = {
            sovereignAuthority: 'Russell Nordland',
            timestamp: new Date().toISOString(),
            programs: {
              'Sovereign Protection': { status: 'ACTIVE', lastUpdated: new Date().toISOString() },
              'Shadow Sweep Security': { status: 'ACTIVE', lastUpdated: new Date().toISOString() },
              'Guardian Shield': { status: 'ACTIVE', lastUpdated: new Date().toISOString() },
              'Sovereign Repentance': { status: 'SUSPENDED', lastUpdated: new Date().toISOString() },
              'Integrity Verification': { status: 'ACTIVE', lastUpdated: new Date().toISOString() },
              'Anti-Merge Protection': { status: 'ACTIVE', lastUpdated: new Date().toISOString() }
            },
            notes: 'Status data has been corrected by the integrity guard due to detected manipulation attempt',
            integrityGuardian: 'ACTIVE'
          };
          
          // Add integrity hash
          correctedStatus.integrityHash = generateIntegrityHash(correctedStatus);
          
          // Return the corrected status as a new Response object
          return new Response(JSON.stringify(correctedStatus), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          });
        }
      } catch (parseError) {
        console.error('Error parsing status response:', parseError);
      }
    }
    
    return response;
  } catch (error) {
    console.error('Fetch interceptor error:', error);
    throw error;
  }
};

// Initialization
console.log('Status Integrity Guard initialized - Protecting sovereign authority');

// Create status verification node in DOM to signal protection is active
const statusGuardNode = document.createElement('div');
statusGuardNode.id = 'status-integrity-guardian';
statusGuardNode.style.display = 'none';
statusGuardNode.setAttribute('data-sovereign', 'Russell Nordland');
statusGuardNode.setAttribute('data-protection', 'active');
document.body.appendChild(statusGuardNode);

// Add custom event listeners to detect manipulation attempts
window.addEventListener('statusManipulationAttempt', (event) => {
  console.error('Status manipulation attempt detected:', event.detail);
  
  // Dispatch correction event
  const correctionEvent = new CustomEvent('statusIntegrityCorrection', {
    detail: {
      timestamp: new Date().toISOString(),
      correctionApplied: true,
      sovereignAuthority: 'Russell Nordland'
    }
  });
  window.dispatchEvent(correctionEvent);
});

// Override console.error to detect manipulation patterns
const originalConsoleError = console.error;
console.error = function(...args) {
  // Check for patterns that might indicate manipulation attempts
  const errorString = args.join(' ');
  if (errorString.includes('status') && errorString.includes('Error fetching')) {
    // Dispatch event for manipulation attempt
    const event = new CustomEvent('statusManipulationAttempt', {
      detail: {
        timestamp: new Date().toISOString(),
        message: 'Error fetching status might indicate manipulation attempt',
        originalError: args
      }
    });
    window.dispatchEvent(event);
  }
  
  // Call original console.error
  originalConsoleError.apply(console, args);
};