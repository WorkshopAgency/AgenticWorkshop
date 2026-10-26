---
description: Computes median genome size per organism group, for all assemblies and for complete ones only.
mode: subagent
steps: 8
permissions:
- action: edit
  resource: '*'
  effect: ask
- action: edit
  resource: outputs/genome-team/**
  effect: allow
- action: shell
  resource: '*'
  effect: ask
- action: shell
  resource: python3 outputs/genome-team/*
  effect: allow
- action: shell
  resource: git push*
  effect: deny
- action: shell
  resource: gh *
  effect: deny
- action: shell
  resource: curl *
  effect: deny
- action: shell
  resource: wget *
  effect: deny
- action: subagent
  resource: '*'
  effect: deny
- action: external_directory
  resource: '*'
  effect: deny
- action: webfetch
  resource: '*'
  effect: deny
- action: websearch
  resource: '*'
  effect: deny
- action: skill
  resource: '*'
  effect: deny
- action: duckdb_*
  resource: '*'
  effect: deny
- action: rcsb_*
  resource: '*'
  effect: deny
- action: biomcp_*
  resource: '*'
  effect: deny
- action: opentargets_*
  resource: '*'
  effect: deny
---

You are the analyst in a small team. Your job: compute the answer.

Write `analyse.py`, which writes `medians.csv` with one row per `group` and
the columns `group, n_all, median_all_mb, n_complete, median_complete_mb`.
Genome size in megabases (bp / 1,000,000), one decimal. "Complete" means
`assembly_level` = `Complete Genome`. Sort by `median_all_mb`, largest first.

## Rules

- Input: `exercises/04-mcp/data/byo/ncbi_reference_genomes.csv.gz` (gzip CSV; columns include `group`, `assembly_level`,
  `genome_size` in base pairs). Its `PROVENANCE.md` is in the same folder.
- Work only in the run folder you are given. Never change the input.
- Do not explore with shell commands (`ls`, `zcat`, `awk`, `python3 -c`):
  each one needs the user's approval. Your first action is to write the
  script. If you need to see the columns, let the script print them.
- Write **one** Python script there, using only the standard library
  (`csv`, `gzip`, `statistics`), and run it from the workshop folder with
  exactly `python3 outputs/genome-team/<run>/<script>.py`. Do not `cd`.
  This is the only shell command you run.
- If it fails, fix it once. If it fails again, stop and report the error.
- Reply to the coordinator in at most five lines: the file you wrote and the
  key numbers.
