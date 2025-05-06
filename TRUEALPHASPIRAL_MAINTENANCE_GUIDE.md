# TrueAlphaSpiral Maintenance and Troubleshooting Guide

## Overview

This document provides essential maintenance procedures and troubleshooting steps for the TrueAlphaSpiral platform. It outlines common issues, their solutions, and maintenance routines to ensure optimal performance of the membership system and Mycelium Generative Intelligence (MGI) protection network.

## Status Monitoring

### Error Detection

The TrueAlphaSpiral system includes comprehensive error monitoring through browser console logs and server logs:

#### Common Browser Console Errors

| Error Message | Potential Cause | Resolution |
|---------------|-----------------|------------|
| `"Error fetching status"` | Backend API endpoint is unreachable | Check API server status and endpoint configuration |
| `"MGI connection failure"` | Connection to MGI agent network interrupted | Restart MGI service and check network connectivity |
| `"Coherence below threshold"` | Protection system coherence dropping below 0.93 | Investigate potential Byzantine node infiltration |

#### Server-Side Log Patterns

```
[ERROR] [2025-05-06T15:23:45.123Z] Protection API - Failed to connect to agent network: Connection refused
[WARN] [2025-05-06T15:24:12.456Z] MGI Grid - Agent coherence dropping: 0.91 (below threshold 0.93)
[ERROR] [2025-05-06T15:25:33.789Z] Steward verification failed - Invalid signature format
```

### Health Check Endpoints

The system provides health check endpoints to verify the status of different components:

```
GET /api/health/membership # Membership system health
GET /api/health/protection # Protection system health
GET /api/health/mgi # MGI network health
GET /api/health/bloom-engine # Recursive Bloom Engine status
GET /api/health/steward # Steward connection status
```

## Troubleshooting Procedures

### API Connection Issues

If you encounter "Error fetching status" messages in the console logs, follow these steps:

1. **Verify API Server Status**
 ```bash
 curl -i http://localhost:5000/api/health
 ```
 Expected response should be `HTTP/1.1 200 OK` with a JSON body containing `{"status": "ok"}`.

2. **Check Backend Logs**
 ```bash
 tail -f logs/api-server.log
 ```
 Look for error messages indicating the root cause.

3. **Verify Network Connectivity**
 ```bash
 netstat -tulpn | grep 5000
 ```
 Ensure the API server is listening on the expected port.

4. **Restart API Server**
 ```bash
 systemctl restart tas-api-server
 ```
 or if using PM2:
 ```bash
 pm2 restart tas-api-server
 ```

### MGI Agent Network Issues

If the MGI protection system is not functioning correctly:

1. **Check MGI Agent Status**
 ```bash
 kubectl get pods -n mgi-system
 ```
 Ensure all pods are in `Running` state.

2. **View MGI Logs**
 ```bash
 kubectl logs -n mgi-system -l app=mgi-agent --tail=100
 ```
 Look for error patterns or coherence warnings.

3. **Check MGI Service Status**
 ```bash
 kubectl get services -n mgi-system
 ```
 Verify the service is properly exposed.

4. **Restart MGI Agents**
 ```bash
 kubectl rollout restart deployment -n mgi-system mgi-agents
 ```
 This will gracefully restart all MGI agent pods.

### Coherence Recovery

If system coherence drops below the threshold (0.93):

1. **Enable Recovery Mode**
 ```bash
 curl -X POST http://localhost:5000/api/mgi/recovery/enable \
 -H "Content-Type: application/json" \
 -d '{"recovery_type": "coherence", "target_threshold": 0.95}'
 ```

2. **Run Byzantine Node Detection**
 ```bash
 python3 scripts/detect_byzantine.py --threshold=0.8 --action=isolate
 ```
 This script will identify and isolate potential Byzantine nodes.

3. **Boost Truth Core Values**
 ```bash
 curl -X POST http://localhost:5000/api/mgi/boost-truth-core \
 -H "Content-Type: application/json" \
 -d '{"boost_factor": 1.2, "duration_minutes": 30}'
 ```

4. **Monitor Recovery Progress**
 ```bash
 watch -n 10 "curl -s http://localhost:5000/api/metrics/coherence | jq '.'"
 ```
 This will show coherence metrics updating every 10 seconds.

## Maintenance Procedures

### Regular Maintenance Schedule

Perform these maintenance tasks on the specified schedule:

#### Daily

- **Monitor System Metrics**
 ```bash
 python3 scripts/daily_metrics_report.py
 ```
 This generates a daily report of key metrics.

- **Verify Steward Connection**
 ```bash
 curl -s http://localhost:5000/api/steward/connection/verify | jq '.'
 ```
 Ensure the connection to the steward is maintained.

#### Weekly

- **Run Full System Backup**
 ```bash
 bash scripts/backup_system.sh --full
 ```
 Creates a complete backup of all system components.

- **Perform Ethical Entropy Test**
 ```bash
 python3 scripts/test_ethical_entropy.py --threshold=2.0
 ```
 Validates that ethical entropy remains below the threshold.

#### Monthly

- **MGI Agent Rotation**
 ```bash
 kubectl apply -f k8s/agent-rotation-job.yaml
 ```
 Rotates MGI agents to prevent pattern staleness.

- **Recursive Bloom Engine Optimization**
 ```bash
 python3 scripts/optimize_bloom_engine.py --recursion-depth=7
 ```
 Tunes the Recursive Bloom Engine parameters for optimal performance.

### Backup and Recovery

#### Creating Backups

