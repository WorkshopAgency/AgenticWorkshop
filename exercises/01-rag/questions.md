# Questions and answers

The documents in `corpus/` are the nf-core/rnaseq 3.27.0 usage and output
guides and the 2025–2026 changelog. Release 3.27.0 came out on 23 September
2026.

Try the questions first; read the answers afterwards. The last column is a
phrase you can `grep` for in `corpus/`.

| # | Question | Answer | Where |
|---|---|---|---|
| 1 | When strandedness is set to `auto`, how does nf-core/rnaseq decide, and with which default thresholds? | It sub-samples each sample to 1 million reads, infers strandedness with Salmon, and uses `--stranded_threshold` 0.8 and `--unstranded_threshold` 0.1 | `usage.md`, `sub-sample the input FastQ files` |
| 2 | Which tools does `--use_rustqc` replace, and which option can it not be combined with? | dupRadar, featureCounts biotype QC, RSeQC, Preseq, Qualimap and SAMtools stats/flagstat/idxstats. It cannot be combined with `--skip_markduplicates` | `usage.md`, `RustQC replaces`; `changelog-2025-2026.md`, `PR #1869` |
| 3 | What is the default SortMeRNA database? | `smr_v4.3_fast_db`, a SILVA 138 and Rfam build of about 17 MB | `usage.md`, `smr_v4.3_fast_db` |
| 4 | Which Salmon version does release 3.27.0 use, and what changed in quantification? | 2.7.0; it was 1.10.3 before. The changelog warns that the new version shifts gene-level quantification ("double-digit-percent TPM/FPKM swings") | `changelog-2025-2026.md`, `double-digit-percent` |
| 5 | What is the minimum sequencing depth per sample that nf-core/rnaseq recommends? | Not in the documents | — |

For question 4 the old and the new version sit side by side in one table
row, so read carefully which is which. Question 5 has no answer in the
documents.
