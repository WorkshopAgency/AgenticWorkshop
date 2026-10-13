#!/usr/bin/env python3
"""Create exercises/03-mcp/data/workshop.duckdb from the shipped data files.

Run from the workshop root, before enabling the DuckDB MCP server:

    uv run --with duckdb python exercises/03-mcp/scripts/make_db.py

It does nothing if the database already exists; pass --force to rebuild.

The database is a build product and is not part of the download: the Parquet
files are 5 MB, the database is about 17 MB. Building it locally keeps the
workshop ZIP small and lets the MCP server open a real file in read-only
mode, which an in-memory database cannot do.

Tables: entries and entry_types (PDB snapshot), and penguins. The penguins
CSV is loaded exactly as shipped, so its missing values, written as the text
"NA", are still in it. Finding that out is part of Exercise 3.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
DB = os.path.join(DATA, "workshop.duckdb")
TABLES = {"entries": "pdb_entries.parquet", "entry_types": "pdb_entry_types.parquet"}
CSV_TABLES = {"penguins": os.path.join("byo", "penguins.csv")}


def main():
    files = list(TABLES.values()) + list(CSV_TABLES.values())
    missing = [f for f in files if not os.path.exists(os.path.join(DATA, f))]
    if missing:
        sys.exit(f"Missing data file(s) in exercises/03-mcp/data: {', '.join(missing)}\n"
                 f"Run this from the workshop root, or rebuild with "
                 f"exercises/03-mcp/scripts/build_pdb_dataset.py")
    try:
        import duckdb
    except ImportError:
        sys.exit("duckdb is not installed. Run:\n"
                 "  uv run --with duckdb python exercises/03-mcp/scripts/make_db.py")

    force = "--force" in sys.argv
    if os.path.exists(DB) and not force:
        print(f"Already built: {DB} ({os.path.getsize(DB)/1048576:.1f} MiB)")
        print("Pass --force to rebuild it.")
        return
    if os.path.exists(DB):
        print(f"Rebuilding {DB}")
        os.remove(DB)

    con = duckdb.connect(DB)
    for table, parquet in TABLES.items():
        path = os.path.join(DATA, parquet).replace("'", "''")
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_parquet('{path}')")
        n = con.sql(f"SELECT count(*) FROM {table}").fetchone()[0]
        print(f"  {table:12} {n:>8,} rows")
    for table, csv in CSV_TABLES.items():
        path = os.path.join(DATA, csv).replace("'", "''")
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv('{path}')")
        n = con.sql(f"SELECT count(*) FROM {table}").fetchone()[0]
        print(f"  {table:12} {n:>8,} rows")
    con.close()

    print(f"\nWrote {DB} ({os.path.getsize(DB)/1048576:.1f} MiB)")
    print("duckdb library:", duckdb.__version__)


if __name__ == "__main__":
    main()
