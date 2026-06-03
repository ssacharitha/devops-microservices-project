# Incident 003A - ConfigMap Misconfiguration

## Impact

Application configuration was intentionally modified with an invalid database hostname.

Pods remained healthy and available from Kubernetes' perspective.

Potential impact was database-dependent functionality becoming unavailable.

## Symptoms

ConfigMap was modified:

DB_HOST: postgres

to:

DB_HOST: postgres-broken

Expected outcome:

Application startup failure and CrashLoopBackOff.

Actual outcome:

Pods remained Running and Ready.

## Detection

Updated ConfigMap:

kubectl edit configmap backend-config

Verified:

kubectl get configmap backend-config -o yaml

Observed:

DB_HOST=postgres-broken

## Investigation

### Step 1 - Verify Existing Pods

Observation:

Existing Pods remained Running.

Reason:

Environment variables are injected during container startup and are not automatically updated in running containers.

### Step 2 - Restart Deployment

Command:

kubectl rollout restart deployment flask-backend

Observation:

New ReplicaSet created.

New Pods started successfully.

No CrashLoopBackOff occurred.

### Step 3 - Verify Configuration Inside New Pods

Command:

kubectl exec -it <pod-name> -- printenv | findstr DB_HOST

Result:

DB_HOST=postgres-broken

Confirmed that new Pods received the modified ConfigMap value.

### Step 4 - Inspect Application Logs

Command:

kubectl logs <pod-name>

Observed:

Flask application started successfully.

Health check requests returned HTTP 200.

No database connection errors were present during startup.

### Step 5 - Verify Health Endpoint

Command:

curl http://devops.local/health

Response:

{"status":"ok","version":"v2"}

Health endpoint continued to report success.

## Root Cause

The Flask application does not validate database connectivity during startup.

The health endpoint only verifies application availability and does not verify database connectivity.

As a result:

* Pods started successfully.
* Readiness checks passed.
* Kubernetes marked Pods as healthy.

Even though the configured database host was invalid.

## Resolution

Restored ConfigMap:

DB_HOST: postgres

Restarted deployment to reload environment variables.

Verified application functionality.

## Key Learning

A successful Kubernetes health check does not guarantee that application dependencies are healthy.

Application health and dependency health are different concerns.

## Improvement Opportunities

Enhance the /health endpoint to validate database connectivity.

Example:

* Verify PostgreSQL is reachable.
* Execute a lightweight database query.
* Return HTTP 503 when dependencies are unavailable.

This would allow Kubernetes readiness probes to detect dependency failures more accurately.

## Commands Used

kubectl edit configmap backend-config

kubectl get configmap backend-config -o yaml

kubectl rollout restart deployment/flask-backend

kubectl get pods -w

kubectl logs <pod-name>

kubectl exec -it <pod-name> -- printenv | findstr DB_HOST

curl http://devops.local/health

## What I Expected

I expected the application to crash and enter CrashLoopBackOff because the database hostname was invalid.

## What Actually Happened

The application started normally and health checks passed.

The database dependency was not validated during startup.

## Why This Matters

This showed me that a healthy Kubernetes Pod does not always mean the application is fully functional.
