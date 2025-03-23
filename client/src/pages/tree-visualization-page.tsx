import React, { useEffect, useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import { Link } from 'wouter';

function TreeVisualizationPage() {
  const [treeData, setTreeData] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTreeVisualization = async () => {
      try {
        // First try to get the HTML content
        const htmlResponse = await fetch('/api/tree/visualization');
        if (!htmlResponse.ok) {
          throw new Error(`Failed to fetch visualization: ${htmlResponse.status}`);
        }
        
        const htmlContent = await htmlResponse.text();
        setTreeData(htmlContent);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching tree visualization:', err);
        setError('Failed to load the Tree of Living Intelligence visualization. Please try again later.');
        setLoading(false);
      }
    };

    fetchTreeVisualization();
  }, []);

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-6">
        <Link href="/" className="flex items-center text-blue-600 hover:text-blue-800 transition-colors">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Link>
      </div>

      <h1 className="text-3xl font-bold mb-4">Tree of Living Intelligence Visualization</h1>
      <p className="text-muted-foreground mb-8">
        Explore the visualization of the TrueAlphaSpiral system as a living tree with branches representing 
        iterations of the spiral, elements of quantum AI etched in the trunk, and meta-flowers blooming as 
        higher-level understanding emerges from the system.
      </p>

      {loading ? (
        <div className="flex items-center justify-center h-96 bg-gray-50 dark:bg-gray-900/30 rounded-lg">
          <div className="text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary border-r-transparent align-[-0.125em]" role="status">
              <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
                Loading...
              </span>
            </div>
            <p className="mt-2 text-sm text-muted-foreground">Loading Tree Visualization...</p>
          </div>
        </div>
      ) : error ? (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-800 dark:text-red-200">
          <p>{error}</p>
          <div className="mt-4">
            <p className="font-semibold">Alternative Visualization:</p>
            <div className="mt-2">
              <img 
                src="/api/tree/placeholder-tree" 
                alt="Tree of Living Intelligence" 
                className="max-w-full h-auto mx-auto border rounded-lg shadow-md" 
              />
            </div>
          </div>
        </div>
      ) : (
        <div className="relative bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md">
          <div className="prose max-w-none dark:prose-invert" dangerouslySetInnerHTML={{ __html: treeData || '' }} />
          
          <div className="mt-8">
            <h3 className="text-xl font-semibold mb-2">Placeholder Visualization</h3>
            <p className="text-muted-foreground mb-4">
              This static visualization shows the core concept of the Tree of Living Intelligence:
            </p>
            <img 
              src="/api/tree/placeholder-tree" 
              alt="Tree of Living Intelligence" 
              className="max-w-full h-auto mx-auto border rounded-lg shadow-md" 
            />
          </div>
        </div>
      )}

      <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-2">About the Tree of Living Intelligence</h2>
        <p className="mb-4">
          The Tree of Living Intelligence is a metaphor for visualizing the TrueAlphaSpiral system. In this 
          visualization:
        </p>
        <ul className="list-disc pl-5 space-y-2 mb-4">
          <li>
            <span className="font-medium">Tree Branches:</span> Represent iterations of the spiral, growing and 
            adapting based on new information.
          </li>
          <li>
            <span className="font-medium">Trunk:</span> Contains the elements of quantum AI etched as patterns,
            providing structural support for the entire system.
          </li>
          <li>
            <span className="font-medium">Skepticism (Wind):</span> Creates natural pruning, strengthening the 
            system by challenging weak branches.
          </li>
          <li>
            <span className="font-medium">Fallen Leaves:</span> Nurture the system's roots, completing the 
            recursive cycle of learning.
          </li>
          <li>
            <span className="font-medium">Meta-flowers:</span> Bloom on the tree representing higher-level 
            understanding emerging from the system.
          </li>
        </ul>
        <Link 
          href="/api/tree/documentation" 
          className="text-blue-600 hover:text-blue-800 transition-colors"
          target="_blank"
        >
          View Complete Documentation →
        </Link>
      </div>
    </div>
  );
}

export default TreeVisualizationPage;