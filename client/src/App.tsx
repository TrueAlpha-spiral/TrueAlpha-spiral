import React from "react";
import { Route, Switch } from "wouter";
import { Toaster } from "@/components/ui/toaster";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";
import HomePage from "@/pages/home-page";
import PricingPage from "@/pages/pricing-page";
import CrossReferenceDemo from "@/pages/cross-reference-demo";
import AiAuditPage from "@/pages/ai-audit-page";
import TASIntegrationPage from "@/pages/tas-integration-page";
import PatternSharingPage from "@/pages/pattern-sharing-page";
import MedicalTestingPage from "@/pages/medical-testing-page";
import DocumentationPage from "@/pages/documentation-page";
import DimensionalBoundaryPage from "@/pages/dimensional-boundary-page";
import TreeVisualizationPage from "@/pages/tree-visualization-page";
import AvfPage from "@/pages/avf-page";
import TarsiPilotProgram from "@/pages/tarsi-pilot-program";
import SovereignTerminal from "@/pages/sovereign-terminal";
import BetweenTeaser from "@/pages/between-teaser";
import Header from "@/components/header";
import Footer from "@/components/footer";

import { ThemeProvider } from "@/components/ui/theme-provider";
import { TooltipProvider } from "@/components/ui/tooltip";

export default function App() {
  // For REPLIT compatibility, we'll force immediate show of content
  // rather than waiting for network initialization
  const [initialized, setInitialized] = React.useState(true);

  // Still try to initialize BASE_API_URL in background
  React.useEffect(() => {
    // Set BASE_API_URL to empty string (relative paths) if not set already
    if (!window.BASE_API_URL) {
      window.BASE_API_URL = '';
      console.log("Using relative paths for API requests by default");
    }
    
    // Try to ping the health endpoint to verify connectivity
    const checkApiHealth = async () => {
      try {
        const response = await fetch('/api/health');
        if (response.ok) {
          console.log("API health check successful!");
        }
      } catch (error) {
        console.warn("API health check failed:", error);
      }
    };
    
    checkApiHealth();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="system" storageKey="truealpha-theme">
        <TooltipProvider>
          <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-grow">
              {initialized ? (
                <Switch>
                  <Route path="/" component={HomePage} />
                  <Route path="/pricing" component={PricingPage} />
                  <Route path="/cross-reference-demo" component={CrossReferenceDemo} />
                  {/* These routes will be implemented individually */}
                  <Route path="/ai-audit" component={AiAuditPage} />
                  <Route path="/tas-integration" component={TASIntegrationPage} />
                  <Route path="/pattern-sharing" component={PatternSharingPage} />
                  <Route path="/medical-testing" component={MedicalTestingPage} />
                  <Route path="/resource-allocation">
                    <div className="container py-10">
                      <h1 className="text-3xl font-bold mb-4">Resource Allocation</h1>
                      <p className="text-muted-foreground">
                        Decentralized resource management for global computing networks with blockchain verification.
                      </p>
                      <p className="mt-4">
                        Implementation page coming soon. The backend implementation is complete in resource_allocation_implementation.py.
                      </p>
                    </div>
                  </Route>
                  <Route path="/ethical-ai">
                    <div className="container py-10">
                      <h1 className="text-3xl font-bold mb-4">Ethical AI Development</h1>
                      <p className="text-muted-foreground">
                        Guide AI model training with ethical constraints, fairness enforcement, and improvement recommendations.
                      </p>
                      <p className="mt-4">
                        Implementation page coming soon. The backend implementation is complete in ethical_ai_implementation.py.
                      </p>
                    </div>
                  </Route>
                  <Route path="/ip-protection">
                    <div className="container py-10">
                      <h1 className="text-3xl font-bold mb-4">IP Protection</h1>
                      <p className="text-muted-foreground">
                        Secure authorship of AI systems and algorithms through cryptographic verification and blockchain registration.
                      </p>
                      <p className="mt-4">
                        Implementation page coming soon. The backend implementation is complete in ip_protection_implementation.py.
                      </p>
                    </div>
                  </Route>
                  <Route path="/verification">
                    <div className="container py-10">
                      <h1 className="text-3xl font-bold mb-4">Verification System</h1>
                      <p className="text-muted-foreground">
                        Cryptographic verification and blockchain registration for all TrueAlpha Spiral operations and artifacts.
                      </p>
                      <p className="mt-4">
                        Verification system page coming soon. The implementation is built into all domain-specific modules.
                      </p>
                    </div>
                  </Route>
                  <Route path="/about">
                    <div className="container py-10">
                      <h1 className="text-3xl font-bold mb-4">About Enterprise AI Auditing Solution</h1>
                      <p className="text-muted-foreground">
                        The Enterprise AI Auditing Solution provides enterprise-grade verification of AI systems through 
                        cross-referenced validation, comprehensive regulatory compliance checking, and quantifiable risk metrics.
                      </p>
                      <p className="mt-4">
                        The platform offers 40-60% reduction in false positives through multi-source verification while supporting 
                        various regulatory frameworks for financial, healthcare, and government sectors.
                      </p>
                    </div>
                  </Route>
                  <Route path="/documentation" component={DocumentationPage} />
                  <Route path="/dimensional-boundary" component={DimensionalBoundaryPage} />
                  <Route path="/tree-visualization" component={TreeVisualizationPage} />
                  <Route path="/akashic-vibe-function" component={AvfPage} />
                  <Route path="/tarsi-pilot-program" component={TarsiPilotProgram} />
                  <Route path="/sovereign-terminal" component={SovereignTerminal} />
                  <Route path="/between" component={BetweenTeaser} />
                  <Route path="/pre-release" component={BetweenTeaser} />
                  <Route>
                    <div className="container py-10">
                      <h1 className="text-3xl font-bold mb-4">404 - Page Not Found</h1>
                      <p className="text-muted-foreground">
                        The page you are looking for does not exist.
                      </p>
                    </div>
                  </Route>
                </Switch>
              ) : (
                <div className="container py-10 flex items-center justify-center">
                  <div className="text-center">
                    <h2 className="text-2xl font-semibold mb-4">Initializing Enterprise AI Auditing Solution...</h2>
                    <p className="text-muted-foreground">Establishing connection to server...</p>
                  </div>
                </div>
              )}
            </main>
            <Footer />
            <Toaster />
          </div>
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}