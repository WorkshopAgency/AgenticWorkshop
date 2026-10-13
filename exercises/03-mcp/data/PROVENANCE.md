# Dataset provenance

The workshop query dataset is derived from public wwPDB index files. Nothing
here is generated, estimated or synthetic: every row comes from the files
listed below. If a number in an exercise disagrees with this data, trust the
data and tell an organiser.

## Sources

| File | Source URL | Retrieved |
|---|---|---|
| `entries.idx` | `https://files.wwpdb.org/pub/pdb/derived_data/index/entries.idx` | 18 September 2026 |
| `pdb_entry_type.txt` | `https://files.wwpdb.org/pub/pdb/derived_data/pdb_entry_type.txt` | 18 September 2026 |

The wwPDB releases PDB data free of copyright restrictions; see the
[wwPDB usage policies](https://www.wwpdb.org/about/usage-policies). The
snapshot covers depositions from **1972-08-11 to 2026-09-09**.

Rebuild both Parquet files and the CSV sample from the original sources:

```bash
uv run --with duckdb python exercises/03-mcp/scripts/build_pdb_dataset.py
```

That re-downloads about 62 MB and takes a few minutes, mostly in compression.
Students do not need to run it.

## Files

| File | Rows | Size | Purpose |
|---|---:|---:|---|
| `pdb_entries.parquet` | 259,693 | 5.0 MiB | The main table. Too large to check by reading. |
| `pdb_entry_types.parquet` | 259,693 | 0.3 MiB | Molecule type and method class. Forces a join. |
| `pdb_sample.csv` | 512 | 87 KiB | A sample small enough to check **by hand**. |
| `workshop.duckdb` | — | 18 MiB | Build product, not shipped. Made by `../scripts/make_db.py`; also holds `penguins` from `byo/penguins.csv`, loaded as shipped. |

The CSV sample is deterministic, not random: it is every entry where
`hash(pdb_id) % 520 = 0`. Rebuilding reproduces exactly the same 512 rows.
It is a sample for checking method, **not** a statistically representative
subset — do not quote percentages from it as if they described the PDB.

## Schema

`entries`

| Column | Type | Notes |
|---|---|---|
| `pdb_id` | VARCHAR | Uppercase, 4 characters. 259,693 distinct values, no duplicates. |
| `classification` | VARCHAR | Deposited header, e.g. `OXYGEN TRANSPORT`. |
| `deposition_date` | DATE | Parsed from `MM/DD/YY`. No nulls. |
| `title` | VARCHAR | Free text, upper case. |
| `source_organism` | VARCHAR | Free text as deposited, **not** a controlled vocabulary. |
| `resolution` | DOUBLE | **NULL for 15,104 entries.** See below. |
| `experiment_type` | VARCHAR | May list several methods, comma separated. |

`entry_types`

| Column | Type | Notes |
|---|---|---|
| `pdb_id` | VARCHAR | Joins to `entries.pdb_id`. Every entry matches; there are no orphans. |
| `molecule_type` | VARCHAR | `prot`, `prot-nuc`, `nuc`, `other`. |
| `method_class` | VARCHAR | `diffraction`, `EM`, `NMR`, `other`. One label per entry. |

## Known quirks — these are real, and deliberately preserved

**1. Resolution is missing for 15,104 entries, and not at random.**
In the source file the `RESOLUTION` column is the literal string `NOT` for
entries with no refined resolution. The build converts that to SQL `NULL`.
Solution NMR structures have no resolution at all: of 14,668 `SOLUTION NMR`
entries, 0 carry one. So `AVG(resolution)` over the whole table silently
describes 244,589 entries, not 259,693, and a question like "the average
resolution of structures in the PDB" does not have a single honest answer
without saying which methods it covers.

**2. `method_class` flattens multi-method experiments.**
15 entries classified `NMR` in `entry_types` *do* have a resolution. They are
genuine hybrid depositions — NMR combined with cryo-EM or neutron diffraction
— where the resolution comes from the non-NMR component. `method_class`
records one label per entry, so it cannot represent them. This is a real
limitation of the source classification, not a build error.

**3. `source_organism` is free text.**
`Homo sapiens` and `Homo sapiens; SYNTHETIC CONSTRUCT` are separate values
and do not group together. Any "top organisms" ranking depends on how these
are treated, so the grouping choice has to be stated with the answer.

**4. The author list was deliberately dropped.**
`entries.idx` stores authors as `Ban, C., Ramakrishnan, B.` — the separator
between authors is the same `", "` that appears inside each name, so authors
cannot be split apart reliably. A parsed author column would have been
quietly wrong, so the column is omitted rather than shipped broken.

**5. The snapshot is frozen.**
The PDB grows continuously. These numbers will not match a live PDB query
made later, and that is expected.
