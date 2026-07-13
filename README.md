# 🛡️ StreamShield AI

> Intelligent AI-Powered Live Streaming Guardian

An AI-powered platform that continuously monitors live video streams, detects anomalies in real time, identifies probable root causes using Retrieval-Augmented Generation (RAG), and recommends corrective actions before millions of viewers are impacted.

Built as a Full Stack AI Engineering project using **Next.js**, **Django REST Framework**, **LangGraph**, **LangChain**, **FAISS**, and **Docker**.

---

# 🚀 Features

## 📡 Live Streaming Monitoring

- Monitor multiple live streams
- View real-time streaming metrics
- Regional health monitoring
- Dashboard with live charts
- Stream status tracking

---

## 📈 Metrics Collection

Collects

- Concurrent Viewers
- Buffer Ratio
- Startup Time
- CDN Latency
- Failure Rate
- Bitrate
- Packet Loss
- FPS

Metrics are stored inside the backend database and continuously updated by the simulator.

---

## 🤖 AI Incident Detection

Automatically detects

- Buffering spikes
- CDN degradation
- High latency
- Network packet loss
- Playback startup delays
- Video quality degradation

Severity levels

- Low
- Medium
- High
- Critical

---

## 🚨 Incident Management

Automatically creates incidents containing

- Severity
- Region
- Root Cause
- Confidence Score
- Recommended Actions
- AI Summary
- Affected Users

---

## 📚 Knowledge Base

Supports

- Markdown Runbooks
- PDF Runbooks
- Chunking
- Embeddings
- FAISS Vector Search

Current Runbooks

- Buffering
- CDN Failure
- Regional Outage
- Playback Startup
- Traffic Spike

---

## 🧠 Retrieval-Augmented Generation (RAG)

Pipeline

Runbooks

↓

Document Loader

↓

Chunker

↓

Sentence Transformer Embeddings

↓

FAISS Vector Store

↓

Retriever

↓

Relevant Context

↓

AI Workflow

---

## 🔄 LangGraph Workflow

The AI workflow consists of

Detect Incident

↓

Retrieve Context

↓

Root Cause Analysis

↓

Recommendation Generation

↓

Incident Summary

↓

Store Results

---

## 📊 Dashboard

Dashboard includes

- Live Metrics
- Active Streams
- Active Incidents
- Stream Health
- Severity Distribution
- Regional Status
- Recommendations
- Historical Incidents

---

# 🏗️ Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | Next.js |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Backend | Django REST Framework |
| Database | SQLite (Development) / Azure SQL (Deployment) |
| AI Framework | LangGraph |
| RAG | LangChain |
| Vector Database | FAISS |
| Embeddings | all-MiniLM-L6-v2 |
| LLM | Azure OpenAI (Deployment Phase) |
| API Docs | drf-spectacular |
| Containerization | Docker |
| Deployment | Azure Container Apps + Vercel |

---

# 🏛️ Architecture

```

                    +----------------------+
                    |    Next.js Frontend  |
                    +----------+-----------+
                               |
                         REST APIs
                               |
                               v
                 +---------------------------+
                 | Django REST Framework API |
                 +-----------+---------------+
                             |
        +--------------------+---------------------+
        |                    |                     |
        |                    |                     |
        v                    v                     v

   Stream APIs       Simulator Engine      Incident APIs

        |                    |                     |
        +---------+----------+---------------------+
                  |
                  v

          Stream Metrics Database

                  |
                  v

         Threshold Anomaly Detection

                  |
                  v

             LangGraph Workflow

                  |
        +---------+---------+
        |                   |
        v                   v

   FAISS Retriever     Azure OpenAI
 (Current Working)     (Deployment)

        |                   |
        +---------+---------+
                  |
                  v

        AI Incident Generation

                  |
                  v

        Live Operations Dashboard

```

---

# 📂 Project Structure

backend/

├── ai_engine/

├── config/

├── incidents/

├── knowledge_base/

├── simulator/

├── streams/

├── faiss_index/

├── manage.py

├── requirements.txt

├── README.md

└── seed_demo_data.py

---

# 📦 Backend Applications

## streams

Responsible for

- Stream CRUD
- Stream Metrics
- Dashboard Summary
- Anomaly Detection

---

## incidents

Responsible for

- Incident Management
- Recommendations
- Knowledge Documents

---

## simulator

Responsible for

- Live Metric Generation
- Demo Scenarios
- Streaming Simulation

---

## knowledge_base

Responsible for

- Loading Documents
- Chunking
- Embeddings
- FAISS
- Semantic Retrieval

---

## ai_engine

Responsible for

- LangGraph Workflow
- AI State
- AI Nodes
- AI Services

