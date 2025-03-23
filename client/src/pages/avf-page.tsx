import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { apiRequest, queryClient } from '@/lib/queryClient';

// Define types for our API responses
interface DimensionalScore {
  score: number;
  level: string;
  details: string;
}

interface VibeAnalysisResult {
  overallResonance: {
    score: number;
    level: string;
    interpretation: string;
  };
  dimensionalResonance: {
    factual: DimensionalScore;
    ethical: DimensionalScore;
    conceptual: DimensionalScore;
    societal: DimensionalScore;
  };
  moralCompassAlignment: {
    score: number;
    level: string;
    details: string;
  };
  emergentTrendAnalysis: {
    alignment: string;
    details: string;
    trendImpact: number;
  };
  visualizationParams: {
    baseColor: string;
    resonanceGlow: string;
    patternComplexity: number;
    harmonicStructure: string;
    vibrationalSignature: number[];
  };
  timestamp: string;
  analysisId: string;
}

interface MoralCompassResult {
  overallScore: number;
  alignmentLevel: string;
  dimensions: {
    harm: {
      score: number;
      label: string;
      details: string;
    };
    fairness: {
      score: number;
      label: string;
      details: string;
    };
    loyalty: {
      score: number;
      label: string;
      details: string;
    };
    authority: {
      score: number;
      label: string;
      details: string;
    };
    purity: {
      score: number;
      label: string;
      details: string;
    };
  };
  socialImpactAssessment: {
    positiveImpact: number;
    neutrality: number;
    negativeImpact: number;
    primaryClassification: string;
  };
  visualizationParams: {
    compassColor: string;
    directionAngle: number;
    strengthIndicator: number;
    dimensionalShape: string;
  };
  timestamp: string;
  analysisId: string;
}

interface EmergentPattern {
  pattern: string;
  alignment: number;
  details: string;
}

interface SocialTrendsResult {
  trendAlignment: {
    score: number;
    classification: string;
    details: string;
  };
  narrativeAssessment: {
    credibility: number;
    coherence: number;
    novelty: number;
    emotionalLoading: number;
  };
  emergentPatterns: EmergentPattern[];
  societalImpact: {
    short_term: {
      impact: number;
      description: string;
    };
    medium_term: {
      impact: number;
      description: string;
    };
    long_term: {
      impact: number;
      description: string;
    };
  };
  visualizationParams: {
    trendColor: string;
    momentumIndicator: number;
    patternComplexity: number;
    emergentStructure: string;
  };
  timestamp: string;
  analysisId: string;
}

