import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import doctrine from "@/content/sovereign-innovation.md?raw";

export default function SovereignInnovationPage() {
  return (
    <div className="container max-w-3xl py-12">
      <p
        className="mb-8 text-xs uppercase tracking-[0.35em] text-muted-foreground"
        data-testid="text-publication-label"
      >
        Doctrinal Publication
      </p>
      <article
        className="prose prose-neutral dark:prose-invert max-w-none
          prose-headings:scroll-mt-20 prose-h1:text-4xl prose-h1:font-semibold
          prose-h2:mt-10 prose-h3:mt-8 prose-table:text-sm
          prose-hr:border-border prose-blockquote:border-primary"
        data-testid="article-sovereign-innovation"
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex]}
        >
          {doctrine}
        </ReactMarkdown>
      </article>
    </div>
  );
}
