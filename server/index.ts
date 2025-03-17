import express, { type Request, Response, NextFunction } from "express";
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { storage } from "./storage";

const app = express();
// Add storage to app.locals for access in routes
app.locals.storage = storage;
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

    // ALWAYS serve the app on port 5000
    // this serves both the API and the client.
    // It is the only port that is not firewalled.
    const port = 5000;
    log("Attempting to start server on port " + port);
    
    // Log environment info
    log(`NODE_ENV: ${process.env.NODE_ENV}`);
    log(`REPL_ID: ${process.env.REPL_ID}`);
    log(`REPL_SLUG: ${process.env.REPL_SLUG}`);
    log(`REPLIT_CLUSTER: ${process.env.REPLIT_CLUSTER}`);
    log(`REPLIT_DOMAINS: ${process.env.REPLIT_DOMAINS}`);
    
    // Add a simple healthcheck route
    app.get('/health', (_req, res) => {
      res.status(200).send('OK - TrueAlphaSpiral system is running');
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
