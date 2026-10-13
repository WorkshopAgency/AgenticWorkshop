# The full-day workshop (25 September 2026)

This folder keeps the exercises as they were run at the full-day DTU workshop
on 25 September 2026. The 2.5-hour conference edition (the rest of this
repository) trimmed and changed them; these are the originals, for reference
and for anyone who wants the longer versions after the workshop.

| Material | What it covers |
|---|---|
| [Full-day README](README-fullday.md) | Setup, models, context and HALp as written for the full day |
| [1 · Skills (1a–1f)](exercises/01-skills/README.md) | Includes 1b (download a structure image), 1c (copy a skill) and 1d (render from coordinates), cut from the conference edition |
| [2 · Agents (2a–2c)](exercises/02-agents/README.md) | Includes building your own swarm for penguins, proteins or your own data |
| [3 · MCP (3a–3i)](exercises/03-mcp/README.md) | All nine parts and the three bring-your-own datasets |
| [4 · Share what you built](exercises/04-share/README.md) | Publish through a fork and pull request, with a Git-scoped agent |
| [5 · Bonus](exercises/05-bonus/README.md) | Vet a plugin; find the bugs in a short BED script |
| [Original agents](agents/) | `bad-agent`, `good-agent` and the five `genome-*` agents as they were. Kept outside `.opencode/`, so OpenCode does not load them |

## Changes from the original

The text is as it was, except:

- **Links** point to the archived copies where they exist, and otherwise to
  the current repository (shared data, MCP notes, HALp).
- **Exercise 3:** the database is now `workshop.duckdb` (it was `pdb.duckdb`),
  because `exercises/03-mcp/scripts/make_db.py` builds one database for both
  editions. The server download is 30 MB, not 20 MB.
- **Exercise 3h, penguins:** the original said "eleven more" penguins have no
  recorded `sex`. It is eleven in total: the two without measurements plus
  nine measured ones (recomputed 13 October 2026).
- **Team folders removed.** The `team-01` … `team-10` working and submission
  folders were empty templates and are gone. Where the text mentions
  `team-NN/`, create your own folder instead.
- **Models in 2c** have changed since: the analyst's `ling-3.0-flash-fin-free`
  no longer exists. The agents in [`agents/`](agents/) show the original
  models; the current ones are in `.opencode/agents/` and
  [admin/model-bakeoff.md](../admin/model-bakeoff.md).
- **Team 5's shared skill** ([pdb-viewer-builder](exercises/04-share/submissions/team-05/pdb-viewer-builder/SKILL.md)),
  submitted on the day through Exercise 4 (pull request #25), lives here with the rest of Exercise 4.
- Paths in commands that pointed at `exercises/04-share` and
  `exercises/05-bonus` now point here.

Back to the [conference edition](../README.md).
