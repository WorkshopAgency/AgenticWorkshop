# Exercise 2a — From a basic agent to a good agent

An agent can complete a task without completing it particularly well.
These initial examples compare a vague instruction with an explicit,
verifiable workflow. PDB visualization is the first case, not the scope
of every exercise in this repository.

## The two agents

| Agent | What changes |
|---|---|
| [bad-agent](../../agents/bad-agent.md) | A plausible but underspecified request to build a viewer. It is not instructed to make mistakes. |
| [good-agent](../../agents/good-agent.md) | Inspects the input, chooses useful views, reuses available skills, records provenance, and checks the result. |

Both are primary agents with the same permissions and 20-step limit. Neither
hardcodes a model or temperature. They are first-iteration teaching examples,
not a tested guarantee of better results or the completed reference visualizer.

In the 23 September rehearsal, both needed more than their first turn: the
basic viewer used nonexistent rendering-library methods, while the explicit
agent spent its initial budget on parsing and had not produced a viewer.
Better instructions are a hypothesis to test, not a result to assume. Check
the deliverable before adding features or increasing the step budget.

A later Big Pickle comparison produced actual viewers. The detailed version
needed follow-ups to finish and to fix chain visibility and stale metadata
when loading another structure. Those cases are now explicit in its
instructions. The lesson is to test and improve the agent, not to trust the
word “good” in its filename.

## Try the same request

Open the repository in OpenCode and start a fresh chat. In the terminal,
use Tab to select `bad-agent`; in Desktop, use the agent selector. Reopen
OpenCode if the newly added agents do not appear.

Use this request:

> Create an interactive browser visualization of PDB 4HHB that I can use to
> explain the structure to another researcher. Save everything under
> outputs/bad-agent. I have a browser and OpenCode; do not require additional
> software installation. Briefly explain how to open and use the result.

Start another fresh chat, select `good-agent`, and repeat the same request,
changing only the output folder to `outputs/good-agent`.

Keep the model, input, available skills/tools, and approval decisions the same.
Do not give the second agent the first agent's output. For a stricter comparison,
use separate extracted copies of the repository so neither can inspect the
other's files. The good example is included here for inspection; it is not hidden
from students or their agents.

## Inspect, improve, and reuse

- Does the structure actually load, and do the controls work?
- Are chains, selected residues, and any ligands identified correctly?
- Is the view useful for explaining the structure, with readable labels?
- Are its scientific claims supported, and are limitations visible?
- Can someone reproduce the view and load a different structure?
- What manual corrections and extra prompts were necessary?

Edit or create an agent of your own and repeat the comparison on another
structure. Judge the generated files and behaviour, not the agent's claim
that it succeeded. One run does not establish a fixed performance difference.

# Exercise 2b — From a good agent to your agent

Create your own agent rather than changing the supplied examples. It can
visualize a structure, review an analysis, check a dataset, or perform another
task you can evaluate. Give it a specific job and a definition of success.

## Create the agent

Ask OpenCode to help create `.opencode/agents/my-agent.md`, or
write the Markdown file yourself. The filename becomes the
agent name. Keep your own agent separate from `bad-agent` and `good-agent`.

Start with a small definition like this:

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

The YAML between `---` markers holds settings. The Markdown below it holds
the instructions. An agent is not a newly trained model: the same model can
run several agents with different instructions and permissions.

## Agent settings reference
This reference is for **OpenCode v2**, checked with 2.0.14 on 23 September 2026.<br>
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
| `model` | Pins the agent to a provider/model | `dtu/gptoss`; leave unset to use the selected/default model or the calling agent's model |
| Model variant | Selects a configured variant | Use `provider/model#variant`; the variant must exist |
| `steps` | Limits agentic iterations before a text-only response | Positive integer, such as `20`. It is not a token limit or an exact count of shell commands |
| `permissions` | Ordered rules controlling which tool actions run, ask, or stop | The last matching rule wins |
| `disabled` | Disables this agent | `true` or `false` |
| `hidden` | Hides a subagent from the `@` suggestion menu | For subagents only. This is not access control or a way to hide a solution file |
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

