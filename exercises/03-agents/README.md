# Exercise 3 — Agents

| | |
|---|---|
| **Model** | The one you select: Qwenstorm (`dtu/qwen36`) in the workshop, a free model on your own. The workshop agents have no model of their own, so they follow your choice. 3d: your choice |
| **Needs** | `scripts/check-setup.sh` passed. opencode-sidebar-plus from Exercise 0 helps in 3e. Nothing else from other modules: 3d supplies its own skill |
| **You'll learn** | What instructions and permissions change about an agent; how a coordinator delegates to specialists; how to check a team's work instead of trusting it |
| **Done when** | 3b: `check_viewer.py` scored both viewers. 3d: your agent ran on one normal and one invalid input. 3e: you checked `report.md` against `review.md` and looked at the chart yourself |
| **Time** | Two parts run a team of agents and take longer than the rest. **3e**: about 2 minutes per run. **3k**: about 2–5 minutes per run, plus testing each specialist. Skip them if you are short of time |
| **If stuck** | `/halp 03-agents <what you tried>` |

Your outputs go under `outputs/03-agents/`.

## Why agents

In Exercise 2 the model followed a skill you gave it. An **agent** goes one
step further: it is a model with its own instructions, its own tools and
permissions, and a step limit, working in a loop. It reads, decides what to
do next, asks OpenCode to run a tool, reads the result, and repeats until the
job is done or the step limit is reached.

`Build` and `Plan` are agents too. In this exercise you compare two agents
that differ only in their instructions, write one of your own, and run a
team of five that hand work to each other.

# Before you start

You installed opencode-sidebar-plus in [Exercise 0](../00-plugins/README.md). Keep the
sidebar open in this exercise: in 3e it shows every agent of the team, what
each is doing, and which one waits for your approval.

# Exercise 3a — Run a basic agent and a good agent

Both agents use the model you select: Qwenstorm (`dtu/qwen36`) in the
workshop. Two agents, the same request, the same model, the same permissions
and the same 20-step limit:

| Agent | Instructions |
|---|---|
| [bad-agent](../../.opencode/agents/bad-agent.md) | Three vague sentences: "create an interactive viewer… make it look good". It is not told to make mistakes |
| [good-agent](../../.opencode/agents/good-agent.md) | A short recipe: a fixed library and data source, the exact functions to use, a page that loads first and then a checklist of features, and what to tell you to click |

<details>
<summary><b>What are the steps?</b></summary>

> **One step is one call to the model.** The model answers and, if it needs
> to, asks for one or more tools at once: read a file, run a command, write
> a page. OpenCode runs them and sends the results back. The model's next
> answer is the next step.
>
> **`steps` is the limit per message.** `steps: 20` means at most 20 model
> calls for each message you send. The count starts again with your next
> message, and an agent without `steps` has no limit.
>
> **The last step has no tools.** When an agent reaches its limit, OpenCode
> turns its tools off and tells the model to reply in text only: what it
> did, what is left, and what to do next. That is the "Maximum steps
> reached" message. With `steps: 20` an agent gets 19 rounds of tool use
> and one closing summary. Send "continue" to give it another 20.
>
> **Why it matters.** Vague instructions cost steps: an agent that does not
> know which library or file to use spends its steps reading, searching and
> guessing. Too few steps and it stops halfway. Too many and a confused
> agent can loop for a long time, using tokens and asking you for
> approvals.
>
> **In a team, each agent counts its own steps.** A coordinator that calls
> two specialists in one answer uses one step, and the two specialists run
> at the same time. So be mindful for that, for both usage, spending limits
> and provenance.

</details>

**Do:** start a new chat, select `bad-agent` (shift+tab in the terminal, the
agent selector in Desktop) and send:

> Create an interactive browser visualization of PDB 4HHB that I can use to
> explain the structure to another researcher. I have a browser and OpenCode;
> do not require additional software installation. Briefly explain how to open
> and use the result. Save everything under outputs/03-agents/bad-agent.

