## [[3.27.0](https://github.com/nf-core/rnaseq/releases/tag/3.27.0)] - 2026-09-23

### Credits

Special thanks to the following for their contributions to the release:

- [Adam Talbot](https://github.com/adamrtalbot)
- [apeleraux](https://github.com/apeleraux)
- [Daniel Lundin](https://github.com/erikrikarddaniel)
- [Davide Bressan](https://github.com/DavideBrex)
- [dawnmy](https://github.com/dawnmy)
- [Dmytro Hlushchenko](https://github.com/CloudCurio)
- [EladH1](https://github.com/EladH1)
- [emmanuel-tan](https://github.com/emmanuel-tan)
- [Evangelos Karatzas](https://github.com/vagkaratzas)
- [Felix Krueger](https://github.com/FelixKrueger)
- [Friederike Hanssen](https://github.com/FriederikeHanssen)
- [Gary Burnett](https://github.com/gburnett-nvidia)
- [Ido Tamir](https://github.com/idot)
- [Jose Espinosa-Carrasco](https://github.com/JoseEspinosa)
- [Joseph Longworth](https://github.com/JosephLongworth)
- [Luisa Santus](https://github.com/luisas)
- [Mahesh Binzer-Panchal](https://github.com/mahesh-panchal)
- [Matthias Hörtenhuber](https://github.com/mashehu)
- [Matthias Zepper](https://github.com/MatthiasZepper)
- [Maxime U Garcia](https://github.com/maxulysse)
- [murphyte](https://github.com/murphyte)
- [mvheetve](https://github.com/mvheetve)
- [Paolo Inglese](https://github.com/piplus2)
- [Phil Ewels](https://github.com/ewels)

### Enhancements and fixes

- [PR #1421](https://github.com/nf-core/rnaseq/pull/1421) - Accept purely numeric sample IDs in `assets/schema_input.json` and coerce `meta.id` to `String` after `samplesheetToList` ([#1419](https://github.com/nf-core/rnaseq/issues/1419))
- [PR #1680](https://github.com/nf-core/rnaseq/pull/1680) - Raise the Nextflow floor to 25.10.4 across `nextflow.config`, the three `nf-test*` workflow matrices, and the README/ro-crate version badges; bump `nf-schema` to 2.6.1; clear the v2-parser lint warnings in local subworkflows and resync six nf-core components carrying upstream-merged strict-syntax fixes
- [PR #1775](https://github.com/nf-core/rnaseq/pull/1775) - Add Parabricks resource configuration guide for full-size genomes (GPU count, memory scaling, retry strategy, `--low-memory` flag)
- [PR #1844](https://github.com/nf-core/rnaseq/pull/1844) - Bump version to 3.27.0dev after release 3.26.0; flip the MultiQC report links and RO-Crate URL/version back to dev
- [PR #1848](https://github.com/nf-core/rnaseq/pull/1848) - Align `actions/checkout` SHA in `nf-test-arm.yml` and `nf-test-gpu.yml` with the template-derived `nf-test.yml` (`v6`) ([#1847](https://github.com/nf-core/rnaseq/issues/1847))
- [PR #1849](https://github.com/nf-core/rnaseq/pull/1849) - Tidy-up batch addressing [#1845](https://github.com/nf-core/rnaseq/issues/1845): README/schema clarifications, `&` → `&&` in three guards, deduplicated `withName` blocks, and removal of the unmaintained `bin/fastq_dir_to_samplesheet.py` (use [nf-core/fetchngs](https://nf-co.re/fetchngs) for samplesheet generation)
- [PR #1850](https://github.com/nf-core/rnaseq/pull/1850) - Use the active aligner's display name in the MultiQC `fail_mapped` per-sample status row, and drop the hardcoded "STAR" reference from the pipeline-completion `min_mapped_reads` warning, so Bowtie2 reports no longer mislabel the metric as STAR ([#1846](https://github.com/nf-core/rnaseq/issues/1846))
- [PR #1851](https://github.com/nf-core/rnaseq/pull/1851) - Split `PREPARE_GENOME` into `PREPARE_GENOME_REFERENCES` (FASTA / GTF / BED / transcript FASTA / chrom.sizes / rRNA / Kraken DB) and `PREPARE_GENOME_INDICES` (per-aligner index build/load) for clearer ownership; no user-facing parameter, output, or behaviour change ([#1721](https://github.com/nf-core/rnaseq/issues/1721)).
- [PR #1852](https://github.com/nf-core/rnaseq/pull/1852) - Flatten `workflows/rnaseq/assets/` back to top-level `assets/` so `nf-core pipelines bump-version` finds `assets/multiqc_config.yml` and updates the report-comment URLs automatically on release bumps
- [PR #1853](https://github.com/nf-core/rnaseq/pull/1853) - Replace remaining pre-admonition `> **NB:**` / `> **Note**` / `> **Warning**` quoteblocks across `docs/usage.md`, `docs/output.md`, and `README.md` with nf-core flavored `:::note` / `:::warning` admonitions
- [PR #1854](https://github.com/nf-core/rnaseq/pull/1854) - Switch the `SORTMERNA` ARM container in `conf/arm.config` to a Wave build from `bioconda::sortmerna=4.3.7`, retiring the last `seqera::` channel reference in the pipeline ([#1431](https://github.com/nf-core/rnaseq/issues/1431))
- [PR #1861](https://github.com/nf-core/rnaseq/pull/1861) - Drop the outdated RiboDetector ONNX multiprocessing hang warnings from `docs/usage.md`, `docs/output.md`, and the `ribo_removal_tool` schema help text, resolved upstream in the pinned `ribodetector=0.3.3` ([#1856](https://github.com/nf-core/rnaseq/issues/1856))
- [PR #1862](https://github.com/nf-core/rnaseq/pull/1862) - Correct the `docs/usage.md` note to state that `--extra_star_align_args` applies to `--aligner star_rsem`, since STAR runs as a standalone step and RSEM quantifies the resulting BAM ([#1857](https://github.com/nf-core/rnaseq/issues/1857))
- [PR #1864](https://github.com/nf-core/rnaseq/pull/1864) - Bump nf-schema to 2.7.2, fixing boolean CLI parameter validation failures under Nextflow 26.x strict syntax ([#1860](https://github.com/nf-core/rnaseq/issues/1860))
- [PR #1869](https://github.com/nf-core/rnaseq/pull/1869) - Add pipeline validation error when `--use_rustqc` and `--skip_markduplicates` are set together, since RustQC requires duplicate-marked BAM files ([#1865](https://github.com/nf-core/rnaseq/issues/1865))
- [PR #1878](https://github.com/nf-core/rnaseq/pull/1878) - Add `trim_only` and `raw` options to `--contaminant_screening_input`: `trim_only` screens reads after adapter trimming but before BBSplit/rRNA removal, enabling detection of contaminants that a species-limited BBSplit index would otherwise discard; `raw` screens pre-trimming reads as a baseline ([#1870](https://github.com/nf-core/rnaseq/issues/1870))
- [PR #1882](https://github.com/nf-core/rnaseq/pull/1882) - Pass `--skip-dup-check` to RustQC when `--with_umi` is set, so `--use_rustqc` works with UMI-deduplicated BAMs: UMICollapse / UMI-tools physically remove PCR duplicates, leaving no reads flagged `0x400`, so duplication QC is not applicable and RustQC's duplicate-marking check would otherwise abort the run ([#1881](https://github.com/nf-core/rnaseq/issues/1881))
- [PR #1883](https://github.com/nf-core/rnaseq/pull/1883) - Update the `tximeta/tximport` module ([nf-core/modules#12362](https://github.com/nf-core/modules/pull/12362)): add a `jq` build dependency and set `LC_COLLATE=C` for reproducible gene-level output ordering
- [PR #1884](https://github.com/nf-core/rnaseq/pull/1884) - Update `trimgalore` module to 2.3.0
- [PR #1885](https://github.com/nf-core/rnaseq/pull/1885) - Bump `quant_tximport_summarizedexperiment` and `quantify_rsem` ([nf-core/modules#12377](https://github.com/nf-core/modules/pull/12377)): sort the collected per-sample inputs to `TXIMETA_TXIMPORT` and `CUSTOM_RSEMMERGECOUNTS` by staged file name, keeping their cache keys stable across `-resume` instead of following non-deterministic task-completion order ([#1879](https://github.com/nf-core/rnaseq/issues/1879))
- [PR #1892](https://github.com/nf-core/rnaseq/pull/1892) - Support a pre-built Bowtie2 index for rRNA removal via `--bowtie2_rrna_index`, skipping on-the-fly index construction from `--ribo_database_manifest` when one is supplied ([#1731](https://github.com/nf-core/rnaseq/issues/1731))
- [PR #1894](https://github.com/nf-core/rnaseq/pull/1894) - Important! Template update for nf-core/tools v4.0.3
- [PR #1899](https://github.com/nf-core/rnaseq/pull/1899) - Update GPU based STAR (Parabricks rna_fq2bam) to version 4.7.1.
- [PR #1902](https://github.com/nf-core/rnaseq/pull/1902) - Update `bam_stringtie_merge` and StringTie modules ([nf-core/modules#12661](https://github.com/nf-core/modules/pull/12661)), allowing runs where all samples fail `--min_mapped_reads` to complete with skipped-sample warnings instead of failing an empty StringTie merge ([#1901](https://github.com/nf-core/rnaseq/issues/1901))
- [PR #1905](https://github.com/nf-core/rnaseq/pull/1905) - Give `TRIMGALORE` an explicit 4 GB memory allocation, replacing the `process_low_memory` label's 1 GB budget that paired with an 8-cpu band and OOM-killed every sample on every retry ([#1903](https://github.com/nf-core/rnaseq/issues/1903))
- [PR #1907](https://github.com/nf-core/rnaseq/pull/1907) - Update `fastq_qc_trim_filter_setstrandedness` ([nf-core/modules#12745](https://github.com/nf-core/modules/pull/12745)), fixing a crash in Salmon auto-strandedness inference when no `--fasta` is supplied (e.g. kallisto-only pseudoalignment runs)
- [PR #1911](https://github.com/nf-core/rnaseq/pull/1911) - Copy instead of symlink index files in `STAR_GENOMEPARAMS_UPGRADE`, fixing broken/missing index files on object-storage-backed work directories (e.g. Azure Batch via azcopy) that can't represent symlinks
- [PR #1913](https://github.com/nf-core/rnaseq/pull/1913) - Update HISAT2 modules; add `--extra_hisat2_align_args` ([#1916](https://github.com/nf-core/rnaseq/issues/1916))
- [PR #1914](https://github.com/nf-core/rnaseq/pull/1914) - Important! Template update for nf-core/tools v4.1.0
- [PR #1915](https://github.com/nf-core/rnaseq/pull/1915) - Add `manifest.diagram` to `nextflow.config`, pointing at the metro map, and wire up process names for `nf-metro serve` live-progress tracking
- [PR #1917](https://github.com/nf-core/rnaseq/pull/1917) - Update `trimgalore` module ([nf-core/modules#12978](https://github.com/nf-core/modules/pull/12978)), dropping the now-redundant `process_low_memory` label
- [PR #1918](https://github.com/nf-core/rnaseq/pull/1918) - Update all nf-core modules and subworkflows to latest upstream
- [PR #1919](https://github.com/nf-core/rnaseq/pull/1919) - Skip biotype QC with a warning instead of crashing when the biotype attribute is absent on the GTF rows featureCounts reads (e.g. NCBI annotations, which only set it on `gene` rows) ([#1886](https://github.com/nf-core/rnaseq/issues/1886))
- [PR #1922](https://github.com/nf-core/rnaseq/pull/1922) - Document `--extra_star_align_args '--alignMatesGapMax <value>'` for users who opt into STAR on prokaryotic data, since STAR's default mate-gap ceiling is far larger than a bacterial genome calls for ([#1691](https://github.com/nf-core/rnaseq/issues/1691))
- [PR #1923](https://github.com/nf-core/rnaseq/pull/1923) - Add `--extra_salmon_index_args`, letting users pass `--keepDuplicates` (or other Salmon index flags) without changing the pipeline default of dropping exact-sequence-duplicate transcripts ([#1259](https://github.com/nf-core/rnaseq/issues/1259))
- [PR #1924](https://github.com/nf-core/rnaseq/pull/1924) - Restore StringTie's `--fr`/`--rf` strandedness flags, dropped by the v3 module update ([PR #1902](https://github.com/nf-core/rnaseq/pull/1902)) with no replacement
- [PR #1925](https://github.com/nf-core/rnaseq/pull/1925) - Trigger a full nf-test run on `conf/`, `bin/` and `assets/` changes, and refresh the StringTie ballgown snapshots left stale by [PR #1924](https://github.com/nf-core/rnaseq/pull/1924)
- [PR #1927](https://github.com/nf-core/rnaseq/pull/1927) - Bump version to 3.27.0 ahead of release, with a Salmon `--libType` config fix/dedup and an nf-test trigger fix picked up along the way
- [PR #1930](https://github.com/nf-core/rnaseq/pull/1930) - Fill in `fastp`/`multiqc`/`seqkit` gaps in the Software dependencies table and add `tests/.nftignore_rustqc` to nf-test triggers, following release review

### Software dependencies

| Dependency    | Old version | New version |
| ------------- | ----------- | ----------- |
| `fastp`       | 1.0.1       | 1.3.6       |
| `hisat2`      | 2.2.1       | 2.2.3       |
| `kallisto`    | 0.51.1      | 0.52.0      |
| `multiqc`     | 1.33        | 1.35        |
| `picard`      | 3.4.0       | 3.5.0       |
| `python`      | 3.9.5       | 3.14.5      |
| `salmon`      | 1.10.3      | 2.7.0       |
| `samtools`    | 1.23.1      | 1.24        |
| `seqkit`      | 2.9.0       | 2.13.0      |
| `stringtie`   | 2.2.3       | 3.0.3       |
| `subread`     | 2.0.6       | 2.1.1       |
| `trim-galore` | 2.1.0       | 2.3.0       |
| `ucsc-tools`  | 377/469     | 482         |

`salmon` and `stringtie`'s major-version bumps measurably shift gene-level quantification on the standard test dataset (double-digit-percent TPM/FPKM swings and some detected/undetected flips for low-to-moderate expression genes), while STAR alignment and library-type inference are unaffected; overall alignment-rate-style QC metrics move by fractions of a percent. Anyone diffing exact per-gene values against a pre-3.27.0 baseline should expect this.

## [[3.26.0](https://github.com/nf-core/rnaseq/releases/tag/3.26.0)] - 2026-05-07

### Credits

Special thanks to the following for their contributions to the release:

- [Daniel Lundin](https://github.com/erikrikarddaniel)
- [Edmund Miller](https://github.com/edmundmiller)
- [Felix Krueger](https://github.com/FelixKrueger)
- [Friederike Hanssen](https://github.com/FriederikeHanssen)
- [James A. Fellows Yates](https://github.com/jfy133)
- [Long Pan](https://github.com/LongpanICR)
- [Luisa Santus](https://github.com/luisas)
- [Matthias Hörtenhuber](https://github.com/mashehu)
- [Maxime U Garcia](https://github.com/maxulysse)
- [Phil Ewels](https://github.com/ewels)
- [Simon Pearce](https://github.com/SPPearce)
- [Thomas Danhorn](https://github.com/tdanhorn)

### Enhancements and fixes

- [PR #1789](https://github.com/nf-core/rnaseq/pull/1789) - Bump `trimgalore` module to 2.1.0 ([nf-core/modules#11524](https://github.com/nf-core/modules/pull/11524)); add ARM Wave container for the new pin in `conf/arm.config`
- [PR #1821](https://github.com/nf-core/rnaseq/pull/1821) - Bump version to 3.26.0dev after release 3.25.0; flip the MultiQC report links and RO-Crate URL/version back to dev
- [PR #1823](https://github.com/nf-core/rnaseq/pull/1823) - Reinstall `trimgalore` module to pull in [nf-core/modules#11308](https://github.com/nf-core/modules/pull/11308), which removes orphan `*_trimmed.fq.gz` outputs left in the workdir by an interrupted previous trim_galore attempt (e.g. AWS Batch retry after a Spot reclaim) that were breaking `FQ_LINT_AFTER_TRIMMING` ([#1807](https://github.com/nf-core/rnaseq/issues/1807))
- [PR #1824](https://github.com/nf-core/rnaseq/pull/1824) - Restore the #1821 entry to the changelog after it was dropped during 3.25.1 prep
- [PR #1826](https://github.com/nf-core/rnaseq/pull/1826) - Auto-merged template update for nf-core/tools v4.0.0, superseded by the v4.0.2 merge in #1827
- [PR #1827](https://github.com/nf-core/rnaseq/pull/1827) - Merge nf-core template v4.0.2
- [PR #1829](https://github.com/nf-core/rnaseq/pull/1829) - Disambiguate the three FastQC instances (raw / trimmed / filtered) in MultiQC General Statistics by suffixing each instance's column titles with `(raw)`, `(trim)` and `(filt)` ([#1828](https://github.com/nf-core/rnaseq/issues/1828))
- [PR #1831](https://github.com/nf-core/rnaseq/pull/1831) - Publish `*.merged.tx2gene_augmented.tsv` alongside the GTF-derived `*.merged.tx2gene.tsv`; this is the table actually consumed by `tximport` (input mappings plus self-mappings for orphan transcripts) and is required to reproduce the published gene-level outputs from the per-sample quantification files ([#1830](https://github.com/nf-core/rnaseq/issues/1830))
- [PR #1832](https://github.com/nf-core/rnaseq/pull/1832) - Suppress non-comparable `*gene_counts_length_scaled.tsv` outputs in `--skip_quantification_merge` mode ([#1822](https://github.com/nf-core/rnaseq/issues/1822))
- [PR #1834](https://github.com/nf-core/rnaseq/pull/1834) - Gate the legacy STAR 2.6.1d pin on a per-entry `star_legacy` flag so custom catalogues with modern indices skip it; rename the iGenomes-named scaffolding (`STAR_ALIGN_IGENOMES`, `use_igenomes_star`, `conf/igenomes_star.config`) to `legacy`-prefixed equivalents; sort the merged Strandedness checks MultiQC tables by sample id for deterministic md5
- [PR #1835](https://github.com/nf-core/rnaseq/pull/1835) - Drop the STAR 2.6.1d alignment pin in favour of a metadata-only upgrade adapter. Genome-map entries flagged `star_legacy = true` route through a new `STAR_GENOMEPARAMS_UPGRADE` process that rewrites the legacy `genomeParameters.txt` to the 2.7.4a schema, so stock STAR runs the modern build the pipeline ships; Sentieon and Parabricks STAR branches bypass the upgrade. Removes `STAR_ALIGN_LEGACY`, the parallel STAR 2.6.1d Wave/conda containers, `conf/legacy_star.config`, and the ARM-specific 2.6.1d override
- [PR #1836](https://github.com/nf-core/rnaseq/pull/1836) - Reinstall `trimgalore` module to pick up upstream label change (`process_high` → `process_medium` + `process_low_memory`); add the matching `process_low_memory` definition (1 GB) to `conf/base.config` per the nf-core/tools template
- [PR #1837](https://github.com/nf-core/rnaseq/pull/1837) - Bump version to 3.26.0 ahead of release
- [PR #1839](https://github.com/nf-core/rnaseq/pull/1839) - Address review feedback from #1838: condense the two large `strandCheckSummaryYaml` JSON snapshots in `multiqc_rnaseq` function tests to `.md5()`; add this Software dependencies subsection summarising tool version bumps in 3.26.0
- [PR #1840](https://github.com/nf-core/rnaseq/pull/1840) - Address further review feedback from #1838: lowercase `Channel.x` → `channel.x` in local test files and `workflows/rnaseq/main.nf`; pin `params.outdir` in the `PIPELINE_COMPLETION` test so Nextflow execution reports land in the nf-test sandbox instead of a literal `null/pipeline_info/` directory; populate the previously empty "Pipeline specific contribution guidelines" section in `docs/CONTRIBUTING.md` with rnaseq-specific notes (test profiles, CI skip env vars, `.nftignore`, snapshots, version-reporting topic, module configs)
- [PR #1841](https://github.com/nf-core/rnaseq/pull/1841) - Pin `TRIMGALORE` to 12 cpus on the rnaseq-side selector to restore `--cores 8` (paired) after the upstream label downgrade in #1836 dropped `task.cpus` to 6 and halved trim_galore throughput
- [PR #1842](https://github.com/nf-core/rnaseq/pull/1842) - Drop the `TRIMGALORE` override from 12 to 8 cpus (`--cores 4` paired); megatests on #1841 showed `--cores 8` only saturates ~2.78 cores effectively, so the lower allocation gives near-identical wall-clock at lower cost

### Software dependencies

| Dependency                             | Old version | New version |
| -------------------------------------- | ----------- | ----------- |
| `trim-galore`                          | 0.6.10      | 2.1.0       |
| `gawk`                                 |             | 5.3.1       |
| `STAR` (legacy)                        | 2.6.1d      |             |
| `hisat2/align`                         | 2.2.1       | 2.2.3       |
| `samtools` (hisat2/align)              | 1.20        | 1.24        |
| `hisat2/build`                         | 2.2.1       | 2.2.3       |
| `samtools` (hisat2/build)              | 1.20        |             |
| `hisat2/extractsplicesites`            | 2.2.1       | 2.2.3       |
| `samtools` (hisat2/extractsplicesites) | 1.20        | 1.24        |

`gawk` is added as a dependency of the new `STAR_GENOMEPARAMS_UPGRADE` local module. The `STAR` (legacy) row reflects removal of the parallel STAR 2.6.1d build that ran alongside the default aligner for legacy iGenomes indices; the pipeline-default STAR is unchanged.

## [[3.25.0](https://github.com/nf-core/rnaseq/releases/tag/3.25.0)] - 2026-04-24

### Credits

Special thanks to the following for their contributions to the release:

- [Friederike Hanssen](https://github.com/FriederikeHanssen)
- [James A. Fellows Yates](https://github.com/jfy133)
- [Justin Payeur](https://github.com/Odulhin)
- [Matthias Hörtenhuber](https://github.com/mashehu)
- [Maxime U Garcia](https://github.com/maxulysse)
- [Muhammad Imran](https://github.com/drimran87)
- [Phil Ewels](https://github.com/ewels)
- Weisheng Wu
- [@wzheng0520](https://github.com/wzheng0520)

### Enhancements and fixes

- [PR #1755](https://github.com/nf-core/rnaseq/pull/1755) - Restructure `--stringtie_ignore_gtf` into a three-stage assemble → merge → quantify workflow via the nf-core `bam_stringtie_merge` subworkflow, publishing `stringtie_merge.gtf` and per-sample `<sample>.denovo.transcripts.gtf`
- [PR #1781](https://github.com/nf-core/rnaseq/pull/1781) - Bump version to 3.25.0dev after release 3.24.0; fix SortMeRNA `%rRNA` appearing only under "Read 2" in MultiQC General Stats by using log filename for sample names instead of parsing paired-end read paths from log content
- [PR #1784](https://github.com/nf-core/rnaseq/pull/1784) - Replace local `gtf2bed` module with nf-core `ea-utils/gtf2bed` module
- [PR #1786](https://github.com/nf-core/rnaseq/pull/1786) - Replace local `bam_post_alignment_qc` subworkflow and `multiqc_custom_biotype` module with nf-core `bam_qc_rnaseq` subworkflow and `custom/multiqccustombiotype` module; update `dupradar` to topic-based version reporting
- [PR #1788](https://github.com/nf-core/rnaseq/pull/1788) - Centralize pipeline-specific module configs in `conf/modules/` following the nf-core/sarek pattern
- [PR #1790](https://github.com/nf-core/rnaseq/pull/1790) - Add `--use_gpu_ribodetector` parameter for GPU-accelerated rRNA removal with ribodetector; update ribodetector module to dual-container approach (x86 only); generalize GPU CI skip from `SKIP_PARABRICKS` to `SKIP_GPU`
- [PR #1792](https://github.com/nf-core/rnaseq/pull/1792) - Always emit a strand-agnostic `<sample>.bigWig`. **Breaking**: per-strand bigWigs are no longer emitted for unstranded libraries, where a `-strand +/-` split carries no biological meaning ([#1275](https://github.com/nf-core/rnaseq/issues/1275))
- [PR #1793](https://github.com/nf-core/rnaseq/pull/1793) - Scope MultiQC's `table_sample_merge` config to samplesheet paired-end IDs so samples with `_1`/`_2` suffixes (e.g. `foo_1`, `foo_2`) are no longer collapsed into a single `foo` row in General Statistics; factor MultiQC wiring into a new local `MULTIQC_RNASEQ` subworkflow
- [PR #1795](https://github.com/nf-core/rnaseq/pull/1795) - Bump `custom/multiqccustombiotype` to fail loudly when the featureCounts output exceeds `--max_biotypes` (default 100), catching misconfigured `--featurecounts_group_type` values that previously hung MultiQC ([#424](https://github.com/nf-core/rnaseq/issues/424))
- [PR #1796](https://github.com/nf-core/rnaseq/pull/1796) - Clarify prokaryotic profile docs: transcripts are extracted from all transcript-like features (CDS, tRNA, rRNA, tmRNA, ncRNA, etc.), not only CDS; CDS is only required for featureCounts biotype QC
- [PR #1799](https://github.com/nf-core/rnaseq/pull/1799) - Bump version to 3.25.0 ahead of release
- [PR #1803](https://github.com/nf-core/rnaseq/pull/1803) - Fix per-sample MultiQC hanging under `--skip_quantification_merge` by building the MultiQC input as a per-sample bundle, so each sample's report fires as soon as its own contributors arrive ([#1797](https://github.com/nf-core/rnaseq/issues/1797))
- [PR #1804](https://github.com/nf-core/rnaseq/pull/1804) - Skip StringTie by default in the `prokaryotic` profile, where reference-guided transcript assembly is not informative for bacterial/archaeal annotations
- [PR #1805](https://github.com/nf-core/rnaseq/pull/1805) - Add a new MultiQC "Strandedness checks" section whose table rows reflect which strandedness analyses actually ran for each sample; narrow the prokaryotic RSeQC skip to prokaryote-unsafe modules only
- [PR #1806](https://github.com/nf-core/rnaseq/pull/1806) - Raise Bowtie2 default `-k` from 1 to 200 for `--aligner bowtie2_salmon` so Salmon's EM has enough multi-mapping evidence to quantify small transcriptomes correctly
- [PR #1811](https://github.com/nf-core/rnaseq/pull/1811) - Update the default SortMeRNA rRNA database to `smr_v4.3_default_db` (SILVA 138) ([#1354](https://github.com/nf-core/rnaseq/issues/1354))
- [PR #1812](https://github.com/nf-core/rnaseq/pull/1812) - Dedupe redundant pipeline-level nf-test cases (fold `min_mapped_reads` into `skip_qc`; prune duplicate pseudo-alignment cases) without losing coverage
- [PR #1814](https://github.com/nf-core/rnaseq/pull/1814) - Sync nf-core components to the latest versions, migrate the remaining local `deseq2_qc` module to topic-based version reporting, and retire `ch_versions` plumbing now that all modules emit versions via topic
- [PR #1815](https://github.com/nf-core/rnaseq/pull/1815) - Gate the nf-test `cleanup` directive on `$CI` so pipeline-test work directories are retained on local reruns and only pruned in CI ([#1813](https://github.com/nf-core/rnaseq/issues/1813))
- [PR #1817](https://github.com/nf-core/rnaseq/pull/1817) - Derive the gene BED via `gffread --bed` on the prokaryotic path so RSeQC `infer_experiment` gets a usable reference; `ea-utils/gtf2bed` only emits BED rows for `exon` features and produced an empty BED from CDS-only prokaryotic annotations
- [PR #1818](https://github.com/nf-core/rnaseq/pull/1818) - Drop redundant `versions.yml` clauses from `saveAs` closures on processes that now emit versions via the `versions` topic; name closure parameters instead of implicit `it` in local workflow / subworkflow files
- [PR #1819](https://github.com/nf-core/rnaseq/pull/1819) - Drop RSeQC `infer_experiment` from the aligner's RSeQC module list when `aligner == 'bowtie2_salmon'` (transcriptome-aligned BAMs can't be inferred against a genomic BED); also skip sentieon tests on the conda profile since its license-server-driven output drifts across conda solves

## [[3.24.0](https://github.com/nf-core/rnaseq/releases/tag/3.24.0)] - 2026-04-09

### Credits

Special thanks to the following for their contributions to the release:

- [Adam Talbot](https://github.com/adamrtalbot)
- [Brian Fulton-Howard](https://github.com/BEFH)
- [Cindy Wang](https://github.com/cwang-lilly)
- [Elad Herz](https://github.com/EladH1)
- [Friederike Hanssen](https://github.com/FriederikeHanssen)
- [@harpbelle](https://github.com/harpbelle)
- [Maxime U Garcia](https://github.com/maxulysse)
- [Phil Ewels](https://github.com/ewels)
- [@sebinheo](https://github.com/sebinheo)

### Enhancements and fixes

- [PR #1740](https://github.com/nf-core/rnaseq/pull/1740) - Bump version to 3.24.0dev after release 3.23.0; always set ID/SM read group tags for STAR and HISAT2 even when `seq_center`/`seq_platform` are not provided
- [PR #1744](https://github.com/nf-core/rnaseq/pull/1744) - Add `--skip_quantification_merge` for per-sample tximport and MultiQC at scale, with sample-centric output directory structure
- [PR #1745](https://github.com/nf-core/rnaseq/pull/1745) - Always skip validation of `igenomes_base` and remove `format: directory-path` from schema to prevent S3 access errors
- [PR #1746](https://github.com/nf-core/rnaseq/pull/1746) - Add `--contaminant_screening_input` to choose contaminant screening on trimmed/filter-passed reads or aligner-unmapped reads, keep `unmapped` as the default, and preserve stable sample IDs throughout the workflow
- [PR #1749](https://github.com/nf-core/rnaseq/pull/1749) - Fix bowtie2 version extraction failing when Perl locale warnings are present (common in WSL/conda setups), which caused MultiQC to crash
- [PR #1750](https://github.com/nf-core/rnaseq/pull/1750) - Add missing tool citations to CITATIONS.md (Bowtie2, Kallisto, RiboDetector, SeqKit, tximport, UMICollapse)
- [PR #1751](https://github.com/nf-core/rnaseq/pull/1751) - Clarify in docs that GFF files should be provided via `--gff`, not `--gtf` ([#1584](https://github.com/nf-core/rnaseq/issues/1584))
- [PR #1752](https://github.com/nf-core/rnaseq/pull/1752) - Remove STAR from RSEM conda environments since STAR alignment runs as a separate process in this workflow, fixing ARM conda compatibility
- [PR #1754](https://github.com/nf-core/rnaseq/pull/1754) - Add experimental RustQC support (`--use_rustqc`): high-performance single-pass replacement for dupRadar, featureCounts biotype QC, RSeQC, Preseq, Qualimap, and SAMtools stats/flagstat/idxstats.
- [PR #1756](https://github.com/nf-core/rnaseq/pull/1756) - Fix iGenomes STAR version detection: replace filename heuristic with explicit check, remove unnecessary `STAR_GENOMEGENERATE_IGENOMES` build path
- [PR #1761](https://github.com/nf-core/rnaseq/pull/1761) - Fix Bowtie2 alignment logs appearing under "Bowtie2 (rRNA removal)" in MultiQC report when using `--aligner bowtie2_salmon`
- [PR #1762](https://github.com/nf-core/rnaseq/pull/1762) - Restore `extra_star_align_args` deduplication so user-supplied STAR flags override pipeline defaults instead of causing a fatal duplicate parameter error ([#1757](https://github.com/nf-core/rnaseq/issues/1757))
- [PR #1763](https://github.com/nf-core/rnaseq/pull/1763) - Bump version to 3.24.0 ahead of release
- [PR #1764](https://github.com/nf-core/rnaseq/pull/1764) - Update nf-core template to v3.5.2, update ro-crate maintainer
- [PR #1766](https://github.com/nf-core/rnaseq/pull/1766) - Update samtools modules to 1.23.1, fixing conda CI snapshot mismatches
- [PR #1769](https://github.com/nf-core/rnaseq/pull/1769) - Remove `--star` from RSEM preparereference test config, fixing conda CI failure after PR #1752 removed STAR from the RSEM environment
- [PR #1768](https://github.com/nf-core/rnaseq/pull/1768) - Update `actions/upload-artifact` from deprecated v3 to v5 in cloud test workflows
- [PR #1770](https://github.com/nf-core/rnaseq/pull/1770) - Exclude non-deterministic qualimap MultiQC files from snapshots, fixing x86/ARM cross-platform CI mismatches
- [PR #1771](https://github.com/nf-core/rnaseq/pull/1771) - Update ribodetector module to 0.3.3 (nf-core/modules#11131)
- [PR #1772](https://github.com/nf-core/rnaseq/pull/1772) - Update ribodetector ARM64 container to 0.3.3
- [PR #1778](https://github.com/nf-core/rnaseq/pull/1778) - Document that the `test` profile must be specified explicitly when running nf-test locally (required for GPU test profile support)
- [PR #1779](https://github.com/nf-core/rnaseq/pull/1779) - Update RustQC to 0.2.1: flag-based duplicate detection removes Parabricks `--skip-dup-check` workaround, junction_annotation `.txt` -> `.log` extension fix

## [[3.23.0](https://github.com/nf-core/rnaseq/releases/tag/3.23.0)] - 2026-02-27

### Credits

Special thanks to the following for their contributions to the release:

- [Albert Palleja](https://github.com/apalleja)
- [Chase Mateusiak](https://github.com/cmatKhan)
- [Christian Mertes](https://github.com/c-mertes)
- [Elad Herz](https://github.com/EladH1)
- [Ezra Greenberg](https://github.com/egreenberg7)
- [Gary Burnett](https://github.com/gburnett-nvidia)
- [Isaac Virshup](https://github.com/ivirshup)
- [Juliana Assis](https://github.com/Juassis)
- [Marine Cambon](https://github.com/marccamb)
- [Matthias Zepper](https://github.com/MatthiasZepper)
- [Sebastian Schulz](https://github.com/sebschulz1)

### Enhancements and fixes

- [PR #1616](https://github.com/nf-core/rnaseq/pull/1616) - Add Sylph for contamination detection.
- [PR #1663](https://github.com/nf-core/rnaseq/pull/1663) - Bump version after release 3.22.2
- [PR #1664](https://github.com/nf-core/rnaseq/pull/1664) - Add support for multiple rRNA removal tools (`--ribo_removal_tool`): SortMeRNA (default), Bowtie2, and RiboDetector; enable BBSplit MultiQC reporting; add paired-end read grouping in MultiQC
- [PR #1665](https://github.com/nf-core/rnaseq/pull/1665) - Bulk update modules/subworkflows; replace CUSTOM_GETCHROMSIZES with SAMTOOLS_FAIDX; update RSEQC modules with Wave containers for ARM compatibility; update ARM containers for RSEQC and UMITOOLS
- [PR #1667](https://github.com/nf-core/rnaseq/pull/1667) - Enhance RSEM output exports and remove unnecessary star_rsem check
- [PR #1669](https://github.com/nf-core/rnaseq/pull/1669) - Enable SeqKit stats MultiQC module for RiboDetector rRNA removal
- [PR #1672](https://github.com/nf-core/rnaseq/pull/1672) - Document star_rsem STAR aligner settings and customization
- [PR #1677](https://github.com/nf-core/rnaseq/pull/1677) - Apply Nextflow 25 strict syntax fixes
- [PR #1685](https://github.com/nf-core/rnaseq/pull/1685) - Add GPU-accelerated STAR alignment and mark duplicates using NVIDIA Parabricks rna_fq2bam (`--use_parabricks_star`)
- [PR #1686](https://github.com/nf-core/rnaseq/pull/1686) - Add support for uncompressed FASTQ input files ([#1343](https://github.com/nf-core/rnaseq/issues/1343))
- [PR #1687](https://github.com/nf-core/rnaseq/pull/1687) - Fix PREPARE_GENOME tests: use single aligner values, correct aligner assignments for index-specific tests, add Kallisto test, remove ineffective Sentieon tests, use file-names-only snapshots for all non-deterministic indices (STAR, Salmon, Kallisto, RSEM, HISAT2)
- [PR #1688](https://github.com/nf-core/rnaseq/pull/1688) - Significantly improved prokaryotic RNA-seq support: new `-profile prokaryotic` for bacterial/archaeal data with Bowtie2+Salmon alignment, GFFREAD transcript extraction for CDS-only annotations, and automatic STAR CDS configuration. We would like to thank [Juliana Assis](https://github.com/Juassis), [Sebastian Schulz](https://github.com/sebschulz1), [Albert Palleja](https://github.com/apalleja) and [Marine Cambon](https://github.com/marccamb) for their [recommendations and extensive testing](https://github.com/nf-core/rnaseq/issues/1512).
- [PR #1689](https://github.com/nf-core/rnaseq/pull/1689) - Migrate to topic-based version reporting for nf-core modules/subworkflows and local modules
- [PR #1694](https://github.com/nf-core/rnaseq/pull/1694) - Replace local iGenomes STAR modules with nf-core module aliases and config-based container overrides
- [PR #1696](https://github.com/nf-core/rnaseq/pull/1696) - Fix offline mode by skipping `igenomes_base` validation when `NXF_OFFLINE=true` ([#1690](https://github.com/nf-core/rnaseq/issues/1690))
- [PR #1697](https://github.com/nf-core/rnaseq/pull/1697) - Add tximport processing for RSEM outputs: gene/transcript length matrices, length-scaled counts, SummarizedExperiment objects, and DESeq2 QC using length-scaled counts ([#1320](https://github.com/nf-core/rnaseq/issues/1320)). **Note for `--aligner star_rsem` users:** the merged count and TPM files at the output root (e.g. `rsem.merged.gene_counts.tsv`) are now produced by tximport, matching the Salmon/Kallisto pathway. The previous RSEM merge script outputs are preserved in the `rsem_merge_counts/` subdirectory.
- [PR #1700](https://github.com/nf-core/rnaseq/pull/1700) - Add FastQC step after BBSplit/rRNA filtering to provide QC metrics on reads used for alignment ([#1276](https://github.com/nf-core/rnaseq/issues/1276))
- [PR #1704](https://github.com/nf-core/rnaseq/pull/1704) - Include single-library samples in merged fastq output when `--save_merged_fastq` is set ([#748](https://github.com/nf-core/rnaseq/issues/748))
- [PR #1707](https://github.com/nf-core/rnaseq/pull/1707) - Enable UMI deduplication with `--aligner star_rsem` ([#829](https://github.com/nf-core/rnaseq/issues/829))
- [PR #1708](https://github.com/nf-core/rnaseq/pull/1708) - Allow `--skip_alignment` with a pre-built `--salmon_index` or `--kallisto_index` without requiring `--fasta` ([#1706](https://github.com/nf-core/rnaseq/issues/1706))
- [PR #1709](https://github.com/nf-core/rnaseq/pull/1709) - Update metro map renders with nf-metro v0.4.7; add source `.mmd` file and regeneration instructions to CONTRIBUTING.md
- [PR #1711](https://github.com/nf-core/rnaseq/pull/1711) - Scope GPU container flags (`--gpus all`, `--nv`) to `process_gpu` tasks only via per-process `containerOptions`, fixing failures on CPU-only nodes in mixed clusters ([#1710](https://github.com/nf-core/rnaseq/issues/1710))
- [PR #1713](https://github.com/nf-core/rnaseq/pull/1713) - Add optional `seq_platform` and `seq_center` samplesheet columns for per-sample BAM read group tags (`PL`, `CN`). Read group assembly is handled via ext.args config closures rather than module inputs. Per-sample `seq_center` overrides the global `--seq_center` parameter. Based on [PR #1701](https://github.com/nf-core/rnaseq/pull/1701) by [@c-mertes](https://github.com/c-mertes).
- [PR #1714](https://github.com/nf-core/rnaseq/pull/1714) - Re-render metro map with nf-metro v0.5.2: improved label spacing, smaller file icon font, and section alignment fix
- [PR #1715](https://github.com/nf-core/rnaseq/pull/1715) - Bump version to 3.23.0 ahead of release
- [PR #1716](https://github.com/nf-core/rnaseq/pull/1716) - Add informative error when Salmon fails to produce strandedness output for auto-strandedness samples
- [PR #1718](https://github.com/nf-core/rnaseq/pull/1718) - Add `--seq_platform` parameter for global sequencing platform BAM read group tag, by analogy with `--seq_center`
- [PR #1719](https://github.com/nf-core/rnaseq/pull/1719) - Docs and changelog cleanup: move descriptions above `<details>` blocks in output.md, add missing software dependencies, sort arm.config alphabetically
- [PR #1724](https://github.com/nf-core/rnaseq/pull/1724) - Update umitools modules: remove patches, add conda channel prefixes, update Wave containers
- [PR #1725](https://github.com/nf-core/rnaseq/pull/1725) - Refine .nftignore patterns to reinstate tx2gene MD5 checking, remove redundant UNTAR version collection
- [PR #1728](https://github.com/nf-core/rnaseq/pull/1728) - Re-render metro map with nf-metro v0.5.4: bolder section labels and number badges for improved visual hierarchy, increased vertical spacing between stacked sections, synchronized animation timing
- [PR #1730](https://github.com/nf-core/rnaseq/pull/1730) - Bump Nextflow from 25.04.0 to 25.04.3 in CI to fix `conda create --mkdir` failure ([nextflow-io/nextflow#5947](https://github.com/nextflow-io/nextflow/issues/5947))
- [PR #1734](https://github.com/nf-core/rnaseq/pull/1734) - Compose `test_prokaryotic` profile on `prokaryotic` to remove duplicated settings
- [PR #1735](https://github.com/nf-core/rnaseq/pull/1735) - Code quality improvements: replace opaque tuple indexing with named destructuring, rename `ch_dummy_file`, move metro map docs, align GPU CI workflow with other workflows
- [PR #1736](https://github.com/nf-core/rnaseq/pull/1736) - Load prokaryotic config in nf-test instead of duplicating params in each test
- [PR #1738](https://github.com/nf-core/rnaseq/pull/1738) - Fix iGenomes STAR conda: use `bioconda` channel for x86_64, reserve `seqera` channel for ARM only

### Parameters

| Old parameter | New parameter                |
| ------------- | ---------------------------- |
|               | `--ribo_removal_tool`        |
|               | `--sylph_db`                 |
|               | `--sylph_taxonomy`           |
|               | `--gffread_transcript_fasta` |
|               | `--extra_bowtie2_align_args` |
|               | `--use_parabricks_star`      |

> **NB:** Parameter has been **added** if just the new parameter information is present.

### Profiles

| Profile       | Description                                            |
| ------------- | ------------------------------------------------------ |
| `prokaryotic` | Settings optimized for bacterial/archaeal RNA-seq data |

### Software dependencies

| Dependency  | Old version | New version |
| ----------- | ----------- | ----------- |
| `bowtie2`   |             | 2.5.4       |
| `seqkit`    |             | 2.9.0       |
| `sylph`     |             | 0.7.0       |
| `sylph-tax` |             | 1.2.0       |

> **NB:** Dependency has been **updated** if both old and new version information is present.
>
> **NB:** Dependency has been **added** if just the new version information is present.
>
> **NB:** Dependency has been **removed** if new version information isn't present.

## [[3.22.2](https://github.com/nf-core/rnaseq/releases/tag/3.22.2)] - 2025-12-11

### Credits

Special thanks to the following for their contributions to the release:

- [ahwanpandey](https://github.com/ahwanpandey)
- [Graeme Grimes](https://github.com/ggrimes)
- [Pontus Höjer](https://github.com/pontushojer)

### Enhancements and fixes

- [PR #1654](https://github.com/nf-core/rnaseq/pull/1654) - Fix tximport to handle tx2gene files with extra columns from `--gtf_extra_attributes`, and fix sample name mangling in DESeq2 QC
- [PR #1655](https://github.com/nf-core/rnaseq/pull/1655) - Fix duplicate flagstat files in MultiQC report when mark duplicates is enabled ([#1653](https://github.com/nf-core/rnaseq/issues/1653))
- [PR #1656](https://github.com/nf-core/rnaseq/pull/1656) - Bump version after release 3.22.1
- [PR #1659](https://github.com/nf-core/rnaseq/pull/1659) - Fix MultiQC sample name collisions when multiple samples share the same FASTQ filename ([#1657](https://github.com/nf-core/rnaseq/issues/1657))
- [PR #1658](https://github.com/nf-core/rnaseq/pull/1658) - Bump nf-core/multiqc module to 1.33
- [PR #1660](https://github.com/nf-core/rnaseq/pull/1660) - Update MultiQC ARM container to 1.33
- [PR #1648](https://github.com/nf-core/rnaseq/pull/1648) - Reduce duplicate coverage in pipeline tests by adding skip options
- [PR #1661](https://github.com/nf-core/rnaseq/pull/1661) - Bump version to 3.22.2 ahead of release

## [[3.22.1](https://github.com/nf-core/rnaseq/releases/tag/3.22.1)] - 2025-12-04

### Credits

Special thanks to the following for their contributions to the release:

- [Elad Herz](https://github.com/EladH1)
- [Matthias Hörtenhuber](https://github.com/mashehu)
- [sisterdot](https://github.com/sisterdot)

### Enhancements and fixes

- [PR #1640](https://github.com/nf-core/rnaseq/pull/1640) - Bump version after release 3.22.0
- [PR #1641](https://github.com/nf-core/rnaseq/pull/1641) - Add arm-based CI tests and fix arm-related issues
- [PR #1645](https://github.com/nf-core/rnaseq/pull/1645) - Fix BAM CSI index access error with UMI deduplication ([#1643](https://github.com/nf-core/rnaseq/issues/1643))
- [PR #1642](https://github.com/nf-core/rnaseq/pull/1642) - Add long format to rsem merge
- [PR #1650](https://github.com/nf-core/rnaseq/pull/1650) - Restrict ARM CI tests to Docker profile only
- [PR #1651](https://github.com/nf-core/rnaseq/pull/1651) - Add dupMatrix files to nftignore to fix conda reproducibility issues

## [[3.22.0](https://github.com/nf-core/rnaseq/releases/tag/3.22.0)] - 2025-11-26

### Credits

Special thanks to the following for their contributions to the release:

- [Ahwan Pandey](https://github.com/ahwanpandey)
- [Cristina Tuñí i Domínguez](https://github.com/ctuni)
- [Elad Herz](https://github.com/EladH1)
- [Emily Miyoshi](https://github.com/emilymiyoshi)
- [Jonathan Manning](https://github.com/pinin4fjords)
- [Pontus Höjer](https://github.com/pontushojer)
- [Siddhartha Bagaria](https://github.com/siddharthab)

### Enhancements and fixes

- [PR #1608](https://github.com/nf-core/rnaseq/pull/1608) - Bump version after release 3.21.0
- [PR #1613](https://github.com/nf-core/rnaseq/pull/1613) - Fix broken link and add latest kit version for Takara UMI prep in usage documentation
- [PR #1614](https://github.com/nf-core/rnaseq/pull/1614) - Template update for nf-core/tools v3.4.1
- [PR #1617](https://github.com/nf-core/rnaseq/pull/1617) - Update bbmap/bbsplit module
- [PR #1618](https://github.com/nf-core/rnaseq/pull/1618) - Fix CI: Ensure confirm-pass job runs for markdown-only PRs
- [PR #1619](https://github.com/nf-core/rnaseq/pull/1619) - Update Credits to reflect current maintainership
- [PR #1620](https://github.com/nf-core/rnaseq/pull/1620) - Fix bigwig strand labeling for reverse-stranded libraries ([#1591](https://github.com/nf-core/rnaseq/issues/1591))
- [PR #1621](https://github.com/nf-core/rnaseq/pull/1621) - Optimize qualimap performance with multi-threaded name sorting
- [PR #1622](https://github.com/nf-core/rnaseq/pull/1622) - Update tximeta/tximport module to fix sample name mangling
- [PR #1624](https://github.com/nf-core/rnaseq/pull/1624) - Document RSeQC inner_distance limitation for genomes with large chromosomes (>500 Mb), such as plant genomes
- [PR #1625](https://github.com/nf-core/rnaseq/pull/1625) - Add documentation warning about Qualimap read counting bug ([#1273](https://github.com/nf-core/rnaseq/issues/1273))
- [PR #1628](https://github.com/nf-core/rnaseq/pull/1628) - Template update for nf-core/tools v3.5.1
- [PR #1630](https://github.com/nf-core/rnaseq/pull/1630) - Fix arm64 profile to use pre-built ARM containers and update documentation
- [PR #1631](https://github.com/nf-core/rnaseq/pull/1631) - Fix bbsplit index staging by using symlinks instead of full copy
- [PR #1632](https://github.com/nf-core/rnaseq/pull/1632) - Add validation error for incompatible `--transcript_fasta` and `--additional_fasta` params ([#1450](https://github.com/nf-core/rnaseq/issues/1450))
- [PR #1635](https://github.com/nf-core/rnaseq/pull/1635) - Fix `--gtf_extra_attributes` to support multiple comma-separated values and correct deprecated parameter name in docs ([#1626](https://github.com/nf-core/rnaseq/issues/1626))
- [PR #1636](https://github.com/nf-core/rnaseq/pull/1636) - Simplify workflow nextflow.config by consolidating redundant patterns
- [PR #1638](https://github.com/nf-core/rnaseq/pull/1638) - Bump version to 3.22.0 ahead of release

## [[3.21.0](https://github.com/nf-core/rnaseq/releases/tag/3.21.0)] - 2025-09-18

### Credits

Special thanks to the following for their contributions to the release:

- [Edmund Miller](https://github.com/edmundmiller)
- [Friederike Hanssen](https://github.com/friederikehanssen)
- [Maxime Garcia](https://github.com/maxulysse)
- [Jonathan Manning](https://github.com/pinin4fjords)

### Enhancements & fixes

- [PR #1597](https://github.com/nf-core/rnaseq/pull/1597) - Bump version after release 3.20.0
- [PR #1603](https://github.com/nf-core/rnaseq/pull/1603) - Add bam input pathway
- [PR #1604](https://github.com/nf-core/rnaseq/pull/1604) - Enable BAM input for RSEM
- [PR #1605](https://github.com/nf-core/rnaseq/pull/1605) - Fix default for umi_discard_read to prevent validation errors in Platform
- [PR #1606](https://github.com/nf-core/rnaseq/pull/1606) - Bump version to 3.21.0 ahead of release

### Software dependencies

| Dependency | Old version | New version |
| ---------- | ----------- | ----------- |
| `MultiQC`  | 1.30        | 1.31        |

## [[3.20.0](https://github.com/nf-core/rnaseq/releases/tag/3.20.0)] - 2025-08-18

### Credits

Special thanks to the following for their contributions to the release:

- [Friederike Hanssen](https://github.com/friederikehanssen)
- [Ido Tamir](https://github.com/idot)
- [Jonathan Manning](https://github.com/pinin4fjords)
- [Maxime Garcia](https://github.com/maxulysse)
- [Usman Rashid](https://github.com/GallVp)

### Enhancements & fixes

- [PR #1568](https://github.com/nf-core/rnaseq/pull/1568) - Bump version after release 3.19.0
- [PR #1571](https://github.com/nf-core/rnaseq/pull/1571) - For umitools use only umi_dedup.sorted.log in multiqc_report
- [PR #1573](https://github.com/nf-core/rnaseq/pull/1573) - Fix salmon.merged.SummarizedExperiment.rds name collision
- [PR #1585](https://github.com/nf-core/rnaseq/pull/1585) - Update awsfulltest.yml to restore aligner-wise outputs
- [PR #1580](https://github.com/nf-core/rnaseq/pull/1580) - Template update for nf-core/tools v3.3.2
- [PR #1590](https://github.com/nf-core/rnaseq/pull/1590) - Addition of Sentieon STAR
- [PR #1594](https://github.com/nf-core/rnaseq/pull/1594) - Exclude star rsem pca from snaps
- [PR #1595](https://github.com/nf-core/rnaseq/pull/1595) - Exclude unstable star_rsem clusterings from snaps

### Software dependencies

| Dependency | Old version | New version |
| ---------- | ----------- | ----------- |
| `MultiQC`  | 1.29        | 1.30        |
| `Sentieon` |             | 202503.01   |

## [[3.19.0](https://github.com/nf-core/rnaseq/releases/tag/3.19.0)] - 2025-06-10

### Credits

Special thanks to the following for their contributions to the release:

- [Alena Nikolaeva](https://github.com/AlenaNik)
- [Anabella Trigila](https://github.com/atrigila)
- [Angel Pizarro](https://github.com/delagoya)
- [Ben Sherman](https://github.com/bentsherman)
- [Dave Carlson](https://github.com/davidecarlson)
- [Gabriel Lichtenstein](https://github.com/glichtenstein)
- [Jonathan Manning](https://github.com/pinin4fjords)
- [Lorenzo Fontana](https://github.com/fntlnz)
- [Matthias Hörtenhuber](https://github.com/mashehu)
- [Milos Micik](https://github.com/milos7250)
- [Maxime Garcia](https://github.com/maxulysse)

### Enhancements & fixes

- [PR #1480](https://github.com/nf-core/rnaseq/pull/1480) - Bump version after release 3.18.0
- [PR #1482](https://github.com/nf-core/rnaseq/pull/1482) - Update trimgalore module for save_unpaired fix
- [PR #1486](https://github.com/nf-core/rnaseq/pull/1486) - Bump STAR build for multiprocessing fix
- [PR #1490](https://github.com/nf-core/rnaseq/pull/1490) - Make genomic FASTA input optional
- [PR #1496](https://github.com/nf-core/rnaseq/pull/1496) - Template update for nf-core/tools v3.2.0
- [PR #1499](https://github.com/nf-core/rnaseq/pull/1499) - Bump MultiQC module to 1.27
- [PR #1508](https://github.com/nf-core/rnaseq/pull/1508) - Fix missing Bracken results in the MultiQC report
- [PR #1528](https://github.com/nf-core/rnaseq/pull/1528) - Improve JSON schema validation files
- [PR #1523](https://github.com/nf-core/rnaseq/pull/1523) - Update preprocessing subworkflow to fix linting block on trimming
- [PR #1521](https://github.com/nf-core/rnaseq/pull/1521) - Updated Perl conda package version for local module gtf2bed for Arm compatibility.
- [PR #1550](https://github.com/nf-core/rnaseq/pull/1550) - Simplify `SummarizedExperiment` outputs.
- [PR #1553](https://github.com/nf-core/rnaseq/pull/1553) - Make jobs automatically resubmit for exit code 175
- [PR #1556](https://github.com/nf-core/rnaseq/pull/1556) - Update index docs to remove references to 'indexing only mode'
- [PR #1558](https://github.com/nf-core/rnaseq/pull/1558) - Remove patches and bump modules for ARM compat
- [PR #1560](https://github.com/nf-core/rnaseq/pull/1560) - General modules update, include updating subworkflows for stats fixes
- [PR #1563](https://github.com/nf-core/rnaseq/pull/1563) - Version bumps ahead of 3.19.0 release
- [PR #1565](https://github.com/nf-core/rnaseq/pull/1565) - Improve reproducibility with Conda
- [PR #1567](https://github.com/nf-core/rnaseq/pull/1567) - Prerelease 3.19.0 fixes

