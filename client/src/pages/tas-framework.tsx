import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { FileText, Dna } from "lucide-react";

interface TasDnaStatus {
  framework: string;
  source: string;
  pythonModules: number;
  documents: number;
}

interface TasDoc {
  id: string;
  title: string;
}

export default function TasFrameworkPage() {
  const [selectedDoc, setSelectedDoc] = useState<string>("README.md");

  const { data: status } = useQuery<TasDnaStatus>({
    queryKey: ["/api/tas-dna/status"],
  });

  const { data: docs, isLoading: docsLoading } = useQuery<TasDoc[]>({
    queryKey: ["/api/tas-dna/docs"],
  });

  const { data: docContent, isLoading: contentLoading } = useQuery<string>({
    queryKey: ["/api/tas-dna/docs", selectedDoc],
    queryFn: async () => {
      const res = await fetch(`/api/tas-dna/docs/${selectedDoc}`);
      if (!res.ok) throw new Error("Failed to load document");
      return res.text();
    },
    enabled: !!selectedDoc,
  });

  return (
    <div className="container py-10">
      <div className="mb-8 flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-3">
          <Dna className="h-8 w-8 text-primary" />
          <div>
            <h1 className="text-3xl font-bold" data-testid="text-framework-title">
              TAS_DNA Framework
            </h1>
            <p className="text-sm text-muted-foreground">
              Deterministic verification &amp; sovereign attestation core
            </p>
          </div>
        </div>
        {status && (
          <div className="ml-auto flex gap-2">
            <Badge variant="secondary" data-testid="badge-modules">
              {status.pythonModules} Python modules
            </Badge>
            <Badge variant="secondary" data-testid="badge-documents">
              {status.documents} documents
            </Badge>
          </div>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        <aside>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            Documents
          </h2>
          <ScrollArea className="h-[70vh] rounded-md border">
            <div className="p-2">
              {docsLoading &&
                Array.from({ length: 8 }).map((_, i) => (
                  <Skeleton key={i} className="mb-2 h-8 w-full" />
                ))}
              {docs?.map((doc) => (
                <button
                  key={doc.id}
                  onClick={() => setSelectedDoc(doc.id)}
                  className={`mb-1 flex w-full items-start gap-2 rounded-md px-3 py-2 text-left text-sm transition-colors hover:bg-accent ${
                    selectedDoc === doc.id ? "bg-accent font-medium" : ""
                  }`}
                  data-testid={`button-doc-${doc.id}`}
                >
                  <FileText className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
                  <span className="break-all">{doc.id}</span>
                </button>
              ))}
            </div>
          </ScrollArea>
        </aside>

        <section className="min-w-0">
          {contentLoading ? (
            <div className="space-y-3">
              <Skeleton className="h-10 w-2/3" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-5/6" />
            </div>
          ) : (
            <article
              className="prose prose-neutral dark:prose-invert max-w-none prose-table:text-sm prose-hr:border-border"
              data-testid="article-doc-content"
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeKatex]}
              >
                {docContent ?? ""}
              </ReactMarkdown>
            </article>
          )}
        </section>
      </div>
    </div>
  );
}
