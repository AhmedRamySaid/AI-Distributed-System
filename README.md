# 🧠 Distributed LLM Inference System
### Efficient Load Balancing & GPU Cluster Task Distribution for 1000+ Concurrent Requests

---

## 📋 Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the System](#running-the-system)
- [Configuration](#configuration)
- [Load Balancing Strategies](#load-balancing-strategies)
- [Fault Tolerance](#fault-tolerance)
- [RAG Pipeline](#rag-pipeline)
- [Testing](#testing)
- [Performance Metrics](#performance-metrics)

---

## Overview

This project implements a distributed system capable of handling **1000+ concurrent user requests** involving Large Language Model (LLM) inference and Retrieval-Augmented Generation (RAG). The system focuses on efficient load balancing and task distribution across GPU clusters to ensure high performance, low latency, and optimal resource utilization.

The system simulates real-world AI workloads where requests require heavy computation and must be distributed dynamically across multiple processing nodes, with a key focus on **scalability**, **performance optimization**, and **fault tolerance**.

---

## System Architecture

```
                        ┌─────────────────┐
                        │   Client Layer   │
                        │ (1000+ Users)    │
                        └────────┬────────┘
                                 │ HTTP Requests
                                 ▼
                        ┌─────────────────┐
                        │   NGINX         │
                        │  Load Balancer  │
                        │   (Port 80)     │
                        └────────┬────────┘
                                 │ Round Robin / Weighted
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
             ┌──────────┐ ┌──────────┐ ┌──────────┐
             │ Worker 1 │ │ Worker 2 │ │ Worker 3 │
             │  :8001   │ │  :8002   │ │  :8003   │
             └──────────┘ └──────────┘ └──────────┘
                    │            │            │
                    └────────────┼────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             ┌──────────┐             ┌──────────────┐
             │  Ollama  │             │   ChromaDB   │
             │  (LLM)   │             │    (RAG)     │
             │ GPU/CPU  │             │ Knowledge DB │
             └──────────┘             └──────────────┘
```

### Components

| Component | Description |
|---|---|
| **Client Layer** | Simulates concurrent users sending inference requests |
| **NGINX Load Balancer** | Distributes incoming requests across GPU worker nodes |
| **GPU Worker Nodes** | FastAPI servers that handle LLM inference and RAG retrieval |
| **Ollama (LLM)** | Runs the `qwen2.5:0.5b` language model for inference |
| **ChromaDB (RAG)** | Vector database storing the knowledge base for context retrieval |

---

## Features

- **Load Balancing** — Round robin and weighted strategies
- **GPU Acceleration** — CUDA streams for parallel GPU processing (NVIDIA)
- **RAG Integration** — TF-IDF based retrieval from a ChromaDB knowledge base
- **Fault Tolerance** — Automatic worker failure detection and request rerouting
- **Scalability** — Handles hundreds of concurrent users
- **Low Latency** — GPU inference reduces response times significantly vs CPU

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Web Server / Load Balancer** | NGINX |
| **API Framework** | FastAPI + Uvicorn |
| **LLM Inference** | Ollama (`qwen2.5:0.5b`) |
| **GPU Computing** | PyTorch + CUDA (NVIDIA) |
| **Vector Database** | ChromaDB |
| **Embeddings** | TF-IDF (scikit-learn) |
| **Language** | Python 3.12 |
| **OS** | Ubuntu (WSL2 on Windows) |

---

## Project Structure

```
server/
├── common/
│   ├── chroma_db/              # Persistent ChromaDB vector store
│   ├── knowledge_base.py       # Study techniques knowledge base documents
│   └── start_server.sh         # Server startup script
├── src/
│   ├── common/
│   │   └── models.py           # Shared data models
│   ├── workers/
│   │   └── gpu_worker.py       # GPU worker node (FastAPI + GPUWorker class)
│   ├── llm/
│   │   └── inference.py        # Ollama LLM inference interface
│   ├── rag/
│   │   ├── ingest.py           # Knowledge base ingestion into ChromaDB
│   │   └── retriever.py        # RAG context retrieval from ChromaDB
│   ├── lb/
│   │   └── load_balancer.conf  # Load balancer configure file (round robin)
│   └── master/
│       └── scheduler.py        # Master node scheduler

└── README.md
```

---

## Setup & Installation

### Prerequisites
- Windows with WSL2 (Ubuntu)
- Python 3.10+
- NVIDIA GPU with CUDA (optional but recommended)
- NGINX

### 1. Install System Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip nginx zstd -y
```

### 2. Install Python Dependencies

```bash
pip install fastapi uvicorn chromadb scikit-learn numpy requests --break-system-packages
```

### 3. Install PyTorch (NVIDIA GPU)

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu128 --break-system-packages
```

### 4. Install Ollama & Pull Model

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:0.5b
```

### 5. Configure NGINX

Create `/etc/nginx/conf.d/loadbalancer.conf`

Remove the default NGINX site:

```bash
sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.bak
sudo nginx -t && sudo systemctl reload nginx
```

### 6. Ingest Knowledge Base

```bash
cd ~/server
python3 -m src.rag.ingest
```

### 7. Windows Port Forwarding (for external access)

In PowerShell as Administrator:

```powershell
$wslIP = (wsl hostname -I).Trim()
netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=80 connectaddress=$wslIP
New-NetFirewallRule -DisplayName "NGINX WSL2" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
```

---

## Running the System

### Quick Start

```bash
~/start_server.sh
```

### Manual Start

```bash
# Start Ollama
ollama serve &

# Start NGINX
sudo systemctl start nginx

# Start GPU Workers
cd ~/server
python3 -m src.workers.gpu_worker --port 8001 &
python3 -m src.workers.gpu_worker --port 8002 &
python3 -m src.workers.gpu_worker --port 8003 &
```

### Sending a Request

```bash
curl -X POST http://localhost/infer \
     -H "Content-Type: application/json" \
     -d '{"query": "How can I remember things better?"}'
```

### Expected Response

```json
{
  "worker_id": 8001,
  "worker_port": 8001,
  "id": 1,
  "result": "To improve memory retention...",
  "latency": 3.49
}
```

---

## Configuration

### LLM Settings (`src/llm/inference.py`)

| Parameter | Default | Description |
|---|---|---|
| `MODEL_NAME` | `qwen2.5:0.5b` | Ollama model to use |
| `TEMPERATURE` | `0.3` | Response creativity (lower = more factual) |
| `MAX_TOKENS` | `512` | Maximum response length |
| `TIMEOUT_SEC` | `120` | Request timeout in seconds |

### RAG Settings (`src/rag/retriever.py`)

| Parameter | Default | Description |
|---|---|---|
| `TOP_K` | `3` | Number of context passages to retrieve |
| `COLLECTION_NAME` | `study_techniques` | ChromaDB collection name |

---

## Load Balancing Strategies

Three strategies are supported, configurable in `nginx.conf`:

### Round Robin (Default)
Distributes requests evenly across workers in rotation.
```nginx
upstream gpu_workers {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```

### Weighted Round Robin
Sends more requests to more powerful workers.
```nginx
upstream gpu_workers {
    server 127.0.0.1:8001 weight=3;
    server 127.0.0.1:8002 weight=2;
    server 127.0.0.1:8003 weight=1;
}
```

### Least Connections
Routes to the worker with fewest active requests.
```nginx
upstream gpu_workers {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```

---

## Fault Tolerance

The system implements fault tolerance at two levels:

### NGINX Level
- Automatically detects worker failures via `max_fails` and `fail_timeout`
- Retries failed requests on the next available worker
- Marks failed workers as unavailable for `fail_timeout` seconds

### Worker Recovery
Workers that recover are automatically reintroduced into the rotation after `fail_timeout` expires.

To simulate a failure:
```bash
# Kill a worker
kill $(lsof -t -i:8001)

# Restart it
cd ~/server && python3 -m src.workers.gpu_worker --port 8001 &
```

---

## RAG Pipeline

The RAG (Retrieval-Augmented Generation) pipeline enhances LLM responses with relevant context:

1. **Ingestion** — Documents from `knowledge_base.py` are embedded using TF-IDF and stored in ChromaDB
2. **Retrieval** — For each query, the top-K most relevant passages are retrieved using cosine similarity
3. **Generation** — Retrieved context is injected into the LLM prompt to produce grounded, accurate answers

```
Query → TF-IDF Embedding → ChromaDB Search → Top-K Passages → LLM Prompt → Answer
```

---

## Testing

### Single Request Test

```bash
curl -X POST http://localhost/infer \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the Feynman technique?"}'
```

### Load Test (Python)

Run the main file with the choosen number of simulated users

### Fault Tolerance Test

```bash
# Start load test, then kill a worker mid-way
kill $(lsof -t -i:8001)
# Observe requests rerouting to remaining workers automatically
```

---

## Performance Metrics

Each response includes server-side latency:

```json
{
  "worker_id": 8001,
  "latency": 3.49
}
```

| Setup | Avg Latency per Request |
|---|---|
| CPU inference | 5–7 seconds |
| GPU inference (RTX 3050) | 0.7–1.5 second |

---

## Team

Built as part of a distributed systems course project focusing on scalable AI infrastructure.
