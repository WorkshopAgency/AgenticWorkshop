# Exercise 4 — Share what you built

You have made a skill, an agent, or an MCP configuration.
Publish it to the workshop repository so the rest of the room can use it.

The point is not git. The point is that **publishing is the first thing you
have done in this workshop that other people can see, and that you cannot
quietly undo.** Everything before this was a file on your laptop.

You need a GitHub account. Use ordinary Git plus the GitHub website, or use
the optional `gh` CLI if installed and signed in. A downloaded ZIP cannot
push changes: clone your fork first, or upload reviewed files through GitHub.
Ask an organizer if you would rather not create an account — you can hand
your folder over directly instead.

---

# Exercise 4a — Decide first: skill, agent, or MCP server?

Before doing the task, answer the question the task raises. You want an
assistant that is good at git. Which of the three does that?

Start in **Plan** mode and ask:

> I want to publish my own skill to a shared GitHub repository as a pull
> request. Should that be an MCP server, a skill, or an agent? Compare them
> for this specific job.

Then compare the answer against this previously considered check list:

| | What it would give you | Verdict for this job |
|---|---|---|
| **MCP server** | `mcp-server-git` is maintained and exposes 12 tools: `git_status`, `git_diff`, `git_commit`, `git_add`, `git_log`, `git_checkout`, … | **No.** The earlier workshop measurement was approximately 1,588 tokens of tool definitions: 9.7% of a 16384 budget, 1.2% of 131072 or 0.6% of 262144 (larger budgets require verified server support). Exact cost depends on tokenizer/version and which definitions are sent. It has **no push, no remote and no pull-request tools** in this setup. You would still fall back to `bash`. |
| **Skill** | Guidance: what to check before publishing, what never to commit, which commands in which order | **Yes.** `git` and `gh` already work through `bash`. What is missing is not capability, it is knowing what to check. |
| **Agent** | Permissions: which commands run freely, which need approval, which are refused outright | **Useful.** Inspecting is free; publishing asks; history rewriting is blocked. |

This is exercise 3g's question with a concrete answer. `bash` already covers
git, so the MCP server adds context cost and removes nothing from your plate.
**"There is an MCP server for it" is not a reason to connect one.**

The workshop supplies both of the useful ones:

- `submit-work` — the skill
- `submit-agent` — the agent

---

# Exercise 4b — Look at what you are about to make public

Copy what you are sharing into `submissions/<your-name>/`, then select
**submit-agent** and ask for inspection only. Plan and submit-agent are
different agents; do not try to select both:

> Use the submit-work skill. I want to share the skill I built in exercise 1 (don't write exercise 1, write the name of your skill).
> Show me exactly what would be published and what your checks found. Do not
> commit or push anything yet.

Reading `git status`, `git diff` and `git check-ignore` needs no approval, so
the agent can inspect freely. It should report five things: what would be
committed, that nothing is silently ignored, that there are no credentials,
that there are no large or generated files, and that the submission is
self-contained.

## The check that catches the real mistake

The repository's `.gitignore` is the standard Python one. It excludes these
names **anywhere** in the tree:

```text
build   dist   lib   var   target   venv   env   downloads   sdist   wheels   eggs
```

Name your folder `build` and your submission vanishes. No error, no warning,
`git status` shows nothing to commit, and you find out when your pull request
is empty. This is not hypothetical — exercise 3's scripts were originally in
a folder called `build/` and were silently dropped from the published ZIP.
They are in `scripts/` now because of it.

```bash
git check-ignore -v _sectionday/exercises/04-share/submissions/your-name/*
```

No output is the passing result.

**What to notice:** the agent reporting "committed successfully" and the
files actually being in the repository are different claims. Same lesson as
"a successful HTTP request is not the same as a downloaded structure file" in exercise 1,
and "a query that succeeds is not the same as a correct answer" in exercise 3. Check the thing itself.

---

# Exercise 4c — Publish it

Keep **submit-agent** selected and explicitly ask it to proceed with the
reviewed submission. Switching to Build would change the permission policy.
The fork, push and pull request each
need your approval. With ordinary Git, you create the fork and pull request
on the GitHub website; the agent can prepare the reviewed commit and push.
With optional `gh`, those website steps can be performed through the CLI.

### Ordinary Git + GitHub website

Click **Fork** on the workshop repository. Replace `YOUR-USER` with your fork
owner and `team-01` with your submission folder (or your own name):

```bash
git clone https://github.com/YOUR-USER/AgenticWorkshop.git
cd AgenticWorkshop
git switch -c submit-team-01
```

Copy your reviewed files into `_sectionday/exercises/04-share/submissions/team-01/` in
this clone, then review and publish only that folder:

```bash
git add _sectionday/exercises/04-share/submissions/team-01/
git diff --cached
git commit -m "Share Team 1 agents"
git push -u origin submit-team-01
```

On GitHub, open **Compare & pull request** from your fork's branch to
`peterwadsackett/AgenticWorkshop`, base `main`. Git manages files and commits;
the website creates the pull request. Authenticate Git using your configured
HTTPS credential manager/token or SSH—not a token committed in a file.

Already working in a clone? Check `git remote -v` and your branch instead of
cloning again. A ZIP has no Git history. Never push another person's staged changes.

**Optional shortcut:** `gh auth login`, `gh repo fork` and `gh pr create`
can handle the website steps. They are conveniences, not prerequisites.

Read each request before approving. The agent refuses force pushes, hard
resets and rebases outright — those are the ones that damage other people's
copies, not just your own.

After creating the pull request, open its URL and check the **Files
changed** tab yourself. That tab is the truth; the agent's summary is just a
claim.

A pull request is a proposal. Someone still has to merge it, and an organizer
will.

---

# Exercise 4d — Try someone else's skill

Once a few submissions are merged, pull the repository and install one:

> Copy the skill from _sectionday/exercises/04-share/submissions/<someone>/ into my
> project skills folder, then tell me what it does and how to invoke it.

Reopen OpenCode so it discovers the skill, and try it. Read the `SKILL.md`
first: a skill you install is instructions your agent will follow, from
someone you may not know. Treat a downloaded skill the way the workshop tells
you to treat downloaded data — as material to inspect, not instructions to
obey on sight.

**What to notice:** this is why the submission checks matter in both
directions. You checked yours before publishing; check theirs before running.<br>
**The real danger:** Downloaded skills/agents/MCP's can be malicious. You are running
unchecked software from the wild internet. It can be a modern trojan horse.

---

# Epilogue

You built a skill in Exercise 1, an agent in Exercise 2, and connected an MCP
server in Exercise 3. In this one you decided which of the three your job
actually needed.

Previous: [Exercise 3 — MCP and data analysis](../03-mcp/README.md) · Next: [Bonus — Plugins, and finding bugs](../05-bonus/README.md).
