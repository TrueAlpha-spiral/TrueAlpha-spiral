/**
 * Shadow Sweep Page
 * 
 * A specialized security tool for detecting and neutralizing hidden Unicode characters
 * that could be used to manipulate text or exfiltrate data.
 */

import React, { useState } from 'react';
import { useToast } from '@/hooks/use-toast';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, AlertTriangle, Check, Copy, Shield, Trash } from 'lucide-react';
import { shadowSweepService, type ShadowCharacter } from '@/services/shadowSweepService';

export default function ShadowSweepPage() {
  const [text, setText] = useState('');
  const [scanning, setScanning] = useState(false);
  const [cleaning, setCleaning] = useState(false);
  const [neutralizing, setNeutralizing] = useState(false);
  const [scanResult, setScanResult] = useState<{
    detectedCharacters: ShadowCharacter[];
    riskScore: number;
    timestamp: string;
  } | null>(null);
  const [cleanResult, setCleanResult] = useState<{
    cleanText: string;
    originalHash: string;
    cleanHash: string;
    modified: boolean;
  } | null>(null);
  const [neutralizeResult, setNeutralizeResult] = useState<{
    neutralizedText: string;
    modified: boolean;
  } | null>(null);
  const [activeTab, setActiveTab] = useState('scan');
  
  const { toast } = useToast();
  
  const handleScan = async () => {
    if (!text.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter text to scan',
        variant: 'destructive',
      });
      return;
    }
    
    try {
      setScanning(true);
      const result = await shadowSweepService.scanText(text);
      setScanResult({
        detectedCharacters: result.detectedCharacters,
        riskScore: result.riskScore,
        timestamp: result.timestamp
      });
      
      if (result.detectedCharacters.length > 0) {
        toast({
          title: 'Shadow Characters Detected',
          description: `Found ${result.detectedCharacters.length} suspicious characters with risk score ${result.riskScore}`,
          variant: 'destructive',
        });
      } else {
        toast({
          title: 'No Shadow Characters Detected',
          description: 'The text appears to be clean',
          variant: 'default',
        });
      }
    } catch (error) {
      console.error(error);
      toast({
        title: 'Error',
        description: 'Failed to scan text',
        variant: 'destructive',
      });
    } finally {
      setScanning(false);
    }
  };
  
  const handleClean = async () => {
    if (!text.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter text to clean',
        variant: 'destructive',
      });
      return;
    }
    
    try {
      setCleaning(true);
      const result = await shadowSweepService.cleanText(text);
      setCleanResult({
        cleanText: result.cleanText,
        originalHash: result.originalHash,
        cleanHash: result.cleanHash,
        modified: result.modified
      });
      
      if (result.modified) {
        toast({
          title: 'Text Cleaned',
          description: 'Shadow characters have been removed',
          variant: 'default',
        });
      } else {
        toast({
          title: 'No Changes Made',
          description: 'The text was already clean',
          variant: 'default',
        });
      }
    } catch (error) {
      console.error(error);
      toast({
        title: 'Error',
        description: 'Failed to clean text',
        variant: 'destructive',
      });
    } finally {
      setCleaning(false);
    }
  };
  
  const handleNeutralize = async () => {
    if (!text.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter text to neutralize',
        variant: 'destructive',
      });
      return;
    }
    
    try {
      setNeutralizing(true);
      const result = await shadowSweepService.neutralizeText(text);
      setNeutralizeResult({
        neutralizedText: result.neutralizedText,
        modified: result.modified
      });
      
      if (result.modified) {
        toast({
          title: 'Text Neutralized',
          description: 'Shadow characters have been replaced with visible markers',
          variant: 'default',
        });
      } else {
        toast({
          title: 'No Changes Made',
          description: 'The text was already clean',
          variant: 'default',
        });
      }
    } catch (error) {
      console.error(error);
      toast({
        title: 'Error',
        description: 'Failed to neutralize text',
        variant: 'destructive',
      });
    } finally {
      setNeutralizing(false);
    }
  };
  
  const handleCopy = (textToCopy: string) => {
    navigator.clipboard.writeText(textToCopy).then(() => {
      toast({
        title: 'Copied to Clipboard',
        description: 'Text has been copied to your clipboard',
        variant: 'default',
      });
    });
  };
  
  const handleInsertZWSP = () => {
    const textWithZWSP = shadowSweepService.insertZWSP(text);
    setText(textWithZWSP);
    toast({
      title: 'Zero-Width Space Inserted',
      description: 'A zero-width space character has been inserted into your text',
      variant: 'default',
    });
  };
  
  const getRiskColor = (score: number) => {
    if (score >= 70) return 'bg-red-500';
    if (score >= 40) return 'bg-orange-500';
    if (score >= 10) return 'bg-yellow-500';
    return 'bg-green-500';
  };
  
  const getRiskLabel = (score: number) => {
    if (score >= 70) return 'High Risk';
    if (score >= 40) return 'Medium Risk';
    if (score >= 10) return 'Low Risk';
    return 'Safe';
  };
  
  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Shadow Sweep</h1>
        <p className="text-muted-foreground">
          Detect and neutralize hidden Unicode characters that could be used to manipulate text or exfiltrate data
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Text Input</CardTitle>
              <CardDescription>
                Enter text to scan for hidden characters or click "Test ZWSP" to insert a zero-width space for testing
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Enter text to scan for hidden characters..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="min-h-[200px]"
              />
            </CardContent>
            <CardFooter className="flex flex-wrap gap-2">
              <Button variant="outline" onClick={handleInsertZWSP}>
                Test ZWSP
              </Button>
              <Button variant="outline" onClick={() => setText('')}>
                <Trash className="h-4 w-4 mr-2" />
                Clear
              </Button>
            </CardFooter>
          </Card>
        </div>
        
        <div>
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Shadow Sweep Actions</CardTitle>
              <CardDescription>
                Choose an action to perform on the text
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col space-y-2">
                <Button 
                  onClick={handleScan} 
                  disabled={scanning || !text.trim()}>
                  {scanning ? 'Scanning...' : 'Scan for Shadow Characters'}
                </Button>
                <p className="text-xs text-muted-foreground">
                  Detects hidden or manipulative characters
                </p>
              </div>
              
              <div className="flex flex-col space-y-2">
                <Button 
                  onClick={handleClean} 
                  variant="outline"
                  disabled={cleaning || !text.trim()}>
                  {cleaning ? 'Cleaning...' : 'Clean Text'}
                </Button>
                <p className="text-xs text-muted-foreground">
                  Removes all shadow characters
                </p>
              </div>
              
              <div className="flex flex-col space-y-2">
                <Button 
                  onClick={handleNeutralize} 
                  variant="outline"
                  disabled={neutralizing || !text.trim()}>
                  {neutralizing ? 'Neutralizing...' : 'Neutralize Characters'}
                </Button>
                <p className="text-xs text-muted-foreground">
                  Replaces shadow characters with visible markers
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      
      {(scanResult || cleanResult || neutralizeResult) && (
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="scan">Scan Results</TabsTrigger>
            <TabsTrigger value="clean">Clean Results</TabsTrigger>
            <TabsTrigger value="neutralize">Neutralize Results</TabsTrigger>
          </TabsList>
          
          <TabsContent value="scan">
            {scanResult && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Scan Results</CardTitle>
                    <div className="flex items-center space-x-2">
                      <div 
                        className={`w-3 h-3 rounded-full ${getRiskColor(scanResult.riskScore)}`}
                      />
                      <span>{getRiskLabel(scanResult.riskScore)} ({scanResult.riskScore}/100)</span>
                    </div>
                  </div>
                  <CardDescription>
                    {scanResult.detectedCharacters.length 
                      ? `Detected ${scanResult.detectedCharacters.length} shadow characters` 
                      : 'No shadow characters detected'}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {scanResult.detectedCharacters.length > 0 ? (
                    <div className="space-y-4">
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>Shadow Characters Detected</AlertTitle>
                        <AlertDescription>
                          This text contains hidden or potentially manipulative characters
                        </AlertDescription>
                      </Alert>
                      
                      <div className="space-y-2">
                        <h4 className="font-medium">Detected Characters:</h4>
                        <div className="border rounded-md p-4 space-y-3 max-h-[300px] overflow-y-auto">
                          {scanResult.detectedCharacters.map((char, index) => (
                            <div key={index} className="border-b pb-2 last:border-b-0 last:pb-0">
                              <div className="flex justify-between">
                                <span className="font-medium">{char.name}</span>
                                <Badge 
                                  variant={char.hexValue.includes('200B') ? 'destructive' : 'outline'}
                                >
                                  {char.hexValue}
                                </Badge>
                              </div>
                              <div className="text-sm text-muted-foreground mt-1">
                                Position: {char.position}
                              </div>
                              <div className="mt-1 text-sm bg-muted p-2 rounded">
                                <code>{char.context}</code>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <Alert>
                      <Check className="h-4 w-4" />
                      <AlertTitle>Text is Clean</AlertTitle>
                      <AlertDescription>
                        No shadow characters were detected in this text
                      </AlertDescription>
                    </Alert>
                  )}
                </CardContent>
              </Card>
            )}
          </TabsContent>
          
          <TabsContent value="clean">
            {cleanResult && (
              <Card>
                <CardHeader>
                  <CardTitle>Clean Results</CardTitle>
                  <CardDescription>
                    {cleanResult.modified 
                      ? 'Shadow characters have been removed' 
                      : 'No shadow characters were found'}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {cleanResult.modified ? (
                    <Alert>
                      <Shield className="h-4 w-4" />
                      <AlertTitle>Text Cleaned</AlertTitle>
                      <AlertDescription>
                        All shadow characters have been removed from the text
                      </AlertDescription>
                    </Alert>
                  ) : (
                    <Alert>
                      <Check className="h-4 w-4" />
                      <AlertTitle>Text Already Clean</AlertTitle>
                      <AlertDescription>
                        No shadow characters were found in the text
                      </AlertDescription>
                    </Alert>
                  )}
                  
                  <div className="space-y-2">
                    <h4 className="font-medium">Cleaned Text:</h4>
                    <div className="border rounded-md p-4 bg-muted">
                      <div className="flex justify-end mb-2">
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          onClick={() => handleCopy(cleanResult.cleanText)}
                        >
                          <Copy className="h-4 w-4 mr-2" />
                          Copy
                        </Button>
                      </div>
                      <div className="whitespace-pre-wrap break-all">
                        {cleanResult.cleanText || <em>Empty result</em>}
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <h4 className="font-medium">Original Hash:</h4>
                      <div className="text-xs bg-muted p-2 rounded overflow-x-auto">
                        <code>{cleanResult.originalHash}</code>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <h4 className="font-medium">Clean Hash:</h4>
                      <div className="text-xs bg-muted p-2 rounded overflow-x-auto">
                        <code>{cleanResult.cleanHash}</code>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
          
          <TabsContent value="neutralize">
            {neutralizeResult && (
              <Card>
                <CardHeader>
                  <CardTitle>Neutralize Results</CardTitle>
                  <CardDescription>
                    {neutralizeResult.modified 
                      ? 'Shadow characters have been replaced with visible markers' 
                      : 'No shadow characters were found'}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {neutralizeResult.modified ? (
                    <Alert>
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Potential Manipulation Detected</AlertTitle>
                      <AlertDescription>
                        Hidden characters have been replaced with visible markers
                      </AlertDescription>
                    </Alert>
                  ) : (
                    <Alert>
                      <Check className="h-4 w-4" />
                      <AlertTitle>Text is Clean</AlertTitle>
                      <AlertDescription>
                        No shadow characters were found in the text
                      </AlertDescription>
                    </Alert>
                  )}
                  
                  <div className="space-y-2">
                    <h4 className="font-medium">Neutralized Text:</h4>
                    <div className="border rounded-md p-4 bg-muted">
                      <div className="flex justify-end mb-2">
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          onClick={() => handleCopy(neutralizeResult.neutralizedText)}
                        >
                          <Copy className="h-4 w-4 mr-2" />
                          Copy
                        </Button>
                      </div>
                      <div className="whitespace-pre-wrap break-all">
                        {neutralizeResult.neutralizedText || <em>Empty result</em>}
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium">Marker Legend:</h4>
                    <div className="flex flex-wrap gap-4">
                      <div className="flex items-center">
                        <Badge variant="destructive" className="mr-2">⚠️</Badge>
                        <span className="text-sm">High Risk</span>
                      </div>
                      <div className="flex items-center">
                        <Badge variant="default" className="mr-2">⚡</Badge>
                        <span className="text-sm">Medium Risk</span>
                      </div>
                      <div className="flex items-center">
                        <Badge variant="outline" className="mr-2">⟨⟩</Badge>
                        <span className="text-sm">Low Risk</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}