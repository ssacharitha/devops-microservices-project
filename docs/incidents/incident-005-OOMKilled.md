## Impact

Container repeatedly exceeded its configured memory limit and was terminated by the Linux OOM (Out Of Memory) Killer.

Application became unstable and entered a restart loop.

---

## Symptoms

Observed:

```bash
kubectl get pods
```

Output:

```text
memory-hog   0/1   CrashLoopBackOff
```

Restart count continued increasing.

---

## Investigation

### Step 1 - Verify Pod Status

Command:

```bash
kubectl get pods
```

Observation:

```text
memory-hog   0/1   CrashLoopBackOff
```

The container was repeatedly failing and being restarted by Kubernetes.

---

### Step 2 - Inspect Pod Details

Command:

```bash
kubectl describe pod memory-hog
```

Output:

```text
State:
  Waiting
  Reason: CrashLoopBackOff

Last State:
  Terminated
  Reason: OOMKilled
```

This provided direct evidence that the previous container instance was terminated because it exceeded its memory limit.

---

### Step 3 - Review Events

Events:

```text
Warning  BackOff
Back-off restarting failed container memory-hog
```

Observation:

Kubernetes was repeatedly attempting to restart the container after each failure.

---

## Root Cause

A test workload continuously allocated memory:

```python
data = []

while True:
    data.append("A" * 1024 * 1024)
```

The container was configured with a memory limit:

```yaml
resources:
  limits:
    memory: "50Mi"
```

The application consumed more than 50 MiB of memory.

When the memory limit was exceeded:

```text
Linux OOM Killer
↓
Container Process Terminated
↓
Exit
↓
Kubernetes Restart
```

This cycle repeated continuously.

---

## Resolution

Removed the test pod:

```bash
kubectl delete pod memory-hog
```

Alternative production resolutions:

* Increase memory limits.
* Reduce application memory consumption.
* Fix memory leaks.
* Optimize application workload.

---

## Verification

Command:

```bash
kubectl get pods
```

Result:

```text
memory-hog pod removed
```

Cluster returned to a healthy state.

---

## Lessons Learned

Kubernetes resource configuration consists of:

### Requests

```yaml
requests:
  memory: 25Mi
```

Requests determine scheduling requirements.

The Kubernetes scheduler uses requests to decide whether a node has sufficient resources to host a pod.

### Limits

```yaml
limits:
  memory: 50Mi
```

Limits define the maximum amount of memory a container may consume.

If a container exceeds its memory limit:

```text
Linux OOM Killer terminates the process
```

---

## Key Observation

CrashLoopBackOff is a symptom.

OOMKilled is the root cause.

Example:

```text
Current State:
CrashLoopBackOff

Last State:
OOMKilled
```

The most important troubleshooting clue was:

```text
Last State:
Reason: OOMKilled
```

---

## Commands Used

```bash
kubectl apply -f memory-hog.yaml

kubectl get pods

kubectl describe pod memory-hog

kubectl delete pod memory-hog
```