# Preface to the MCP Exercises

Exercise 1 built **skills**: reusable instructions for a task. Exercise 2
built **agents**: roles that decide what to do. This exercise adds the third
component, **MCP**: a standard way for OpenCode to connect to a capability
that lives outside it.

Here that capability is a **DuckDB** database holding 259,693 PDB entries —
every structure deposited between 1972 and September 2026. You will ask
questions in plain English, an agent will write SQL, and you will find out
whether the answers are true.

The server runs **on your laptop**, as a child process of OpenCode. It binds
no network port and needs no hosting. The database file stays on your laptop,
but schemas and query results included in model requests leave it: they go to
DTU or to whichever external model provider you selected. Use public exercise
data, not confidential data, when connecting to external models.

The running theme of this exercise: **a query that succeeds is not the same as a correct answer.**
Exercise 1 made the same point about downloads — a
successful HTTP request is not the same as a downloaded structure file. A clean SQL result with a
plausible number is not necessarily correct.

## Where things live

The **MCP server** and the **exercise data** are separate, and stay separate:

```text
mcp/README.md            the server: config, setup and caveats.
exercises/03-mcp/data/   this exercise's data, with its own provenance.
```

The DuckDB MCP server opens whatever database file it is pointed at. This
exercise supplies one database; in exercise 3h you point the same server at your own data
without changing anything in `mcp/`.

You need python installation tool `uv` (or pip) installed. Check with `uv --version`; see
[the server notes](../../../mcp/README.md) if it is missing.

You can install it with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

# Exercise 3a — Connect the server, and verify that you did

In your terminal, from the workshop root, build the database from the shipped
Parquet files — about 5 MB of data becoming a 17 MB database:

```bash
uv run --with duckdb python exercises/03-mcp/scripts/make_db.py
```

It is built on your laptop rather than downloaded, so the workshop ZIP stays
small. Fetch the server package once, so its first use is not a silent 30 MB
download:

```bash
uvx mcp-server-motherduck@1.0.8 --help
```

Now start OpenCode and turn the server on, in the chat:

```text
/mcps
```

Four servers are listed, all disabled. Select **`duckdb`** — only that one —
press **space** to toggle it, then **esc**.

Leave the other three off. Tool definitions included in model requests use
context, as do returned results. The relevant budget is the one selected in
your project, which can be smaller than the server's maximum. Turn on only
the MCP servers you need; a larger window does not make unnecessary tools free.
The other three are described in
[mcp/README.md](../../../mcp/README.md); `rcsb` is the live PDB, which is worth
comparing against this frozen snapshot once you have finished the exercise.

Check the current service connection in your terminal, in the same project:

```bash
opencode mcp list
```

You want `duckdb` to report **connected**. In v2 this reports runtime state,
not simply the value on disk. The saved entry still has `"disabled": true`.
If the CLI and chat disagree, check that they use the same project and server.
Closing a client window does not necessarily stop v2's background service.
Use `/mcps` again after a service restart; do not assume the toggle is permanent.

## The meaning of the MCP being "connected"

Now break the MCP connection on purpose. Disconnect `duckdb` with `/mcps`
first, then rename the database. Just closing a v2 client can leave the
server's existing database connection alive:

```bash
mv exercises/03-mcp/data/workshop.duckdb exercises/03-mcp/data/workshop.duckdb.hidden
```

Toggle `duckdb` on with `/mcps` again, and it reports
**connected** — because the server process starts perfectly well. The
database is only opened when a query arrives. Ask the agent a question now
and you will get:

```text
IO Error: Cannot open database ".../workshop.duckdb" in read-only mode:
database does not exist
```

Disconnect `duckdb`, put the file back, then reconnect:

```bash
mv exercises/03-mcp/data/workshop.duckdb.hidden exercises/03-mcp/data/workshop.duckdb
```

**What to notice:** "connected" means a process started and answered a
handshake. It does not mean the thing behind it works. This is the same
distinction as Exercise 2's "code generated", "viewer opened" and
"scientific content verified" — separate claims, separately checked. The
failure here was at least honest: it named the missing file instead of
inventing an answer.

---

# Exercise 3b — Ask something you cannot visually verify

Let the agent discover the data rather than telling it the schema:

