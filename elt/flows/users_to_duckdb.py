from __future__ import annotations

import os
from typing import List, Dict, Any

import duckdb
import pandas as pd
import requests
from prefect import flow, task, get_run_logger


API_ORIGIN = os.getenv("API_ORIGIN", "http://localhost:8000")
DUCKDB_PATH = os.getenv("DUCKDB_PATH", os.path.join(os.getcwd(), "warehouse.duckdb"))


@task
def fetch_users() -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_ORIGIN}/users/")
    resp.raise_for_status()
    data = resp.json()
    # backend returns {items,total,page,size}
    return data.get("items", [])


@task
def load_to_duckdb(users: List[Dict[str, Any]]) -> int:
    logger = get_run_logger()
    df = pd.DataFrame(users)
    con = duckdb.connect(DUCKDB_PATH)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS users_raw (
            id INTEGER,
            email VARCHAR,
            name VARCHAR
        )
        """
    )
    # simple replace load
    con.execute("DELETE FROM users_raw")
    con.register("users_df", df)
    con.execute("INSERT INTO users_raw SELECT * FROM users_df")
    count = con.execute("SELECT COUNT(*) FROM users_raw").fetchone()[0]
    con.close()
    logger.info("Loaded %s rows into DuckDB at %s", count, DUCKDB_PATH)
    return int(count)


@flow(name="users-to-duckdb")
def users_to_duckdb_flow() -> int:
    users = fetch_users()
    count = load_to_duckdb(users)
    return count


if __name__ == "__main__":
    users_to_duckdb_flow()


