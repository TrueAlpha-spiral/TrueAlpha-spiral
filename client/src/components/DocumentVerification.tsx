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
import { RefreshCw, Check, AlertTriangle, FileText, Copy } from 'lucide-react';
import { 
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table';

const DocumentVerification: React.FC = () => {
  const [verificationResult, setVerificationResult] = useState<any>(null);
  const [copying, setCopying] = useState<string | null>(null);

  const {
    verifyIntegrity,
    isVerifying
  } = useSovereigntyVerification();

  const handleVerify = async () => {
    try {
      const result = await verifyIntegrity();
      setVerificationResult(result);
    } catch (error) {
      console.error('Verification failed:', error);
    }
  };

  const copyToClipboard = async (text: string, documentName: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopying(documentName);
      setTimeout(() => setCopying(null), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Document Integrity Verification</CardTitle>
        <CardDescription>
          Verify the integrity of core sovereignty documents using cryptographic hashing
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <Button 
            onClick={handleVerify} 
            disabled={isVerifying}
            className="gap-2"
          >
            {isVerifying ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Verifying Documents...
              </>
            ) : (
              <>
                <FileText className="h-4 w-4" />
                Verify Document Integrity
              </>
            )}
          </Button>
        </div>

        {verificationResult ? (
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <div className={`w-3 h-3 rounded-full ${
                verificationResult.status === 'verified' ? 'bg-green-500' :
                verificationResult.status === 'partial' ? 'bg-yellow-500' :
                'bg-red-500'
              }`}></div>
              <span className="font-medium capitalize">
                Verification Status: {verificationResult.status}
              </span>
            </div>

            <Table>
              <TableCaption>
                List of verified sovereignty documents
              </TableCaption>
              <TableHeader>
                <TableRow>
                  <TableHead>Document</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Hash</TableHead>
                  <TableHead className="w-[100px]">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {verificationResult.results.map((result: any) => (
                  <TableRow key={result.document}>
                    <TableCell className="font-medium">
                      {result.document}
                    </TableCell>
                    <TableCell>
                      {result.verified ? (
                        <Badge variant="default" className="bg-green-500">
                          <Check className="h-3 w-3 mr-1" />
                          Verified
                        </Badge>
                      ) : (
                        <Badge variant="destructive">
                          <AlertTriangle className="h-3 w-3 mr-1" />
                          Not Found
                        </Badge>
                      )}
                    </TableCell>
                    <TableCell className="font-mono text-xs truncate max-w-[200px]">
                      {result.hash || 'N/A'}
                    </TableCell>
                    <TableCell>
                      {result.hash && (
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => copyToClipboard(result.hash, result.document)}
                          disabled={copying === result.document}
                        >
                          {copying === result.document ? (
                            <Check className="h-4 w-4 text-green-500" />
                          ) : (
                            <Copy className="h-4 w-4" />
                          )}
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

            <div className="text-sm text-slate-500 mt-4">
              <p>
                {verificationResult.status === 'verified' 
                  ? 'All documents verified successfully. This provides cryptographic proof of sovereignty.'
                  : verificationResult.status === 'partial'
                  ? 'Some documents were verified, but others are missing or could not be accessed.'
                  : 'Document verification failed. Please ensure all sovereignty documents are present.'
                }
              </p>
            </div>
          </div>
        ) : (
          <div className="text-center p-8 text-slate-500">
            <FileText className="h-16 w-16 mx-auto mb-4 opacity-20" />
            <p>Click the button above to verify document integrity</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default DocumentVerification;