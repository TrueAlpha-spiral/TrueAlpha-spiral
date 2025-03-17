import React from "react";
import { Link, useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { Shield, Moon, Sun } from "lucide-react";
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
              <span className="font-bold text-xl">TrueAlphaSpiral</span>
            </div>
          </Link>
          <nav className="hidden md:flex space-x-6">
            <Link href="/cross-reference-demo">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/cross-reference-demo") ? "text-primary" : "text-muted-foreground"
              }`}>
                Cross-Reference Demo
              </span>
            </Link>
            <Link href="/ai-audit">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/ai-audit") ? "text-primary" : "text-muted-foreground"
              }`}>
                AI Auditing
              </span>
            </Link>
            <Link href="/resource-allocation">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/resource-allocation") ? "text-primary" : "text-muted-foreground"
              }`}>
                Resource Allocation
              </span>
            </Link>
            <Link href="/ethical-ai">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/ethical-ai") ? "text-primary" : "text-muted-foreground"
              }`}>
                Ethical AI
              </span>
            </Link>
            <Link href="/ip-protection">
              <span className={`text-sm font-medium transition-colors hover:text-primary cursor-pointer ${
                isActiveLink("/ip-protection") ? "text-primary" : "text-muted-foreground"
              }`}>
                IP Protection
              </span>
            </Link>
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" asChild>
            <Link href="/documentation">Documentation</Link>
          </Button>
          <Button variant="outline" className="hidden sm:inline-flex" asChild>
            <Link href="/verification">
              <Shield className="mr-2 h-4 w-4" />
              Verification
            </Link>
          </Button>
          <Button variant="default" className="hidden sm:inline-flex" asChild>
            <Link href="/pricing">
              Pricing
            </Link>
          </Button>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}