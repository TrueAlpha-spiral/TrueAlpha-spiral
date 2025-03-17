import React from "react";
import { Link } from "wouter";
import { Shield } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t py-6 md:py-10">
      <div className="container flex flex-col md:flex-row justify-between items-center">
        <div className="flex flex-col items-center md:items-start gap-2 mb-4 md:mb-0">
          <div className="flex items-center space-x-2">
            <Shield className="h-5 w-5 text-primary" />
            <span className="font-bold">TrueAlphaSpiral</span>
          </div>
          <p className="text-sm text-muted-foreground text-center md:text-left">
            Bridging universal truth with human cognition
          </p>
          <p className="text-xs text-muted-foreground">
            © {new Date().getFullYear()} Russell Nordland. All rights reserved.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-8 text-sm">
          <div className="flex flex-col gap-2">
            <h3 className="font-medium">Applications</h3>
            <Link href="/ai-audit">
              <a className="text-muted-foreground hover:text-primary transition-colors">
                AI Auditing
              </a>
            </Link>
            <Link href="/resource-allocation">
              <a className="text-muted-foreground hover:text-primary transition-colors">
                Resource Allocation
              </a>
            </Link>
            <Link href="/ethical-ai">
              <a className="text-muted-foreground hover:text-primary transition-colors">
                Ethical AI
              </a>
            </Link>
            <Link href="/ip-protection">
              <a className="text-muted-foreground hover:text-primary transition-colors">
                IP Protection
              </a>
            </Link>
          </div>

          <div className="flex flex-col gap-2">
            <h3 className="font-medium">Resources</h3>
            <Link href="/documentation">
              <a className="text-muted-foreground hover:text-primary transition-colors">
                Documentation
              </a>
            </Link>
            <Link href="/verification">
              <a className="text-muted-foreground hover:text-primary transition-colors">
                Verification
              </a>
            </Link>
            <Link href="/about">
              <a className="text-muted-foreground hover:text-primary transition-colors">
                About
              </a>
            </Link>
          </div>

          <div className="flex flex-col gap-2 col-span-2 md:col-span-1">
            <h3 className="font-medium">Core Concepts</h3>
            <p className="text-xs text-muted-foreground">
              Quantum Authentication
            </p>
            <p className="text-xs text-muted-foreground">
              Truth Pattern Recognition
            </p>
            <p className="text-xs text-muted-foreground">
              Sovereign Equation Protection
            </p>
            <p className="text-xs font-mono text-muted-foreground mt-2">
              S(t+1) = S(t) + α[...]
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}