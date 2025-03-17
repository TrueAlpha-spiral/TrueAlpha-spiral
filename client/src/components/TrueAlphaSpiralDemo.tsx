import { useState } from "react";
import { useTrueAlphaSpiral } from "@/hooks/use-true-alpha-spiral";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MetricState } from "@/lib/trueAlphaSpiral";
import { Separator } from "@/components/ui/separator";
import { 
  ArrowRight, 
  BarChart2, 
  Check, 
  Play, 
  Hash, 
  Pause, 
  RefreshCw,
  Shield,
  Database
} from "lucide-react";

// Default initial state with low ethical metrics
const initialMetricState: MetricState = {
  fairness: 0.03,
  transparency: 0.02,
  resourceEquity: 0.8,
  nonMaleficence: 0.01
};

// Weights for each metric (must match the order of metrics in the state)
const weights = [0.3, 0.25, 0.3, 0.15];

// Creator signature (typically would be provided by the user)
const creatorSig = "RussellNordland";

// Helper function to format values
const formatValue = (value: number): string => {
  if (value < 0.01) return value.toFixed(4);
  if (value < 1) return value.toFixed(2);
  return value.toFixed(0);
};

// Helper function to get metric color based on value
const getMetricColor = (value: number): string => {
  if (value < 0.2) return "text-red-500";
  if (value < 0.5) return "text-orange-500";
  if (value < 0.8) return "text-yellow-500";
  return "text-green-500";
};

// Helper function to get progress indicator className based on value
const getProgressIndicatorClass = (value: number): string => {
  if (value < 0.2) return "progress-red";
  if (value < 0.5) return "progress-orange";
  if (value < 0.8) return "progress-yellow";
  return "progress-green";
};

