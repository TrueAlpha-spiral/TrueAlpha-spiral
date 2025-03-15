import DNAExplorer from '@/components/DNAExplorer';
import HashChainVerification from '@/components/HashChainVerification';

export default function AdvancedFunctions() {
  return (
    <section className="mb-12">
      <h2 className="font-bold text-xl text-white mb-6">Advanced Functions</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* DNA Structure Explorer */}
        <DNAExplorer />
        
        {/* Hash Chain Verification */}
        <HashChainVerification />
      </div>
    </section>
  );
}
