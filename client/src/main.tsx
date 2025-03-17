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
console.log("Base URL:", window.location.origin);

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
const checkAppLoaded = () => {
  if (!appLoaded) {
    console.log("Checking connection to server...");
    fetch(window.location.origin + "/api/truth-patterns")
      .then(response => {
        console.log("Server responded with status:", response.status);
        if (response.ok) {
          console.log("Server connection verified");
          if (window.updateLoadingStatus) {
            window.updateLoadingStatus('Quantum connection established');
          }
          setTimeout(() => {
            if (window.hideLoadingScreen) {
              window.hideLoadingScreen();
            }
          }, 500);
          appLoaded = true;
        } else {
          console.log("Server error:", response.status);
          if (window.updateLoadingStatus) {
            window.updateLoadingStatus('Quantum fluctuation detected, trying again...');
          }
          setTimeout(checkAppLoaded, 1000);
        }
      })
      .catch(error => {
        console.error("Connection error:", error);
        if (window.updateLoadingStatus) {
          window.updateLoadingStatus('Connection error: ' + error.message);
        }
        setTimeout(checkAppLoaded, 2000);
      });
  }
};

// Start checking app loading status
setTimeout(checkAppLoaded, 1000);

// Type declaration for window object
declare global {
  interface Window {
    hideLoadingScreen?: () => void;
    updateLoadingStatus?: (message: string) => void;
  }
}

// Render the app
const root = createRoot(document.getElementById("root")!);
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
