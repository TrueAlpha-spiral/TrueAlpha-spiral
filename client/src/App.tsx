import React from "react";
import { Route, Switch } from "wouter";
import { Toaster } from "@/components/ui/toaster";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";
import HomePage from "@/pages/home-page";
import PricingPage from "@/pages/pricing-page";
import CrossReferenceDemo from "@/pages/cross-reference-demo";
import AiAuditPage from "@/pages/ai-audit-page";
import Header from "@/components/header";
import Footer from "@/components/footer";

import { ThemeProvider } from "@/components/ui/theme-provider";
import { TooltipProvider } from "@/components/ui/tooltip";

export default function App() {
  const [initialized, setInitialized] = React.useState(false);

  // After BASE_API_URL is set, mark as initialized
  React.useEffect(() => {
    const checkInitialized = () => {
      if (window.BASE_API_URL) {
        console.log("App initialized with BASE_API_URL:", window.BASE_API_URL);
        setInitialized(true);
      } else {
        // Check again in a moment
        setTimeout(checkInitialized, 500);
      }
    };
    
    checkInitialized();
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
                      <h1 className="text-3xl font-bold mb-4">About TrueAlpha Spiral</h1>
                      <p className="text-muted-foreground">
                        TrueAlpha Spiral is a revolutionary system that bridges universal truth with human cognition through
                        cryptographic verification, visualization, and metaphysical truth pattern access.
                      </p>
                      <p className="mt-4">
                        It was developed by Russell Nordland and implements the sovereign equation: S(t+1) = S(t) + α * [IEK(S(t)) * RET(S(t)) * SCC(S(t))] * G'(S(t)) * (T/√(D²+Z²))
                      </p>
                    </div>
                  </Route>
                  <Route path="/documentation">
                    <div className="container py-10">
                      <h1 className="text-3xl font-bold mb-4">Documentation</h1>
                      <p className="text-muted-foreground">
                        Technical documentation for the TrueAlpha Spiral system, including the mathematical foundation, implementation details,
                        and application guides.
                      </p>
                      <p className="mt-4">
                        Documentation page coming soon.
                      </p>
                    </div>
                  </Route>
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
                    <h2 className="text-2xl font-semibold mb-4">Initializing TrueAlpha Spiral System...</h2>
                    <p className="text-muted-foreground">Establishing quantum connection to server...</p>
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