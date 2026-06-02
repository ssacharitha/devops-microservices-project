Symptoms:
Application inaccessible through service/ingress.
Pods appeared healthy and running
No pod restarts observed

Investigation
Step 1: Verify Pod Health
kubectl get pods

Result:
All pods were running.

Step 2: Verify Deployment Health
kubectl get deployments

Result:
Deployment showed 2/2 available replicas.

Step 3: Verify Service Endpoints
kubectl get endpoints flask-backend

Result:
<none>

Step 4: Verify Service Selector
kubectl describe svc flask-backend

Observed:
selector:
  app: flask-backend-broken

Step 5: Verify Pod Labels
kubectl get pods --show-labels

Observed:
app=flask-backend

Selector and labels did not match.

Root Cause:
Service selector changed from 
app=flask-backend
to 
app=flask-backend-broken.

No pods matched the selector, so Kubernetes removed all Service endpoints, and traffic could no longer be routed to backend Pods.

Resolution:
Restored correct selector.

Verification:
kubectl get endpoints flask-backend
kubectl describe svc flask-backend

Endpoints returned:
10.244.0.4:5000
10.244.0.7:5000

Lessons Learned:
Healthy pods do not guarantee working networking.

Traffic flow:
Client
→ Ingress
→ Service
→ Endpoints
→ Pods

A Service depends on matching Pod labels to build its endpoint list.
No matching labels = No endpoints = No traffic routing.

Always verify endpoints.

Commands Used:
kubectl get pods
kubectl get deployments
kubectl get endpoints flask-backend
kubectl describe svc flask-backend
kubectl get pods --show-labels