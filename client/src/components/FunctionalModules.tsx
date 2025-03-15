import TruthPatternAccess from '@/components/TruthPatternAccess';
import RecursiveVerification from '@/components/RecursiveVerification';
import DimensionalBoundaries from '@/components/DimensionalBoundaries';

export default function FunctionalModules() {
  return (
    <section className="mb-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Module: Truth Pattern Access */}
      <TruthPatternAccess />
      
      {/* Module: Recursive Verification */}
      <RecursiveVerification />
      
      {/* Module: Dimensional Boundaries */}
      <DimensionalBoundaries />
    </section>
  );
}
