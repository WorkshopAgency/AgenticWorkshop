# Agentic Workshop

**Building and employing agents for data analysis and visualization**
Hands-on, individual work.
Dimitrios S. Kanakoglou (dimkan@dtu.dk) · Peter Wad Sackett (pwsa@dtu.dk)

You work in OpenCode on your own laptop. The chat uses OpenCode's free
models, Big Pickle by default. Exercises 1 and 5 call two small models at
OpenRouter directly, with a workshop key the organisers give you. The DTU
models are optional, when they are running. A paid subscription is not
required to participate.

[Download the workshop ZIP](https://github.com/WorkshopAgency/AgenticWorkshop/archive/refs/heads/main.zip) ·
[Quick start](#quick-start--install-download-and-open) ·
[Agenda](#agenda)

## Quick start — install, download and open

1. **Install dependencies:** OpenCode, Git, uv and Python 3.10 or later.
   Nothing else: uv fetches the Python packages an exercise needs when it
   needs them. Open the tab for your computer:

   <details>
   <summary><b>macOS</b></summary>

   In Terminal:

   ```bash
   xcode-select --install
   curl -LsSf https://astral.sh/uv/install.sh | sh
   curl -fsSL https://opencode.ai/v2/install | bash
   ```

   `xcode-select` opens a window that installs Git; accept it and let it
   finish. If it says the tools are already installed, you already have Git.
   Then open a new terminal and install a current Python, since Macs come
   with 3.9:

   ```bash
   uv python install 3.12 --default
   ```

   With Homebrew, `brew install git uv python` does the same for Git, uv and
   Python.

   </details>

   <details>
   <summary><b>Windows (WSL2) and Linux</b></summary>

   On Windows, install WSL2 first: open
   PowerShell as administrator, run `wsl --install`, restart, and open
   **Ubuntu** from the Start menu. Do everything in this workshop in that
   Ubuntu terminal. Then, in Ubuntu or in your Linux terminal:

   ```bash
   sudo apt update && sudo apt install -y git curl python3
   curl -LsSf https://astral.sh/uv/install.sh | sh
   curl -fsSL https://opencode.ai/v2/install | bash
   ```

   Then open a new terminal. Ubuntu 22.04 and later come with Python 3.10 or
   newer; on an older system, also run `uv python install 3.12 --default`.
   On other Linux distributions, install Git, curl and Python with your
   package manager.

   </details>

   **On both:** `npm install -g @opencode/cli` installs the same OpenCode if
   you prefer npm. If you already have OpenCode v2, run `opencode upgrade`
   instead. The terminal version (CLI) is preferred; OpenCode Desktop is also
   supported, and the CLI can run in a browser too, at no extra cost.
2. Go to or make a folder where you want the workshop to be.
3. Get the workshop, either with Git:
   `git clone https://github.com/WorkshopAgency/AgenticWorkshop.git`
   or by [downloading the ZIP](https://github.com/WorkshopAgency/AgenticWorkshop/archive/refs/heads/main.zip) and unzipping it.
   This creates the workshop folder where the rest of the workshop will be. It can be renamed, but the text calls it the workshop root, and every path you will type is
   relative to it.
4. In **OpenCode Desktop**, open that extracted folder as your project—the
   folder containing both `README.md` and `opencode.json`, not its parent.
   For the terminal version, run `opencode` from inside that folder, or
   `opencode serve` for the browser version.
5. To check that your environment is suitable for the workshop, open a terminal inside the workshop root, run `scripts/check-setup.sh`. Fix any ❌.
6. Inside the workshop root, start a new chat. Using the CLI, just write `opencode`. Exiting and running opencode again is a common way for fresh starts
   and incorporating new skills, etc.
   You can also run a terminal command without leaving OpenCode: type `!`
   at the start of the prompt (for example `!scripts/check-setup.sh`), and
   `esc` to go back to the chat. **The command and its output become part of
   the chat and are sent to the model**, so never use `!` for anything
   secret, such as the workshop key.
7. The default model is **Big Pickle**, a free OpenCode model. Other models
   are in the model selector (`/models` in the terminal version); see
   [the models you can use](#llm-models-you-can-use).

Python 3.10 or later is required for security reasons. uv starts the
notebook's Python and the database server in Exercise 4; Python runs the
scripts in the exercises and the ones the agents write. No GitHub account is
needed during the workshop.
There are subfolders in the workshop root for different exercises and you can create your own. When you create your own, you go in those 
and run `opencode` for a clean start for the project/task/exercise. This workshop has dependencies and you need to run opencode from the workshop's root folder.

<details>
<summary>Coming from OpenCode v1, and your global settings</summary>

Leave your existing global `opencode.jsonc`, `package.json` and
`node_modules` alone. OpenCode combines the project configuration with your
global settings automatically.

> **This workshop has moved to OpenCode v2.** v2 ships as a different package,
> `@opencode/cli`, so the old `curl -fsSL https://opencode.ai/install | bash`
> installs v1 and will not match these materials. Install with
> `npm install -g @opencode/cli` and check `opencode --version` reports 2.x.
>
> If you already have v1, remove it first. On Homebrew that is
> `brew uninstall opencode`. Avoid `opencode uninstall`: it removes all related
> files, including your global configuration and saved credentials.
>
> Some commands changed. `opencode agent list` is now `opencode debug agents`,
> `opencode web` is now `opencode serve`, and `opencode debug skill` is gone;
> use `/skills` in the chat instead.

</details>

## Before the exercises: three pieces of advice in a lesson format

### Lesson one — you are in charge of your data

Every prompt you send goes somewhere. Where depends on the model you picked
in the selector, and the difference matters before you paste anything real
into a chat.

| What you choose | Where your data goes |
|---|---|
| **Free models** (the default) | Model requests go to a third party; retention and training terms depend on the specific offer |
| **The workshop key** (Exercises 1 and 5) | Requests go to OpenRouter and the model's provider; send only the exercises' own data |
| **DTU models** (optional) | Model requests go to our DTU service; external tools can still send data elsewhere |
| **Your own subscription** (Codex, Claude, others) | Depends on that provider, and on whether you have opted out of having your data used for training |

User discretion is advised at all times. You are in charge of your data, you
are in charge of the permissions you give your models, and you are in charge
of which data you put in front of them. Nothing in this workshop removes that
responsibility from you, and no default setting decides it for you.

Use public data with external models. Keep anything confidential or personal
on the DTU models, or off the machine entirely.

### Lesson two — `/compact` is your friend

A conversation has a fixed budget. Everything counts against it: your
messages, the model's replies, file contents it has read, and every tool
result it has seen. When the budget runs out mid-task, the run stops being
useful.

`/compact` summarises the conversation so far and continues with the summary
in place of the raw history. You keep the thread, you get the room back.

Get to know it early, on a conversation you do not mind losing, rather than
discovering it when you are deep in an exercise. The sooner the better.

### Lesson three — use `/themes` before anything else to look cool (in front of your PI) and personalise your experience

Opencode (v1 and v2) harnesses comes with their own preinstalled themes. Pick one 
that inspires you to finish this workshop (hint: maybe `matrix` will do the trick).

## Agenda

Every module stands alone: you can start any of them from a fresh chat, skip
one, or come back to it later. Each module's README starts with its
model, needs, and a *Done when* check.

| Module | You'll learn |
|---|---|
| Welcome · `scripts/check-setup.sh` · `/halp hello` | Is my laptop ready? |
| [Concepts — Slides](https://workshopagency.github.io/AgenticWorkshop/workshop.html) | Model, harness, tool, skill, agent, MCP |
| [Exercise 0 — Plugins](exercises/00-plugins/README.md) | What a plugin is; install the two you use today |
| [Exercise 1 — RAG](exercises/01-rag/README.md) | Why retrieval stops a weak model inventing answers |
| [Exercise 2 — Skills](exercises/02-skills/README.md) | Turn a repeated task into a tested skill |
| [Exercise 3 — Agents](exercises/03-agents/README.md) | Instructions and permissions, and a team of agents |
| [Exercise 4 — MCP](exercises/04-mcp/README.md) | Connect a database, then check its answers |
| [Exercise 5 — Decision model](exercises/05-decide/README.md) | Typed decisions with probabilities instead of prose |
| [Exercise 6 — Safety](exercises/06-safety/README.md) | Prompt injection, and what permissions do and don't stop |
| Wrap-up | When to use an agent, and how to check one |

<details>
<summary>The words we use: harness, skill, agent, MCP, plugin</summary>

* **Harness**: the program around the model. Here it is **OpenCode**: it builds
  what the model sees, runs the tools on your laptop, and asks you first.
* **Skills**: reusable instructions an agent loads for a task, optionally with
  supporting scripts. A skill explains a workflow; it is not itself a tool call.
* **Agents**: AI components that use skills to achieve a goal. An agent can
  **reason, plan, choose skills, execute actions, and adapt** based on the
  results.
* **MCP**: a standard way to connect the agent to a capability that lives
  outside OpenCode, such as a database or a public biological data service.
  The server is either a program OpenCode starts on your laptop, or a remote
  service it connects to over the network.
* **Plugins**: code that changes OpenCode itself, such as the sidebar and the
  notebook you install in Exercise 0. A plugin runs with your permissions and
  nothing sandboxes it, so look before you install one.

**Simple example:** a travel-planning agent might have skills such as *search
flights*, *find hotels*, and *create itinerary*. The **agent** decides which
skills to use and in what order to plan the trip.

</details>

<details>
<summary>The workshop folder: where agents, skills and plugins go</summary>

Open the workshop root folder. OpenCode reads agents and skills from
`.opencode/`; the exercise folders hold the teaching materials.


This is the structure of the extracted folder. Everything you will be asked to
run or open is a path relative to this root, so the folder's own name does not
matter.
```text
AgenticWorkshop/
   opencode.json                Model connections, limits, permissions, MCP servers
   admin.md                     Server notes for the organisers
   scripts/check-setup.sh       Is this laptop ready? (--module <name> for one module)
   .opencode/                   What OpenCode loads: agents, skills and plugins
      agents/
         HALp.md                Hidden hint helper, invoked with /halp
         bad-agent.md           Basic PDB agent example, Exercise 3a
         good-agent.md          More explicit PDB agent example, Exercise 3a
         genome-coordinator.md  Delegates to the four specialists below, Exercise 3e
         genome-auditor.md      Checks data, units and missing values
         genome-analyst.md      Writes and runs the analysis
         genome-visualizer.md   Makes the plots
         genome-reviewer.md     Independently rechecks the results
         safe-analyst.md        Locked-down data agent, Exercise 6
      commands/
         halp.md                The /halp command
      scripts/
         halp-context.py        Show safe limits or adjust one context with approval
      skills/
         skill-builder/         A subfolder INSIDE skills
            SKILL.md            The skill-builder instructions
      plugins/                  The plugins you clone in Exercise 0; only its README is in Git
   exercises/
      00-plugins/               Install the two plugins and the workshop key
      01-rag/                   Retrieval-augmented generation, as a notebook
      02-skills/
      03-agents/
         starter/csv-profile/   A ready-made skill for Exercise 3d
         buggy/                 A script that runs and prints wrong numbers, for 3f–3j
      04-mcp/
         data/                  The PDB snapshot, and byo/ for three other datasets
         scripts/               Build the DuckDB database
      05-decide/                A typed decision model built on token probabilities, as a notebook
      06-safety/                A data file with a planted instruction
      shared/                   look.py: the colours the exercise scripts print in
   outputs/                     Where your results go, one folder per module (not in Git)
   mcp/                         Notes on the four MCP servers this project configures
   slides/                      The concepts deck, published from Markdown
```
OpenCode reads `.opencode/` folder for project agents, skills and plugins, while `opencode.json` in the workshop root
contains the model connections, limits and permissions.

`skills` is the parent skill folder and `skill-builder` - the workshop supplied skill - is a separate subfolder
inside it. The complete path is `.opencode/skills/skill-builder/SKILL.md`.
GitHub collapses a chain of folders with a single child into one line, such
as `skills/skill-builder`; that is a compact display, not a single folder
name.

Each additional skill gets its own subfolder and `SKILL.md`. Agent definitions
are Markdown files directly inside `.opencode/agents/`. A `.gitkeep` file in
an otherwise empty folder is only a Git/ZIP placeholder, not an agent or skill.

Files inside `exercises/` are not loaded by OpenCode. An agent or skill only
takes effect once it is in `.opencode/agents/` or `.opencode/skills/`, which
is why Exercise 3d asks you to copy its starter skill there. Plugins are
loaded from `.opencode/plugins/` when OpenCode starts, which is why Exercise 0
clones the plugins there and then restarts OpenCode.

The leading dot may hide `.opencode` in your file browser, but OpenCode can
still read it. Do not rename it, move it out of the project, or put
`opencode.json` inside it. Open the repository root, not `.opencode` itself.

The `exercises/` and `mcp/` folders organize workshop materials. Creating
an `mcp/` folder does not activate an MCP server: `mcp/` holds documentation
only. An MCP server is configured under `mcp` in `opencode.json`, and is
either a program downloaded on demand or a remote service you connect to.
Four are configured and all ship switched off; Exercise 4 turns one on.
See [mcp/README.md](mcp/README.md) for what each provides.

See the OpenCode documentation for [agents](https://opencode.ai/v2/docs/agents/)
and [skills](https://opencode.ai/v2/docs/skills/).

</details>

## How OpenCode works in this workshop

OpenCode is the **harness**: the program around the model. You type in a
chat; the model proposes what to do; OpenCode runs the tools on your laptop,
after asking you, and sends the results back to the model. Everything you do
today happens in that loop.

<details>
<summary>Agents, models, approvals and commands</summary>

**Agents.** OpenCode always runs one agent in the chat. Switch with
**shift+tab** (in Desktop, with the agent selector); the current one is shown
under the input box.

| Agent | Use it to |
|---|---|
| **Plan** | Discuss and design. It reads files without asking, but cannot run commands or create or change files |
| **Build** | Do the work: write files and run commands, asking you first |
| Workshop agents | `bad-agent`, `good-agent`, `genome-coordinator`, `safe-analyst`, … are used in Exercises 3 and 6 |

**Agents and models.** The model shown under the input box answers for the
current agent. Plan and Build can use different models: add a `model` to the
agent in `opencode.json`, next to the `permissions` the workshop already gives
Plan, for example

```json
"agents": { "plan": { "model": "opencode/mimo-v2.6-flash-free", "permissions": [ … ] } }
```

Restart OpenCode; shift+tab then switches agent and model together.

**One chat, one history.** Switching agent or model inside a chat keeps the
whole conversation: the next model receives your messages, the earlier answers
and every tool result, including the contents of files the agent read, and
all of it goes to that model's provider. Each model keeps its own cache, so
after a switch the history is processed again. To compare models, or to keep
something away from a provider, start a new chat.

**Approvals.** When an agent wants to edit a file or run a command, OpenCode
shows a prompt. Read what it wants to do, then choose:

- **Allow once**: the safe default. It will ask again next time.
- **Always allow**: stops it asking again for that kind of action. Use it only
  for actions you understand.
- **Reject**: refuses. The agent has to find another way, or tell you it
  cannot.

Every action the agent takes is listed in the chat as a tool call. The tool
calls, not the agent's summary, are the record of what happened.

**Commands you will use:**

| Command | What it does |
|---|---|
| `/models` | Choose the model. The default is Big Pickle, a free model; the DTU models, when running, are under **DTU** |
| `/skills` | List the skills OpenCode has found |
| `/mcps` | Switch MCP servers on and off (Exercise 4) |
| `/compact` | Summarise a long chat to free up the context window |
| `/halp <exercise> <question>` | Ask HALp, the workshop helper, for a hint |
| `/sidebar` | Change what the sidebar shows (plugin from Exercise 0). `ctrl+x b` shows or hides it |
| `/notebook <file>` | Open a notebook next to the chat (plugin from Exercise 0) |
| `opencode reload` | In a terminal: make OpenCode pick up new skills, agents or settings |
| `!<command>` | Run a shell command without leaving OpenCode; `esc` goes back to the chat. See below |

**Running a command inside OpenCode.** Type `!` at the start of the prompt:
it switches to **Shell**, and the command runs in the workshop folder with
its output shown in the chat. Most "in a terminal" steps can be done this way.
But the command and its output become part of the conversation and are sent
to the model with your next message. So never use `!` for anything secret,
such as the workshop key in Exercise 0c, and think twice before printing
data that could carry instructions (Exercise 6). Long outputs also fill the
context like any other message.

Start a **new chat** for each exercise, so the model does not carry the last
one's context into the next. Your results go under `outputs/<exercise>/`,
which Git ignores.

</details>

## Getting help

### Ask HALp

HALp offers hints and setup help, not finished exercise answers. In a **fresh
chat**, try `/halp Where should I start?` It uses a **free external model**:
public information and redacted errors only; do not use a private research chat.

<details>
<summary>Using HALp and returning to your exercise</summary>

Open a **fresh chat** and type `/halp` followed by your question:

```text
/halp I am on Exercise 2c. Where should I copy my skill?
/halp Why can I not see the workshop agents?
```

HALp reads the current workshop instructions and gives hints and setup help,
not finished exercise answers. It can help adjust context settings after
you approve the change. It initially uses **Big Pickle, a free external model**:
share public information and redacted errors only. Do not invoke it inside
a private research conversation, because the existing history can reach
that provider too.

When you return to an exercise, select your exercise agent and model again.
HALp's permissions and context help are just below.

</details>

<details>
<summary>HALp's permissions, privacy and context adjustments</summary>

Start a **fresh chat**, then type `/halp` followed by your question:

```text
/halp I am on Exercise 2c. Where should I copy the skill folder?
/halp What should I check before increasing Mistral's context?
```

HALp reads the current exercise instructions, offers one next step and helps
with setup. Its instructions prohibit exercise solutions; check its advice
as you would any model output. It uses **Big Pickle,
a free external model**: only send public workshop information and redacted
errors. The command switches the current chat, so its existing history can
also reach that provider—do not invoke it inside a private research chat.

HALp can show this project's DTU budgets and change `limit.context` and
`limit.output` up to the published running maxima, with your command approval.
Higher server limits need organiser verification. The supplied helper cannot
change URLs or keys. HALp is not allowed to operate the
cluster or publish your work. Read every approval request.

To resume an exercise, select **Build** or your exercise agent **and model**
again. HALp is hidden from the usual agent selector; `/halp` is the intended
entry point. This is a UI convention, not an access-control boundary.

</details>

### Try this first

If `/halp`, workshop agents or updated settings are missing, OpenCode may still
be using cached configuration. Exit OpenCode, then run these commands **in your
terminal, inside the extracted workshop folder**:

```bash
opencode reload
opencode .
```

Start a fresh chat and try `/halp hello`. Simply closing and reopening the
interface may not refresh its background service. This reload does not edit
your files. If the problem remains, show an organiser
the error and your `opencode --version`; do not reinstall or delete your settings.

<details>
<summary>So many errors - so little time</summary>

| What you see | What to do |
|---|---|
| `/halp`, agents or updated settings are missing | [Try this first](#try-this-first): exit, run `opencode reload` in the workshop folder, then reopen. |
| DTU models are missing | They are optional and may not be running. Otherwise check that OpenCode opened the folder containing `opencode.json`, then follow the reload step above. |
| Connection failed / 503 | Ask an organiser to check the model's start command. |
| After upgrading OpenCode: "port … is already in use" | The old version is still running in the background. Run `opencode service restart`, then start OpenCode again. |
| Invalid API key / 401 | In Exercises 1 and 5: check `.openrouter-key` (Exercise 0c). In the chat: check for old provider settings. |
| Not found / 404 | Use a fresh workshop download; ask an organiser to check the URL if it persists. |
| Free models or other providers are missing | Check model visibility and v2 `disabled` settings; ask an organiser about stale v1 configuration. The supplied workshop JSON does not hide them. |
| Too many requests / 429 | Wait briefly and try again; the servers are shared. |
| Context too long | Compact the conversation or start a new chat. |
| Repeated compaction or the same reads without progress | Keep the supplied `compaction` settings: OpenCode 2.0.14's default buffer can exceed a small local context budget. Restart with the current workshop configuration and a fresh chat; send persistent failures to an organiser. |

Send Peter or Dimitrios the **model name and exact error message** if you need
help. Do not disable certificate checks or change server settings yourself.

OpenCode may ask to edit files or run commands **on your computer**. Review
those requests before allowing them. Work in the exercise folder.
When comparing models, start a fresh chat: switching models within a chat
can keep the earlier conversation and tool results.
</details>

## LLM Models you can use

The chat uses Big Pickle, a free model, unless you choose another with `/models`. Exercises 1 and 5 use the workshop key; the DTU models are optional.

<details>
<summary>Free, paid, local and DTU models: what to be aware of</summary>

First be aware of the pricing - it can be creative.
* Free models - check the provider's retention and training terms; no price does not mean private
* Paid models - often subscription-based. Maybe as safe and confidential as the provider says
* Local models - running on your own hardware. As confidential as your system
* DTU models - hosted by the workshop organisers, optional and only when running. Use the supplied public data and follow DTU's data-handling rules

</details>

### Free models from OpenCode

<details>
<summary>Details</summary>

The free models OpenCode offers at the time of writing. Free offers change
without notice, and your local `opencode models` list can still show models
that are gone; `scripts/check-setup.sh --module 03-agents` checks the live
list.

| Model ID | Notes |
|---|---|
| `opencode/big-pickle` | **Workshop default**, and the 3e coordinator and auditor. Free-period data may be used to improve the model |
| `opencode/mimo-v2.6-flash-free` | 3e analyst. Free-period data may be used to improve the model |
| `opencode/beam-free` | 3e visualizer and reviewer. Not used for training; kept 30 days for safety reasons |
| `opencode/deepseek-v4.1-flash-free` | Zero-retention provider |
| `opencode/glm-5.3-flash-free` | Zero-retention provider |
| `opencode/flint-40b-free` | Free-period data may be used to improve the model |
| `opencode/nemotron-3.5-lightning-free` | Free-period data may be used to improve the model |
| `opencode/nemotron-3.5-super-vl-free` | Also reads images. Free-period data may be used to improve the model |
| `opencode/beam-free` | Not used for training, but kept for 30 days for safety. Not offered in some countries |
| `opencode/jev-1.13-free` | TypeSafe AI's model for fast, structured decisions. OpenCode publishes no data terms for it |

**Watch for contributor models.** None is offered at the moment, but they come
and go. A contributor model can train on what you submit to it, and the word
`contributor` is in its model ID but **not** in the name the selector shows
you. If you want to avoid them, check the ID rather than the name.

None of the agents in exercise 3e uses a contributor model. Big Pickle and
MiMo may still use free-period data to improve the model, and Beam's provider
keeps data for 30 days, according to
[OpenCode's model page](https://opencode.ai/docs/zen/).

Free does not mean private, and terms differ between offers. Use public
exercise data with external models, and
send nothing confidential or personal. See
[OpenCode's model-specific privacy terms](https://opencode.ai/docs/zen/#privacy).

Sources: [live model list](https://opencode.ai/zen/v1/models),
[model catalogue](https://models.dev/api.json),
[Zen pricing](https://opencode.ai/docs/zen/#pricing).

</details>

### The workshop key: two small models at OpenRouter

<details>
<summary>Details</summary>

Exercises 1 and 5 call models directly, outside OpenCode, so you can see
exactly what goes in and what comes back. They use
[OpenRouter](https://openrouter.ai), with a key the organisers give you at
the start (Exercise 0c):

| Exercise | Model | For |
|---|---|---|
| 1 — RAG | Mistral Nemo 12B, and `bge-base` for search | Answers from retrieved pieces |
| 5 — Decision model | Llama 3.1 8B | Answers with token probabilities |

The key is shared by the room and has a spending limit. Keep it in
`.openrouter-key`, which Git ignores; never paste it into a chat or commit it.

</details>

### The DTU models (optional)

<details>
<summary>Details</summary>

The workshop project shows one **DTU** group containing:

| Model | Context | Maximum output | Description |
|---|---:|---:|---:|
| GPT-OSS 20B | 16384 | 4096 | Alternative general model |
| Mistral Nemo 12B | 16384 | 4096 | Smaller checkpoint; check tool behaviour on your task |
| Qwen 3.6 35B-A3B | 16384 | 4096 | Analysis and tool use |
| Qwen 3.8 27B FP8 | 32768 | 4096 | Larger starting context |

The DTU group is added alongside OpenCode's available free models
and your other configured providers. This file does not restrict the provider
list or change your global configuration. Other providers may require their
own sign-in or API key.

**Does opening the folder start the models?** No. It connects to models that
Peter and Dimitrios start when they are available; the workshop does not
depend on them. With them running, `RAG_DTU=1` in front of the commands of
Exercises 1 and 5 uses them instead of the workshop key.

See [OpenCode project configuration](https://opencode.ai/v2/docs/config/#per-project).

</details>

### Show free models if they are hidden

<details>
<summary>Details</summary>

The DTU Qwen 3.8 effort choices are **low** and **medium**, plus the model's
default when no effort is selected. Mistral Nemo has **no reasoning-effort
selector**. These are model-specific: do not copy an effort from another model.
After updating the workshop files, run `opencode reload`, reopen OpenCode and
select the model again if an old session still shows an unsupported effort.


- **Desktop:** open the model selector → **Manage models**, search for a
  model above, and turn its switch on under OpenCode. Return to the selector
  and choose it. Enable individual free models rather than every paid model.
- **Terminal:** type `/models`, search for the model name, and select it.
  It does not have to be a favourite to appear in search. If your version
  shows a Favourite action, you can use it for easier access next time.
- If the entire OpenCode provider is missing, check your other project/global
  configuration for v2 `providers` entries and a model's `disabled: true`
  setting. Ask an organiser to inspect stale v1 settings rather than adding
  `enabled_providers` or `disabled_providers` to this v2 project. The supplied
  workshop configuration does not hide the free models. Preserve unrelated settings.
- Restart OpenCode after configuration changes. If a listed model is still
  absent, check your OpenCode version and the current live list; a setting
  cannot restore a retired offer. Do not add a paid model as a substitute
  unless you intend to pay.

The Desktop visibility switches and configuration restrictions are different
things. We do not change your saved visibility choices or global settings.
See [provider filtering](https://opencode.ai/v2/docs/config/#disabled-providers).

</details>

### Your own subscriptions or API accounts

<details>
<summary>Details</summary>

Use `/connect` in the terminal, or **Connect provider** in Desktop, choose
your provider, and complete its supported sign-in. Then select its model.
For example, OpenCode documents using a GitHub Copilot subscription.
Not every chat subscription includes third-party or API access; separate
API usage may be billed. Keep personal keys out of this repository.
See [supported providers and sign-in methods](https://opencode.ai/v2/docs/providers/).

Changing the selected model changes the chat model. Background tasks, such
as naming the chat, use a small model from the same provider as your chat, so
they do not send your conversation anywhere else.

</details>

## Reference

You do not need these for the exercises.

### Connecting to the DTU models by hand

<details>
<summary>Connection fields for a separate project without the supplied JSON</summary>

The ZIP method above is the workshop setup. These fields are only a fallback
for connecting in another project. The form creates separate providers; it
does not reproduce the single DTU group. There is no need to add these
separate providers when you already use the supplied workshop JSON.

Choose **Custom provider** and use the fields below. Create a separate
provider for each model you want. The connection type is **OpenAI-compatible**.

Use each Base URL exactly as shown, with no additional path at the end.
After entering the provider and model fields, select **Submit**.

The connection form may not offer context/output fields. If it does not,
set those limits in JSON using the instructions after the tables.
The supplied JSON already contains them.
See [OpenCode custom providers](https://opencode.ai/v2/docs/providers/#custom-provider).

#### Qwen 3.6 35B-A3B

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-qwen36` |
| Display name | `DTU Qwen 3.6` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/qwen36` |
| API key | Leave empty |
| Models → Model ID | `qwen36` |
| Models → Display Name | `Qwen 3.6 35B-A3B` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `16384` |
| Output limit, in JSON | `4096` |

#### Qwen 3.8 27B FP8

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-qwen38` |
| Display name | `DTU Qwen 3.8` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/qwen38` |
| API key | Leave empty |
| Models → Model ID | `qwen38` |
| Models → Display Name | `Qwen 3.8 27B FP8` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `32768` |
| Output limit, in JSON | `4096` |

#### Mistral Nemo 12B

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-mistral` |
| Display name | `DTU Mistral` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/mistral` |
| API key | Leave empty |
| Models → Model ID | `mistral` |
| Models → Display Name | `Mistral Nemo 12B` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `16384` |
| Output limit, in JSON | `4096` |

#### GPT-OSS 20B

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-gptoss` |
| Display name | `DTU GPT-OSS` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/gptoss` |
| API key | Leave empty |
| Models → Model ID | `gptoss` |
| Models → Display Name | `GPT-OSS 20B` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `16384` |
| Output limit, in JSON | `4096` |

</details>

### Changing your context setting (DTU models)

<details>
<summary>Details</summary>

The project sets OpenCode v2's compaction buffer to `2048` and retains about
`4096` recent tokens. Its default `20000` buffer is larger than our smaller
DTU context budgets and caused repeated compaction during testing. Leave
these supplied settings in place. This client setting does not allocate GPU
memory or increase a model server's context capacity.

Context is the space available for instructions, conversation, tool results
and the answer. Output is the maximum answer length, including reasoning.
Both are measured in tokens.

There are three different settings: the **server's verified maximum**, your
**selected context budget**, and your **answer limit**. Raising a number in
your JSON does not increase the server's capacity.

| Model | Starting context | Maximum running context | Starting output | Maximum output |
|---|---:|---:|---:|---:|
| Qwen 3.6 | 16384 | 32768 | 4096 | 4096 |
| Qwen 3.8 | 32768 | 32768 | 4096 | 8192 |
| Mistral Nemo | 16384 | 16384 | 4096 | 4096 |
| GPT-OSS | 16384 | 16384 | 4096 | 8192 |

**Students may choose up to the maxima above without asking an organiser.**
Start with the supplied
values and increase when useful. Changing JSON does not enlarge the server.
Higher limits require a server change and validation by an organiser.
**Do not select 262144 for ordinary workshop tasks.** Long requests consume
shared memory and processing time, leaving less capacity for other teams.
Setting a ceiling alone does not immediately allocate that entire amount.

These are useful sizes to recognise, not a requirement to use powers of two:

| Context value | When to consider it |
|---:|---|
| `4096` | Unsuitable with our `4096` answer allowance: input and instructions also need space |
| `8192` | Short tasks with enough room left for tools and input |
| `16384` | Default for GPT-OSS, Mistral and Qwen 3.6 |
| `32768` | Default for Qwen 3.8; confirm server support before increasing another model |
| `65536` | Only with organiser approval and a verified server capacity |
| `131072` | Target ceiling for Mistral/GPT-OSS; not a normal workshop budget |
| `262144` | Target ceiling for Qwen only; do not use without explicit approval |

#### Change the budget in your own project

In `opencode.json`, find the model under `providers → dtu → models → model ID`.
Edit `limit.context` and/or `limit.output`, within the table above. For example,
Qwen 3.8 at its current maximum context and output:

```json
{
  "name": "Qwen 3.8 27B FP8",
  "limit": {
    "context": 32768,
    "output": 8192
  }
}
```

This is one model entry, not a complete OpenCode configuration. Preserve the
other fields, save, then run `opencode reload` and reopen OpenCode.
Alternatively, from the project root:

```bash
python3 .opencode/scripts/halp-context.py --model qwen38 --context 32768 --output 8192
opencode reload
```

You can also ask `/halp` to make this change; approve the command when prompted.
Use plain integer digits: **`262144`, not `262.144` or
`262,144`**. Never exceed the model's verified server limit. The total includes
the answer; a 32768 context does not allow 32768 input tokens plus a 4096 answer.

This model entry applies to every agent using that provider/model ID in the
project. It is not an agent-level setting. Do not put `context` in an agent's
Markdown header or copy your personal configuration/keys into a team submission.
For a new experiment, use a fresh chat; compact or shorten an existing long
conversation before lowering its budget. Return to the supplied defaults
after your task.
</details>

---

After the workshop: [additional tools, projects and research](additional.md).

To go deeper: exercises with more time end with a **Dive Deeper** section,
for example [Exercise 1](exercises/01-rag/README.md) and
[Exercise 2](exercises/02-skills/README.md).

For WorkShop organisers: [server administration and model settings](admin.md).
