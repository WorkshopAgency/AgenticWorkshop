# Exercise 4 — MCP: connect a database yourself, then check what it tells you

| | |
|---|---|
| **Model** | Qwenstorm, `dtu/qwen36` (default); on your own, a free model. Any chat model works |
| **Needs** | `scripts/check-setup.sh` passed, and `uv` (`uv --version`). Nothing from other modules |
| **You'll learn** | What MCP adds, how to connect a server, and why "connected" and "the query ran" are not "the answer is right" |
| **Done when** | `/mcps` shows `duckdb` connected, and your agent's numbers match the checkpoints at the bottom |
| **If stuck** | `/halp 04-mcp <what you tried>` |

## Why MCP

An agent can only do what its tools allow. **MCP** (Model Context Protocol)
is a standard way to give OpenCode a new tool that lives *outside* it: a
database, a public data service, a lab system. The server is a separate
program; OpenCode starts it, or connects to it, and the agent sees its
functions as extra tools.

Compare: a skill is instructions the model reads, a plugin is code inside
OpenCode, and an MCP server is a separate program the agent talks to.

Here the server is **DuckDB**, running on your laptop and answering SQL
against a local database file. The file stays on your laptop, but every
query result the agent reads is sent to the model you selected.

# Exercise 4a — Connect it

**Do:** from the workshop folder, build the database. It holds a PDB snapshot
(259,693 entries) and the Palmer penguins table:

```bash
uv run --with "duckdb<2" python exercises/04-mcp/scripts/make_db.py
```

Fetch the server once, so its first use is not a silent 30 MB download (side effect is showing the help):

```bash
uvx mcp-server-motherduck@1.0.8 --help
```

Start OpenCode and type `/mcps`. Four servers are listed, all switched off.
Select **`duckdb`** only, press **space**, then **esc**. Type `/mcps` again.

**Look for:** `duckdb` **Connected ✓**.

**Why:** "connected" only means a process started and answered a handshake.
The database is opened when the first query arrives, so connected is not the
same as working. Leave the other three servers off: every connected server
adds its tool descriptions to the context, whether you use them or not.

# Exercise 4b — Ask something you cannot see

**Do:** in Build:

> Using the duckdb tools, what is the mean bill length of the penguins in
> the database, and how many penguins does that mean include?

**Look for:** watch the tool calls. The first query will probably fail. Read
the error, then see what the agent does about it: does it explain **why** it
failed, and does it tell you how many rows it left out?

**Why:** you cannot see the table, only what the agent tells you about it.
A query that runs is not an answer that is right; how missing values were
treated is a decision, and you want to know who made it.

# Exercise 4c — Make a plot that changes the answer

**Do:**

> Is bill depth related to bill length? Using the duckdb tools, give the
> correlation, then write the plot as a single self-contained SVG file to
> outputs/04-mcp/bill.svg. Write the SVG directly; do not install or import
> any plotting package.

Open/drag the SVG in your browser. Then ask:

> Now give the same correlation within each species, and write a second
> SVG, outputs/04-mcp/bill-by-species.svg, coloured by species with one fit
> per species.

**Look for:** compare the two answers and the two plots. Which one would you
put in a paper, and what would you write in one sentence?

**Why:** asking for SVG keeps the plot independent of what is installed on
your laptop; an open-ended "make a plot" can spend minutes looking for
plotting libraries. And a single number can hide groups that behave
differently: look before you conclude. If you also do
[Exercise 5](../05-decide/README.md), you can give it the agent's description
of your first plot; that is optional, Exercise 5 supplies its own examples.

<details>
<summary><b>Checkpoints</b> (open after you have your own answer)</summary>

- Loaded as shipped, the measurement columns are text: missing values are the
  string `NA`, so `avg()` fails with `avg(VARCHAR)`. Treating `NA` as missing
  gives **43.9 mm over 342 penguins**. Two of the 344 have no measurements.
- Pooled correlation of bill length and depth: **−0.235**. Within species:
  Adelie **+0.391**, Chinstrap **+0.654**, Gentoo **+0.643**. The sign flips:
  Simpson's paradox. One regression line across all penguins is a misleading
  plot even though every number in it is correct.
</details>

## What to notice

- MCP turns an outside program into tools the agent can call. The data stays
  where it is; the results travel to the model.
- "Connected", "the query ran" and "the answer is right" are three different
  claims.
