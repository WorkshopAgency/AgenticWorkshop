# MCP servers

Notes on the MCP servers this project configures. **This folder holds
documentation only** — there is no server code here and nothing to install
from it.

| Server | Kind | Setup cost | Tools | Used by |
|---|---|---|---:|---|
| [`duckdb`](#duckdb--query-a-local-database) | local (`uv`) | 30 MB download | 4 | [Exercise 3](../exercises/03-mcp/README.md) |
| [`rcsb`](#rcsb--the-live-pdb) | local (`uv`) | ~1 MB more | 38 | not used in an exercise |
| [`biomcp`](#biomcp--43-biomedical-databases) | local (`uv`) | ~1 MB more | 83 | exercises planned |
| [`opentargets`](#opentargets--remote-no-install) | **remote** (no auth) | **nothing** | 5 | exercise planned |

All four ship with **`"disabled": true` under `mcp.servers`** (OpenCode v2).
Use **`/mcps`** to connect only the server you need. This overrides the disabled
setting for the running service; it does not rewrite `opencode.json`.
Closing a client window is not necessarily restarting v2's background service.
For persistent enablement, set that server's `"disabled": false` and reload
the project. The old v1 `enabled` field is not the v2 setting.

Turn on only what you are using. Tool definitions included in a request use
context even if the agent does not call those tools. An idle server can add
overhead to the conversation; exact behaviour depends on the OpenCode version
and which tools are exposed to that agent.

---

## The two kinds, and what the difference means

### Local servers — `"type": "local"`

A program on **your laptop**. OpenCode starts it as a child process and talks
to it over stdin and stdout: it writes a JSON line to the child's stdin and
reads one back from its stdout. No network port, no hosting, no URL. The
process exits when OpenCode closes the pipe.

```json
{ "type": "local", "command": ["uvx", "rcsb-mcp@0.15.0"] }
```

- **Needs `uv`.** `uvx` fetches the package from PyPI on first use and caches
  it in `~/.cache/uv`. Nothing is stored in this repository.
- **Needs a one-time download.** Measured on macOS arm64: DuckDB 30 MB,
  `rcsb` 8.5 MB, `biomcp` 8.7 MB — but **31 MB for all three together**,
  because they share almost every dependency. Once DuckDB is cached, the
  other two cost about 1 MB each. Half of DuckDB's 30 MB is the DuckDB
  engine itself.
- **Works offline afterwards**, though `rcsb` and `biomcp` then have no data
  to query, because they are clients for online services.
- **Your data stays local** if the server reads local files, as `duckdb` does.

Warm the cache before the workshop rather than during it:

```bash
uvx mcp-server-motherduck@1.0.8 --help
uvx rcsb-mcp@0.15.0 --help
uvx --from biomcp-server==0.7.0 bio-mcp --help
```

### Remote servers — `"type": "remote"`

Someone else runs the server. OpenCode connects to a URL over HTTPS.

```json
{ "type": "remote", "url": "https://mcp.platform.opentargets.org/mcp" }
```

- **Nothing to install.** No `uv`, no download, no Python, no platform
  problems. This is the one kind that works on any laptop immediately.
- **"No auth"** means no account, token or API key — you connect and use it.
  The four in the life-science list that need no auth are run by public
  institutions; most remote MCP servers are commercial and need OAuth or a
  subscription key.
- **It needs the network, every time.** If the room's wifi fails, or the
  service is down or rate-limited, the server is simply unavailable. A local
  server would still have worked.
- **Your queries leave your machine.** You are sending text to a third party.
  Fine for public gene and protein identifiers; not for anything confidential.
  The same warning the workshop gives about free external models applies.

Neither kind is better. Local costs a download and gives you independence;
remote costs a dependency on someone else's uptime and gives you zero setup.
Exercise 3 uses a local one to reduce dependence on an external data service.
Installation, permissions, paths and model availability can still fail.

---

## `duckdb` — query a local database

**Local, `uv`, 4 tools.** `mcp-server-motherduck` 1.0.8, by MotherDuck.

Opens a DuckDB database file and runs SQL against it. Not tied to any
dataset: `--db-path` points it at whatever database you give it. Exercise 3
supplies a PDB snapshot; point it at your own data and nothing else changes.

| Tool | Does |
|---|---|
| `execute_query` (`sql`) | Runs SQL and returns rows |
| `list_tables` | Lists tables and views |
| `list_columns` (`table`) | Column names and types |
| `list_databases` | Attached databases |

`switch_database_connection` is **not** exposed, because
`--allow-switch-databases` is not set, so the agent cannot repoint it.

**Read-only is narrower than it sounds.** `CREATE`, `UPDATE`, `DELETE` and
`ATTACH` are refused by DuckDB. But this **succeeds** and writes a file to
your disk:

```sql
COPY (SELECT 1 AS x) TO 'PROOF.parquet' (FORMAT parquet)
```

`read_csv('...')` will likewise open any file the process can reach.
Read-only describes the *database*, not the *filesystem* — the same
distinction the agent exercises make about `edit: deny` not making an agent
read-only when it can still run shell commands.

`--max-rows 100` and `--max-chars 8000` are set deliberately: the default cap
is 1024 rows, and one careless `SELECT *` would fill a small model's context.

Setup and the exercise: [Exercise 3](../exercises/03-mcp/README.md).

## `rcsb` — the live PDB

**Local, `uv`, 38 tools.** `rcsb-mcp` 0.15.0.

The Protein Data Bank, live, as structured tools. No exercise uses it — it is
here to explore, and because it is the natural companion to the frozen PDB
snapshot in Exercise 3. Ask both the same question and the difference between
a local snapshot and a live service becomes concrete.

| Group | Tools |
|---|---|
| Build a search | `rcsb_query_fulltext`, `rcsb_query_attribute`, `rcsb_query_sequence`, `rcsb_query_chemical`, `rcsb_query_structure`, `rcsb_query_seqmotif`, `rcsb_query_strucmotif`, `rcsb_query_composer` |
| Run it | `rcsb_search_request`, `rcsb_list_pdb_search_attributes` |
| Free text → ontology | `rcsb_find_go_terms`, `rcsb_find_interpro_domains`, `rcsb_find_enzyme_classes`, `rcsb_find_disease_terms`, `rcsb_find_organisms` |
| Entry data | `rcsb_get_entries`, `rcsb_get_polymer_entities`, `rcsb_get_nonpolymer_entities` (ligands), `rcsb_get_branched_entities` (glycans), `rcsb_get_assemblies`, `rcsb_get_interfaces`, `rcsb_get_chem_comps` |
| Chains and instances | `rcsb_get_polymer_entity_instances`, `rcsb_get_nonpolymer_entity_instances`, `rcsb_get_branched_entity_instances` |
| Sequence cross-reference | `rcsb_seqcoord_alignments` (PDB ↔ UniProt ↔ NCBI), `rcsb_seqcoord_annotations`, `rcsb_seqcoord_group_alignments`, `rcsb_seqcoord_group_annotations` |
| Grouping and external records | `rcsb_get_entry_groups`, `rcsb_get_polymer_entity_groups`, `rcsb_get_nonpolymer_entity_groups`, `rcsb_get_uniprot`, `rcsb_get_pubmed`, `rcsb_get_group_provenance` |
| Output | `rcsb_render_report` — a self-contained HTML report of a search |

It does real structural work, not only metadata: **sequence-similarity search**
(MMseqs2), **3D shape similarity** against an existing structure, and
**structural-motif search** for a geometric arrangement of residues. Its own
examples use `4HHB`, `4HHB.A` and `4HHB_3` — the same haemoglobin structure as
Exercises 1 to 3.

It queries RCSB over the network, so it needs a connection despite being a
local process.

## `biomcp` — 43 biomedical databases

**Local, `uv`, 83 tools.** `biomcp-server` 0.7.0.

The broad one: roughly one tool per resource across about 57 endpoints.
Exercises are planned for it.

| Area | Tools include |
|---|---|
| Genes and expression | `gene_enrichment`, `gene_full_profile`, `gene_go_annotation`, `ensembl_gene_lookup`, `ensembl_homologs`, `gtex_tissue_expression`, `gtex_eqtl`, `expression_atlas_gene`, `geo_dataset_search`, `hgnc_search` |
| Variants | `gwas_variant_associations`, `gwas_gene_variants`, `gnomad_variant_lookup`, `gnomad_gene_constraint`, `clinvar_query`, `dbsnp_search`, `variant_annotate`, `ewas_*`, `mqtl_*` |
| Proteins and interactions | `uniprot_annotate`, `protein_domains`, `protein_glycosylation`, `protein_tissue_expression`, `string_interactions`, `biogrid_interactions`, `intact_interactions`, `uniparc_*` |
| Structures | `pdb_structure_summary`, `alphafold_structure`, `emdb_structure_lookup` |
| Chemistry and drugs | `chembl_drug_search`, `chebi_compound`, `chebi_search`, `unichem_mapping`, `compound_info`, `lipid_lookup`, `glycan_lookup` |
| Pathways and targets | `kegg_pathway_search`, `kegg_pathway_genes`, `reactome_pathway_search`, `go_term_lookup`, `ot_target_info`, `ot_target_disease` |
| Literature | `pubmed_search`, `europepmc_search`, `openalex_work_search` |
| Sequences and archives | `blast_search`, `ncbi_fetch_sequence`, `ena_sequence_search`, `sra_search`, `bioproject_search`, `genome_assembly_search`, `ucsc_genome_info` |
| Other omics | `pride_*` (proteomics), `metabolomics_*`, `microbiome_study_search`, `cellxgene_search`, `biosample_*`, `plasmid_search` |
| Model organisms | `flybase_*`, `wormbase_*`, `rgd_*`, `plant_gene_lookup`, `taxonomy_lookup` |
| Meta | `tool_inventory`, `db_health_check`, `get_analysis_template`, `intelligent_analyze` |

Breadth has a cost beyond context. **83 tool descriptions is a lot to choose
from**, and a small model picks the wrong tool more often than it does with
four. Use it with one of the larger-context models, and check which tool it
actually called rather than trusting the answer. `tool_inventory` is a good
first request: it lets the model list what it has instead of guessing.

Compare `pdb_structure_summary` — one tool — with `rcsb`'s 38. This server is
wide and shallow; `rcsb` is narrow and deep. They complement each other.

## `opentargets` — remote, no install

**Remote, no authentication, 5 tools.** Run by the Open Targets Platform.

Target–disease association evidence: which genes are implicated in which
diseases, with the supporting evidence and scores.

| Tool | Does |
|---|---|
| `get_open_targets_graphql_schema` | Returns the GraphQL schema, filtered by category |
| `get_type_dependencies` | Schema subsets for specific types |
| `search_entities` | Finds targets, diseases and drugs by name |
| `query_open_targets_graphql` | Runs a GraphQL query |
| `batch_query_open_targets_graphql` | Runs one query over many variable sets |

This one is interesting for a reason beyond the data. It does not wrap each
question in its own tool — it hands the agent **a schema and a query
language** and expects it to compose the query. That is the same skill as
writing SQL against DuckDB in Exercise 3, one layer up, and it is checkable
the same way: read the query before approving it, and ask what it returned
rather than trusting the summary.

Nothing to install. Add the URL, toggle it on, use it — which makes it the
obvious fallback for anyone whose `uv` install fails during the session.

---

## Adding another server

Register it under `mcp.servers` in `opencode.json` with `"disabled": true`, and add a
section here. Give it a folder of its own only when it needs files of its own;
documentation alone belongs in this file.

Check tool count and definition size before adopting a server. For scale,
using the earlier workshop measurements (approximate and version/tokenizer-dependent):

| Server | Tools | Tool definitions | 16384 budget | 131072 budget | 262144 budget |
|---|---:|---:|---:|---:|---:|
| `duckdb` | 4 | ~780 tokens | 4.8% | 0.6% | 0.3% |
| `opentargets` | 5 | ~4,400 tokens | 26.9% | 3.4% | 1.7% |
| `rcsb` | 38 | ~21,200 tokens | 129.4% | 16.2% | 8.1% |
| `biomcp` | 83 | ~17,400 tokens | 106.2% | 13.3% | 6.6% |

These are **v1 full-catalog measurements**, not the current v2 prompt cost.
V2 defaults to Code Mode, which groups MCP tools and changes their exposure;
do not assume every full tool schema is sent in every request. Returned data
still uses context. The larger columns are **target-capacity comparisons, not deployment
claims**. Follow the [context guide](../README.md#changing-your-context-setting)
and confirm server support before changing your budget; approval is required
above 32768. Inputs, results and answers need space too. Keep unnecessary
servers off even when they fit: context capacity and reliable tool selection
are different concerns.

## Behaviour worth knowing

- **Connected is not working.** A missing database can pass the handshake and
  still fail every query. Ask the agent what a query returned.
- **Read-only is not write-free.** DuckDB in read-only mode refuses `CREATE`,
  `UPDATE`, `DELETE` and `ATTACH`, but `COPY ... TO` still writes a file
  outside the database.
- **Tool counts:** 4 for DuckDB, 38 for RCSB, 83 for BioMCP and 5 for Open
  Targets, read from each server's `tools/list`.
- **Downloads:** the three local servers' wheels are 30 MB, 8.5 MB and 8.7 MB
  on their own, 31 MB together.
- **Switching a server on or off** with `/mcps` leaves `opencode.json`
  unchanged.