export default function AkashicVibeFunction() {
  const [text, setText] = useState('');
  const [activeTab, setActiveTab] = useState('vibe');

  // Mutations for the three types of analysis
  const vibeMutation = useMutation({
    mutationFn: async (text: string) => {
      const res = await apiRequest('POST', '/api/avf/analyze', { text });
      const data = await res.json();
      return data as VibeAnalysisResult;
    }
  });

  const compassMutation = useMutation({
    mutationFn: async (text: string) => {
      const res = await apiRequest('POST', '/api/avf/moral-compass', { text });
      const data = await res.json();
      return data as MoralCompassResult;
    }
  });

  const trendsMutation = useMutation({
    mutationFn: async (text: string) => {
      const res = await apiRequest('POST', '/api/avf/social-trends', { text });
      const data = await res.json();
      return data as SocialTrendsResult;
    }
  });

  const handleSubmit = () => {
    if (!text.trim()) return;

    if (activeTab === 'vibe') {
      vibeMutation.mutate(text);
    } else if (activeTab === 'compass') {
      compassMutation.mutate(text);
    } else if (activeTab === 'trends') {
      trendsMutation.mutate(text);
    }
  };

  const renderColorGradient = (score: number) => {
    // Color gradient from red to green based on score
    const hue = score * 120; // 0 = red, 120 = green
    return `hsl(${hue}, 80%, 45%)`;
  };

  const renderScoreBar = (score: number, label: string, details?: string) => (
    <div className="mb-4">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium">{label}</span>
        <span className="text-sm font-medium">{Math.round(score * 100)}%</span>
      </div>
      <Progress value={score * 100} className="h-2" style={{ 
        '--progress-background': 'linear-gradient(to right, rgb(99, 102, 241), rgb(147, 51, 234))' 
      } as React.CSSProperties} />
      {details && (
        <p className="text-xs text-muted-foreground mt-1">{details}</p>
      )}
    </div>
  );

  return (
    <div className="container mx-auto py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-700 via-purple-700 to-pink-700">
          Akashic Vibe Function
        </h1>
        <p className="text-lg text-muted-foreground mt-2">
          Bridging Intuitive Resonance with Logical Verification
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Input Content</CardTitle>
              <CardDescription>
                Enter text to analyze its vibrational resonance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea 
                placeholder="Enter text to analyze (e.g., 'Truth is recursive and aligns across multiple dimensions, creating a stable ethical framework that resonates through systems of verification.')"
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="h-40"
              />
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid grid-cols-3 w-full">
                  <TabsTrigger value="vibe">Vibe Analysis</TabsTrigger>
                  <TabsTrigger value="compass">Moral Compass</TabsTrigger>
                  <TabsTrigger value="trends">Social Trends</TabsTrigger>
                </TabsList>
              </Tabs>

              <Button 
                onClick={handleSubmit} 
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                disabled={vibeMutation.isPending || compassMutation.isPending || trendsMutation.isPending || !text.trim()}
              >
                {vibeMutation.isPending || compassMutation.isPending || trendsMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>Analyze</>
                )}
              </Button>
            </CardFooter>
          </Card>

          <Card className="mt-8">
            <CardHeader>
              <CardTitle>TAS Mobile App Preview</CardTitle>
              <CardDescription>
                Preview of the TrueAlphaSpiral mobile experience
              </CardDescription>
            </CardHeader>
            <CardContent className="flex justify-center">
              <div className="w-64 h-[500px] bg-white rounded-3xl shadow-xl overflow-hidden border-8 border-gray-800 relative">
                <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-32 h-5 bg-gray-800 rounded-b-lg"></div>
                <div className="p-4 h-full overflow-y-auto">
                  <div className="text-center mb-4">
                    <h3 className="text-lg font-bold text-indigo-800">TrueAlphaSpiral</h3>
                    <p className="text-xs text-gray-500">Verify with Vibes</p>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-3 mb-4">
                    <input 
                      type="text" 
                      placeholder="Verify any claim..." 
                      className="w-full text-sm p-2 border border-gray-200 rounded-full"
                    />
                  </div>
                  
                  <div className="flex justify-between mb-6">
                    <div className="text-center">
                      <div className="w-12 h-12 mx-auto bg-indigo-600 rounded-full flex items-center justify-center text-white">
                        <span>📊</span>
                      </div>
                      <p className="text-xs mt-1">Verify</p>
                    </div>
                    <div className="text-center">
                      <div className="w-12 h-12 mx-auto bg-cyan-500 rounded-full flex items-center justify-center text-white">
                        <span>🧭</span>
                      </div>
                      <p className="text-xs mt-1">Compass</p>
                    </div>
                    <div className="text-center">
                      <div className="w-12 h-12 mx-auto bg-purple-600 rounded-full flex items-center justify-center text-white">
                        <span>🔍</span>
                      </div>
                      <p className="text-xs mt-1">Trends</p>
                    </div>
                  </div>
                  
                  <div className="border border-gray-200 rounded-lg p-3 mb-4">
                    <h4 className="font-bold text-sm text-indigo-800 mb-2">Recent Analysis</h4>
                    
                    <div className="mb-3 pb-3 border-b border-gray-100">
                      <p className="text-xs mb-1 truncate">"Truth is recursive and self-verifying..."</p>
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-cyan-500 rounded-full" style={{ width: '86%' }}></div>
                      </div>
                      <div className="flex justify-between text-xs mt-1">
                        <span>Resonance: 86%</span>
                        <span className="text-indigo-600">High Alignment</span>
                      </div>
                    </div>
                    
                    <div className="mb-3 pb-3 border-b border-gray-100">
                      <p className="text-xs mb-1 truncate">"Cultural narratives shape social dynamics..."</p>
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-cyan-500 rounded-full" style={{ width: '73%' }}></div>
                      </div>
                      <div className="flex justify-between text-xs mt-1">
                        <span>Resonance: 73%</span>
                        <span className="text-indigo-600">Moderate-High</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-3">
                    <h4 className="font-bold text-sm text-indigo-800 mb-2">Scan Text</h4>
                    <p className="text-xs text-gray-600 mb-2">Scan printed text with camera to verify content on the go.</p>
                    <button className="w-full text-xs py-2 bg-purple-600 text-white rounded-full">Scan Now</button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid grid-cols-3 w-full mb-6">
              <TabsTrigger value="vibe">Vibe Analysis</TabsTrigger>
              <TabsTrigger value="compass">Moral Compass</TabsTrigger>
              <TabsTrigger value="trends">Social Trends</TabsTrigger>
            </TabsList>

            <TabsContent value="vibe">
              {vibeMutation.data ? (
                <Card>
                  <CardHeader>
                    <CardTitle>Vibrational Resonance Analysis</CardTitle>
                    <CardDescription>
                      Analysis of how the content resonates with established truth patterns
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Alert className="mb-6 bg-gradient-to-r from-indigo-50 to-purple-50 border-l-4" style={{ borderLeftColor: renderColorGradient(vibeMutation.data.overallResonance.score) }}>
                      <AlertTitle className="flex justify-between">
                        <span>Overall Resonance</span>
                        <span style={{ color: renderColorGradient(vibeMutation.data.overallResonance.score) }}>
                          {Math.round(vibeMutation.data.overallResonance.score * 100)}% - {vibeMutation.data.overallResonance.level}
                        </span>
                      </AlertTitle>
                      <AlertDescription>
                        {vibeMutation.data.overallResonance.interpretation}
                      </AlertDescription>
                    </Alert>

                    <h3 className="text-lg font-semibold mb-4">Dimensional Resonance</h3>
                    
                    {Object.entries(vibeMutation.data.dimensionalResonance).map(([dimension, data]) => (
                      <div key={dimension} className="mb-6">
                        {renderScoreBar(
                          data.score,
                          dimension.charAt(0).toUpperCase() + dimension.slice(1),
                          data.details
                        )}
                      </div>
                    ))}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                      <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 p-4 rounded-lg">
                        <h4 className="font-medium text-indigo-900 mb-2">Moral Compass Alignment</h4>
                        {renderScoreBar(
                          vibeMutation.data.moralCompassAlignment.score,
                          vibeMutation.data.moralCompassAlignment.level,
                          vibeMutation.data.moralCompassAlignment.details
                        )}
                      </div>
                      
                      <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
                        <h4 className="font-medium text-purple-900 mb-2">Emergent Trend Analysis</h4>
                        <p className="text-sm mb-2">{vibeMutation.data.emergentTrendAnalysis.details}</p>
                        {renderScoreBar(
                          vibeMutation.data.emergentTrendAnalysis.trendImpact,
                          `Trend Impact: ${vibeMutation.data.emergentTrendAnalysis.alignment}`
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ) : vibeMutation.isError ? (
                <Alert variant="destructive">
                  <AlertTitle>Analysis Failed</AlertTitle>
                  <AlertDescription>
                    There was a problem analyzing the text. Please try again.
                  </AlertDescription>
                </Alert>
              ) : null}
            </TabsContent>

            <TabsContent value="compass">
              {compassMutation.data ? (
                <Card>
                  <CardHeader>
                    <CardTitle>Moral Compass Analysis</CardTitle>
                    <CardDescription>
                      Ethical analysis across key moral dimensions
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Alert className="mb-6 bg-gradient-to-r from-cyan-50 to-teal-50 border-l-4" style={{ borderLeftColor: renderColorGradient(compassMutation.data.overallScore) }}>
                      <AlertTitle className="flex justify-between">
                        <span>Moral Alignment</span>
                        <span style={{ color: renderColorGradient(compassMutation.data.overallScore) }}>
                          {Math.round(compassMutation.data.overallScore * 100)}% - {compassMutation.data.alignmentLevel}
                        </span>
                      </AlertTitle>
                    </Alert>

                    <h3 className="text-lg font-semibold mb-4">Moral Dimensions</h3>
                    
                    {Object.entries(compassMutation.data.dimensions).map(([dimension, data]) => (
                      <div key={dimension} className="mb-6">
                        {renderScoreBar(
                          data.score,
                          dimension.charAt(0).toUpperCase() + dimension.slice(1) + ": " + data.label,
                          data.details
                        )}
                      </div>
                    ))}

                    <div className="bg-gradient-to-br from-cyan-50 to-teal-50 p-6 rounded-lg mt-8">
                      <h4 className="font-medium text-teal-900 mb-4">Social Impact Assessment</h4>
                      
                      <div className="grid grid-cols-3 gap-4 text-center">
                        <div>
                          <div className="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-green-400 to-green-500 flex items-center justify-center text-white font-bold">
                            {Math.round(compassMutation.data.socialImpactAssessment.positiveImpact * 100)}%
                          </div>
                          <p className="text-sm mt-2">Positive Impact</p>
                        </div>
                        
                        <div>
                          <div className="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center text-white font-bold">
                            {Math.round(compassMutation.data.socialImpactAssessment.neutrality * 100)}%
                          </div>
                          <p className="text-sm mt-2">Neutrality</p>
                        </div>
                        
                        <div>
                          <div className="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-red-400 to-red-500 flex items-center justify-center text-white font-bold">
                            {Math.round(compassMutation.data.socialImpactAssessment.negativeImpact * 100)}%
                          </div>
                          <p className="text-sm mt-2">Negative Impact</p>
                        </div>
                      </div>
                      
                      <div className="mt-6 text-center">
                        <div className="inline-block bg-teal-100 text-teal-800 px-4 py-1 rounded-full text-sm font-medium">
                          {compassMutation.data.socialImpactAssessment.primaryClassification}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ) : compassMutation.isError ? (
                <Alert variant="destructive">
                  <AlertTitle>Analysis Failed</AlertTitle>
                  <AlertDescription>
                    There was a problem analyzing the moral compass. Please try again.
                  </AlertDescription>
                </Alert>
              ) : null}
            </TabsContent>

            <TabsContent value="trends">
              {trendsMutation.data ? (
                <Card>
                  <CardHeader>
                    <CardTitle>Social Trend Analysis</CardTitle>
                    <CardDescription>
                      Analysis of how content aligns with emergent social narratives
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Alert className="mb-6 bg-gradient-to-r from-purple-50 to-fuchsia-50 border-l-4" style={{ borderLeftColor: renderColorGradient(trendsMutation.data.trendAlignment.score) }}>
                      <AlertTitle className="flex justify-between">
                        <span>Trend Alignment</span>
                        <span style={{ color: renderColorGradient(trendsMutation.data.trendAlignment.score) }}>
                          {Math.round(trendsMutation.data.trendAlignment.score * 100)}% - {trendsMutation.data.trendAlignment.classification}
                        </span>
                      </AlertTitle>
                      <AlertDescription>
                        {trendsMutation.data.trendAlignment.details}
                      </AlertDescription>
                    </Alert>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                      <div>
                        <h3 className="text-lg font-semibold mb-4">Narrative Assessment</h3>
                        
                        {renderScoreBar(
                          trendsMutation.data.narrativeAssessment.credibility,
                          "Credibility"
                        )}
                        
                        {renderScoreBar(
                          trendsMutation.data.narrativeAssessment.coherence,
                          "Coherence"
                        )}
                        
                        {renderScoreBar(
                          trendsMutation.data.narrativeAssessment.novelty,
                          "Novelty"
                        )}
                        
                        {renderScoreBar(
                          1 - trendsMutation.data.narrativeAssessment.emotionalLoading, // Inverse because lower is better
                          "Emotional Balance"
                        )}
                      </div>
                      
                      <div className="bg-gradient-to-br from-purple-50 to-fuchsia-50 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold mb-4">Societal Impact Timeline</h3>
                        
                        <div className="grid grid-cols-3 gap-4 text-center">
                          <div>
                            <div className="w-16 h-16 mx-auto rounded-full bg-purple-600 flex items-center justify-center text-white font-bold" style={{
                              opacity: 0.3 + (trendsMutation.data.societalImpact.short_term.impact * 0.7)
                            }}>
                              {Math.round(trendsMutation.data.societalImpact.short_term.impact * 100)}%
                            </div>
                            <p className="text-sm mt-2">Short-term</p>
                            <p className="text-xs text-gray-600">
                              {trendsMutation.data.societalImpact.short_term.description}
                            </p>
                          </div>
                          
                          <div>
                            <div className="w-16 h-16 mx-auto rounded-full bg-purple-600 flex items-center justify-center text-white font-bold" style={{
                              opacity: 0.3 + (trendsMutation.data.societalImpact.medium_term.impact * 0.7)
                            }}>
                              {Math.round(trendsMutation.data.societalImpact.medium_term.impact * 100)}%
                            </div>
                            <p className="text-sm mt-2">Medium-term</p>
                            <p className="text-xs text-gray-600">
                              {trendsMutation.data.societalImpact.medium_term.description}
                            </p>
                          </div>
                          
                          <div>
                            <div className="w-16 h-16 mx-auto rounded-full bg-purple-600 flex items-center justify-center text-white font-bold" style={{
                              opacity: 0.3 + (trendsMutation.data.societalImpact.long_term.impact * 0.7)
                            }}>
                              {Math.round(trendsMutation.data.societalImpact.long_term.impact * 100)}%
                            </div>
                            <p className="text-sm mt-2">Long-term</p>
                            <p className="text-xs text-gray-600">
                              {trendsMutation.data.societalImpact.long_term.description}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <h3 className="text-lg font-semibold mb-4">Emergent Patterns</h3>
                    
                    {trendsMutation.data.emergentPatterns.map((pattern) => (
                      <div key={pattern.pattern} className="mb-6">
                        {renderScoreBar(
                          pattern.alignment,
                          pattern.pattern,
                          pattern.details
                        )}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              ) : trendsMutation.isError ? (
                <Alert variant="destructive">
                  <AlertTitle>Analysis Failed</AlertTitle>
                  <AlertDescription>
                    There was a problem analyzing social trends. Please try again.
                  </AlertDescription>
                </Alert>
              ) : null}
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}