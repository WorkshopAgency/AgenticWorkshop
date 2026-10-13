# Bonus exercises

Two optional exercises. Do neither, one, or both, in any order, whenever you
have time. Nothing later/earlier depends on them.

- **5a — Plugins.** The one extension mechanism that runs code on your laptop
  before you type anything. Mostly reading and one small install.
- **5b — Finding bugs.** A working script that prints wrong answers, and the
  ladder of things to reach for, starting with what OpenCode already has.

If you build something in 5b that you would use again, Exercise 4 is how you
share it.

---

# Exercise 5a — Plugins, and why they are different

Exercise 4a asked whether a job wants a skill, an agent or an MCP server.
There is a fourth option, and it is the one to be careful with.

| | What it is | When it runs |
|---|---|---|
| Skill | Markdown the agent may load | When the agent decides it is relevant |
| Agent | Markdown defining a role and permissions | When you select it |
| MCP server | A separate program exposing tools | When the agent calls a tool, subject to permissions |
| **Plugin** | **JavaScript or TypeScript** | **At startup, before you type anything** |

An OpenCode plugin is a JS/TS module that receives Bun's shell API. It loads
automatically from `.opencode/plugins/` or `~/.config/opencode/plugins/`, and
npm plugins are installed automatically by Bun at startup. The documentation
describes hooks for shell execution, file events and permissions, and no
sandbox.

**Two things to know before you try any of this on v2.**

Most plugins you will find were written for v1, and **v1 plugin implementations
do not run in v2**. The plugin API changed. A plugin can install cleanly, appear
in the list and simply never do anything. Treat "it installed" as no evidence at
all, and check that it actually did something.

**Plugin state goes stale.** v2 keeps a background service that caches
configuration, so what `opencode plugin list` or `opencode mcp list` reports can
be the previous state rather than the current one. After adding, removing or
editing a plugin, run `opencode reload`, or `opencode service restart` if that is
not enough. An enabled server can otherwise keep reporting as disabled.

v2 also adds a plugin command: `opencode plugin list`, `add`, `check`, `update`,
`remove`.

A skill is instructions your agent may follow. An MCP server is a tool your
agent must ask to use. A plugin is code that already ran.

## What to check before installing one

There are over 130 plugins in the community registry. These five columns
decide whether you can make an informed choice:

| Check | Why |
|---|---|
| Lines of code | Can you read it? 80 lines is a different decision from 27,000 |
| Runtime dependencies | Each one is another author you are trusting |
| Outbound URLs | Does it send anything anywhere |
| Licence | No licence means no permission to use it |
| Last commit | Abandoned code with shell access is a liability |

Four plugins, measured on 21 September 2026:

