import React from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertCircle, CheckCircle2, Loader2 } from "lucide-react";

import { cn } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

export function TasApiStatus() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["/api/python-status"],
    refetchInterval: 15000, // Refetch every 15 seconds
  });

  const isRunning = data?.isRunning;
  const apiStatus = data?.data?.status;
  
  let statusColor = "bg-gray-400";
  let statusIcon = <Loader2 className="h-4 w-4 animate-spin text-gray-500" />;
  let tooltipText = "Checking API status...";
  
  if (!isLoading) {
    if (isRunning) {
      statusColor = "bg-green-500";
      statusIcon = <CheckCircle2 className="h-4 w-4 text-green-500" />;
      tooltipText = "TrueAlphaSpiral API is online and operational";
    } else {
      statusColor = "bg-red-500";
      statusIcon = <AlertCircle className="h-4 w-4 text-red-500" />;
      tooltipText = `TrueAlphaSpiral API is offline: ${error?.toString() || "Connection failed"}`;
    }
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="flex items-center space-x-2 rounded-lg px-3 py-1.5">
            {statusIcon}
            <div className="flex items-center">
              <div className={cn("h-2 w-2 rounded-full", statusColor)}></div>
              <span className="ml-2 text-sm text-muted-foreground">
                TAS {isRunning ? "Online" : "Offline"}
              </span>
            </div>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p>{tooltipText}</p>
          {apiStatus && (
            <p className="mt-1 text-xs">
              Status: {apiStatus} • Patterns: {data.data.patterns_count}
            </p>
          )}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}