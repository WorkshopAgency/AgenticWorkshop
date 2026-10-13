# Exercise 1 — Skills

| | |
|---|---|
| **Time** | 30 min: 1a (12) · 1e (3) · 1f (15) |
| **Model** | `opencode/big-pickle` (default). Any chat model works |
| **Needs** | `scripts/check-setup.sh` passed. Nothing from other modules |
| **You'll learn** | Turn a repeated task into a skill: describe → discuss → build → test → improve |
| **Done when** | `/skills` lists your two skills, and each has passed one normal, one invalid and one different input that *you* checked |
| **If stuck** | `/halp 01-skills <what you tried>` |

## Before you start
Create a skill through conversation, improve it after testing, and reuse it
on another input. The examples below use protein structures, but the same
process applies to other data-analysis tasks.

Open the extracted workshop folder in OpenCode. In the terminal, start
`opencode` from that folder. Keep your exercise files inside the project.

Select **Plan** mode to discuss the task
before implementation. Select **Build** mode when you are ready to create/manipulate files.
In Desktop, use the agent selector. Review requested file changes and shell
commands in either mode; planning is not a substitute for checking permissions.
Type `/` in the terminal interface to see the available commands.

The basic pattern is: **describe → discuss → build → test → improve**.
Ask for an explanation whenever a proposed step is unclear.
The exercise set is about creating and improving skills.

# Exercise 1a — Download a PDB file

Start in **Plan** mode with a simple request:

> Create a skill that downloads a pdb file

The more precise and detailed you frame your request, the better. While a conversation will likely
reveal ambiguities and lack of detail, then having a good starting point is valuable.
Think of the AI as a real assistant you need to explain a task to.

> Create a project skill called pdb-download that downloads a PDB file
> given its entry ID. Ask me about any choices we need to make before
> implementing it.

Discuss the download source, file format, destination, and what should happen
when an ID is invalid or a file already exists. The skill should work both
when you request it directly and when an agent needs it during another task.
You will see a lot of AI feedback and you can not simply ignore it, so read it carefully.

When the proposal is clear, switch to **Build** mode:

You can write "Build it", "Proceed", "Implement" or any words to that effect - or be more precise

> Implement the agreed pdb-download skill in
> .opencode/skills/pdb-download/SKILL.md. Keep supporting files in that
> skill's folder and ask before overwriting existing work.

OpenCode discovers skills when it loads the project. Type `/skills` in the
chat. If the new skill is missing, run `opencode reload` in a terminal from
the workshop folder, or exit and reopen OpenCode. Then try it:

The simple

>Download pdb 4HHB

will successfully download the entry in the main workshop folder. If dissatisfied with that, be precise

> Use the pdb-download skill to download 4HHB into outputs/01-skills/pdb.

Inspect the saved file. A successful HTTP request alone does not tell you
whether the response is the expected structure file rather than an error page.
It is important to note that only **Build** allows for pdb downloading, as that is file manipulation.

Return to **Plan** and improve the skill:

> Review pdb-download. Propose checks that the downloaded file can be
> parsed, contains atomic coordinates, and corresponds to the requested
> entry. If the source publishes a checksum for that exact file, compare
> against it. Otherwise say that source-checksum verification is unavailable;
> do not invent a checksum. Explain the changes before implementing them.

Approve the changes in **Build**, then test again. Try a different valid ID
and an invalid input.<br>
A list of several IDs is supplied in
[`pdb_to_download.txt`](pdb_to_download.txt). One of them is deliberately invalid:

> Use the pdb-download skill to download the entries listed in
> exercises/01-skills/pdb_to_download.txt into outputs/01-skills/pdb.

**What to notice:** Useful checks emerge from discussing and testing the task.
A locally computed hash is a file fingerprint, not proof that it matches the
source. Keep unrelated tasks in separate skills rather than growing one skill
to cover everything.

# Exercise 1e — A skill that helps make skills

Inspect [skill-builder](../../.opencode/skills/skill-builder/SKILL.md).
It helps an agent clarify a skill's purpose, write useful instructions,
choose supporting files, and check the result. It is itself a skill, not
a separate agent or a newly trained model.

Example request in OpenCode **Plan** mode:

> Use skill-builder to review the pdb-download skill. Explain which
> instructions are useful, what is missing, and how we could test it.
> Propose changes before implementing them.

Finalize the improved skill in the usual way, if there is anything to improve.

# Exercise 1f — Make and test your own data-analysis skill

Build a skill for a task every analysis starts with: **profiling a table
before trusting it**. The suggested skill is `csv-profile`. It reports row and
column counts, column types, missing values per column (including text
markers such as `NA`), units where the provenance states them, and counts
per group for a named column. You may choose another small task you repeat
in your own work instead.

Start in **Plan** mode:

> Use skill-builder to design a project skill called csv-profile that
> profiles a CSV or CSV.GZ file before analysis: rows, columns, types,
> missing values (including text markers such as NA), and counts per
> group for a column I name. It must use only what is on my laptop and
> write its report to outputs/01-skills/. Ask me about choices first.

Review the proposal before switching to Build mode and authorizing
implementation. Then test it on three inputs:

| Test | Input | What a correct skill does |
|---|---|---|
| Normal | `exercises/03-mcp/data/byo/uniprot_human_proteins.csv.gz`, grouped by `protein_existence` | Reports counts you can confirm yourself |
| Invalid | a file name that does not exist | Says so; invents no profile |
| Different | `exercises/03-mcp/data/byo/penguins.csv`, grouped by `species` | Finds the `NA` markers: 2 rows with no measurements; 11 rows without `sex` (those 2 plus 9 measured ones) |

The data provenance is in
[`PROVENANCE.md`](../03-mcp/data/byo/PROVENANCE.md).

The skill belongs in `.opencode/skills/<skill-name>/SKILL.md`. Give each skill
its own subfolder. Add scripts, references, or assets only when they help.

Inspect the outputs yourself. Record what passed and what you have not
tested, then revise the skill in response to actual failures. Exercise 2b
uses a profiling skill; it supplies its own copy, so you do not need to
finish this one first.

# Epilogue
Read the `SKILL.md` file with a text editor to see what the skill contains.
You can add/modify instructions directly yourself if you prefer to do it without the AI.
This can be done both at very simple and very complex levels.<br>
Source: [https://www.skillsdirectory.com/docs/skill-md-format](https://www.skillsdirectory.com/docs/skill-md-format)

More skills exercises (1b–1d) are in the [full-day version](../../_sectionday/exercises/01-skills/README.md#exercise-1b--download-an-existing-structure-image).

Next: [Exercise 2 — Agents](../02-agents/README.md).
