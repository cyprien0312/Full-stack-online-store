import duckdb


def main() -> None:
    con = duckdb.connect("data/duckdb/db.duckdb")
    rows = con.execute("show tables").fetchall()
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()