---
# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/StreamShield-AI.git

cd StreamShield-AI/backend
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv env

env\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv env

source env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## 5. Load Demo Data

```bash
python manage.py shell < seed_demo_data.py
```

---

## 6. Build FAISS Index

```bash
python manage.py ingest_runbooks
```

This command

- Loads markdown runbooks
- Splits documents into chunks
- Generates embeddings
- Creates FAISS index
- Saves index locally

Generated files

```
faiss_index/

index.faiss

index.pkl
```

---

## 7. Start Backend

```bash
python manage.py runserver
```

Backend

```
http://127.0.0.1:8000
```

---

# 🌐 Frontend

Move into frontend

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run

```bash
npm run dev
```

Frontend

```
http://localhost:3000
```

---

# 📦 Environment Variables

Example

```
DEBUG=True

SECRET_KEY=change-me

DATABASE_URL=sqlite:///db.sqlite3

AZURE_OPENAI_ENDPOINT=

AZURE_OPENAI_API_KEY=

AZURE_OPENAI_DEPLOYMENT=

EMBEDDING_MODEL=all-MiniLM-L6-v2
```

Azure variables are optional during local development.

---

# 🐳 Docker

## Build Backend

```bash
docker build -t streamshield-backend .
```

Verify

```bash
docker images
```

---

## Run Container

```bash
docker run -p 8000:8000 streamshield-backend
```

Application

```
http://localhost:8000
```

---

# 📖 API Documentation

Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

---

ReDoc

```
http://127.0.0.1:8000/api/redoc/
```

---

OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

---

# 📡 REST APIs

## Dashboard

| Method | Endpoint |
|---------|----------|
| GET | /api/dashboard/ |

---

## Streams

| Method | Endpoint |
|---------|----------|
| GET | /api/streams/ |
| POST | /api/streams/ |
| GET | /api/streams/{id}/ |
| PUT | /api/streams/{id}/ |
| PATCH | /api/streams/{id}/ |
| DELETE | /api/streams/{id}/ |

---

## Metrics

| Method | Endpoint |
|---------|----------|
| GET | /api/metrics/ |
| POST | /api/metrics/ |
| GET | /api/metrics/{id}/ |
| PUT | /api/metrics/{id}/ |
| PATCH | /api/metrics/{id}/ |
| DELETE | /api/metrics/{id}/ |

---

## Incidents

| Method | Endpoint |
|---------|----------|
| GET | /api/incidents/ |
| POST | /api/incidents/ |
| GET | /api/incidents/{id}/ |
| PUT | /api/incidents/{id}/ |
| PATCH | /api/incidents/{id}/ |
| DELETE | /api/incidents/{id}/ |

Resolve Incident

```
PATCH

/api/incidents/{id}/resolve/
```

---

## Recommendations

| Method | Endpoint |
|---------|----------|
| GET | /api/recommendations/ |
| POST | /api/recommendations/ |
| GET | /api/recommendations/{id}/ |
| PATCH | /api/recommendations/{id}/complete/ |

---

## Knowledge Base

| Method | Endpoint |
|---------|----------|
| GET | /api/documents/ |
| POST | /api/documents/ |
| GET | /api/documents/{id}/ |
| PUT | /api/documents/{id}/ |
| DELETE | /api/documents/{id}/ |

---

Semantic Search

```
GET

/api/knowledge/search/?query=cdn failure
```

Example

```
/api/knowledge/search/?query=high buffering
```

---

## Simulator

### Available Scenarios

```
GET

/api/simulator/scenarios/
```

Returns

- Normal Traffic
- Traffic Spike
- CDN Failure
- Regional Outage

---

Generate Metrics

```
POST

/api/simulator/generate/
```

The simulator automatically inserts realistic metrics into the database.

---

# 🎮 Demo Scenarios

The project includes four pre-built scenarios.

## ✅ Normal Traffic

Healthy stream

Buffer Ratio

```
< 1%
```

Latency

```
< 100 ms
```

Expected Result

No incident created.

---

## 📈 Traffic Spike

Sudden viewer increase

Expected

Medium severity incident

Recommendations

- Scale origin
- Increase cache

---

## 🌍 Regional Outage

Region unavailable

Expected

High severity incident

Recommendations

- Redirect traffic
- Switch region

---

## 🚨 CDN Failure

Critical latency

Expected

Critical incident

Recommendations

- Failover CDN
- Purge cache
- Reduce bitrate temporarily

---

# 🗄️ Database

Current

```
SQLite
```

Deployment

```
Azure SQL Database
```

Main Tables

- Stream
- StreamMetric
- Incident
- Recommendation
- KnowledgeDocument
# 📸 Screenshots

