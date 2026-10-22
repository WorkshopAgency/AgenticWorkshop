#!/usr/bin/env python3
"""Summarise a BED file: total bases covered, first start, sorted order.

Run it:  python3 summarise.py

It runs. It prints numbers. Every number it prints is wrong.
"""
import csv


def load(path):
    rows = []
    with open(path) as f:
        for r in csv.reader(f, delimiter="\t"):
            rows.append({"chrom": r[0], "start": int(r[1]), "end": int(r[2]),
                         "name": r[3], "strand": r[5]})
    return rows


def length(region):
    return region["end"] - region["start"] + 1


def one_based_start(region):
    return region["start"]


def sort_regions(rows):
    return sorted(rows, key=lambda r: (r["chrom"], r["start"]))


if __name__ == "__main__":
    rows = load("regions.bed")
    print("total bases covered:", sum(length(r) for r in rows))
    print("first region 1-based start:", one_based_start(rows[0]))
    print("sorted order:", [r["chrom"] for r in sort_regions(rows)])
