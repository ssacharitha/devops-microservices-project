## 🚀 DevOps Microservices Project ##

A containerized Flask REST API with PostgreSQL, orchestrated using Docker Compose to simulate real-world DevOps workflows.

---

## 🏗 Architecture Overview ##

Client → Flask Backend (Container) → PostgreSQL (Container)

- Backend connects to database using Docker service discovery (`DB_HOST=db`)
- Docker Compose manages networking between containers
- Persistent volume ensures database data retention
- Database schema is automatically initialized using an init.sql script

---

## 📌 Phase 1 – Flask + PostgreSQL Backend ##

- REST API built with Flask
- PostgreSQL database integration
- Environment variable configuration
- Health check endpoint

---

## 🐳 Phase 2 – Dockerized Multi-Container Setup ##

- Backend containerized using Docker
- PostgreSQL containerized
- Multi-container orchestration with Docker Compose
- Internal container networking using service names
- Persistent volume for database storage
- Automated database initialization using SQL init script

---

## 🚀 API Endpoints ##

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /health  | Health check |
| GET    | /tasks   | Fetch all tasks |
| POST   | /tasks   | Create a new task |

---

## 🛠 Tech Stack ##

- Python (Flask)
- PostgreSQL
- Docker
- Docker Compose
- Kubernetes (Kind – upcoming phase)

---

## 🧠 DevOps Concepts Demonstrated ##

- Containerization
- Service discovery
- Environment-based configuration
- Persistent storage with Docker volumes
- Infrastructure reproducibility
- Multi-container orchestration

---

## ▶️ Run Locally ##

```bash
docker compose up --build

Once running, access the API:

- Health Check: http://localhost:5000/health
- Get Tasks: http://localhost:5000/tasks