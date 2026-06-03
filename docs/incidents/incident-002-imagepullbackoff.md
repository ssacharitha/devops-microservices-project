# Incident 002 - ImagePullBackOff During Deployment Rollout

## Impact

A new application version could not be deployed.

The existing application remained available because Kubernetes retained healthy Pods from the previous ReplicaSet.

Affected Components:

* Deployment rollout
* New ReplicaSet
* New Pod creation

Unaffected Components:

* Existing Flask Pods
* PostgreSQL Pod
* Service
* Ingress

## Symptoms

Observed Pod status:

ImagePullBackOff

During rollout, a newly created Pod failed to start.

## Detection

Command:

kubectl get pods -w

Observed:

ErrImagePull
ImagePullBackOff

## Investigation

### Step 1 - Observe Rollout

Command:

kubectl get pods -w

Observed:

* Existing Pods remained healthy.
* New Pod was created.
* New Pod entered ErrImagePull state.

### Step 2 - Inspect Pod Events

Command:

kubectl describe pod 

Observed:

Failed to pull image

docker.io/ssacharitha/devops-project-backend

not found

### Step 3 - Verify Deployment State

Command:

kubectl get deployment flask-backend

Observed:

READY: 2/2
AVAILABLE: 2

The existing application remained available.

### Step 4 - Inspect ReplicaSets

Command:

kubectl get rs

Observed:

Old ReplicaSet:
2 Ready Pods

New ReplicaSet:
0 Ready Pods

## Root Cause

Deployment image was intentionally changed from:

ssacharitha/devops-project-backend

to:

ssacharitha/devops-project-backend

The specified image tag did not exist in Docker Hub.

Kubelet could not pull the image and repeatedly retried, resulting in ErrImagePull followed by ImagePullBackOff.

## Resolution

Executed:

kubectl rollout undo deployment/flask-backend

Result:

* The previous ReplicaSet became active again.
* Failed ReplicaSet scaled to 0 replicas.
* Deployment successfully rolled back.

Verification:

kubectl rollout status deployment/flask-backend

Deployment successfully rolled out.

## Prevention

* Use immutable image tags based on Git commit SHA.
* Validate image existence before deployment.
* Use CI/CD validation checks.
* Avoid deploying manually typed image tags.

## Technical Learning

ImagePullBackOff and CrashLoopBackOff are different failures.

ImagePullBackOff:

* The container never starts.
* Application logs may not exist.
* Pod Events provide the most useful information.

CrashLoopBackOff:

* Container starts and crashes.
* Application logs become the primary troubleshooting source.

## Commands Used

kubectl get pods -w

kubectl describe pod

kubectl get deployment

kubectl get rs

kubectl rollout history deployment/flask-backend

kubectl rollout undo deployment/flask-backend

kubectl rollout status deployment/flask-backend

## What I Expected

I expected Kubernetes to create a new pod and fail to pull the image.

## What Actually Happened

The old pods remained available because Kubernetes used a RollingUpdate strategy.

A new ReplicaSet was created.

The new pod entered ErrImagePull and then ImagePullBackOff.

## What Surprised Me

Rollback reused the previous ReplicaSet instead of creating a new one.
