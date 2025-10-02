# Full‑Stack Python + ELT Monorepo

This repository contains a production‑ready learning/project scaffold to build:
- A FastAPI backend (REST API, auth-ready)
- A modern frontend (Next.js, coming next)
- A data ELT stack (Prefect + dbt, coming next)

## Structure

```
backend/   # FastAPI service
frontend/  # Next.js app (to be scaffolded)
elt/       # Prefect flows + dbt project
docs/      # Architecture and runbooks
```

## Architecture

```mermaid
flowchart LR
  subgraph "Client"
    B[Browser]
  end

  subgraph "Frontend"
    FE[Next.js React TS]
  end

  subgraph "Backend"
    BE[FastAPI]
    DB[(Postgres)]
  end

  subgraph "ELT"
    PF[Prefect users_flow]
    CSV[(raw/users.csv)]
    DDB[(DuckDB)]
    DBT[dbt models]
  end

  B -->|HTTP| FE
  FE -->|/api/* rewrite| BE
  BE --> DB

  PF -->|GET /users/| BE
  PF --> CSV
  PF -->|load raw.raw_users| DDB
  DBT -->|transform| DDB
```

More details in `docs/ARCHITECTURE.md`.

## Quickstart (backend only for now)

Prerequisites: Python 3.11+, Docker (optional for later), Make (optional)

```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Visit: http://localhost:8000/healthz and /docs

## Roadmap (high‑level)
- Backend CRUD + Auth, DB migrations
- Frontend scaffold + auth flow
- ELT: Prefect orchestration + dbt models + data quality
- Docker Compose + CI/CD


