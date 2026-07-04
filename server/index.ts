import express, { type Request, Response, NextFunction } from "express";
import cors from "cors";
import path from "path";
import fs from "fs";
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { storage } from "./storage";
import { spawn } from "child_process";
import { existsSync } from "fs";

// Import analytics functions
import { analyzeConceptDrift, generateIntegrityReport, getEntityMetrics } from './services/cross-dimensional-analytics';

const app = express();
// Add storage to app.locals for access in routes
app.locals.storage = storage;

// Configure CORS for maximum Replit compatibility
// Enable CORS for all origins in development and Replit environments
// Configure CORS with specific origin handling for Replit
app.use(cors({
  origin: function(origin, callback) {
    // Allow requests with no origin (like mobile apps, curl, or Postman)
    if(!origin) return callback(null, true);
    
    // Allow all origins in development 
    if (process.env.NODE_ENV === 'development') {
      return callback(null, true);
    }
    
    // Handle Replit domains
    if (process.env.REPLIT_DOMAINS) {
      const replitDomains = process.env.REPLIT_DOMAINS.split(',').map(domain => `https://${domain.trim()}`);
      if (origin && replitDomains.indexOf(origin) !== -1) {
        return callback(null, true);
      }
    }
    
    // Default allow for safety
    callback(null, true);
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'Accept', 'Cache-Control', 'X-Requested-With']
}));

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use((req, res, next) => {
  const start = Date.now();
  const path = req.path;
  let capturedJsonResponse: Record<string, any> | undefined = undefined;

  // Check for special path that needs JSON
  if (path === '/api/dimensional-simulation') {
    req.headers['accept'] = 'application/json';
    res.setHeader('Content-Type', 'application/json');
  }

  const originalResJson = res.json;
  res.json = function (bodyJson, ...args) {
    capturedJsonResponse = bodyJson;
    return originalResJson.apply(res, [bodyJson, ...args]);
  };

  res.on("finish", () => {
    const duration = Date.now() - start;
    if (path.startsWith("/api")) {
      let logLine = `${req.method} ${path} ${res.statusCode} in ${duration}ms`;
      if (capturedJsonResponse) {
        logLine += ` :: ${JSON.stringify(capturedJsonResponse)}`;
      }

      if (logLine.length > 80) {
        logLine = logLine.slice(0, 79) + "…";
      }

      log(logLine);
    }
  });

  next();
});

