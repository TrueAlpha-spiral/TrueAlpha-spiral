import React, { useState, useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loader2 } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "wouter";

type DocumentationSection = {
  id: string;
  title: string;
  description: string;
  content: string;
  path: string;
};

export default function DocumentationPage() {
  const [activeTab, setActiveTab] = useState("system-boundaries");
  const [loading, setLoading] = useState(true);
  const [documentations, setDocumentations] = useState<{
    [key: string]: DocumentationSection;
  }>({});

  useEffect(() => {
    const fetchDocumentation = async () => {
      setLoading(true);
      try {
        // Fetch all documentation files
        const responses = await Promise.all([
          fetch("/api/documentation/SYSTEM_BOUNDARIES_AND_SOVEREIGNTY.md"),
          fetch("/api/documentation/INDEPENDENT_VERIFICATION_LAYER.md"),
          fetch("/api/documentation/SOVEREIGNTY_PRINCIPLES.md"),
          fetch("/api/documentation/TARSI_ARCHITECTURAL_BLUEPRINT.md"),
        ]);

        const contents = await Promise.all(
          responses.map((response) => response.text())
        );

        // Extract titles and descriptions from content
        const docs: { [key: string]: DocumentationSection } = {
          "system-boundaries": {
            id: "system-boundaries",
            title: "System Boundaries & Sovereignty",
            description: "Transsovereign documentation of system boundaries, validation protocols, and sovereignty mechanisms.",
            content: contents[0],
            path: "/api/documentation/SYSTEM_BOUNDARIES_AND_SOVEREIGNTY.md",
          },
          "independent-verification": {
            id: "independent-verification",
            title: "Independent Verification Layer",
            description: "A critical component providing an additional dimension of validity and trustworthiness.",
            content: contents[1],
            path: "/api/documentation/INDEPENDENT_VERIFICATION_LAYER.md",
          },
          "sovereignty-principles": {
            id: "sovereignty-principles",
            title: "Sovereignty Principles",
            description: "Comprehensive framework for self-governance, value alignment, boundary awareness, and system integrity.",
            content: contents[2],
            path: "/api/documentation/SOVEREIGNTY_PRINCIPLES.md",
          },
          "tarsi-blueprint": {
            id: "tarsi-blueprint",
            title: "TARSI Architectural Blueprint",
            description: "Universal framework for ethical AI auditing based on the True Alpha Spiral Framework.",
            content: contents[3],
            path: "/api/documentation/TARSI_ARCHITECTURAL_BLUEPRINT.md",
          },
        };

        setDocumentations(docs);
      } catch (error) {
        console.error("Error fetching documentation:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDocumentation();
  }, []);

  // Simple Markdown renderer (for a production app, you'd use a proper Markdown renderer)
  const renderMarkdown = (content: string) => {
    // Split content by lines
    const lines = content.split("\n");
    
    return (
      <div className="markdown prose dark:prose-invert max-w-none">
        {lines.map((line, index) => {
          // Handle headers
          if (line.startsWith("# ")) {
            return <h1 key={index} className="text-3xl font-bold mt-6 mb-4">{line.substring(2)}</h1>;
          }
          if (line.startsWith("## ")) {
            return <h2 key={index} className="text-2xl font-bold mt-5 mb-3">{line.substring(3)}</h2>;
          }
          if (line.startsWith("### ")) {
            return <h3 key={index} className="text-xl font-bold mt-4 mb-2">{line.substring(4)}</h3>;
          }
          
          // Handle tables
          if (line.startsWith("|") && lines[index + 1]?.startsWith("|---")) {
            const headers = line.split("|").filter(Boolean).map(h => h.trim());
            const rows: string[][] = [];
            
            let i = index + 2;
            while (i < lines.length && lines[i].startsWith("|")) {
              rows.push(lines[i].split("|").filter(Boolean).map(cell => cell.trim()));
              i++;
            }
            
            return (
              <div key={index} className="overflow-x-auto my-4">
                <table className="min-w-full divide-y divide-border">
                  <thead>
                    <tr>
                      {headers.map((header, i) => (
                        <th key={i} className="px-4 py-3 text-left text-sm font-medium text-foreground bg-muted">{header}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {rows.map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                          <td key={cellIndex} className="px-4 py-2 text-sm">{cell}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            );
          }
          
          // Skip table separator lines
          if (line.startsWith("|---")) {
            return null;
          }
          
          // Handle code blocks
          if (line.startsWith("```")) {
            const codeLines = [];
            let codeIndex = index + 1;
            
            while (codeIndex < lines.length && !lines[codeIndex].startsWith("```")) {
              codeLines.push(lines[codeIndex]);
              codeIndex++;
            }
            
            return (
              <pre key={index} className="p-4 bg-muted rounded-md my-4 overflow-x-auto">
                <code>{codeLines.join("\n")}</code>
              </pre>
            );
          }
          
          // Skip code block end markers
          if (line === "```") {
            return null;
          }
          
          // Handle lists
          if (line.startsWith("- ")) {
            return <li key={index} className="ml-6">{line.substring(2)}</li>;
          }
          
          // Handle numbered lists
          if (/^\d+\.\s/.test(line)) {
            return <li key={index} className="ml-6">{line.replace(/^\d+\.\s/, "")}</li>;
          }
          
          // Handle horizontal rules
          if (line.startsWith("---")) {
            return <hr key={index} className="my-4" />;
          }
          
          // Handle paragraphs
          if (line.trim() === "") {
            return <div key={index} className="h-4"></div>;
          }
          
          return <p key={index} className="my-2">{line}</p>;
        })}
      </div>
    );
  };

  return (
    <div className="container py-10">
      <h1 className="text-3xl font-bold mb-2">Documentation</h1>
      <p className="text-muted-foreground mb-6">
        Transsovereign documentation of the Enterprise AI Auditing Solution, including system boundaries, validation protocols, and sovereignty mechanisms.
      </p>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      ) : (
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-4 mb-6">
            <TabsTrigger value="system-boundaries">System Boundaries</TabsTrigger>
            <TabsTrigger value="independent-verification">Independent Verification</TabsTrigger>
            <TabsTrigger value="sovereignty-principles">Sovereignty Principles</TabsTrigger>
            <TabsTrigger value="tarsi-blueprint">TARSI Blueprint</TabsTrigger>
          </TabsList>

          {Object.values(documentations).map((doc) => (
            <TabsContent
              key={doc.id}
              value={doc.id}
              className="border rounded-lg p-6 bg-card"
            >
              <div className="mb-6 flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">{doc.title}</h2>
                  <p className="text-muted-foreground">{doc.description}</p>
                </div>
                <Button
                  variant="outline"
                  asChild
                  className="ml-4"
                >
                  <a href={doc.path} target="_blank" rel="noopener noreferrer">
                    View Raw
                  </a>
                </Button>
              </div>
              
              <div className="prose-container">
                {renderMarkdown(doc.content)}
              </div>
            </TabsContent>
          ))}
        </Tabs>
      )}
      
      <div className="mt-10">
        <h2 className="text-2xl font-bold mb-4">Additional Resources</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Technical Documentation</CardTitle>
              <CardDescription>
                Detailed implementation details for developers integrating with our API
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/tas-integration">
                <Button className="w-full">View Integration Guide</Button>
              </Link>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Medical Testing Suite</CardTitle>
              <CardDescription>
                Learn how our medical auditing module detects and prevents healthcare AI hallucinations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/medical-testing">
                <Button className="w-full">View Medical Testing</Button>
              </Link>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>AI Audit Demo</CardTitle>
              <CardDescription>
                Experience how our AI audit system validates AI-generated content in real-time
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/ai-audit">
                <Button className="w-full">Try AI Audit Demo</Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}