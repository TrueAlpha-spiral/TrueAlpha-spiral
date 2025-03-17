import React from 'react';
import { Link } from 'wouter';
import { Check, Shield, Database, Zap, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const PricingPage = () => {
  return (
    <div className="py-12 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-4xl font-bold mb-4">Pricing Plans</h1>
          <p className="text-muted-foreground text-lg">
            Choose the right plan for your AI truth verification needs.
            Protect your content, reputation, and audience with TrueAlphaSpiral.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Basic Plan */}
          <Card className="border-2 border-muted flex flex-col">
            <CardHeader>
              <div className="flex items-center justify-center bg-primary/10 w-12 h-12 rounded-full mb-4">
                <Shield className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Basic</CardTitle>
              <div className="mt-2">
                <span className="text-3xl font-bold">$29</span>
                <span className="text-muted-foreground">/month</span>
              </div>
              <CardDescription className="mt-2">
                Essential truth verification for individuals and small teams.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-grow">
              <ul className="space-y-3">
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>1,000 verifications per month</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Pattern-based detection</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Basic fact checking</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Email support</span>
                </li>
                <li className="flex items-start text-muted-foreground">
                  <AlertTriangle className="h-5 w-5 mr-2 mt-0.5" />
                  <span>No API access</span>
                </li>
                <li className="flex items-start text-muted-foreground">
                  <AlertTriangle className="h-5 w-5 mr-2 mt-0.5" />
                  <span>No custom patterns</span>
                </li>
              </ul>
            </CardContent>
            <CardFooter>
              <Button className="w-full" asChild>
                <Link href="#demo">Start Free Trial</Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Pro Plan */}
          <Card className="border-2 border-primary flex flex-col relative">
            <div className="absolute top-0 right-0 bg-primary text-primary-foreground text-xs font-medium px-3 py-1 rounded-bl-lg rounded-tr-lg">
              MOST POPULAR
            </div>
            <CardHeader>
              <div className="flex items-center justify-center bg-primary/10 w-12 h-12 rounded-full mb-4">
                <Zap className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Pro</CardTitle>
              <div className="mt-2">
                <span className="text-3xl font-bold">$99</span>
                <span className="text-muted-foreground">/month</span>
              </div>
              <CardDescription className="mt-2">
                Advanced verification for content teams and businesses.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-grow">
              <ul className="space-y-3">
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>10,000 verifications per month</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Advanced pattern detection</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Comprehensive fact checking</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>API access (REST)</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Custom patterns (up to 10)</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Priority email & chat support</span>
                </li>
              </ul>
            </CardContent>
            <CardFooter>
              <Button className="w-full bg-primary hover:bg-primary/90" asChild>
                <Link href="#demo">Start 14-Day Trial</Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Enterprise Plan */}
          <Card className="border-2 border-muted flex flex-col">
            <CardHeader>
              <div className="flex items-center justify-center bg-primary/10 w-12 h-12 rounded-full mb-4">
                <Database className="h-6 w-6 text-primary" />
              </div>
              <CardTitle>Enterprise</CardTitle>
              <div className="mt-2">
                <span className="text-3xl font-bold">Custom</span>
                <span className="text-muted-foreground"></span>
              </div>
              <CardDescription className="mt-2">
                Full-scale verification for organizations with high-volume needs.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-grow">
              <ul className="space-y-3">
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Unlimited verifications</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Custom AI model training</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Domain-specific fact database</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Advanced API (REST + GraphQL)</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Unlimited custom patterns</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>Dedicated account manager</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>SLA with 99.9% uptime</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-2 mt-0.5" />
                  <span>On-premise deployment option</span>
                </li>
              </ul>
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="w-full" asChild>
                <Link href="/contact">Contact Sales</Link>
              </Button>
            </CardFooter>
          </Card>
        </div>

        {/* FAQ Section */}
        <div className="mt-20 max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-8">Frequently Asked Questions</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">How accurate is the TrueAlphaSpiral verification engine?</h3>
              <p className="text-muted-foreground">
                TrueAlphaSpiral uses a multi-layered approach combining pattern detection, fact checking, and contextual analysis.
                Our system achieves 92%+ accuracy in identifying fabricated or speculative content, with continuous improvements
                as our fact database expands.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">Can I integrate TrueAlphaSpiral with my existing content management system?</h3>
              <p className="text-muted-foreground">
                Yes, Pro and Enterprise plans include API access that allows seamless integration with most content management
                systems, publishing platforms, and custom applications. We provide detailed documentation and integration support.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">What happens if I exceed my monthly verification limit?</h3>
              <p className="text-muted-foreground">
                If you reach your monthly verification limit, you'll have the option to upgrade to a higher tier or
                purchase additional verifications as needed. We'll notify you when you're approaching your limit.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">How is TrueAlphaSpiral different from other fact-checking services?</h3>
              <p className="text-muted-foreground">
                Unlike traditional fact-checking services that rely solely on databases, TrueAlphaSpiral combines
                quantum-inspired pattern detection with factual verification to identify speculative content, subtle fabrications,
                and unverified claims with greater precision and speed.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">Can I cancel my subscription at any time?</h3>
              <p className="text-muted-foreground">
                Yes, you can cancel your subscription at any time. Billing occurs monthly, and you'll maintain access until
                the end of your current billing period.
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <h2 className="text-2xl font-bold mb-4">Ready to protect your content integrity?</h2>
          <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
            Join leading organizations using TrueAlphaSpiral to verify content integrity, 
            detect AI fabrications, and build trust with their audience.
          </p>
          <div className="flex gap-4 justify-center">
            <Button asChild>
              <Link href="#demo">Try for Free</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/contact">Schedule Demo</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;