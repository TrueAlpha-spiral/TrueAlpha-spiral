import { useState, useCallback, useEffect } from 'react';
import { 
  trueAlphaSpiral, 
  MetricState, 
  MetricWeights 
} from '@/lib/trueAlphaSpiral';

interface TrueAlphaSpiralOptions {
  initialState: MetricState;
  thetaTarget?: number;
  alpha?: number;
  weights: MetricWeights;
  creatorSig: string;
  autoIterate?: boolean;
  iterationInterval?: number;
  targetThreshold?: number;
}

export function useTrueAlphaSpiral({
  initialState,
  thetaTarget = 0.9,
  alpha = 0.5,
  weights,
  creatorSig,
  autoIterate = false,
  iterationInterval = 5000, // 5 seconds by default
  targetThreshold = 0.85 // Stop auto iterations when metrics reach this threshold
}: TrueAlphaSpiralOptions) {
  const [currentState, setCurrentState] = useState<MetricState>(initialState);
  const [hashChain, setHashChain] = useState<string[]>(['0'.repeat(64)]); // Initial hash
  const [iterationCount, setIterationCount] = useState(0);
  const [isIterating, setIsIterating] = useState(autoIterate);
  const [isTargetReached, setIsTargetReached] = useState(false);

  // Check if all metrics have reached target threshold
  const checkTargetReached = useCallback((state: MetricState) => {
    return Object.values(state).every(value => value >= targetThreshold);
  }, [targetThreshold]);

  // Perform a single iteration
  const iterate = useCallback(() => {
    if (isTargetReached) return;

    const prevHash = hashChain[hashChain.length - 1];
    const { nextState, hash } = trueAlphaSpiral(
      currentState,
      thetaTarget,
      alpha,
      weights,
      creatorSig,
      prevHash
    );

    setCurrentState(nextState);
    setHashChain(prev => [...prev, hash]);
    setIterationCount(prev => prev + 1);
    
    const targetReached = checkTargetReached(nextState);
    if (targetReached) {
      setIsTargetReached(true);
      setIsIterating(false);
    }
  }, [
    currentState, 
    thetaTarget, 
    alpha, 
    weights, 
    creatorSig, 
    hashChain, 
    checkTargetReached, 
    isTargetReached
  ]);

  // Start automated iterations
  const startIterating = useCallback(() => {
    if (!isTargetReached) {
      setIsIterating(true);
    }
  }, [isTargetReached]);

  // Stop automated iterations
  const stopIterating = useCallback(() => {
    setIsIterating(false);
  }, []);

  // Reset to initial state
  const reset = useCallback(() => {
    setCurrentState(initialState);
    setHashChain(['0'.repeat(64)]);
    setIterationCount(0);
    setIsTargetReached(false);
  }, [initialState]);

  // Handle auto iterations
  useEffect(() => {
    if (!isIterating || isTargetReached) return;
    
    const intervalId = setInterval(iterate, iterationInterval);
    
    return () => {
      clearInterval(intervalId);
    };
  }, [iterate, isIterating, isTargetReached, iterationInterval]);

  // Calculate improvement percentages for each metric
  const getImprovementPercentages = useCallback(() => {
    const improvements: Record<string, number> = {};
    
    Object.keys(initialState).forEach(key => {
      const initial = initialState[key];
      const current = currentState[key];
      const improvement = ((current - initial) / initial) * 100;
      improvements[key] = isFinite(improvement) ? improvement : 0;
    });
    
    return improvements;
  }, [initialState, currentState]);

  // Calculate overall improvement
  const getOverallImprovement = useCallback(() => {
    const initialSum = Object.values(initialState).reduce((sum, val) => sum + val, 0);
    const currentSum = Object.values(currentState).reduce((sum, val) => sum + val, 0);
    
    return ((currentSum - initialSum) / initialSum) * 100;
  }, [initialState, currentState]);

  return {
    currentState,
    hashChain,
    latestHash: hashChain[hashChain.length - 1],
    iterationCount,
    isIterating,
    isTargetReached,
    improvements: getImprovementPercentages(),
    overallImprovement: getOverallImprovement(),
    iterate,
    startIterating,
    stopIterating,
    reset
  };
}