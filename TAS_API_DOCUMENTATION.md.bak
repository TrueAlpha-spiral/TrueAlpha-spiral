# TrueAlpha Spiral API Documentation

## Overview

The TrueAlpha Spiral (TAS) Enterprise AI Auditing Solution provides a robust REST API for interacting with the system. This document details all available API endpoints, request/response formats, and usage examples.

## Base URL

All API endpoints are relative to your deployment's base URL:

- Local development: `http://localhost:5000`
- Deployed version: Your application's domain

## Authentication

Authentication is not currently required for API access in this demonstration version. Production implementations should implement appropriate authentication and authorization mechanisms.

## Common Response Formats

All API responses follow a standard format:

```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

For errors:

```json
{
  "status": "error",
  "message": "Error description",
  "errorCode": "ERROR_CODE",
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

## API Endpoints

### Health and Status

#### GET /api/health

Checks the health status of the API server.

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2025-03-22T19:00:00.000Z",
  "environment": "development",
  "service": "Enterprise AI Auditing Solution"
}
```

#### GET /api/python-system/status

Checks the status of the Python API service.

**Response:**

```json
{
  "status": "running",
  "version": "1.0.0",
  "uptime": "2h 30m",
  "dependencies": ["numpy", "scikit-learn", "pandas"]
}
```

### Truth Patterns

#### GET /api/truth-patterns

Retrieves all available truth patterns.

**Response:**

```json
{
  "status": "success",
  "data": {
    "patterns": [
      {
        "id": 1,
        "name": "Implementation Claims",
        "description": "Detects claims about implementation details that may be speculative or fabricated.",
        "category": "Technical",
        "confidenceThreshold": 0.85,
        "isActive": true,
        "createdAt": "2025-03-22T19:00:00.000Z",
        "updatedAt": "2025-03-22T19:00:00.000Z"
      },
      // Additional patterns...
    ]
  },
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

#### GET /api/truth-patterns/:id

Retrieves a specific truth pattern by ID.

**Parameters:**
- `id` (path parameter): The ID of the truth pattern to retrieve

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Implementation Claims",
    "description": "Detects claims about implementation details that may be speculative or fabricated.",
    "category": "Technical",
    "confidenceThreshold": 0.85,
    "isActive": true,
    "createdAt": "2025-03-22T19:00:00.000Z",
    "updatedAt": "2025-03-22T19:00:00.000Z"
  },
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

#### POST /api/truth-patterns

Creates a new truth pattern.

**Request Body:**

```json
{
  "name": "Causal Confusion",
  "description": "Detects statements that confuse correlation with causation.",
  "category": "Logical",
  "confidenceThreshold": 0.8,
  "isActive": true
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 6,
    "name": "Causal Confusion",
    "description": "Detects statements that confuse correlation with causation.",
    "category": "Logical",
    "confidenceThreshold": 0.8,
    "isActive": true,
    "createdAt": "2025-03-22T19:00:00.000Z",
    "updatedAt": "2025-03-22T19:00:00.000Z"
  },
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

### Verification

#### POST /api/verify-text

Verifies text content against truth patterns.

**Request Body:**

```json
{
  "text": "Our AI model achieves 99.9% accuracy on all tasks and works perfectly every time.",
  "confidenceThreshold": 0.75,
  "includeHighlights": true
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "verificationId": 123,
    "text": "Our AI model achieves 99.9% accuracy on all tasks and works perfectly every time.",
    "truthScore": 0.45,
    "highlights": [
      {
        "startIndex": 13,
        "endIndex": 37,
        "highlightType": "exaggeration",
        "confidenceScore": 0.92,
        "patternId": 1,
        "message": "Unverifiable claim about implementation performance."
      }
    ],
    "summary": "The text contains potential exaggerations about AI model performance."
  },
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

### AI Auditing

#### POST /api/ai-audits

Creates a new AI system audit.

**Request Body:**

