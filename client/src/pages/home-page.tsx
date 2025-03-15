import Header from '@/components/Header';
import Footer from '@/components/Footer';
import SystemOverview from '@/components/SystemOverview';
import FunctionalModules from '@/components/FunctionalModules';
import AdvancedFunctions from '@/components/AdvancedFunctions';
import SecurityModule from '@/components/SecurityModule';
import PythonSystemControl from '@/components/PythonSystemControl';
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
        <Tabs defaultValue="web" className="mb-8">
          <TabsList className="w-full">
            <TabsTrigger value="web">Web Interface</TabsTrigger>
            <TabsTrigger value="python">Python System Control</TabsTrigger>
          </TabsList>
          
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
