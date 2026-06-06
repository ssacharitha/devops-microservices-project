# Incident-004-Readiness-Probe-Failure.md

## Impact

New application pods were deployed successfully but never became Ready.

Traffic continued flowing only to the previous healthy ReplicaSet.

Deployment rollout eventually exceeded its progress deadline.

---

## Symptoms

Observed:

```bash
kubectl get pods
```

Output:

```text
flask-backend-7cc94f599c-bsk64   0/1   Running
```

Pod status:

```text
STATUS = Running
READY  = 0/1
```

Application container was running, but Kubernetes refused to mark the pod as Ready.

Deployment rollout failed:

```bash
kubectl rollout status deployment/flask-backend
```

Output:

```text
error: deployment "flask-backend" exceeded its progress deadline
```

---

## Investigation

### Step 1 - Verify Pod Status

Command:

```bash
kubectl get pods
```

Observation:

```text
0/1 Running
```

Unlike CrashLoopBackOff, the container was not restarting.

This indicated an application availability or probe issue.

---

### Step 2 - Inspect Pod Events

Command:

```bash
kubectl describe pod flask-backend-7cc94f599c-bsk64
```

Events:

```text
Warning  Unhealthy

Readiness probe failed:
HTTP probe failed with statuscode: 404
```

This immediately pointed to a readiness probe configuration problem.

---

### Step 3 - Verify Service Endpoints

Command:

```bash
kubectl get endpoints flask-backend
```

Output:

```text
10.244.0.3:5000
10.244.0.9:5000
```

Observation:

Endpoints still existed because older healthy pods were still serving traffic.

---

### Step 4 - Review Deployment Configuration

Configured readiness probe:

```yaml
readinessProbe:
  httpGet:
    path: /health-broken
    port: 5000
```

Application only exposed:

```python
@app.route("/health")
```

Requests to:

```text
/health-broken
```

returned:

```text
404 Not Found
```

causing readiness failures.

---

## Root Cause

Readiness probe path was incorrectly configured.

Configured path:

```yaml
path: /health-broken
```

Actual application endpoint:

```yaml
path: /health
```

Because the readiness probe continuously received HTTP 404 responses, Kubernetes never marked the pod as Ready.

---

## Resolution

Restored the readiness probe path:

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 5000
```

Applied deployment changes.

---

## Verification

Commands:

```bash
kubectl rollout status deployment/flask-backend

kubectl get pods

kubectl get endpoints flask-backend
```

Expected Results:

```text
READY   STATUS
1/1     Running
```

Deployment rollout completed successfully.

Service endpoints were restored.

---

## Lessons Learned

A pod can be:

```text
Running
```

but still:

```text
Not Ready
```

Readiness probes control:

```text
Traffic Routing
```

not:

```text
Container Restarts
```

If readiness fails:

```text
Pod remains running
Pod removed from Service endpoints
Traffic is not sent to the pod
```

If liveness fails:

```text
Container is restarted
```

---

## Commands Used

```bash
kubectl get pods

kubectl describe pod flask-backend-7cc94f599c-bsk64

kubectl get endpoints flask-backend

kubectl rollout status deployment/flask-backend
```