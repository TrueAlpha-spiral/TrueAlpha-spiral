import React from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { apiRequest } from '@/lib/queryClient';
import { Loader2 } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import TextHighlighter from '@/components/ui/text-highlighter';
import { Progress } from '@/components/ui/progress';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { VerificationResult } from '@shared/schema';

// Verification form schema
const verificationFormSchema = z.object({
  content: z.string().min(10, 'Text must be at least 10 characters long').max(10000, 'Text cannot exceed 10,000 characters'),
});

type VerificationFormValues = z.infer<typeof verificationFormSchema>;

export interface VerificationFormProps {
  className?: string;
}

/**
 * VerificationForm component that allows users to submit text for verification.
 */
export function VerificationForm({ className }: VerificationFormProps) {
  const [verificationResult, setVerificationResult] = React.useState<VerificationResult | null>(null);

  // Define form
  const form = useForm<VerificationFormValues>({
    resolver: zodResolver(verificationFormSchema),
    defaultValues: {
      content: '',
    },
  });

  // Define verification mutation
  const verifyMutation = useMutation({
    mutationFn: async (values: VerificationFormValues) => {
      const response = await apiRequest('POST', '/api/verify', values);
      return await response.json() as VerificationResult;
    },
    onSuccess: (data) => {
      setVerificationResult(data);
    },
  });

  // Handle form submission
  const onSubmit = (values: VerificationFormValues) => {
    verifyMutation.mutate(values);
  };

  // Get score text and color
  const getScoreInfo = (score: number) => {
    if (score >= 0.8) {
      return {
        text: 'High Factuality',
        description: 'The content appears to be highly factual with minimal speculative or fabricated elements.',
        color: 'bg-green-500',
      };
    } else if (score >= 0.6) {
      return {
        text: 'Moderate Factuality',
        description: 'The content contains a mix of factual information and speculative elements.',
        color: 'bg-amber-500',
      };
    } else {
      return {
        text: 'Low Factuality',
        description: 'The content contains significant potentially fabricated or highly speculative elements.',
        color: 'bg-red-500',
      };
    }
  };

  return (
    <div className={className}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="content"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Content to Verify</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Enter text to verify for factuality..."
                    className="min-h-[200px] resize-y"
                    {...field}
                  />
                </FormControl>
                <FormDescription>
                  Enter text you want to verify for factuality. The TrueAlphaSpiral system will analyze
                  the content for potential fabrications or speculative elements.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button
            type="submit"
            disabled={verifyMutation.isPending}
            className="w-full sm:w-auto"
          >
            {verifyMutation.isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Verifying...
              </>
            ) : (
              'Verify Content'
            )}
          </Button>
        </form>
      </Form>

      {verificationResult && (
        <div className="mt-8 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Verification Results</CardTitle>
              <CardDescription>
                Analysis completed in {(verificationResult.processingTimeMs / 1000).toFixed(2)} seconds
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Score section */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-sm">Truth Score</h3>
                  <span className="text-sm font-medium">
                    {Math.round(verificationResult.truthScore * 100)}%
                  </span>
                </div>
                <Progress value={verificationResult.truthScore * 100} className={getScoreInfo(verificationResult.truthScore).color} />
                <p className="text-sm text-muted-foreground">
                  {getScoreInfo(verificationResult.truthScore).description}
                </p>
              </div>

              {/* Summary section */}
              <div className="space-y-2">
                <h3 className="font-semibold text-sm">Summary</h3>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div className="bg-green-100 dark:bg-green-900/30 rounded-md p-2">
                    <div className="font-semibold">{verificationResult.summary.factualCount}</div>
                    <div className="text-xs">Factual</div>
                  </div>
                  <div className="bg-amber-100 dark:bg-amber-900/30 rounded-md p-2">
                    <div className="font-semibold">{verificationResult.summary.speculativeCount}</div>
                    <div className="text-xs">Speculative</div>
                  </div>
                  <div className="bg-red-100 dark:bg-red-900/30 rounded-md p-2">
                    <div className="font-semibold">{verificationResult.summary.fabricatedCount}</div>
                    <div className="text-xs">Fabricated</div>
                  </div>
                </div>
              </div>

              {/* Highlighted text */}
              <div className="space-y-2">
                <h3 className="font-semibold text-sm">Analyzed Content</h3>
                <div className="border rounded-md p-4 bg-card">
                  <TextHighlighter 
                    text={verificationResult.originalText} 
                    highlights={verificationResult.highlights} 
                  />
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between text-xs text-muted-foreground">
              <div>
                <span className="font-mono">ID: {verificationResult.id}</span>
              </div>
              <div>
                Powered by TrueAlphaSpiral verification engine
              </div>
            </CardFooter>
          </Card>
        </div>
      )}
    </div>
  );
}

export default VerificationForm;