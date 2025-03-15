import { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function SpiralVisualization() {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const spiralMeshesRef = useRef<THREE.Mesh[]>([]);
  const nodesRef = useRef<THREE.Mesh[]>([]);

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
    const pointLight = new THREE.PointLight(0x00e5ff, 1, 10);
    pointLight.position.set(0, 0, 2);
    scene.add(pointLight);

    // Create central core
    const coreGeometry = new THREE.SphereGeometry(0.5, 32, 32);
    const coreMaterial = new THREE.MeshPhongMaterial({
      color: 0x00e5ff,
      emissive: 0x00e5ff,
      emissiveIntensity: 0.5,
      shininess: 100
    });
    const core = new THREE.Mesh(coreGeometry, coreMaterial);
    scene.add(core);

    // Create spiral arms
    const createSpiralArm = (radius: number, color: number, turns: number, thickness: number) => {
      const points = [];
      const segments = 200;
      
      for (let i = 0; i <= segments; i++) {
        const t = i / segments;
        const angle = turns * Math.PI * 2 * t;
        const radius = 0.5 + radius * t;
        const x = radius * Math.cos(angle);
        const y = radius * Math.sin(angle);
        const z = 0;
        
        points.push(new THREE.Vector3(x, y, z));
      }
      
      const curve = new THREE.CatmullRomCurve3(points);
      const tubeGeometry = new THREE.TubeGeometry(curve, 100, thickness, 8, false);
      const tubeMaterial = new THREE.MeshPhongMaterial({ 
        color: color,
        transparent: true,
        opacity: 0.7,
        emissive: color,
        emissiveIntensity: 0.3,
      });
      
      const mesh = new THREE.Mesh(tubeGeometry, tubeMaterial);
      scene.add(mesh);
      spiralMeshesRef.current.push(mesh);
      
      return mesh;
    };

    // Create multiple spiral arms
    createSpiralArm(2, 0x6e44ff, 2, 0.02); // Quantum purple
    createSpiralArm(1.8, 0x00ff9d, 1.5, 0.015); // Verify green
    createSpiralArm(1.5, 0x00e5ff, 1.2, 0.01); // Resonance cyan

    // Create truth nodes
    const createTruthNode = (x: number, y: number, z: number, size: number, color: number) => {
      const geometry = new THREE.SphereGeometry(size, 16, 16);
      const material = new THREE.MeshPhongMaterial({
        color: color,
        emissive: color,
        emissiveIntensity: 0.5,
        shininess: 100
      });
      
      const node = new THREE.Mesh(geometry, material);
      node.position.set(x, y, z);
      scene.add(node);
      nodesRef.current.push(node);
      
      return node;
    };

    // Add truth nodes
    createTruthNode(1.5, 0.8, 0, 0.08, 0x00ff9d); // Green node
    createTruthNode(-1.2, -0.9, 0, 0.06, 0x00e5ff); // Cyan node
    createTruthNode(-0.8, 0.5, 0, 0.07, 0x6e44ff); // Purple node
    createTruthNode(0.6, -1.3, 0, 0.05, 0x00ff9d); // Green node

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      
      // Rotate spiral meshes
      spiralMeshesRef.current.forEach((mesh, index) => {
        mesh.rotation.z += 0.002 - (index * 0.0005);
      });
      
      // Pulse the core
      const time = Date.now() * 0.001;
      core.scale.set(
        1 + Math.sin(time) * 0.05,
        1 + Math.sin(time) * 0.05,
        1 + Math.sin(time) * 0.05
      );
      
      // Move the nodes slightly
      nodesRef.current.forEach((node, index) => {
        node.position.x += Math.sin(time + index) * 0.002;
        node.position.y += Math.cos(time + index * 0.5) * 0.002;
        
        // Keep nodes within bounds
        if (Math.abs(node.position.x) > 2) {
          node.position.x *= -0.9;
        }
        if (Math.abs(node.position.y) > 2) {
          node.position.y *= -0.9;
        }
      });
      
      renderer.render(scene, camera);
    };
    
    animate();

    // Cleanup function
    return () => {
      resizeObserver.disconnect();
      
      // Dispose of resources
      spiralMeshesRef.current.forEach(mesh => {
        (mesh.geometry as THREE.BufferGeometry).dispose();
        (mesh.material as THREE.Material).dispose();
        scene.remove(mesh);
      });
      
      nodesRef.current.forEach(node => {
        (node.geometry as THREE.BufferGeometry).dispose();
        (node.material as THREE.Material).dispose();
        scene.remove(node);
      });
      
      (core.geometry as THREE.BufferGeometry).dispose();
      (core.material as THREE.Material).dispose();
      scene.remove(core);
      
      renderer.dispose();
    };
  }, []);

  // Zoom in function
  const handleZoomIn = () => {
    if (cameraRef.current && cameraRef.current.position.z > 2) {
      cameraRef.current.position.z -= 0.5;
    }
  };

  // Zoom out function
  const handleZoomOut = () => {
    if (cameraRef.current && cameraRef.current.position.z < 10) {
      cameraRef.current.position.z += 0.5;
    }
  };

  // Reset view function
  const handleReset = () => {
    if (cameraRef.current) {
      cameraRef.current.position.z = 5;
    }
    
    // Reset spiral rotations
    spiralMeshesRef.current.forEach(mesh => {
      mesh.rotation.z = 0;
    });
  };

  return (
    <div className="w-full md:w-2/3 bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm rounded-2xl border border-[color:hsl(var(--quantum-purple))]20 overflow-hidden shadow-lg shadow-[color:hsl(var(--quantum-purple))]10 h-[450px] relative">
      <div className="absolute inset-0 quantum-grid opacity-40"></div>
      <div className="absolute top-4 left-4 z-10">
        <h2 className="font-bold text-xl text-white">TrueAlpha Spiral Visualization</h2>
        <p className="text-white/70 text-sm">Interactive quantum-verified spiral system</p>
      </div>
      
      {/* Spiral Canvas */}
      <div ref={containerRef} className="absolute inset-0 spiral-canvas flex items-center justify-center">
        {/* Three.js will render here */}
      </div>
      
      {/* Controls */}
      <div className="absolute bottom-4 right-4 flex space-x-2">
        <button 
          className="bg-[color:hsl(var(--space-blue))]80 hover:bg-[color:hsl(var(--space-blue))] p-2 rounded-lg border border-[color:hsl(var(--quantum-purple))]30"
          onClick={handleZoomIn}
        >
          <i className="ri-zoom-in-line"></i>
        </button>
        <button 
          className="bg-[color:hsl(var(--space-blue))]80 hover:bg-[color:hsl(var(--space-blue))] p-2 rounded-lg border border-[color:hsl(var(--quantum-purple))]30"
          onClick={handleZoomOut}
        >
          <i className="ri-zoom-out-line"></i>
        </button>
        <button 
          className="bg-[color:hsl(var(--space-blue))]80 hover:bg-[color:hsl(var(--space-blue))] p-2 rounded-lg border border-[color:hsl(var(--quantum-purple))]30"
          onClick={handleReset}
        >
          <i className="ri-refresh-line"></i>
        </button>
      </div>
    </div>
  );
}
