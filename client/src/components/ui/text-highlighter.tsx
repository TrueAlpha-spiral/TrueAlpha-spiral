import React from 'react';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';

export interface TextHighlight {
  startIndex: number;
  endIndex: number;
  type: 'factual' | 'speculative' | 'fabricated';
  confidenceScore: number;
  message: string;
  patternName?: string;
}

export interface TextHighlighterProps {
  text: string;
  highlights: TextHighlight[];
  className?: string;
}

/**
 * TextHighlighter component that displays text with color-coded highlights
 * based on factuality assessment.
 */
export function TextHighlighter({ text, highlights, className }: TextHighlighterProps) {
  // Sort highlights by start index to process them in order
  const sortedHighlights = [...highlights].sort((a, b) => a.startIndex - b.startIndex);
  
  // Build segments that will contain either highlighted or regular text
  const segments: React.ReactNode[] = [];
  let lastIndex = 0;
  
  sortedHighlights.forEach((highlight, index) => {
    // Add any text before this highlight as a regular segment
    if (highlight.startIndex > lastIndex) {
      segments.push(
        <span key={`regular-${index}`} className="text-foreground">
          {text.substring(lastIndex, highlight.startIndex)}
        </span>
      );
    }
    
    // Add the highlighted segment
    const highlightedText = text.substring(highlight.startIndex, highlight.endIndex);
    
    // Skip if the text is empty (shouldn't happen with proper highlights)
    if (highlightedText.trim() === '') {
      lastIndex = highlight.endIndex;
      return;
    }
    
    const scoreText = `${Math.round(highlight.confidenceScore * 100)}%`;
    
    // Determine highlight color based on type
    let highlightClass = '';
    switch (highlight.type) {
      case 'factual':
        highlightClass = 'bg-green-100 dark:bg-green-900/30 text-green-900 dark:text-green-300';
        break;
      case 'speculative':
        highlightClass = 'bg-amber-100 dark:bg-amber-900/30 text-amber-900 dark:text-amber-300';
        break;
      case 'fabricated':
        highlightClass = 'bg-red-100 dark:bg-red-900/30 text-red-900 dark:text-red-300';
        break;
    }
    
    segments.push(
      <Tooltip key={`highlight-${index}`}>
        <TooltipTrigger asChild>
          <span className={cn("px-0.5 rounded cursor-help", highlightClass)}>
            {highlightedText}
          </span>
        </TooltipTrigger>
        <TooltipContent className="max-w-sm">
          <div className="space-y-1">
            <div className="font-medium">
              {highlight.type === 'factual' ? 'Factual Content' : 
               highlight.type === 'speculative' ? 'Speculative Content' : 
               'Potentially Fabricated'}
              {highlight.patternName && ` (${highlight.patternName})`}
            </div>
            <div className="text-sm text-muted-foreground">{highlight.message}</div>
            <div className="text-xs font-mono pt-1">
              Confidence: {scoreText}
            </div>
          </div>
        </TooltipContent>
      </Tooltip>
    );
    
    lastIndex = highlight.endIndex;
  });
  
  // Add any remaining text after the last highlight
  if (lastIndex < text.length) {
    segments.push(
      <span key="final-regular" className="text-foreground">
        {text.substring(lastIndex)}
      </span>
    );
  }
  
  return (
    <div className={cn("text-highlighter whitespace-pre-wrap", className)}>
      {segments}
    </div>
  );
}

export default TextHighlighter;