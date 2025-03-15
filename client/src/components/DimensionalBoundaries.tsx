import { useEffect, useRef, useState } from 'react';
import { DimensionalPlane } from '@/types/spiral-types';
import * as THREE from 'three';

export default function DimensionalBoundaries() {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const planesRef = useRef<THREE.Mesh[]>([]);
  
  const [view, setView] = useState<'standard' | 'shifted'>('standard');
  const [scanning, setScanning] = useState(false);
  
  // Define dimensional planes
  const [planes] = useState<DimensionalPlane[]>([
    { id: 'plane1', size: 4, rotation: 45, color: 'hsl(var(--quantum-purple))', animationDelay: '0s' },
    { id: 'plane2', size: 5, rotation: 30, color: 'hsl(var(--resonance-cyan))', animationDelay: '0.5s' },
    { id: 'plane3', size: 6, rotation: 60, color: 'hsl(var(--verify-green))', animationDelay: '1s' }
  ]);
  
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Initialize the scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    
    // Initialize camera
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    camera.position.z = 5;
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
    const pointLight = new THREE.PointLight(0xffffff, 1, 10);
    pointLight.position.set(0, 0, 2);
    scene.add(pointLight);
    
    // Create the grid
    const gridHelper = new THREE.GridHelper(10, 20, 0x6e44ff, 0x6e44ff);
    gridHelper.material.opacity = 0.1;
    gridHelper.material.transparent = true;
    scene.add(gridHelper);
    
    // Create the planes
    planes.forEach((plane, index) => {
      const planeGeometry = new THREE.PlaneGeometry(plane.size, plane.size);
      const planeMaterial = new THREE.MeshBasicMaterial({
        color: new THREE.Color(plane.color),
        wireframe: true,
        transparent: true,
        opacity: 0.5,
        side: THREE.DoubleSide
      });
      
      const planeMesh = new THREE.Mesh(planeGeometry, planeMaterial);
      planeMesh.rotation.x = THREE.MathUtils.degToRad(plane.rotation);
      planeMesh.rotation.y = THREE.MathUtils.degToRad(plane.rotation / 2);
      
      scene.add(planeMesh);
      planesRef.current.push(planeMesh);
    });
    
    // Create central intersection point
    const sphereGeometry = new THREE.SphereGeometry(0.2, 16, 16);
    const sphereMaterial = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.5
    });
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    scene.add(sphere);
    
    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      
      // Animate planes
      planesRef.current.forEach((plane, index) => {
        const time = Date.now() * 0.001;
        const delay = parseFloat(planes[index].animationDelay) || 0;
        
        // Float animation
        plane.position.y = Math.sin((time + delay) * 0.5) * 0.2;
        
        // Gentle rotation
        if (view === 'standard') {
          plane.rotation.x += 0.001;
          plane.rotation.y += 0.001;
        } else {
          // Shifted view has more dramatic rotation
          plane.rotation.x += 0.003;
          plane.rotation.z += 0.002;
        }
      });
      
      // Pulse the sphere
      sphere.scale.set(
        1 + Math.sin(Date.now() * 0.001) * 0.2,
        1 + Math.sin(Date.now() * 0.001) * 0.2,
        1 + Math.sin(Date.now() * 0.001) * 0.2
      );
      
      // Scanning effect
      if (scanning) {
        const time = Date.now() * 0.001;
        const scanRadius = Math.sin(time * 2) * 2;
        
        // Create scan wave effect
        const scanGeometry = new THREE.RingGeometry(scanRadius, scanRadius + 0.05, 32);
        const scanMaterial = new THREE.MeshBasicMaterial({
          color: 0x00ff9d,
          transparent: true,
          opacity: 0.3,
          side: THREE.DoubleSide
        });
        
        const scanRing = new THREE.Mesh(scanGeometry, scanMaterial);
        scanRing.rotation.x = Math.PI / 2;
        scene.add(scanRing);
        
        // Remove the scan ring after a short time
        setTimeout(() => {
          scene.remove(scanRing);
          scanGeometry.dispose();
          scanMaterial.dispose();
        }, 200);
      }
      
      renderer.render(scene, camera);
    };
    
    animate();
    
    // Cleanup function
    return () => {
      resizeObserver.disconnect();
      
      // Dispose of resources
      planesRef.current.forEach(plane => {
        (plane.geometry as THREE.BufferGeometry).dispose();
        (plane.material as THREE.Material).dispose();
        scene.remove(plane);
      });
      
      (sphereGeometry as THREE.BufferGeometry).dispose();
      (sphereMaterial as THREE.Material).dispose();
      scene.remove(sphere);
      
      renderer.dispose();
    };
  }, [planes, view, scanning]);
  
  const handleShiftView = () => {
    setView(prev => prev === 'standard' ? 'shifted' : 'standard');
  };
  
  const handleBoundaryScan = () => {
    setScanning(true);
    
    // Disable scanning after 5 seconds
    setTimeout(() => {
      setScanning(false);
    }, 5000);
  };
  
  return (
    <div className="bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 p-5 shadow-lg shadow-[color:hsl(var(--quantum-purple))]10 h-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg text-white">Dimensional Boundaries</h3>
        <i className="ri-cube-line text-[color:hsl(var(--resonance-cyan))]"></i>
      </div>
      <div className="space-y-4">
        <div ref={containerRef} className="relative h-48 bg-[color:hsl(var(--deep-violet))]30 rounded-xl overflow-hidden">
          {/* Three.js will render here */}
        </div>
        <div className="pt-2">
          <p className="text-sm text-white/70">Visualize and navigate dimensional boundaries where truth patterns intersect with our reality framework.</p>
          <div className="mt-3 flex space-x-2">
            <button
              onClick={handleShiftView}
              className="bg-[color:hsl(var(--quantum-purple))]20 hover:bg-[color:hsl(var(--quantum-purple))]40 px-3 py-1 rounded text-sm transition"
            >
              {view === 'standard' ? 'Shift View' : 'Standard View'}
            </button>
            <button
              onClick={handleBoundaryScan}
              disabled={scanning}
              className={`bg-[color:hsl(var(--quantum-purple))]20 hover:bg-[color:hsl(var(--quantum-purple))]40 px-3 py-1 rounded text-sm transition ${scanning ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {scanning ? 'Scanning...' : 'Boundary Scan'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