Start with the supplied DTU limits. Follow the [context instructions](../../README-fullday.md#changing-your-context-setting)
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

# Exercise 2c — A team of specialists

One agent can do a task. A coordinated team splits a larger question into
bounded jobs with explicit handoffs. This is our introduction to the **agent
swarm idea**: a coordinator and specialist subagents, not agents magically
sharing memory or doing everything in parallel.

## First: the genome-size demonstration

The five agents are already in [`.opencode/agents/`](../../../.opencode/agents/),
the folder OpenCode reads. Their common goal is:

> How do genome size and gene density differ across organism groups, and how
> does restricting the analysis to complete assemblies change the conclusions?

| Agent file | Job | Model |
|---|---|---|
| [genome-coordinator.md](../../agents/genome-coordinator.md) | Delegate the work and assemble the report | `opencode/big-pickle` |
| [genome-auditor.md](../../agents/genome-auditor.md) | Check data, units and missing values | `opencode/mimo-v2.6-flash-free` |
| [genome-analyst.md](../../agents/genome-analyst.md) | Write and run the analysis | `opencode/ling-3.0-flash-fin-free` |
| [genome-visualizer.md](../../agents/genome-visualizer.md) | Create browser-readable plots | `opencode/muse-spark-1.3-contributor-free` |
| [genome-reviewer.md](../../agents/genome-reviewer.md) | Independently check results and plots | `opencode/nemotron-3.5-lightning-free` |

All five roles use external free models from OpenCode, so this example does
not require the DTU servers. Prompts, data and specialist results go to
third-party providers. **Use only the supplied public data**, especially
with the Muse contributor model; read the free-model warning in the
[main README](../../README-fullday.md).

Inspect outputs and ask for corrections when needed. Record the models and
any interventions in your write-up; a successful response alone does not
establish that an analysis is correct.

From a terminal **inside the downloaded workshop root** (beside
`opencode.json`), run:

```bash
opencode mini --agent genome-coordinator --model opencode/big-pickle --prompt "Run the genome-size team task with all four specialist subagents. Save the actual outputs in a new folder under outputs/genome-team/. Report failed or untested steps."
```

This opens the interactive terminal so you can approve edits and commands.
Do not add `--auto`. You start **one coordinator**, which delegates to the
other four agents. They work toward one goal in dependency order:
audit → analysis → visualization → review → final report. They do not need
five terminals or simultaneous execution. If progress pauses, check the
specialist's child session for an approval request. In our 2.0.14 rehearsal,
`opencode run --auto` approved the parent but did not remove child approvals;
it is not a substitute for the interactive workflow.

**Desktop:** open the workshop as a project, select `genome-coordinator` in
the agent selector, explicitly choose **Big Pickle**, and paste the same
quoted prompt into a new chat. Selecting a primary agent does not necessarily
replace a chat's already selected model.

Python 3.10+ and access to all five models are required. Leave MCP off; no
extra Python packages are required. Check the five are listed by
`opencode models` before you start.

Free offers change without notice. If one of the five has gone, set that
agent's `model:` to another model you can reach and say in your write-up which
one you used. The coordinator is the one agent whose absence stops the whole
run.
If the agent is missing, check that you opened the folder containing
`.opencode/agents/` and reopen OpenCode. Do not silently switch models.

When the run finishes, inspect `report.md`, `plots.html`, `review.md` and
`agent-run.md` inside the new output folder. These must be the team's actual
outputs, including failures and corrections—not supplied example answers.

## Then: choose your team's target

Do not simply repeat the genome demonstration. Choose one of these, or your
own question with a dataset you are allowed to use:

| Target | A concrete starting question |
|---|---|
| [Penguins](../../../exercises/03-mcp/data/byo/PROVENANCE.md#penguinscsv) | Why do pooled and within-species bill-measurement correlations disagree? Show the missing-data handling, correlations, plot and interpretation. |
| [Human proteins](../../../exercises/03-mcp/data/byo/PROVENANCE.md#uniprot_human_proteinscsvgz) | How does the number of human proteins change with the evidence criterion? Show counts, exclusions, a plot and a defensible conclusion. |
| Your own dataset | Define one answerable question, the input, an observable result and a check that could prove the answer wrong. Use public or synthetic data with external models. |

Create **four or more specialists plus a coordinator**. You can adapt the
reference definitions or write your own. Assign every role to a different model:
a local model, a free model from OpenCode, or a personally connected provider. Check
access and any cost before choosing; different display names for the same
provider/model are not different models.

Agree each specialist's input, narrow responsibility, output and success check.
An auditor, analyst, visualizer and independent reviewer are a starting point,
not compulsory names. An extra specialist needs a separate job—for example,
sensitivity analysis—not just another copy of the analyst.

Copy the five example Markdown files into your team's working folder and
rename them with your team prefix. Edit each agent's `model:` field,
description, task instructions, permissions and expected outputs. Change the
coordinator's question, dataset path and helper names, and each specialist's
methods to suit penguins, proteins or your own target. The agents write their
own analysis tools during the run; there is no pre-computed pipeline to call.
Keep original data intact.

Test specialists individually with `@team-01-auditor` (substitute your team's
number and actual name). Give them explicit input/output paths. Only then run
the coordinator. Use `mode: subagent` and a deny-all `subagent` rule for specialists; use
`mode: primary` for the coordinator with an explicit list of allowed helpers:

```yaml
permissions:
  - { action: subagent, resource: '*', effect: deny }
  - { action: subagent, resource: team-01-auditor, effect: allow }
  - { action: subagent, resource: team-01-analyst, effect: allow }
  - { action: subagent, resource: team-01-visualizer, effect: allow }
  - { action: subagent, resource: team-01-reviewer, effect: allow }
```

This block only illustrates delegation; preserve the rest of your permission
settings. Change **every helper name** when copying it to another team.
Do not assume renaming a file updates its coordinator's instructions or rules.
Give each worker separate output files. Review permission requests and keep
publishing separate from the analytical run.

## Team folders and hand-off

Your team has two folders, using `team-01` through `team-10`:

```text
exercises/02-agents/team-01/                 Working definitions and team goal
_sectionday/exercises/04-share/submissions/team-01/      Reviewed copies to share
```

Use filenames such as `team-01-coordinator.md` and `team-01-auditor.md` to
avoid collisions with the demonstration and other teams. Keep the working
folder as the source; the sharing folder is a reviewed snapshot. Do not put
data, credentials, caches or generated results in either folder.

1. Choose a human team coordinator to maintain a **team fork** and agreed
   branch. Members contribute only their team's working files, through PRs
   from their forks or branches where they have access. No workshop main-branch
   write access is assumed or granted.
2. Agree a branch/commit to use. The coordinator downloads that exact revision
   from the team fork. Unmerged work is not in the workshop main ZIP; use the
   contributor's branch/commit link if it has not been merged.
3. Read the downloaded definitions and required scripts/skills. Copy the
   agreed agent Markdown files into the project-root `.opencode/agents/`.
   Copy complete supporting skill folders into `.opencode/skills/` and keep
   referenced project files at the paths the instructions expect. Review any
   existing installed file before replacing it.
4. Confirm the model IDs are available to the coordinator, reopen OpenCode,
   and inspect `opencode debug agents`. Select the team coordinator agent and
   run in a fresh output folder. Team members' provider credentials are not
   included in the download; use your own connections.
5. Copy reviewed definitions into your team's sharing folder. Follow the
   existing Exercise 4 procedure with `team-01` (or your team number) as the
   submission name. The existing submit-agent only publishes under submissions;
   it is not the tool for collaborating on the working folder in step 1.

OpenCode **does not auto-load** the agents from either team folder. Folder
names do not provide access control. Work only on your team's files and
check what is included in every PR.

A downloaded ZIP has **no Git history** and cannot simply `git push`. Clone
your fork for Git collaboration, or use GitHub's file upload/PR interface.
The final coordinator can still download a ZIP to run the team locally.
Keep generated runs under `outputs/`, which is ignored by this repository.

### Contribute with ordinary Git

Fork the repository using GitHub's **Fork** button. Replace `YOUR-USER` below
with the owner of your fork, and replace `team-01` with your team number:

```bash
git clone https://github.com/YOUR-USER/AgenticWorkshop.git
cd AgenticWorkshop
git switch -c team-01-agents
```

Put your working files into `exercises/02-agents/team-01/`, then:

```bash
git add exercises/02-agents/team-01/
git diff --cached
git commit -m "Add Team 1 agents"
git push -u origin team-01-agents
```

In GitHub, open a pull request **to the agreed team fork and branch**. Review
and merge the agreed files there. Do not assume you can push to the workshop
repository. GitHub CLI (`gh`) is optional, not required. The submission agent
remains limited to Exercise 4 submissions; use ordinary Git for this working folder.

### Run your own team

The human coordinator downloads the agreed revision and copies the reviewed
agent files into `.opencode/agents/` as described above. From that project root:

```bash
opencode mini --agent team-01-coordinator --model opencode/big-pickle --prompt "Run our agreed team task with your specialist subagents. Save this run in a new outputs/team-01/ folder. Report results, corrections and anything untested."
```

Use your actual coordinator filename without `.md` and its chosen model ID.
In Desktop, select that coordinator **and model**, then paste the prompt.
Only the coordinator needs all the provider
connections for the assembled team; credentials are never shared in the files.

## What to inspect at the end

Did each specialist actually run on the intended model? Were the hand-offs
clear? Can the reviewer reproduce the result without trusting the analyst's
summary? Does the coordinator expose a failed task instead of filling the gap
with a guess? Inspect the artifacts, try a missing input or denied action, and
repeat a run. Record any manual fixes beside that run. More agents and larger
contexts are not guarantees of better answers.

---

Previous: [Exercise 1 — Skills](../01-skills/README.md) · Next: [Exercise 3 — MCP and data analysis](../03-mcp/README.md).
