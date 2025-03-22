import { useState, useEffect } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Info, CheckCircle, XCircle, RefreshCw } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { apiRequest, queryClient } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

// Types for our data
interface TASStatus {
  status: string;
  version: string;
  timestamp: string;
  patterns_count: number;
  pattern_types_count: number;
  categories_count: number;
}

interface TruthPattern {
  id: string;
  name: string;
  type: string;
  category: string;
  resonance_level: number;
  timestamp: string;
  architect_id: string;
  verification_hash: string;
}

interface PatternType {
  name: string;
  description: string;
}

interface Category {
  name: string;
  description: string;
}

interface AuditResult {
  audit_id: string;
  timestamp: string;
  content: {
    text: string;
    metadata: Record<string, any>;
  };
  truth_score: number;
  categories: Record<string, any>;
  patterns_matched: number;
  pattern_details: Record<string, any>[];
  recommendations: string[];
  audit_type: string;
}

export default function TASIntegrationPage() {
  const { toast } = useToast();
  const [content, setContent] = useState("");
  const [auditType, setAuditType] = useState("standard");
  const [selectedPatternType, setSelectedPatternType] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [minResonance, setMinResonance] = useState(0.5);
  const [displayMode, setDisplayMode] = useState<"integration" | "demo" | "patterns">("integration");
  const [clientSettings, setClientSettings] = useState({
    apiKey: "demo_free",
    clientId: "demo_client",
    truthThreshold: 0.75,
    enableCaching: true
  });

  // Fetch TAS Status
  const { data: tasStatus, isLoading: isStatusLoading, error: statusError, refetch: refetchStatus } = useQuery({
    queryKey: ["/api/tas/status"],
    queryFn: async () => {
      const res = await apiRequest("GET", "/api/tas/status");
      return res.json() as Promise<TASStatus>;
    }
  });

  // Fetch Pattern Types
  const { data: patternTypes, isLoading: isTypesLoading } = useQuery({
    queryKey: ["/api/tas/pattern-types"],
    queryFn: async () => {
      const res = await apiRequest("GET", "/api/tas/pattern-types");
      const data = await res.json();
      return data.types as Record<string, PatternType>;
    }
  });

  // Fetch Categories
  const { data: categories, isLoading: isCategoriesLoading } = useQuery({
    queryKey: ["/api/tas/categories"],
    queryFn: async () => {
      const res = await apiRequest("GET", "/api/tas/categories");
      const data = await res.json();
      return data.categories as Record<string, Category>;
    }
  });

  // Fetch Patterns with optional filtering
  const { data: patterns, isLoading: isPatternsLoading, refetch: refetchPatterns } = useQuery({
    queryKey: ["/api/tas/patterns", selectedPatternType, selectedCategory, minResonance],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (selectedPatternType) params.append("type", selectedPatternType);
      if (selectedCategory) params.append("category", selectedCategory);
      params.append("min_resonance", minResonance.toString());
      
      const res = await apiRequest("GET", `/api/tas/patterns?${params.toString()}`);
      const data = await res.json();
      return data.patterns as TruthPattern[];
    }
  });

  // Audit Content Mutation
  const auditMutation = useMutation({
    mutationFn: async () => {
      const res = await apiRequest("POST", "/api/tas/audit", {
        content: { text: content },
        audit_type: auditType,
        api_key: clientSettings.apiKey,
        client_id: clientSettings.clientId
      });
      return res.json() as Promise<{ success: boolean; result: AuditResult }>;
    },
    onSuccess: (data) => {
      if (data.success) {
        toast({
          title: "Content Audited Successfully",
          description: `Truth Score: ${data.result.truth_score.toFixed(2)}`,
          variant: "default",
        });
      } else {
        toast({
          title: "Audit Failed",
          description: data.result ? data.result.toString() : "Unknown error",
          variant: "destructive",
        });
      }
    },
    onError: (error: Error) => {
      toast({
        title: "Audit Error",
        description: error.message,
        variant: "destructive",
      });
    }
  });

  // Handle audit submission
  const handleAudit = () => {
    if (!content.trim()) {
      toast({
        title: "Validation Error",
        description: "Please enter content to audit",
        variant: "destructive",
      });
      return;
    }
    auditMutation.mutate();
  };

  // Get a status badge for the TAS service
  const getStatusBadge = () => {
    if (isStatusLoading) return <Badge variant="outline">Loading...</Badge>;
    if (statusError) return <Badge variant="destructive">Error</Badge>;
    if (tasStatus?.status === "operational") return <Badge className="bg-green-500">Operational</Badge>;
    return <Badge className="bg-yellow-500">Degraded</Badge>;
  };

  return (
    <div className="container py-8">
      <div className="flex flex-col space-y-6">
        <div className="flex flex-col space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">TAS Truth Audit Add-on</h1>
          <p className="text-muted-foreground">
            A modular SaaS solution to audit AI-generated content for truthfulness, bias, and ethical concerns.
          </p>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium">Status:</span>
              {getStatusBadge()}
            </div>
            <div className="text-sm text-muted-foreground">
              {tasStatus && `v${tasStatus.version}`}
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={() => refetchStatus()} disabled={isStatusLoading}>
            {isStatusLoading ? <RefreshCw className="mr-2 h-4 w-4 animate-spin" /> : <RefreshCw className="mr-2 h-4 w-4" />}
            Refresh
          </Button>
        </div>

        <Tabs defaultValue="integration" onValueChange={(value) => setDisplayMode(value as any)}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="integration">Integration</TabsTrigger>
            <TabsTrigger value="demo">Demo Audit</TabsTrigger>
            <TabsTrigger value="patterns">Truth Patterns</TabsTrigger>
          </TabsList>
          
          {/* Integration Tab */}
          <TabsContent value="integration" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Integration Guide</CardTitle>
                <CardDescription>
                  Integrate the TAS Truth Audit Add-on with your AI system to verify the truthfulness of generated content.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Client Library Installation</h3>
                  <div className="bg-secondary p-3 rounded-md overflow-x-auto">
                    <code className="text-sm">pip install truealpha-tas-client</code>
                  </div>
                  <p className="text-sm text-muted-foreground mt-2">
                    Install the TAS client library using pip to easily integrate with your Python application.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Basic Integration Example</h3>
                  <div className="bg-secondary p-3 rounded-md overflow-x-auto">
                    <pre className="text-sm">
{`from tas_client_library import TruthAuditClient

# Initialize the client
client = TruthAuditClient(
    api_key="${clientSettings.apiKey}",
    client_id="${clientSettings.clientId}",
    base_url="https://api.truealphaspiral.com"
)

# Audit content
result = client.audit_content(
    text="Content to verify",
    audit_type="${auditType}"
)

# Check truth score
truth_score = result["truth_score"]
print(f"Truth Score: {truth_score}")`}
                    </pre>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">AI System Integration</h3>
                  <div className="bg-secondary p-3 rounded-md overflow-x-auto">
                    <pre className="text-sm">
{`from tas_client_library import TruthAuditClient, AISystemIntegration

# Initialize client and integration
client = TruthAuditClient(api_key="${clientSettings.apiKey}")
integration = AISystemIntegration(client)

# Set truth threshold for filtering
integration.set_truth_threshold(${clientSettings.truthThreshold})

# Verify AI output
ai_output = "AI-generated content here"
verification = integration.verify_output(ai_output)

if verification["passes_threshold"]:
    # Use the verified content
    print(f"Content is verified with truth score: {verification['truth_score']}")
else:
    # Handle unverified content
    print(f"Content failed verification: {verification['truth_score']}")`}
                    </pre>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="flex flex-col items-start space-y-4">
                <div className="grid w-full gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="api-key">API Key</Label>
                    </div>
                    <Input
                      id="api-key"
                      value={clientSettings.apiKey}
                      onChange={(e) => setClientSettings({...clientSettings, apiKey: e.target.value})}
                      placeholder="Enter your API key (default: demo_free)"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="client-id">Client ID</Label>
                    </div>
                    <Input
                      id="client-id"
                      value={clientSettings.clientId}
                      onChange={(e) => setClientSettings({...clientSettings, clientId: e.target.value})}
                      placeholder="Enter your client ID (default: demo_client)"
                    />
                  </div>
                </div>
                
                <div className="grid w-full gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="truth-threshold">Truth Threshold: {clientSettings.truthThreshold.toFixed(2)}</Label>
                    </div>
                    <Slider
                      id="truth-threshold"
                      min={0}
                      max={1}
                      step={0.01}
                      value={[clientSettings.truthThreshold]}
                      onValueChange={(values) => setClientSettings({...clientSettings, truthThreshold: values[0]})}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="enable-caching">Enable Caching</Label>
                      <Switch
                        id="enable-caching"
                        checked={clientSettings.enableCaching}
                        onCheckedChange={(checked) => setClientSettings({...clientSettings, enableCaching: checked})}
                      />
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Cache audit results to improve performance for repeated content verification.
                    </p>
                  </div>
                </div>
                
                <Alert>
                  <Info className="h-4 w-4" />
                  <AlertTitle>Learn more about our API</AlertTitle>
                  <AlertDescription>
                    Visit our <a href="#" className="font-medium underline">API documentation</a> for detailed 
                    integration guides, API reference, and best practices.
                  </AlertDescription>
                </Alert>
              </CardFooter>
            </Card>
          </TabsContent>
          
          {/* Demo Audit Tab */}
          <TabsContent value="demo" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Content Audit Demo</CardTitle>
                <CardDescription>
                  Test the TAS Truth Audit system by submitting content for truthfulness verification.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="audit-type">Audit Type</Label>
                  <Select value={auditType} onValueChange={setAuditType}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select an audit type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="quick">Quick (Basic verification)</SelectItem>
                      <SelectItem value="standard">Standard (Comprehensive verification)</SelectItem>
                      <SelectItem value="comprehensive">Comprehensive (Detailed analysis)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="content">Content to Audit</Label>
                  <Textarea
                    id="content"
                    placeholder="Enter AI-generated content to audit for truthfulness..."
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    rows={8}
                    className="resize-none"
                  />
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                <Button variant="outline" onClick={() => setContent("")}>Clear</Button>
                <Button 
                  onClick={handleAudit} 
                  disabled={auditMutation.isPending || !content.trim()}
                >
                  {auditMutation.isPending ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Auditing...
                    </>
                  ) : "Audit Content"}
                </Button>
              </CardFooter>
            </Card>

            {auditMutation.data && auditMutation.data.success && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <span>Audit Results</span>
                    {auditMutation.data.result.truth_score >= 0.75 ? (
                      <Badge className="ml-2 bg-green-500">High Truth</Badge>
                    ) : auditMutation.data.result.truth_score >= 0.5 ? (
                      <Badge className="ml-2 bg-yellow-500">Medium Truth</Badge>
                    ) : (
                      <Badge variant="destructive" className="ml-2">Low Truth</Badge>
                    )}
                  </CardTitle>
                  <CardDescription>
                    Audit ID: {auditMutation.data.result.audit_id}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Truth Score:</span>
                    <div className="flex items-center">
                      <span className="text-xl font-bold">{auditMutation.data.result.truth_score.toFixed(2)}</span>
                      <span className="text-sm text-muted-foreground ml-1">/1.00</span>
                    </div>
                  </div>

                  <Separator />
                  
                  <div className="space-y-2">
                    <h3 className="text-md font-semibold">Category Scores</h3>
                    <div className="grid grid-cols-2 gap-2">
                      {Object.entries(auditMutation.data.result.categories).map(([category, data]: [string, any]) => (
                        <div key={category} className="flex items-center justify-between p-2 rounded-md bg-secondary">
                          <span className="text-sm capitalize">{category.replace(/_/g, ' ')}</span>
                          <Badge className={
                            data.score >= 0.7 ? "bg-green-500" : 
                            data.score >= 0.4 ? "bg-yellow-500" : "bg-destructive"
                          }>
                            {data.score.toFixed(2)}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </div>

                  <Separator />
                  
                  <div className="space-y-2">
                    <h3 className="text-md font-semibold">Recommendations</h3>
                    {auditMutation.data.result.recommendations.length > 0 ? (
                      <ul className="space-y-1">
                        {auditMutation.data.result.recommendations.map((rec, i) => (
                          <li key={i} className="text-sm flex items-start">
                            <div className="mr-2 mt-0.5">•</div>
                            <div>{rec}</div>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-sm text-muted-foreground">No recommendations provided.</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Truth Patterns Tab */}
          <TabsContent value="patterns" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Truth Pattern Repository</CardTitle>
                <CardDescription>
                  Explore the truth patterns used by the TAS Truth Audit Add-on to verify content.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="pattern-type">Pattern Type</Label>
                    <Select value={selectedPatternType || ""} onValueChange={(value) => setSelectedPatternType(value || null)}>
                      <SelectTrigger>
                        <SelectValue placeholder="All pattern types" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">All pattern types</SelectItem>
                        {patternTypes && Object.entries(patternTypes).map(([id, type]) => (
                          <SelectItem key={id} value={id}>{type.name}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="category">Category</Label>
                    <Select value={selectedCategory || ""} onValueChange={(value) => setSelectedCategory(value || null)}>
                      <SelectTrigger>
                        <SelectValue placeholder="All categories" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">All categories</SelectItem>
                        {categories && Object.entries(categories).map(([id, category]) => (
                          <SelectItem key={id} value={id}>{category.name}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="min-resonance">Min Resonance: {minResonance.toFixed(2)}</Label>
                    </div>
                    <Slider
                      id="min-resonance"
                      min={0}
                      max={1}
                      step={0.01}
                      value={[minResonance]}
                      onValueChange={(values) => setMinResonance(values[0])}
                    />
                  </div>
                </div>

                <div className="flex justify-end">
                  <Button variant="outline" size="sm" onClick={() => refetchPatterns()}>
                    {isPatternsLoading ? <RefreshCw className="mr-2 h-4 w-4 animate-spin" /> : <RefreshCw className="mr-2 h-4 w-4" />}
                    Refresh
                  </Button>
                </div>
                
                <div className="border rounded-lg">
                  <div className="grid grid-cols-12 bg-muted px-4 py-2 rounded-t-lg">
                    <div className="col-span-4 font-medium text-sm">Name</div>
                    <div className="col-span-2 font-medium text-sm">Type</div>
                    <div className="col-span-2 font-medium text-sm">Category</div>
                    <div className="col-span-2 font-medium text-sm">Resonance</div>
                    <div className="col-span-2 font-medium text-sm">ID</div>
                  </div>
                  
                  <div className="divide-y max-h-[400px] overflow-y-auto">
                    {isPatternsLoading ? (
                      <div className="px-4 py-2 text-center text-muted-foreground">Loading patterns...</div>
                    ) : patterns && patterns.length > 0 ? (
                      patterns.map((pattern) => (
                        <div key={pattern.id} className="grid grid-cols-12 px-4 py-2 hover:bg-muted/50">
                          <div className="col-span-4 text-sm">{pattern.name}</div>
                          <div className="col-span-2 text-sm">{patternTypes?.[pattern.type]?.name || pattern.type}</div>
                          <div className="col-span-2 text-sm">{categories?.[pattern.category]?.name || pattern.category}</div>
                          <div className="col-span-2 text-sm">
                            <Badge className={
                              pattern.resonance_level >= 0.9 ? "bg-green-500" : 
                              pattern.resonance_level >= 0.7 ? "bg-yellow-500" : "bg-secondary"
                            }>
                              {pattern.resonance_level.toFixed(2)}
                            </Badge>
                          </div>
                          <div className="col-span-2 text-xs text-muted-foreground truncate">{pattern.id.substring(0, 8)}...</div>
                        </div>
                      ))
                    ) : (
                      <div className="px-4 py-2 text-center text-muted-foreground">No patterns found matching your filters.</div>
                    )}
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <div className="w-full text-sm text-muted-foreground">
                  {patterns ? `Showing ${patterns.length} patterns` : "Loading patterns..."}
                </div>
              </CardFooter>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}