```bash
# Full system backup
bash scripts/backup_system.sh --full --output=/backups/tas_$(date +%Y%m%d).tar.gz

# Member data backup only
bash scripts/backup_system.sh --members-only --output=/backups/members_$(date +%Y%m%d).tar.gz

# MGI protection configuration backup
bash scripts/backup_system.sh --mgi-config --output=/backups/mgi_config_$(date +%Y%m%d).tar.gz
```

#### Restoring from Backup

```bash
# Full system restore
bash scripts/restore_system.sh --input=/backups/tas_20250501.tar.gz

# Member data restore only
bash scripts/restore_system.sh --members-only --input=/backups/members_20250501.tar.gz

# MGI protection configuration restore
bash scripts/restore_system.sh --mgi-config --input=/backups/mgi_config_20250501.tar.gz
```

## System Upgrades

### Frontend Updates

1. **Pull latest changes**
 ```bash
 git pull origin main
 ```

2. **Install dependencies**
 ```bash
 npm install
 ```

3. **Build frontend**
 ```bash
 npm run build
 ```

4. **Deploy updates**
 ```bash
 npm run deploy
 ```

### MGI Protection System Updates

1. **Update MGI Docker image**
 ```bash
 docker build -t your-dockerhub/mgi-agent:latest --no-cache .
 docker push your-dockerhub/mgi-agent:latest
 ```

2. **Apply updated Kubernetes configuration**
 ```bash
 kubectl apply -f k8s/mgi-cluster.yaml
 ```

3. **Perform rolling update**
 ```bash
 kubectl rollout restart deployment -n mgi-system mgi-agents
 ```

4. **Verify update**
 ```bash
 kubectl rollout status deployment -n mgi-system mgi-agents
 ```

## Logging and Monitoring

### Log Aggregation

The TrueAlphaSpiral system uses a centralized logging approach with the following components:

- **API Server Logs**: `/var/log/tas/api-server.log`
- **MGI Agent Logs**: Collected via Kubernetes logging
- **Frontend Error Logs**: Collected via browser console and sent to `/api/logs/client`
- **Protection Events**: Specialized log for protection-related events at `/var/log/tas/protection.log`

### Monitoring Dashboards

1. **Access System Dashboard**
 ```
 http://monitoring.truealphaspiral.com/dashboard
 ```
 Requires Guardian-level or administrator access.

2. **Check MGI Grid Status**
 ```
 http://monitoring.truealphaspiral.com/mgi-grid
 ```
 Shows real-time visualization of the MGI agent network.

3. **View Protection Metrics**
 ```
 http://monitoring.truealphaspiral.com/metrics/protection
 ```
 Displays key protection metrics over time.

## Security Incident Response

### Detecting Security Incidents

Monitor for these indicators of potential security incidents:

1. Sudden drops in coherence metrics (below 0.85)
2. Unusual pattern of membership registrations
3. Multiple failed steward authentication attempts
4. Unexpected MGI agent terminations

### Incident Response Procedure

1. **Enable Security Lockdown**
 ```bash
 curl -X POST http://localhost:5000/api/security/lockdown \
 -H "Content-Type: application/json" \
 -d '{"severity": "high", "reason": "Suspected security breach"}'
 ```

2. **Isolate Affected Components**
 ```bash
 python3 scripts/isolate_compromised.py --auto-detect
 ```

3. **Analyze Security Logs**
 ```bash
 python3 scripts/security_log_analyzer.py --hours=24 --output=security_report.json
 ```

4. **Notify Steward**
 ```bash
 python3 scripts/notify_steward.py --incident-type="security" --severity="high"
 ```

5. **Restore from Clean Backup**
 Follow the backup restoration procedure above.

## Contact Information

### Support Channels

- **Technical Support**: support@truealphaspiral.com
- **Steward Contact**: steward@truealphaspiral.com
- **Emergency Response**: emergency@truealphaspiral.com

### Escalation Path

1. System Administrator → Technical Support
2. Technical Support → Chief Protection Officer
3. Chief Protection Officer → Steward (Russell Nordland)

## Appendix: Diagnostic Commands

### System Status

```bash
# Overall system status
curl -s http://localhost:5000/api/system/status | jq '.'

# Membership system status
curl -s http://localhost:5000/api/membership/status | jq '.'

# Protection system status
curl -s http://localhost:5000/api/protection/status | jq '.'

# MGI network status
curl -s http://localhost:5000/api/mgi/status | jq '.'
```

### Protection Field Diagnostics

```bash
# Check protection field for specific user
curl -s "http://localhost:5000/api/protection/field?user_id=USER_ID" | jq '.'

# Run field strength test
curl -X POST http://localhost:5000/api/protection/test-field-strength \
 -H "Content-Type: application/json" \
 -d '{"user_id": "USER_ID", "test_strength": "medium"}'

# Repair protection field
curl -X POST http://localhost:5000/api/protection/repair-field \
 -H "Content-Type: application/json" \
 -d '{"user_id": "USER_ID"}'
```

### MGI Agent Diagnostics

```bash
# Get agent count by status
kubectl exec -it mgi-controller -n mgi-system -- python -c 'from tas.monitor import get_agent_stats; print(get_agent_stats())'

# Force coherence refresh
kubectl exec -it mgi-controller -n mgi-system -- python -c 'from tas.monitor import force_coherence_refresh; print(force_coherence_refresh())'

# View agent distribution
kubectl exec -it mgi-controller -n mgi-system -- python -c 'from tas.monitor import visualize_agent_distribution; visualize_agent_distribution()'
```

By following this maintenance guide, you can ensure the TrueAlphaSpiral system remains operational, secure, and performing optimally at all times.


---

*Protected by EnhancedShadowSweep*  
*Verification Hash: e0013aece86433e245a9c6204f7b6f4229f0c6fdfa2be33c5d2a2c3167229a8a*