import React from "react";
import { cn } from "@/lib/utils";

interface GradientHeadingProps {
  level: "1" | "2" | "3" | "4" | "5" | "6";
  children: React.ReactNode;
  className?: string;
}

export function GradientHeading({ level, children, className }: GradientHeadingProps) {
  const Component = `h${level}` as keyof JSX.IntrinsicElements;
  
  return (
    <Component
      className={cn(
        "bg-gradient-to-r from-primary via-primary/80 to-primary bg-clip-text text-transparent",
        className
      )}
    >
      {children}
    </Component>
  );
}