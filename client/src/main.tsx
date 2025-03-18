import { createRoot } from "react-dom/client";
import { StrictMode } from "react";
import App from "./App";
import "./index.css";

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
const potentialBaseUrls = [
  window.location.origin, // Default: includes protocol, hostname, and port
  `${window.location.protocol}//${window.location.hostname}`, // Protocol and hostname without port
  window.location.origin.replace(/:\d+$/, ''), // Remove port if present
  window.location.origin.replace(/:\d+$/, '') + ':5000', // Use explicit port 5000
  window.location.origin.replace(/:5173$/, ':5000'), // Vite dev port to server port
  window.location.origin.replace(/:\d+$/, '') // No port at all
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
  
  // First try the simpler /api endpoint for connectivity test - use a specific API endpoint
  fetch(currentBaseUrl + "/api/truth-patterns", {
    method: "GET",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Cache-Control": "no-cache"
    }
  })
    .then(response => {
      console.log("Truth patterns API endpoint responded with status:", response.status);
      if (response.ok) {
        console.log("Server connection verified through /api/truth-patterns endpoint");
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
      console.log("Truth patterns endpoint responded with status:", response.status);
      if (response.ok) {
        console.log("Truth patterns endpoint verified");
        
        // Check Python API server status using currentBaseUrl
        fetch(currentBaseUrl + "/api/python-system/status")
          .then(pythonResponse => {
            if (pythonResponse.ok) {
              console.log("Python API server connection verified");
              // Save the working base URL for the whole application to use
              window.BASE_API_URL = currentBaseUrl;
              console.log("Setting global BASE_API_URL to:", window.BASE_API_URL);
              
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
