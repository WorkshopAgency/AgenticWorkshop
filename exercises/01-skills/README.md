# Exercise 1 — Skills

| | |
|---|---|
| **Time** | 30 min: 1a (12) · 1e (3) · 1f (15) |
| **Model** | `opencode/big-pickle` (default). Any chat model works |
| **Needs** | `scripts/check-setup.sh` passed. Nothing from other modules |
| **You'll learn** | Turn a repeated task into a skill: describe → discuss → build → test → improve |
| **Done when** | `/skills` lists your two skills, and each has passed one normal, one invalid and one different input that *you* checked |
| **If stuck** | `/halp 01-skills <what you tried>` |

## Why skills

Every time you start a new chat, the model starts from nothing. If you
download a structure, profile a table or run a QC check the same way every
week, you would explain it again every week, and get a slightly different
result each time.

A **skill** writes the procedure down once: a short instruction file,
`SKILL.md`, plus any scripts it needs, in a folder OpenCode knows. The agent
loads it when a task matches its description. A skill is not a new model and
not a program on its own; it is instructions the model reads when it needs
them.

The pattern for this exercise is **describe → discuss → build → test →
improve**. The model is your assistant: the clearer you explain the task, the
better the skill.

## Before you start

Open the workshop folder in OpenCode: in a terminal, `cd` into it and type
`opencode`. Keep your exercise files inside the project.

OpenCode has two main agents, and you switch between them with
**shift+tab** (in Desktop, with the agent selector):

- **Plan** reads and discusses. It reads files without asking, and cannot
  run commands or create or change files.
- **Build** does the work: it writes files and runs commands, and asks you
  first.

When Build wants to write a file or run a command, OpenCode shows a prompt
with three choices. **Allow once** is the safe default. **Always allow**
stops it asking again for that kind of action. **Reject** refuses,
and the agent has to find another way. Read what it wants to do before you
choose; planning first is not a substitute for checking the prompts.

Type `/` in the chat to see all commands.

# Exercise 1a — Download a PDB file

## Ask for a skill, and let it ask you back (4 min)

**Do:** in **Plan**, start simply:

> Create a skill that downloads a pdb file

Then compare with a more precise request:

> Create a project skill called pdb-download that downloads a PDB file
> given its entry ID. Ask me about any choices we need to make before
> implementing it.

**Look for:** questions about the download source, the file format (legacy
PDB or mmCIF), where to save it, and what to do with an invalid ID or a file
that already exists. Answer them, or ask for its recommendation. Read the
proposal carefully; you will be asked to approve what it builds.

**Why:** the more precise your request, the better the start; the
conversation finds the gaps neither of you thought about. Think of the AI as
a real assistant you need to explain a task to. The skill should work both
when you ask for it directly and when an agent needs it in another task.

## Build it (3 min)

**Do:** switch to **Build** and ask it to implement what you agreed:

> Implement the agreed pdb-download skill in
> .opencode/skills/pdb-download/SKILL.md. Keep supporting files in that
> skill's folder and ask before overwriting existing work.

Approve the file it wants to write. Then type `/skills` in the chat. If
`pdb-download` is missing, run `opencode reload` in a terminal in the
workshop folder, then start a new chat.

**Look for:** a folder `.opencode/skills/pdb-download/` with `SKILL.md` and
perhaps a script. Open `SKILL.md`: a short header with `name` and
`description`, then the instructions.

**Why:** the `description` is what the agent reads to decide *whether* to use
the skill, so it matters more than it looks.

## Use it, and check what you got (3 min)

**Do:**

> Use the pdb-download skill to download 4HHB into outputs/01-skills/pdb.

Then the list of IDs supplied in [`pdb_to_download.txt`](pdb_to_download.txt),
where one is deliberately invalid:

> Use the pdb-download skill to download the entries listed in
> exercises/01-skills/pdb_to_download.txt into outputs/01-skills/pdb.

**Look for:** open the saved files. Is each one really a structure, with
atom records, or could it be an error page saved under a structure-file name? Did it
report the invalid ID, or quietly skip it?

**Why:** a successful download is not the same as the right file. "The
request worked" and "I have a structure" are two different claims.

## Improve it (2 min)

**Do:** back in **Plan**:

> Review pdb-download. Propose checks that the downloaded file can be
> parsed, contains atomic coordinates, and corresponds to the requested
> entry. If the source publishes a checksum for that exact file, compare
> against it. Otherwise say that source-checksum verification is unavailable;
> do not invent a checksum. Explain the changes before implementing them.

Approve the changes in **Build**, then test again with a different valid ID
and an invalid one.

**Why:** useful checks come from discussing and testing the task, not from
the first draft. A checksum you computed yourself is a fingerprint of your
file, not proof that it matches the source.

# Exercise 1e — A skill that helps make skills (3 min)

**Do:** open [skill-builder](../../.opencode/skills/skill-builder/SKILL.md)
and skim it. Then, in **Plan**:

> Use skill-builder to review the pdb-download skill. Explain which
> instructions are useful, what is missing, and how we could test it.
> Propose changes before implementing them.