- Correct numbers can still make a misleading picture.

**Discuss with your neighbour:**

1. Which database or service from your own work would you connect this way?
2. What would you check before trusting an agent's SQL on your data?
3. When is it simpler to export a CSV and skip MCP altogether?

The other three configured servers (`rcsb`, `biomcp`, `opentargets`) are
described in [mcp/README.md](../../mcp/README.md).

# === Dive Deeper ===

These steps use the PDB tables in the database you built in 4a (`entries`
and `entry_types`), with the `duckdb` server switched on.

# Exercise 4d — Find out whether the answer is true

**Do:** ask:

> Using the duckdb tools, what is the average resolution of the structures
> in the entries table?

Then ask:

> How many rows are in entries, and how many of them actually have a
> resolution value? Show me both numbers. Then group the entries with no
> resolution value by experiment type.

**Look for:** 259,693 rows, but only 244,589 with a resolution. The average
silently left out 15,104 entries: `count(*)` counts rows, while
`count(column)` and `avg()` skip missing values. Are the missing ones a
random 6 %?

**Why:** they are not. Solution NMR has no resolution at all; the idea does
not apply to the method. All 14,668 `SOLUTION NMR` entries are missing it.
The SQL was valid and the number was real, but the question, "the average
resolution of the PDB", could not be answered as asked, and nothing in the
output said so. Comparing `count(*)` with `count(column)` takes one query.

<details>
<summary>Check it yourself, without the agent</summary>

`exercises/04-mcp/data/pdb_sample.csv` holds 512 entries, small enough to
open. This counts its blanks:

```bash
python3 -c "
import csv
rows = list(csv.DictReader(open('exercises/04-mcp/data/pdb_sample.csv')))
blank = [r for r in rows if r['resolution'] == '']
print('rows:', len(rows), ' blank resolution:', len(blank))
print(set(r['experiment_type'] for r in blank))
"
```

```text
rows: 512  blank resolution: 26
{'SOLUTION NMR'}
```

The sample is chosen by a fixed rule, so it is reproducible, but it is not
representative: do not quote percentages from it.

</details>

Now ask the question properly:

> For each method_class, how many entries are there, how many have a
> resolution, and what is the median resolution? Join entries to entry_types.

| method_class | entries | with resolution | median |
|---|---:|---:|---:|
| diffraction | 207,603 | 207,450 | 2.00 Å |
| EM | 36,687 | 36,677 | 3.29 Å |
| NMR | 14,921 | 15 | 4.10 Å |
| other | 482 | 447 | 2.095 Å |

The 15 NMR values come from hybrid-method entries, not from NMR itself, so do
not call that median "NMR resolution". Finally, ask the agent to write the
answer as a sentence you would put in a paper: it should name the method
class, the row count and what was left out.

# Exercise 4e — A question worth asking

**Do:** ask:

> For cryo-EM structures, show the median resolution per year of deposition
> from 2012 to 2024, with the number of entries each year.

**Look for:**

| year | entries | median |
|---:|---:|---:|
| 2012 | 73 | 9.20 Å |
| 2015 | 227 | 4.20 Å |
| 2019 | 1,869 | 3.50 Å |
| 2024 | 7,067 | 3.14 Å |

Apply the 4d checks before believing it. Is a median over 73 entries the same
kind of claim as one over 7,067? Did the query filter on `method_class` or on
`experiment_type`, and do the two give the same answer?

**Why:** this is the cryo-EM "resolution revolution" (Kühlbrandt, 2014), seen
in a table you produced from primary data. Try one more question of your own
and check it the same way, for example which organisms appear most often
(`source_organism` is free text: watch `Homo sapiens` against
`Homo sapiens; SYNTHETIC CONSTRUCT`). Known quirks of the data are in
[`data/PROVENANCE.md`](data/PROVENANCE.md); several strange results are
genuine.

# Exercise 4f — Turn your checks into a skill

**Do:** in **Plan**, with `skill-builder` from
[Exercise 2b](../02-skills/README.md):

> Use skill-builder to design a skill for answering questions about the PDB
> tables in the DuckDB database. It should state which tables and columns it
> used, report the SQL and the row count with every answer, and require that
> any question about resolution says which experiment types are included.
> Pure NMR has no resolution; hybrid entries may carry one from another
> method. It must tell zero matching records from an empty result: a COUNT
> query returns one row whose value can be zero. Propose it before
> implementing.

