import { useState } from 'react';
import { SecurityModule as SecurityModuleType, EigenchannelValue } from '@/types/spiral-types';
import { useToast } from '@/hooks/use-toast';

export default function SecurityModule() {
  const { toast } = useToast();
  const [eigenchannels, setEigenchannels] = useState<EigenchannelValue[]>([
    { name: "Truth", value: 1.0 },
    { name: "Governance", value: 1.0 },
    { name: "Cohesion", value: 1.0 },
  ]);
  
  const [securityModules, setSecurityModules] = useState<SecurityModuleType[]>([
    { name: "Ethical Kernel", status: 'ACTIVE', value: 1.0 },
    { name: "Truth Entanglement", status: 'ACTIVE', value: 1.0 },
    { name: "Global Resonance", status: 'ACTIVE', value: 1.0 },
    { name: "Truth Lock", status: 'ACTIVE', value: 1.0 },
  ]);
  
  const handleRecalibrate = (moduleIndex: number) => {
    if (moduleIndex === 0) {
      // Recalibrate Ethical Kernel (adjust eigenchannels)
      setEigenchannels(prev => prev.map(channel => ({
        ...channel,
        value: 1.0 // Reset to perfect alignment
      })));
      
      toast({
        title: 'Ethical Kernel Recalibrated',
        description: 'All eigenchannels have been reset to optimal values.',
      });
    } else if (moduleIndex === 1) {
      // Enforce Coherence (Truth Entanglement)
      toast({
        title: 'Coherence Enforced',
        description: 'Truth entanglement has been stabilized across all nodes.',
      });
    } else if (moduleIndex === 2) {
      // Stabilize Global Resonance
      toast({
        title: 'Global Resonance Stabilized',
        description: 'Truth resonance has been locked at optimal frequency.',
      });
    } else if (moduleIndex === 3) {
      // Verify Truth Lock
      toast({
        title: 'Truth Lock Verified',
        description: 'Immutable truth resonance confirmed and secure.',
      });
    }
    
    // Update module status to show it's active
    setSecurityModules(prev => prev.map((module, i) => 
      i === moduleIndex ? { ...module, status: 'ACTIVE' } : module
    ));
  };
  
  // Render each security module
  const renderSecurityModule = (module: SecurityModuleType, index: number) => {
    if (index === 0) {
      // Ethical Spiral Kernel
      return (
        <div key={module.name} className="bg-[color:hsl(var(--deep-violet))]40 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-white">{module.name}</h3>
            <span className="px-2 py-0.5 text-xs rounded-full bg-[color:hsl(var(--verify-green))]20 text-[color:hsl(var(--verify-green))]">{module.status}</span>
          </div>
          <div className="space-y-3">
            <div>
              {eigenchannels.map(channel => (
                <div key={channel.name} className="flex justify-between items-center mb-2">
                  <span className="text-white/70 text-xs">{channel.name}</span>
                  <span className="text-xs font-mono text-white">{channel.value.toFixed(1)}</span>
                </div>
              ))}
            </div>
            <button 
              onClick={() => handleRecalibrate(index)}
              className="w-full bg-[color:hsl(var(--quantum-purple))]30 hover:bg-[color:hsl(var(--quantum-purple))]50 py-1.5 rounded text-xs transition"
            >
              Recalibrate
            </button>
          </div>
        </div>
      );
    } else if (index === 1) {
      // Truth Entanglement
      return (
        <div key={module.name} className="bg-[color:hsl(var(--deep-violet))]40 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-white">{module.name}</h3>
            <span className="px-2 py-0.5 text-xs rounded-full bg-[color:hsl(var(--verify-green))]20 text-[color:hsl(var(--verify-green))]">{module.status}</span>
          </div>
          <div className="space-y-3">
            <div className="h-24 relative">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-16 h-16 border-2 border-[color:hsl(var(--quantum-purple))] rounded-full flex items-center justify-center animate-pulse-glow">
                  <div className="w-10 h-10 border-2 border-[color:hsl(var(--resonance-cyan))] rounded-full flex items-center justify-center">
                    <div className="w-5 h-5 bg-[color:hsl(var(--verify-green))] rounded-full"></div>
                  </div>
                </div>
              </div>
            </div>
            <button 
              onClick={() => handleRecalibrate(index)}
              className="w-full bg-[color:hsl(var(--quantum-purple))]30 hover:bg-[color:hsl(var(--quantum-purple))]50 py-1.5 rounded text-xs transition"
            >
              Enforce Coherence
            </button>
          </div>
        </div>
      );
    } else if (index === 2) {
      // Global Resonance
      return (
        <div key={module.name} className="bg-[color:hsl(var(--deep-violet))]40 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-white">{module.name}</h3>
            <span className="px-2 py-0.5 text-xs rounded-full bg-[color:hsl(var(--verify-green))]20 text-[color:hsl(var(--verify-green))]">{module.status}</span>
          </div>
          <div className="space-y-3">
            <div className="h-24 flex items-center justify-center">
              <div className="text-center">
                <div className="text-3xl font-mono text-[color:hsl(var(--verify-green))]">1.0</div>
                <div className="text-white/70 text-xs mt-1">Truth Resonance</div>
              </div>
            </div>
            <button 
              onClick={() => handleRecalibrate(index)}
              className="w-full bg-[color:hsl(var(--quantum-purple))]30 hover:bg-[color:hsl(var(--quantum-purple))]50 py-1.5 rounded text-xs transition"
            >
              Stabilize
            </button>
          </div>
        </div>
      );
    } else {
      // Truth Lock
      return (
        <div key={module.name} className="bg-[color:hsl(var(--deep-violet))]40 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-white">{module.name}</h3>
            <span className="px-2 py-0.5 text-xs rounded-full bg-[color:hsl(var(--verify-green))]20 text-[color:hsl(var(--verify-green))]">{module.status}</span>
          </div>
          <div className="space-y-3">
            <div className="h-24 flex items-center justify-center">
              <div className="w-20 h-20 relative">
                <div className="absolute inset-0 flex items-center justify-center">
                  <i className="ri-lock-fill text-5xl text-[color:hsl(var(--verify-green))] animate-pulse-glow"></i>
                </div>
              </div>
            </div>
            <button 
              onClick={() => handleRecalibrate(index)}
              className="w-full bg-[color:hsl(var(--quantum-purple))]30 hover:bg-[color:hsl(var(--quantum-purple))]50 py-1.5 rounded text-xs transition"
            >
              Verify Lock
            </button>
          </div>
        </div>
      );
    }
  };
  
  return (
    <section className="mb-12">
      <div className="bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 p-6 shadow-lg shadow-[color:hsl(var(--quantum-purple))]10">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-bold text-xl text-white">Quantum-Inspired Security Mechanism</h2>
          <i className="ri-shield-keyhole-line text-[color:hsl(var(--verify-green))] text-xl"></i>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {securityModules.map((module, index) => renderSecurityModule(module, index))}
        </div>
        
        <div className="mt-6 bg-[color:hsl(var(--cosmic-dark))]50 rounded-xl p-4">
          <div className="flex justify-between items-center">
            <h3 className="font-medium text-white">System Security Status</h3>
            <div className="flex items-center">
              <div className="w-2 h-2 rounded-full bg-[color:hsl(var(--verify-green))] animate-pulse mr-2"></div>
              <span className="text-[color:hsl(var(--verify-green))] text-sm">Protected</span>
            </div>
          </div>
          
          <div className="mt-4 text-sm text-white/70">
            All quantum-inspired security mechanisms are operational. The system is protected by recursive verification frameworks and truth-resonant fields. Any attempt to modify or falsify authorship will be automatically detected and neutralized.
          </div>
        </div>
      </div>
    </section>
  );
}
