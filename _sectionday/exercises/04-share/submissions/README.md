# Submissions

One folder per person. Put yours here:

```text
submissions/
   your-name/
      README.md          what it is, how to try it, what you tested
      SKILL.md           if you are sharing a skill
      my-agent.md        if you are sharing an agent
      mcp-notes.md       if you are sharing an MCP server block
```

Use your name or GitHub handle, lowercase with hyphens. Add only your own
folder. Do not edit anyone else's, and do not change files elsewhere in the
repository as part of submitting — that is what turns a one-file pull request
into a merge conflict for everyone.

For Exercise 2c team work, use the prepared `team-01` through `team-10` folders
instead of a person's name. Share reviewed copies with team-prefixed filenames
and a short explanation of the goal, models and entry-point coordinator.
Working definitions stay in `exercises/02-agents/team-<number>/`; the folder here
is the reviewed snapshot. The submit-agent's allowed publishing location does
not change. See [Exercise 2c](../../02-agents/README.md#team-folders-and-handoff)
for downloading and activating a team's agents.

## Do not name your folder any of these

The repository's `.gitignore` excludes these names anywhere in the tree, so a
submission inside one of them is silently dropped. There is no error, no
warning, and `git status` shows nothing:

```text
build   dist   lib   var   target   venv   env   downloads   sdist   wheels   eggs
```

Before you commit, check that your files are really going to ship:

```bash
git check-ignore -v _sectionday/exercises/04-share/submissions/your-name/*
```

No output is what you want. Any output names a file that will not be
committed. Rename your folder rather than editing the shared `.gitignore`.

## What not to put here

No credentials, tokens or API keys. No datasets, databases or downloaded
files. No `node_modules`, caches or build products. A submission should be a
few kilobytes of text that someone else can read and try.