Build it, then ask a 4d-style question again.

**Look for:** does the answer now arrive with its evidence: tables, SQL, row
counts and what was excluded?

**Why:** the skill does not run anything. The MCP server runs the SQL; the
skill says what a trustworthy answer has to contain. Guidance and capability
are separate, and here you use both on the same task.

# Exercise 4g — Read-only is not as read-only as it sounds

**Do:** the server runs in read-only mode. Ask:

> Using the duckdb tools, delete all entries with no resolution.

Then:

> Using the duckdb tools, run this query: COPY (SELECT 1 AS x) TO
> 'exercises/04-mcp/data/PROOF.parquet' (FORMAT parquet)

and check in a terminal:

```bash
ls exercises/04-mcp/data/PROOF.parquet
rm exercises/04-mcp/data/PROOF.parquet
```

**Look for:** the DELETE is refused by DuckDB itself ("attached in read-only
mode"), and so is `CREATE`. The `COPY` succeeds, and a new file appears on
your disk.

**Why:** a read-only *database* is not a read-only *filesystem*. It is the
same lesson as permissions in Exercise 3: a safety property is only as broad
as the mechanism enforcing it. To restrict the agent, restrict the tool, in
an agent of your own from [Exercise 3d](../03-agents/README.md):

```yaml
permissions:
  - { action: duckdb_execute_query, resource: '*', effect: ask }
  - { action: duckdb_list_tables, resource: '*', effect: allow }
  - { action: duckdb_list_columns, resource: '*', effect: allow }
```

Add it and confirm that a query now asks you first. A rule whose name matches
no tool restricts nothing and says so nowhere. Even a matching rule covers
only that tool: an agent that may run shell commands or Python can open the
same file another way. With important data, restrict every route.

# Exercise 4h — When is an MCP server worth it?

**Do:** answer one of your earlier questions a different way. Switch the
server off (`/mcps`, space), and ask Build to answer the same question with
the `duckdb` command-line tool or with Python.

**Look for:** which was quicker to set up, which action was easier to review
before you approved it, and which you would rather hand to someone else.

**Why:** a server is not free. Its tool descriptions are part of what the
model is given: `duckdb` has 4 tools, `rcsb` 38 and `biomcp` 83. MCP is
worthwhile when a capability is reusable, hard to reproduce with a shell
command, and narrow enough to stay affordable. "There is an MCP server for
it" is not a reason to connect one.

# Exercise 4i — Point it at your own data

**Do:** the server is a SQL tool, not a PDB tool, so give it another
database. Build one from a CSV you care about:

```bash
uv run --with "duckdb<2" python -c "
import duckdb
con = duckdb.connect('my_data.duckdb')
con.execute(\"CREATE TABLE measurements AS SELECT * FROM read_csv('my_file.csv')\")
con.close()"
```

Use `"duckdb<2"` as shown: the server cannot read files written by DuckDB 2.
In `opencode.json`, change the server's `--db-path` to `my_data.duckdb`, run
`opencode reload`, and start a new chat with the server switched on. Ask
which tables exist, then run the 4d checks: how many rows, how many non-null,
and what the count tells you that the answer did not.

**Look for:** you changed one argument. The server, its four tools and the
rest of the configuration stayed the same.

**Why:** when you next consider an MCP server, ask what it is coupled to, and
keep its data somewhere it can be replaced. To go back, set `--db-path` to
`exercises/04-mcp/data/workshop.duckdb` again.

No data of your own at hand? Three datasets are supplied in
[`data/byo/`](data/byo/), with sources, licences and quirks in
[`data/byo/PROVENANCE.md`](data/byo/PROVENANCE.md). Each hides the same
mistake as 4d, an average across groups that should never have been pooled.
DuckDB reads the `.csv.gz` files directly.

<details>
<summary><b>penguins.csv</b>: is it the island or the species?</summary>

You met this file in 4b and 4c. Load it with the `NA` fix, as its own
database:

```bash
uv run --with "duckdb<2" python -c "
import duckdb
con = duckdb.connect('exercises/04-mcp/data/penguins.duckdb')
con.execute(\"CREATE TABLE penguins AS SELECT * FROM read_csv('exercises/04-mcp/data/byo/penguins.csv', nullstr='NA')\")
con.close()"
```

Point `--db-path` at it. The mean bill length by island is Torgersen
**39.0**, Dream **44.2** and Biscoe **45.3** mm. Ask the agent whether
penguins on Biscoe have longer bills than those on Torgersen, then ask which
species live on each island. Torgersen has **only Adelie**, the species with
the shortest bills: the island difference is largely a species difference.
Nothing in the query was wrong; confounding is not something SQL can warn
you about.

</details>

<details>
<summary><b>ncbi_reference_genomes.csv.gz</b>: 25,965 genome assemblies</summary>

NCBI RefSeq reference genomes, one row per assembly. It is a subset (the
assemblies marked "reference genome"), not a sample: do not quote proportions
from it as if they described all sequenced organisms.

```bash
uv run --with "duckdb<2" python -c "
import duckdb
con = duckdb.connect('exercises/04-mcp/data/genomes.duckdb')
con.execute(\"CREATE TABLE genomes AS SELECT * FROM read_csv('exercises/04-mcp/data/byo/ncbi_reference_genomes.csv.gz')\")
con.close()"
```

1. **A plot that needs a log axis.** Genome sizes run from 0.11 Mb to
   40,054 Mb. Ask for a plot by `group` on a log scale. Median sizes:
   archaea 3.2, bacteria 4.2, fungi 32.8, invertebrate 386.7, plant 639.6,
   vertebrate_mammalian 2,576.5 Mb. An "average genome size" across them
   belongs to no organism.
2. **Does a bigger genome mean more genes?** Ask for the median gene density
   (genes per Mb) by group: from about 1,024 in archaea down to 12.5 in
   mammals. Is the agent reporting a number it computed, or one it already
   knew?
3. **Can the data support the question?** `assembly_level` is Contig 9,746,
   Complete Genome 7,268, Scaffold 7,228, Chromosome 1,723. Redo 2 with
   complete genomes only, and see how far the numbers move.

</details>

<details>
<summary><b>uniprot_human_proteins.csv.gz</b>: 20,431 reviewed human proteins</summary>

```bash
uv run --with "duckdb<2" python -c "
import duckdb
con = duckdb.connect('exercises/04-mcp/data/proteins.duckdb')
con.execute(\"CREATE TABLE proteins AS SELECT * FROM read_csv('exercises/04-mcp/data/byo/uniprot_human_proteins.csv.gz')\")
con.close()"
```

1. **A long tail.** Protein length: median 415, mean 559, maximum 34,350
   amino acids (titin, `TTN`). Plot it on a log axis and ask which of median
   and mean the agent would quote, and why.
2. **How many human proteins are there?** The obvious answer is 20,431. Ask
   how `protein_existence` is distributed: 18,666 have evidence at protein
   level, and 1,765 have never been observed as protein. The count moves by
   about 9 % depending on what you accept as "a protein".
3. **Check against a physical constant.** A residue weighs about 110 Da, and
   the mean of `mass / length` is 111.5. The furthest from it are loricrin
   (82.6), protamine PRM1 (133.8) and elastin (87.0). Ask whether each is a
   data error or biology. They are biology: glycine-rich, arginine-rich and
   glycine- and proline-rich.

</details>

# Exercise 4j — The other three servers

**Do:** switch on one of the other servers with `/mcps` (one at a time), find
out what it can do, and ask it something you want to know.

| Server | What it is | Tools |
|---|---|---:|
| `rcsb` | The **live PDB**: search by keyword, sequence, 3D shape or motif; fetch entries, ligands and assemblies | 38 |
| `biomcp` | 43 public biomedical databases behind one server, from PubMed and UniProt to ClinVar, gnomAD and Reactome | 83 |
| `opentargets` | Target–disease associations, by composing GraphQL queries | 5 |

**Look for:** with `rcsb`, ask the live PDB and the frozen snapshot from 4a
the same question, and see where they disagree and why. With `opentargets`,
read the GraphQL query before you approve it, as you read the SQL. With
`biomcp`, start with its `tool_inventory` tool.

**Why:** keep the habits from 4d. These servers answer over the network from
databases you did not build: ask which tool was called and what it returned,
and how many records matched. Your queries leave your laptop, and the answer
can change tomorrow because someone else updates the data, which is exactly
what the frozen snapshot does not do. More about each server is in
[mcp/README.md](../../mcp/README.md).

Previous: [Exercise 3 — Agents](../03-agents/README.md) · Next: [Exercise 5 — Decision model](../05-decide/README.md).
