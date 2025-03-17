import React from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { apiRequest } from '@/lib/queryClient';
import { ArrowLeft, Loader2, Info, AlertCircle, CheckCircle2, XCircle } from 'lucide-react';
import { Link } from 'wouter';

import { Button } from '@/components/ui/button';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import TextHighlighter from '@/components/ui/text-highlighter';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { VerificationResult, CrossReferenceResult } from '@shared/schema';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

// Cross-reference form schema
const crossReferenceFormSchema = z.object({
  content: z.string().min(10, 'Text must be at least 10 characters long').max(5000, 'Text cannot exceed 5,000 characters'),
  regulatoryFramework: z.enum(['general', 'financial_services', 'healthcare', 'government', 'education']),
});

type CrossReferenceFormValues = z.infer<typeof crossReferenceFormSchema>;

/**
 * Cross Reference Demo page that demonstrates the cross-reference verification feature
 */
function CrossReferenceDemo() {
  const [verificationResult, setVerificationResult] = React.useState<VerificationResult | null>(null);
  const [crossReferenceResult, setCrossReferenceResult] = React.useState<CrossReferenceResult | null>(null);
  const [completedAudit, setCompletedAudit] = React.useState<any | null>(null);

  // Define form
  const form = useForm<CrossReferenceFormValues>({
    resolver: zodResolver(crossReferenceFormSchema),
    defaultValues: {
      content: '',
      regulatoryFramework: 'general',
    },
  });

  // Define verification mutation
  const verifyMutation = useMutation({
    mutationFn: async (values: CrossReferenceFormValues) => {
      const response = await apiRequest('POST', '/api/cross-reference', {
        content: values.content,
        regulatoryFramework: values.regulatoryFramework
      });
      return await response.json();
    },
    onSuccess: (data) => {
      setVerificationResult(data.verificationResult);
      setCrossReferenceResult(data.crossReferenceResult);
    },
  });

  // Define audit mutation
  const auditMutation = useMutation({
    mutationFn: async (values: CrossReferenceFormValues) => {
      const response = await apiRequest('POST', '/api/ai-audit', {
        content: values.content,
        clientName: 'Demo Client',
        aiSystemName: 'Demo AI System',
        regulatoryFramework: values.regulatoryFramework,
        options: {
          includeCrossReference: true,
          generateRecommendations: true
        }
      });
      return await response.json();
    },
    onSuccess: (data) => {
      setCompletedAudit(data);
    },
  });

  // Handle form submission
  const onSubmit = (values: CrossReferenceFormValues) => {
    // Reset previous results
    setVerificationResult(null);
    setCrossReferenceResult(null);
    setCompletedAudit(null);
    
    // Call verification API
    verifyMutation.mutate(values);
  };

  // Handle full audit submission
  const runFullAudit = () => {
    const values = form.getValues();
    auditMutation.mutate(values);
  };

  // Get verification status badge
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'verified':
        return <Badge className="bg-green-500">Verified</Badge>;
      case 'requires_review':
        return <Badge className="bg-amber-500">Requires Review</Badge>;
      case 'rejected':
        return <Badge className="bg-red-500">Rejected</Badge>;
      default:
        return <Badge className="bg-gray-500">Unknown</Badge>;
    }
  };

  // Get score color
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500';
    if (score >= 0.6) return 'bg-amber-500';
    return 'bg-red-500';
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Link>
          </Button>
        </div>

        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-2">Cross-Reference Verification Demo</h1>
          <p className="text-muted-foreground mb-8">
            This demo demonstrates the cross-reference verification feature, which compares results from multiple verification methods to provide more accurate assessment of content factuality.
          </p>

          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Content Verification</CardTitle>
              <CardDescription>
                Enter content to verify across multiple verification methods
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                  <FormField
                    control={form.control}
                    name="content"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Content to Verify</FormLabel>
                        <FormControl>
                          <Textarea
                            placeholder="Enter text to verify for factuality..."
                            className="min-h-[200px] resize-y"
                            {...field}
                          />
                        </FormControl>
                        <FormDescription>
                          Enter text you want to verify using multiple verification methods.
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={form.control}
                    name="regulatoryFramework"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Regulatory Framework</FormLabel>
                        <Select 
                          onValueChange={field.onChange} 
                          defaultValue={field.value}
                        >
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select a regulatory framework" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="general">General</SelectItem>
                            <SelectItem value="financial_services">Financial Services</SelectItem>
                            <SelectItem value="healthcare">Healthcare</SelectItem>
                            <SelectItem value="government">Government</SelectItem>
                            <SelectItem value="education">Education</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormDescription>
                          Select the regulatory framework relevant to this content
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <Button
                    type="submit"
                    disabled={verifyMutation.isPending}
                    className="w-full sm:w-auto"
                  >
                    {verifyMutation.isPending ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Verifying...
                      </>
                    ) : (
                      'Verify Content'
                    )}
                  </Button>
                </form>
              </Form>
            </CardContent>
          </Card>

          {(verificationResult && crossReferenceResult) && (
            <Tabs defaultValue="cross-reference" className="space-y-6">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="cross-reference">Cross-Reference Results</TabsTrigger>
                <TabsTrigger value="verification-details">Verification Details</TabsTrigger>
              </TabsList>
              
              <TabsContent value="cross-reference" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span>Cross-Reference Analysis</span>
                      {getStatusBadge(crossReferenceResult.verificationStatus)}
                    </CardTitle>
                    <CardDescription>
                      Comparative analysis across multiple verification methods
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Confidence Score */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-sm">Confidence Score</h3>
                        <span className="text-sm font-medium">
                          {Math.round(crossReferenceResult.confidenceScore * 100)}%
                        </span>
                      </div>
                      <Progress value={crossReferenceResult.confidenceScore * 100} className={getScoreColor(crossReferenceResult.confidenceScore)} />
                      <p className="text-sm text-muted-foreground">
                        Overall confidence based on cross-reference verification
                      </p>
                    </div>
                    
                    {/* Reliability Score */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-sm">Reliability Score</h3>
                        <span className="text-sm font-medium">
                          {Math.round(crossReferenceResult.crossReferenceAnalysis.reliabilityScore * 100)}%
                        </span>
                      </div>
                      <Progress value={crossReferenceResult.crossReferenceAnalysis.reliabilityScore * 100} className={getScoreColor(crossReferenceResult.crossReferenceAnalysis.reliabilityScore)} />
                      <p className="text-sm text-muted-foreground">
                        Reliability of verification based on agreement between verification methods
                      </p>
                    </div>
                    
                    {/* Discrepancies */}
                    <Accordion type="single" collapsible className="w-full">
                      <AccordionItem value="discrepancies">
                        <AccordionTrigger className="font-semibold text-sm">
                          <div className="flex items-center">
                            <AlertCircle className="h-4 w-4 mr-2 text-amber-500" />
                            Discrepancies ({crossReferenceResult.crossReferenceAnalysis.discrepancies.length})
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          {crossReferenceResult.crossReferenceAnalysis.discrepancies.length > 0 ? (
                            <div className="space-y-4">
                              {crossReferenceResult.crossReferenceAnalysis.discrepancies.map((discrepancy, index) => (
                                <div key={index} className="border rounded-md p-3 bg-amber-50 dark:bg-amber-900/20">
                                  <p className="text-sm font-medium mb-2">
                                    {discrepancy.sentence}
                                  </p>
                                  <div className="text-xs text-muted-foreground grid grid-cols-2 gap-2">
                                    <div>
                                      <span className="font-medium">Results:</span> {discrepancy.assessments.map(a => a.type).join(', ')}
                                    </div>
                                    <div>
                                      <span className="font-medium">Recommendation:</span> {discrepancy.recommendation}
                                    </div>
                                  </div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <p className="text-sm text-muted-foreground">
                              No discrepancies found between verification methods.
                            </p>
                          )}
                        </AccordionContent>
                      </AccordionItem>
                      
                      <AccordionItem value="consistencies">
                        <AccordionTrigger className="font-semibold text-sm">
                          <div className="flex items-center">
                            <CheckCircle2 className="h-4 w-4 mr-2 text-green-500" />
                            Consistencies ({crossReferenceResult.crossReferenceAnalysis.consistencies.length})
                          </div>
                        </AccordionTrigger>
                        <AccordionContent>
                          {crossReferenceResult.crossReferenceAnalysis.consistencies.length > 0 ? (
                            <div className="space-y-4">
                              {crossReferenceResult.crossReferenceAnalysis.consistencies.map((consistency, index) => (
                                <div key={index} className="border rounded-md p-3 bg-green-50 dark:bg-green-900/20">
                                  <p className="text-sm font-medium mb-2">
                                    {consistency.sentence}
                                  </p>
                                  <div className="text-xs text-muted-foreground grid grid-cols-2 gap-2">
                                    <div>
                                      <span className="font-medium">Type:</span> {consistency.agreedType}
                                    </div>
                                    <div>
                                      <span className="font-medium">Sources:</span> {consistency.sources.join(', ')}
                                    </div>
                                  </div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <p className="text-sm text-muted-foreground">
                              No consistent verifications found between methods.
                            </p>
                          )}
                        </AccordionContent>
                      </AccordionItem>
                    </Accordion>
                    
                    {/* Verification Methods Comparison */}
                    <div className="space-y-2">
                      <h3 className="font-semibold text-sm">Verification Methods Comparison</h3>
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Metric</TableHead>
                            <TableHead>Primary Method</TableHead>
                            <TableHead>Secondary Method</TableHead>
                            <TableHead>Variance</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          <TableRow>
                            <TableCell>Truth Score</TableCell>
                            <TableCell>{Math.round(verificationResult.truthScore * 100)}%</TableCell>
                            <TableCell>{Math.round((1 - crossReferenceResult.crossReferenceAnalysis.scoreVariance) * 100)}%</TableCell>
                            <TableCell>
                              <Badge className={Math.abs(crossReferenceResult.crossReferenceAnalysis.scoreVariance) > 0.2 ? "bg-amber-500" : "bg-green-500"}>
                                {Math.abs(Math.round(crossReferenceResult.crossReferenceAnalysis.scoreVariance * 100))}%
                              </Badge>
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Verified Segments</TableCell>
                            <TableCell>{verificationResult.summary.factualCount}</TableCell>
                            <TableCell>{crossReferenceResult.crossReferenceAnalysis.consistencies.length}</TableCell>
                            <TableCell>
                              {Math.abs(verificationResult.summary.factualCount - crossReferenceResult.crossReferenceAnalysis.consistencies.length)}
                            </TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between border-t pt-6">
                    <Button variant="outline" disabled={!verificationResult} onClick={runFullAudit}>
                      {auditMutation.isPending ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Running...
                        </>
                      ) : (
                        'Run Full AI Audit'
                      )}
                    </Button>
                    <div className="text-xs text-muted-foreground">
                      Cross-reference verification completed
                    </div>
                  </CardFooter>
                </Card>
                
                {/* Full Audit Results */}
                {completedAudit && (
                  <Card>
                    <CardHeader>
                      <CardTitle>AI Audit Results</CardTitle>
                      <CardDescription>
                        Comprehensive AI audit with regulatory compliance assessment
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <Alert>
                        <Info className="h-4 w-4" />
                        <AlertTitle>Audit Summary</AlertTitle>
                        <AlertDescription>
                          {completedAudit.auditSummary}
                        </AlertDescription>
                      </Alert>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <h3 className="font-semibold text-sm">Risk Score</h3>
                          <Progress value={completedAudit.riskScore} className={
                            completedAudit.riskScore > 75 ? "bg-red-500" :
                            completedAudit.riskScore > 50 ? "bg-amber-500" :
                            "bg-green-500"
                          } />
                          <p className="text-sm text-muted-foreground">
                            {completedAudit.riskScore}/100
                          </p>
                        </div>
                        
                        <div className="space-y-2">
                          <h3 className="font-semibold text-sm">Compliance Score</h3>
                          <Progress value={completedAudit.complianceScore} className={
                            completedAudit.complianceScore > 75 ? "bg-green-500" :
                            completedAudit.complianceScore > 50 ? "bg-amber-500" :
                            "bg-red-500"
                          } />
                          <p className="text-sm text-muted-foreground">
                            {completedAudit.complianceScore}/100
                          </p>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <h3 className="font-semibold text-sm">Recommendations</h3>
                        <ul className="list-disc pl-5 space-y-1">
                          {completedAudit.recommendations.map((recommendation: string, index: number) => (
                            <li key={index} className="text-sm text-muted-foreground">
                              {recommendation}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>
              
              <TabsContent value="verification-details">
                <Card>
                  <CardHeader>
                    <CardTitle>Verification Details</CardTitle>
                    <CardDescription>
                      Detailed analysis of the content verification
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Score section */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-sm">Truth Score</h3>
                        <span className="text-sm font-medium">
                          {Math.round(verificationResult.truthScore * 100)}%
                        </span>
                      </div>
                      <Progress value={verificationResult.truthScore * 100} className={getScoreColor(verificationResult.truthScore)} />
                    </div>

                    {/* Summary section */}
                    <div className="space-y-2">
                      <h3 className="font-semibold text-sm">Summary</h3>
                      <div className="grid grid-cols-3 gap-2 text-center">
                        <div className="bg-green-100 dark:bg-green-900/30 rounded-md p-2">
                          <div className="font-semibold">{verificationResult.summary.factualCount}</div>
                          <div className="text-xs">Factual</div>
                        </div>
                        <div className="bg-amber-100 dark:bg-amber-900/30 rounded-md p-2">
                          <div className="font-semibold">{verificationResult.summary.speculativeCount}</div>
                          <div className="text-xs">Speculative</div>
                        </div>
                        <div className="bg-red-100 dark:bg-red-900/30 rounded-md p-2">
                          <div className="font-semibold">{verificationResult.summary.fabricatedCount}</div>
                          <div className="text-xs">Fabricated</div>
                        </div>
                      </div>
                    </div>

                    {/* Highlighted text */}
                    <div className="space-y-2">
                      <h3 className="font-semibold text-sm">Analyzed Content</h3>
                      <div className="border rounded-md p-4 bg-card">
                        <TextHighlighter 
                          text={verificationResult.originalText} 
                          highlights={verificationResult.highlights} 
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          )}
        </div>
      </div>
    </div>
  );
}

export default CrossReferenceDemo;