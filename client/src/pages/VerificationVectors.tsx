import React, { useState } from 'react';
import { useSovereigntyVerification } from '@/hooks/useSovereigntyVerification';
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { RefreshCw, FileText, Layers, Shield, Fingerprint, Calendar, Sigma, Lock } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import DocumentVerification from '@/components/DocumentVerification';
import VerificationEquation from '@/components/VerificationEquation';

const VerificationVectors: React.FC = () => {
  const {
    verificationVectors,
    isLoadingVectors,
  } = useSovereigntyVerification();

  // Group vectors by type
  const groupedVectors: Record<string, any[]> = {};
  
  if (verificationVectors) {
    verificationVectors.forEach((vector: any) => {
      if (!groupedVectors[vector.type]) {
        groupedVectors[vector.type] = [];
      }
      groupedVectors[vector.type].push(vector);
    });
  }

  // Icons mapping for vector types
  const getTypeIcon = (type: string) => {
    switch(type.toLowerCase()) {
      case 'conceptual':
        return <Layers className="h-5 w-5" />;
      case 'temporal':
        return <Calendar className="h-5 w-5" />;
      case 'axiom':
        return <Sigma className="h-5 w-5" />;
      case 'identity':
        return <Fingerprint className="h-5 w-5" />;
      default:
        return <Shield className="h-5 w-5" />;
    }
  };

  // Color mapping for strength
  const getStrengthColor = (strength: string) => {
    switch(strength) {
      case 'Very High':
        return 'bg-blue-500';
      case 'High':
        return 'bg-green-500';
      case 'Medium':
        return 'bg-yellow-500';
      case 'Low':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="container mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Verification Vectors</h1>
        <p className="text-slate-500">
          Multiple independent verification mechanisms proving sole creatorship
        </p>
      </div>

      <Tabs defaultValue="vectors" className="mb-8">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="vectors">Verification Vectors</TabsTrigger>
          <TabsTrigger value="documents">Document Verification</TabsTrigger>
          <TabsTrigger value="equation">Verification Equation</TabsTrigger>
        </TabsList>
        
        <TabsContent value="vectors" className="mt-6">
          {isLoadingVectors ? (
            <div className="h-[300px] flex items-center justify-center">
              <RefreshCw className="h-6 w-6 animate-spin mr-3" />
              <span>Loading verification vectors...</span>
            </div>
          ) : (
            <div className="space-y-8">
              {Object.entries(groupedVectors).map(([type, vectors]) => (
                <Card key={type} className="overflow-hidden">
                  <CardHeader className="flex flex-row items-center gap-4 pb-2">
                    <div className="bg-primary/10 p-3 rounded-full">
                      {getTypeIcon(type)}
                    </div>
                    <div>
                      <CardTitle className="capitalize">{type} Verification Vectors</CardTitle>
                      <CardDescription>
                        {type === 'conceptual' && 'Complex conceptual patterns that cannot be replicated'}
                        {type === 'temporal' && 'Chronological evidence establishing creator timeline'}
                        {type === 'axiom' && 'Fundamental principles that define the system'}
                        {type === 'identity' && 'Personal identity markers tied to creator'}
                        {!['conceptual', 'temporal', 'axiom', 'identity'].includes(type) && 
                          'Independent verification mechanisms'}
                      </CardDescription>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
                      {vectors.map((vector: any) => (
                        <div key={vector.id} className="border rounded-lg p-4">
                          <div className="flex justify-between items-start">
                            <div className="font-semibold">{vector.name}</div>
                            <Badge variant={
                              vector.strength === 'Very High' ? 'default' : 
                              vector.strength === 'High' ? 'secondary' : 
                              vector.strength === 'Medium' ? 'outline' : 
                              'destructive'
                            }>
                              {vector.strength}
                            </Badge>
                          </div>
                          
                          <div className="mt-2 text-sm text-slate-600">
                            {vector.description}
                          </div>
                          
                          {vector.filePath && (
                            <div className="mt-3 text-xs flex items-center text-slate-500">
                              <FileText className="h-3 w-3 mr-1" />
                              {vector.filePath}
                            </div>
                          )}
                          
                          <div className="mt-3 flex items-center">
                            <div className={`h-2 flex-1 rounded-full ${getStrengthColor(vector.strength)} opacity-70`} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
              
              <div className="text-center p-6 bg-slate-50 rounded-lg mt-8">
                <Lock className="h-8 w-8 mx-auto mb-3 text-slate-400" />
                <h3 className="text-lg font-semibold mb-2">The Sovereignty Reinforcement Paradox</h3>
                <p className="text-slate-600 max-w-2xl mx-auto">
                  The more a sovereignty claim is challenged, the stronger it becomes.
                  Each challenge creates a new verification vector that strengthens the overall system,
                  as referenced in the Quantum Metaphysical Equation.
                </p>
              </div>
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="documents" className="mt-6">
          <DocumentVerification />
        </TabsContent>
        
        <TabsContent value="equation" className="mt-6">
          <VerificationEquation />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default VerificationVectors;