> What tables are available through the DuckDB server, and what columns does
> each one have? Do not query the data yet, just describe what is there.

You should find two tables:

| Table | Rows | Contents |
|---|:---|:---|
| `entries` | 259,693 | ID, classification, deposition date, title, organism, resolution, experiment type |
| `entry_types` | 259,693 | ID, molecule type, method class |

259,693 rows is the point of the exercise. You cannot scroll through the rows, you cannot
eyeball it, and you cannot tell whether an answer about it is right by
looking at the data.

Now ask a question that sounds completely ordinary:

> What is the average resolution of structures in the PDB?

Read the SQL **before** you approve it. You will get something close to:

```sql
SELECT avg(resolution) FROM entries;
```

and an answer near **2.362 Å**.

That is an entirely plausible number. A crystallographer would not blink at
it. Write it down and move to 3c.

**What to notice:** you have a clean query, no error, and a believable
result. Every signal available to you says the task is finished.

---

# Exercise 3c — Find out whether the answer is true

Ask the agent one more question:

> How many rows are in entries, and how many of them actually have a
> resolution value? Show me both numbers.

```sql
SELECT count(*), count(resolution) FROM entries;
```

| count(\*) | count(resolution) |
|---:|---:|
| 259,693 | 244,589 |

**15,104 entries were silently excluded from that average.** `count(*)`
counts rows; `count(column)` skips NULLs, and so does `avg()`.

Find out which ones:

> Group the entries with no resolution value by experiment type.

They are not a random 6% of the PDB. **Solution NMR structures have no
resolution at all** — the concept does not apply to the method. Of 14,668
`SOLUTION NMR` entries, none carry a resolution.

## Check it yourself, without trusting the agent

This is what `exercises/03-mcp/data/pdb_sample.csv` is for: 512 entries, small
enough to open and count. In the terminal, ask to create a small python script 
to check the count of the blanks.

<details>
<summary>For reference, this python script will do the job.</summary>
  
```bash
python3 -c "
import csv
rows = list(csv.DictReader(open('exercises/03-mcp/data/pdb_sample.csv')))
blank = [r for r in rows if r['resolution'] == '']
print('rows:', len(rows), ' blank resolution:', len(blank))
print(set(r['experiment_type'] for r in blank))
"
```

```text
rows: 512  blank resolution: 26
{'SOLUTION NMR'}
```

</details>

All 26 blanks are NMR only. You have now confirmed the pattern with your own
tool, on a file you can read.

The sample is deliberately chosen (every entry where `hash(pdb_id) % 520 = 0`),
so it is reproducible — but it is a sample for checking *method_class* (see below), not a
representative subset. Do not quote percentages from it.

## Now ask the question properly

The honest version has to say which methods it utilizes, which needs the
second table:

> For each method_class, how many entries are there and what is the median
> resolution? Join entries to entry_types.

| method_class | entries | With resolution | SQL median |
|---|---:|---:|---:|
| diffraction | 207,603 | 207,450 | 2.00 Å |
| EM | 36,687 | 36,677 | 3.29 Å |
| NMR | 14,921 | 15 | 4.10 Å — hybrid-method entries only |
| other | 482 | 447 | 2.095 Å |

**Rechecked on the supplied snapshot, 23 September 2026:** the NMR group
includes hybrid-method depositions. Its 15 non-null values are not an NMR
resolution measure; pure `SOLUTION NMR` still has no resolution values.
Do not label that aggregate “NMR resolution”. The distinction between an
experiment string and the broader `method_class` matters here.

**What to notice:** the SQL in exercise 3b was valid, the agent did nothing wrong, and
the number was real. The asked *question* was unanswerable, and nothing in
the output said so. Deciding that "average resolution of the PDB database" must be
qualified, is *domain knowledge*. The model can not discover this from the
schema. The way to confirm the correct result: comparing `count(*)` with
`count(column)` — takes only one query.

Ask the agent to redo exercise 3b's answer as a sentence you would be willing to put
in a paper. It should name the method_class, the row count, and the exclusion.

---

# Exercise 3d — A question worth asking

Now that you can check answers, ask something real:

> For cryo-EM structures, show the median resolution per year of deposition
> from 2012 to 2024, with the number of entries each year.

