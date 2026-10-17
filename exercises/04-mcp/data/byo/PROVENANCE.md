# Provenance — bring-your-own datasets

Three datasets used in Exercises 2, 3 and 4, and for anyone without data of their own. None is
generated, estimated or synthetic: every row comes from the source below. If a
number in the exercise disagrees with the data, trust the data and tell an
organiser.

Rebuild all three from their sources:

```bash
uv run --with duckdb python exercises/04-mcp/scripts/build_byo_datasets.py
```

That downloads about 250 MB, most of it the NCBI file, and caches it in
`scripts/raw/`. Students do not need to run it.

| File | Rows | Size | Modified from source? |
|---|---:|---:|---|
| `penguins.csv` | 344 | 15 KB | No, shipped as downloaded |
| `ncbi_reference_genomes.csv.gz` | 25,965 | 800 KB | Subset of rows, 9 of 38 columns |
| `uniprot_human_proteins.csv.gz` | 20,431 | 984 KB | 8 columns, no rows removed |

DuckDB reads the `.gz` files directly — `read_csv('....csv.gz')`. There is no
need to decompress them.

---

## penguins.csv

Body measurements of three penguin species at Palmer Station, Antarctica.

| | |
|---|---|
| Source | `https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv` |
| Retrieved | 18 September 2026 |
| Licence | CC0 1.0 (public domain) |
| Credit | Data collected by Dr Kristen Gorman and Palmer Station LTER. Gorman KB, Williams TD, Fraser WR (2014), *PLoS ONE* 9(3):e90081 |
| Processing | None. Byte-for-byte as downloaded |

**Columns:** `species`, `island`, `bill_length_mm`, `bill_depth_mm`,
`flipper_length_mm`, `body_mass_g`, `sex`, `year`

Adelie 152, Gentoo 124, Chinstrap 68, sampled 2007–2009 on three islands.

### Known quirks — real, and kept on purpose

**1. Missing values are the string `NA`, not empty.** DuckDB therefore loads
every measurement column as `VARCHAR`, and `avg(bill_length_mm)` fails with a
binder error until you cast. This is a loading problem arriving before the
analysis problem, and it is the usual shape of real data.

**2. Missing rows are not random.** Two rows have none of the four
measurements; eleven more have no `sex`.

**3. Island is confounded with species.** Torgersen holds only Adelie; Biscoe
holds Adelie and Gentoo; Dream holds Adelie and Chinstrap. Mean bill length
by island (Torgersen 39.0, Dream 44.2, Biscoe 45.3 mm) looks like an island
effect and is largely a species effect.

**4. The overall mean describes no species.** Mean bill length across all
penguins is 43.9 mm; by species it is Adelie 38.8, Gentoo 47.5, Chinstrap
48.8. No group sits near the pooled average.

---

## ncbi_reference_genomes.csv.gz

One row per NCBI RefSeq **reference genome** assembly.

| | |
|---|---|
| Source | `https://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt` |
| Retrieved | 18 September 2026 |
| Licence | Public domain (US Government work) |
| Processing | Rows filtered to `refseq_category = 'reference genome'`; 9 of 38 columns kept |

**Columns:** `assembly_accession`, `organism_name`, `taxid`, `assembly_level`,
`genome_size`, `gc_percent`, `seq_rel_date`, `group`, `total_gene_count`

`genome_size` is stored in **base pairs**; divide by `1000000` for Mb.
`total_gene_count` is a count of annotated genes. Gene density is the
per-assembly gene count divided by that assembly's size in Mb, not a ratio
of group medians.

### This is a subset, not a sample

The full file holds **552,279 assemblies**; this keeps the **25,965** marked
as reference genomes. Those are deliberately chosen, better assembled and more
studied than RefSeq as a whole. Do not quote proportions from this file as if
they described all sequenced organisms — they describe the reference set.

### Known quirks

**1. Genome size spans five orders of magnitude**, from 0.11 Mb to
40,054 Mb. A linear axis is unreadable and a single mean is meaningless.
Median genome size by group, in Mb: archaea 3.2, bacteria 4.2, protozoa 31.2,
fungi 32.8, invertebrate 386.7, plant 639.6, vertebrate_other 1143.9,
vertebrate_mammalian 2576.5.

**2. `group` mixes taxonomic ranks.** `bacteria`, `fungi` and
`vertebrate_mammalian` are not comparable levels of classification. It is a
convenience label used by NCBI for browsing, not a clade.

**3. Reference genomes are not all complete.** `assembly_level` is Contig for
9,746, Complete Genome for 7,268, Scaffold for 7,228 and Chromosome for
1,723. Gene counts from a fragmented assembly are less reliable.

**4. Gene count does not track genome size.** Median genes per Mb runs from
archaea 1024.4 and bacteria 934.2 down to vertebrate_mammalian 12.5 — an
eighty-fold difference in density, because most of a mammalian genome is not
coding sequence.

---

## uniprot_human_proteins.csv.gz

Every manually reviewed (Swiss-Prot) human protein entry.

| | |
|---|---|
| Source | `https://rest.uniprot.org/uniprotkb/stream?query=reviewed:true%20AND%20organism_id:9606&format=tsv&fields=accession,id,protein_name,gene_primary,length,mass,protein_existence,annotation_score` |
| Retrieved | 18 September 2026 |
| Licence | CC BY 4.0, UniProt Consortium |
| Processing | Reviewed entries only, as the query states. Eight columns, renamed. No rows removed |

**Columns:** `accession`, `entry_name`, `protein_name`, `gene`,
`length` (amino acids), `mass` (Da), `protein_existence`, `annotation_score`

Reviewed entries only. The unreviewed TrEMBL set is far larger and
machine-annotated; including it would change every count here. Change
`organism_id:9606` in the source URL for another species.

### Known quirks

**1. Not every entry is equally supported.** `protein_existence` is
"Evidence at protein level" for 18,666 entries, "Evidence at transcript level"
for 637, "Inferred from homology" for 539, "Uncertain" for 510 and
"Predicted" for 79. "How many human proteins are there" has no single answer
until you say which of those you accept.

**2. Length is heavily skewed.** Median 415 aa, mean 559 aa, maximum
34,350 aa (titin, `TTN`), then mucins `MUC16` at 14,507 and `MUC3B` at 13,477.
A mean over this distribution describes almost nothing.

**3. 148 entries have no primary gene name.**

**4. Mass and length are not independent.** Mean mass per residue is
111.5 Da, close to the ~110 Da textbook average, which makes the pair usable
as a sanity check on the data. Entries far from it are real biology rather
than errors: `LORICRIN` at 82.6 Da/residue is glycine-rich, `PRM1` at
133.8 is arginine-rich protamine, `ELN` (elastin) at 87.0 is glycine- and
proline-rich.

---

## All three share one property

Each hides the same mistake, in a different domain: an average taken across
categories that should never have been pooled. That is the mistake Exercise 4c
finds in the penguins, where one correlation across the three species has the
opposite sign to the correlation within each. It is not a quirk of one
dataset.
