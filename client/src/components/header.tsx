import React from "react";
import { Link, useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { Shield } from "lucide-react";

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
            <Link href="/ai-audit">
              <a className={`text-sm font-medium transition-colors hover:text-primary ${
                isActiveLink("/ai-audit") ? "text-primary" : "text-muted-foreground"
              }`}>
                AI Auditing
              </a>
            </Link>
            <Link href="/resource-allocation">
              <a className={`text-sm font-medium transition-colors hover:text-primary ${
                isActiveLink("/resource-allocation") ? "text-primary" : "text-muted-foreground"
              }`}>
                Resource Allocation
              </a>
            </Link>
            <Link href="/ethical-ai">
              <a className={`text-sm font-medium transition-colors hover:text-primary ${
                isActiveLink("/ethical-ai") ? "text-primary" : "text-muted-foreground"
              }`}>
                Ethical AI
              </a>
            </Link>
            <Link href="/ip-protection">
              <a className={`text-sm font-medium transition-colors hover:text-primary ${
                isActiveLink("/ip-protection") ? "text-primary" : "text-muted-foreground"
              }`}>
                IP Protection
              </a>
            </Link>
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <Link href="/documentation">
            <Button variant="ghost">Documentation</Button>
          </Link>
          <Link href="/verification">
            <Button variant="outline" className="hidden sm:inline-flex">
              <Shield className="mr-2 h-4 w-4" />
              Verification
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
}