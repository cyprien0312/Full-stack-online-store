# System Architecture

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

## Notes
- Frontend uses Next rewrites to avoid CORS by proxying to the backend.
- Prefect extracts from the backend API, lands raw CSV, loads into DuckDB raw schema.
- dbt transforms raw tables into analytics schema tables.
- Docker Compose brings up `db`, `backend`, `frontend`, and `elt` services for local dev.

