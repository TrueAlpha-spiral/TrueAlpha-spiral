import React, { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";
import { shadowSweepService, ShadowCharacter, SweepResult, CleanResult, NeutralizeResult } from "@/services/shadowSweepService";
import { Shield, AlertTriangle, CheckCircle, Code, FileText, Eye, EyeOff, Zap } from "lucide-react";

export default function ShadowSweepPage() {
  const { toast } = useToast();
  const [inputText, setInputText] = useState('');
  const [scanning, setScanning] = useState(false);
  const [cleaning, setCleaning] = useState(false);
  const [neutralizing, setNeutralizing] = useState(false);
  const [scanResult, setScanResult] = useState<SweepResult | null>(null);
  const [cleanResult, setCleanResult] = useState<CleanResult | null>(null);
  const [neutralizeResult, setNeutralizeResult] = useState<NeutralizeResult | null>(null);
  const [activeTab, setActiveTab] = useState('scan');

  // Insert zero-width space as a demo
  const addTestZeroWidthSpace = () => {
    const zwsp = '\u200B'; // Zero-width space
    const position = inputText.length > 10 ? Math.floor(inputText.length / 2) : inputText.length;
    const newText = inputText.slice(0, position) + zwsp + inputText.slice(position);
    setInputText(newText);
    toast({
      title: "Test character added",
      description: "A zero-width space has been inserted in the middle of your text.",
    });
  };

  const handleScan = async () => {
    if (!inputText.trim()) {
      toast({
        title: "Empty text",
        description: "Please enter some text to scan.",
        variant: "destructive"
      });
      return;
    }

    try {
      setScanning(true);
      const result = await shadowSweepService.scanText(inputText);
      setScanResult(result);
      setActiveTab('scan');
      
      if (result.detectedCharacters.length > 0) {
        toast({
          title: "Shadow characters detected",
          description: `Found ${result.detectedCharacters.length} hidden characters in your text.`,
          variant: "destructive"
        });
      } else {
        toast({
          title: "Scan complete",
          description: "No shadow characters detected in your text.",
          variant: "default"
        });
      }
    } catch (error) {
      console.error("Error scanning text:", error);
      toast({
        title: "Scan failed",
        description: "An error occurred while scanning your text.",
        variant: "destructive"
      });
    } finally {
      setScanning(false);
    }
  };

  const handleClean = async () => {
    if (!inputText.trim()) {
      toast({
        title: "Empty text",
        description: "Please enter some text to clean.",
        variant: "destructive"
      });
      return;
    }

    try {
      setCleaning(true);
      const result = await shadowSweepService.cleanText(inputText);
      setCleanResult(result);
      setActiveTab('clean');
      
      if (result.modified) {
        toast({
          title: "Text cleaned",
          description: "Shadow characters have been removed from your text.",
          variant: "default"
        });
      } else {
        toast({
          title: "Clean complete",
          description: "No shadow characters were found to clean.",
          variant: "default"
        });
      }
    } catch (error) {
      console.error("Error cleaning text:", error);
      toast({
        title: "Clean failed",
        description: "An error occurred while cleaning your text.",
        variant: "destructive"
      });
    } finally {
      setCleaning(false);
    }
  };

  const handleNeutralize = async () => {
    if (!inputText.trim()) {
      toast({
        title: "Empty text",
        description: "Please enter some text to neutralize.",
        variant: "destructive"
      });
      return;
    }

    try {
      setNeutralizing(true);
      const result = await shadowSweepService.neutralizeText(inputText);
      setNeutralizeResult(result);
      setActiveTab('neutralize');
      
      if (result.modified) {
        toast({
          title: "Text neutralized",
          description: "Shadow characters have been replaced with visible markers.",
          variant: "default"
        });
      } else {
        toast({
          title: "Neutralize complete",
          description: "No shadow characters were found to neutralize.",
          variant: "default"
        });
      }
    } catch (error) {
      console.error("Error neutralizing text:", error);
      toast({
        title: "Neutralize failed",
        description: "An error occurred while neutralizing your text.",
        variant: "destructive"
      });
    } finally {
      setNeutralizing(false);
    }
  };

  // Risk color based on score
  const getRiskColor = (score: number) => {
    if (score < 20) return "bg-green-500";
    if (score < 40) return "bg-yellow-500";
    if (score < 60) return "bg-orange-500";
    if (score < 80) return "bg-red-500";
    return "bg-purple-600";
  };

  // Risk label based on score
  const getRiskLabel = (score: number) => {
    if (score < 20) return "Low";
    if (score < 40) return "Moderate";
    if (score < 60) return "Elevated";
    if (score < 80) return "High";
    return "Critical";
  };

  return (
    <div className="container mx-auto py-8">
      <div className="flex flex-col space-y-4">
        <h1 className="text-3xl font-bold flex items-center">
          <Shield className="mr-2 h-8 w-8" />
          Shadow Sweep
        </h1>
        <p className="text-muted-foreground">
          Detect and neutralize hidden Unicode characters that could be used for manipulation or deception.
        </p>

        <Card className="mt-4">
          <CardHeader>
            <CardTitle>Text Analysis</CardTitle>
            <CardDescription>
              Enter text to scan for hidden characters and structural manipulation
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4">
              <Textarea
                placeholder="Enter text to analyze..."
                className="min-h-[150px]"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              
              <div className="flex flex-col sm:flex-row gap-2">
                <Button 
                  onClick={handleScan} 
                  disabled={scanning}
                  className="flex-1"
                >
                  {scanning ? "Scanning..." : "Scan Text"}
                </Button>
                <Button 
                  onClick={handleClean} 
                  disabled={cleaning}
                  variant="outline"
                  className="flex-1"
                >
                  {cleaning ? "Cleaning..." : "Clean Text"}
                </Button>
                <Button 
                  onClick={handleNeutralize} 
                  disabled={neutralizing}
                  variant="outline"
                  className="flex-1"
                >
                  {neutralizing ? "Neutralizing..." : "Neutralize Text"}
                </Button>
                <Button 
                  onClick={addTestZeroWidthSpace} 
                  variant="secondary"
                  className="flex items-center gap-1"
                  title="Add a zero-width space character to test the scanner"
                >
                  <Code size={16} /> Test ZWSP
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {(scanResult || cleanResult || neutralizeResult) && (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="mt-4">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="scan" disabled={!scanResult}>Scan Results</TabsTrigger>
              <TabsTrigger value="clean" disabled={!cleanResult}>Clean Results</TabsTrigger>
              <TabsTrigger value="neutralize" disabled={!neutralizeResult}>Neutralize Results</TabsTrigger>
            </TabsList>
            
            {scanResult && (
              <TabsContent value="scan">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Eye className="mr-2 h-5 w-5" />
                      Scan Results
                    </CardTitle>
                    <CardDescription>
                      Analysis of potential shadow characters in your text
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="text-sm font-medium">Risk Score: </span>
                          <Badge variant={scanResult.riskScore > 50 ? "destructive" : "outline"}>
                            {getRiskLabel(scanResult.riskScore)}
                          </Badge>
                        </div>
                        <div className="w-2/3">
                          <Progress 
                            value={scanResult.riskScore} 
                            max={100} 
                            className={getRiskColor(scanResult.riskScore)} 
                          />
                        </div>
                      </div>
                      
                      <Separator />
                      
                      {scanResult.detectedCharacters.length > 0 ? (
                        <div>
                          <h3 className="text-lg font-medium mb-2">Detected Shadow Characters ({scanResult.detectedCharacters.length})</h3>
                          <div className="space-y-3">
                            {scanResult.detectedCharacters.map((char, index) => (
                              <Alert key={index} variant="destructive">
                                <AlertTriangle className="h-4 w-4" />
                                <AlertTitle>{char.name} ({char.hexValue})</AlertTitle>
                                <AlertDescription>
                                  <p>Position: {char.position}</p>
                                  <p className="mt-1">Context: "{char.context}"</p>
                                </AlertDescription>
                              </Alert>
                            ))}
                          </div>
                        </div>
                      ) : (
                        <Alert>
                          <CheckCircle className="h-4 w-4" />
                          <AlertTitle>No shadow characters detected</AlertTitle>
                          <AlertDescription>
                            Your text appears to be free of hidden Unicode manipulations.
                          </AlertDescription>
                        </Alert>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            )}
            
            {cleanResult && (
              <TabsContent value="clean">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <FileText className="mr-2 h-5 w-5" />
                      Clean Results
                    </CardTitle>
                    <CardDescription>
                      Shadow characters removed from text
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {cleanResult.modified ? (
                        <Alert>
                          <CheckCircle className="h-4 w-4" />
                          <AlertTitle>Text cleaned successfully</AlertTitle>
                          <AlertDescription>
                            Shadow characters have been removed from your text.
                          </AlertDescription>
                        </Alert>
                      ) : (
                        <Alert>
                          <CheckCircle className="h-4 w-4" />
                          <AlertTitle>No modifications needed</AlertTitle>
                          <AlertDescription>
                            No shadow characters were found in your text.
                          </AlertDescription>
                        </Alert>
                      )}
                      
                      <div className="mt-4">
                        <h3 className="text-sm font-medium mb-1">Original Text:</h3>
                        <div className="p-3 bg-secondary rounded-md text-xs overflow-x-auto whitespace-pre-wrap">
                          {cleanResult.originalText}
                        </div>
                        
                        <h3 className="text-sm font-medium mb-1 mt-4">Cleaned Text:</h3>
                        <div className="p-3 bg-secondary rounded-md text-xs overflow-x-auto whitespace-pre-wrap">
                          {cleanResult.cleanText}
                        </div>
                        
                        <div className="mt-4 grid grid-cols-2 gap-4">
                          <div>
                            <h3 className="text-sm font-medium mb-1">Original Hash:</h3>
                            <div className="p-2 bg-secondary rounded-md text-xs overflow-x-auto">
                              {cleanResult.originalHash}
                            </div>
                          </div>
                          <div>
                            <h3 className="text-sm font-medium mb-1">Clean Hash:</h3>
                            <div className="p-2 bg-secondary rounded-md text-xs overflow-x-auto">
                              {cleanResult.cleanHash}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button 
                      onClick={() => setInputText(cleanResult.cleanText)}
                      className="w-full"
                    >
                      Use Cleaned Text
                    </Button>
                  </CardFooter>
                </Card>
              </TabsContent>
            )}
            
            {neutralizeResult && (
              <TabsContent value="neutralize">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <EyeOff className="mr-2 h-5 w-5" />
                      Neutralize Results
                    </CardTitle>
                    <CardDescription>
                      Shadow characters replaced with visible markers
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {neutralizeResult.modified ? (
                        <Alert>
                          <Zap className="h-4 w-4" />
                          <AlertTitle>Text neutralized successfully</AlertTitle>
                          <AlertDescription>
                            Shadow characters have been replaced with visible markers.
                          </AlertDescription>
                        </Alert>
                      ) : (
                        <Alert>
                          <CheckCircle className="h-4 w-4" />
                          <AlertTitle>No modifications needed</AlertTitle>
                          <AlertDescription>
                            No shadow characters were found in your text.
                          </AlertDescription>
                        </Alert>
                      )}
                      
                      <div className="mt-4">
                        <h3 className="text-sm font-medium mb-1">Original Text:</h3>
                        <div className="p-3 bg-secondary rounded-md text-xs overflow-x-auto whitespace-pre-wrap">
                          {neutralizeResult.originalText}
                        </div>
                        
                        <h3 className="text-sm font-medium mb-1 mt-4">Neutralized Text:</h3>
                        <div className="p-3 bg-secondary rounded-md text-xs overflow-x-auto whitespace-pre-wrap">
                          {neutralizeResult.neutralizedText}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button 
                      onClick={() => setInputText(neutralizeResult.neutralizedText)}
                      className="w-full"
                    >
                      Use Neutralized Text
                    </Button>
                  </CardFooter>
                </Card>
              </TabsContent>
            )}
          </Tabs>
        )}
        
        <Card className="mt-4">
          <CardHeader>
            <CardTitle>About Shadow Sweep</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p>
                <strong>Shadow Sweep</strong> is a Unicode security feature that detects and neutralizes hidden characters 
                and structural manipulations in text content. These invisible characters can be used for:
              </p>
              <ul className="list-disc pl-5 space-y-1">
                <li>Manipulating URLs to look legitimate but direct to malicious sites</li>
                <li>Sneaking unauthorized content past filtering systems</li>
                <li>Creating steganographic side-channels for data exfiltration</li>
                <li>Evading plagiarism detection</li>
              </ul>
              <p>
                Shadow Sweep's advanced character analysis provides protection against these sophisticated attacks,
                ensuring the structural integrity of digital content.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}