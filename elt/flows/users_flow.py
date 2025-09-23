from pathlib import Path
import csv
import duckdb
import httpx
from prefect import flow, task


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RAW_DIR = DATA_DIR / "raw"
DB_DIR = DATA_DIR / "duckdb"
DB_PATH = DB_DIR / "db.duckdb"


@task
def fetch_users(api_url: str) -> list[dict]:
    resp = httpx.get(f"{api_url.rstrip('/')}/users/")
    resp.raise_for_status()
    payload = resp.json()
    return payload.get("items", []) if isinstance(payload, dict) else payload


@task
def write_csv(rows: list[dict]) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / "users.csv"
    if not rows:
        path.write_text("")
        return path
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sorted(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


@task
def load_duckdb(csv_path: Path) -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    con.execute("DROP TABLE IF EXISTS raw.raw_users;")
    con.execute(
        """
        CREATE TABLE raw.raw_users AS
        SELECT * FROM read_csv_auto(?);
        """,
        [str(csv_path)],
    )
    con.close()


@flow
def users_flow(api_url: str = "http://backend:8000") -> None:
    rows = fetch_users(api_url)
    csv_path = write_csv(rows)
    load_duckdb(csv_path)


if __name__ == "__main__":
    users_flow()