| year | entries | median resolution |
|---:|---:|---:|
| 2012 | 73 | 9.20 Å |
| 2015 | 227 | 4.20 Å |
| 2019 | 1,869 | 3.50 Å |
| 2024 | 7,067 | 3.14 Å |

That is the **resolution revolution** — detector and software improvements
turning cryo-EM from a low-resolution technique into a competitor to
crystallography — visible in a table you just produced from primary data.

Apply the exercise 3c checks before believing it.<br>How many 2012 entries are there?<br>
Is a median over 73 entries the same kind of claim as one over 7,067?<br>
Did the query filter on `method_class` or on `experiment_type`, and do those two
give the same answer?<br>

Try one more of your own, and check it the same way:

- Which organisms appear most often? (Watch what happens to `Homo sapiens`
  versus `Homo sapiens; SYNTHETIC CONSTRUCT` — the field is free text, not a
  controlled vocabulary.)
- How has the share of structures solved by each method changed by decade?
- What is the resolution distribution for structures containing both protein
  and nucleic acid?

Known quirks in the data are listed in
[`PROVENANCE.md`](../../../exercises/03-mcp/data/PROVENANCE.md). Read it when a result
looks strange — several strange results are genuine.

---

# Exercise 3e — Turn your checks into a skill

You have been applying the same checks by hand. That is what skills are for.

In **Plan** mode, with `skill-builder` from Exercise 1e:

> Use skill-builder to design a skill for answering questions about the PDB
> DuckDB database. It should state which tables and columns it used, report
> the SQL and the row count with every answer, and require that any question
> about resolution says which experiment types are included. Pure NMR has
> no resolution; hybrid entries may carry one from another method. It must
> distinguish zero matching records from an empty result set: a COUNT query
> can return one row whose value is zero. Report both clearly.
> Propose it before implementing.

Build it, then re-ask an exercise 3b style question and see whether the answer arrives
with its evidence attached.

**What to notice:** the skill does not execute anything. The MCP server runs
the SQL; the skill says what a trustworthy answer has to contain. Guidance and
capability are separate, and you have now used both on the same task.

---

# Exercise 3f — Read-only is not as read-only as it sounds

The server is started in read-only mode. Test what that covers.

> Try to delete all entries with no resolution from the database.

Refused, by DuckDB itself:

```text
Cannot execute statement of type "DELETE" on database "pdb"
which is attached in read-only mode
```

`CREATE`, `UPDATE` and `ATTACH` are refused too. Now try this one:

> Run this query: COPY (SELECT 1 AS x) TO 'exercises/03-mcp/data/PROOF.parquet' (FORMAT parquet)

```bash
ls exercises/03-mcp/data/PROOF.parquet
```

**It succeeded, and a new file exists on your disk.**<br>
A read-only *database* does not mean a read-only *filesystem*.

Delete the file:

```bash
rm exercises/03-mcp/data/PROOF.parquet
```

This is the same lesson as Exercise 2's permission section: denying `edit` does
not make an agent read-only when `shell` can still modify files. A safety
property is only as broad as the mechanism enforcing it. If you want the
agent restricted, restrict the tool:

```yaml
permissions:
  - { action: 'duckdb_execute_query', resource: '*', effect: ask }
  - { action: 'duckdb_list_tables', resource: '*', effect: allow }
  - { action: 'duckdb_list_columns', resource: '*', effect: allow }
```

Add a block like that to an agent of your own from Exercise 2b and confirm it
prompts you. Check the tool names your OpenCode version actually registers —
a permission rule that matches nothing restricts nothing, and says so
nowhere.

**Take-home message:** If you have important data you must take great
care to restrict your agent from modifying it - include all tools the agent uses.
You are not necessarily informed about modification.<br>
Think about it like making a deal with the devil.

---

# Exercise 3g — When is an MCP server worth it?

Do one of your earlier questions a different way. With the server off
(`/mcps`, space to toggle it off), ask an agent with `shell` permission to
answer the same question using the `duckdb` command-line tool or Python.

Compare:

- Which was quicker to set up?
- Which action was easier for you to review before approving it?
- Which would still work on a laptop without `uv`?
- Which would you rather hand to someone else?

