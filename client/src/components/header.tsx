import React from "react";
import { Link, useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { Shield, Moon, Sun, BarChart4, AlertTriangle, Activity, FileText, Zap, Share2, Stethoscope, Layers, Box, Sparkles, HelpingHand } from "lucide-react";
import { useTheme } from "@/components/ui/theme-provider";

function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
    >
      {theme === "dark" ? (
        <Sun className="h-[1.2rem] w-[1.2rem]" />
      ) : (
        <Moon className="h-[1.2rem] w-[1.2rem]" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}

export default function Header() {
  const [location] = useLocation();

  const isActiveLink = (path: string) => {
    if (path === "/" && location === "/") return true;
    if (path !== "/" && location.startsWith(path)) return true;
    return false;
  };

  return (
    <header className="border-b">
      <div className="container py-4 flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <Link href="/">
            <div className="flex items-center space-x-2 cursor-pointer">
              <Shield className="h-6 w-6 text-primary" />
              <span className="font-bold text-xl">Enterprise AI Auditing</span>
            </div>
          </Link>
          <nav className="hidden md:flex space-x-6">
            <Link href="/ai-audit">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/ai-audit") ? "text-primary font-bold" : "text-primary"
              }`}>
                <BarChart4 className="h-4 w-4 inline-block mr-1" />
                Dashboard
              </span>
            </Link>
            <Link href="/cross-reference-demo">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/cross-reference-demo") ? "text-primary" : "text-muted-foreground"
              }`}>
                <Activity className="h-4 w-4 inline-block mr-1" />
                Cross-Reference Demo
              </span>
            </Link>
            <Link href="/resource-allocation">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/resource-allocation") ? "text-primary" : "text-muted-foreground"
              }`}>
                <FileText className="h-4 w-4 inline-block mr-1" />
                Compliance Reports
              </span>
            </Link>
            <Link href="/ethical-ai">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/ethical-ai") ? "text-primary" : "text-muted-foreground"
              }`}>
                <AlertTriangle className="h-4 w-4 inline-block mr-1" />
                Risk Assessment
              </span>
            </Link>
            <Link href="/tas-integration">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/tas-integration") ? "text-primary" : "text-muted-foreground"
              }`}>
                <Zap className="h-4 w-4 inline-block mr-1" />
                TAS Integration
              </span>
            </Link>
            <Link href="/pattern-sharing">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/pattern-sharing") ? "text-primary" : "text-muted-foreground"
              }`}>
                <Share2 className="h-4 w-4 inline-block mr-1" />
                Pattern Sharing
              </span>
            </Link>
            <Link href="/medical-testing">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/medical-testing") ? "text-primary" : "text-muted-foreground"
              }`}>
                <Stethoscope className="h-4 w-4 inline-block mr-1" />
                Medical Testing
              </span>
            </Link>
            <Link href="/dimensional-boundary">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/dimensional-boundary") ? "text-primary" : "text-muted-foreground"
              }`}>
                <Layers className="h-4 w-4 inline-block mr-1" />
                Dimension Simulation
              </span>
            </Link>
            <Link href="/akashic-vibe-function">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/akashic-vibe-function") ? "text-primary" : "text-muted-foreground"
              }`}>
                <Sparkles className="h-4 w-4 inline-block mr-1" />
                Akashic Vibe Function
              </span>
            </Link>
            <Link href="/tarsi-pilot-program">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/tarsi-pilot-program") ? "text-primary" : "text-muted-foreground"
              }`}>
                <HelpingHand className="h-4 w-4 inline-block mr-1" />
                TARSI Pilot Program
              </span>
            </Link>
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" asChild>
            <Link href="/documentation">
              <FileText className="mr-2 h-4 w-4" />
              Documentation
            </Link>
          </Button>
          <Button variant="outline" className="hidden sm:inline-flex" asChild>
            <Link href="/verification">
              <Shield className="mr-2 h-4 w-4" />
              Compliance Check
            </Link>
          </Button>
          <Button variant="default" className="hidden sm:inline-flex" asChild>
            <Link href="/pricing">
              <BarChart4 className="mr-2 h-4 w-4" />
              Enterprise Plans
            </Link>
          </Button>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}