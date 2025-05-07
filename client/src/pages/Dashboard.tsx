import React, { useState } from 'react';
import { useSovereigntyVerification } from '@/hooks/useSovereigntyVerification';
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardFooter, 
  CardHeader, 
  CardTitle 
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { 
  Shield, 
  Check, 
  AlertTriangle, 
  X, 
  RefreshCw,
  Award,
  FileText,
  Hash,
  Lock
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const Dashboard = () => {
  const {
    verificationVectors,
    challengeRecords,
    dashboardMetrics,
    sovereigntyBadges,
    isLoadingVectors,
    isLoadingChallenges,
    isLoadingMetrics,
    isLoadingSovereigntyBadges,
    verifyIntegrity,
    isVerifying,
    getCurrentVerificationStrength,
    getDocumentIntegrityStatus,
    isVerificationComplete,
  } = useSovereigntyVerification();

  const [activeVector, setActiveVector] = useState<number | null>(null);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'verified':
        return 'bg-green-500';
      case 'partial':
        return 'bg-yellow-500';
      case 'failed':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStrengthLevel = (strength: number) => {
    if (strength >= 90) return 'Quantum';
    if (strength >= 75) return 'Very High';
    if (strength >= 60) return 'High';
    if (strength >= 45) return 'Medium';
    if (strength >= 30) return 'Moderate';
    return 'Low';
  };

  const renderVerificationChart = () => {
    if (!verificationVectors || isLoadingVectors) {
      return <div className="h-[200px] flex items-center justify-center">Loading verification data...</div>;
    }

    const data = [
      { name: 'Verified', value: verificationVectors.filter((v: any) => v.strength === 'High' || v.strength === 'Very High').length },
      { name: 'Medium', value: verificationVectors.filter((v: any) => v.strength === 'Medium').length },
      { name: 'Low', value: verificationVectors.filter((v: any) => v.strength === 'Low').length }
    ];

    const COLORS = ['#10b981', '#f59e0b', '#71717a'];

    return (
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            fill="#8884d8"
            paddingAngle={5}
            dataKey="value"
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => [`${value} vectors`, 'Count']} />
        </PieChart>
      </ResponsiveContainer>
    );
  };

  const handleOneClickVerification = () => {
    verifyIntegrity();
  };

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">Personal Sovereignty Dashboard</h1>
          <p className="text-slate-500">Verify and protect your digital autonomy</p>
        </div>
        <Button 
          onClick={handleOneClickVerification} 
          disabled={isVerifying}
          size="lg"
          className="gap-2"
        >
          {isVerifying ? (
            <>
              <RefreshCw className="h-4 w-4 animate-spin" />
              Verifying...
            </>
          ) : (
            <>
              <Shield className="h-5 w-5" />
              One-Click Verification
            </>
          )}
        </Button>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Verification Strength</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {getStrengthLevel(getCurrentVerificationStrength())}
            </div>
            <Progress 
              value={getCurrentVerificationStrength()} 
              className="h-2 mt-2" 
            />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Document Integrity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${getStatusColor(getDocumentIntegrityStatus())}`}></div>
              <div className="text-2xl font-bold capitalize">
                {getDocumentIntegrityStatus()}
              </div>
            </div>
            <div className="text-xs text-slate-500 mt-2">
              {getDocumentIntegrityStatus() === 'verified' 
                ? 'All documents verified successfully' 
                : getDocumentIntegrityStatus() === 'partial' 
                  ? 'Some documents verified, others pending'
                  : 'Document verification needed'
              }
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Challenge Response</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {challengeRecords?.length || 0} Challenges
            </div>
            <div className="text-xs text-slate-500 mt-2">
              {challengeRecords?.filter((c: any) => c.isResolved).length || 0} resolved, strengthening verification
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Verification Vectors */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Verification Vectors</CardTitle>
            <CardDescription>Multiple independent verification mechanisms</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoadingVectors ? (
              <div className="h-[200px] flex items-center justify-center">
                <RefreshCw className="h-5 w-5 animate-spin mr-2" />
                Loading verification vectors...
              </div>
            ) : (
              <div className="space-y-4">
                {verificationVectors?.map((vector: any) => (
                  <div 
                    key={vector.id} 
                    className={`border rounded-lg p-4 cursor-pointer transition-all ${
                      activeVector === vector.id ? 'border-primary' : 'border-border'
                    }`}
                    onClick={() => setActiveVector(activeVector === vector.id ? null : vector.id)}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="font-semibold">{vector.name}</div>
                        <div className="text-xs text-slate-500">{vector.type}</div>
                      </div>
                      <Badge variant={
                        vector.strength === 'Very High' ? 'default' : 
                        vector.strength === 'High' ? 'secondary' : 
                        vector.strength === 'Medium' ? 'outline' : 
                        'destructive'
                      }>
                        {vector.strength}
                      </Badge>
                    </div>
                    
                    {activeVector === vector.id && (
                      <div className="mt-2 text-sm text-slate-600">
                        {vector.description}
                        {vector.filePath && (
                          <div className="mt-1 text-xs flex items-center">
                            <FileText className="h-3 w-3 mr-1" />
                            {vector.filePath}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Verification Distribution</CardTitle>
            <CardDescription>Strength across vectors</CardDescription>
          </CardHeader>
          <CardContent>
            {renderVerificationChart()}
          </CardContent>
        </Card>
      </div>

      {/* Challenge Records & Badges */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Challenge Records</CardTitle>
            <CardDescription>
              Challenges strengthen verification through the Sovereignty Reinforcement Paradox
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoadingChallenges ? (
              <div className="h-[200px] flex items-center justify-center">
                <RefreshCw className="h-5 w-5 animate-spin mr-2" />
                Loading challenge records...
              </div>
            ) : challengeRecords?.length === 0 ? (
              <div className="h-[200px] flex flex-col items-center justify-center text-slate-500">
                <AlertTriangle className="h-10 w-10 mb-2" />
                <p>No challenges recorded yet</p>
              </div>
            ) : (
              <div className="space-y-4">
                {challengeRecords?.map((challenge: any) => (
                  <div key={challenge.id} className="border rounded-lg p-4">
                    <div className="flex justify-between">
                      <div className="font-semibold">{challenge.patternType}</div>
                      <Badge variant={challenge.isResolved ? 'default' : 'outline'}>
                        {challenge.isResolved ? 'Resolved' : 'Open'}
                      </Badge>
                    </div>
                    <p className="text-sm mt-1">{challenge.description}</p>
                    <div className="mt-2 flex items-center text-xs text-slate-500">
                      <div className="mr-4">
                        Before: {challenge.verificationStrengthBeforeChallenge}
                      </div>
                      <div className="flex items-center">
                        After: {challenge.verificationStrengthAfterChallenge}
                        <span className="ml-1 text-green-500">
                          (+{parseFloat(challenge.verificationStrengthAfterChallenge) - 
                             parseFloat(challenge.verificationStrengthBeforeChallenge)})
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Sovereignty Badges</CardTitle>
            <CardDescription>Recognition of verified sovereignty</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoadingSovereigntyBadges ? (
              <div className="h-[200px] flex items-center justify-center">
                <RefreshCw className="h-5 w-5 animate-spin mr-2" />
                Loading badges...
              </div>
            ) : sovereigntyBadges?.length === 0 ? (
              <div className="h-[200px] flex flex-col items-center justify-center text-slate-500">
                <Award className="h-10 w-10 mb-2" />
                <p>Complete verification to earn badges</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4">
                {sovereigntyBadges?.map((badge: any) => (
                  <div key={badge.id} className="border rounded-lg p-3 flex flex-col items-center">
                    <div className="w-12 h-12 flex items-center justify-center bg-slate-100 rounded-full mb-2">
                      <Award className="h-6 w-6 text-primary" />
                    </div>
                    <div className="text-center">
                      <div className="font-semibold text-sm">{badge.badgeName}</div>
                      <div className="text-xs text-slate-500">{new Date(badge.issuedAt).toLocaleDateString()}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;