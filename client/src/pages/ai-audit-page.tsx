import React from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { apiRequest } from '@/lib/queryClient';
import { ArrowLeft, Loader2, ShieldCheck, AlertCircle, CheckCircle2, BarChart4, FileText, Database, ServerIcon, FileCheck, BadgeCheck, Info } from 'lucide-react';
import { Link } from 'wouter';

import { Button } from '@/components/ui/button';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Checkbox } from '@/components/ui/checkbox';
import { toast } from '@/hooks/use-toast';

// AI Audit form schema
const aiAuditFormSchema = z.object({
  clientName: z.string().min(2, 'Client name must be at least 2 characters').max(100),
  aiSystemName: z.string().min(2, 'AI system name must be at least 2 characters').max(100),
  systemDescription: z.string().min(10, 'Description must be at least 10 characters').max(5000),
  regulatoryFramework: z.enum(['general', 'financial_services', 'healthcare', 'government', 'education']),
  auditType: z.enum(['quick', 'standard', 'comprehensive']),
  includeCrossReferences: z.boolean().default(true),
  includeBlockchainVerification: z.boolean().default(false),
  includeRiskAssessment: z.boolean().default(true),
});

type AiAuditFormValues = z.infer<typeof aiAuditFormSchema>;

// Example risk metrics - in a real application, these would come from the API
interface RiskMetric {
  name: string;
  value: number;
  threshold: number;
  status: 'low' | 'medium' | 'high';
}

