import { useState } from 'react';
import { calculateSovereignty } from '@/lib/cryptoUtils';

export default function SovereignEquation() {
  const [truth, setTruth] = useState(1.0);
  const [distance, setDistance] = useState(1.0);
  const [size, setSize] = useState(1.0);
  
  const sovereignty = calculateSovereignty(truth, distance, size);
  
  return (
    <div className="bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 p-5 shadow-lg shadow-[color:hsl(var(--quantum-purple))]10">
      <h2 className="font-bold text-lg text-white mb-3">Sovereign Equation</h2>
      <div className="flex items-center justify-center py-3 px-4 bg-[color:hsl(var(--deep-violet))]50 rounded-xl">
        <div className="text-center">
          <div className="text-xl font-mono text-[color:hsl(var(--resonance-cyan))]">
            <div className="mb-1">Sovereignty = {sovereignty}</div>
            <div className="border-b-2 border-[color:hsl(var(--quantum-purple))] my-1"></div>
            <div className="flex justify-center items-center">
              <span className="text-[color:hsl(var(--verify-green))]">{truth.toFixed(1)}</span>
              <span className="mx-1 text-white">/</span>
              <span className="text-white">{distance.toFixed(1)}</span>
            </div>
            <span className="mx-2 text-white">&gt;&lt;</span>
            <span className="text-[color:hsl(var(--quantum-purple))]">{size.toFixed(1)}</span>
          </div>
        </div>
      </div>
      <p className="text-white/70 text-sm mt-3">Mathematical representation of sovereign truth distribution across dimensional boundaries</p>
      
      <div className="mt-4 space-y-3">
        <div className="space-y-1">
          <div className="flex justify-between items-center">
            <label className="text-white/70 text-xs">Truth</label>
            <span className="text-[color:hsl(var(--verify-green))] text-xs">{truth.toFixed(1)}</span>
          </div>
          <input 
            type="range"
            min="0.1"
            max="2"
            step="0.1"
            value={truth}
            onChange={(e) => setTruth(parseFloat(e.target.value))}
            className="w-full h-1 bg-[color:hsl(var(--cosmic-dark))]70 rounded-lg appearance-none cursor-pointer accent-[color:hsl(var(--verify-green))]"
          />
        </div>
        
        <div className="space-y-1">
          <div className="flex justify-between items-center">
            <label className="text-white/70 text-xs">Distance</label>
            <span className="text-white text-xs">{distance.toFixed(1)}</span>
          </div>
          <input 
            type="range"
            min="0.1"
            max="2"
            step="0.1"
            value={distance}
            onChange={(e) => setDistance(parseFloat(e.target.value))}
            className="w-full h-1 bg-[color:hsl(var(--cosmic-dark))]70 rounded-lg appearance-none cursor-pointer accent-white"
          />
        </div>
        
        <div className="space-y-1">
          <div className="flex justify-between items-center">
            <label className="text-white/70 text-xs">Size</label>
            <span className="text-[color:hsl(var(--quantum-purple))] text-xs">{size.toFixed(1)}</span>
          </div>
          <input 
            type="range"
            min="0.1"
            max="2"
            step="0.1"
            value={size}
            onChange={(e) => setSize(parseFloat(e.target.value))}
            className="w-full h-1 bg-[color:hsl(var(--cosmic-dark))]70 rounded-lg appearance-none cursor-pointer accent-[color:hsl(var(--quantum-purple))]"
          />
        </div>
      </div>
    </div>
  );
}