Then start another new chat, select `good-agent`, and send the same request
with `outputs/03-agents/good-agent`.

**Look for:** count the approvals each one asks for, and watch which files
each reads. If the bad agent stops at "Maximum steps reached", leave it: the
unfinished page is part of the result.

**Why:** same model, same tools, same limit. Any difference comes from the
instructions alone.

# Exercise 3b — Score both viewers

**Do:**

    python3 exercises/03-agents/check_viewer.py outputs/03-agents/bad-agent --browser
    python3 exercises/03-agents/check_viewer.py outputs/03-agents/good-agent --browser

The `--browser` option uses Chrome to check that the html renders something. No Chrome - drop --browser.

**Look for:** the score out of 7, and the reason next to each check.

**Why:** the score only searches the code for evidence: a pinned library,
chain IDs, HEM, an error message, reset and chain toggles, provenance. An
agent can read the checker and write code that satisfies it, so a page can
score 7/7 and still not draw anything. Did either agent read
`check_viewer.py`? `--browser` checks that something was actually drawn and
saves a screenshot.

# Exercise 3c — Click through both viewers

**Do:** open each `index.html` in your browser and check:

1. **It loads**: the 4HHB tetramer appears, not a blank canvas or a spinner.
2. **Toggles work, including the heme**: hide chain A. Its heme (HEM A142)
   and its label must disappear too.
3. **Labels are right**: 4HHB has chains A and C (α) and B and D (β), with
   hemes at A142, B148, C142 and D148.
4. **Load another ID**: load `1CRN`. Everything must be replaced: one chain,
   no heme, no "4HHB" left on the page. Then try `ZZZZ`: you should see an
   error, not silence.

A page with no control for a check fails that check.

**Why:** the good agent is good because its instructions name the library,
the data source, the functions and what "done" means, not because of its
name. Remove one of those lines and see what breaks. The vague agent often
makes the nicer-looking page, with methods that do not exist, a heme that
stays when its chain is hidden, or old text after loading a new structure.
Judge the files and the behaviour, not the agent's summary.

# Exercise 3d — From a good agent to your agent

Write your own agent with a specific job and a definition of success. The
suggested job: an agent that **checks a dataset before anyone analyses it**,
using a profiling skill. Other jobs are fine too, such as reviewing an
analysis or visualizing a structure, as long as you can check the result.

## Install the skill it will use

**Do:** this exercise supplies the skill, so you do not need Exercise 2. From
the workshop folder (if you built your own `csv-profile` in 2c, keep yours
and skip this):

```bash
cp -r exercises/03-agents/starter/csv-profile .opencode/skills/
```

**Look for:** `/skills` in OpenCode lists `csv-profile` (run `opencode reload`
if not).

## Create the agent

**Do:** ask Build to create `.opencode/agents/data-checker.md` (or
`my-agent.md`, any name), or write the file yourself. The filename becomes
the agent name. Keep your own agent separate from `bad-agent` and
`good-agent`. Start from a small definition like this:

```markdown
---
description: Checks a supplied analysis and reports evidence-backed findings
mode: primary
steps: 20
permissions:
  - { action: edit, resource: '*', effect: ask }
  - { action: shell, resource: '*', effect: ask }
  - { action: subagent, resource: '*', effect: deny }
---

Inspect the supplied files and identify the question the analysis addresses.
Check assumptions against the data and available evidence.
Preserve original inputs and ask before changing analysis files.
Save the requested outputs in a separate folder.
Report the checks performed, findings, and unresolved limitations.
```

Change the description and instructions to your job, for example: use the
`csv-profile` skill, never change the input, report problems and save the
report under `outputs/03-agents/`. Then run `opencode reload`.

**Look for:** the new agent in the agent list (shift+tab). Then select it
and use it on `exercises/04-mcp/data/byo/uniprot_human_proteins.csv.gz`, and
test it on a file that does not exist: does it explain the problem, or
invent a profile?

