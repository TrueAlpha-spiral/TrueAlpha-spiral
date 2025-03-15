export default function Footer() {
  return (
    <footer className="py-6 px-6 border-t border-[color:hsl(var(--quantum-purple))]30 bg-[color:hsl(var(--cosmic-dark))]30">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <div className="w-8 h-8 hexagon bg-[color:hsl(var(--quantum-purple))] flex items-center justify-center">
              <i className="ri-spiral-line text-white text-sm"></i>
            </div>
            <div>
              <h2 className="font-bold text-lg tracking-tight">
                <span className="text-[color:hsl(var(--resonance-cyan))]">True</span>
                <span className="text-[color:hsl(var(--verify-green))]">Alpha</span>
              </h2>
              <p className="text-white/50 text-xs">Sovereign Authorship System</p>
            </div>
          </div>
          
          <div className="text-center md:text-right">
            <div className="text-white/70 text-sm">
              Architect: Russell Nordland
            </div>
            <div className="text-white/50 text-xs mt-1">
              Protected by Immutable Proof of Authorship
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
