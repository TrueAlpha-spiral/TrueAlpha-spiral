import { useAuth } from "@/hooks/use-auth";
import { Button } from "@/components/ui/button";

export default function Header() {
  const { user, logoutMutation } = useAuth();
  
  const handleLogout = () => {
    logoutMutation.mutate();
  };
  
  return (
    <header className="py-4 px-6 md:px-12 backdrop-blur-sm bg-[color:hsl(var(--space-blue))]80 border-b border-[color:hsl(var(--quantum-purple))]30 sticky top-0 z-50">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="w-10 h-10 hexagon bg-[color:hsl(var(--quantum-purple))] flex items-center justify-center animate-pulse-glow">
            <i className="ri-spiral-line text-white text-xl"></i>
          </div>
          <h1 className="font-bold text-xl sm:text-2xl tracking-tight">
            <span className="text-[color:hsl(var(--resonance-cyan))] glow-text">True</span>
            <span className="text-[color:hsl(var(--verify-green))]">Alpha</span> Spiral
          </h1>
        </div>
        
        <div className="flex items-center space-x-4">
          {user && (
            <div className="hidden md:flex items-center space-x-1 bg-[color:hsl(var(--cosmic-dark))]50 px-3 py-1.5 rounded-lg border border-[color:hsl(var(--quantum-purple))]30">
              <i className="ri-verified-badge-fill text-[color:hsl(var(--verify-green))]"></i>
              <span className="text-sm font-mono">Verified: {user.username}</span>
            </div>
          )}
          <div className="flex space-x-2">
            {user && (
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={handleLogout} 
                className="hover:bg-[color:hsl(var(--quantum-purple))]30 transition"
                disabled={logoutMutation.isPending}
              >
                {logoutMutation.isPending ? (
                  <i className="ri-loader-2-line animate-spin"></i>
                ) : (
                  <i className="ri-logout-box-line"></i>
                )}
              </Button>
            )}
            <div className="bg-[color:hsl(var(--quantum-purple))]20 p-2 rounded-lg cursor-pointer hover:bg-[color:hsl(var(--quantum-purple))]30 transition">
              <i className="ri-settings-4-line"></i>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
