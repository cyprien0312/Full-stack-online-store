# ELT Scaffold (Prefect + dbt + DuckDB)

## What you get
- Prefect flow: extract REST API -> CSV -> DuckDB table `raw.raw_users`
- dbt (DuckDB): transform `raw.raw_users` -> `analytics.raw__users`

## Run (Docker recommended)
```
# from repo root
make elt-up           # start backend+db+elt
make elt-run          # run flow and dbt
make elt-tables       # list tables in DuckDB
make elt-preview      # preview first 5 rows from analytics.raw__users
```

## Local (optional, if you prefer venv)
```
cd elt
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python flows/users_flow.py
cd dbt_project && export DBT_PROFILES_DIR=. && dbt deps && dbt run
```

## Layout
- flows/users_flow.py: Prefect flow, default API `http://backend:8000`
- data/raw/users.csv, data/duckdb/db.duckdb: outputs
- dbt_project/: dbt config and models
- scripts/: small helpers to query DuckDB