**Look for:** the tool calls should show the agent loading `skill-builder`
before answering. If it suggests improvements you agree with, apply them in
Build.

**Why:** skill-builder is itself just a skill: instructions for writing good
instructions. Skills can build on each other.

# Exercise 1f — Make and test your own data-analysis skill (15 min)

Every analysis should start with the same question: **can I trust this
table?** Build a skill that profiles a table before anyone computes anything
from it. The suggested skill is `csv-profile`; you may choose another small
task you repeat in your own work instead.

## Design and build it (7 min)

**Do:** in **Plan**:

> Use skill-builder to design a project skill called csv-profile that
> profiles a CSV or CSV.GZ file before analysis: rows, columns, types,
> missing values (including text markers such as NA), and counts per
> group for a column I name. It must use only what is on my laptop and
> write its report to outputs/01-skills/. Ask me about choices first.

Answer its questions, then switch to **Build** and ask it to implement the
design.

**Look for:** a folder `.opencode/skills/csv-profile/` with `SKILL.md` and
probably a Python script. The agent may run a first test on its own; read
what it tested.

## Test it on three inputs (6 min)

**Do:** start a new chat in **Build** and ask for each of these:

| Test | Ask it to profile | What a correct skill does |
|---|---|---|
| Normal | `exercises/03-mcp/data/byo/uniprot_human_proteins.csv.gz`, grouped by `protein_existence` | Reports counts you can confirm yourself |
| Invalid | a file name that does not exist | Says so; invents no profile |
| Different | `exercises/03-mcp/data/byo/penguins.csv`, grouped by `species` | Finds the `NA` markers: 2 rows with no measurements; 11 rows without `sex` (those 2 plus 9 measured ones) |

If it says a report already exists, decide whether to overwrite it: a skill
that asks before replacing your results is doing its job.

**Look for:** check at least one number yourself, for example the penguin
`NA` counts. The data provenance is in
[`PROVENANCE.md`](../03-mcp/data/byo/PROVENANCE.md).

**Why:** three inputs test three different things: that it works, that it
fails honestly, and that it was not written for one file only. Record what
passed and what you have not tested, then fix the skill where it actually
failed.

## What to notice

- A skill is a folder: `SKILL.md` plus whatever scripts it needs. Read it; you
  can edit it by hand as well as through the agent.
- The `description` decides when the skill is used; the instructions decide
  how.
- Plan discusses, Build acts, and every action is a prompt you can read.
- "It ran" is not "it is right". Your checks, not the agent's summary, are the
  evidence.

**Discuss with your neighbour:**

1. What would you have missed if you had accepted the first version of
   `pdb-download`?
2. Which task from your own work would make a good skill, and what three
   inputs would you test it on?
3. When would you rather write a plain script than a skill?

Exercise 2b uses a profiling skill too; it supplies its own copy, so you do
not need to finish 1f first. The skill file format is described at
[skillsdirectory.com](https://www.skillsdirectory.com/docs/skill-md-format).

# Optional extra — a notebook inside OpenCode (8 min)

For when you finish early. A plugin,
[opencode-notebook](https://github.com/dskanakoglou/opencode-notebook), adds a
Jupyter-style notebook panel next to the chat. You and the agent share one
live Python kernel: either of you can run cells, and both see the outputs. A
plugin is code that runs inside OpenCode; Exercise 2 says more.

**Do:**

1. Install it, unless you already did in Exercise 0: in a terminal in the
   workshop folder, clone it into this project's plugin folder, then quit
   OpenCode (`ctrl+c`) and start it again:

   ```bash
   git clone -q --depth 1 --branch v0.1.1 https://github.com/dskanakoglou/opencode-notebook .opencode/plugins/opencode-notebook
   ```

   Git notes that the tag "is not a commit" and that you are on a "detached
   HEAD"; both are expected.
2. In **Build**, in a new chat:

   > Write outputs/01-skills/penguins.py as a notebook with # %% cells that
   > profiles exercises/03-mcp/data/byo/penguins.csv: its shape, missing
   > values per column, penguins per species, and a scatter plot of bill
   > length against bill depth. List pandas and matplotlib in a
   > # /// script block. Then run it with notebook_run.

3. Open the panel with `/notebook outputs/01-skills/penguins.py`. Move with
   `↑` `↓`, run a cell with `r`, all of them with `a`, open a plot with `o`.
4. Mark the missing-values cell with `space`, go back to the chat with
   `ctrl+x ←`, and ask:

   > Look at the cell I marked: which columns have missing values?

**Look for:** writing `penguins.py` asked for your approval; running it with
`notebook_run` did not. The first run downloads the kernel's packages (about
400 MB), so it can take a minute. The top of the panel names your terminal and
says whether it can draw plots there; elsewhere `o` opens them.

**Why:** a plugin's tools run without OpenCode's approval prompt, even under a
rule that says "ask". That is why `notebook_run` only runs notebooks under
`outputs/`, and why you read a plugin before you install it. To remove it,
delete `.opencode/plugins/opencode-notebook` and restart OpenCode.

Next: [Exercise 2 — Agents](../02-agents/README.md).
