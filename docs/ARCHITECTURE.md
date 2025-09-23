# System Architecture

```mermaid
flowchart LR
  subgraph Client
    B[Browser]
  end

  subgraph Frontend
    FE[Next.js (React, TS)]
  end

  subgraph Backend
    BE[FastAPI]
    DB[(PostgreSQL)]
  end

  subgraph ELT
    PF[Prefect Flow\\nusers_flow]
    CSV[(raw/users.csv)]
    DDB[(DuckDB\\nraw, analytics)]
    DBT[dbt (DuckDB)\\nmodels]
  end

  B -->|HTTP| FE
  FE -->|/api/* rewrites| BE
  BE -->|SQLAlchemy| DB

  PF -->|GET /users/| BE
  PF -->|write| CSV
  PF -->|load raw.raw_users| DDB
  DBT -->|transform| DDB

  style BE fill:#e6f3ff,stroke:#5aa0e6
  style FE fill:#e9ffe6,stroke:#67c23a
  style PF fill:#fff3e6,stroke:#f5a623
  style DBT fill:#fff3e6,stroke:#f5a623
  style DB fill:#f0f0f0,stroke:#bdbdbd
  style DDB fill:#f0f0f0,stroke:#bdbdbd
```

## Notes
- Frontend uses Next rewrites to avoid CORS by proxying to the backend.
- Prefect extracts from the backend API, lands raw CSV, loads into DuckDB raw schema.
- dbt transforms raw tables into analytics schema tables.
- Docker Compose brings up `db`, `backend`, `frontend`, and `elt` services for local dev.