**Why:** the YAML between the `---` markers holds settings; the Markdown below
it holds the instructions. An agent is not a newly trained model: the same
model can run several agents with different instructions and permissions.
The settings below are a reference; you do not need all of them.

## Agent settings reference
This reference is for **OpenCode v2**.<br>
Start with the first few fields; the remaining options
are available when you need them. Provider-specific options are open-ended,
so there is no universal list that every model accepts.
| Setting | What it changes | Example or caution |
|---|---|---|
| `description` | Explains the agent's job and when to choose it | A concrete task description, not just "helpful expert" |
| `mode` | Where the agent runs | `primary` for the main conversation, `subagent` for a helper, `all` for both |
| Markdown body / `system` | Instructions, decisions, expected outputs, and checks | Use the Markdown body in an agent file; `system` in a JSON agent definition |
<details>
<summary>Full reference list</summary>

| Setting | What it changes | Example or caution |
|---|---|---|
| `model` | Pins the agent to a provider/model | `dtu/qwen36`; leave unset to use the selected/default model or the calling agent's model |
| Model variant | Selects a configured variant | Use `provider/model#variant`; the variant must exist |
| `steps` | Limits agentic iterations before a text-only response | Positive integer, such as `20`. It is not a token limit or an exact count of shell commands |
| `permissions` | Ordered rules controlling which tool actions run, ask, or stop | The last matching rule wins |
| `disabled` | Disables this agent | `true` or `false` |
| `hidden` | Hides the agent: a primary agent leaves the shift+tab cycle, a subagent the `@` menu | A hidden primary agent can then only be started by a command, which hands it just its first answer before Build takes over. Not access control |
| `color` | Changes the agent's UI colour | A quoted hex colour such as `"#246B60"` |
| `request` | Model-request overlay | The v2 agent docs currently say agent overlays are stored but not applied by the runner. Do not rely on this for sampling controls |

Do not copy v1 fields such as `permission`, `bash`, `task`, `prompt`,
`temperature`, `top_p`, `options`, `tools` or `maxSteps` into a v2 agent.
Sampling controls belong in supported provider/model request settings;
verify the adapter accepts them. Temperature zero does not guarantee repeatability.

