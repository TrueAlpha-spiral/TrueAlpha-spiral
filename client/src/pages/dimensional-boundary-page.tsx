import React, { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";
import { Loader2, Maximize2, Minimize2, Play, RefreshCw, Square } from "lucide-react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";

// Define types for the simulation
type Dimension = {
  id: string;
  name: string;
  description: string;
  integrity: number;
  color: string;
  rules: string[];
};

type Entity = {
  id: string;
  name: string;
  startDimension: string;
  targetDimension: string;
  integrityImpact: number;
  crossingProbability: number;
  currentPosition: {
    x: number;
    y: number;
    dimension: string;
  };
  size: number;
  color: string;
  status: "waiting" | "crossing" | "succeeded" | "failed";
  path: Array<{x: number, y: number, dimension: string}>;
};

type SimulationState = {
  id: string;
  status: "idle" | "running" | "paused" | "completed";
  dimensions: Dimension[];
  entities: Entity[];
  crossingEvents: CrossingEvent[];
  startTime?: string;
  currentTime?: string;
  config: {
    speed: number;
    boundaryStrength: number;
    allowMultipleCrossings: boolean;
    dimensionalDecayRate: number;
  };
};

type CrossingEvent = {
  id: string;
  entityId: string;
  fromDimension: string;
  toDimension: string;
  timestamp: string;
  success: boolean;
  integrityImpact: number;
  anomalies: string[];
};

const DEFAULT_DIMENSIONS: Dimension[] = [
  { 
    id: "dim-truth", 
    name: "Truth Domain", 
    description: "The fundamental domain where objective truths reside",
    integrity: 0.95,
    color: "#6e44ff",
    rules: [
      "All statements must be verifiable",
      "Logical consistency is mandatory",
      "No contradictions allowed"
    ]
  },
  { 
    id: "dim-ethical", 
    name: "Ethical Domain", 
    description: "The domain of moral principles and ethical frameworks",
    integrity: 0.88,
    color: "#00e5ff",
    rules: [
      "Actions must consider all stakeholders",
      "Harm minimization is prioritized",
      "Transparency is required"
    ]
  },
  { 
    id: "dim-regulatory", 
    name: "Regulatory Domain", 
    description: "The domain of legal and regulatory frameworks",
    integrity: 0.92,
    color: "#00ff9d",
    rules: [
      "Compliance with applicable laws",
      "Documentation of all processes",
      "Auditability of all actions"
    ]
  }
];

export default function DimensionalBoundaryPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [activeTab, setActiveTab] = useState("simulation");
  const [selectedDimension, setSelectedDimension] = useState<string | null>(null);
  const [selectedEntity, setSelectedEntity] = useState<string | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  
  // Use query to get simulation state
  const { data: simulation, isLoading, error } = useQuery<SimulationState>({
    queryKey: ['/api/simulation/state'],
    refetchInterval: 1000, // Poll for updates
  });
  
  // Mutation for starting the simulation
  const startSimulationMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch('/api/simulation/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      return await response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/simulation/state'] });
      toast({
        title: "Simulation Started",
        description: "Dimensional boundary crossing simulation is now running",
      });
    },
    onError: (error) => {
      toast({
        title: "Error Starting Simulation",
        description: error.message,
        variant: "destructive",
      });
    },
  });
  
  // Mutation for pausing the simulation
  const pauseSimulationMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch('/api/simulation/pause', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      return await response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/simulation/state'] });
      toast({
        title: "Simulation Paused",
        description: "You can resume the simulation at any time",
      });
    },
  });
  
  // Mutation for resetting the simulation
  const resetSimulationMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch('/api/simulation/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      return await response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/simulation/state'] });
      toast({
        title: "Simulation Reset",
        description: "Simulation has been reset to initial state",
      });
      setSelectedEntity(null);
      setSelectedDimension(null);
    },
  });
  
  // Mutation for updating simulation config
  const updateConfigMutation = useMutation({
    mutationFn: async (config: SimulationState['config']) => {
      const response = await fetch('/api/simulation/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      return await response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/simulation/state'] });
      toast({
        title: "Configuration Updated",
        description: "Simulation parameters have been updated",
      });
    },
  });
  
  // Mutation for adding a new entity
  const addEntityMutation = useMutation({
    mutationFn: async (entity: Partial<Entity>) => {
      const response = await fetch('/api/simulation/entity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entity),
      });
      return await response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/simulation/state'] });
      toast({
        title: "Entity Added",
        description: "New entity has been added to the simulation",
      });
    },
  });
  
  // Effect to handle drawing the simulation
  useEffect(() => {
    if (!simulation || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw dimensions as background regions
    drawDimensions(ctx, canvas, simulation.dimensions);
    
    // Draw boundary lines between dimensions
    drawBoundaries(ctx, canvas, simulation.dimensions, simulation.config.boundaryStrength);
    
    // Draw entities
    drawEntities(ctx, simulation.entities);
    
    // Draw crossing paths
    drawCrossingPaths(ctx, simulation.entities);
    
    // Draw selected entity highlight
    if (selectedEntity) {
      const entity = simulation.entities.find(e => e.id === selectedEntity);
      if (entity) {
        drawEntityHighlight(ctx, entity);
      }
    }
    
  }, [simulation, selectedEntity, canvasRef]);
  
  const drawDimensions = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement, dimensions: Dimension[]) => {
    const width = canvas.width;
    const height = canvas.height;
    const dimensionWidth = width / dimensions.length;
    
    dimensions.forEach((dimension, index) => {
      const x = index * dimensionWidth;
      
      // Create gradient for dimension
      const gradient = ctx.createLinearGradient(x, 0, x + dimensionWidth, 0);
      gradient.addColorStop(0, `${dimension.color}22`); // More transparent
      gradient.addColorStop(0.5, `${dimension.color}44`);
      gradient.addColorStop(1, `${dimension.color}22`);
      
      ctx.fillStyle = gradient;
      ctx.fillRect(x, 0, dimensionWidth, height);
      
      // Add dimension label
      ctx.fillStyle = dimension.color;
      ctx.font = '14px "Space Grotesk", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(dimension.name, x + dimensionWidth / 2, 20);
      
      // Show integrity level indicator
      const integrityHeight = height * dimension.integrity;
      ctx.fillStyle = `${dimension.color}33`;
      ctx.fillRect(x, height - integrityHeight, dimensionWidth, integrityHeight);
      
      // Integrity label
      ctx.fillStyle = dimension.color;
      ctx.fillText(`Integrity: ${Math.round(dimension.integrity * 100)}%`, x + dimensionWidth / 2, height - 10);
    });
  };
  
  const drawBoundaries = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement, dimensions: Dimension[], boundaryStrength: number) => {
    const width = canvas.width;
    const height = canvas.height;
    const dimensionWidth = width / dimensions.length;
    
    // Draw boundaries between dimensions
    for (let i = 1; i < dimensions.length; i++) {
      const x = i * dimensionWidth;
      
      // Draw boundary line with varying intensity based on strength
      const lineWidth = boundaryStrength * 5;
      ctx.lineWidth = lineWidth;
      
      // Create boundary gradient
      const gradient = ctx.createLinearGradient(x - lineWidth/2, 0, x + lineWidth/2, 0);
      gradient.addColorStop(0, `${dimensions[i-1].color}88`);
      gradient.addColorStop(0.5, '#ffffff');
      gradient.addColorStop(1, `${dimensions[i].color}88`);
      
      ctx.strokeStyle = gradient;
      ctx.beginPath();
      ctx.moveTo(x, 30); // Start below the dimension labels
      
      // Create wavy boundary line
      for (let y = 30; y < height - 30; y += 10) {
        const waveMagnitude = boundaryStrength * 5;
        const offset = Math.sin(y / 20) * waveMagnitude;
        ctx.lineTo(x + offset, y);
      }
      
      ctx.stroke();
    }
  };
  
  const drawEntities = (ctx: CanvasRenderingContext2D, entities: Entity[]) => {
    entities.forEach(entity => {
      ctx.fillStyle = entity.color;
      
      // Add glow effect based on entity status
      ctx.shadowColor = entity.color;
      ctx.shadowBlur = entity.status === 'crossing' ? 20 : 5;
      
      // Draw the entity as a circle
      ctx.beginPath();
      ctx.arc(entity.currentPosition.x, entity.currentPosition.y, entity.size, 0, Math.PI * 2);
      ctx.fill();
      
      // Reset shadow
      ctx.shadowBlur = 0;
      
      // Add label if not tiny
      if (entity.size > 5) {
        ctx.fillStyle = '#ffffff';
        ctx.font = `${Math.max(10, entity.size / 2)}px "Space Grotesk", sans-serif`;
        ctx.textAlign = 'center';
        ctx.fillText(entity.name, entity.currentPosition.x, entity.currentPosition.y + entity.size + 15);
      }
    });
  };
  
  const drawCrossingPaths = (ctx: CanvasRenderingContext2D, entities: Entity[]) => {
    entities.forEach(entity => {
      if (entity.path.length < 2) return;
      
      // Draw the path
      ctx.strokeStyle = `${entity.color}66`; // Semi-transparent
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(entity.path[0].x, entity.path[0].y);
      
      for (let i = 1; i < entity.path.length; i++) {
        ctx.lineTo(entity.path[i].x, entity.path[i].y);
      }
      
      ctx.stroke();
    });
  };
  
  const drawEntityHighlight = (ctx: CanvasRenderingContext2D, entity: Entity) => {
    // Draw highlight around selected entity
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 3]);
    ctx.beginPath();
    ctx.arc(entity.currentPosition.x, entity.currentPosition.y, entity.size + 10, 0, Math.PI * 2);
    ctx.stroke();
    ctx.setLineDash([]);
  };
  
  const toggleFullscreen = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    if (!isFullscreen) {
      if (canvas.requestFullscreen) {
        canvas.requestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
    
    setIsFullscreen(!isFullscreen);
  };
  
  // Handler for updating simulation speed
  const handleSpeedChange = (value: number[]) => {
    if (!simulation) return;
    
    updateConfigMutation.mutate({
      ...simulation.config,
      speed: value[0],
    });
  };
  
  // Handler for updating boundary strength
  const handleBoundaryStrengthChange = (value: number[]) => {
    if (!simulation) return;
    
    updateConfigMutation.mutate({
      ...simulation.config,
      boundaryStrength: value[0],
    });
  };
  
  // Handler for toggling multiple crossings
  const handleMultipleCrossingsToggle = (value: boolean) => {
    if (!simulation) return;
    
    updateConfigMutation.mutate({
      ...simulation.config,
      allowMultipleCrossings: value,
    });
  };
  
  // Handler for dimension decay rate change
  const handleDecayRateChange = (value: number[]) => {
    if (!simulation) return;
    
    updateConfigMutation.mutate({
      ...simulation.config,
      dimensionalDecayRate: value[0],
    });
  };
  
  // Function to get status badge color
  const getStatusColor = (status: SimulationState['status']) => {
    switch (status) {
      case 'running': return 'bg-green-500';
      case 'paused': return 'bg-amber-500';
      case 'completed': return 'bg-blue-500';
      default: return 'bg-slate-500';
    }
  };

  // Function to format timestamps
  const formatTime = (timeString?: string) => {
    if (!timeString) return 'N/A';
    const date = new Date(timeString);
    return date.toLocaleTimeString();
  };
  
  // Mock data if the simulation is still loading
  const mockSimulation: SimulationState = {
    id: 'sim-initial',
    status: 'idle',
    dimensions: DEFAULT_DIMENSIONS,
    entities: [],
    crossingEvents: [],
    config: {
      speed: 0.5,
      boundaryStrength: 0.7,
      allowMultipleCrossings: false,
      dimensionalDecayRate: 0.02,
    }
  };

  const simulationData = simulation || mockSimulation;
  
  return (
    <div className="container py-10">
      <h1 className="text-3xl font-bold mb-2">Dimensional Boundary Crossing Simulation</h1>
      <p className="text-muted-foreground mb-6">
        Visualize and simulate how entities cross between different conceptual dimensions, observing boundary integrity and verification protocols in action.
      </p>
      
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid grid-cols-3 mb-6">
          <TabsTrigger value="simulation">Simulation</TabsTrigger>
          <TabsTrigger value="configuration">Configuration</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
        </TabsList>
        
        <TabsContent value="simulation" className="space-y-4">
          <div className="flex space-x-4">
            <div className="w-3/4">
              <Card className="relative">
                <CardHeader className="pb-2">
                  <div className="flex justify-between items-center">
                    <CardTitle>Boundary Crossing Visualization</CardTitle>
                    <div className="flex items-center space-x-2">
                      <Badge className={getStatusColor(simulationData.status)}>
                        {simulationData.status.charAt(0).toUpperCase() + simulationData.status.slice(1)}
                      </Badge>
                      <Button variant="outline" size="sm" onClick={toggleFullscreen}>
                        {isFullscreen ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
                      </Button>
                    </div>
                  </div>
                  <CardDescription>
                    Visualizing {simulationData.dimensions.length} dimensions and {simulationData.entities.length} entities
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="border rounded-md overflow-hidden relative" style={{ height: '500px' }}>
                    {isLoading ? (
                      <div className="absolute inset-0 flex items-center justify-center bg-black/10">
                        <Loader2 className="h-8 w-8 animate-spin text-primary" />
                      </div>
                    ) : error ? (
                      <div className="absolute inset-0 flex items-center justify-center bg-black/10">
                        <p className="text-destructive">Error loading simulation: {error.message}</p>
                      </div>
                    ) : (
                      <canvas 
                        ref={canvasRef}
                        width={800}
                        height={500}
                        className="w-full h-full"
                        onClick={(e) => {
                          // Handle canvas clicks to select entities
                          const canvas = canvasRef.current;
                          if (!canvas || !simulationData) return;
                          
                          const rect = canvas.getBoundingClientRect();
                          const x = e.clientX - rect.left;
                          const y = e.clientY - rect.top;
                          
                          // Find if an entity was clicked
                          const clickedEntity = simulationData.entities.find(entity => {
                            const dx = entity.currentPosition.x - x;
                            const dy = entity.currentPosition.y - y;
                            return Math.sqrt(dx*dx + dy*dy) <= entity.size;
                          });
                          
                          if (clickedEntity) {
                            setSelectedEntity(clickedEntity.id);
                          } else {
                            // Check if a dimension was clicked
                            const dimensionWidth = canvas.width / simulationData.dimensions.length;
                            const dimensionIndex = Math.floor(x / dimensionWidth);
                            if (dimensionIndex >= 0 && dimensionIndex < simulationData.dimensions.length) {
                              setSelectedDimension(simulationData.dimensions[dimensionIndex].id);
                            }
                          }
                        }}
                      />
                    )}
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between pt-2">
                  <div>
                    <p className="text-sm text-muted-foreground">
                      Started: {formatTime(simulationData.startTime)} | 
                      Current: {formatTime(simulationData.currentTime)}
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      onClick={() => resetSimulationMutation.mutate()}
                      variant="outline"
                      size="sm"
                      disabled={resetSimulationMutation.isPending}
                    >
                      {resetSimulationMutation.isPending ? (
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      ) : (
                        <RefreshCw className="h-4 w-4 mr-2" />
                      )}
                      Reset
                    </Button>
                    
                    {simulationData.status === 'running' ? (
                      <Button
                        onClick={() => pauseSimulationMutation.mutate()}
                        variant="outline"
                        size="sm"
                        disabled={pauseSimulationMutation.isPending}
                      >
                        {pauseSimulationMutation.isPending ? (
                          <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        ) : (
                          <Square className="h-4 w-4 mr-2" />
                        )}
                        Pause
                      </Button>
                    ) : (
                      <Button
                        onClick={() => startSimulationMutation.mutate()}
                        variant="default"
                        size="sm"
                        disabled={startSimulationMutation.isPending}
                      >
                        {startSimulationMutation.isPending ? (
                          <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        ) : (
                          <Play className="h-4 w-4 mr-2" />
                        )}
                        {simulationData.status === 'paused' ? 'Resume' : 'Start'}
                      </Button>
                    )}
                  </div>
                </CardFooter>
              </Card>
            </div>
            
            <div className="w-1/4 space-y-4">
              {selectedEntity && (
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">Selected Entity</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    {simulationData.entities.find(e => e.id === selectedEntity) ? (
                      <>
                        <div className="space-y-1">
                          <p className="font-medium text-lg">{simulationData.entities.find(e => e.id === selectedEntity)?.name}</p>
                          <div className="flex items-center space-x-2">
                            <div 
                              className="w-3 h-3 rounded-full" 
                              style={{ backgroundColor: simulationData.entities.find(e => e.id === selectedEntity)?.color }} 
                            />
                            <span className="text-sm font-medium">
                              Status: {simulationData.entities.find(e => e.id === selectedEntity)?.status}
                            </span>
                          </div>
                        </div>
                        
                        <Separator />
                        
                        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                          <div className="text-muted-foreground">From Dimension:</div>
                          <div>{simulationData.dimensions.find(d => 
                            d.id === simulationData.entities.find(e => e.id === selectedEntity)?.startDimension
                          )?.name}</div>
                          
                          <div className="text-muted-foreground">To Dimension:</div>
                          <div>{simulationData.dimensions.find(d => 
                            d.id === simulationData.entities.find(e => e.id === selectedEntity)?.targetDimension
                          )?.name}</div>
                          
                          <div className="text-muted-foreground">Integrity Impact:</div>
                          <div>{simulationData.entities.find(e => e.id === selectedEntity)?.integrityImpact.toFixed(2)}</div>
                          
                          <div className="text-muted-foreground">Crossing Probability:</div>
                          <div>{(simulationData.entities.find(e => e.id === selectedEntity)?.crossingProbability || 0) * 100}%</div>
                        </div>
                        
                        <Separator />
                        
                        <div className="text-sm">
                          <div className="text-muted-foreground mb-1">Crossing History:</div>
                          {simulationData.crossingEvents
                            .filter(e => e.entityId === selectedEntity)
                            .map(event => (
                              <div key={event.id} className="mb-1 p-1 rounded-sm border text-xs">
                                <div className="flex justify-between">
                                  <span className={event.success ? "text-green-500" : "text-red-500"}>
                                    {event.success ? "Success" : "Failed"}
                                  </span>
                                  <span className="text-muted-foreground">{formatTime(event.timestamp)}</span>
                                </div>
                                <div>
                                  {simulationData.dimensions.find(d => d.id === event.fromDimension)?.name} →{" "}
                                  {simulationData.dimensions.find(d => d.id === event.toDimension)?.name}
                                </div>
                                {event.anomalies.length > 0 && (
                                  <div className="mt-1">
                                    <span className="text-amber-500">Anomalies: {event.anomalies.length}</span>
                                  </div>
                                )}
                              </div>
                            ))}
                          
                          {simulationData.crossingEvents.filter(e => e.entityId === selectedEntity).length === 0 && (
                            <div className="text-muted-foreground text-xs">No crossing attempts yet</div>
                          )}
                        </div>
                      </>
                    ) : (
                      <p className="text-muted-foreground">Entity not found</p>
                    )}
                  </CardContent>
                </Card>
              )}
              
              {selectedDimension && (
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">Selected Dimension</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    {simulationData.dimensions.find(d => d.id === selectedDimension) ? (
                      <>
                        <div className="space-y-1">
                          <p className="font-medium text-lg">
                            {simulationData.dimensions.find(d => d.id === selectedDimension)?.name}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {simulationData.dimensions.find(d => d.id === selectedDimension)?.description}
                          </p>
                        </div>
                        
                        <Separator />
                        
                        <div className="space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="text-sm font-medium">Integrity</span>
                            <span className="text-sm">
                              {Math.round((simulationData.dimensions.find(d => d.id === selectedDimension)?.integrity || 0) * 100)}%
                            </span>
                          </div>
                          <div className="h-2 rounded-full overflow-hidden bg-muted">
                            <div 
                              className="h-full rounded-full"
                              style={{ 
                                width: `${Math.round((simulationData.dimensions.find(d => d.id === selectedDimension)?.integrity || 0) * 100)}%`,
                                backgroundColor: simulationData.dimensions.find(d => d.id === selectedDimension)?.color 
                              }}
                            />
                          </div>
                        </div>
                        
                        <Separator />
                        
                        <div className="space-y-1">
                          <span className="text-sm font-medium">Dimensional Rules</span>
                          <ul className="text-sm space-y-1 ml-4 list-disc">
                            {simulationData.dimensions.find(d => d.id === selectedDimension)?.rules.map((rule, i) => (
                              <li key={i}>{rule}</li>
                            ))}
                          </ul>
                        </div>
                        
                        <Separator />
                        
                        <div className="text-sm">
                          <div className="text-muted-foreground mb-1">Entities:</div>
                          <div className="grid grid-cols-2 gap-1">
                            {simulationData.entities
                              .filter(e => e.currentPosition.dimension === selectedDimension)
                              .map(entity => (
                                <div 
                                  key={entity.id}
                                  className="flex items-center space-x-1 cursor-pointer p-1 rounded hover:bg-muted"
                                  onClick={() => setSelectedEntity(entity.id)}
                                >
                                  <div 
                                    className="w-2 h-2 rounded-full" 
                                    style={{ backgroundColor: entity.color }} 
                                  />
                                  <span className="text-xs truncate">{entity.name}</span>
                                </div>
                              ))}
                            
                            {simulationData.entities.filter(e => e.currentPosition.dimension === selectedDimension).length === 0 && (
                              <div className="text-muted-foreground text-xs">No entities in this dimension</div>
                            )}
                          </div>
                        </div>
                      </>
                    ) : (
                      <p className="text-muted-foreground">Dimension not found</p>
                    )}
                  </CardContent>
                </Card>
              )}
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg">Crossing Events</CardTitle>
                </CardHeader>
                <CardContent className="h-[200px] overflow-y-auto space-y-2">
                  {simulationData.crossingEvents.length > 0 ? (
                    simulationData.crossingEvents.slice().reverse().map(event => (
                      <div 
                        key={event.id} 
                        className="p-2 text-xs border rounded-md"
                        onClick={() => setSelectedEntity(event.entityId)}
                      >
                        <div className="flex justify-between items-center">
                          <span className={`font-medium ${event.success ? "text-green-500" : "text-red-500"}`}>
                            {event.success ? "Successful Crossing" : "Failed Crossing"}
                          </span>
                          <span className="text-muted-foreground">{formatTime(event.timestamp)}</span>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Entity: </span>
                          {simulationData.entities.find(e => e.id === event.entityId)?.name}
                        </div>
                        <div>
                          <span className="text-muted-foreground">From: </span>
                          {simulationData.dimensions.find(d => d.id === event.fromDimension)?.name}
                          <span className="text-muted-foreground"> To: </span>
                          {simulationData.dimensions.find(d => d.id === event.toDimension)?.name}
                        </div>
                        {event.anomalies.length > 0 && (
                          <div className="mt-1">
                            <span className="text-amber-500">Anomalies detected: {event.anomalies.length}</span>
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="text-center text-muted-foreground">
                      No crossing events recorded yet
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
        
        <TabsContent value="configuration" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Simulation Parameters</CardTitle>
                <CardDescription>
                  Configure the behavior of the dimensional boundary simulation
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label htmlFor="simulationSpeed">Simulation Speed</Label>
                    <span className="text-sm">{simulationData.config.speed.toFixed(1)}x</span>
                  </div>
                  <Slider
                    id="simulationSpeed"
                    defaultValue={[simulationData.config.speed]}
                    min={0.1}
                    max={2}
                    step={0.1}
                    onValueChange={handleSpeedChange}
                  />
                  <p className="text-xs text-muted-foreground">
                    Controls how quickly entities move and boundaries fluctuate
                  </p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label htmlFor="boundaryStrength">Boundary Strength</Label>
                    <span className="text-sm">{Math.round(simulationData.config.boundaryStrength * 100)}%</span>
                  </div>
                  <Slider
                    id="boundaryStrength"
                    defaultValue={[simulationData.config.boundaryStrength]}
                    min={0.1}
                    max={1}
                    step={0.05}
                    onValueChange={handleBoundaryStrengthChange}
                  />
                  <p className="text-xs text-muted-foreground">
                    Determines how difficult it is to cross between dimensions
                  </p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label htmlFor="decayRate">Dimensional Decay Rate</Label>
                    <span className="text-sm">{simulationData.config.dimensionalDecayRate.toFixed(3)}</span>
                  </div>
                  <Slider
                    id="decayRate"
                    defaultValue={[simulationData.config.dimensionalDecayRate]}
                    min={0}
                    max={0.1}
                    step={0.001}
                    onValueChange={handleDecayRateChange}
                  />
                  <p className="text-xs text-muted-foreground">
                    Rate at which dimension integrity decreases with each crossing
                  </p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <Label htmlFor="multipleCrossings">Allow Multiple Crossings</Label>
                    <Button 
                      variant={simulationData.config.allowMultipleCrossings ? "default" : "outline"}
                      size="sm"
                      onClick={() => handleMultipleCrossingsToggle(!simulationData.config.allowMultipleCrossings)}
                    >
                      {simulationData.config.allowMultipleCrossings ? "Enabled" : "Disabled"}
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    When enabled, entities can attempt to cross multiple boundaries in sequence
                  </p>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>Add New Entity</CardTitle>
                <CardDescription>
                  Create a new entity to participate in the simulation
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="entityName">Entity Name</Label>
                  <Input id="entityName" placeholder="Enter entity name" />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="startDimension">Start Dimension</Label>
                    <Select>
                      <SelectTrigger id="startDimension">
                        <SelectValue placeholder="Select dimension" />
                      </SelectTrigger>
                      <SelectContent>
                        {simulationData.dimensions.map(dimension => (
                          <SelectItem key={dimension.id} value={dimension.id}>
                            {dimension.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="targetDimension">Target Dimension</Label>
                    <Select>
                      <SelectTrigger id="targetDimension">
                        <SelectValue placeholder="Select dimension" />
                      </SelectTrigger>
                      <SelectContent>
                        {simulationData.dimensions.map(dimension => (
                          <SelectItem key={dimension.id} value={dimension.id}>
                            {dimension.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="integrityImpact">Integrity Impact</Label>
                    <Select>
                      <SelectTrigger id="integrityImpact">
                        <SelectValue placeholder="Select impact" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0.01">Minimal (0.01)</SelectItem>
                        <SelectItem value="0.05">Low (0.05)</SelectItem>
                        <SelectItem value="0.1">Medium (0.1)</SelectItem>
                        <SelectItem value="0.2">High (0.2)</SelectItem>
                        <SelectItem value="0.5">Critical (0.5)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="entitySize">Entity Size</Label>
                    <Select>
                      <SelectTrigger id="entitySize">
                        <SelectValue placeholder="Select size" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="5">Small (5)</SelectItem>
                        <SelectItem value="10">Medium (10)</SelectItem>
                        <SelectItem value="15">Large (15)</SelectItem>
                        <SelectItem value="20">Extra Large (20)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                <Button className="w-full">Add Entity</Button>
              </CardContent>
            </Card>
            
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Dimension Configuration</CardTitle>
                <CardDescription>
                  Current dimensions in the simulation with their properties
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="text-left border-b">
                        <th className="pb-2">Name</th>
                        <th className="pb-2">Description</th>
                        <th className="pb-2">Integrity</th>
                        <th className="pb-2">Rules</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {simulationData.dimensions.map(dimension => (
                        <tr key={dimension.id} className="hover:bg-muted cursor-pointer" onClick={() => setSelectedDimension(dimension.id)}>
                          <td className="py-2">
                            <div className="flex items-center space-x-2">
                              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: dimension.color }} />
                              <span>{dimension.name}</span>
                            </div>
                          </td>
                          <td className="py-2 text-sm text-muted-foreground">{dimension.description}</td>
                          <td className="py-2">
                            <div className="w-24 h-2 rounded-full bg-muted overflow-hidden">
                              <div 
                                className="h-full rounded-full" 
                                style={{ 
                                  width: `${Math.round(dimension.integrity * 100)}%`,
                                  backgroundColor: dimension.color 
                                }}
                              />
                            </div>
                            <div className="text-xs text-right mt-1">{Math.round(dimension.integrity * 100)}%</div>
                          </td>
                          <td className="py-2 text-sm">
                            <span className="text-muted-foreground">{dimension.rules.length} rules</span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
        
        <TabsContent value="analysis" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Crossing Success Metrics</CardTitle>
              <CardDescription>
                Analysis of boundary crossing attempts and success rates
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg">Total Crossings</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold">{simulationData.crossingEvents.length}</div>
                      <p className="text-sm text-muted-foreground">Attempts to cross dimensional boundaries</p>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg">Success Rate</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold">
                        {simulationData.crossingEvents.length > 0 
                          ? Math.round((simulationData.crossingEvents.filter(e => e.success).length / simulationData.crossingEvents.length) * 100)
                          : 0}%
                      </div>
                      <p className="text-sm text-muted-foreground">Percentage of successful crossings</p>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg">Anomalies</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold">
                        {simulationData.crossingEvents.reduce((total, event) => total + event.anomalies.length, 0)}
                      </div>
                      <p className="text-sm text-muted-foreground">Detected anomalies during crossings</p>
                    </CardContent>
                  </Card>
                </div>
                
                <div className="space-y-2">
                  <h3 className="font-medium">Dimensional Integrity Over Time</h3>
                  <div className="h-64 border rounded-md p-4 flex items-center justify-center">
                    <p className="text-muted-foreground">Integrity visualization will appear here with more simulation data</p>
                  </div>
                  <p className="text-xs text-muted-foreground text-center">
                    Tracks how dimension integrity changes as entities cross boundaries
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Entity Performance</CardTitle>
                <CardDescription>
                  Analysis of how different entities perform when crossing boundaries
                </CardDescription>
              </CardHeader>
              <CardContent className="h-80 overflow-y-auto">
                <table className="w-full">
                  <thead>
                    <tr className="text-left border-b">
                      <th className="pb-2">Entity</th>
                      <th className="pb-2">Attempts</th>
                      <th className="pb-2">Success Rate</th>
                      <th className="pb-2">Avg. Impact</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    {simulationData.entities.map(entity => {
                      const entityEvents = simulationData.crossingEvents.filter(e => e.entityId === entity.id);
                      const successRate = entityEvents.length > 0 
                        ? (entityEvents.filter(e => e.success).length / entityEvents.length) * 100 
                        : 0;
                      const avgImpact = entityEvents.length > 0
                        ? entityEvents.reduce((sum, event) => sum + event.integrityImpact, 0) / entityEvents.length
                        : 0;
                        
                      return (
                        <tr 
                          key={entity.id} 
                          className="hover:bg-muted cursor-pointer"
                          onClick={() => setSelectedEntity(entity.id)}
                        >
                          <td className="py-2">
                            <div className="flex items-center space-x-2">
                              <div 
                                className="w-3 h-3 rounded-full" 
                                style={{ backgroundColor: entity.color }} 
                              />
                              <span>{entity.name}</span>
                            </div>
                          </td>
                          <td className="py-2">{entityEvents.length}</td>
                          <td className="py-2">
                            <div className="flex items-center space-x-2">
                              <div className="w-16 h-2 rounded-full bg-muted overflow-hidden">
                                <div 
                                  className="h-full rounded-full" 
                                  style={{ 
                                    width: `${Math.round(successRate)}%`,
                                    backgroundColor: successRate > 70 ? 'green' : successRate > 30 ? 'orange' : 'red'
                                  }}
                                />
                              </div>
                              <span className="text-xs">{Math.round(successRate)}%</span>
                            </div>
                          </td>
                          <td className="py-2">{avgImpact.toFixed(2)}</td>
                        </tr>
                      );
                    })}
                    
                    {simulationData.entities.length === 0 && (
                      <tr>
                        <td colSpan={4} className="py-4 text-center text-muted-foreground">
                          No entities to analyze yet
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>Boundary Analysis</CardTitle>
                <CardDescription>
                  Analysis of dimensional boundary permeability and crossing patterns
                </CardDescription>
              </CardHeader>
              <CardContent className="h-80 overflow-y-auto">
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium mb-2">Boundary Permeability</h3>
                    {simulationData.dimensions.slice(0, -1).map((fromDim, i) => {
                      const toDim = simulationData.dimensions[i + 1];
                      
                      // Calculate permeability between these two dimensions
                      const crossings = simulationData.crossingEvents.filter(e => 
                        (e.fromDimension === fromDim.id && e.toDimension === toDim.id) ||
                        (e.fromDimension === toDim.id && e.toDimension === fromDim.id)
                      );
                      
                      const successRate = crossings.length > 0 
                        ? (crossings.filter(e => e.success).length / crossings.length) * 100
                        : 0;
                        
                      return (
                        <div key={`${fromDim.id}-${toDim.id}`} className="mb-3 border rounded-md p-3">
                          <div className="flex justify-between items-center mb-2">
                            <div className="flex items-center">
                              <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: fromDim.color }} />
                              <span className="text-sm">{fromDim.name}</span>
                              <span className="mx-2">↔</span>
                              <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: toDim.color }} />
                              <span className="text-sm">{toDim.name}</span>
                            </div>
                            <span className="text-sm font-medium">{crossings.length} crossings</span>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <div className="w-full h-2 rounded-full bg-muted overflow-hidden">
                              <div 
                                className="h-full rounded-full" 
                                style={{ 
                                  width: `${Math.round(successRate)}%`,
                                  background: `linear-gradient(to right, ${fromDim.color}, ${toDim.color})`
                                }}
                              />
                            </div>
                            <span className="text-xs w-12">{Math.round(successRate)}% perm.</span>
                          </div>
                        </div>
                      );
                    })}
                    
                    {simulationData.dimensions.length < 2 && (
                      <p className="text-muted-foreground text-center">
                        Need at least two dimensions to analyze boundaries
                      </p>
                    )}
                  </div>
                  
                  <div>
                    <h3 className="font-medium mb-2">Anomaly Hotspots</h3>
                    {simulationData.crossingEvents.some(e => e.anomalies.length > 0) ? (
                      <div className="space-y-2">
                        {simulationData.dimensions.map(dim => {
                          // Count anomalies when this dimension is involved
                          const anomalies = simulationData.crossingEvents
                            .filter(e => e.fromDimension === dim.id || e.toDimension === dim.id)
                            .reduce((sum, event) => sum + event.anomalies.length, 0);
                            
                          if (anomalies === 0) return null;
                          
                          return (
                            <div key={dim.id} className="flex items-center space-x-2">
                              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: dim.color }} />
                              <span className="text-sm">{dim.name}:</span>
                              <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                                <div 
                                  className="h-full rounded-full bg-amber-500" 
                                  style={{ width: `${Math.min(100, anomalies * 5)}%` }}
                                />
                              </div>
                              <span className="text-xs">{anomalies} anomalies</span>
                            </div>
                          );
                        })}
                      </div>
                    ) : (
                      <p className="text-muted-foreground text-center">
                        No anomalies detected in crossings yet
                      </p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}