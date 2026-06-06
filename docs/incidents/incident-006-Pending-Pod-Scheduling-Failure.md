# Incident-006-Pending-Pod-Scheduling-Failure

## Impact

A newly created pod remained in the Pending state and never started.

No container was created, no image was pulled, and the application never ran.

---

## Symptoms

Observed:

```bash
kubectl get pods
```

Output:

```text
NAME      READY   STATUS    RESTARTS   AGE
big-pod   0/1     Pending   0          12s
```

The pod remained stuck in the Pending state.

---

## Investigation

### Step 1 - Verify Pod Status

Command:

```bash
kubectl get pods
```

Observation:

```text
STATUS = Pending
```

Unlike previous incidents:

* No ImagePullBackOff
* No CrashLoopBackOff
* No OOMKilled

The pod never progressed beyond scheduling.

---

### Step 2 - Inspect Pod Events

Command:

```bash
kubectl describe pod big-pod
```

Events:

```text
Warning  FailedScheduling

0/1 nodes are available:
1 Insufficient cpu,
1 Insufficient memory.
```

This immediately identified the scheduling failure.

---

### Step 3 - Verify Node Capacity

Command:

```bash
kubectl describe node devops-cluster-control-plane
```

Allocatable Resources:

```text
cpu:    8
memory: 8108136Ki
```

Approximately:

```text
CPU    = 8 cores
Memory = 7.7 GiB
```

---

### Step 4 - Review Pod Resource Requests

Pod configuration:

```yaml
resources:
  requests:
    cpu: "10"
    memory: "10Gi"
```

Requested resources exceeded available node capacity.

Comparison:

```text
Requested CPU    = 10 cores
Available CPU    = 8 cores

Requested Memory = 10 GiB
Available Memory ≈ 7.7 GiB
```

The scheduler could not find a suitable node.

---

## Root Cause

The pod requested more CPU and memory than any node in the cluster could provide.

Because Kubernetes could not find a node capable of satisfying the requests, the scheduler refused to place the pod.

The pod remained in:

```text
Pending
```

state indefinitely.

---

## Resolution

Delete the oversized test pod:

```bash
kubectl delete pod big-pod
```

Production alternatives:

* Reduce resource requests.
* Add larger nodes.
* Add additional worker nodes.
* Optimize application resource consumption.

---

## Verification

Command:

```bash
kubectl get pods
```

Result:

```text
big-pod removed
```

Cluster returned to normal operation.

---

## Lessons Learned

Kubernetes scheduling decisions are based primarily on resource requests.

Example:

```yaml
requests:
  cpu: "10"
  memory: "10Gi"
```

The scheduler evaluates whether any node can satisfy those requirements.

If no node has sufficient allocatable resources:

```text
Pod remains Pending
```

and is never scheduled.

---

## Requests vs Limits

### Requests

```yaml
requests:
  memory: 10Gi
```

Requests are used by the Kubernetes scheduler when selecting a node.

Requests affect:

```text
Pod Placement
```

---

### Limits

```yaml
limits:
  memory: 10Gi
```

Limits control maximum runtime resource consumption.

Limits affect:

```text
Container Execution
```

Exceeding memory limits can lead to:

```text
OOMKilled
```

as demonstrated in Incident 005.

---

## Key Observation

Scheduling failures occur before containers exist.

Because the pod was never scheduled:

```text
No Node Assignment
No Container Creation
No Image Pull
No Application Startup
No Logs
```

Attempting:

```bash
kubectl logs big-pod
```

would fail because no container was ever started.

---

## Commands Used

```bash
kubectl apply -f big-pod.yaml

kubectl get pods

kubectl describe pod big-pod

kubectl describe node devops-cluster-control-plane

kubectl delete pod big-pod
```