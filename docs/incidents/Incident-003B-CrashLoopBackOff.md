# Incident 003B - CrashLoopBackOff Due to Invalid Startup Command

## Date

2026-06-04

## Severity

Medium (Intentional Lab Failure)

## Impact

Application pods became unavailable after deployment configuration was modified with an invalid startup command.

New pods failed to start and entered CrashLoopBackOff state.

## Symptoms

Observed:

```bash
kubectl get pods
```

Output:

```text
0/1 CrashLoopBackOff
```

Application was unavailable on newly created pods.

## Investigation

### Step 1 - Verify Pod Status

Command:

```bash
kubectl get pods
```

Observation:

```text
flask-backend-7944f78dd6-hlb7k   0/1   CrashLoopBackOff
```

Pod was repeatedly restarting.

---

### Step 2 - Inspect Application Logs

Command:

```bash
kubectl logs flask-backend-7944f78dd6-hlb7k
```

Output:

```text
python: can't open file '/app/nonexistent.py': [Errno 2] No such file or directory
```

This immediately identified the root cause.

---

### Step 3 - Inspect Pod Events

Command:

```bash
kubectl describe pod flask-backend-7944f78dd6-hlb7k
```

Events:

```text
Successfully pulled image
Created container
Started container
Back-off restarting failed container
```

Observation:

Events confirmed repeated restart attempts but did not provide the application-level error.

---

### Step 4 - Compare Logs vs Events

Logs provided:

```text
Exact application failure
```

Events provided:

```text
Container lifecycle information
```

Logs were the fastest path to root cause identification.

## Root Cause

Deployment startup command was intentionally modified:

```yaml
command:
- python
- nonexistent.py
```

Container startup process attempted to execute:

```bash
python nonexistent.py
```

The file did not exist inside the container image.

Python exited immediately with:

```text
No such file or directory
```

Kubernetes detected container failure and continuously restarted it.

## Resolution

Removed invalid startup command.

Rolled back deployment:

```bash
kubectl rollout undo deployment/flask-backend
```

## Verification

Commands:

```bash
kubectl rollout status deployment/flask-backend
kubectl get pods
kubectl get rs
```

Results:

* Previous healthy ReplicaSet became active.
* Broken ReplicaSet scaled down.
* Application pods returned to Running state.

## Key Learning

CrashLoopBackOff indicates that the container starts but the application process exits repeatedly.

For CrashLoopBackOff investigations:

1. Check pod status.
2. Inspect application logs.
3. Inspect previous logs if required.
4. Review pod events.
5. Identify startup failure.
6. Correct configuration or application issue.

## Commands Used

```bash
kubectl get pods

kubectl logs flask-backend-7944f78dd6-hlb7k

kubectl describe pod flask-backend-7944f78dd6-hlb7k

kubectl rollout undo deployment/flask-backend

kubectl rollout status deployment/flask-backend

kubectl get rs
```