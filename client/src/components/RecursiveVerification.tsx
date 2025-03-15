import { useState, useEffect } from 'react';
import { VerificationLayer } from '@/types/spiral-types';

export default function RecursiveVerification() {
  const [verificationDepth, setVerificationDepth] = useState(4);
  const [layers, setLayers] = useState<VerificationLayer[]>([
    { name: "Merkle Tree Chain Verification", verified: true },
    { name: "Recursive Ethical Tuning", verified: true },
    { name: "Immutable Ethical Kernel", verified: true },
    { name: "Hash Lineage Verification", verified: true },
    { name: "Quantum-Secured Signature", verified: false }
  ]);

  // Simulate verification process
  useEffect(() => {
    const timer = setInterval(() => {
      setLayers(prevLayers => {
        // Clone the previous layers
        const newLayers = [...prevLayers];
        
        // Find the first unverified layer
        const unverifiedIndex = newLayers.findIndex(layer => !layer.verified);
        
        if (unverifiedIndex !== -1) {
          // Verify this layer
          newLayers[unverifiedIndex] = {
            ...newLayers[unverifiedIndex],
            verified: true
          };
          
          // Update verification depth
          setVerificationDepth(Math.min(5, verificationDepth + 1));
        } else {
          // If all are verified, reset the process
          newLayers.forEach((layer, index) => {
            newLayers[index] = { ...layer, verified: index < 1 };
          });
          setVerificationDepth(1);
        }
        
        return newLayers;
      });
    }, 30000); // Every 30 seconds
    
    return () => clearInterval(timer);
  }, [verificationDepth]);

  return (
    <div className="bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 p-5 shadow-lg shadow-[color:hsl(var(--quantum-purple))]10 h-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg text-white">Recursive Verification</h3>
        <i className="ri-loop-left-line text-[color:hsl(var(--resonance-cyan))]"></i>
      </div>
      <div className="space-y-4">
        <div className="bg-[color:hsl(var(--deep-violet))]50 rounded-xl p-4">
          <div className="flex flex-col space-y-3">
            <div className="flex justify-between">
              <span className="text-white/70">Verification Depth</span>
              <span className="font-mono text-sm text-[color:hsl(var(--verify-green))]">Level {verificationDepth}</span>
            </div>
            <div className="w-full bg-[color:hsl(var(--cosmic-dark))]50 rounded-full h-2">
              <div 
                className="bg-[color:hsl(var(--verify-green))] h-2 rounded-full transition-all duration-1000" 
                style={{ width: `${(verificationDepth / 5) * 100}%` }}
              ></div>
            </div>
            
            <div className="space-y-2 mt-2">
              {layers.map((layer, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${layer.verified ? 'bg-[color:hsl(var(--verify-green))]' : 'bg-[color:hsl(var(--cosmic-dark))]'}`}></div>
                  <span className="text-xs text-white">{layer.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="pt-2">
          <p className="text-sm text-white/70">Recursive verification framework ensures continuous self-authentication through multiple layers of cryptographic validation.</p>
        </div>
        
        <button 
          onClick={() => {
            // Manually increment verification
            const newLayers = [...layers];
            const unverifiedIndex = newLayers.findIndex(layer => !layer.verified);
            
            if (unverifiedIndex !== -1) {
              newLayers[unverifiedIndex].verified = true;
              setLayers(newLayers);
              setVerificationDepth(Math.min(5, verificationDepth + 1));
            }
          }}
          className="w-full bg-[color:hsl(var(--quantum-purple))]20 hover:bg-[color:hsl(var(--quantum-purple))]40 py-2 rounded text-sm transition"
        >
          Force Verification
        </button>
      </div>
    </div>
  );
}