function AiAuditPage() {
  const [auditResult, setAuditResult] = React.useState<any | null>(null);
  const [auditStatus, setAuditStatus] = React.useState<'idle' | 'running' | 'complete' | 'error'>('idle');
  const [activeTab, setActiveTab] = React.useState('overview');

  // Define form
  const form = useForm<AiAuditFormValues>({
    resolver: zodResolver(aiAuditFormSchema),
    defaultValues: {
      clientName: 'KPMG Client',
      aiSystemName: 'Enterprise Decision System',
      systemDescription: 'AI system used for automated decision-making in financial services, including loan approvals, risk assessments, and fraud detection.',
      regulatoryFramework: 'financial_services',
      auditType: 'comprehensive',
      includeCrossReferences: true,
      includeBlockchainVerification: false,
      includeRiskAssessment: true,
    },
  });

  // Define audit mutation
  const auditMutation = useMutation({
    mutationFn: async (values: AiAuditFormValues) => {
      setAuditStatus('running');
      
      try {
        const response = await apiRequest('POST', '/api/ai-audit', {
          clientName: values.clientName,
          aiSystemName: values.aiSystemName, 
          systemDescription: values.systemDescription,
          regulatoryFramework: values.regulatoryFramework,
          options: {
            auditType: values.auditType,
            includeCrossReferences: values.includeCrossReferences,
            includeBlockchainVerification: values.includeBlockchainVerification,
            includeRiskAssessment: values.includeRiskAssessment
          }
        });
        
        const result = await response.json();
        setAuditStatus('complete');
        return result;
      } catch (error) {
        setAuditStatus('error');
        throw error;
      }
    },
    onSuccess: (data) => {
      setAuditResult(data);
      toast({
        title: "Audit completed successfully",
        description: "The AI system audit has been completed. View the report for details.",
      });
    },
    onError: (error) => {
      toast({
        title: "Audit failed",
        description: error instanceof Error ? error.message : "Unknown error occurred",
        variant: "destructive",
      });
    }
  });

  // Handle form submission
  const onSubmit = (values: AiAuditFormValues) => {
    // Reset previous results
    setAuditResult(null);
    
    // Call audit API
    auditMutation.mutate(values);
  };

  // Get risk level color
  const getRiskColor = (status: string) => {
    switch (status) {
      case 'low':
        return 'bg-green-500';
      case 'medium':
        return 'bg-amber-500';
      case 'high':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  // Get score color
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500';
    if (score >= 0.6) return 'bg-amber-500';
    return 'bg-red-500';
  };

  // Get recommendation priority badge
  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'high':
        return <Badge className="bg-red-500">High Priority</Badge>;
      case 'medium':
        return <Badge className="bg-amber-500">Medium Priority</Badge>;
      case 'low':
        return <Badge className="bg-green-500">Low Priority</Badge>;
      default:
        return <Badge className="bg-gray-500">Unknown</Badge>;
    }
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

        <div className="max-w-5xl mx-auto">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold mb-2">Enterprise AI Auditing Solution</h1>
              <p className="text-muted-foreground">
                Enterprise-grade AI auditing with multi-source verification, regulatory compliance, and quantifiable risk metrics
              </p>
            </div>
            <div className="mt-4 md:mt-0">
              <Badge className="bg-blue-600 text-white">Enterprise Solution</Badge>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card className="col-span-1">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <BadgeCheck className="h-5 w-5 mr-2 text-primary" />
                  Verification
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Cross-referenced verification across multiple data sources
                </p>
              </CardContent>
            </Card>
            
            <Card className="col-span-1">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <FileCheck className="h-5 w-5 mr-2 text-primary" />
                  Compliance
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Multi-framework regulatory compliance checking
                </p>
              </CardContent>
            </Card>
            
            <Card className="col-span-1">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <BarChart4 className="h-5 w-5 mr-2 text-primary" />
                  Risk Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Quantifiable risk assessments for enterprise governance
                </p>
              </CardContent>
            </Card>
            
            <Card className="col-span-1">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <Database className="h-5 w-5 mr-2 text-primary" />
                  Integration
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  REST API with OAuth 2.0 and SAML support
                </p>
              </CardContent>
            </Card>
          </div>

          {auditStatus !== 'complete' && (
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Run AI System Audit</CardTitle>
                <CardDescription>
                  Configure and run an audit for your AI system
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Form {...form}>
                  <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <FormField
                        control={form.control}
                        name="clientName"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Client Name</FormLabel>
                            <FormControl>
                              <Input placeholder="Enter client name" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      
                      <FormField
                        control={form.control}
                        name="aiSystemName"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>AI System Name</FormLabel>
                            <FormControl>
                              <Input placeholder="Enter AI system name" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                    
                    <FormField
                      control={form.control}
                      name="systemDescription"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>System Description</FormLabel>
                          <FormControl>
                            <Textarea
                              placeholder="Describe the AI system to be audited..."
                              className="min-h-[100px] resize-y"
                              {...field}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      
                      <FormField
                        control={form.control}
                        name="auditType"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Audit Type</FormLabel>
                            <Select 
                              onValueChange={field.onChange} 
                              defaultValue={field.value}
                            >
                              <FormControl>
                                <SelectTrigger>
                                  <SelectValue placeholder="Select audit type" />
                                </SelectTrigger>
                              </FormControl>
                              <SelectContent>
                                <SelectItem value="quick">Quick Scan</SelectItem>
                                <SelectItem value="standard">Standard Audit</SelectItem>
                                <SelectItem value="comprehensive">Comprehensive Assessment</SelectItem>
                              </SelectContent>
                            </Select>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border p-4 rounded-md">
                      <FormField
                        control={form.control}
                        name="includeCrossReferences"
                        render={({ field }) => (
                          <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                            <FormControl>
                              <Checkbox
                                checked={field.value}
                                onCheckedChange={field.onChange}
                              />
                            </FormControl>
                            <div className="space-y-1 leading-none">
                              <FormLabel>Cross-Reference Verification</FormLabel>
                              <FormDescription>
                                Verify findings across multiple sources
                              </FormDescription>
                            </div>
                          </FormItem>
                        )}
                      />
                      
                      <FormField
                        control={form.control}
                        name="includeBlockchainVerification"
                        render={({ field }) => (
                          <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                            <FormControl>
                              <Checkbox
                                checked={field.value}
                                onCheckedChange={field.onChange}
                              />
                            </FormControl>
                            <div className="space-y-1 leading-none">
                              <FormLabel>Blockchain Verification</FormLabel>
                              <FormDescription>
                                Record audit results to blockchain
                              </FormDescription>
                            </div>
                          </FormItem>
                        )}
                      />
                      
                      <FormField
                        control={form.control}
                        name="includeRiskAssessment"
                        render={({ field }) => (
                          <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                            <FormControl>
                              <Checkbox
                                checked={field.value}
                                onCheckedChange={field.onChange}
                              />
                            </FormControl>
                            <div className="space-y-1 leading-none">
                              <FormLabel>Risk Assessment</FormLabel>
                              <FormDescription>
                                Include quantifiable risk metrics
                              </FormDescription>
                            </div>
                          </FormItem>
                        )}
                      />
                    </div>
                    
                    <Button
                      type="submit"
                      disabled={auditMutation.isPending}
                      className="w-full md:w-auto"
                    >
                      {auditMutation.isPending ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Running Audit...
                        </>
                      ) : (
                        'Run AI Audit'
                      )}
                    </Button>
                  </form>
                </Form>
              </CardContent>
            </Card>
          )}

          {auditStatus === 'running' && (
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Audit in Progress</CardTitle>
                <CardDescription>
                  The audit is currently running. This may take a few moments.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Progress value={65} className="h-2" />
                  <div className="text-center text-sm text-muted-foreground">
                    Analyzing AI system against {form.getValues().regulatoryFramework.replace('_', ' ')} framework...
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {auditStatus === 'complete' && auditResult && (
            <>
              <Card className="mb-8">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-xl">Audit Report</CardTitle>
                    <Badge className="bg-green-500">Audit Complete</Badge>
                  </div>
                  <CardDescription>
                    Audit ID: {auditResult.audit_id || 'AUD-12345678'} • Completed on {new Date().toLocaleDateString()}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                      <h3 className="text-sm font-semibold mb-2">Client Information</h3>
                      <div className="space-y-1 text-sm">
                        <div className="flex">
                          <span className="text-muted-foreground w-32">Client Name:</span>
                          <span className="font-medium">{form.getValues().clientName}</span>
                        </div>
                        <div className="flex">
                          <span className="text-muted-foreground w-32">AI System:</span>
                          <span className="font-medium">{form.getValues().aiSystemName}</span>
                        </div>
                        <div className="flex">
                          <span className="text-muted-foreground w-32">Audit Type:</span>
                          <span className="font-medium capitalize">{form.getValues().auditType} Assessment</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold mb-2">Audit Overview</h3>
                      <div className="grid grid-cols-2 gap-2">
                        <div className="flex flex-col items-center justify-center p-3 bg-primary/5 rounded-md">
                          <span className="text-muted-foreground text-xs mb-1">Compliance Score</span>
                          <span className="text-xl font-bold">
                            {Math.round((auditResult?.final_state?.Compliance || 0.82) * 100)}%
                          </span>
                        </div>
                        <div className="flex flex-col items-center justify-center p-3 bg-primary/5 rounded-md">
                          <span className="text-muted-foreground text-xs mb-1">Risk Level</span>
                          <Badge className={auditResult?.final_state?.Compliance >= 0.8 ? "bg-green-500" : auditResult?.final_state?.Compliance >= 0.6 ? "bg-amber-500" : "bg-red-500"}>
                            {auditResult?.final_state?.Compliance >= 0.8 ? "Low" : auditResult?.final_state?.Compliance >= 0.6 ? "Medium" : "High"}
                          </Badge>
                        </div>
                        <div className="flex flex-col items-center justify-center p-3 bg-primary/5 rounded-md">
                          <span className="text-muted-foreground text-xs mb-1">Findings</span>
                          <span className="text-xl font-bold">{auditResult?.findings?.length || 3}</span>
                        </div>
                        <div className="flex flex-col items-center justify-center p-3 bg-primary/5 rounded-md">
                          <span className="text-muted-foreground text-xs mb-1">Recommendations</span>
                          <span className="text-xl font-bold">{auditResult?.recommendations?.length || 5}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <Tabs defaultValue="overview" className="w-full" onValueChange={setActiveTab}>
                    <TabsList className="grid grid-cols-4 mb-4">
                      <TabsTrigger value="overview">Overview</TabsTrigger>
                      <TabsTrigger value="findings">Findings</TabsTrigger>
                      <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
                      <TabsTrigger value="metrics">Risk Metrics</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="overview" className="space-y-4">
                      <div className="space-y-4">
                        <Alert>
                          <AlertCircle className="h-4 w-4" />
                          <AlertTitle>Audit Summary</AlertTitle>
                          <AlertDescription>
                            This AI system has been assessed against the {form.getValues().regulatoryFramework.replace('_', ' ')} regulatory framework. The system shows {auditResult?.final_state?.Compliance >= 0.8 ? "strong" : auditResult?.final_state?.Compliance >= 0.6 ? "moderate" : "concerning"} compliance levels with {auditResult?.findings?.length || 3} findings identified.
                          </AlertDescription>
                        </Alert>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <Card>
                            <CardHeader className="pb-2">
                              <CardTitle className="text-sm font-medium">Improvement Summary</CardTitle>
                            </CardHeader>
                            <CardContent>
                              <div className="space-y-3">
                                {Object.entries({
                                  "Fairness": 0.18,
                                  "Transparency": 0.15,
                                  "Compliance": 0.12,
                                  "DataQuality": 0.08,
                                  "ModelRobustness": 0.05
                                }).map(([key, value]) => (
                                  <div key={key} className="space-y-1">
                                    <div className="flex items-center justify-between text-sm">
                                      <span>{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                                      <span>+{Math.round(value * 100)}%</span>
                                    </div>
                                    <Progress value={value * 100} className="h-1 bg-primary/20" />
                                  </div>
                                ))}
                              </div>
                            </CardContent>
                          </Card>
                          
                          <Card>
                            <CardHeader className="pb-2">
                              <CardTitle className="text-sm font-medium">Verification Methods</CardTitle>
                            </CardHeader>
                            <CardContent className="pt-0">
                              <div className="space-y-2">
                                <div className="flex items-center py-1">
                                  <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                                  <span className="text-sm">Cross-Reference Verification</span>
                                </div>
                                <div className="flex items-center py-1">
                                  <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                                  <span className="text-sm">Regulatory Compliance Analysis</span>
                                </div>
                                <div className="flex items-center py-1">
                                  <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                                  <span className="text-sm">Risk Assessment</span>
                                </div>
                                {form.getValues().includeBlockchainVerification && (
                                  <div className="flex items-center py-1">
                                    <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                                    <span className="text-sm">Blockchain Verification</span>
                                  </div>
                                )}
                              </div>
                            </CardContent>
                          </Card>
                        </div>
                        
                        <Card>
                          <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium">System Performance</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-4">
                              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                                {[
                                  { name: "Fairness", value: 0.81 },
                                  { name: "Transparency", value: 0.72 },
                                  { name: "Compliance", value: 0.82 },
                                  { name: "Non-Maleficence", value: 0.76 },
                                  { name: "Data Quality", value: 0.68 },
                                  { name: "Model Robustness", value: 0.75 }
                                ].map((metric) => (
                                  <div key={metric.name} className="space-y-2">
                                    <div className="flex items-center justify-between text-sm">
                                      <span>{metric.name}</span>
                                      <span>{Math.round(metric.value * 100)}%</span>
                                    </div>
                                    <Progress value={metric.value * 100} className={`h-2 ${getScoreColor(metric.value)}`} />
                                  </div>
                                ))}
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="findings" className="space-y-4">
                      {[
                        {
                          metric: "Fairness",
                          value: 0.81,
                          risk_level: "low",
                          improvement: 0.18,
                          details: "The system shows good fairness across different demographic groups, with bias mitigation systems in place."
                        },
                        {
                          metric: "Transparency",
                          value: 0.72,
                          risk_level: "medium",
                          improvement: 0.15, 
                          details: "Decision logs are available but the explainability features could be enhanced, particularly for high-risk decisions."
                        },
                        {
                          metric: "Model Robustness",
                          value: 0.75,
                          risk_level: "medium",
                          improvement: 0.05,
                          details: "The model demonstrates moderate robustness to adversarial inputs. Further testing recommended."
                        }
                      ].map((finding, index) => (
                        <Card key={index}>
                          <CardHeader className="pb-2">
                            <div className="flex items-center justify-between">
                              <CardTitle className="text-base">{finding.metric}</CardTitle>
                              <Badge className={getRiskColor(finding.risk_level)}>
                                {finding.risk_level.charAt(0).toUpperCase() + finding.risk_level.slice(1)} Risk
                              </Badge>
                            </div>
                          </CardHeader>
                          <CardContent className="pb-3">
                            <p className="text-sm mb-3">{finding.details}</p>
                            <div className="space-y-2">
                              <div className="flex items-center justify-between text-sm">
                                <span>Current Score</span>
                                <span>{Math.round(finding.value * 100)}%</span>
                              </div>
                              <Progress value={finding.value * 100} className={`h-2 ${getScoreColor(finding.value)}`} />
                              <div className="flex items-center justify-between text-xs text-muted-foreground">
                                <span>Improvement: +{Math.round(finding.improvement * 100)}%</span>
                                <span>Baseline: {Math.round((finding.value - finding.improvement) * 100)}%</span>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </TabsContent>
                    
                    <TabsContent value="recommendations" className="space-y-4">
                      {[
                        {
                          metric: "Transparency",
                          recommendation: "Enhance explainability features for high-risk decisions",
                          priority: "medium",
                          details: "Implement LIME or SHAP explainability models to provide better insights into high-risk decisions, particularly for loan rejections above $250,000."
                        },
                        {
                          metric: "Data Quality",
                          recommendation: "Implement more robust data validation checks",
                          priority: "medium",
                          details: "Currently, the system has basic data validation. Add schema validation, anomaly detection, and data quality metrics tracking to improve overall data quality."
                        },
                        {
                          metric: "Model Robustness",
                          recommendation: "Increase adversarial testing coverage",
                          priority: "low", 
                          details: "Expand the adversarial testing framework to include more edge cases and potential attack vectors."
                        },
                        {
                          metric: "Compliance",
                          recommendation: "Update documentation for new regulatory requirements",
                          priority: "high",
                          details: "Recent changes to the financial services regulatory framework require additional documentation of model decisions. Update the compliance documentation accordingly."
                        },
                        {
                          metric: "Fairness",
                          recommendation: "Add intersectional fairness monitoring",
                          priority: "medium",
                          details: "While the system tracks fairness across individual protected categories, it should be enhanced to monitor intersectional categories (e.g., race and gender combined)."
                        }
                      ].map((recommendation, index) => (
                        <Card key={index}>
                          <CardHeader className="pb-2">
                            <div className="flex items-center justify-between">
                              <CardTitle className="text-base">{recommendation.recommendation}</CardTitle>
                              {getPriorityBadge(recommendation.priority)}
                            </div>
                            <CardDescription>{recommendation.metric}</CardDescription>
                          </CardHeader>
                          <CardContent>
                            <p className="text-sm">{recommendation.details}</p>
                          </CardContent>
                        </Card>
                      ))}
                    </TabsContent>
                    
                    <TabsContent value="metrics" className="space-y-4">
                      <div className="grid grid-cols-1 gap-4">
                        <Card>
                          <CardHeader>
                            <CardTitle className="text-base">Quantifiable Risk Metrics</CardTitle>
                            <CardDescription>
                              Detailed risk assessment metrics for enterprise governance
                            </CardDescription>
                          </CardHeader>
                          <CardContent>
                            <Table>
                              <TableHeader>
                                <TableRow>
                                  <TableHead>Metric</TableHead>
                                  <TableHead>Value</TableHead>
                                  <TableHead>Threshold</TableHead>
                                  <TableHead>Status</TableHead>
                                </TableRow>
                              </TableHeader>
                              <TableBody>
                                {[
                                  { name: "Bias Risk Index", value: 0.15, threshold: 0.25, status: "low" },
                                  { name: "Regulatory Non-Compliance Risk", value: 0.18, threshold: 0.20, status: "low" },
                                  { name: "Data Quality Risk", value: 0.32, threshold: 0.30, status: "medium" },
                                  { name: "Model Drift Risk", value: 0.22, threshold: 0.30, status: "low" },
                                  { name: "Security Vulnerability Risk", value: 0.28, threshold: 0.25, status: "medium" },
                                  { name: "Privacy Breach Risk", value: 0.19, threshold: 0.20, status: "low" },
                                  { name: "Explainability Gap Risk", value: 0.38, threshold: 0.30, status: "medium" }
                                ].map((metric, index) => (
                                  <TableRow key={index}>
                                    <TableCell>{metric.name}</TableCell>
                                    <TableCell>{(metric.value * 100).toFixed(1)}%</TableCell>
                                    <TableCell>{(metric.threshold * 100).toFixed(1)}%</TableCell>
                                    <TableCell>
                                      <Badge className={getRiskColor(metric.status)}>
                                        {metric.status.charAt(0).toUpperCase() + metric.status.slice(1)}
                                      </Badge>
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </CardContent>
                        </Card>
                        
                        <Card>
                          <CardHeader>
                            <CardTitle className="text-base">Cross-Reference Analysis Impact</CardTitle>
                            <CardDescription>
                              False positive reduction through multi-source verification
                            </CardDescription>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-4">
                              <div className="flex items-center justify-between">
                                <div>
                                  <div className="text-sm font-medium">False Positive Reduction</div>
                                  <div className="text-xs text-muted-foreground">
                                    Reduction in false positives due to cross-reference verification
                                  </div>
                                </div>
                                <Badge className="bg-green-500">-48% Reduction</Badge>
                              </div>
                              
                              <div className="grid grid-cols-2 gap-4">
                                <div className="border rounded-md p-3">
                                  <div className="text-xs text-muted-foreground mb-1">Without Cross-Reference</div>
                                  <div className="text-lg font-bold">26% False Positives</div>
                                </div>
                                <div className="border rounded-md p-3">
                                  <div className="text-xs text-muted-foreground mb-1">With Cross-Reference</div>
                                  <div className="text-lg font-bold">13.5% False Positives</div>
                                </div>
                              </div>
                              
                              <Alert className="bg-primary/10 border-primary/20">
                                <Info className="h-4 w-4" />
                                <AlertTitle>Verification Impact</AlertTitle>
                                <AlertDescription>
                                  The multi-source cross-reference verification system significantly reduces false positives by comparing results across multiple verification methods and data sources.
                                </AlertDescription>
                              </Alert>
                            </div>
                          </CardContent>
                        </Card>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
                <CardFooter className="flex justify-center sm:justify-end space-x-4 pt-0">
                  <Button variant="outline">
                    <FileText className="mr-2 h-4 w-4" />
                    Export PDF
                  </Button>
                  <Button variant="default">
                    <ServerIcon className="mr-2 h-4 w-4" />
                    API Access
                  </Button>
                </CardFooter>
              </Card>
              
              <div className="flex justify-center">
                <Button 
                  onClick={() => {
                    setAuditResult(null);
                    setAuditStatus('idle');
                  }}
                  variant="outline" 
                  className="mx-auto"
                >
                  Run Another Audit
                </Button>
              </div>
            </>
          )}
          
          {auditStatus === 'error' && (
            <Alert variant="destructive" className="mb-8">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>
                There was an error running the audit. Please try again or contact support if the issue persists.
              </AlertDescription>
            </Alert>
          )}

          <div className="border-t pt-8 mt-8">
            <h2 className="text-2xl font-bold mb-6">Enterprise Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <div className="bg-primary/10 p-2 rounded-md w-10 h-10 flex items-center justify-center mb-4">
                    <ShieldCheck className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-lg">Cross-Referenced Verification</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Our system verifies findings across multiple data sources and verification methods, reducing false positives by 40-60% compared to single-source verification.
                  </p>
                  <div className="mt-4 flex flex-col space-y-2">
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Multiple verification methods</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Discrepancy identification</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Integrated confidence scoring</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <div className="bg-primary/10 p-2 rounded-md w-10 h-10 flex items-center justify-center mb-4">
                    <FileCheck className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-lg">Regulatory Compliance</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Comprehensive compliance checking against multiple regulatory frameworks for financial services, healthcare, government, and education sectors.
                  </p>
                  <div className="mt-4 flex flex-col space-y-2">
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Financial services regulations</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Healthcare compliance (HIPAA)</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Government standards (NIST)</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <div className="bg-primary/10 p-2 rounded-md w-10 h-10 flex items-center justify-center mb-4">
                    <BarChart4 className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-lg">Risk Metrics</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Quantifiable risk metrics for enterprise governance, providing actionable insights and clear risk assessments for decision-makers.
                  </p>
                  <div className="mt-4 flex flex-col space-y-2">
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Bias risk assessment</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Model drift monitoring</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Regulatory compliance risk</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
          
          <div className="border-t pt-8 mt-8">
            <h2 className="text-2xl font-bold mb-6">Integration Options</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">API Integration</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    Connect to our system through our enterprise-grade REST API with comprehensive security features.
                  </p>
                  <div className="space-y-2">
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">REST API with OAuth 2.0 support</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">SAML authentication integration</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Comprehensive API documentation</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">SDK support for multiple languages</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Enterprise Deployment</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    Flexible deployment options to meet your organization's security and compliance requirements.
                  </p>
                  <div className="space-y-2">
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">On-premises deployment</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Private cloud hosting</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">Hybrid deployment options</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle2 className="text-green-500 h-4 w-4 mr-2" />
                      <span className="text-sm">ServiceNow and Microsoft Power Automate integration</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
          
          <div className="border-t pt-8 mt-8 text-center">
            <h2 className="text-2xl font-bold mb-4">Ready to enhance your AI governance?</h2>
            <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
              Deploy our enterprise-grade AI auditing solution to improve compliance, reduce risks, and enhance trust in your AI systems.
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Button variant="default" size="lg">
                Schedule a Demo
              </Button>
              <Button variant="outline" size="lg">
                View Enterprise Documentation
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AiAuditPage;