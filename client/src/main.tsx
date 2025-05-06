import { createRoot } from "react-dom/client";
import { StrictMode } from "react";
import App from "./App";
import "./index.css";
import { initializeStatusChecker } from "./lib/statusChecker";

// Global error handling for debugging
window.addEventListener('error', (event) => {
  console.error('Global error caught:', event.message, event.error);
  
  // Update loading status if there's an error
  if (window.updateLoadingStatus) {
    window.updateLoadingStatus('Error: ' + event.message);
  }
});

// Add debugging info
console.log("Starting TrueAlphaSpiral application...");
console.log("Environment:", import.meta.env.MODE);
// Detect environment and use appropriate base URL
const isReplit = window.location.hostname.includes('replit') || 
                window.location.hostname.includes('.repl.co') ||
                window.location.hostname.includes('repl.run') ||
                window.location.hostname.includes('replit.dev');

// In Replit, we need to detect the correct base URL format
// Try multiple URL formats for maximum compatibility
// Start with the empty string for relative URLs first as it should work in Replit
const potentialBaseUrls = [
  '', // Empty string for relative URLs (best for Replit)
  window.location.origin, // Default: includes protocol, hostname, and port
  `${window.location.protocol}//${window.location.hostname}:5000`, // Explicit port 5000
  `https://${window.location.hostname}`, // HTTPS with hostname only
  `${window.location.protocol}//${window.location.hostname}`, // Protocol and hostname without port
  `//${window.location.host}`, // Protocol-relative URL
  
  // Additional Replit-specific patterns
  ...(window.location.hostname.includes('replit') ? [
    `https://${window.location.hostname.split('.')[0]}.replit.dev`,
    `https://${window.location.hostname}`,
    window.location.origin.replace(/:\d+$/, ''), // Remove port if present
  ] : [])
];

// Global variable to store the working base URL after verification
window.BASE_API_URL = '';

console.log("Potential base URLs:", potentialBaseUrls);
console.log("Running in Replit:", isReplit);

// We'll try these URLs in sequence until one works
let baseUrlIndex = 0;
const baseUrl = potentialBaseUrls[baseUrlIndex];

// Add a network status indicator
const statusIndicator = document.createElement('div');
statusIndicator.style.position = 'fixed';
statusIndicator.style.bottom = '10px';
statusIndicator.style.right = '10px';
statusIndicator.style.padding = '5px 10px';
statusIndicator.style.borderRadius = '5px';
statusIndicator.style.fontSize = '12px';
statusIndicator.style.fontFamily = 'monospace';
statusIndicator.style.zIndex = '9999';
statusIndicator.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
statusIndicator.style.color = '#00e5ff';
statusIndicator.style.border = '1px solid #6e44ff';
statusIndicator.id = 'network-status';

// Function to update connection status
function updateNetworkStatus(online: boolean) {
  if (online) {
    statusIndicator.textContent = '🟢 Connected';
    statusIndicator.style.color = '#00ff9d';
  } else {
    statusIndicator.textContent = '🔴 Disconnected';
    statusIndicator.style.color = '#ff3e3e';
    
    // Update loading status
    if (window.updateLoadingStatus) {
      window.updateLoadingStatus('Connection lost. Attempting to reconnect...');
    }
  }
}

// Initial status
updateNetworkStatus(navigator.onLine);

// Listen for online/offline events
window.addEventListener('online', () => {
  updateNetworkStatus(true);
  if (window.updateLoadingStatus) {
    window.updateLoadingStatus('Connection restored, continuing...');
  }
});
window.addEventListener('offline', () => updateNetworkStatus(false));

// Add indicator to body
document.body.appendChild(statusIndicator);

// Check if the application loaded properly
let appLoaded = false;
let checkAttempts = 0;
const maxAttempts = 10;

