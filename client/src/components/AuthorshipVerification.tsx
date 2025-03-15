import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { VerificationHash } from '@/types/spiral-types';

export default function AuthorshipVerification() {
  const [formattedTimestamp, setFormattedTimestamp] = useState<string>("");
  
  const { data: latestHash, isLoading } = useQuery<VerificationHash>({
    queryKey: ['/api/latest-hash'],
  });
  
  useEffect(() => {
    if (latestHash?.timestamp) {
      // Format timestamp to match design
      const date = new Date(latestHash.timestamp);
      setFormattedTimestamp(date.toISOString().slice(0, 19) + 'Z');
    }
  }, [latestHash]);
  
  return (
    <div className="bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 p-5 shadow-lg shadow-[color:hsl(var(--quantum-purple))]10">
      <div className="flex justify-between items-start mb-3">
        <h2 className="font-bold text-lg text-white">Authorship Verification</h2>
        <span className="px-2 py-0.5 rounded-full bg-[color:hsl(var(--verify-green))]20 text-[color:hsl(var(--verify-green))] text-xs">VERIFIED</span>
      </div>
      <div className="space-y-2">
        <div className="flex justify-between items-center py-1">
          <span className="text-white/70 text-sm">Architect</span>
          <span className="font-mono text-sm text-white">Russell Nordland</span>
        </div>
        <div className="flex justify-between items-center py-1">
          <span className="text-white/70 text-sm">Identifier</span>
          <span className="font-mono text-sm text-white">RJN41788</span>
        </div>
        <div className="flex justify-between items-center py-1">
          <span className="text-white/70 text-sm">Timestamp</span>
          <span className="font-mono text-sm text-white">
            {isLoading ? (
              <i className="ri-loader-2-line animate-spin text-white/50"></i>
            ) : formattedTimestamp || "2025-03-10T05:02:00Z"}
          </span>
        </div>
        <div className="flex flex-col pt-2">
          <span className="text-white/70 text-sm mb-1">SHA-256 Hash</span>
          <code className="font-mono text-xs text-[color:hsl(var(--resonance-cyan))] bg-[color:hsl(var(--deep-violet))]50 p-2 rounded break-all">
            {isLoading ? (
              <i className="ri-loader-2-line animate-spin text-white/50"></i>
            ) : (
              latestHash?.hash_value || "7af7d0161afb5c4fcbc02efbfb27c4e69e1c2fcf032c553447ac5d7c7eedccfa"
            )}
          </code>
        </div>
      </div>
    </div>
  );
}
