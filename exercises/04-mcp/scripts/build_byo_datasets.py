#!/usr/bin/env python3
"""Build the three bring-your-own-data sets in exercises/04-mcp/data/byo/.

Rebuild:
    uv run --with "duckdb<2" python exercises/04-mcp/scripts/build_byo_datasets.py

Downloads three public datasets, trims them, and writes:

    penguins.csv                   344 rows, unmodified
    ncbi_reference_genomes.csv.gz  25,965 rows, subset and trimmed
    uniprot_human_proteins.csv.gz  20,431 rows, trimmed

Students do not need to run this; the built files are shipped. Sources,
licences and processing steps are recorded in data/byo/PROVENANCE.md.

The NCBI download is 240 MB and is cached in scripts/raw/ so a rerun does
not fetch it again. Pass --force to rebuild outputs that already exist.
"""
import csv
import gzip
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(os.path.dirname(HERE), "data", "byo")

PENGUINS_URL = ("https://raw.githubusercontent.com/allisonhorst/palmerpenguins/"
                "main/inst/extdata/penguins.csv")
NCBI_URL = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt"
UNIPROT_URL = ("https://rest.uniprot.org/uniprotkb/stream"
               "?query=reviewed:true%20AND%20organism_id:9606&format=tsv"
               "&fields=accession,id,protein_name,gene_primary,length,mass,"
               "protein_existence,annotation_score")

# Nine of the assembly summary's 38 columns.
NCBI_COLUMNS = ["assembly_accession", "organism_name", "taxid", "assembly_level",
                "genome_size", "gc_percent", "seq_rel_date", "group",
                "total_gene_count"]

# UniProt's TSV headers, and the names we give them.
UNIPROT_COLUMNS = [
    ("Entry", "accession"),
    ("Entry Name", "entry_name"),
    ("Protein names", "protein_name"),
    ("Gene Names (primary)", "gene"),
    ("Length", "length"),
    ("Mass", "mass"),
    ("Protein existence", "protein_existence"),
    ("Annotation", "annotation_score"),
]

FORCE = "--force" in sys.argv


def fetch(url, name):
    """Download into scripts/raw/, reusing the file if it is already there."""
    os.makedirs(RAW, exist_ok=True)
    dest = os.path.join(RAW, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"  cached   {name} ({os.path.getsize(dest) / 1048576:.1f} MB)")
        return dest
    print(f"  download {name} ...")
    urllib.request.urlretrieve(url, dest)
    print(f"           {os.path.getsize(dest) / 1048576:.1f} MB")
    return dest


def skip(path):
    if os.path.exists(path) and not FORCE:
        print(f"  exists   {os.path.basename(path)} (pass --force to rebuild)")
        return True
    return False


def build_penguins():
    out = os.path.join(OUT, "penguins.csv")
    if skip(out):
        return
    src = fetch(PENGUINS_URL, "penguins.csv")
    with open(src, "rb") as f_in, open(out, "wb") as f_out:
        f_out.write(f_in.read())          # shipped unmodified
    with open(out) as f:
        n = sum(1 for _ in f) - 1
    print(f"  wrote    penguins.csv  {n:,} rows, unmodified")


def build_ncbi():
    out = os.path.join(OUT, "ncbi_reference_genomes.csv.gz")
    if skip(out):
        return
    src = fetch(NCBI_URL, "assembly_summary_refseq.txt")
    header, kept, total = None, 0, 0
    with open(src, encoding="utf-8", errors="replace") as f, \
            gzip.open(out, "wt", newline="", encoding="utf-8") as g:
        w = csv.DictWriter(g, fieldnames=NCBI_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for line in f:
            if line.startswith("#assembly_accession"):
                header = line[1:].rstrip("\n").split("\t")
                continue
            if line.startswith("#") or header is None:
                continue
            total += 1
            row = dict(zip(header, line.rstrip("\n").split("\t")))
            # Reference genomes only: better assembled and more studied than
            # RefSeq as a whole. A subset, not a sample -- see PROVENANCE.md.
            if row.get("refseq_category") != "reference genome":
                continue
            w.writerow(row)
            kept += 1
    print(f"  wrote    ncbi_reference_genomes.csv.gz  {kept:,} of {total:,} assemblies")


def build_uniprot():
    out = os.path.join(OUT, "uniprot_human_proteins.csv.gz")
    if skip(out):
        return
    src = fetch(UNIPROT_URL, "uniprot_human_reviewed.tsv")
    with open(src, encoding="utf-8", errors="replace", newline="") as f, \
            gzip.open(out, "wt", newline="", encoding="utf-8") as g:
        r = csv.DictReader(f, delimiter="\t")
        w = csv.writer(g)
        w.writerow([new for _, new in UNIPROT_COLUMNS])
        n = 0
        for row in r:
            w.writerow([row.get(old, "") for old, _ in UNIPROT_COLUMNS])
            n += 1
    print(f"  wrote    uniprot_human_proteins.csv.gz  {n:,} rows")


def report():
    print("\n--- built ---")
    for name in ("penguins.csv", "ncbi_reference_genomes.csv.gz",
                 "uniprot_human_proteins.csv.gz"):
        p = os.path.join(OUT, name)
        if os.path.exists(p):
            size = os.path.getsize(p)
            unit = f"{size / 1048576:.2f} MB" if size > 1048576 else f"{size / 1024:.0f} KB"
            print(f"  {name:34} {unit}")
    print("\nDuckDB reads the .gz files directly: read_csv('....csv.gz')")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_penguins()
    build_ncbi()
    build_uniprot()
    report()
