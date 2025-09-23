import duckdb


def main(limit: int = 5) -> None:
    con = duckdb.connect("data/duckdb/db.duckdb")
    df = con.execute(f"select * from analytics.raw__users limit {limit}").fetchdf()
    print(df)


if __name__ == "__main__":
    main()