// Function to try connecting with different base URLs
const tryConnect = (urlIndex: number) => {
  if (urlIndex >= potentialBaseUrls.length) {
    // If we've tried all URLs, increment the attempt counter and restart from the first URL
    checkAttempts++;
    if (checkAttempts < maxAttempts) {
      console.log(`All base URLs failed. Retrying... (Attempt ${checkAttempts + 1}/${maxAttempts})`);
      setTimeout(() => tryConnect(0), 2000);
    } else {
      // Max attempts reached
      console.log("Max connection attempts reached, proceeding anyway");
      if (window.updateLoadingStatus) {
        window.updateLoadingStatus('Proceeding with limited connectivity');
      }
      setTimeout(() => {
        if (window.hideLoadingScreen) {
          window.hideLoadingScreen();
        }
      }, 1000);
      appLoaded = true;
    }
    return;
  }
  
  const currentBaseUrl = potentialBaseUrls[urlIndex];
  console.log(`Trying base URL: ${currentBaseUrl} (Attempt ${checkAttempts + 1}/${maxAttempts}, URL ${urlIndex + 1}/${potentialBaseUrls.length})`);
  
  // First try the health endpoint which we know is working
  // Also try both /api/health and /health since Express might expose both
  const healthEndpoint = urlIndex % 2 === 0 ? "/api/health" : "/health";
  console.log(`Trying health endpoint: ${currentBaseUrl}${healthEndpoint}`);
  
  fetch(currentBaseUrl + healthEndpoint, {
    method: "GET",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Cache-Control": "no-cache"
    },
    mode: 'cors',
    credentials: 'include'
  })
    .then(response => {
      console.log("Health API endpoint responded with status:", response.status);
      if (response.ok) {
        console.log("Server connection verified through /api/health endpoint");
        if (window.updateLoadingStatus) {
          window.updateLoadingStatus('Quantum connection established');
        }
        
        // Basic connectivity verified, proceed with response
        return response;
      } else {
        throw new Error("Server unavailable");
      }
    })
    .then(response => {
      console.log("Health endpoint responded with status:", response.status);
      if (response.ok) {
        console.log("Health endpoint verified, connection established");
        
        // Check Python API server status using currentBaseUrl
        // Save the working base URL as soon as we confirm the first API works
        // This ensures it's available for the rest of the application
        window.BASE_API_URL = currentBaseUrl;
        console.log("Setting global BASE_API_URL to:", window.BASE_API_URL);

        fetch(currentBaseUrl + "/api/python-system/status")
          .then(pythonResponse => {
            if (pythonResponse.ok) {
              console.log("Python API server connection verified");
              
              if (window.updateLoadingStatus) {
                window.updateLoadingStatus('Quantum DNA integration complete');
              }
            } else {
              console.log("Python API server not fully initialized, proceeding anyway");
            }
            
            // Hide loading screen after a short delay
            setTimeout(() => {
              if (window.hideLoadingScreen) {
                window.hideLoadingScreen();
              }
            }, 800);
            appLoaded = true;
          })
          .catch(() => {
            console.log("Python API server connection failed, proceeding anyway");
            setTimeout(() => {
              if (window.hideLoadingScreen) {
                window.hideLoadingScreen();
              }
            }, 800);
            appLoaded = true;
          });
      } else {
        console.log("Server error:", response.status);
        if (window.updateLoadingStatus) {
          window.updateLoadingStatus(`Quantum fluctuation detected (${checkAttempts}/${maxAttempts}), recalibrating...`);
        }
        // Try the next base URL
        setTimeout(() => tryConnect(urlIndex + 1), 1500);
      }
    })
    .catch(error => {
      console.error("Connection error:", error);
      if (window.updateLoadingStatus) {
        window.updateLoadingStatus(`Connection error (${checkAttempts}/${maxAttempts}): ${error.message}`);
      }
      // Try the next base URL
      setTimeout(() => tryConnect(urlIndex + 1), 2000);
    });
};

// Start the connection attempt with the first URL
setTimeout(() => tryConnect(0), 1000);

// Set a fallback timeout to hide the loading screen even if we can't connect at all
// This ensures users won't get stuck on the loading screen indefinitely
setTimeout(() => {
  if (!appLoaded) {
    console.log("Fallback timeout reached, forcing app to load anyway");
    // In Replit environment, we'll default to using relative URLs if all attempts fail
    window.BASE_API_URL = '';
    if (window.updateLoadingStatus) {
      window.updateLoadingStatus('Proceeding with application initialization');
    }
    setTimeout(() => {
      if (window.hideLoadingScreen) {
        window.hideLoadingScreen();
      }
      appLoaded = true;
      
      // Add a visible note about using relative paths
      console.log("Using relative paths for API requests due to connectivity issues");
      
      // Final attempt with relative paths for critical endpoints
      fetch('/api/health')
        .then(response => {
          if (response.ok) {
            console.log("Server connection verified with final relative path attempt");
          }
        })
        .catch(err => console.log("Final connection attempt failed:", err));
    }, 800);
  }
}, 10000); // Reduced timeout to 10 seconds for better UX

// Initialize the status checker with sovereign protection to ensure system integrity
setTimeout(() => {
  console.log("Initializing TrueAlphaSpiral Status Checker with Russell Nordland's sovereign protection");
  const statusChecker = initializeStatusChecker();
  
  // Ensure we have a status endpoint working
  statusChecker.fetchStatus()
    .then(status => {
      if (status) {
        console.log("Sovereign status verified and protected");
      } else {
        console.log("Status endpoint not yet available, will continue monitoring");
      }
    });
    
  // Load the Sovereign Defense Shield for client-side protection
  console.log("Loading Sovereign Defense Shield to prevent misappropriation");
  const script = document.createElement('script');
  script.src = '/sovereign_defense_shield.js';
  script.setAttribute('data-creator', 'Russell Nordland');
  script.setAttribute('data-integrity', 'sovereign');
  document.body.appendChild(script);
}, 2000);

// Type declaration for window object
declare global {
  interface Window {
    hideLoadingScreen?: () => void;
    updateLoadingStatus?: (message: string) => void;
    BASE_API_URL: string;
  }
}

// Render the app
const root = createRoot(document.getElementById("root")!);
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