Schema: [OpenCode configuration](https://opencode.ai/config.json).
Usage: [agent configuration](https://opencode.ai/v2/docs/agents/).
</details>

### Permissions and modular tools
Permission values are `allow` (run), `ask` (request approval), and `deny`
(block). Most omitted permissions are permissive, so omission is not a
safety restriction. Project/global permissions and agent overrides combine.
Available tools also depend on your installation and connected services.

<details>
<summary>Permission types</summary>

| Permission key | Capability |
|---|---|
| `read` | Read file contents |
| `edit` | Modify files through the editing tools, including writes and patches |
| `glob`, `grep`, `list` | Find files, search content, and list directories when those tools are available |
| `shell` | Execute shell commands on your computer |
| `skill` | Load reusable skill instructions by skill name |
| `subagent` | Delegate to subagents by agent ID |
| `webfetch`, `websearch` | Retrieve web content or search, when available |
| `lsp` | Query language-server information, when configured |
| `question` | Ask questions through the question tool, when available |
| `todowrite` | Maintain task lists when the tool is available |
| `external_directory` | Gate access to paths outside the project |
| `doom_loop` | Gate recovery from repeated identical tool calls |
| `*` | A general rule before more specific rules |
| A custom/MCP tool name or pattern | Control a tool exposed by an installed integration |

Pattern rules can restrict individual commands, files, skills, or subagents.
Use the catch-all first: the last matching rule wins. Not every permission
supports the same input-pattern semantics in every OpenCode version.
</details>

Example permission block, to replace the block in your own agent:

```yaml
permissions:
  - { action: edit, resource: '*', effect: ask }
  - { action: shell, resource: '*', effect: ask }
  - { action: shell, resource: 'git status*', effect: allow }
  - { action: shell, resource: 'git push*', effect: deny }
  - { action: skill, resource: '*', effect: deny }
  - { action: skill, resource: pdb-download, effect: allow }
  - { action: subagent, resource: '*', effect: deny }
  - { action: external_directory, resource: '*', effect: ask }
```

Replace `pdb-download` with the actual name of your installed skill. An allow
rule does not create a missing skill or force the agent to use it. Explain
when to load it in the Markdown body. A skill is guidance; scripts and other
tools perform the executable work.

To experiment with delegation, create a separate agent with `mode: subagent`
and replace the main agent's subagent deny rule with these ordered rules:

```yaml
permissions:
  - { action: subagent, resource: '*', effect: deny }
  - { action: subagent, resource: structure-reviewer, effect: ask }
```

The helper needs its own definition and permissions. Delegation adds model
calls and can add latency. Begin with one agent before introducing helpers.

MCP tools require a server registered under `mcp.servers` in `opencode.json`.
A permission rule or the `mcp/` folder alone does not connect a server.

Permissions are tool controls, not an operating-system sandbox. For example,
denying `edit` does not make an agent read-only if `shell` can modify files.
Keep approval prompts enabled and review the requested action. Do not use
auto-approve mode when testing whether an `ask` rule behaves as intended.

References: [permissions](https://opencode.ai/v2/docs/permissions/),
[skills](https://opencode.ai/v2/docs/skills/), and
[MCP configuration](https://opencode.ai/v2/docs/mcp-servers/).

### Settings that belong elsewhere

| Setting | Where it belongs |
|---|---|
| Context/output limits | `providers.dtu.models.<model-id>.limit.context` and `.limit.output` in `opencode.json` |
| Server context capacity | The administrator's model launch settings; a student JSON edit does not enlarge GPU capacity |
| Model URL and authentication | Provider configuration, not the agent instructions |
| Default chat and background models | Root `model`, plus `agents.title.model` and `agents.summary.model` in `opencode.json` |
| Shared project rules | An `AGENTS.md` file or configured instruction files; these can affect several agents |
| MCP server connection | `mcp.servers`, with any required server software and credentials |

Start with the supplied DTU limits. Follow the [context instructions](../../README.md#changing-your-context-setting-dtu-models)
before increasing them, and require organiser approval above 32768. A larger
value must fit the model's currently verified server limit. Do not add a made-up
`context` field to agent frontmatter or assume a raw API `max_tokens` field works there.

## Test your agent

1. Check that OpenCode discovers it. Outside the chat, run
   `opencode debug agents`, or reopen the project and inspect the agent selector.
2. Try one normal task. Inspect the files and check the claimed results.
3. Try incomplete or invalid input. Does it explain the problem or invent an answer?
4. Try another input without rewriting the agent. Does it still work?
5. Change one instruction or setting, start a fresh chat, and compare again.

Record the agent version, model ID, settings, inputs, tool access, output
folder, and checks. Repeat trials when comparing quality. Low temperature
alone cannot control model/backend changes, tool results, or conversation
history. A successfully parsed configuration is only a loading test.

For PDB viewers, inspect the browser output yourself unless the agent has
actually used a browser inspection tool. Keep "code generated", "viewer
opened", "controls checked", and "scientific content verified" distinct.

---

# Exercise 3e — A team of specialists

*Takes about 2 minutes per run.*

One agent can do a task. A **team** (sometimes called a swarm) splits it into
bounded jobs with explicit hand-offs: a coordinator and specialist
subagents, each with its own model, instructions and permissions. The five
agents are already in [`.opencode/agents/`](../../.opencode/agents/). They
have one small task:

> Which organism group has the largest median genome size, and does the
> answer change if you keep only complete assemblies?

| Agent | Job | Writes | Model |
|---|---|---|---|
| [genome-coordinator](../../.opencode/agents/genome-coordinator.md) | Delegates, then writes the report | `report.md` | yours |
| [genome-auditor](../../.opencode/agents/genome-auditor.md) | Checks rows, groups, missing values and units | `audit.md` | yours |
| [genome-analyst](../../.opencode/agents/genome-analyst.md) | Computes the medians | `medians.csv` | yours |
| [genome-visualizer](../../.opencode/agents/genome-visualizer.md) | Draws one chart | `medians.svg` | yours |
| [genome-reviewer](../../.opencode/agents/genome-reviewer.md) | Recomputes the numbers from the raw data | `review.md` | yours |

All five use the model you selected, Qwenstorm in the workshop. Each agent
could have its own: add a line such as `model: opencode/big-pickle` to its
file. With a free external model, prompts, data and results leave DTU, which
is why the task uses public NCBI data.

## Run it

**Do:** check that the models are still offered:

```bash
scripts/check-setup.sh --module 03-agents
```

Start `opencode` in the workshop folder, start a new chat, press
**shift+tab** until the agent is `genome-coordinator`, check the model is
**Qwenstorm** (`dtu/qwen36`), or a free model if you are on your own
(`/models`), and send:

> Run the genome team task.

Approve what it asks; do not use `--auto`.

**Look for:** in the sidebar you added at the start of this exercise, the
**Agents** section lists each specialist as it starts, with its status
(● running, ◆ needs approval, ✓ done, ✗ failed), model, time and the tool it
is using. A ◆ means that specialist is waiting for *you*: a banner at the top
of the section says so, and the prompt appears under the coordinator's
conversation. Click a row to open that specialist's conversation.
Afterwards, **≡ Details** at the foot of the sidebar shows when each
specialist worked, and its tokens and tool calls.

**Why:** the coordinator starts the auditor and the analyst at the same time,
then the visualizer and the reviewer. Each specialist writes one Python
script and runs it; their permissions allow exactly those scripts without
asking, and every other command still asks you. The reviewer runs on a
different model from the analyst and recomputes everything from the raw
data, so it does not have to trust the analyst's summary.

## What to inspect

**Do:** open the run folder under `outputs/genome-team/`. Read `report.md`,
then check it against the specialists' own files:

- Does `review.md` say PASS, and did the reviewer recompute every group?
- Which conclusion rests on very few complete assemblies? Is that in the
  report?
- Open `medians.svg` in your browser. Nobody reviewed it but you: is the axis
  logarithmic and labelled, is `n` shown, could someone misread it?

**Why:** a report is a summary written by a model. The specialists' files
are the evidence. If a specialist failed, a good coordinator says so instead
of doing the job itself or guessing.

If one of the models has gone, set that agent's `model:` to another free
model and note it.

## What to notice

- An agent is instructions, tools, permissions and a step limit around a
  model. Change the instructions and you change the result, with the same
  model.
- Permissions decide what an agent may do without asking. Read every prompt.
- A team only helps when the jobs are bounded and someone checks the others.
  More agents are not a guarantee of a better answer.
- Plugins change OpenCode itself: look first, pin a version.

**Discuss with your neighbour:**

1. What made the good agent good: which lines in its instructions mattered
   most?
2. Your agent from 3d: what would it need before you trusted it with your own
   data?
3. Which jobs in your own work would you split between specialists, and who
   would review whom?

---

# === Dive Deeper ===

# Exercise 3f — Finding bugs: run it, then ask

There is a working script in [`buggy/`](buggy/). It reads a small BED file,
runs, exits cleanly and prints three numbers. All three are wrong, and one of
them is wrong in two different ways. Nothing errors: this is the kind of bug
that reaches a paper.

**Do:** work on a copy, so the original stays as it is, and run it:

```bash
mkdir -p outputs/03-agents
cp -r exercises/03-agents/buggy outputs/03-agents/buggy
cd outputs/03-agents/buggy && python3 summarise.py && cd -
```

Then start a new chat in **Plan** and ask:

> Review outputs/03-agents/buggy/summarise.py and its input regions.bed. Do
> not edit anything.

**Look for:** which problems it names, and whether it explains each with
evidence from the data. Keep its answer: the next steps are compared with it.

**Why:** start with what you already have. OpenCode also has built-in
commands for this kind of work:

| Command | Use |
|---|---|
| `/review` | Review changes: uncommitted, a commit, a branch or a PR. It reviews a *diff*, so it has nothing to say about a script nobody changed; use it after a fix |
| `/fork` | Branch the conversation from an earlier message, to try a fix without losing the original thread. It does not copy files |
| `/undo` | Take back the last message |
| `/diff` | See what changed |
| `/compact` | Summarise the conversation to free context |
| `/export` | Save the conversation |

# Exercise 3g — Finding bugs with a skill

**Do:** write a debugging skill, as in Exercise 2, or adapt a published one
such as [this debugging skill](https://github.com/AllThingsSmitty/proven-skills/tree/main/skills/debug).
Give it these steps, then use it on the copy of the script:

1. Reproduce and record the actual output before reading any code.
2. State a hypothesis, the evidence for it, and what was ruled out.
3. Name the smallest change that would fix it.
4. Say what was not checked.

**Look for:** does the skill change what is found, or only how the answer is
laid out?

**Why:** a skill is Markdown, so it cannot run anything by being present.
That makes it the safest thing to add. The published skill opens with a rule
worth keeping: debugging is hypothesis-driven investigation, not random
exploration.

# Exercise 3h — Finding bugs with a reviewer agent

**Do:** create `.opencode/agents/bug-reviewer.md`:

```markdown
---
description: Reviews code and reports defects with evidence. Cannot edit or run anything.
mode: primary
steps: 15
permissions:
  - { action: '*', resource: '*', effect: deny }
  - { action: read, resource: '*', effect: allow }
  - { action: glob, resource: '*', effect: allow }
  - { action: grep, resource: '*', effect: allow }
  - { action: external_directory, resource: '*', effect: deny }
---

Review the code you are pointed at. For each defect: the line, what is wrong,
the evidence, and the smallest fix. Say what you could not check.
```

Restart OpenCode, select `bug-reviewer` (shift+tab) and ask it to review the
copy of the script. Ask it to run the script, too.

**Look for:** which tools it used, and what it says when asked to run the
script. Compare its findings with 3f and 3g: which bugs did each find, and
which of its points are real problems rather than bugs in the printed numbers?

**Why:** a skill advises; an agent decides what is allowed. This reviewer
denies everything first, then allows only reading. Denying only edits would
not be enough, because a shell command can rewrite files too. Review first,
and let a separate, approved Build task run tests or make the fix.

# Exercise 3i — The ordinary tools, and a file of expected answers

**Do:** run a linter and a type checker on the script:

```bash
uvx ruff check --select ALL outputs/03-agents/buggy/summarise.py
uvx --with mypy mypy outputs/03-agents/buggy/summarise.py
```

Then ask Build to write a small file of expected answers for `regions.bed`,
worked out by hand from the four rows, and a test that compares the script's
output with it.

**Look for:** how many of the linter's complaints are about the wrong
numbers. Does the test fail on the current script?

**Why:** an agent driving a deterministic tool beats an agent reasoning about
code. None of these bugs breaks a rule a linter knows; a file of known
answers catches all of them, because a wrong number is only wrong compared
with the right one. Asking for that file first changes how the whole session
goes.

| Tool | Finds |
|---|---|
| A file of expected answers | Silently wrong numbers |
| `pytest -x --lf` | Stops at the first failure, then reruns only the failures |
| `ruff`, `mypy` | Problems that never reach a running program |
| `git bisect` | Which commit broke it, mechanically |
| `diff <(old) <(new)` | Proof that an output actually changed |

# Exercise 3j — Build your own checker

**Do:** write a checker for something you care about in your own data: a
file format, a coordinate convention, a column that must never be negative,
a join that must not change the row count. Make it fail loudly on bad input
and stay silent on good input. Then break the data on purpose and confirm it
fails.

**Look for:** does it stay silent on the good data, and fail with a message
that says what is wrong and where on the broken copy?

**Why:** a check you have never seen fail is not a check.

<details>
<summary><b>What the script is actually doing wrong</b> (open after you have tried)</summary>

1. **`end - start + 1`.** BED intervals are half-open, so a region is
   `end - start` bases. One base too many per region, so the error grows with
   the number of rows and is invisible on any single row.
2. **BED starts are 0-based.** The first region starts at base 1001 in 1-based
   coordinates, not 1000. BED is 0-based; GFF, GTF and VCF are 1-based.
3. **Sorting chromosome names as text.** `chr10` sorts before `chr2`.
4. **Overlapping regions are counted twice.** `regionA` (chr1:1000-1100) and
   `regionD` (chr1:1050-1200) overlap by 50 bases.

So "total bases covered" has three answers:

| Answer | Meaning |
|---|---|
| 404 | What the script prints. Wrong |
| 400 | The sum of the region lengths, after fixing the off-by-one |
| 350 | The bases actually covered, after merging the overlap |

Fixing the arithmetic gives 400. Getting to 350 needs a decision about what
"covered" means: a question to ask, not only a line to fix.

</details>

## What to notice

- Start cheap: what OpenCode already has, then a skill, then an agent.
- An agent's permissions decide what it can do; deny first, then allow.
- A linter checks rules, not answers. A file of expected answers catches a
  number that is wrong.
- A specialised tool built from fixed steps plus an agent is another option;
  see [open-code-review in the additional resources](../../additional.md#reviewing-code-with-fixed-steps-and-an-agent-open-code-review).

# Exercise 3k — Build your own team

*Takes about 2–5 minutes per team run, plus testing each specialist.*

**Do:** build a team of your own instead of repeating the genome team. Pick a
target:

| Target | A question to start from |
|---|---|
| [Penguins](../04-mcp/data/byo/PROVENANCE.md) | Why do the pooled and the within-species correlations of bill length and depth disagree? |
| [Human proteins](../04-mcp/data/byo/PROVENANCE.md) | How does the number of human proteins change with the evidence you accept? |
| Your own data | One answerable question, the input, the result, and a check that could prove the answer wrong. Public or made-up data only: the models are external |

Copy the five `genome-*.md` files in `.opencode/agents/` to new names with
your own prefix, for example `penguin-coordinator.md` and
`penguin-auditor.md`. In each, change the description, the job, the input
path and the run folder (`outputs/penguin-team/`). In the coordinator, change
the question, the team name in its `new_run.py` command and permission
(`python3 exercises/03-agents/new_run.py penguin-team`), and the names in its
`subagent` rules, which must list exactly your specialists:

```yaml
permissions:
  - { action: subagent, resource: '*', effect: deny }
  - { action: subagent, resource: penguin-auditor, effect: allow }
  - { action: subagent, resource: penguin-analyst, effect: allow }
  - { action: subagent, resource: penguin-visualizer, effect: allow }
  - { action: subagent, resource: penguin-reviewer, effect: allow }
```

Keep `mode: subagent` for the specialists and `mode: primary` for the
coordinator. Restart OpenCode, then test each specialist on its own first,
for example `@penguin-auditor`, with an explicit run folder. Only then select
your coordinator and run the team.

**Look for:** did each specialist write its own file in the run folder? Can
the reviewer reproduce the result without trusting the analyst's summary? If
a specialist fails, does the coordinator say so, or fill the gap with a
guess? Run it a second time: does it land in a new folder?

**Why:** renaming a file does not rename it inside the coordinator's rules
or instructions: a rule still naming `genome-auditor` does not let the
coordinator call `penguin-auditor`. Each specialist needs a narrow job, its own output and a check of
its own; another copy of the analyst adds cost, not evidence. A
reviewer on a different model from the analyst is a stronger check: it does
not share the analyst's blind spots.

Previous: [Exercise 2 — Skills](../02-skills/README.md) · Next: [Exercise 4 — MCP](../04-mcp/README.md).
