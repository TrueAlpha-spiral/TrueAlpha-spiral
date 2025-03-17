import React from 'react';
import { Link } from 'wouter';
import { ShieldCheck, AlertTriangle, BarChart4, Check } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import VerificationForm from '@/components/verification-form';

interface SystemStatus {
  status: string;
  version: string;
  components: Record<string, string>;
  lastUpdated: string;
}

function HomePage() {
  // Fetch system status
  const { data: systemStatus, isLoading: systemStatusLoading } = useQuery<SystemStatus>({
    queryKey: ['/api/python-system/status'],
  });

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white py-24">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-12">
            <div className="md:w-1/2 space-y-6">
              <div className="inline-block px-3 py-1 bg-white/20 rounded-full text-sm font-medium mb-2">
                NEW: Cross-Reference Verification Technology
              </div>
              <h1 className="text-4xl md:text-5xl font-bold leading-tight">
                AI Content Verification with Multi-Source Cross-Referencing
              </h1>
              <p className="text-xl">
                Our advanced verification engine now features cross-reference technology that compares results across multiple verification methods for superior accuracy and reliability.
              </p>
              <div className="flex flex-wrap gap-3">
                <Link href="/cross-reference-demo" className="bg-white text-purple-700 hover:bg-purple-50 transition-colors px-6 py-3 rounded-lg font-medium">
                  Try Cross-Reference Demo
                </Link>
                <Link href="#verify" className="bg-transparent border border-white text-white hover:bg-white/10 transition-colors px-6 py-3 rounded-lg font-medium">
                  Basic Verification
                </Link>
              </div>
              <div className="flex items-center text-sm">
                <Check className="text-green-300 h-4 w-4 mr-2" />
                <span>No credit card required for trial</span>
                <span className="mx-2">•</span>
                <Check className="text-green-300 h-4 w-4 mr-2" />
                <span>Enterprise-ready API</span>
                <span className="mx-2">•</span>
                <Check className="text-green-300 h-4 w-4 mr-2" />
                <span>14-day money back</span>
              </div>
            </div>
            <div className="md:w-1/2">
              <div className="relative bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20">
                <div className="absolute -top-3 -right-3 bg-green-500 text-white text-xs px-3 py-1 rounded-full font-medium">
                  System Online
                </div>
                <h3 className="text-xl font-semibold mb-3">System Status</h3>
                {systemStatusLoading ? (
                  <p>Loading system status...</p>
                ) : (
                  <div className="space-y-3">
                    {systemStatus?.components && Object.entries(systemStatus.components).map(([key, value]) => (
                      <div key={key} className="flex items-center gap-2">
                        {value === 'active' ? (
                          <Check className="text-green-400 h-5 w-5" />
                        ) : (
                          <AlertTriangle className="text-amber-400 h-5 w-5" />
                        )}
                        <span className="capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                        <span className="text-xs bg-white/20 px-2 py-0.5 rounded ml-auto">
                          {value}
                        </span>
                      </div>
                    ))}
                    <div className="text-xs text-white/70 mt-2">
                      Last Updated: {systemStatus?.lastUpdated && new Date(systemStatus.lastUpdated).toLocaleTimeString()}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Key Capabilities</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card rounded-xl p-6 shadow-sm border border-primary/50 ring-1 ring-primary/10">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4 relative">
                <div className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-0.5 rounded-full font-medium">
                  New
                </div>
                <ShieldCheck className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Cross-Reference Verification</h3>
              <p className="text-muted-foreground">
                Compare verification results across multiple methods to improve accuracy and detect discrepancies for enhanced reliability.
              </p>
            </div>
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <AlertTriangle className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Speculative Content Flagging</h3>
              <p className="text-muted-foreground">
                Highlight speculative claims and statements that lack proper verification or citation.
              </p>
            </div>
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <BarChart4 className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Truth Confidence Scoring</h3>
              <p className="text-muted-foreground">
                Receive detailed confidence scores and analysis of content factuality with visual highlighting.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Verification Section */}
      <section id="verify" className="py-16 bg-gray-50 dark:bg-gray-900/30">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-4">Verify Content</h2>
            <p className="text-center text-muted-foreground mb-8">
              Paste any text to verify its factuality using the TrueAlphaSpiral verification engine.
            </p>
            <VerificationForm />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">How AI Content Verification Works</h2>
          <p className="text-center text-muted-foreground mb-12 max-w-2xl mx-auto">
            Our verification engine uses advanced algorithms to analyze content integrity and factuality.
          </p>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <span className="text-xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Multi-Method Analysis</h3>
              <p className="text-muted-foreground">
                Content is analyzed using multiple verification methods, including pattern matching, known facts checking, and cross-source verification.
              </p>
            </div>
            
            <div className="bg-card rounded-xl p-6 shadow-sm border border-primary/50 ring-1 ring-primary/10">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <span className="text-xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Cross-Reference Validation</h3>
              <p className="text-muted-foreground">
                Verification results are cross-referenced across methods to identify discrepancies and consistencies, enhancing overall reliability.
              </p>
              <div className="text-xs text-white mt-2 px-2 py-1 bg-green-500 rounded-md inline-block">New Feature</div>
            </div>
            
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <span className="text-xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Comprehensive Reporting</h3>
              <p className="text-muted-foreground">
                Detailed reports include verification results, cross-reference analysis, risk assessments, and regulatory compliance evaluation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to safeguard your content integrity?</h2>
          <p className="max-w-2xl mx-auto mb-8">
            Choose the plan that fits your organization's needs. From small teams to enterprise solutions, 
            we have pricing options that scale with your verification requirements.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button variant="outline" asChild>
              <Link href="#verify">Basic Verification</Link>
            </Button>
            <Button variant="default" className="bg-white text-primary hover:bg-white/90" asChild>
              <Link href="/cross-reference-demo">Try Cross-Reference Demo</Link>
            </Button>
          </div>
          <p className="mt-6 text-sm max-w-lg mx-auto">
            Start verifying your content today with our advanced AI auditing technology
          </p>
        </div>
      </section>
    </div>
  );
}

export default HomePage;

// Button component for the links (since we didn't import the Button component)
function Button({ 
  children, 
  variant = 'default', 
  className = '', 
  asChild = false
}: { 
  children: React.ReactNode; 
  variant?: 'default' | 'outline'; 
  className?: string; 
  asChild?: boolean;
}) {
  const baseStyles = "px-6 py-3 rounded-lg font-medium transition-colors";
  const variantStyles = {
    default: "bg-primary text-primary-foreground hover:bg-primary/90",
    outline: "border border-primary/20 bg-transparent hover:bg-primary/10"
  };
  
  const buttonClassName = `${baseStyles} ${variantStyles[variant]} ${className}`;
  
  return asChild ? (
    <span className={buttonClassName}>{children}</span>
  ) : (
    <button className={buttonClassName}>{children}</button>
  );
}