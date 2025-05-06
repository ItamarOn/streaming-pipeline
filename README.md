# 📊 Streaming Pipeline - Documentation

## 🧩 Overview

This project demonstrates a full real-time streaming pipeline built with Kafka, Redis, and FastAPI. It includes a simulated clickstream producer, a Kafka consumer that aggregates data into Redis, and a FastAPI service that exposes click counts via HTTP.

---

## 🧪 Phase 1: Local Docker-Compose Setup

This phase simulates a full pipeline on your development machine using Docker Compose.

### Services Involved:

* **Kafka**: Message broker for ingesting events.
* **Zookeeper**: Required for Kafka coordination.
* **Redis**: In-memory storage used for aggregation.
* **Producer**: Sends random user click events to Kafka.
* **Consumer**: Reads from Kafka and updates Redis.
* **API (FastAPI)**: Provides an HTTP endpoint to query user click counts.

### Setup

   ```bash
   cd streaming-pipeline
   docker-compose up --build
   ```

### Accessing the System

* Monitor messages via logs: `docker-compose logs -f producer`
* Check there is data in Redis:
   - Run the following command to check if there is data in Redis:
     ```bash
     docker exec -it redis redis-cli
     ```
   - Then run the following command to check if there is data in Redis:
     ```bash
     keys *
     ```
   - or use python script to check if there is data in Redis:
     ```python
     import redis

     r = redis.Redis(host="localhost", port=6379)
     raw = r.hgetall("clicks")
     data = {k.decode(): int(v.decode()) for k, v in raw.items()}
     sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
     for i, (user, count) in enumerate(sorted_data[:10], 1):
        print(f"{i}. {user} - {count} clicks")
     ```
    - This will print the top 10 users with the most clicks:
     ```
     1. matthew.thompson@dell.com - 38 clicks
     2. david.taylor@tesla.com - 37 clicks
     ...
    ```
* Query data manually:
  ```bash
  curl http://localhost:8000/clicks/ava.young@zoom.us
  ```

> ✅ This phase is orchestrated entirely by Docker Compose and is ideal for local development and testing.

---

## 🚀 Phase 2 – Minikube Kubernetes Setup (Local K8s Cluster)

In this phase, we deploy the same services in a local Kubernetes environment using Minikube.

### Initial Setup

```bash
brew install minikube
minikube start

# Point Docker to build inside Minikube:
eval $(minikube -p minikube docker-env)

# Build custom images:
docker build -t streaming-pipeline-producer ./producer
docker build -t streaming-pipeline-consumer ./consumer
docker build -t streaming-pipeline-api ./api
```

### Apply Kubernetes manifests

```bash
cd k8s-manifests
kubectl apply -f .
```

### Accessing the API

**Option 1: Port-forward**

```bash
kubectl port-forward service/api 8000:8000
curl http://localhost:8000/clicks/lily.green@stripe.com
```

**Option 2: Minikube's dynamic URL**

```bash
minikube service api --url
```

---

## 📁 Folder Structure

```
streaming-pipeline/
├── producer/                  # Kafka producer code and Dockerfile
├── consumer/                  # Kafka consumer code and Dockerfile
├── api/                       # FastAPI service code and Dockerfile
├── docker-compose.yml         # Docker Compose setup for local simulation
└── k8s-manifests/             # Kubernetes manifests for Minikube setup
```

---

## 🔜 Next Step: AWS EKS

We’ll deploy this exact architecture on Amazon Elastic Kubernetes Service (EKS), with proper IAM roles, networking, and managed services like MSK (Kafka) or ElastiCache (Redis).

Stay tuned and remember our structure:
```
[Producer Pod] --> [Kafka] <-- [Consumer Pod] --> [Redis]   <-- [API Pod] <-- Client
```
