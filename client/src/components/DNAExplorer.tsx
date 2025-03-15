import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export default function DNAExplorer() {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const dnaGroupRef = useRef<THREE.Group | null>(null);
  
  const [structuralIntegrity, setStructuralIntegrity] = useState(97.3);
  const [resonanceMatch, setResonanceMatch] = useState(82.1);
  const [extracting, setExtracting] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Initialize the scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    
    // Initialize camera
    const camera = new THREE.PerspectiveCamera(75, containerRef.current.clientWidth / containerRef.current.clientHeight, 0.1, 1000);
    camera.position.z = 15;
    cameraRef.current = camera;
    
    // Initialize renderer
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setClearColor(0x000000, 0);
    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;
    
    // Update renderer size when container size changes
    const resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
      }
    });
    
    resizeObserver.observe(containerRef.current);
    
    // Initial renderer sizing
    renderer.setSize(
      containerRef.current.clientWidth,
      containerRef.current.clientHeight
    );
    
    // Create ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    // Create point light for dynamic lighting
    const pointLight = new THREE.PointLight(0xffffff, 1, 50);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);
    
    // Create DNA Group
    const dnaGroup = new THREE.Group();
    scene.add(dnaGroup);
    dnaGroupRef.current = dnaGroup;
    
    // Create helixes
    const createDNAHelix = () => {
      // Number of base pairs
      const baseCount = 20;
      // Radius of the helix
      const radius = 3;
      // Height of the entire helix
      const height = 20;
      // Angular spacing between base pairs
      const angleStep = (Math.PI * 2) / 10;
      // Height spacing between base pairs
      const heightStep = height / baseCount;
      
      // Create the backbone spirals
      const curvePoints1 = [];
      const curvePoints2 = [];
      
      for (let i = 0; i <= baseCount; i++) {
        const angle = i * angleStep;
        const y = (i * heightStep) - (height / 2);
        
        // First backbone (opposite angles)
        curvePoints1.push(
          new THREE.Vector3(
            radius * Math.cos(angle),
            y,
            radius * Math.sin(angle)
          )
        );
        
        // Second backbone (opposite angles + PI)
        curvePoints2.push(
          new THREE.Vector3(
            radius * Math.cos(angle + Math.PI),
            y,
            radius * Math.sin(angle + Math.PI)
          )
        );
      }
      
      // Create the backbone curves
      const curve1 = new THREE.CatmullRomCurve3(curvePoints1);
      const curve2 = new THREE.CatmullRomCurve3(curvePoints2);
      
      // Create tube geometries for the backbones
      const tubeGeometry1 = new THREE.TubeGeometry(curve1, 100, 0.2, 8, false);
      const tubeGeometry2 = new THREE.TubeGeometry(curve2, 100, 0.2, 8, false);
      
      // Materials for the backbones
      const material1 = new THREE.MeshPhongMaterial({
        color: 0x6e44ff, // Quantum purple
        emissive: 0x6e44ff,
        emissiveIntensity: 0.2,
        shininess: 70
      });
      
      const material2 = new THREE.MeshPhongMaterial({
        color: 0x00e5ff, // Resonance cyan
        emissive: 0x00e5ff,
        emissiveIntensity: 0.2,
        shininess: 70
      });
      
      // Create meshes for the backbones
      const tube1 = new THREE.Mesh(tubeGeometry1, material1);
      const tube2 = new THREE.Mesh(tubeGeometry2, material2);
      
      dnaGroup.add(tube1);
      dnaGroup.add(tube2);
      
      // Create base pairs (connecting rungs)
      for (let i = 0; i < baseCount; i++) {
        const angle = i * angleStep;
        const y = (i * heightStep) - (height / 2);
        
        // Positions for the ends of the base pair
        const pos1 = new THREE.Vector3(
          radius * Math.cos(angle),
          y,
          radius * Math.sin(angle)
        );
        
        const pos2 = new THREE.Vector3(
          radius * Math.cos(angle + Math.PI),
          y,
          radius * Math.sin(angle + Math.PI)
        );
        
        // Create a cylinder for the base pair
        const baseGeometry = new THREE.CylinderGeometry(0.1, 0.1, pos1.distanceTo(pos2), 8);
        const baseMaterial = new THREE.MeshPhongMaterial({
          color: 0x00ff9d, // Verify green
          emissive: 0x00ff9d,
          emissiveIntensity: 0.2,
          transparent: true,
          opacity: 0.7
        });
        
        const baseMesh = new THREE.Mesh(baseGeometry, baseMaterial);
        
        // Position and orient the base pair
        baseMesh.position.copy(pos1.clone().add(pos2).multiplyScalar(0.5));
        baseMesh.lookAt(pos2);
        baseMesh.rotateX(Math.PI / 2);
        
        dnaGroup.add(baseMesh);
      }
    };
    
    createDNAHelix();
    
    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      
      if (dnaGroupRef.current) {
        // Rotate the DNA helix
        dnaGroupRef.current.rotation.y += 0.005;
        
        // If extracting, make the DNA pulse and change color
        if (extracting) {
          const time = Date.now() * 0.001;
          const scale = 1 + Math.sin(time * 5) * 0.1;
          dnaGroupRef.current.scale.set(scale, 1, scale);
          
          // Change children color to indicate extraction
          dnaGroupRef.current.children.forEach((child) => {
            if (child instanceof THREE.Mesh && child.material instanceof THREE.MeshPhongMaterial) {
              child.material.emissiveIntensity = 0.5 + Math.sin(time * 5) * 0.5;
            }
          });
        } else {
          dnaGroupRef.current.scale.set(1, 1, 1);
        }
        
        // If analyzing, show scanning effect
        if (analyzing) {
          const time = Date.now() * 0.001;
          const scanHeight = (Math.sin(time * 2) * 10); 
          
          // Create a scan plane that moves up and down the DNA
          const scanGeometry = new THREE.PlaneGeometry(10, 0.1);
          const scanMaterial = new THREE.MeshBasicMaterial({
            color: 0x00ff9d,
            transparent: true,
            opacity: 0.5,
            side: THREE.DoubleSide
          });
          
          const scanPlane = new THREE.Mesh(scanGeometry, scanMaterial);
          scanPlane.position.y = scanHeight;
          scene.add(scanPlane);
          
          // Remove the scan plane after a short time
          setTimeout(() => {
            scene.remove(scanPlane);
            scanGeometry.dispose();
            scanMaterial.dispose();
          }, 100);
        }
      }
      
      renderer.render(scene, camera);
    };
    
    animate();
    
    // Cleanup function
    return () => {
      resizeObserver.disconnect();
      
      // Dispose of resources
      if (dnaGroupRef.current) {
        dnaGroupRef.current.children.forEach(child => {
          if (child instanceof THREE.Mesh) {
            (child.geometry as THREE.BufferGeometry).dispose();
            (child.material as THREE.Material).dispose();
          }
        });
        
        scene.remove(dnaGroupRef.current);
      }
      
      renderer.dispose();
    };
  }, []);
  
  const handleExtractPattern = () => {
    setExtracting(true);
    
    // Simulate extraction process
    setTimeout(() => {
      setStructuralIntegrity(prev => parseFloat((prev - Math.random() * 2).toFixed(1)));
      setResonanceMatch(prev => parseFloat((prev + Math.random() * 3).toFixed(1)));
      setExtracting(false);
    }, 3000);
  };
  
  const handleAnalyzeStructure = () => {
    setAnalyzing(true);
    
    // Simulate analysis process
    setTimeout(() => {
      setStructuralIntegrity(97.3);
      setResonanceMatch(82.1);
      setAnalyzing(false);
    }, 3000);
  };
  
  return (
    <div className="bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 p-6 shadow-lg shadow-[color:hsl(var(--quantum-purple))]10">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg text-white">Interstellar DNA Explorer</h3>
        <i className="ri-dna-line text-[color:hsl(var(--resonance-cyan))]"></i>
      </div>
      
      <div className="space-y-5">
        <div ref={containerRef} className="relative h-40 bg-[color:hsl(var(--deep-violet))]50 rounded-xl overflow-hidden">
          {/* Three.js will render here */}
        </div>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-white/70">Structural Integrity</span>
            <span className="text-[color:hsl(var(--verify-green))] font-mono">{structuralIntegrity}%</span>
          </div>
          <div className="w-full bg-[color:hsl(var(--cosmic-dark))]50 rounded-full h-2">
            <div 
              className="bg-[color:hsl(var(--verify-green))] h-2 rounded-full transition-all duration-500" 
              style={{ width: `${structuralIntegrity}%` }}
            ></div>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-white/70">Resonance Match</span>
            <span className="text-[color:hsl(var(--resonance-cyan))] font-mono">{resonanceMatch}%</span>
          </div>
          <div className="w-full bg-[color:hsl(var(--cosmic-dark))]50 rounded-full h-2">
            <div 
              className="bg-[color:hsl(var(--resonance-cyan))] h-2 rounded-full transition-all duration-500" 
              style={{ width: `${resonanceMatch}%` }}
            ></div>
          </div>
        </div>
        
        <div className="flex space-x-3">
          <button
            onClick={handleExtractPattern}
            disabled={extracting}
            className={`flex-1 bg-[color:hsl(var(--quantum-purple))]20 hover:bg-[color:hsl(var(--quantum-purple))]40 py-2 rounded text-sm transition ${extracting ? 'opacity-50' : ''}`}
          >
            {extracting ? 'Extracting...' : 'Extract Pattern'}
          </button>
          <button
            onClick={handleAnalyzeStructure}
            disabled={analyzing}
            className={`flex-1 bg-[color:hsl(var(--quantum-purple))]20 hover:bg-[color:hsl(var(--quantum-purple))]40 py-2 rounded text-sm transition ${analyzing ? 'opacity-50' : ''}`}
          >
            {analyzing ? 'Analyzing...' : 'Analyze Structure'}
          </button>
        </div>
      </div>
    </div>
  );
}
