# Exercise 3 — MCP: connect a database yourself, then check what it tells you

| | |
|---|---|
| **Time** | 10 min |
| **Model** | `opencode/big-pickle` (default). Any chat model works |
| **Needs** | `scripts/check-setup.sh` passed, and `uv` (`uv --version`). Nothing from other modules |
| **You'll learn** | What MCP adds, how to connect a server, and why "connected" and "the query ran" are not "the answer is right" |
| **Done when** | `opencode mcp list` shows `duckdb` connected, and your agent's numbers match the checkpoints at the bottom |
| **If stuck** | `/halp 03-mcp <what you tried>` |

**MCP** (Model Context Protocol) is a standard way to give OpenCode a capability
that lives outside it. Here it is a **DuckDB** server that runs on your laptop
and answers SQL against a local database file. The file stays on your laptop,
but query results that the agent reads are sent to the model you selected.

## 1. Connect it (3 min)

From the workshop root, build the database. It holds a PDB snapshot (259,693
entries) and the Palmer penguins table:

```bash
uv run --with duckdb python exercises/03-mcp/scripts/make_db.py
```

Fetch the server once, so its first use is not a silent 30 MB download:

```bash
uvx mcp-server-motherduck@1.0.8 --help
```

Start OpenCode and type `/mcps`. Four servers are listed, all disabled.
Select **`duckdb`** only, press **space**, then **esc**. Check in a terminal:

```bash
opencode mcp list
```

You want `duckdb` **connected**. That only means a process started and
answered a handshake. The database is opened when the first query arrives.

## 2. Ask something you cannot see (3 min)

> Using the duckdb tools, what is the mean bill length of the penguins in
> the database, and how many penguins does that mean include?

Watch the tool calls. The first query will probably fail. Read the error, then
see what the agent does about it: does it explain **why** it failed, and does
it tell you how many rows it left out?

## 3. Make a plot that changes the answer (4 min)

> Is bill depth related to bill length? Using the duckdb tools, give the
> correlation, then write the plot as a single self-contained SVG file to
> outputs/03-mcp/bill.svg. Write the SVG directly; do not install or import
> any plotting package.

Open the SVG in your browser. Asking for SVG keeps the plot independent of
what is installed on your laptop; an open-ended "make a plot" can spend
minutes looking for plotting libraries.

Then ask:

> Now give the same correlation within each species, and write a second
> SVG, outputs/03-mcp/bill-by-species.svg, coloured by species with one fit
> per species.

Compare the two answers. Which one would you put in a paper, and what would
you write in one sentence? If you also do [Exercise 4](../04-decide/README.md),
you can give it the agent's description of your first plot. That is optional;
Exercise 4 supplies its own examples.

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

## After the workshop

- The other three configured servers (`rcsb`, `biomcp`, `opentargets`):
  [mcp/README.md](../../mcp/README.md).

Previous: [Exercise 2 — Agents](../02-agents/README.md) · Next: [Exercise 4 — Decision model](../04-decide/README.md).