```json
{
  "clientName": "ACME Corporation",
  "aiSystemName": "ACME Customer Service AI",
  "regulatoryFramework": "EU-AI-Act",
  "systemData": {
    "modelType": "Large Language Model",
    "parametersCount": 7000000000,
    "trainingDataSources": ["Customer queries", "Knowledge base"],
    "deploymentContext": "Customer service chatbot"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "auditId": 456,
    "clientName": "ACME Corporation",
    "aiSystemName": "ACME Customer Service AI",
    "regulatoryFramework": "EU-AI-Act",
    "status": "initialized",
    "createdAt": "2025-03-22T19:00:00.000Z"
  },
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

#### GET /api/ai-audits/:id

Retrieves a specific AI audit by ID.

**Parameters:**
- `id` (path parameter): The ID of the AI audit to retrieve

**Response:**

```json
{
  "status": "success",
  "data": {
    "auditId": 456,
    "clientName": "ACME Corporation",
    "aiSystemName": "ACME Customer Service AI",
    "regulatoryFramework": "EU-AI-Act",
    "status": "completed",
    "riskScore": 0.35,
    "complianceScore": 0.82,
    "auditSummary": "The AI system meets most compliance requirements but has areas for improvement.",
    "recommendations": [
      "Improve documentation of data sources",
      "Implement more robust bias testing",
      "Add explainability features for high-risk decisions"
    ],
    "blockchainRecord": "0x1a2b3c4d5e6f...",
    "completedAt": "2025-03-22T20:00:00.000Z",
    "createdAt": "2025-03-22T19:00:00.000Z",
    "updatedAt": "2025-03-22T20:00:00.000Z"
  },
  "timestamp": "2025-03-22T20:30:00.000Z"
}
```

### Dimensional Boundary Simulation

#### GET /api/dimensional-boundary/status

Gets the current status of the dimensional boundary simulation.

**Response:**

```json
{
  "status": "running",
  "dimensions": 4,
  "entities": 8,
  "config": {
    "speed": 1.0,
    "boundaryStrength": 0.7,
    "allowMultipleCrossings": true,
    "dimensionalDecayRate": 0.05
  },
  "timestamp": "2025-03-22T19:00:00.000Z"
}
```

#### GET /api/dimensional-boundary/dimensions

Retrieves the dimensions configured in the simulation.

**Response:**

```json
{
  "dimensions": [
    {
      "id": "dim-1",
      "name": "Factual Domain",
      "description": "Domain of objective, verifiable facts and empirical data",
      "integrity": 0.95,
      "color": "#4285f4",
      "rules": ["Must be empirically verifiable", "Must have clear attribution"]
    },
    // Additional dimensions...
  ]
}
```

#### POST /api/dimensional-boundary/start

Starts a new dimensional boundary simulation.

**Request Body (optional):**

```json
{
  "config": {
    "speed": 1.5,
    "boundaryStrength": 0.5,
    "allowMultipleCrossings": false,
    "dimensionalDecayRate": 0.1
  },
  "dimensions": [
    // Custom dimensions if desired
  ]
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Simulation started",
  "simulationId": "sim-1234567890"
}
```

#### POST /api/dimensional-boundary/stop

Stops the current dimensional boundary simulation.

**Response:**

```json
{
  "status": "success",
  "message": "Simulation stopped"
}
```

#### GET /api/dimensional-boundary/simulation

Gets the full state of the current dimensional boundary simulation.

**Response:**

```json
{
  "id": "sim-1234567890",
  "status": "running",
  "dimensions": [
    // Dimension details
  ],
  "entities": [
    // Entity details
  ],
  "crossingEvents": [
    // Crossing event details
  ],
  "config": {
    // Configuration details
  },
  "startTime": "2025-03-22T19:00:00.000Z",
  "currentTime": "2025-03-22T19:05:00.000Z"
}
```

### Documentation

#### GET /api/documentation/:filename

Retrieves documentation content for specific system aspects.

**Parameters:**
- `filename` (path parameter): The documentation file to retrieve

**Response:**

Returns the content of the requested documentation file.

### Shadow Defense System

#### GET /api/shadow-defense/status

Retrieves the current status of the Shadow Defense System.

**Response:**

```json
{
  "status": "active",
  "systemStatus": {
    "overallIntegrity": 1,
    "driftDetectionRate": 0.5,
    "neutralizationSuccessRate": 1,
    "learningEfficiency": 0.01,
    "shieldStrength": 0.91,
    "securityScore": 0.783
  },
  "timestamp": "2025-03-22T21:01:45.166Z"
}
```

#### GET /api/shadow-defense/drift-history

Retrieves the history of detected content drifts.

**Response:**

```json
{
  "count": 1,
  "driftHistory": [
    {
      "detected": true,
      "score": 0.189,
      "pattern": {
        "id": "pat-iulJ1Db9dP",
        "content": "This is a test content that might have drift.",
        "source": "test",
        "timestamp": "2025-03-22T21:01:09.561Z"
      },
      "layer": "epsilon",
      "timestamp": "2025-03-22T21:01:09.561Z",
      "neutralizationSuccess": true,
      "recommendations": ["Continue normal monitoring operations"]
    }
  ]
}
```

#### GET /api/shadow-defense/security-events

Retrieves all logged security events.

**Response:**

```json
{
  "count": 2,
  "securityEvents": [
    {
      "id": 1,
      "eventType": "drift-detected",
      "timestamp": "2025-03-22T21:01:09.562Z",
      "data": {
        "patternId": "pat-iulJ1Db9dP",
        "layer": "epsilon",
        "driftScore": 0.189,
        "neutralizationSuccess": true
      },
      "systemStatus": {
        "overallIntegrity": 1,
        "driftDetectionRate": 0.5,
        "neutralizationSuccessRate": 1,
        "learningEfficiency": 0,
        "shieldStrength": 0.91,
        "securityScore": 0.782
      },
      "severity": "info",
      "processed": false
    }
  ]
}
```

#### GET /api/shadow-defense/security-events/:eventType

Retrieves security events of a specific type.

**Parameters:**
- `eventType` (path parameter): The type of security events to retrieve

**Response:**

```json
{
  "eventType": "unauthorized_access",
  "count": 1,
  "securityEvents": [
    {
      "id": 2,
      "eventType": "unauthorized_access",
      "timestamp": "2025-03-22T21:01:16.777Z",
      "data": {
        "ip": "192.168.1.1",
        "endpoint": "/admin"
      },
      "systemStatus": {
        "overallIntegrity": 1,
        "driftDetectionRate": 0.5,
        "neutralizationSuccessRate": 1,
        "learningEfficiency": 0,
        "shieldStrength": 0.91,
        "securityScore": 0.782
      },
      "severity": "high",
      "sourceIp": "192.168.1.1",
      "userId": 123,
      "sessionId": "sess_123456",
      "processed": false
    }
  ]
}
```

#### GET /api/shadow-defense/recommendations

Retrieves security recommendations based on system status and drift history.

**Response:**

```json
{
  "systemStatus": {
    "overallIntegrity": 1,
    "driftDetectionRate": 0.5,
    "neutralizationSuccessRate": 1,
    "learningEfficiency": 0.01,
    "shieldStrength": 0.91,
    "securityScore": 0.783
  },
  "driftBasedRecommendations": [
    {
      "recommendation": "Continue normal monitoring operations",
      "frequency": 1
    }
  ],
  "systemRecommendations": [
    {
      "recommendation": "Enhance pattern learning by providing more diverse training examples",
      "priority": "medium"
    }
  ],
  "timestamp": "2025-03-22T21:01:45.166Z"
}
```

#### POST /api/shadow-defense/detect-drift

Detects drift in the provided content.

**Request Body:**

```json
{
  "content": "Content to analyze for drift",
  "context": {
    "source": "application_name",
    "userId": 123
  }
}
```

**Response:**

```json
{
  "detected": true,
  "driftResult": {
    "detected": true,
    "score": 0.189,
    "pattern": {
      "id": "pat-iulJ1Db9dP",
      "content": "This is a test content that might have drift.",
      "source": "test",
      "timestamp": "2025-03-22T21:01:09.561Z"
    },
    "layer": "epsilon",
    "timestamp": "2025-03-22T21:01:09.561Z",
    "neutralizationSuccess": true,
    "recommendations": ["Continue normal monitoring operations"]
  }
}
```

#### POST /api/shadow-defense/log-event

Logs a new security event.

**Request Body:**

```json
{
  "eventType": "unauthorized_access",
  "data": {
    "ip": "192.168.1.1",
    "endpoint": "/admin"
  },
  "severity": "high",
  "sourceIp": "192.168.1.1",
  "userId": 123,
  "sessionId": "sess_123456"
}
```

**Response:**

```json
{
  "success": true,
  "event": {
    "id": 2,
    "eventType": "unauthorized_access",
    "timestamp": "2025-03-22T21:01:16.777Z",
    "data": {
      "ip": "192.168.1.1",
      "endpoint": "/admin"
    },
    "systemStatus": {
      "overallIntegrity": 1,
      "driftDetectionRate": 0.5,
      "neutralizationSuccessRate": 1,
      "learningEfficiency": 0,
      "shieldStrength": 0.91,
      "securityScore": 0.782
    },
    "severity": "high",
    "sourceIp": "192.168.1.1",
    "userId": 123,
    "sessionId": "sess_123456",
    "processed": false
  },
  "timestamp": "2025-03-22T21:01:16.777Z"
}
```

#### POST /api/shadow-defense/learn-pattern

Learns a new security pattern.

**Request Body:**

```json
{
  "pattern": "Secure pattern for API access",
  "layer": "gamma"
}
```

**Response:**

```json
{
  "success": true,
  "pattern": "Secure pattern for API access",
  "layer": "gamma",
  "timestamp": "2025-03-22T21:01:34.781Z"
}
```

## Error Codes

- `INVALID_REQUEST`: The request format is invalid
- `RESOURCE_NOT_FOUND`: The requested resource was not found
- `VALIDATION_ERROR`: Request validation failed
- `INTERNAL_ERROR`: An internal server error occurred
- `SERVICE_UNAVAILABLE`: A required service is unavailable

## Rate Limiting

The API currently does not implement rate limiting in the demonstration version. Production implementations should include appropriate rate limiting.

## Versioning

The current API version is v1. All endpoints should be considered as v1 endpoints.

## Support

For issues or questions about the API, please contact the system administrator.