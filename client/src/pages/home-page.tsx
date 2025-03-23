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
      <section className="bg-gradient-to-r from-blue-700 to-blue-900 text-white py-24">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-12">
            <div className="md:w-1/2 space-y-6">
              <div className="inline-block px-3 py-1 bg-white/20 rounded-full text-sm font-medium mb-2">
                ENTERPRISE-GRADE: 40-60% Reduction in False Positives
              </div>
              <h1 className="text-4xl md:text-5xl font-bold leading-tight">
                TrueAlphaSpiral AI Auditing Solution with Cross-Reference Technology
              </h1>
              <p className="text-xl">
                Our advanced auditing platform features cross-reference technology that verifies AI outputs across multiple regulatory frameworks for superior compliance and risk assessment.
              </p>
              <div className="flex flex-wrap gap-3">
                <Link href="/cross-reference-demo" className="bg-white text-blue-700 hover:bg-blue-50 transition-colors px-6 py-3 rounded-lg font-medium">
                  View Cross-Reference Demo
                </Link>
                <Link href="#verify" className="bg-transparent border border-white text-white hover:bg-white/10 transition-colors px-6 py-3 rounded-lg font-medium">
                  Request Enterprise Demo
                </Link>
              </div>
              <div className="flex flex-wrap items-center text-sm">
                <Check className="text-green-300 h-4 w-4 mr-2" />
                <span>Financial Sector Compliance</span>
                <span className="mx-2">•</span>
                <Check className="text-green-300 h-4 w-4 mr-2" />
                <span>Healthcare AI Frameworks</span>
                <span className="mx-2">•</span>
                <Check className="text-green-300 h-4 w-4 mr-2" />
                <span>Government Regulatory Standards</span>
              </div>
            </div>
            <div className="md:w-1/2">
              <div className="relative bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20">
                <div className="absolute -top-3 -right-3 bg-green-500 text-white text-xs px-3 py-1 rounded-full font-medium">
                  Systems Online
                </div>
                <h3 className="text-xl font-semibold mb-3">Platform Status</h3>
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
          <h2 className="text-3xl font-bold text-center mb-12">Enterprise AI Auditing Capabilities</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card rounded-xl p-6 shadow-sm border border-primary/50 ring-1 ring-primary/10">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4 relative">
                <div className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-0.5 rounded-full font-medium">
                  New
                </div>
                <ShieldCheck className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Multi-Framework Compliance</h3>
              <p className="text-muted-foreground">
                Automatically audit AI systems against multiple regulatory frameworks including financial, healthcare, and government standards.
              </p>
            </div>
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <AlertTriangle className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Risk Assessment Dashboard</h3>
              <p className="text-muted-foreground">
                Comprehensive risk metrics with quantifiable measurements for AI outputs, error rates, and compliance gaps across enterprise systems.
              </p>
            </div>
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4 relative">
                <div className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-0.5 rounded-full font-medium">
                  New
                </div>
                <BarChart4 className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">False Positive Reduction</h3>
              <p className="text-muted-foreground">
                Reduce false positives by 40-60% through our advanced cross-reference verification technology with multi-source validation.
              </p>
              <div className="mt-4">
                <Link href="/tree-visualization" className="text-primary hover:text-primary/80 text-sm font-medium inline-flex items-center">
                  View Tree of Living Intelligence
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Verification Section */}
      <section id="verify" className="py-16 bg-gray-50 dark:bg-gray-900/30">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-4">Enterprise AI Audit Request</h2>
            <p className="text-center text-muted-foreground mb-8">
              Request a comprehensive AI audit for your enterprise systems using TrueAlphaSpiral's advanced cross-reference verification technology.
            </p>
            <VerificationForm />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">Enterprise AI Auditing Methodology</h2>
          <p className="text-center text-muted-foreground mb-12 max-w-2xl mx-auto">
            Our auditing platform uses enterprise-grade verification technology to ensure AI regulatory compliance across multiple frameworks.
          </p>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <span className="text-xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Multi-Framework Evaluation</h3>
              <p className="text-muted-foreground">
                AI systems are evaluated against multiple regulatory frameworks simultaneously, including FINRA, HIPAA, and FedRAMP requirements.
              </p>
            </div>
            
            <div className="bg-card rounded-xl p-6 shadow-sm border border-primary/50 ring-1 ring-primary/10">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <span className="text-xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Cross-Reference Verification</h3>
              <p className="text-muted-foreground">
                Results from multiple auditing methods are cross-referenced to significantly reduce false positives (40-60% reduction) and ensure compliance.
              </p>
              <div className="text-xs text-white mt-2 px-2 py-1 bg-green-500 rounded-md inline-block">Enterprise Feature</div>
            </div>
            
            <div className="bg-card rounded-xl p-6 shadow-sm border">
              <div className="bg-primary/10 p-3 rounded-lg w-fit mb-4">
                <span className="text-xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Quantifiable Risk Assessment</h3>
              <p className="text-muted-foreground">
                Comprehensive reports with quantifiable risk metrics enable enterprise customers to precisely assess AI compliance and operational risks.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-blue-800 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to ensure AI compliance across your enterprise?</h2>
          <p className="max-w-2xl mx-auto mb-8">
            TrueAlphaSpiral offers tailored enterprise solutions for comprehensive AI auditing and compliance. 
            Our platform scales with your organization's regulatory requirements across all sectors.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button variant="outline" asChild>
              <Link href="#verify">Request Enterprise Demo</Link>
            </Button>
            <Button variant="default" className="bg-white text-blue-800 hover:bg-white/90" asChild>
              <Link href="/cross-reference-demo">View Cross-Reference Technology</Link>
            </Button>
          </div>
          <p className="mt-6 text-sm max-w-lg mx-auto">
            Implement enterprise-grade AI auditing with 40-60% reduction in false positives through our cross-reference technology
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