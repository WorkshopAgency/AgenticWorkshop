---
marp: true
theme: dtu
paginate: true
---

<!-- _class: lead workshop-cover -->
<!-- _paginate: false -->

# UAAA - Agentic Workshop

## For data analysis

<div class="presenters">Dimitrios S. Kanakoglou &amp; Peter Wad Sackett<br>With HALp, our workshop helper</div>

<div class="workshop-date">25 September 2026 · DTU Health Tech</div>

<div class="acknowledgements">Thank you to <strong>Anders Gorm Pedersen, Ole Lund<br>and Kristoffer Vitting-Seerup</strong><br>for facilitating the workshop and contributing ideas<br>during the initial brainstorming.</div>

---

# Models and harnesses

The **model** generates responses and proposes actions from the information
available in its context.

The **harness** manages that context, applies permissions, executes tool calls
and returns their results to the model.

Today, OpenCode is our harness. You can change the model while keeping
the same project and tools.

Model inference may happen at DTU or another provider.
Project commands run on your laptop unless you explicitly configure otherwise.

<!-- Sources: https://opencode.ai/v2/docs/ and https://opencode.ai/v2/docs/providers/ -->

---

# Why OpenCode?

- Compare local, free and paid models within the same project.
- Inspect and share skills and agent definitions as ordinary files.
- Connect scientific tools through MCP.
- Review proposed actions, set permissions and inspect tool results.

The aim is to learn an architecture you can reuse across tools and research
projects, without depending on one model provider.

<!-- Sources: https://opencode.ai/v2/docs/agents/ https://opencode.ai/v2/docs/providers/ https://opencode.ai/v2/docs/permissions/ -->

---

# Skills and agents

An **agent** uses a model and tools to pursue a goal over multiple steps.
In OpenCode, we configure its role, instructions, model and permissions.

A **skill** packages reusable instructions, with optional scripts or resources,
for a particular task. An agent can load it when needed.

For example, a structure-analysis agent could use a PDB-download skill.

OpenCode reads skills from `.opencode/skills/<name>/SKILL.md`
and agents from `.opencode/agents/<name>.md`.

A coordinator can delegate bounded jobs to specialist agents and combine
their results. Permissions determine what each agent may do.

<!-- Sources: https://opencode.ai/v2/docs/skills/ and https://opencode.ai/v2/docs/agents/ -->

---

# MCP servers and plugins

**MCP** is a protocol for discovering and accessing tools, resources and
prompts exposed by servers. Our DuckDB server exposes database tools.

A **plugin** is code that extends OpenCode itself, for example by responding
to events or adding a notification when work finishes.

Enable only the MCP servers you need. Inspect plugins before installing
them: they execute code, and their API must match your OpenCode version.

<!-- Sources: https://opencode.ai/v2/docs/mcp-servers/ and https://opencode.ai/v2/docs/plugins/ -->

---

# MCP (Model Context Protocol)

![width:1040](assets/mcp-overview.png)

[OpenCode MCP server documentation](https://opencode.ai/v2/docs/mcp-servers/)

<!-- Diagram supplied by https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro. Examples illustrate the architecture, not a verified compatibility list. Configuration: https://opencode.ai/v2/docs/mcp-servers/ -->

---

# Free, paid and DTU models

| Choice | What you need to know |
|---|---|
| **OpenCode free models** | No model payment for the current free offers. Availability and limits can change. Requests leave DTU(!) |
| **Paid models** | Connect a supported subscription or API account. Check what it includes and how usage is billed. |
| **Four DTU models** | Workshop-hosted GPT-OSS, Mistral and two Qwens. Shared GPU capacity and context limits apply. |

Choose a model with `/models`. 

A chat subscription does not necessarily include API access. 

We use public datasets throughout this workshop.

<!-- Sources: workshop README and opencode.json; https://opencode.ai/v2/docs/providers/ -->

---

# Three lessons before we start

1. **You are in charge of your data.** Check the provider and the
   permissions you approve. Use public data with external models.

2. **`/compact` is your friend.** Summarise a long conversation to make
   room. Keep important decisions in files because summaries lose detail.

3. **`/theme` helps you look cool in front of your PI.** Choose a theme
   you enjoy working with. Try it before starting the exercises.

<!-- Lessons from the workshop README. Compaction: https://opencode.ai/v2/docs/compaction/ -->

---

# HALp: the workshop helper

<pre style="position:absolute;right:64px;top:40px;font-size:22px;line-height:1.15;background:none;border:0;padding:0;"> [o_o]  &lt;{ let's look }
 /|_|\
  / \</pre>

Start a **fresh chat**, then type `/halp` and your question:

```text
/halp I am on Exercise 1c. Where should I copy my skill?
/halp Why can I not see the workshop agents?
```

HALp reads the exercise instructions and offers hints or setup help.
It can help adjust context settings with your approval.

HALp initially uses a **free external model**. Share only public information
and redacted errors. Afterwards, select your exercise agent and model again.

If HALp gets stuck too, call a human :D

---

# Exercise 1: skills

Turn a repeated task into a reusable, testable skill.

1. Follow the PDB examples, then copy and improve a skill.
2. Use `skill-builder` to help create your own.
3. Test it on a new input and a deliberately invalid one.

**Tip:** Specify expected outputs and failure behaviour, not just the happy path.

`exercises/01-skills/README.md`

---

# Exercise 2: agents and coordination

Compare agent designs, then divide a larger task into specialist roles.

1. Give the basic and detailed agents the same request.
2. Build and test an agent for a well-defined task.
3. Try the coordinator and specialists, then adapt the team to your question.

**Tip:** Give each specialist a clear input, expected output and permission boundary.

`exercises/02-agents/README.md`

---

# Exercise 3: MCPs and data analysis

Give an agent access to structured data through DuckDB.

1. Build the supplied database and enable the DuckDB MCP server.
2. Work through the questions and verification steps.
3. Extend the analysis to a supplied alternative dataset or your own public data.

**Tip:** Ask for the SQL and independently check a small result.

`exercises/03-mcp/README.md`

---

# Exercise 4: sharing

Make your work usable by someone outside your team.

1. Choose a skill or agent to share and review everything it contains.
2. Follow the submission instructions and document how to use it.
3. Try another team's contribution in your own project.

**Tip:** Remove private data and credentials. Test the shared copy, not only your original.

`_sectionday/exercises/04-share/README.md`

---

# Bonus: plugins and debugging

Explore how extensions and independent checks change an agent's workflow.

1. Inspect a plugin and check its compatibility before installing it.
2. Review the supplied buggy script with an agent.
3. Compare its findings with deterministic checks and known-answer tests.

**Tip:** A plausible explanation is a starting point. Reproduce the bug.

`_sectionday/exercises/05-bonus/README.md`

---

<!-- _class: lead workshop-thanks -->

# Thank you, everyone!

Thank you for your curiosity, questions and contributions today.

We hope you leave with something useful for your own research.

Dimitrios, Peter & HALp

[Workshop repository](https://github.com/peterwadsackett/AgenticWorkshop)<br>
[Further reading and projects: additional.md](https://github.com/peterwadsackett/AgenticWorkshop/blob/main/additional.md)