| Plugin | Lines | Deps | Outbound | Licence |
|---|---:|---:|---|---|
| [opencode-simple-notify](https://github.com/Yusuzhan/opencode-simple-notify) | 77 | 0 | none | MIT |
| [envsitter-guard](https://github.com/boxpositron/envsitter-guard) | 920 | 0 | none | MIT |
| [Context Analysis](https://github.com/IgorWarzocha/Opencode-Context-Analysis-Plugin) | 1047 | 1 | none | **none** |
| [cc-safety-net](https://github.com/kenryu42/cc-safety-net) | ~27 MB bundled | 0 | one npm version check | MIT |

## Read one, then install it

`opencode-simple-notify` is 77 lines in one file with no dependencies. It
sends a desktop notification when a session finishes, errors, **asks for
permission**, or waits for your answer. That last one is the useful part: a
run that stops for approval is easy to miss.

Read the whole file first. It is short enough that you have no excuse!

```bash
curl -fsSL https://raw.githubusercontent.com/Yusuzhan/opencode-simple-notify/main/index.js | less
```

Then install it project-locally and restart OpenCode:

```bash
mkdir -p .opencode/plugins
curl -fsSL -o .opencode/plugins/notify.js \
  https://raw.githubusercontent.com/Yusuzhan/opencode-simple-notify/main/index.js
```

macOS uses `osascript` and Linux uses `dbus-send` with a notification daemon.
Inside WSL2 it will probably do nothing, which is itself worth seeing.

**Rehearsed on v2.0.14, 23 September 2026:** this exact plugin failed to load:
`Plugin must export a default definition with an id and an effect or setup function`.
Treat it as an intentional compatibility-check example, not a working
notification solution. Reloading cannot repair a v1 plugin API mismatch.
Inspect the diagnostic, then remove the test file.

Remove it by deleting the file (or keep it).

## Two things to notice

<details>
<summary>Try Dimitrios's Sidebar Plus — a working OpenCode v2 plugin</summary>

[opencode-sidebar-plus](https://github.com/dskanakoglou/opencode-sidebar-plus)
adds a context gauge, agent task list, live tool activity, shell timers, changed
files, alerts and clickable subagent sessions. `/details` shows run history;
`/sidebar` lets you switch individual features on and off. It requires
**OpenCode 2.0.16 or later**, not v1 or the workshop's older 2.0.14 installation.
Check `opencode --version` first.

Read its `server.ts` and `tui.tsx` before installing. This is executable plugin
code, not a skill. Clone it into a separate folder outside the workshop:

```bash
git clone https://github.com/dskanakoglou/opencode-sidebar-plus.git
```

Or download and extract its ZIP. In the workshop's `opencode.json`, add this
top-level field, using the **absolute path** to your extracted plugin folder:

```json
"plugins": ["/absolute/path/to/opencode-sidebar-plus"]
```

Merge this entry with any existing `plugins` array; do not replace the whole
configuration. On WSL, use the Linux path. This loads both the sidebar and its
small `todo` tool. No build step is required. Exit OpenCode, run
`opencode reload` from the workshop folder, and reopen it.

Try `/sidebar`, then ask your agent to record a short task list for its next
multi-step task. Use `/details` to inspect the run. For Exercise 2c, the
Sub-agents section shows actual direct child sessions once delegation happens;
click one to inspect it. It does not list all installed agent definitions or
create a swarm for you. Agent/model selection remains in OpenCode's usual UI.

The original one-line Context widget may remain visible too. The project's
[installation guide](https://github.com/dskanakoglou/opencode-sidebar-plus#install)
shows the optional `cli.json` setting to hide it and how to install the sidebar
without the additional `todo` tool.

To remove the plugin, remove only its entry from `plugins`, reload and reopen.
If you hid OpenCode's original Context widget, restore that setting as well.
Treat status indicators as aids, not evidence that the analysis is correct.

</details>

**Popularity and auditability are different axes.** `cc-safety-net` has over
1500 stars, an MIT licence, zero runtime dependencies, and blocks destructive
commands. It is also about 27 MB across hundreds of files with a minified
build, so nobody in this room is going to verify it. That is a choice you are
allowed to make, as long as you know you are making it.

**Search `cc-safety-net` on GitHub.** More than one repository has that name.
Decide which one you would install, and how you decided.

The Context Analysis plugin computes a token breakdown locally and is genuinely
useful next to `/compact`. Its README also suggests pasting the README into
OpenCode and asking it to install the plugin for you. Exercise 3f says what is
wrong with that.

---

# Exercise 5b — Finding bugs

There is a working script in [`buggy/`](buggy/). It runs, exits cleanly and
prints three numbers. All three are wrong, and one of them is wrong in two
different ways.

```bash
cd _sectionday/exercises/05-bonus/buggy
python3 summarise.py
```

```text
total bases covered: 404
first region 1-based start: 1000
sorted order: ['chr1', 'chr1', 'chr10', 'chr2']
```

Nothing errored. This is the class of bug that reaches publication.

Work through the steps in order. The point of the order is that each step is
cheaper than the next, and most bugs do not need the later ones.

## Step 1 — What OpenCode already has

Before installing anything, these are built in:

| Command | Use |
|---|---|
| `/review` | Review changes. Takes `commit`, `branch` or `pr`; defaults to uncommitted |
| `/fork` | Branch the session from an earlier message |
| `/undo`, `/redo` | Take back the last message, or restore it |
| `/diff` | See what changed |
| `/compact` | Summarise the session to reclaim context |
| `/export` | Export the transcript as JSON |

**Fork before you let an agent try a fix.** This branches the conversation,
not the filesystem. Preserve the original script or use a separate copy;
both chats can otherwise edit the same files. Compare the two attempts.

In a Git checkout, `/review` reviews changes (uncommitted, commit, branch or
PR), not automatically every file in the project. A fresh ZIP has no Git
history, and the supplied script may have no diff. In that case ask in Plan:
“Review `_sectionday/exercises/05-bonus/buggy/summarise.py` and its BED input. Do not edit
anything.” Note what it finds and what it misses. Use `/review` after a fix
when there is an actual diff to inspect.

## Step 2 — A skill

A skill is Markdown, so it cannot execute anything by being present. That
makes it the safest thing to add.

Write one, or adapt [a published debugging skill](https://github.com/AllThingsSmitty/agent-skills/tree/main/skills/debug),
which opens with a rule worth keeping:

> Debugging is hypothesis-driven investigation, not random exploration. The
> goal is to find the root cause, not just a fix that makes the symptom
> disappear.

Give your skill these steps, then use it on the script:

1. Reproduce and record the actual output before reading any code.
2. State a hypothesis and the evidence for it, and what you ruled out.
3. Name the smallest change that would fix it.
4. Say what you did not check.

## Step 3 — An agent

A skill advises. An agent decides what is allowed.

Build a reviewer that denies edits **and shell commands**. Denying only edits
does not prevent a shell command from rewriting files. Review first; use a
separate, approved Build task to execute tests or implement a fix.

```yaml
---
description: Reviews code and reports defects with evidence. Cannot edit or publish.
mode: all
model: dtu/gptoss
steps: 15
permissions:
  - { action: '*', resource: '*', effect: deny }
  - { action: read, resource: '*', effect: allow }
  - { action: glob, resource: '*', effect: allow }
  - { action: grep, resource: '*', effect: allow }
  - { action: external_directory, resource: '*', effect: deny }
---
```

Run it on the script and compare with what `/review` told you in step 1.

## Step 4 — The boring tools

An agent driving a deterministic tool beats an agent reasoning about code
(and Peter will love me for including these).

| Tool | Finds |
|---|---|
| `git bisect` | Which commit broke it. Mechanical, no guessing |
| `pytest -x --lf` | Stop at the first failure, then rerun only failures |
| `ruff`, `mypy` | Bugs that never reach runtime |
| `diff <(old) <(new)` | Proof that an output actually changed |
| A known-answer file | The only thing that catches a silently wrong number |

None of the bugs in the script would be caught by a linter. All of them are
caught by one small file of expected answers. Ask your agent to write that
file first, and notice how differently the session goes.

## Step 5 — Build your own checker

Write a checker for something you actually care about: a file format, a
coordinate convention, a column that must never be negative, a join that must
not change the row count.

Make it fail loudly on bad input and say nothing on good input. Then break the
data on purpose and confirm it fails. A check you have never seen fail is not
a check.

If it is useful, publish it with [Exercise 4](../04-share/README.md).

## What the script is actually doing wrong

Do not read this until you have tried.

<details>
<summary>The four bugs</summary>

1. **`end - start + 1`.** BED intervals are half-open, so a region is
   `end - start` bases. Off by one per region, so the error grows with the
   number of rows and is invisible on any single row.
2. **BED starts are 0-based.** Reporting `start` as a 1-based coordinate
   understates every start by exactly one base. BED is 0-based; GFF, GTF and
   VCF are 1-based.
3. **Lexicographic chromosome sort.** `chr10` sorts before `chr2`.
4. **Overlapping regions are double counted.** `regionA` is chr1:1000-1100 and
   `regionD` is chr1:1050-1200. They overlap by 50 bases.

So "total bases covered" has three defensible answers:

| Answer | Meaning |
|---|---|
| 404 | What the script prints. Wrong |
| 400 | Sum of region lengths, after fixing the off-by-one |
| 350 | Distinct bases actually covered, after merging the overlap |

An agent that fixes the arithmetic still returns 400. Getting to 350 requires
asking what "covered" means, which no amount of reading the code will tell
you. That is the difference between a fix and an answer.

</details>

---

## Where to go next

- [Additional resources](../../../additional.md): model serving, agent frameworks, scientific tools and papers to explore after today.
- [Dimitrios's Sidebar Plus](https://github.com/dskanakoglou/opencode-sidebar-plus): see your agent's context, tasks, activity and delegated subagents. Follow its [installation guide](https://github.com/dskanakoglou/opencode-sidebar-plus#install), or expand the Sidebar Plus section in Exercise 5a above.

Previous: [Exercise 4 — Share what you built](../04-share/README.md).
