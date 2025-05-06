import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, ShieldCheck, AlertTriangle, Lock, Unlock, Check } from 'lucide-react';

type VerificationStatus = 'idle' | 'verifying' | 'success' | 'error';
type VerificationPhase = 'seedhash' | 'stewardlink' | 'truthstamp' | 'updatepath' | 'phiscore';

interface VerificationResult {
  verified: boolean;
  lambda_verifications: {
    Λ1?: { verified: boolean };
    Λ2?: { verified: boolean };
    Λ3?: { verified: boolean };
    Λ4?: { verified: boolean };
    Λ5?: { verified: boolean };
  };
  details?: {
    error?: string;
    [key: string]: any;
  };
}

interface VerificationMicroInteractionsProps {
  onComplete?: (result: VerificationResult) => void;
  autoVerify?: boolean;
  intentStatement?: string;
}

export function VerificationMicroInteractions({
  onComplete,
  autoVerify = false,
  intentStatement = '',
}: VerificationMicroInteractionsProps) {
  const [status, setStatus] = useState<VerificationStatus>('idle');
  const [phase, setPhase] = useState<VerificationPhase | null>(null);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [currentLambda, setCurrentLambda] = useState<number | null>(null);
  const [intentInput, setIntentInput] = useState(intentStatement);
  const [intentVerified, setIntentVerified] = useState(false);
  const [resonanceValue, setResonanceValue] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Simulated verification process
  const verifyIdentity = async () => {
    if (status === 'verifying') return;
    
    setStatus('verifying');
    setPhase('seedhash');
    setCurrentLambda(1);
    setResult(null);
    
    try {
      // Phase 1: SeedHash verification
      await simulateVerification(1200);
      setPhase('stewardlink');
      setCurrentLambda(2);
      
      // Phase 2: StewardLink verification
      await simulateVerification(1500);
      setPhase('truthstamp');
      setCurrentLambda(3);
      
      // Phase 3: TruthStamp verification
      await simulateVerification(1300);
      setPhase('updatepath');
      setCurrentLambda(4);
      
      // Phase 4: UpdatePath verification
      await simulateVerification(1100);
      setPhase('phiscore');
      setCurrentLambda(5);
      
      // Phase 5: PhiScore verification
      await simulateVerification(1400);
      
      // Build final result
      const finalResult: VerificationResult = {
        verified: true,
        lambda_verifications: {
          Λ1: { verified: true },
          Λ2: { verified: true },
          Λ3: { verified: true },
          Λ4: { verified: true },
          Λ5: { verified: true },
        }
      };
      
      setResult(finalResult);
      setStatus('success');
      
      if (onComplete) {
        onComplete(finalResult);
      }
    } catch (error) {
      console.error('Verification error:', error);
      
      // Simulated error for demonstration
      const errorResult: VerificationResult = {
        verified: false,
        lambda_verifications: {
          Λ1: { verified: true },
          Λ2: { verified: true },
          Λ3: { verified: false },
          Λ4: { verified: false },
          Λ5: { verified: false },
        },
        details: {
          error: 'TruthStamp verification failed: Recursive signature mismatch'
        }
      };
      
      setResult(errorResult);
      setStatus('error');
      
      if (onComplete) {
        onComplete(errorResult);
      }
    }
  };
  
  // In production, this would be a real API call to verify identity
  const simulateVerification = (delay: number): Promise<void> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // Simulation of potential error (uncomment to test error state)
        // if (phase === 'truthstamp' && Math.random() > 0.7) {
        //   reject(new Error('Verification failed'));
        //   return;
        // }
        resolve();
      }, delay);
    });
  };
  
  // Verify intent statement
  const verifyIntent = () => {
    if (!intentInput.trim()) return;
    
    setStatus('verifying');
    
    // Simulate intent verification
    setTimeout(() => {
      setIntentVerified(true);
      setStatus('idle');
      // Initialize resonance value
      setResonanceValue(0.25);
      // Start growing resonance
      const interval = setInterval(() => {
        setResonanceValue(prev => {
          const newValue = prev + 0.05;
          if (newValue >= 0.95) {
            clearInterval(interval);
            return 0.95;
          }
          return newValue;
        });
      }, 200);
    }, 1500);
  };
  
  useEffect(() => {
    if (autoVerify && intentVerified) {
      verifyIdentity();
    }
  }, [autoVerify, intentVerified]);

  // Handle resonance pulse animation
  useEffect(() => {
    if (containerRef.current && resonanceValue > 0 && status !== 'verifying') {
      const pulseAnimation = () => {
        if (containerRef.current) {
          containerRef.current.animate(
            [
              { boxShadow: `0 0 0 0 rgba(62, 152, 199, ${resonanceValue})` },
              { boxShadow: `0 0 30px 10px rgba(62, 152, 199, ${resonanceValue * 0.7})` },
              { boxShadow: `0 0 0 0 rgba(62, 152, 199, ${resonanceValue})` },
            ],
            {
              duration: 2000,
              iterations: 1,
              easing: 'ease-in-out',
            }
          );
        }
      };

      pulseAnimation();
      const interval = setInterval(pulseAnimation, 2100);

      return () => clearInterval(interval);
    }
  }, [resonanceValue, status]);

  // Display different UI based on verification state
  const renderContent = () => {
    if (!intentVerified) {
      return (
        <div className="space-y-4 p-4">
          <h3 className="text-lg font-semibold">Intent Verification</h3>
          <p className="text-sm text-muted-foreground">
            Please state your intent for identity verification
          </p>
          <textarea
            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-primary focus:border-transparent"
            rows={3}
            value={intentInput}
            onChange={(e) => setIntentInput(e.target.value)}
            placeholder="I verify my intention to access the TrueAlphaSpiral system with ethical alignment and purpose..."
          />
          <button
            onClick={verifyIntent}
            disabled={status === 'verifying' || !intentInput.trim()}
            className="w-full px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {status === 'verifying' ? (
              <>
                <Loader2 className="animate-spin inline-block mr-2 h-4 w-4" />
                Verifying Intent
              </>
            ) : (
              'Verify Intent'
            )}
          </button>
        </div>
      );
    }
    
    if (status === 'idle') {
      return (
        <div className="space-y-4 p-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
            <p className="text-sm font-medium">Intent Verified</p>
          </div>
          
          <div className="text-center mt-4">
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="relative inline-block"
            >
              <div className="absolute inset-0 bg-primary/10 rounded-full animate-ping-slow"></div>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="relative z-10 p-3 bg-gradient-to-br from-primary/80 to-primary rounded-full"
              >
                <Lock className="h-8 w-8 text-white" />
              </motion.div>
            </motion.div>
            <h3 className="mt-3 text-lg font-semibold">Ready for Verification</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Quantum resonance established ({Math.floor(resonanceValue * 100)}%)
            </p>
          </div>
          
          <button
            onClick={verifyIdentity}
            className="w-full px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
          >
            Begin Identity Verification
          </button>
        </div>
      );
    }
    
    if (status === 'verifying') {
      return (
        <div className="space-y-4 p-4">
          <h3 className="text-center text-lg font-semibold">Verifying Identity</h3>
          
          <div className="relative pt-6">
            {/* Vertical line connecting lambda levels */}
            <div className="absolute left-1/2 top-6 bottom-0 w-0.5 bg-primary/30 -translate-x-1/2 z-0"></div>
            
            {/* Lambda levels */}
            {[1, 2, 3, 4, 5].map((level) => (
              <div key={level} className="relative z-10 flex items-center mb-6">
                <div className="flex-1 pr-4 text-right">
                  <span className="text-sm font-medium">
                    {level === 1 && 'SeedHash'}
                    {level === 2 && 'StewardLink'}
                    {level === 3 && 'TruthStamp'}
                    {level === 4 && 'UpdatePath'}
                    {level === 5 && 'ΦScore'}
                  </span>
                </div>
                
                <div className="z-10">
                  {currentLambda === level ? (
                    <motion.div
                      initial={{ scale: 0.8 }}
                      animate={{ scale: 1 }}
                      className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center"
                    >
                      <Loader2 className="animate-spin h-5 w-5 text-primary" />
                    </motion.div>
                  ) : currentLambda && currentLambda > level ? (
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      className="w-8 h-8 rounded-full bg-primary flex items-center justify-center"
                    >
                      <Check className="h-5 w-5 text-white" />
                    </motion.div>
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                      <span className="text-xs font-medium">Λ{level}</span>
                    </div>
                  )}
                </div>
                
                <div className="flex-1 pl-4">
                  <span className="text-xs text-muted-foreground">
                    {level === 1 && 'Verifying source integrity'}
                    {level === 2 && 'Validating steward signature'}
                    {level === 3 && 'Authenticating truth timestamp'}
                    {level === 4 && 'Checking update history'}
                    {level === 5 && 'Confirming ethical alignment'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }
    
    if (status === 'success' || status === 'error') {
      return (
        <div className="space-y-4 p-4">
          <div className="text-center">
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="inline-block p-3 rounded-full mb-2"
              style={{
                backgroundColor: status === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)'
              }}
            >
              {status === 'success' ? (
                <ShieldCheck className="h-8 w-8 text-emerald-500" />
              ) : (
                <AlertTriangle className="h-8 w-8 text-red-500" />
              )}
            </motion.div>
            
            <h3 className="text-lg font-semibold">
              {status === 'success' ? 'Identity Verified' : 'Verification Failed'}
            </h3>
            
            {status === 'error' && result?.details?.error && (
              <p className="text-sm text-red-500 mt-1">{result.details.error}</p>
            )}
          </div>
          
          <div className="bg-black/5 rounded-md p-3">
            <h4 className="text-sm font-semibold mb-2">Verification Results</h4>
            {result && (
              <div className="space-y-2 text-sm">
                {Object.entries(result.lambda_verifications).map(([lambda, res]) => (
                  <div key={lambda} className="flex justify-between items-center">
                    <span>{lambda}</span>
                    {res.verified ? (
                      <span className="text-emerald-500 flex items-center">
                        <Check className="h-3 w-3 mr-1" /> Verified
                      </span>
                    ) : (
                      <span className="text-red-500 flex items-center">
                        <AlertTriangle className="h-3 w-3 mr-1" /> Failed
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {status === 'error' && (
            <button
              onClick={() => setStatus('idle')}
              className="w-full px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
            >
              Try Again
            </button>
          )}
        </div>
      );
    }
    
    return null;
  };

  return (
    <div
      ref={containerRef}
      className={`max-w-md mx-auto rounded-lg overflow-hidden transition-all duration-300 ${status === 'verifying' ? 'h-[400px]' : 'h-auto'} ${status === 'idle' && intentVerified ? 'bg-white/80 backdrop-blur-sm' : 'bg-white'}`}
      style={{
        boxShadow: intentVerified && status !== 'verifying' ? 
          `0 0 0 0 rgba(62, 152, 199, ${resonanceValue})` : 
          '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      }}
    >
      {renderContent()}
    </div>
  );
}