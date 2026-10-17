# Exercise 3 — Agents

| | |
|---|---|
| **Model** | 3a: `opencode/big-pickle`, selected by you for both agents. 3b: your choice. 3c: the coordinator on Big Pickle; each specialist's own model is set in its file |
| **Needs** | `scripts/check-setup.sh` passed. opencode-sidebar-plus from Exercise 0 helps in 3c. Nothing else from other modules: 3b supplies its own skill |
| **You'll learn** | What instructions and permissions change about an agent; how a coordinator delegates to specialists; how to check a team's work instead of trusting it |
| **Done when** | 3a: `check_viewer.py` scored both viewers. 3b: your agent ran on one normal and one invalid input. 3c: you checked `report.md` against `review.md` and looked at the chart yourself |
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
sidebar open in this exercise: in 3c it shows every agent of the team, what
each is doing, and which one waits for your approval.

# Exercise 3a — From a basic agent to a good agent

Use **`opencode/big-pickle`** for both agents and select it yourself before
each run. Two agents, the same request, the same model, the same permissions
and the same 20-step limit:

| Agent | Instructions |
|---|---|
| [bad-agent](../../.opencode/agents/bad-agent.md) | Three vague sentences: "create an interactive viewer… make it look good". It is not told to make mistakes |
| [good-agent](../../.opencode/agents/good-agent.md) | A short recipe: a fixed library and data source, the exact functions to use, a page that loads first and then a checklist of features, and what to tell you to click |

## 1. Run both

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

## 2. Score both

**Do:**

    python3 exercises/03-agents/check_viewer.py outputs/03-agents/bad-agent --browser
    python3 exercises/03-agents/check_viewer.py outputs/03-agents/good-agent --browser

Without Chrome, leave out `--browser` and just drag the html file to your browser.

**Look for:** the score out of 7, and the reason next to each check.

**Why:** the score only searches the code for evidence: a pinned library,
chain IDs, HEM, an error message, reset and chain toggles, provenance. An
agent can read the checker and write code that satisfies it, so a page can
score 7/7 and still not draw anything. Did either agent read
`check_viewer.py`? `--browser` checks that something was actually drawn and
saves a screenshot.

## 3. Click through it

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

# Exercise 3b — From a good agent to your agent

Write your own agent with a specific job and a definition of success. The
suggested job: an agent that **checks a dataset before anyone analyses it**,
using a profiling skill. Other jobs are fine too, such as reviewing an
analysis or visualizing a structure, as long as you can check the result.

## Install the skill it will use

**Do:** this exercise supplies the skill, so you do not need Exercise 2. From
the workshop folder (if you built your own `csv-profile` in 2f, keep yours
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

# Exercise 3c — A team of specialists

One agent can do a task. A **team** (sometimes called a swarm) splits it into
bounded jobs with explicit hand-offs: a coordinator and specialist
subagents, each with its own model, instructions and permissions. The five
agents are already in [`.opencode/agents/`](../../.opencode/agents/). They
have one small task:

> Which organism group has the largest median genome size, and does the
> answer change if you keep only complete assemblies?

| Agent | Job | Writes | Model |
|---|---|---|---|
| [genome-coordinator](../../.opencode/agents/genome-coordinator.md) | Delegates, then writes the report | `report.md` | `opencode/big-pickle` |
| [genome-auditor](../../.opencode/agents/genome-auditor.md) | Checks rows, groups, missing values and units | `audit.md` | `opencode/big-pickle` |
| [genome-analyst](../../.opencode/agents/genome-analyst.md) | Computes the medians | `medians.csv` | `opencode/mimo-v2.6-flash-free` |
| [genome-visualizer](../../.opencode/agents/genome-visualizer.md) | Draws one chart | `medians.svg` | `opencode/space-bunny-free` |
| [genome-reviewer](../../.opencode/agents/genome-reviewer.md) | Recomputes the numbers from the raw data | `review.md` | `opencode/space-bunny-free` |

All five are free external models: prompts, data and results leave DTU, and
Big Pickle and MiMo may use them to improve their models. That is why the
task uses public NCBI data.

## Run it

**Do:** check that the models are still offered:

```bash
scripts/check-setup.sh --module 03-agents
```

Start `opencode` in the workshop folder, start a new chat, press
**shift+tab** until the agent is `genome-coordinator`, check the model is
**Big Pickle** (`/models` if not), and send:

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
2. Your agent from 3b: what would it need before you trusted it with your own
   data?
3. Which jobs in your own work would you split between specialists, and who
   would review whom?

---

Previous: [Exercise 2 — Skills](../02-skills/README.md) · Next: [Exercise 4 — MCP](../04-mcp/README.md).
