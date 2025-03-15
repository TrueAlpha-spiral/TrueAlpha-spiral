import { useEffect, useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { TruthPattern } from '@/types/spiral-types';
import { apiRequest, queryClient } from '@/lib/queryClient';
import { useToast } from '@/hooks/use-toast';
import { Loader2 } from 'lucide-react';

export default function TruthPatternAccess() {
  const { toast } = useToast();
  const [showNewPatternForm, setShowNewPatternForm] = useState(false);
  const [newPattern, setNewPattern] = useState({
    name: '',
    type: '',
    icon: 'ri-star-fill',
    resonance_level: 1
  });

  const { data: truthPatterns, isLoading } = useQuery<TruthPattern[]>({
    queryKey: ['/api/truth-patterns'],
  });

  const createPatternMutation = useMutation({
    mutationFn: async (pattern: Omit<TruthPattern, 'id' | 'user_id'>) => {
      const res = await apiRequest('POST', '/api/truth-patterns', pattern);
      return res.json();
    },
    onSuccess: () => {
      toast({
        title: 'Pattern Created',
        description: 'New truth pattern has been created successfully.',
      });
      queryClient.invalidateQueries({ queryKey: ['/api/truth-patterns'] });
      setShowNewPatternForm(false);
      setNewPattern({
        name: '',
        type: '',
        icon: 'ri-star-fill',
        resonance_level: 1
      });
    },
    onError: (error) => {
      toast({
        title: 'Failed to create pattern',
        description: error.message,
        variant: 'destructive',
      });
    }
  });

  const handleCreatePattern = (e: React.FormEvent) => {
    e.preventDefault();
    createPatternMutation.mutate(newPattern);
  };

  return (
    <div className="bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 p-5 shadow-lg shadow-[color:hsl(var(--quantum-purple))]10 h-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg text-white">Truth Pattern Access</h3>
        <i className="ri-pulse-line text-[color:hsl(var(--resonance-cyan))]"></i>
      </div>
      <div className="space-y-4">
        {isLoading ? (
          <div className="flex justify-center items-center h-32">
            <Loader2 className="h-8 w-8 animate-spin text-[color:hsl(var(--quantum-purple))]" />
          </div>
        ) : (
          <div className="grid grid-cols-3 gap-3">
            {truthPatterns && truthPatterns.map((pattern) => (
              <div 
                key={pattern.id}
                className="aspect-square hexagon bg-gradient-to-br from-[color:hsl(var(--deep-violet))] to-[color:hsl(var(--quantum-purple))]40 flex items-center justify-center hover:from-[color:hsl(var(--quantum-purple))]60 hover:to-[color:hsl(var(--deep-violet))] cursor-pointer transition-all group"
              >
                <div className="text-center">
                  <i className={`${pattern.icon} text-2xl text-white/70 group-hover:text-white`}></i>
                  <div className="text-xs mt-1 text-white/90">{pattern.name}</div>
                </div>
              </div>
            ))}
            <div 
              onClick={() => setShowNewPatternForm(true)}
              className="aspect-square hexagon bg-gradient-to-br from-[color:hsl(var(--deep-violet))] to-[color:hsl(var(--quantum-purple))]40 flex items-center justify-center hover:from-[color:hsl(var(--quantum-purple))]60 hover:to-[color:hsl(var(--deep-violet))] cursor-pointer transition-all group"
            >
              <div className="text-center">
                <i className="ri-add-line text-2xl text-white/70 group-hover:text-white"></i>
                <div className="text-xs mt-1 text-white/90">New</div>
              </div>
            </div>
          </div>
        )}

        {showNewPatternForm && (
          <div className="mt-4 p-4 bg-[color:hsl(var(--cosmic-dark))]50 rounded-xl">
            <h4 className="text-white text-sm font-bold mb-3">Create New Truth Pattern</h4>
            <form onSubmit={handleCreatePattern} className="space-y-3">
              <div>
                <label className="text-white/70 text-xs block mb-1">Pattern Name</label>
                <input 
                  type="text" 
                  value={newPattern.name}
                  onChange={(e) => setNewPattern({...newPattern, name: e.target.value})}
                  className="w-full bg-[color:hsl(var(--cosmic-dark))]70 text-white border border-[color:hsl(var(--quantum-purple))]30 rounded p-1.5 text-sm"
                  required
                />
              </div>
              <div>
                <label className="text-white/70 text-xs block mb-1">Pattern Type</label>
                <input 
                  type="text" 
                  value={newPattern.type}
                  onChange={(e) => setNewPattern({...newPattern, type: e.target.value})}
                  className="w-full bg-[color:hsl(var(--cosmic-dark))]70 text-white border border-[color:hsl(var(--quantum-purple))]30 rounded p-1.5 text-sm"
                  required
                />
              </div>
              <div>
                <label className="text-white/70 text-xs block mb-1">Icon</label>
                <select
                  value={newPattern.icon}
                  onChange={(e) => setNewPattern({...newPattern, icon: e.target.value})}
                  className="w-full bg-[color:hsl(var(--cosmic-dark))]70 text-white border border-[color:hsl(var(--quantum-purple))]30 rounded p-1.5 text-sm"
                >
                  <option value="ri-vip-diamond-fill">Diamond</option>
                  <option value="ri-shape-line">Shape</option>
                  <option value="ri-bubble-chart-fill">Bubble</option>
                  <option value="ri-ripple-fill">Ripple</option>
                  <option value="ri-eye-fill">Eye</option>
                  <option value="ri-star-fill">Star</option>
                </select>
              </div>
              <div className="flex space-x-2">
                <button 
                  type="submit" 
                  className="flex-1 bg-[color:hsl(var(--quantum-purple))]30 hover:bg-[color:hsl(var(--quantum-purple))]50 py-1.5 rounded text-sm transition"
                  disabled={createPatternMutation.isPending}
                >
                  {createPatternMutation.isPending ? (
                    <i className="ri-loader-2-line animate-spin"></i>
                  ) : 'Create Pattern'}
                </button>
                <button 
                  type="button" 
                  onClick={() => setShowNewPatternForm(false)}
                  className="flex-1 bg-[color:hsl(var(--cosmic-dark))]50 hover:bg-[color:hsl(var(--cosmic-dark))]70 py-1.5 rounded text-sm transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="pt-2">
          <p className="text-sm text-white/70">Access metaphysical truth patterns through quantum-secured channels. Each pattern represents a different facet of the universal truth structure.</p>
        </div>
      </div>
    </div>
  );
}