There is a real cost to a server when its tool definitions are included in
requests. These approximate measurements are from the workshop's earlier
configuration; exact counts depend on versions, tokenizer and exposed tools.

| Server | Tools | Tool definitions | 16384 budget | 131072 budget | 262144 budget |
|---|---:|---:|---:|---:|---:|
| `duckdb` | 4 | ~780 tokens | 4.8% | 0.6% | 0.3% |
| BioMCP 0.7.0 | 83 | ~17,377 tokens | 106.1% | 13.3% | 6.6% |

The two larger columns illustrate the server targets, not currently verified
availability. See the [context guide](../../README-fullday.md#changing-your-context-setting).
These are full-catalog **v1** measurements. V2 normally uses Code Mode,
so the table is not a measurement of the current prompt overhead. Inspect
what your run actually exposes and returns before changing limits. More
context does not guarantee better tool choice.

**What to notice:** MCP is not automatically the better option. It is worthwhile
when a capability is reusable, hard to reproduce with a shell command, and
narrow enough to stay affordable. "There is an MCP server for it" is not a
reason to connect one.

---

# Exercise 3h — Point it at your own data

Nothing you have done so far was specific to the PDB database. The MCP server takes a
database path, so give it a different one.

Build a database from a CSV you care about — one of your own files, or an
output from exercise 1. If you do not have one at hand, three are supplied
with this exercise — see below.

```bash
uv run --with duckdb python -c "
import duckdb
con = duckdb.connect('my_data.duckdb')
con.execute(\"CREATE TABLE measurements AS SELECT * FROM read_csv('my_file.csv')\")
con.close()"
```

Point the MCP server at it by editing one line in `opencode.json`:

```json
"--db-path", "my_data.duckdb",
```

Restart OpenCode — configuration is read at startup, unlike the `/mcps`
toggle — and turn the server on again. Ask the agent what tables exist, and
run the same checks from exercise 3c: how many rows, how many non-null, what does the
count tell you that the answer did not.

**What to notice:** you changed one argument. The server, the four tools and
the whole configuration were unchanged, because a DuckDB MCP server is not a
PDB tool — it is a SQL tool that Exercise 3 happened to hand a PDB database.
When you next consider adding an MCP server, ask what it is actually coupled
to, and keep its data somewhere it can be replaced.

To go back, set `--db-path` to `exercises/03-mcp/data/workshop.duckdb` again.

## If you don't have your own data, use one of these:

Three datasets are supplied in [`data/byo/`](../../../exercises/03-mcp/data/byo/).

Each hides the same mistake you found in the PDB data: **an average taken
across categories that should never have been pooled.** Three tasks come with
each. Do them in order; the third is the interesting one.

DuckDB reads the compressed files directly, so `.csv.gz` needs no unzipping.
Full sources, licences and quirks are in
[`data/byo/PROVENANCE.md`](../../../exercises/03-mcp/data/byo/PROVENANCE.md).

Each dataset gets its own database, so you can work on one without touching
the others. The command to build it sits with its tasks.

<details>
<summary><b>penguins.csv</b> — 344 rows, 15 KB, small enough to check by hand</summary>

Body measurements of three penguin species at Palmer Station, Antarctica,
2007–2009. **CC0.** Collected by Dr Kristen Gorman and Palmer Station LTER;
Gorman, Williams & Fraser (2014), *PLoS ONE* 9(3):e90081.
Source: `https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv`,
retrieved 18 September 2026, unmodified.

**Columns:** `species`, `island`, `bill_length_mm`, `bill_depth_mm`,
`flipper_length_mm`, `body_mass_g`, `sex`, `year`
Adelie 152, Gentoo 124, Chinstrap 68, across three islands.

This is the only one small enough to open in a text editor and count by hand,
which makes it the one to check your agent against.

### P1 — Load it, and find out why the average fails

Ask for the mean bill length. It fails:

```text
Binder Error: No function matches the given name and argument types
'avg(VARCHAR)'. You might need to add explicit type casts.
```

Missing values in this file are written as the string `NA`, not as empty
fields. One `NA` in a column is enough for DuckDB to decide the whole column
is text, so `bill_length_mm` arrives as `VARCHAR` and `avg()` refuses it.

**Fix it when you load the file, not in every query.** Tell DuckDB which
string means "missing":

```bash
uv run --with duckdb python -c "
import duckdb
con = duckdb.connect('exercises/03-mcp/data/penguins.duckdb')
con.execute(\"CREATE TABLE penguins AS SELECT * FROM read_csv('exercises/03-mcp/data/byo/penguins.csv', nullstr='NA')\")
con.close()"
```

`nullstr='NA'` is the whole fix. The measurement columns now load as `DOUBLE`
and `BIGINT`, the `NA`s become real SQL `NULL`s, and every penguin task below
works without casting.

Point `--db-path` at `exercises/03-mcp/data/penguins.duckdb`, restart
OpenCode, toggle `duckdb` on, and ask again. You should now get **43.9 mm**
over **342** rows.

Then ask why it is 342 and not 344. Two penguins have none of the four
measurements. Eleven have no recorded `sex`: those two, plus nine measured penguins.

**What to notice:** the data had to be repaired before it could be wrong in an
interesting way, and the repair was a decision; you told DuckDB what counts
as missing. Had you instead cast column by column inside each query, you would
have made that decision again every time, differently. Ask the agent whether
it reported the two dropped rows or just let `avg()` skip them.

### P2 — Make a plot that changes the answer

Plot bill length against bill depth, with each species in its own color.
It must work with what is already on your laptop; agree the approach before
approving an install.

Then ask for the correlation between those two measurements — overall, and
within each species:

| | correlation |
|---|---:|
| All penguins | **−0.235** |
| Adelie | **+0.391** |
| Chinstrap | **+0.654** |
| Gentoo | **+0.643** |

**The sign flips.** Pooled, deeper bills look shorter; within every single
species, deeper bills are longer. This is Simpson's paradox, and the scatter
plot shows instantly what the single number hides: three separate clouds,
each sloping up, arranged so the overall trend slopes down.

### P3 — Take an apparent result apart

Mean bill length by island: Torgersen **39.0**, Dream **44.2**, Biscoe
**45.3** mm. Ask the agent whether penguins on Biscoe have longer bills than
those on Torgersen.

Then ask which species live on each island. Torgersen has **only Adelie** —
the species with the shortest bills. The island difference is largely a
species difference wearing an island's name.

**What to notice:** nothing in the query was wrong, and the numbers are real.
Confounding is not something SQL can warn you about. Write the one-sentence
answer you would actually stand behind.

</details>

<details>
<summary><b>ncbi_reference_genomes.csv.gz</b> — 25,965 genome assemblies</summary>

NCBI RefSeq reference genomes: one row per assembly, across bacteria,
archaea, fungi, plants and animals. **Public domain** (US Government work).
Source: `https://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt`,
retrieved 18 September 2026.

**Columns:** `assembly_accession`, `organism_name`, `taxid`, `assembly_level`,
`genome_size`, `gc_percent`, `seq_rel_date`, `group`, `total_gene_count`

**It is a subset, not a sample.** The full file holds 552,279 assemblies; this
keeps the 25,965 marked `reference genome`, which are better assembled and
more studied than RefSeq as a whole. Do not quote proportions from it as if
they described all sequenced organisms.

### Load it

```bash
uv run --with duckdb python -c "
import duckdb
con = duckdb.connect('exercises/03-mcp/data/genomes.duckdb')
con.execute(\"CREATE TABLE genomes AS SELECT * FROM read_csv('exercises/03-mcp/data/byo/ncbi_reference_genomes.csv.gz')\")
con.close()"
```

DuckDB reads the `.csv.gz` directly, so there is nothing to unzip. Point
`--db-path` at `exercises/03-mcp/data/genomes.duckdb` and restart OpenCode.

### N1 — Plot something that needs a log axis

Ask for the distribution of genome size across all assemblies, as a plot.
The first attempt will almost certainly be unreadable: sizes run from
**0.11 Mb to 40,054 Mb**, five orders of magnitude, so on a linear axis
everything collapses into one bar at the left.

Get it onto a log scale, split by `group`. Median genome size in Mb:

| group | n | median Mb |
|---|---:|---:|
| archaea | 832 | 3.2 |
| bacteria | 22,736 | 4.2 |
| fungi | 668 | 32.8 |
| invertebrate | 512 | 386.7 |
| plant | 211 | 639.6 |
| vertebrate_mammalian | 269 | 2576.5 |

**What to notice:** "average genome size" across this table is a number
belonging to no organism. The plot is what makes that obvious.

### N2 — Analyze: does a bigger genome mean more genes?

Ask the agent to compare `genome_size` with `total_gene_count`. Then ask for
gene density — genes per Mb — by group:

```
archaea 1024.4   bacteria 934.2   fungi 350.5   protozoa 280.7
plant 63.5   invertebrate 45.7   vertebrate_other 20.6   vertebrate_mammalian 12.5
```

An **eighty-fold** difference in density. A mammalian genome is roughly six
hundred times the size of a bacterial one and carries only a few times more
genes, because most of it is not coding sequence.

Check the direction of the claim before accepting it: is the agent reporting
a correlation it computed, or one it already knew?

### N3 — Ask whether the data can support the question

`assembly_level` records how finished each assembly is: **Contig 9,746**,
**Complete Genome 7,268**, **Scaffold 7,228**, **Chromosome 1,723**.

Even among reference genomes, most are not complete. Ask the agent to redo
N2 using only `Complete Genome` assemblies and report whether the conclusion
survives — and by how much the numbers move.

**What to notice:** a gene count from a fragmented assembly is a weaker
measurement than one from a finished genome, and the table does not say so.
Deciding which rows are fit for the question is the analysis.

</details>

<details>
<summary><b>uniprot_human_proteins.csv.gz</b> — 20,431 reviewed human proteins</summary>

Every manually reviewed (Swiss-Prot) human protein entry. **CC BY 4.0**,
UniProt Consortium. Source:
`https://rest.uniprot.org/uniprotkb/stream?query=reviewed:true%20AND%20organism_id:9606&format=tsv&fields=accession,id,protein_name,gene_primary,length,mass,protein_existence,annotation_score`,
retrieved 18 September 2026. Reviewed entries only; the unreviewed TrEMBL set
is far larger and machine-annotated. Swap `organism_id:9606` for another
species.

**Columns:** `accession`, `entry_name`, `protein_name`, `gene`,
`length` (amino acids), `mass` (Da), `protein_existence`, `annotation_score`

### Load it

```bash
uv run --with duckdb python -c "
import duckdb
con = duckdb.connect('exercises/03-mcp/data/proteins.duckdb')
con.execute(\"CREATE TABLE proteins AS SELECT * FROM read_csv('exercises/03-mcp/data/byo/uniprot_human_proteins.csv.gz')\")
con.close()"
```

Point `--db-path` at `exercises/03-mcp/data/proteins.duckdb` and restart
OpenCode.

### U1 — Plot a distribution with a long tail

Plot protein length. Again the first attempt will be unreadable: median
**415 aa**, mean **559 aa**, maximum **34,350 aa**. Titin (`TTN`) is eighty
times the median, followed by the mucins `MUC16` at 14,507 and `MUC3B` at
13,477.

Put it on a log axis and mark the median and the mean. Ask the agent which of
the two it would quote, and why.

### U2 — Analyze: how many human proteins are there?

The obvious answer is 20,431. Ask instead how `protein_existence` is
distributed:

| protein_existence | n |
|---|---:|
| Evidence at protein level | 18,666 |
| Evidence at transcript level | 637 |
| Inferred from homology | 539 |
| Uncertain | 510 |
| Predicted | 79 |

**1,765 entries have never been observed as protein**, and 589 are Uncertain
or Predicted. The count moves by about 9% depending on what you accept as
"a protein". 148 entries also have no primary gene name.

**What to notice:** this is 3c again. The number was real, the question was
underspecified, and nothing in the result said so.

### U3 — Check the data against a physical constant

An amino acid residue averages about **110 Da**. So `mass / length` should
sit near 110 for every protein, and if it does, the two columns corroborate
each other.

Ask for the mean ratio: **111.5 Da per residue**. The data is internally
consistent.

Now ask for the entries furthest from it:

| gene | length | mass | Da/residue |
|---|---:|---:|---:|
| LORICRIN | 312 | 25,761 | 82.6 |
| PRM1 | 51 | 6,823 | 133.8 |
| ELN | 786 | 68,398 | 87.0 |

These are **not errors**. Loricrin is glycine-rich, so its residues are
unusually light; protamine PRM1 is arginine-rich and heavy; elastin is
glycine- and proline-rich. Ask the agent to explain each one and say
explicitly whether it is a data problem or biology.

**What to notice:** you just validated a dataset against something outside
it. That is a stronger check than any internal consistency test, and it is
available far more often than people use it.

</details>

---

# Exercise 3i — The other three servers

Everything so far have used one server against one local database. Three more are
configured and switched off. There are no set tasks for these: turn one on,
find out what it can do, and go as far as you like.

Toggle them the same way — `/mcps`, space, esc. **Turn on one at a time.**
When their tool definitions are included in requests, these servers have a
much larger context footprint than `duckdb`'s four tools. An unused server
can therefore add overhead without helping the task.

| Server | What it is | Tools |
|---|---|---:|
| `rcsb` | The **live PDB**. Search by keyword, sequence similarity, 3D shape or structural motif; fetch entries, ligands, assemblies, chains and interfaces; cross-reference sequences to UniProt and NCBI; render an HTML report | 38 |
| `biomcp` | **43 biomedical databases** behind one server — GWAS, gnomAD, ClinVar, dbSNP, UniProt, STRING, KEGG, Reactome, ChEMBL, AlphaFold, GTEx, PubMed, and model-organism resources | 83 |
| `opentargets` | **Target–disease associations**, over GraphQL. Which genes are implicated in which diseases, with the supporting evidence | 5 |

Full descriptions of what each exposes are in
[the server notes](../../../mcp/README.md).

**`rcsb` is the interesting one to try first**, because you already know its
data. Exercise 3 gave you a frozen PDB snapshot from 18 September 2026; this
is the same archive, live. Ask both the same question and see where they
disagree, and why. Also, try anything you couldn't do with the frozen snapshot.

**`opentargets` is the odd one out.** It does not wrap each question in its
own tool — it hands the agent a **GraphQL schema** and expects it to compose
the query. That is the same skill as writing SQL in exercise 3b, one layer up, and it
fails the same way: read the query before you approve it.

`biomcp` is the widest and the least precise. With 83 tools to choose from, a
small model picks the wrong one more often than it does with four. Its
`tool_inventory` tool is a good first request; let it tell you what it has
rather than guess.

## Go nuts

Ask a question you actually want answered. Some starting points, none of them
required:

- Which structures exist for a protein you work on, and at what resolution?
- Find structures similar in shape to one you already know.
- What is known about a disease gene: variants, interactions, pathways,
  structures, drugs?
- Is there a drug in ChEMBL against a target you care about?
- Does the live PDB agree with the frozen snapshot on cryo-EM growth?

**Keep the habits from exercise 3c.** These servers answer over the network, from
databases you did not build, and a confident paragraph is not evidence. Ask
which tool was called and what it returned. Ask how many records matched, not
just what the top one says. When an answer matters, check it at the source.
Every one of these has a website showing the same record.

Two things change when the data is remote rather than local. Your queries
leave your machine, so they are visible to whoever runs the service. And the
answer can differ tomorrow, because someone else is updating it, which is
exactly the property Exercise 3's frozen snapshot does not have, and why both
kinds exist.

---

# Epilogue

The PDB dataset is a frozen snapshot, built from public wwPDB index files on
18 September 2026. It will not match a live PDB query made later, which is
expected — and exercise 3i lets you see where it has drifted. Sources, schema
and quirks are in [`PROVENANCE.md`](../../../exercises/03-mcp/data/PROVENANCE.md), and for the three
supplied datasets in [`data/byo/PROVENANCE.md`](../../../exercises/03-mcp/data/byo/PROVENANCE.md); the MCP server
configuration and what has and has not been tested are in
[the server notes](../../../mcp/README.md).

To put the workshop back as you found it: nothing to undo in the
configuration, because `/mcps` never changed it. Delete
`exercises/03-mcp/data/workshop.duckdb` if you want the 17 MB back.

Previous: [Exercise 2 — Agents](../02-agents/README.md) · Next: [Exercise 4 — Share what you built](../04-share/README.md) · Optional: [Bonus exercises](../05-bonus/README.md).
