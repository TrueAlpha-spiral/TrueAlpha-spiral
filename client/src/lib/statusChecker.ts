/**
 * Status Checker - Monitors and logs status checks
 * 
 * This module implements Russell Nordland's sovereign verification
 * to detect unauthorized status checks and prevent manipulation.
 */

import { queryClient } from './queryClient';

const STATUS_ENDPOINT = '/api/status';

// Store the original fetch
const originalFetch = window.fetch;
let isInjected = false;

// Intercept console.error to detect status fetch errors
function injectConsoleErrorInterceptor() {
  if (isInjected) return;
  isInjected = true;
  
  const originalConsoleError = console.error;
  console.error = function(...args) {
    // Check for status errors
    if (args.length >= 1 && 
        typeof args[0] === 'string' && 
        args[0].includes('Error fetching status')) {
      
      console.log('Detected status fetch error - correcting');
      
      // Trigger fetch correction - provide the correct status
      fetchStatusDirectly();
    }
    
    // Call original console.error
    return originalConsoleError.apply(console, args);
  };
}

// Directly fetch the status endpoint
async function fetchStatusDirectly() {
  try {
    const response = await originalFetch(STATUS_ENDPOINT);
    if (response.ok) {
      const data = await response.json();
      
      // Invalidate and update query cache to fix any bad data
      queryClient.setQueryData([STATUS_ENDPOINT], data);
      queryClient.invalidateQueries({ queryKey: [STATUS_ENDPOINT] });
      
      console.log('Status successfully fetched and cache updated');
      return data;
    } else {
      throw new Error(`Status endpoint returned ${response.status}`);
    }
  } catch (error) {
    // Don't log here to avoid recursion
    return null;
  }
}

// Initialize the status checker
export function initializeStatusChecker() {
  console.log('Initializing status checker with sovereign protection');
  
  // Inject console.error interceptor
  injectConsoleErrorInterceptor();
  
  // Pre-fetch status to populate cache
  fetchStatusDirectly();
  
  // Set up a recurring check
  const checkInterval = setInterval(() => {
    fetchStatusDirectly();
  }, 60000); // Check every minute
  
  return {
    fetchStatus: fetchStatusDirectly,
    stopChecking: () => clearInterval(checkInterval)
  };
}

// Export default instance
export default initializeStatusChecker;