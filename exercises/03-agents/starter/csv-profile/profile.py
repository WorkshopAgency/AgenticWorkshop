#!/usr/bin/env python3
"""Profile a CSV or CSV.GZ file: rows, columns, types, missing values, groups.

Standard library only. Usage:

    python3 profile.py data.csv.gz [--group COLUMN] [--out report.md]
"""
import argparse
import csv
import gzip
import os
import sys
from collections import Counter

MARKERS = {"NA", "N/A", "NaN", "nan", "null", "NULL", "None", "-", "?"}


def open_table(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", newline="")
    return open(path, newline="")


def kind(value):
    """Classify one non-missing cell as int, float or text."""
    try:
        int(value)
        return "int"
    except ValueError:
        pass
    try:
        float(value)
        return "float"
    except ValueError:
        return "text"


def column_type(kinds, markers):
    """Summarise a column from the kinds of its non-missing cells."""
    if not kinds:
        return "empty"
    if set(kinds) <= {"int"}:
        base = "integer"
    elif set(kinds) <= {"int", "float"}:
        base = "number"
    else:
        return "text"
    return f"{base} (read as text by tools that treat {', '.join(sorted(markers))} as text)" if markers else base


def profile(path, group):
    with open_table(path) as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        if group and group not in columns:
            sys.exit(f"Column '{group}' is not in {path}. Columns: {', '.join(columns)}")
        empty = Counter()
        markers = {c: Counter() for c in columns}
        kinds = {c: Counter() for c in columns}
        groups = Counter()
        rows = 0
        for row in reader:
            rows += 1
            for c in columns:
                v = (row.get(c) or "").strip()
                if v == "":
                    empty[c] += 1
                elif v in MARKERS:
                    markers[c][v] += 1
                else:
                    kinds[c][kind(v)] += 1
            if group:
                groups[(row.get(group) or "").strip() or "(empty)"] += 1
    return columns, rows, empty, markers, kinds, groups


def report(path, group, columns, rows, empty, markers, kinds, groups):
    lines = [f"# Profile of `{os.path.basename(path)}`", "",
             f"- Rows: **{rows:,}**", f"- Columns: **{len(columns)}**", "",
             "| Column | Type | Empty | Text markers |", "|---|---|---:|---|"]
    for c in columns:
        found = ", ".join(f"`{m}` ×{n}" for m, n in markers[c].most_common()) or "-"
        lines.append(f"| {c} | {column_type(kinds[c], markers[c])} | {empty[c]} | {found} |")
    if group:
        lines += ["", f"## Counts per `{group}`", "", f"| {group} | Rows |", "|---|---:|"]
        lines += [f"| {g} | {n:,} |" for g, n in groups.most_common()]
    lines += ["", "Units and meanings are not inferred. Check the provenance file next to the data."]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("file")
    p.add_argument("--group", help="column to count rows by")
    p.add_argument("--out", help="also write the report to this Markdown file")
    a = p.parse_args()
    if not os.path.isfile(a.file):
        sys.exit(f"File not found: {a.file}")
    try:
        text = report(a.file, a.group, *profile(a.file, a.group))
    except (csv.Error, UnicodeDecodeError, OSError) as e:
        sys.exit(f"Could not parse {a.file} as CSV: {e}")
    print(text)
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w") as f:
            f.write(text + "\n")
        print(f"\nWrote {a.out}")


if __name__ == "__main__":
    main()
