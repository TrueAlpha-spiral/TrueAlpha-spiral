import React, { useEffect, useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiRequest, queryClient } from '@/lib/queryClient';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/hooks/use-auth';
import { Loader2, ShieldAlert, Shield, Zap, Fingerprint, Calculator, RefreshCw, Power, PowerOff, HeartPulse } from 'lucide-react';

interface SystemStatus {
  initialized: boolean;
  running: boolean;
  start_time: string | null;
  recursive_cycle: number;
  last_update: string;
  sovereignty?: number;
  components: {
    [key: string]: {
      status: string;
      initialized: boolean;
      last_scan?: string;
      last_protection?: string;
    };
  };
}

export default function PythonSystemControl() {
  const { toast } = useToast();
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('status');

  // Fetch system status directly from Python API
  const { 
    data: systemStatus, 
    isLoading: isLoadingStatus,
    error: statusError,
    refetch: refetchStatus
  } = useQuery<SystemStatus>({
    queryKey: ['/api/python-system/status'],
    queryFn: async () => {
      try {
        // Get the current hostname and protocol - will work both locally and on Replit
        const protocol = window.location.protocol;
        const hostname = window.location.hostname;
        
        // Direct fetch to Python API server on the same hostname
        // Using relative URL to avoid CORS issues in production
        const response = await fetch(`/api/python/status`, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch system status');
        }
        return await response.json();
      } catch (error) {
        console.error('Error fetching system status:', error);
        throw error;
      }
    },
    refetchInterval: 5000, // Auto-refresh every 5 seconds
  });

  // Start system mutation
  const startMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/python/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!res.ok) {
        throw new Error('Failed to start system');
      }
      return await res.json();
    },
    onSuccess: () => {
      toast({
        title: 'System Started',
        description: 'TrueAlphaSpiral system has been started successfully',
      });
      queryClient.invalidateQueries({ queryKey: ['/api/python-system/status'] });
    },
    onError: (error) => {
      toast({
        title: 'Failed to Start System',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  // Stop system mutation
  const stopMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/python/stop`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!res.ok) {
        throw new Error('Failed to stop system');
      }
      return await res.json();
    },
    onSuccess: () => {
      toast({
        title: 'System Stopped',
        description: 'TrueAlphaSpiral system has been stopped successfully',
      });
      queryClient.invalidateQueries({ queryKey: ['/api/python-system/status'] });
    },
    onError: (error) => {
      toast({
        title: 'Failed to Stop System',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  // Verify integrity mutation
  const verifyIntegrityMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/python/verify-integrity`, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!res.ok) {
        throw new Error('Failed to verify integrity');
      }
      return await res.json();
    },
    onSuccess: (data) => {
      toast({
        title: 'System Integrity Verification',
        description: data.integrity_verified 
          ? 'System integrity verified successfully' 
          : 'System integrity verification failed',
        variant: data.integrity_verified ? 'default' : 'destructive',
      });
    },
    onError: (error) => {
      toast({
        title: 'Failed to Verify System Integrity',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  // Enforce binary quantum law mutation
  const enforceBinaryLawMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/python/enforce-binary-law`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!res.ok) {
        throw new Error('Failed to enforce binary law');
      }
      return await res.json();
    },
    onSuccess: () => {
      toast({
        title: 'Binary Quantum Law Enforced',
        description: 'No free will, only cosmic order',
      });
    },
    onError: (error) => {
      toast({
        title: 'Failed to Enforce Binary Quantum Law',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  // Verify architect mutation
  const verifyArchitectMutation = useMutation({
    mutationFn: async (architect_id: string) => {
      const res = await fetch(`/api/python/verify-architect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ architect_id })
      });
      if (!res.ok) {
        throw new Error('Failed to verify architect');
      }
      return await res.json();
    },
    onSuccess: (data) => {
      toast({
        title: 'Architect Verification',
        description: data.architect_verified 
          ? 'Architect identity verified successfully' 
          : 'Architect identity verification failed',
        variant: data.architect_verified ? 'default' : 'destructive',
      });
    },
    onError: (error) => {
      toast({
        title: 'Failed to Verify Architect',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  // Calculate sovereignty mutation
  const calculateSovereigntyMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/python/calculate-sovereignty`, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!res.ok) {
        throw new Error('Failed to calculate sovereignty');
      }
      return await res.json();
    },
    onSuccess: (data) => {
      toast({
        title: 'Sovereignty Calculation',
        description: `Sovereignty value: ${data.sovereignty.toFixed(4)}`,
      });
      queryClient.invalidateQueries({ queryKey: ['/api/python-system/status'] });
    },
    onError: (error) => {
      toast({
        title: 'Failed to Calculate Sovereignty',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  // Restart system mutation
  const restartMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/python/restart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!res.ok) {
        throw new Error('Failed to restart system');
      }
      return await res.json();
    },
    onSuccess: () => {
      toast({
        title: 'System Restarted',
        description: 'TrueAlphaSpiral system has been restarted successfully',
      });
      queryClient.invalidateQueries({ queryKey: ['/api/python-system/status'] });
    },
    onError: (error) => {
      toast({
        title: 'Failed to Restart System',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  // Verify architect when logged in
  useEffect(() => {
    if (user && user.username) {
      verifyArchitectMutation.mutate(user.username);
    }
  }, [user]);

  // Format date string
  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleString();
  };

  // Get component status badge
  const getStatusBadge = (status: string) => {
    switch(status) {
      case 'active':
        return <Badge className="bg-green-500">Active</Badge>;
      case 'ready':
        return <Badge className="bg-blue-500">Ready</Badge>;
      case 'inactive':
        return <Badge className="bg-gray-500">Inactive</Badge>;
      default:
        return <Badge className="bg-yellow-500">{status}</Badge>;
    }
  };

  if (isLoadingStatus) {
    return (
      <div className="flex items-center justify-center p-6">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2">Loading TrueAlphaSpiral system status...</span>
      </div>
    );
  }

  if (statusError) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-red-500">System Error</CardTitle>
          <CardDescription>
            Failed to connect to the TrueAlphaSpiral Python system
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p>The Python API server may not be running. Please check the console logs for more information.</p>
        </CardContent>
        <CardFooter>
          <Button variant="outline" onClick={() => refetchStatus()}>
            <RefreshCw className="mr-2 h-4 w-4" /> Retry Connection
          </Button>
        </CardFooter>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle className="text-gradient bg-gradient-to-r from-blue-600 to-purple-600">
              TrueAlphaSpiral System Control
            </CardTitle>
            <CardDescription>
              Sovereign concept protection system control panel
            </CardDescription>
          </div>
          {systemStatus?.running ? (
            <Badge className="bg-green-500">RUNNING</Badge>
          ) : (
            <Badge className="bg-red-500">STOPPED</Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="w-full">
            <TabsTrigger value="status">System Status</TabsTrigger>
            <TabsTrigger value="components">Components</TabsTrigger>
            <TabsTrigger value="operations">Operations</TabsTrigger>
          </TabsList>
          
          <TabsContent value="status" className="py-4">
            <div className="grid gap-4">
              <div className="space-y-2">
                <h3 className="text-lg font-medium">System Overview</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Initialized</p>
                    <p>{systemStatus?.initialized ? '✓ Yes' : '✗ No'}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Status</p>
                    <p>{systemStatus?.running ? '✓ Running' : '✗ Stopped'}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Start Time</p>
                    <p>{systemStatus ? formatDate(systemStatus.start_time) : 'Never'}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Last Update</p>
                    <p>{systemStatus ? formatDate(systemStatus.last_update) : 'Never'}</p>
                  </div>
                </div>
              </div>
              
              <Separator />
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium">Recursive Cycle</h3>
                  <span className="text-xl font-bold">{systemStatus?.recursive_cycle || 0}</span>
                </div>
                <Progress value={((systemStatus?.recursive_cycle || 0) % 100) / 100 * 100} className="h-2" />
              </div>
              
              <Separator />
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium">Sovereignty</h3>
                  <span className="text-xl font-bold">{systemStatus?.sovereignty?.toFixed(4) || 'N/A'}</span>
                </div>
                <div className="text-sm text-muted-foreground">
                  sovereignty = truth/distance &gt;&lt; size
                </div>
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="components" className="py-4">
            <div className="space-y-4">
              {systemStatus && Object.entries(systemStatus.components).map(([key, component]) => (
                <div key={key} className="rounded-lg border p-3">
                  <div className="flex justify-between items-center">
                    <h3 className="text-base font-medium capitalize">{key.replace('_', ' ')}</h3>
                    {getStatusBadge(component.status)}
                  </div>
                  <div className="mt-2 text-sm text-muted-foreground">
                    {component.last_scan && (
                      <div>Last Scan: {formatDate(component.last_scan)}</div>
                    )}
                    {component.last_protection && (
                      <div>Last Protection: {formatDate(component.last_protection)}</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>
          
          <TabsContent value="operations" className="py-4">
            <div className="grid grid-cols-2 gap-4">
              <Button 
                onClick={() => startMutation.mutate()} 
                disabled={systemStatus?.running || startMutation.isPending}
                className="flex items-center"
              >
                {startMutation.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Power className="mr-2 h-4 w-4" />
                )}
                Start System
              </Button>
              
              <Button 
                onClick={() => stopMutation.mutate()} 
                disabled={!systemStatus?.running || stopMutation.isPending}
                variant="destructive"
                className="flex items-center"
              >
                {stopMutation.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <PowerOff className="mr-2 h-4 w-4" />
                )}
                Stop System
              </Button>
              
              <Button 
                onClick={() => verifyIntegrityMutation.mutate()} 
                disabled={verifyIntegrityMutation.isPending}
                variant="outline"
                className="flex items-center"
              >
                {verifyIntegrityMutation.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Shield className="mr-2 h-4 w-4" />
                )}
                Verify Integrity
              </Button>
              
              <Button 
                onClick={() => enforceBinaryLawMutation.mutate()} 
                disabled={enforceBinaryLawMutation.isPending}
                variant="outline"
                className="flex items-center"
              >
                {enforceBinaryLawMutation.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <ShieldAlert className="mr-2 h-4 w-4" />
                )}
                Enforce Binary Law
              </Button>
              
              <Button 
                onClick={() => calculateSovereigntyMutation.mutate()} 
                disabled={calculateSovereigntyMutation.isPending}
                variant="outline"
                className="flex items-center"
              >
                {calculateSovereigntyMutation.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Calculator className="mr-2 h-4 w-4" />
                )}
                Calculate Sovereignty
              </Button>
              
              <Button 
                onClick={() => restartMutation.mutate()} 
                disabled={restartMutation.isPending}
                variant="outline"
                className="flex items-center"
              >
                {restartMutation.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <RefreshCw className="mr-2 h-4 w-4" />
                )}
                Restart System
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
      <CardFooter className="flex justify-between">
        <div className="text-sm text-muted-foreground">
          Architect: Russell Nordland
        </div>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={() => refetchStatus()} 
          className="flex items-center"
        >
          <RefreshCw className="mr-2 h-4 w-4" /> Refresh
        </Button>
      </CardFooter>
    </Card>
  );
}