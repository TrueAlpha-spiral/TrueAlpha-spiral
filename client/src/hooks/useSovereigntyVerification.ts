import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiRequest } from '@/lib/queryClient';

export function useSovereigntyVerification() {
  const queryClient = useQueryClient();

  const { data: verificationVectors, isLoading: isLoadingVectors } = useQuery({
    queryKey: ['/api/verification-vectors'],
  });

  const { data: challengeRecords, isLoading: isLoadingChallenges } = useQuery({
    queryKey: ['/api/challenge-records'],
  });

  const { data: dashboardMetrics, isLoading: isLoadingMetrics } = useQuery({
    queryKey: ['/api/dashboard-metrics'],
  });

  const { data: sovereigntyBadges, isLoading: isLoadingSovereigntyBadges } = useQuery({
    queryKey: ['/api/sovereignty-badges'],
  });

  // One-click verification mutation
  const { mutate: verifyIntegrity, isPending: isVerifying } = useMutation({
    mutationFn: async () => {
      const response = await apiRequest('GET', '/api/verify-integrity');
      return response.json();
    },
    onSuccess: () => {
      // Invalidate relevant queries to refresh data
      queryClient.invalidateQueries({ queryKey: ['/api/dashboard-metrics'] });
    },
  });

  // Create challenge record mutation
  const { mutate: createChallengeRecord, isPending: isCreatingChallenge } = useMutation({
    mutationFn: async (challenge: any) => {
      const response = await apiRequest('POST', '/api/challenge-records', challenge);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/challenge-records'] });
    },
  });

  // Update challenge record mutation
  const { mutate: updateChallengeRecord, isPending: isUpdatingChallenge } = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: any }) => {
      const response = await apiRequest('PATCH', `/api/challenge-records/${id}`, data);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/challenge-records'] });
    },
  });

  // Calculate verification strength mutation
  const { mutate: calculateVerificationStrength, isPending: isCalculating } = useMutation({
    mutationFn: async ({ baseStrength, challenges }: { baseStrength: number; challenges: any[] }) => {
      const response = await apiRequest('POST', '/api/calculate-verification-strength', {
        baseStrength,
        challenges,
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/dashboard-metrics'] });
    },
  });

  // Get current verification strength from metrics
  const getCurrentVerificationStrength = () => {
    if (!dashboardMetrics) return 0;
    
    const strengthMetric = dashboardMetrics.find(
      (metric: any) => metric.metricName === 'verificationStrength'
    );
    
    return strengthMetric ? parseFloat(strengthMetric.metricValue) : 0;
  };

  // Get document integrity status from metrics
  const getDocumentIntegrityStatus = () => {
    if (!dashboardMetrics) return 'unknown';
    
    const statusMetric = dashboardMetrics.find(
      (metric: any) => metric.metricName === 'documentIntegrityStatus'
    );
    
    return statusMetric ? statusMetric.metricValue : 'unknown';
  };

  // Check if verification is complete (all documents verified)
  const isVerificationComplete = () => {
    return getDocumentIntegrityStatus() === 'verified';
  };

  return {
    // Data
    verificationVectors,
    challengeRecords,
    dashboardMetrics,
    sovereigntyBadges,
    
    // Loading states
    isLoadingVectors,
    isLoadingChallenges,
    isLoadingMetrics,
    isLoadingSovereigntyBadges,
    
    // Mutation functions
    verifyIntegrity,
    createChallengeRecord,
    updateChallengeRecord,
    calculateVerificationStrength,
    
    // Mutation loading states
    isVerifying,
    isCreatingChallenge,
    isUpdatingChallenge,
    isCalculating,
    
    // Helper functions
    getCurrentVerificationStrength,
    getDocumentIntegrityStatus,
    isVerificationComplete,
  };
}