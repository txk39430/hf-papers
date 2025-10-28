# 🧠 HF Papers — Hugging Face Papers Clone

A local implementation of [Hugging Face Papers](https://huggingface.co/papers), built from scratch using **FastAPI**, **PostgreSQL**, and **Redis**.  
This project runs locally first and will be extended into a full-stack web app.

---

## 🚀 Project Overview

The goal is to create a lightweight system that fetches and stores AI research paper metadata (title, authors, date, etc.) and displays them in a web interface — similar to Hugging Face’s “Papers” portal.

**Current components:**
- **FastAPI** backend (`api/`) for REST APIs  
- **PostgreSQL** database for persistent storage  
- **Redis** for caching  
- **Docker Compose** (`ops/`) for local container orchestration

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| Backend | FastAPI | REST API Framework |
| Database | PostgreSQL | Main database |
| Cache | Redis | Caching and message queue |
| Infrastructure | Docker, Docker Compose | Container management |
| Language | Python 3.12 | Core development language |

---

## 🧩 Local Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/txk39430/hf-papers.git
cd hf-papers

 # tiny change