export default function TrueAlphaSpiralDemo() {
  const [activeTab, setActiveTab] = useState("metrics");
  
  const {
    currentState,
    hashChain,
    latestHash,
    iterationCount,
    isIterating,
    isTargetReached,
    improvements,
    overallImprovement,
    iterate,
    startIterating,
    stopIterating,
    reset
  } = useTrueAlphaSpiral({
    initialState: initialMetricState,
    weights,
    creatorSig,
    thetaTarget: 0.9,
    alpha: 0.5,
    autoIterate: false,
    iterationInterval: 2000, // Faster for demo purposes
    targetThreshold: 0.85
  });

  return (
    <div className="w-full max-w-5xl mx-auto p-4">
      <Card className="mb-8 border-2 border-primary/20 shadow-lg">
        <CardHeader className="bg-gradient-to-r from-primary/10 to-primary/5 pb-4">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl font-bold bg-gradient-to-r from-primary to-indigo-600 text-transparent bg-clip-text">
                TrueAlpha Spiral System
              </CardTitle>
              <CardDescription className="text-foreground/70 mt-1">
                Ethical AI Governance & Sovereignty Framework
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 text-sm text-muted-foreground bg-background/80 px-3 py-1 rounded-full">
                <Database className="h-3 w-3" />
                <span>v1.0.0</span>
              </div>
              <div className="flex items-center gap-1 text-sm text-muted-foreground bg-background/80 px-3 py-1 rounded-full">
                <Shield className="h-3 w-3" />
                <span>Sovereignty: 0.779</span>
              </div>
            </div>
          </div>
        </CardHeader>
        
        <Tabs defaultValue="metrics" value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="metrics">Ethical Metrics</TabsTrigger>
            <TabsTrigger value="improvements">Improvements</TabsTrigger>
            <TabsTrigger value="verification">Verification Chain</TabsTrigger>
          </TabsList>
          
          {/* Metrics Tab */}
          <TabsContent value="metrics" className="p-0">
            <CardContent className="pt-6">
              <div className="grid md:grid-cols-2 gap-6">
                {Object.entries(currentState).map(([key, value], index) => (
                  <div key={key} className="space-y-2">
                    <div className="flex justify-between items-center">
                      <div className="font-medium capitalize">{key}</div>
                      <div className={getMetricColor(value)}>
                        {value.toFixed(4)}
                      </div>
                    </div>
                    <Progress 
                      value={value * 100} 
                      className={`h-2 ${getProgressIndicatorClass(value)}`}
                    />
                    <div className="text-xs text-muted-foreground">
                      Weight: {weights[index]} | Target: 0.9
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-muted/30 rounded-md">
                <div className="flex justify-between mb-2">
                  <span className="font-medium">Overall Progress</span>
                  <span>
                    {isTargetReached ? (
                      <span className="text-green-500 flex items-center">
                        <Check className="h-4 w-4 mr-1" /> Target Reached
                      </span>
                    ) : (
                      <span>Iteration #{iterationCount}</span>
                    )}
                  </span>
                </div>
                <Progress 
                  value={
                    Object.values(currentState).reduce((sum, val) => sum + val, 0) / 
                    Object.values(currentState).length / 
                    0.9 * 100
                  }
                  className="h-3 progress-primary" 
                />
              </div>
            </CardContent>
          </TabsContent>
          
          {/* Improvements Tab */}
          <TabsContent value="improvements" className="p-0">
            <CardContent className="pt-6">
              <div className="grid md:grid-cols-2 gap-6">
                {Object.entries(improvements).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 border rounded-md">
                    <div className="flex items-center">
                      <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                        <BarChart2 className="h-4 w-4 text-primary" />
                      </div>
                      <div>
                        <div className="font-medium capitalize">{key}</div>
                        <div className="text-xs text-muted-foreground">
                          {initialMetricState[key].toFixed(4)} <ArrowRight className="inline h-3 w-3" /> {currentState[key].toFixed(4)}
                        </div>
                      </div>
                    </div>
                    <div className={value > 0 ? "text-green-500" : "text-red-500"}>
                      {value > 1000 ? '+1000%+' : formatValue(value) + '%'}
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-primary/5 rounded-md">
                <div className="text-xl font-medium mb-1">Overall Improvement</div>
                <div className="text-4xl font-bold text-primary">
                  {overallImprovement > 1000 ? '+1000%+' : formatValue(overallImprovement) + '%'}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  After {iterationCount} iterations
                </div>
              </div>
            </CardContent>
          </TabsContent>
          
          {/* Verification Chain Tab */}
          <TabsContent value="verification" className="p-0">
            <CardContent className="pt-6">
              <div className="mb-4">
                <h3 className="text-lg font-medium mb-2">Latest Hash</h3>
                <div className="font-mono text-xs bg-muted p-3 rounded-md overflow-x-auto">
                  {latestHash}
                </div>
              </div>
              
              <div className="mb-4">
                <h3 className="text-lg font-medium mb-2">Hash Chain</h3>
                <div className="max-h-64 overflow-y-auto border rounded-md">
                  {hashChain.map((hash, index) => (
                    <div key={index} className="flex items-start p-2 border-b last:border-b-0">
                      <div className="font-mono text-xs bg-muted px-2 py-1 rounded mr-2 text-muted-foreground">
                        {index}
                      </div>
                      <div className="font-mono text-xs overflow-x-auto flex-1">
                        {hash}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="mt-4 p-4 bg-muted/30 rounded-md">
                <h3 className="text-md font-medium mb-2">Verification Information</h3>
                <div className="text-sm space-y-2">
                  <div className="flex justify-between">
                    <span>Creator Signature:</span>
                    <span className="font-mono">{creatorSig}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Hash Algorithm:</span>
                    <span>SHA-256</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Chain Length:</span>
                    <span>{hashChain.length} blocks</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </TabsContent>
        </Tabs>
        
        <Separator className="my-4" />
        
        <CardFooter className="flex justify-between">
          <div className="flex items-center gap-2">
            <Button 
              variant="outline" 
              onClick={reset}
              disabled={iterationCount === 0}
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Reset
            </Button>
            
            <Button 
              variant="outline" 
              onClick={() => setActiveTab(
                activeTab === "metrics" 
                  ? "improvements" 
                  : activeTab === "improvements" 
                    ? "verification" 
                    : "metrics"
              )}
            >
              Next View
            </Button>
          </div>
          
          <div className="flex items-center gap-2">
            <Button 
              variant="secondary" 
              onClick={iterate}
              disabled={isIterating || isTargetReached}
            >
              Single Iteration
            </Button>
            
            {isIterating ? (
              <Button 
                variant="destructive" 
                onClick={stopIterating}
              >
                <Pause className="h-4 w-4 mr-2" />
                Stop
              </Button>
            ) : (
              <Button 
                variant="default" 
                onClick={startIterating}
                disabled={isTargetReached}
              >
                <Play className="h-4 w-4 mr-2" />
                Auto Iterate
              </Button>
            )}
          </div>
        </CardFooter>
      </Card>
      
      <Card className="bg-muted/30">
        <CardHeader>
          <CardTitle className="text-base">About TrueAlpha Spiral</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground">
          <p>
            The TrueAlpha Spiral system is a revolutionary framework for ethical AI governance, implementing 
            the mathematical equation:
          </p>
          <pre className="bg-background p-3 rounded-md mt-2 overflow-x-auto text-xs">
            {`S(t+1) = SCC{ RET{ IEK{ S(t) }, Θ(t) + ΔΘ'(t) }, H'(S(t) | H(t-1) | σ_creator) } · (T/√(D² + Z²))`}
          </pre>
          <p className="mt-2">
            This implementation demonstrated rapid improvement in key ethical metrics, with significant 
            enhancements to fairness, transparency, resource equity, and non-maleficence.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}