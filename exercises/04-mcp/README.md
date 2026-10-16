# Exercise 4 — MCP: connect a database yourself, then check what it tells you

| | |
|---|---|
| **Time** | 10 min |
| **Model** | `opencode/big-pickle` (default). Any chat model works |
| **Needs** | `scripts/check-setup.sh` passed, and `uv` (`uv --version`). Nothing from other modules |
| **You'll learn** | What MCP adds, how to connect a server, and why "connected" and "the query ran" are not "the answer is right" |
| **Done when** | `opencode mcp list` shows `duckdb` connected, and your agent's numbers match the checkpoints at the bottom |
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

## 1. Connect it (3 min)

**Do:** from the workshop folder, build the database. It holds a PDB snapshot
(259,693 entries) and the Palmer penguins table:

```bash
uv run --with duckdb python exercises/04-mcp/scripts/make_db.py
```

Fetch the server once, so its first use is not a silent 30 MB download:

```bash
uvx mcp-server-motherduck@1.0.8 --help
```

Start OpenCode and type `/mcps`. Four servers are listed, all switched off.
Select **`duckdb`** only, press **space**, then **esc**. Check in a terminal:

```bash
opencode mcp list
```

**Look for:** `duckdb` **connected**.

**Why:** "connected" only means a process started and answered a handshake.
The database is opened when the first query arrives, so connected is not the
same as working. Leave the other three servers off: every connected server
adds its tool descriptions to the context, whether you use them or not.

## 2. Ask something you cannot see (3 min)

**Do:** in Build:

> Using the duckdb tools, what is the mean bill length of the penguins in
> the database, and how many penguins does that mean include?

**Look for:** watch the tool calls. The first query will probably fail. Read
the error, then see what the agent does about it: does it explain **why** it
failed, and does it tell you how many rows it left out?

**Why:** you cannot see the table, only what the agent tells you about it.
A query that runs is not an answer that is right; how missing values were
treated is a decision, and you want to know who made it.

## 3. Make a plot that changes the answer (4 min)

**Do:**

> Is bill depth related to bill length? Using the duckdb tools, give the
> correlation, then write the plot as a single self-contained SVG file to
> outputs/04-mcp/bill.svg. Write the SVG directly; do not install or import
> any plotting package.

Open the SVG in your browser. Then ask:

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

Previous: [Exercise 3 — Agents](../03-agents/README.md) · Next: [Exercise 5 — Decision model](../05-decide/README.md).
