# Exercise 0 — Plugins

| | |
|---|---|
| **Model** | None; you only install |
| **Needs** | `scripts/check-setup.sh` passed, Git, and the workshop key from the organisers |
| **You'll learn** | What a plugin is, how to look at one before you install it, and how to take it out again |
| **Done when** | A sidebar shows next to the chat, `/notebook` opens a notebook, and `.openrouter-key` holds the workshop key |
| **If stuck** | `/halp 00-plugins <what you tried>` |

## Why plugins

A skill gives an agent instructions. An MCP server connects it to a tool
outside OpenCode. A **plugin** changes OpenCode itself: it is code that runs
inside OpenCode, with the same access to your laptop as OpenCode has, and
nothing sandboxes it. So you look before you install, you pin a version, and
you know how to take it out again.

You install two plugins, written for this workshop, and use them in the
exercises that follow:

- **opencode-sidebar-plus** shows what each agent is doing: its context, its to-do
  list, the tool it is running, and every sub-agent it starts.
- **opencode-notebook** opens a notebook next to the chat. You run it one
  cell at a time and see each cell's input and output; the agent can run and
  read the same notebook. Exercise 1 is done in it.

## Before you start

Open a terminal in the workshop folder (the one with `opencode.json`). The
commands below are the only ones in this exercise; after that you work in
OpenCode.

# Exercise 0a — Look before you install

**Do:** skim the README of each plugin, and the two files OpenCode runs,
`tui.tsx` (what you see) and `server.ts` (what the agent gets):

- [opencode-sidebar-plus at v0.3.2](https://github.com/dskanakoglou/opencode-sidebar-plus/tree/v0.3.2)
- [opencode-notebook at v0.1.9](https://github.com/dskanakoglou/opencode-notebook/tree/v0.1.9)

**Why:** ask of every plugin what it reads and what it adds to OpenCode. The
notebook plugin, for example, gives the agent a tool that runs Python, and
its README says plainly that this tool does not ask before it runs.

# Exercise 0b — Install both

**Do:** clone each one into this project's plugin folder - `.opencode/plugins/`:

```bash
git -c advice.detachedHead=false clone -q --depth 1 --branch v0.3.2 https://github.com/dskanakoglou/opencode-sidebar-plus .opencode/plugins/opencode-sidebar-plus
git -c advice.detachedHead=false clone -q --depth 1 --branch v0.1.9 https://github.com/dskanakoglou/opencode-notebook .opencode/plugins/opencode-notebook
```

No Git? Download the ZIP of
[opencode-sidebar-plus](https://github.com/dskanakoglou/opencode-sidebar-plus/archive/refs/tags/v0.3.2.zip)
and of [opencode-notebook](https://github.com/dskanakoglou/opencode-notebook/archive/refs/tags/v0.1.9.zip),
unzip them, and move the folders to `.opencode/plugins/opencode-sidebar-plus` and
`.opencode/plugins/opencode-notebook`.

**Why:** OpenCode runs whatever it finds in `.opencode/plugins/` when it
starts: a plugin is just a folder of code. `--branch` pins the version, so
what you looked at is what runs, even if the author changes the plugin later.

# Exercise 0c — Add the workshop key

**Do:** at a workshop, the organisers give you a key; otherwise, get your
own first (see *Not at a workshop?* below). Put it in a file in the workshop
folder, replacing `PASTE-THE-KEY-HERE`:

```bash
echo  PASTE-THE-KEY-HERE > .openrouter-key
```

**Why:** Exercises 1 and 5 call small models at
[OpenRouter](https://openrouter.ai) directly, outside OpenCode, and an API
key is how OpenRouter knows the call is allowed. Treat a key like a password:
it stays in this file, which Git ignores, and is never pasted into a chat,
because everything in a chat is sent to the model.

<details>
<summary><b>Not at a workshop? Get your own OpenRouter key</b></summary>

1. Make an account at [openrouter.ai](https://openrouter.ai).
2. Add credit on the [Credits](https://openrouter.ai/settings/credits) page.
   Both exercises use paid models (Mistral Nemo and the bge-base embedding
   model in Exercise 1, Llama 3.1 8B in Exercise 5), so the key needs a
   positive balance. They are cheap: all the runs we made while preparing
   this workshop cost less than one US cent together. OpenRouter adds a fee
   of 5.5% (at least $0.80) when you buy credit.
3. Create a key on the [Keys](https://openrouter.ai/settings/keys) page. Give
   it a name and a **credit limit**, for example $1, so a key that leaks
   cannot spend your whole balance. Copy the key when it is shown; it starts
   with `sk-or-v1-`.
4. Optional: in the [privacy settings](https://openrouter.ai/settings/privacy),
   choose whether your requests may go to providers that may train on your
   data.
5. Put the key in `.openrouter-key` with the command above. Or set it in your
   shell instead, `export OPENROUTER_API_KEY=sk-or-v1-…`; the exercises read
   either.

If a key ever leaks, delete it on the Keys page and create a new one.

</details>

# Exercise 0d — Check it worked

**Do:** quit OpenCode if it is running (`ctrl+c`), start it again in the
workshop folder, and send any message, for example "hello".

**Look for:**

- a sidebar on the right with the context window and the agent's activity.
  No sidebar? Widen the terminal or press `ctrl+x b`;
- `/notebook` in the list when you type `/` in the chat.

Then run `scripts/check-setup.sh --module 01-rag` in the terminal: it says
whether the key works.

**Why:** plugins load only when OpenCode starts, which is why you restart.

## What to notice

- A plugin is code you run with your own permissions. Read it, pin it, and
  know how to remove it.
- The plugins are installed for this project only. To remove one, delete its
  folder and restart OpenCode:

  ```bash
  rm -rf .opencode/plugins/opencode-sidebar-plus
  ```

**Discuss with your neighbour:** which of the two plugins could do more harm
if its author turned hostile, and why?

Next: [Exercise 1 — RAG](../01-rag/README.md).
