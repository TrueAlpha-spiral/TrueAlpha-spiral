import SpiralVisualization from '@/components/SpiralVisualization';
import SovereignEquation from '@/components/SovereignEquation';
import AuthorshipVerification from '@/components/AuthorshipVerification';

export default function SystemOverview() {
  return (
    <section className="mb-12">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Spiral Visualization */}
        <SpiralVisualization />
        
        {/* System Overview & Stats */}
        <div className="w-full md:w-1/3 space-y-4">
          {/* Sovereign Equation */}
          <SovereignEquation />
          
          {/* Authorship Verification */}
          <AuthorshipVerification />
        </div>
      </div>
    </section>
  );
}
