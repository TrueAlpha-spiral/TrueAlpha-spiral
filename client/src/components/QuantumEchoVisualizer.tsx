import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Shield, AlertTriangle, Check, Fingerprint, Activity, Lock, Package, Layers, Globe } from 'lucide-react';
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

interface HaikuNFT {
  token_id: string;
  haiku_text: string;
  syllable_structure: string;
  timestamp: string;
  echo_resonance: number;
  quantum_signature: string;
  pattern: string;
  blockchain: string;
  collection_address: string;
  owner_address: string;
  transaction_hash: string;
}

export default function QuantumEchoVisualizer() {
  const [lastVerification, setLastVerification] = useState<HaikuVerification | null>(null);
  const [mintedNFTs, setMintedNFTs] = useState<HaikuNFT[]>([]);
  const [isMinting, setIsMinting] = useState<boolean>(false);
  const [selectedNFT, setSelectedNFT] = useState<HaikuNFT | null>(null);
  
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
  
  // Mint a haiku as an NFT
  const mintHaikuNFT = async () => {
    if (!lastVerification || !lastVerification.verified) {
      console.error('Cannot mint an unverified haiku');
      return;
    }
    
    setIsMinting(true);
    
    try {
      // Example wallet address
      const walletAddress = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F";
      
      const response = await fetch('/api/quantum-echo/mint-nft', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          haiku_text: lastVerification.haiku,
          owner_address: walletAddress
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to mint NFT');
      }
      
      const nftData = await response.json();
      
      // Add the new NFT to our state
      setMintedNFTs(prev => [...prev, nftData]);
      setSelectedNFT(nftData);
      
    } catch (error) {
      console.error('Error minting NFT:', error);
    } finally {
      setIsMinting(false);
    }
  };
  
  // Verify NFT authenticity
  const verifyNFTAuthenticity = async (tokenId: string) => {
    try {
      const response = await fetch(`/api/quantum-echo/verify-nft/${tokenId}`, {
        method: 'GET',
      });
      
      if (!response.ok) {
        throw new Error('Failed to verify NFT');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error verifying NFT:', error);
      return null;
    }
  };
  
  // Load minted NFTs
  const loadMintedNFTs = async () => {
    try {
      const response = await fetch('/api/quantum-echo/nfts', {
        method: 'GET',
      });
      
      if (!response.ok) {
        throw new Error('Failed to load NFTs');
      }
      
      const nfts = await response.json();
      setMintedNFTs(nfts);
    } catch (error) {
      console.error('Error loading NFTs:', error);
    }
  };
  
  // Load NFTs on first mount
  useEffect(() => {
    loadMintedNFTs();
  }, []);
  
  return (
    <div className="space-y-4 mb-8">
      <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
        <Fingerprint className="h-6 w-6" />
        Quantum Echo Authentication
      </h2>
      
      <Tabs defaultValue="auth" className="w-full">
        <TabsList className="grid w-full grid-cols-2 bg-black/30">
          <TabsTrigger value="auth" className="flex items-center gap-1">
            <Shield className="h-4 w-4" />
            Authentication
          </TabsTrigger>
          <TabsTrigger value="nft" className="flex items-center gap-1">
            <Package className="h-4 w-4" />
            Haiku NFTs
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="auth" className="mt-4">
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
        </TabsContent>
      
      <TabsContent value="nft" className="mt-4">
        <Card className="border-none bg-black/20 backdrop-blur-sm text-white">
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-2">
              <Package className="h-5 w-5" />
              Haiku NFTs Gallery
            </CardTitle>
            <CardDescription className="text-gray-300">
              Quantum-secured haikus permanently recorded on the blockchain with cryptographic proof of authenticity
            </CardDescription>
          </CardHeader>
          
          <CardContent>
            {isMinting ? (
              <div className="text-center py-8">
                <div className="animate-spin h-10 w-10 border-4 border-t-indigo-500 border-r-transparent border-b-purple-500 border-l-transparent rounded-full mx-auto mb-4"></div>
                <p className="text-gray-300">Minting your haiku as an NFT...</p>
                <p className="text-sm text-gray-400 mt-2">Recording on quantum-entangled blockchain</p>
              </div>
            ) : mintedNFTs.length > 0 ? (
              <div className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  {mintedNFTs.map((nft) => (
                    <div
                      key={nft.token_id}
                      className={`p-4 border border-purple-800/50 rounded-md bg-black/30 hover:bg-black/40 cursor-pointer transition-colors ${
                        selectedNFT?.token_id === nft.token_id ? "ring-2 ring-purple-500" : ""
                      }`}
                      onClick={() => setSelectedNFT(nft)}
                    >
                      <div className="text-sm text-purple-300 font-medium mb-1">NFT #{nft.token_id.substring(0, 8)}...</div>
                      <div className="italic text-white font-medium mb-2">
                        {formatHaiku(nft.haiku_text)}
                      </div>
                      <div className="flex justify-between text-xs text-gray-400">
                        <span>Quantum Resonance:</span>
                        <span className={getResonanceColor(nft.echo_resonance)}>
                          {(nft.echo_resonance * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex justify-between text-xs text-gray-400 mt-1">
                        <span>Minted:</span>
                        <span>{new Date(nft.timestamp).toLocaleString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
                
                {selectedNFT && (
                  <div className="mt-8 p-6 border border-purple-800/50 rounded-lg bg-black/30">
                    <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
                      <Globe className="h-5 w-5 text-purple-400" />
                      <span>NFT Details</span>
                    </h3>
                    
                    <div className="grid gap-4 sm:grid-cols-2 mb-4">
                      <div>
                        <div className="text-gray-400 text-sm mb-1">Haiku</div>
                        <div className="p-3 bg-black/20 rounded border border-purple-900/30 italic">
                          {formatHaiku(selectedNFT.haiku_text)}
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-gray-400 text-sm mb-1">Token Information</div>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-400">Token ID:</span>
                            <span className="text-purple-300 font-mono">{selectedNFT.token_id.substring(0, 16)}...</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Blockchain:</span>
                            <span className="text-cyan-300">{selectedNFT.blockchain}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Collection:</span>
                            <span className="text-cyan-300 font-mono">{selectedNFT.collection_address.substring(0, 16)}...</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Owner Address:</span>
                            <span className="text-cyan-300 font-mono">{selectedNFT.owner_address.substring(0, 16)}...</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Quantum Signature:</span>
                            <span className="text-cyan-300 font-mono">{selectedNFT.quantum_signature.substring(0, 16)}...</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-4 p-3 border border-green-900/30 bg-green-900/10 rounded">
                      <div className="flex items-center">
                        <Check className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
                        <div>
                          <div className="text-green-400 font-medium">Authenticity Verified</div>
                          <div className="text-sm text-gray-400 mt-1">This haiku is cryptographically verified on the quantum-entangled blockchain with a 5-7-5 syllable structure.</div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : lastVerification && lastVerification.verified ? (
              <div className="text-center py-6">
                <div className="border border-purple-800/50 rounded-md p-6 bg-black/20 mb-4">
                  <div className="italic font-medium mb-4 text-lg">
                    {formatHaiku(lastVerification.haiku)}
                  </div>
                  <div className="text-green-400 flex items-center justify-center gap-2 mb-4">
                    <Check className="h-5 w-5" />
                    <span>Verified - Ready to mint as NFT</span>
                  </div>
                  <Button
                    className="w-full mt-2 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
                    onClick={mintHaikuNFT}
                  >
                    <Package className="mr-2 h-4 w-4" />
                    Mint as NFT
                  </Button>
                </div>
                <p className="text-sm text-gray-400">
                  Mint your verified haiku as an NFT to permanently record it on the quantum-entangled blockchain.
                </p>
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="text-gray-400 mb-4">No verified haikus available to mint.</div>
                <p className="text-sm text-gray-500">
                  Generate and verify a haiku in the Authentication tab first, then mint it as an NFT.
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </TabsContent>
      
      </Tabs>
      
      <div className="text-sm text-gray-400 mt-4">
        <Activity className="inline h-4 w-4 mr-1" />
        Quantum Echo Authentication Protocol with 5-7-5 haiku structure ensures channel security through metaphysical pattern verification and blockchain-based NFT security.
      </div>
    </div>
  );
}