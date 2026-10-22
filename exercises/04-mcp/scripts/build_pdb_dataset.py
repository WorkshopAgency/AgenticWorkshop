#!/usr/bin/env python3
"""Build the workshop DuckDB/Parquet dataset from wwPDB derived data.

Rebuild:
    uv run --with "duckdb<2" python exercises/04-mcp/scripts/build_pdb_dataset.py

Downloads three public wwPDB index files, normalises them, and writes the
Parquet tables and the hand-checkable CSV sample into exercises/04-mcp/data/.
Run it from the workshop root. Students do not need to run this; the built
files are shipped. See exercises/04-mcp/data/PROVENANCE.md.
"""
import os, sys, urllib.request

BASE = "https://files.wwpdb.org/pub/pdb/derived_data"
SOURCES = {
    "entries.idx": f"{BASE}/index/entries.idx",
    "pdb_entry_type.txt": f"{BASE}/pdb_entry_type.txt",
}
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(os.path.dirname(HERE), "data")
ZSTD_LEVEL = 22          # keeps the repository download near 5 MB
SAMPLE_MODULUS = 520     # deterministic ~1-in-520 sample, no RNG


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for name, url in SOURCES.items():
        dest = os.path.join(RAW, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f"cached   {name} ({os.path.getsize(dest):,} bytes)")
            continue
        print(f"download {name} <- {url}")
        urllib.request.urlretrieve(url, dest)
        print(f"         {os.path.getsize(dest):,} bytes")


def build():
    import duckdb
    con = duckdb.connect()
    con.execute(f"""
    CREATE VIEW raw_entries AS SELECT * FROM read_csv(
        '{RAW}/entries.idx', delim='\t', header=false, skip=2,
        quote='', escape='', ignore_errors=true,
        columns={{'idcode':'VARCHAR','hdr':'VARCHAR','acc':'VARCHAR','compound':'VARCHAR',
                  'src':'VARCHAR','authors':'VARCHAR','res':'VARCHAR','exp':'VARCHAR'}});
    """)
    con.execute(f"""
    CREATE VIEW raw_types AS SELECT * FROM read_csv(
        '{RAW}/pdb_entry_type.txt', delim='\t', header=false,
        quote='', escape='', ignore_errors=true,
        columns={{'idcode':'VARCHAR','mol':'VARCHAR','meth':'VARCHAR'}});
    """)
    # RESOLUTION is the literal string 'NOT' for entries with no refined
    # resolution (solution NMR and similar). It becomes SQL NULL here, so
    # aggregates skip it instead of failing on a cast.
    con.execute("""
    CREATE TABLE entries AS
    SELECT upper(trim(idcode))                       AS pdb_id,
           nullif(trim(hdr), '')                     AS classification,
           try_strptime(trim(acc), '%m/%d/%y')::DATE AS deposition_date,
           nullif(trim(compound), '')                AS title,
           nullif(trim(src), '')                     AS source_organism,
           CASE WHEN trim(res) IN ('NOT', '', '-1.00') THEN NULL
                ELSE try_cast(trim(res) AS DOUBLE) END AS resolution,
           nullif(trim(exp), '')                     AS experiment_type
    FROM raw_entries WHERE trim(idcode) <> '';
    """)
    con.execute("""
    CREATE TABLE entry_types AS
    SELECT upper(trim(idcode)) AS pdb_id,
           trim(mol)           AS molecule_type,
           trim(meth)          AS method_class
    FROM raw_types WHERE trim(idcode) <> '';
    """)

    os.makedirs(OUT, exist_ok=True)
    p = lambda n: os.path.join(OUT, n)
    opts = f"FORMAT parquet, COMPRESSION zstd, COMPRESSION_LEVEL {ZSTD_LEVEL}"
    con.execute(f"COPY entries     TO '{p('pdb_entries.parquet')}'     ({opts})")
    con.execute(f"COPY entry_types TO '{p('pdb_entry_types.parquet')}' ({opts})")
    con.execute(f"""
    COPY (SELECT e.*, t.molecule_type, t.method_class
          FROM entries e LEFT JOIN entry_types t USING (pdb_id)
          WHERE hash(e.pdb_id) % {SAMPLE_MODULUS} = 0
          ORDER BY e.pdb_id)
    TO '{p('pdb_sample.csv')}' (FORMAT csv, HEADER)""")

    print("\n--- built ---")
    for n in ("pdb_entries.parquet", "pdb_entry_types.parquet", "pdb_sample.csv"):
        print(f"{n:26} {os.path.getsize(p(n))/1048576:6.2f} MiB")
    for label, q in [
        ("entries",           "SELECT count(*) FROM entries"),
        ("distinct pdb_id",   "SELECT count(DISTINCT pdb_id) FROM entries"),
        ("date range",        "SELECT min(deposition_date)||' .. '||max(deposition_date) FROM entries"),
        ("null resolution",   "SELECT count(*) FROM entries WHERE resolution IS NULL"),
        ("entry_types rows",  "SELECT count(*) FROM entry_types"),
        ("sample rows",       f"SELECT count(*) FROM entries WHERE hash(pdb_id) % {SAMPLE_MODULUS} = 0"),
    ]:
        print(f"{label:26} {con.sql(q).fetchone()[0]}")


if __name__ == "__main__":
    fetch()
    build()
