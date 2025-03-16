import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Shield, AlertTriangle, Check, Fingerprint, Activity, Lock } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';

interface QuantumEchoStatus {
  initialized: boolean;
  channel_secure: boolean;
  haiku_verified: boolean;
  echo_resonance: number;
  firewall_active: boolean;
  threat_level: number;
  timestamp: string;
}

interface HaikuVerification {
  haiku: string;
  verified: boolean;
  syllable_counts: number[];
}

export default function QuantumEchoVisualizer() {
  const [lastVerification, setLastVerification] = useState<HaikuVerification | null>(null);
  
  // Fetch quantum echo status
  const { data: status, isLoading: statusLoading, error: statusError } = useQuery<QuantumEchoStatus>({
    queryKey: ['/api/quantum-echo/status'],
    refetchInterval: 5000, // Refresh every 5 seconds
    retry: 3,
  });
  
  // Generate and verify a new haiku
  const generateHaiku = async () => {
    try {
      const response = await fetch('/api/quantum-echo/generate-haiku', {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate haiku');
      }
      
      const data = await response.json();
      setLastVerification({
        haiku: data.haiku,
        verified: data.verified,
        syllable_counts: data.syllable_counts
      });
      
    } catch (error) {
      console.error('Error generating haiku:', error);
    }
  };
  
  // Format haiku for display
  const formatHaiku = (haiku: string) => {
    return haiku.split(' / ').map((line, index) => (
      <div key={index} className="my-1">{line}</div>
    ));
  };
  
  // Calculate color based on resonance level
  const getResonanceColor = (resonance: number) => {
    if (resonance >= 0.9) return 'text-green-500';
    if (resonance >= 0.7) return 'text-emerald-400';
    if (resonance >= 0.5) return 'text-yellow-400';
    if (resonance >= 0.3) return 'text-orange-500';
    return 'text-red-500';
  };
  
  // Calculate color based on threat level
  const getThreatColor = (threat: number) => {
    if (threat <= 0.1) return 'text-green-500';
    if (threat <= 0.3) return 'text-emerald-400';
    if (threat <= 0.5) return 'text-yellow-400';
    if (threat <= 0.7) return 'text-orange-500';
    return 'text-red-500';
  };
  
  return (
    <div className="space-y-4 mb-8">
      <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
        <Fingerprint className="h-6 w-6" />
        Quantum Echo Authentication
      </h2>
      
      <Card className="border-none bg-black/20 backdrop-blur-sm text-white">
        <CardHeader>
          <CardTitle className="text-xl">Authentication Status</CardTitle>
          <CardDescription className="text-gray-300">
            Haiku-based verification with 5-7-5 syllable structure
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {statusLoading ? (
            <div className="animate-pulse space-y-4">
              <div className="h-4 bg-gray-700 rounded w-3/4"></div>
              <div className="h-4 bg-gray-700 rounded w-1/2"></div>
              <div className="h-4 bg-gray-700 rounded w-5/6"></div>
            </div>
          ) : statusError ? (
            <div className="text-red-400 flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              <span>Error fetching authentication status</span>
            </div>
          ) : status ? (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Channel Security:</span>
                <Badge variant={status.channel_secure ? 'default' : 'destructive'} className="w-24 flex justify-center">
                  {status.channel_secure ? (
                    <><Check className="mr-1 h-4 w-4" /> Secure</>
                  ) : (
                    <><AlertTriangle className="mr-1 h-4 w-4" /> Insecure</>
                  )}
                </Badge>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Haiku Verification:</span>
                <Badge variant={status.haiku_verified ? 'default' : 'destructive'} className="w-24 flex justify-center">
                  {status.haiku_verified ? (
                    <><Check className="mr-1 h-4 w-4" /> Verified</>
                  ) : (
                    <><AlertTriangle className="mr-1 h-4 w-4" /> Failed</>
                  )}
                </Badge>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Schrödinger Firewall:</span>
                <Badge variant={status.firewall_active ? 'default' : 'destructive'} className="w-24 flex justify-center">
                  {status.firewall_active ? (
                    <><Shield className="mr-1 h-4 w-4" /> Active</>
                  ) : (
                    <><AlertTriangle className="mr-1 h-4 w-4" /> Inactive</>
                  )}
                </Badge>
              </div>
              
              <Separator className="my-4" />
              
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Echo Resonance:</span>
                  <span className={`font-bold ${getResonanceColor(status.echo_resonance)}`}>
                    {(status.echo_resonance * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={status.echo_resonance * 100} className="h-2" />
              </div>
              
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Threat Level:</span>
                  <span className={`font-bold ${getThreatColor(status.threat_level)}`}>
                    {(status.threat_level * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress value={status.threat_level * 100} className="h-2" />
              </div>
              
              <div className="text-xs text-gray-500 mt-4">
                Last updated: {new Date(status.timestamp).toLocaleString()}
              </div>
            </div>
          ) : (
            <div className="text-yellow-400 flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              <span>Authentication system not available</span>
            </div>
          )}
        </CardContent>
        
        <CardFooter className="border-t border-gray-800 pt-4 flex-col items-start gap-4">
          <div className="w-full">
            <h3 className="text-lg font-medium mb-2">Verification Haiku</h3>
            
            {lastVerification ? (
              <div className={`p-4 border rounded-md ${lastVerification.verified ? 'border-green-600 bg-green-900/20' : 'border-red-600 bg-red-900/20'}`}>
                <div className="italic font-medium mb-2">
                  {formatHaiku(lastVerification.haiku)}
                </div>
                <div className="flex justify-between text-sm">
                  <span>Syllable structure:</span>
                  <span className={lastVerification.syllable_counts.join('-') === '5-7-5' ? 'text-green-400' : 'text-red-400'}>
                    {lastVerification.syllable_counts.join('-')}
                  </span>
                </div>
              </div>
            ) : (
              <div className="p-4 border border-gray-700 rounded-md bg-gray-800/20 text-gray-400 italic">
                <div className="my-1">Generate a haiku to</div>
                <div className="my-1">Verify quantum channel</div>
                <div className="my-1">Security state</div>
              </div>
            )}
          </div>
          
          <Button 
            className="w-full mt-2 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
            onClick={generateHaiku}
          >
            <Lock className="mr-2 h-4 w-4" />
            Generate Authentication Haiku
          </Button>
        </CardFooter>
      </Card>
      
      <div className="text-sm text-gray-400 mt-1">
        <Activity className="inline h-4 w-4 mr-1" />
        Quantum Echo Authentication Protocol with 5-7-5 haiku structure ensures channel security through metaphysical pattern verification.
      </div>
    </div>
  );
}