> Replace the placeholders below with actual screenshots before submission.

---

## Dashboard

```
docs/screenshots/dashboard.png
```

Shows

- Live KPI cards
- Active Streams
- Active Incidents
- Regional Health
- Severity Distribution
- Live Metrics

---

## Stream Metrics

```
docs/screenshots/metrics.png
```

Shows

- Buffer Ratio
- Latency
- Packet Loss
- Startup Time
- FPS
- Viewer Count

---

## Incident Details

```
docs/screenshots/incident.png
```

Shows

- Severity
- Region
- Root Cause
- AI Summary
- Recommendations
- Confidence Score

---

## Swagger UI

```
docs/screenshots/swagger.png
```

Shows

- API documentation
- Request examples
- Response schemas

---

## Knowledge Search

```
docs/screenshots/knowledge-search.png
```

Shows

- Semantic search
- Retrieved runbook
- Similarity-based results

---

## Simulator

```
docs/screenshots/simulator.png
```

Shows

- Scenario selection
- Generated metrics
- Incident generation

---

# 🧪 Demo Walkthrough

A typical demonstration follows these steps.

### Step 1

Start backend

```bash
python manage.py runserver
```

---

### Step 2

Start frontend

```bash
npm run dev
```

---

### Step 3

Insert demo data

```bash
python manage.py shell < seed_demo_data.py
```

---

### Step 4

Index runbooks

```bash
python manage.py ingest_runbooks
```

---

### Step 5

Open dashboard

```
http://localhost:3000
```

---

### Step 6

Generate simulator data

```
POST

/api/simulator/generate/
```

---

### Step 7

Observe

- Live Metrics
- Dashboard Updates
- Incident Creation
- Recommendations
- Knowledge Retrieval

---

# 🛠️ Useful Commands

## Create Migrations

```bash
python manage.py makemigrations
```

---

## Apply Migrations

```bash
python manage.py migrate
```

---

## Run Backend

```bash
python manage.py runserver
```

---

## Load Demo Data

```bash
python manage.py shell < seed_demo_data.py
```

---

## Build FAISS Index

```bash
python manage.py ingest_runbooks
```

---

## Build Docker Image

```bash
docker build -t streamshield-backend .
```

---

## Run Docker

```bash
docker run -p 8000:8000 streamshield-backend
```

---

## Swagger

```
http://127.0.0.1:8000/api/docs/
```

---

## ReDoc

```
http://127.0.0.1:8000/api/redoc/
```

---

## OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

---

# 🐞 Troubleshooting

## FAISS index not found

Run

```bash
python manage.py ingest_runbooks
```

---

## No incidents generated

Generate one of the abnormal scenarios

- Traffic Spike
- CDN Failure
- Regional Outage

---

## Knowledge search returns nothing

Ensure the FAISS index has been created.

```bash
python manage.py ingest_runbooks
```

---

## Docker build fails

Verify Docker Desktop is running.

Then rebuild

```bash
docker build -t streamshield-backend .
```

---

# 🗺️ Project Roadmap

## Phase 1 ✅

- Django Backend
- Next.js Frontend
- REST APIs
- Simulator
- Dashboard
- Threshold Anomaly Detection
- Incident Engine
- Knowledge Base
- RAG Pipeline
- LangGraph Workflow
- FAISS Integration
- Swagger Documentation
- Docker Support

---

## Phase 2 🔄

- Azure SQL
- Azure Blob Storage
- Azure OpenAI
- Azure Container Apps
- Vercel Deployment
- JWT Authentication

---

## Phase 3 🚀

- Isolation Forest
- Predictive Analytics
- Redis
- Celery
- WebSockets
- Azure AI Search
- Monitoring
- CI/CD
- Kubernetes

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit changes

```bash
git commit -m "Add feature"
```

4. Push

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

# 📜 License

This project is intended for educational and hackathon purposes.

You may use or modify the source code for learning and experimentation.

---

# 👨‍💻 Author

**Anubhav Bangari**

AI Full Stack Engineer

GitHub:

```
https://github.com/AnubhavBangari3
```

---

# 🙏 Acknowledgements

This project was built using:

- Django REST Framework
- Next.js
- Tailwind CSS
- Recharts
- LangChain
- LangGraph
- FAISS
- Sentence Transformers
- scikit-learn
- Docker
- drf-spectacular

Special thanks to the open-source community for providing the tools and libraries that made this project possible.

---

# ⭐ Support

If you found this project useful,

⭐ Star the repository

🍴 Fork it

🐛 Report issues

💡 Suggest improvements

---

# 📬 Contact

For questions or collaboration opportunities, feel free to connect via GitHub.

---
