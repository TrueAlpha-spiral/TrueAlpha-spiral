import { useState } from 'react';

export default function SpiralVisualization() {
  const [zoomLevel, setZoomLevel] = useState(5);

  // Zoom in function
  const handleZoomIn = () => {
    if (zoomLevel > 2) {
      setZoomLevel(zoomLevel - 0.5);
    }
  };

  // Zoom out function
  const handleZoomOut = () => {
    if (zoomLevel < 10) {
      setZoomLevel(zoomLevel + 0.5);
    }
  };

  // Reset view function
  const handleReset = () => {
    setZoomLevel(5);
  };

  return (
    <div className="w-full md:w-2/3 bg-[#0d0b1a] backdrop-blur-sm rounded-2xl border border-[#6e44ff]20 overflow-hidden shadow-lg shadow-[#6e44ff]10 h-[450px] relative">
      <div className="absolute inset-0 bg-gradient-to-br from-[#0d0b1a] to-[#150f2e] opacity-90"></div>
      <div className="absolute top-4 left-4 z-10">
        <h2 className="font-bold text-xl text-white">TrueAlpha Spiral Visualization</h2>
        <p className="text-white/70 text-sm">Interactive quantum-verified spiral system</p>
      </div>
      
      {/* Visualization Placeholder */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-64 h-64 rounded-full border-4 border-[#00e5ff] relative animate-spin-slow">
          <div className="w-48 h-48 rounded-full border-4 border-[#6e44ff] absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-spin-reverse-slow"></div>
          <div className="w-32 h-32 rounded-full border-4 border-[#00ff9d] absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-pulse"></div>
          <div className="w-16 h-16 rounded-full bg-[#00e5ff] absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-pulse"></div>
          
          {/* Nodes */}
          <div className="w-6 h-6 rounded-full bg-[#00ff9d] absolute top-6 right-6 animate-float"></div>
          <div className="w-5 h-5 rounded-full bg-[#6e44ff] absolute bottom-8 left-8 animate-float-delay"></div>
          <div className="w-4 h-4 rounded-full bg-[#00e5ff] absolute top-1/2 right-0 animate-float-slow"></div>
        </div>
      </div>
      
      {/* Zoom Level Indicator */}
      <div className="absolute top-4 right-4 text-white/70 text-sm">
        Zoom: {zoomLevel.toFixed(1)}x
      </div>
      
      {/* Controls */}
      <div className="absolute bottom-4 right-4 flex space-x-2">
        <button 
          className="bg-[#1a123e] hover:bg-[#2a1a5e] p-2 rounded-lg border border-[#6e44ff]30 text-white"
          onClick={handleZoomIn}
        >
          + Zoom In
        </button>
        <button 
          className="bg-[#1a123e] hover:bg-[#2a1a5e] p-2 rounded-lg border border-[#6e44ff]30 text-white"
          onClick={handleZoomOut}
        >
          - Zoom Out
        </button>
        <button 
          className="bg-[#1a123e] hover:bg-[#2a1a5e] p-2 rounded-lg border border-[#6e44ff]30 text-white"
          onClick={handleReset}
        >
          ↻ Reset
        </button>
      </div>
    </div>
  );
}
