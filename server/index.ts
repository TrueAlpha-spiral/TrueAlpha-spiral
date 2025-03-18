import express, { type Request, Response, NextFunction } from "express";
import cors from "cors";
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { storage } from "./storage";

const app = express();
// Add storage to app.locals for access in routes
app.locals.storage = storage;

// Configure CORS
const replitDomain = process.env.REPLIT_DOMAINS ? 
  `https://${process.env.REPLIT_DOMAINS.split(',')[0]}` : 
  undefined;

// Allow all origins in development mode for maximum compatibility
// In production, we would tighten this up
app.use(cors({
  origin: process.env.NODE_ENV === 'development' ? 
    true : // Allow any origin in development mode
    [
      'http://localhost:5000',
      'http://localhost:3000',
      'http://localhost:443',
      'https://localhost:443',
      replitDomain || 'https://truealphaspiral.replit.app',
    ].filter(Boolean),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use((req, res, next) => {
  const start = Date.now();
  const path = req.path;
  let capturedJsonResponse: Record<string, any> | undefined = undefined;

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
    // In Replit, we'll use the port Replit expects for webview access
    let port = 443; // Default port for HTTPS access
    
    // Check environment variables in order of precedence
    if (process.env.PORT) {
      port = parseInt(process.env.PORT);
      log(`Using PORT environment variable: ${port}`);
    } else if (process.env.REPL_ID && process.env.REPLIT_CLUSTER) {
      // For Replit environment
      port = 5000; // This is the recommended port for Replit's webview
      log(`Using Replit-specific port for webview access: ${port}`);
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
      res.status(200).send('OK - TrueAlphaSpiral system is running');
    });
    
    // Root API endpoint for Replit compatibility testing
    app.get('/api', (_req, res) => {
      res.setHeader('Content-Type', 'application/json');
      res.send(JSON.stringify({ 
        message: 'TrueAlphaSpiral API is running',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV,
        replitDomain,
        service: 'KPMG AI Auditing Solution'
      }));
    });
    
    server.listen({
      port,
      host: "0.0.0.0",
      reusePort: true,
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
    }).on('error', (error) => {
      log(`Error starting server: ${error.message}`, 'error');
    });
  } catch (error) {
    log(`Uncaught error during startup: ${error instanceof Error ? error.message : String(error)}`, 'error');
    console.error('Startup error details:', error);
  }
})();
