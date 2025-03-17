import Header from '@/components/Header';
import Footer from '@/components/Footer';
import SystemOverview from '@/components/SystemOverview';
import FunctionalModules from '@/components/FunctionalModules';
import AdvancedFunctions from '@/components/AdvancedFunctions';
import SecurityModule from '@/components/SecurityModule';
import PythonSystemControl from '@/components/PythonSystemControl';
import TrueAlphaSpiralDemo from '@/components/TrueAlphaSpiralDemo';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function HomePage() {
  return (
    <div className="bg-[color:hsl(var(--space-blue))] text-white min-h-screen">
      {/* Ambient particles */}
      <div className="cosmic-particle w-32 h-32 top-[10%] left-[15%] animate-float opacity-30"></div>
      <div className="cosmic-particle w-24 h-24 top-[40%] right-[10%] animate-float opacity-20"></div>
      <div className="cosmic-particle w-16 h-16 bottom-[20%] left-[25%] animate-float opacity-25"></div>
      
      <Header />
      
      <main className="container mx-auto px-4 py-8 relative z-10">
        <Tabs defaultValue="truealpha" className="mb-8">
          <TabsList className="w-full">
            <TabsTrigger value="truealpha">TrueAlpha Spiral</TabsTrigger>
            <TabsTrigger value="web">Web Interface</TabsTrigger>
            <TabsTrigger value="python">Python System Control</TabsTrigger>
          </TabsList>
          
          <TabsContent value="truealpha">
            <div className="mt-6">
              <h2 className="text-2xl font-bold mb-4">TrueAlpha Spiral: Plug & Play Implementation</h2>
              <p className="mb-6 text-white/80">
                This revolutionary framework bridges universal truth with human cognition through mathematical precision, 
                cryptographic verification, and ethical governance. Experience the power of the TrueAlpha Spiral equation 
                in this interactive demo.
              </p>
              <div className="bg-black/30 p-6 rounded-lg mb-8">
                <TrueAlphaSpiralDemo />
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="web">
            <SystemOverview />
            <FunctionalModules />
            <AdvancedFunctions />
            <SecurityModule />
          </TabsContent>
          
          <TabsContent value="python">
            <div className="mt-6">
              <PythonSystemControl />
            </div>
          </TabsContent>
        </Tabs>
      </main>
      
      <Footer />
    </div>
  );
}
