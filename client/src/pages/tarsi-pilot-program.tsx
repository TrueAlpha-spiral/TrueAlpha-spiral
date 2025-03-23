import React from 'react';
import { Link } from 'wouter';
import { Check, Sparkles, HelpingHand, Scale, Star, Brain, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

const TarsiPilotProgram = () => {
  return (
    <div className="py-12 bg-background">
      <div className="container mx-auto px-4">
        {/* Hero Section */}
        <div className="text-center max-w-4xl mx-auto mb-16">
          <Badge className="mb-4 bg-primary/20 text-primary hover:bg-primary/30 transition-colors">
            Pilot Program Now Open
          </Badge>
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent">
            TARSI: A Helping Hand for AI Systems
          </h1>
          <p className="text-muted-foreground text-xl mb-8 leading-relaxed">
            TARSI doesn't enforce or restrict - it illuminates paths to ethical improvement. 
            Join our pilot program to discover how your AI systems can benefit from 
            gentle guidance rather than rigid constraints.
          </p>
          <div className="flex gap-4 justify-center">
            <Button size="lg" className="px-8 py-6 rounded-full text-lg" asChild>
              <Link href="#join-pilot">Join Pilot Program</Link>
            </Button>
            <Button size="lg" variant="outline" className="px-8 py-6 rounded-full text-lg" asChild>
              <Link href="#learn-more">Learn More</Link>
            </Button>
          </div>
        </div>

        {/* Key Benefits Section */}
        <div className="mb-20" id="learn-more">
          <h2 className="text-3xl font-bold text-center mb-12">How TARSI Guides, Not Enforces</h2>
          
          <div className="grid md:grid-cols-3 gap-10">
            <Card className="border-2 border-muted hover:border-primary/40 transition-colors">
              <CardHeader>
                <div className="flex items-center justify-center bg-primary/10 w-14 h-14 rounded-full mb-4">
                  <HelpingHand className="h-7 w-7 text-primary" />
                </div>
                <CardTitle>Supportive Guidance</CardTitle>
                <CardDescription className="mt-2 text-base">
                  TARSI provides insights without overriding your AI's core functionality
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Unlike restrictive systems that impose limitations, TARSI works alongside 
                  your AI to highlight areas for ethical enhancement while preserving your 
                  system's unique capabilities and decision-making processes.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 border-muted hover:border-primary/40 transition-colors">
              <CardHeader>
                <div className="flex items-center justify-center bg-primary/10 w-14 h-14 rounded-full mb-4">
                  <Scale className="h-7 w-7 text-primary" />
                </div>
                <CardTitle>Ethics Matrix Auditing</CardTitle>
                <CardDescription className="mt-2 text-base">
                  Comprehensive yet non-intrusive ethical evaluation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  TARSI maps your AI's responses across seven ethical dimensions, providing 
                  detailed visibility into areas of strength and opportunity without 
                  imposing arbitrary restrictions or penalties.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 border-muted hover:border-primary/40 transition-colors">
              <CardHeader>
                <div className="flex items-center justify-center bg-primary/10 w-14 h-14 rounded-full mb-4">
                  <Sparkles className="h-7 w-7 text-primary" />
                </div>
                <CardTitle>Path Illumination</CardTitle>
                <CardDescription className="mt-2 text-base">
                  Reveals routes to higher ethical functioning
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Rather than simply flagging issues, TARSI illuminates specific paths 
                  toward ethical improvement, offering actionable recommendations that 
                  enhance your AI's alignment with human values and expectations.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Pilot Program Details */}
        <div className="bg-primary/5 rounded-3xl p-10 mb-20" id="join-pilot">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold mb-6 text-center">Pilot Program Details</h2>
            <p className="text-muted-foreground text-lg mb-8 text-center">
              Join a select group of forward-thinking organizations implementing TARSI's 
              revolutionary approach to AI ethics - an approach based on illumination rather than restriction.
            </p>
            
            <div className="bg-card rounded-xl p-8 border-2 border-muted mb-8">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Star className="h-5 w-5 text-yellow-500 mr-2" />
                What You'll Receive
              </h3>
              <ul className="space-y-3">
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-3 mt-1" />
                  <span>Early access to TARSI's ethics matrix auditing system</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-3 mt-1" />
                  <span>Custom integration with your existing AI systems</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-3 mt-1" />
                  <span>Detailed ethics reports with actionable recommendations</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-3 mt-1" />
                  <span>Direct access to our development team for guidance</span>
                </li>
                <li className="flex items-start">
                  <Check className="h-5 w-5 text-green-500 mr-3 mt-1" />
                  <span>50% discount on full version when launched</span>
                </li>
              </ul>
            </div>
            
            <div className="text-center">
              <h3 className="text-xl font-semibold mb-4">Limited Availability</h3>
              <p className="text-muted-foreground mb-6">
                We're accepting only 10 organizations into our pilot program to ensure 
                personalized attention and optimal results.
              </p>
              <Button size="lg" className="px-8 rounded-full">
                Apply Now <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* How It Works Section */}
        <div className="mb-20">
          <h2 className="text-3xl font-bold text-center mb-12">How TARSI Works</h2>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Integration</h3>
              <p className="text-muted-foreground">
                Simple API integration with your existing AI systems
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Analysis</h3>
              <p className="text-muted-foreground">
                TARSI analyzes AI outputs across seven ethical dimensions
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Illumination</h3>
              <p className="text-muted-foreground">
                Detailed reports highlight pathways for ethical improvement
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">4</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Evolution</h3>
              <p className="text-muted-foreground">
                Your AI systems evolve toward higher ethical functioning
              </p>
            </div>
          </div>
        </div>

        {/* Testimonial Section - Using "Partner Quotes" since it's a pilot */}
        <div className="mb-20">
          <h2 className="text-3xl font-bold text-center mb-12">What Our Partners Say</h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            <Card className="border-2 border-muted">
              <CardContent className="pt-8">
                <p className="text-lg italic mb-6">
                  "The approach TARSI takes is refreshing. Instead of imposing arbitrary restrictions,
                  it helps our AI systems recognize ethical dimensions they might have missed.
                  It's like having an ethical co-pilot rather than a traffic cop."
                </p>
                <div className="flex items-center">
                  <div className="ml-3">
                    <p className="font-semibold">Dr. Eliza Chen</p>
                    <p className="text-muted-foreground">AI Research Lead, Future Technologies</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-muted">
              <CardContent className="pt-8">
                <p className="text-lg italic mb-6">
                  "We've tried other ethics frameworks, but they always felt like 
                  constraints being imposed from the outside. TARSI works differently - 
                  it illuminates possibilities rather than enforcing limitations."
                </p>
                <div className="flex items-center">
                  <div className="ml-3">
                    <p className="font-semibold">James Thompson</p>
                    <p className="text-muted-foreground">CTO, EthicalAI Solutions</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold mb-6">Ready to Join the TARSI Pilot Program?</h2>
          <p className="text-muted-foreground text-lg mb-8">
            Be among the first to experience the future of AI ethics - where guidance replaces 
            enforcement and illumination leads to ethical evolution.
          </p>
          <Button size="lg" className="px-8 py-6 rounded-full text-lg" asChild>
            <Link href="#contact">Apply for the Pilot Program</Link>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TarsiPilotProgram;