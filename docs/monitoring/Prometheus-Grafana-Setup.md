# Prometheus-Grafana-Setup.md

## Overview

This document describes the implementation of Prometheus and Grafana monitoring for the DevOps Kubernetes project.

The monitoring stack was deployed using the kube-prometheus-stack Helm chart and provides:

* Prometheus for metrics collection
* Grafana for visualization
* Alertmanager for alert management
* Node Exporter for node-level metrics
* kube-state-metrics for Kubernetes object metrics

---

## Architecture

Flask Application
↓
Kubernetes Cluster
↓
Prometheus
↓
Grafana Dashboards

Components:

* Prometheus
* Grafana
* Alertmanager
* Node Exporter
* kube-state-metrics

---

## Prerequisites

* Docker Desktop
* Kubernetes (Kind)
* kubectl
* Helm

Verify Helm:

```bash
helm version
```

---

## Installation

### Add Helm Repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update
```

### Install Monitoring Stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack
```

---

## Verification

Verify monitoring pods:

```bash
kubectl get pods
```

Expected components:

* monitoring-grafana
* monitoring-kube-prometheus-prometheus
* monitoring-kube-state-metrics
* monitoring-prometheus-node-exporter
* monitoring-kube-prometheus-alertmanager

---

## Access Grafana

Port Forward:

```bash
kubectl port-forward svc/monitoring-grafana 3000:80
```

Access:

```text
http://localhost:3000
```

Default username:

```text
admin
```

Retrieve password:

```bash
kubectl get secret monitoring-grafana -o jsonpath="{.data.admin-password}"
```

Decode Base64 value and log in.

---

## Built-in Dashboards

The following dashboards were automatically installed:

* Kubernetes / Compute Resources / Cluster
* Kubernetes / Compute Resources / Pod
* Kubernetes / Compute Resources / Workload
* Kubernetes / Networking / Pod
* Kubernetes / API Server
* Grafana Overview
* Alertmanager Overview

---

## Monitoring Application Pods

Selected Pod:

```text
flask-backend-855b554b49-2j8rz
```

Observed Metrics:

### CPU

| Metric                  | Value   |
| ----------------------- | ------- |
| CPU Usage               | 0.00116 |
| CPU Request             | 0.100   |
| CPU Limit               | 0.200   |
| CPU Request Utilization | 1.16%   |

### Memory

| Metric                     | Value    |
| -------------------------- | -------- |
| Memory Usage               | 37.4 MiB |
| Memory Request             | 128 MiB  |
| Memory Limit               | 256 MiB  |
| Memory Request Utilization | 29.2%    |
| Memory Limit Utilization   | 14.6%    |

---

## Relationship to Previous Incidents

### Incident 005 – OOMKilled

Grafana memory dashboards can be used to detect increasing memory consumption before a container exceeds its memory limit and becomes OOMKilled.

### Incident 006 – Pending Pod

Resource requests displayed in Grafana correspond to scheduler decisions that determine whether a pod can be placed on a node.

---

## Dashboard Screenshots

### CPU Usage

Shows CPU consumption of the Flask application pod.

![CPU Usage](../screenshots/cpu_usage.png)

### CPU Throttling

Shows whether Kubernetes is throttling CPU usage.

![CPU Throttling](../screenshots/cpu_throttling.png)

### CPU Quota

Displays CPU requests, limits, and utilization percentages.

![CPU Quota](../screenshots/cpu_quota.png)

### Memory Usage

Shows memory consumption of the Flask application pod.

![Memory Usage](../screenshots/memory_usage.png)

### Memory Quota

Displays memory requests, limits, and utilization percentages.

![Memory Quota](../screenshots/memory_quota.png)

---

## Key Learnings

* Prometheus collects metrics from Kubernetes workloads.
* Grafana visualizes metrics using dashboards.
* Resource requests affect scheduling.
* Resource limits affect runtime behavior.
* Monitoring provides early warning before outages occur.
* Observability complements troubleshooting and incident response.