(async () => {
  try {
    log("Starting server initialization...");
    const server = await registerRoutes(app);
    log("Routes registered successfully");

    app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
      const status = err.status || err.statusCode || 500;
      const message = err.message || "Internal Server Error";

      res.status(status).json({ message });
      // Log the error instead of throwing it
      console.error('Server error:', err);
    });

    // Special routes for direct API access
    // Add explicit API JSON endpoints before Vite middleware
    app.get('/api/dimensional-boundary/status', (req, res) => {
      // Forward this specifically to our API handler with explicit JSON header
      req.headers['accept'] = 'application/json';
      res.setHeader('Content-Type', 'application/json');
      
      // Create direct API response to bypass Vite middleware
      const simulationStatus = storage.getDimensionalBoundaryStatus();
      res.json(simulationStatus || { 
        status: "idle", 
        message: "Dimensional boundary simulation not running" 
      });
    });
    
    // Add additional explicit API endpoints here
    // Add endpoint for legacy /api/dimensional-simulation to ensure it returns JSON
    app.get('/api/dimensional-simulation', (req, res) => {
      // Force JSON content type and bypass Vite
      res.setHeader('Content-Type', 'application/json');
      res.removeHeader('X-Powered-By');
      
      const simulation = storage.getDimensionalBoundarySimulation();
      if (!simulation) {
        // Return plain JSON to avoid Vite processing
        return res.end(JSON.stringify({ 
          status: 'error', 
          message: 'No simulation running' 
        }));
      }
      // Use end with stringified JSON to bypass Vite
      res.end(JSON.stringify(simulation));
    });
    
    app.get('/api/dimensional-boundary/dimensions', (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      const dimensions = storage.getDimensionalBoundarySimulation()?.dimensions || [];
      res.json({ dimensions });
    });
    
    // Start dimensional boundary simulation
    app.post('/api/dimensional-boundary/start', (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      const config = req.body?.config || {};
      const simulation = storage.startDimensionalBoundarySimulation(config);
      res.json({ 
        status: 'success', 
        message: 'Simulation started',
        simulationId: simulation.id
      });
    });
    
    // Stop dimensional boundary simulation
    app.post('/api/dimensional-boundary/stop', (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      storage.stopDimensionalBoundarySimulation();
      res.json({ 
        status: 'success', 
        message: 'Simulation stopped' 
      });
    });
    
    // Get full simulation state
    app.get('/api/dimensional-boundary/simulation', (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      const simulation = storage.getDimensionalBoundarySimulation();
      if (!simulation) {
        return res.json({ 
          status: 'error', 
          message: 'No simulation running' 
        });
      }
      res.json(simulation);
    });
    
    // Use direct imports of analytics functions
    
    // Cross-dimensional analytics endpoints
    app.get('/api/dimensional-boundary/integrity-report', (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      const report = generateIntegrityReport();
      res.json(report);
    });
    
    app.get('/api/dimensional-boundary/entity-metrics', (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      const metrics = getEntityMetrics();
      res.json(metrics);
    });
    
    app.post('/api/dimensional-boundary/analyze-drift', (req, res) => {
      res.setHeader('Content-Type', 'application/json');
      const { conceptId, sourceDimension, targetDimension } = req.body || {};
      
      // Validate required parameters
      if (!conceptId || !sourceDimension || !targetDimension) {
        return res.status(400).json({
          status: 'error',
          message: 'Missing required parameters: conceptId, sourceDimension, targetDimension',
          timestamp: new Date().toISOString()
        });
      }
      
      const analysis = analyzeConceptDrift(conceptId, sourceDimension, targetDimension);
      res.json(analysis);
    });
    
    log("Setting up Vite or static files...");
    // importantly only setup vite in development and after
    // setting up all the other routes so the catch-all route
    // doesn't interfere with the other routes
    if (app.get("env") === "development") {
      log("Setting up Vite for development...");
      await setupVite(app, server);
      log("Vite setup complete");
    } else {
      log("Setting up static file serving...");
      serveStatic(app);
      log("Static file serving setup complete");
    }

    // Special configuration for Replit environment
    // In Replit, we'll use port 5000 as that's what the workflow expects
    let port = 5000; // Use port 5000 to match workflow configuration
    
    // Check environment variables in order of precedence
    if (process.env.PORT) {
      port = parseInt(process.env.PORT);
      log(`Using PORT environment variable: ${port}`);
    } else if (process.env.REPL_ID && process.env.REPLIT_CLUSTER) {
      // For Replit environment
      port = 5000; // Use port 5000 to match workflow configuration
      log(`Using port 5000 to match workflow configuration`);
    }
    
    // Log port decision
    log(`Selected port: ${port}`);
    log("Attempting to start server on port " + port);
    
    // Log environment info
    log(`NODE_ENV: ${process.env.NODE_ENV}`);
    log(`REPL_ID: ${process.env.REPL_ID}`);
    log(`REPL_SLUG: ${process.env.REPL_SLUG}`);
    log(`REPLIT_CLUSTER: ${process.env.REPLIT_CLUSTER}`);
    log(`REPLIT_DOMAINS: ${process.env.REPLIT_DOMAINS}`);
    
    // Add simple healthcheck routes
    app.get('/health', (_req, res) => {
      res.status(200).send('OK - TrueAlphaSpiral Enterprise AI Auditing Solution is running');
    });
    
    // Root API endpoint for Replit compatibility testing
    app.get('/api', (_req, res) => {
      res.setHeader('Content-Type', 'application/json');
      const primaryReplitDomain = process.env.REPLIT_DOMAINS ? 
        `https://${process.env.REPLIT_DOMAINS.split(',')[0]}` : undefined;
        
      res.send(JSON.stringify({ 
        message: 'TrueAlphaSpiral API is running',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV,
        replitDomain: primaryReplitDomain,
        service: 'TrueAlphaSpiral Enterprise AI Auditing Solution'
      }));
    });
    
    // Add a simple test endpoint at the root to bypass Vite middleware
    app.get('/test', (_req, res) => {
      res.send(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>TrueAlphaSpiral Enterprise AI Auditing Solution Test</title>
        </head>
        <body>
          <h1>TrueAlphaSpiral Enterprise AI Auditing Solution Test Page</h1>
          <p>Server is working! Generated at: ${new Date().toISOString()}</p>
          <p>Environment: ${process.env.NODE_ENV || 'development'}</p>
          <p>Replit Domain: ${process.env.REPLIT_DOMAINS || 'Not running on Replit'}</p>
        </body>
        </html>
      `);
    });
    
    // Explicit root route handler before Vite takes over
    app.get('/', (_req, res, next) => {
      // In development, let Vite handle this through its middleware
      if (app.get("env") === "development") {
        return next();
      }
      
      // In production, serve the static index.html
      const indexPath = path.resolve(__dirname, "public", "index.html");
      if (fs.existsSync(indexPath)) {
        return res.sendFile(indexPath);
      }
      
      // Fallback if index.html doesn't exist
      res.send(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>TrueAlphaSpiral Enterprise AI Auditing Solution</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 40px; color: #333; }
            h1 { color: #6e44ff; }
            .container { max-width: 800px; margin: 0 auto; }
          </style>
        </head>
        <body>
          <div class="container">
            <h1>TrueAlphaSpiral Enterprise AI Auditing Solution</h1>
            <p>Welcome to the TrueAlphaSpiral Enterprise AI Auditing Solution.</p>
            <p>The system is running in ${process.env.NODE_ENV || 'development'} mode.</p>
            <p>Current time: ${new Date().toISOString()}</p>
            <p>To test the API, try <a href="/api/health">/api/health</a></p>
          </div>
        </body>
        </html>
      `);
    });
    
    server.listen({
      port,
      host: "0.0.0.0",
    }, () => {
      const serverAddress = server.address();
      const addressInfo = typeof serverAddress === 'object' && serverAddress 
        ? `${serverAddress.address}:${serverAddress.port}` 
        : String(serverAddress);
      
      log(`Server now listening on ${addressInfo}`);
      
      // Log both localhost and Replit domain URLs
      log(`Server accessible at http://localhost:${port}`);
      if (process.env.REPLIT_DOMAINS) {
        const replitDomain = `https://${process.env.REPLIT_DOMAINS.split(',')[0]}`;
        log(`Server accessible at ${replitDomain}`);
      }
      
      // ============================================================
      // PERMANENT INTEGRATION: Start Python API Watchdog
      // ============================================================
      if (existsSync('./python_api_watchdog.py')) {
        log('Starting Python API Watchdog (PERMANENT SOLUTION)');
        const pythonWatchdog = spawn('python', ['python_api_watchdog.py'], {
          stdio: 'ignore',
          detached: true
        });
        
        // Set up process event handlers
        pythonWatchdog.on('error', (err) => {
          console.error('Failed to start Python API Watchdog:', err);
        });
        
        log(`Python API Watchdog started with PID ${pythonWatchdog.pid}`);
        process.env.PYTHON_API_URL = 'http://localhost:8001';
        
        // Unref to allow the process to run independently of the parent
        pythonWatchdog.unref();
      } else {
        log('Python API Watchdog script not found - unable to ensure permanent Python API connection');
      }
    }).on('error', (error) => {
      log(`Error starting server: ${error.message}`, 'error');
    });
  } catch (error) {
    log(`Uncaught error during startup: ${error instanceof Error ? error.message : String(error)}`, 'error');
    console.error('Startup error details:', error);
  }
})();
