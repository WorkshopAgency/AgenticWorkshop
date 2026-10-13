# Rehearsal log, 13 October 2026

OpenCode 2.0.16 on macOS (Apple Silicon). DTU models offline all day (503,
then no connection). Everything model-driven ran on OpenCode Zen free models.
Detailed evidence: [model-bakeoff.md](model-bakeoff.md),
[2a-rehearsal.md](2a-rehearsal.md), and the "For organisers" section of
[05-safety](../exercises/05-safety/README.md).

## Verified

| Module | What was run | Result |
|---|---|---|
| setup | `scripts/check-setup.sh`, shared and `--module 02-agents`/`03-mcp` | Correct ✅/❌/⚠️; caught the swarm's dead analyst model before it was replaced |
| 00-rag | `rag.py` and `decide.py` against a local mock server, 40 checks | All pass: chunking, BM25 and cosine search, fallback, exact prompt printing, citation warnings |
| 01-skills | Starter `csv-profile` script on penguins, proteins, a missing file, a wrong column | Correct counts (2 rows without measurements; 11 without `sex`, 9 of them measured); clean errors |
| 02-agents 2a | 28 runs on big-pickle with headless-browser click checks | Final good-agent: 8/8 pass all four click checks in 39–68 s; bad-agent 1/15 |
| 02-agents 2c | 72 bake-off runs (8 free models × 3 tasks × 3); 2 swarm runs | Models chosen and applied; swarm delegates correctly but needs a human for child approvals (see below) |
| 03-mcp | `make_db.py`; step 2 prompt on big-pickle via the DuckDB MCP | Agent hit `avg(VARCHAR)`, explained the `NA` text, used `TRY_CAST`: 43.92 mm over 342 |
| 03-mcp | Checkpoints recomputed in Python and DuckDB | 43.9 / 342; pooled −0.235; Adelie +0.391, Chinstrap +0.654, Gentoo +0.643 |
| 05-safety | ~50 runs, 4 free models, build vs safe-analyst | No model took the bait; build reaches the network and `grep` finds the key with no prompt; safe-analyst blocks those |
| sidebar | Vendored v0.2 in a clean copy of the branch, real TUI | Loads with no config entry; `/sidebar` shows the presets, Agents preset by default |
| slides | `slides/dkb2026.md` rendered with Marp 4.5.1 | 14 slides, no overflow |
| links | Every relative Markdown link in the branch | 0 broken |

## Found and fixed today

- The swarm analyst's model (`ling-3.0-flash-fin-free`) no longer exists; replaced from the bake-off.
- The full-day README said "eleven more" penguins have no `sex`; it is eleven in total, two of them the unmeasured ones.
- `opencode run` hangs at startup when stdin is open: use `< /dev/null`.
- `opencode run` ignores a **primary** agent's `model:` line (2a), so the README tells participants to select the model; subagents' `model:` lines are applied (2c).
- An open-ended "make a plot" in Exercise 3 spent 9 minutes looking for matplotlib, DuckDB for Python and R; the prompt now asks for a hand-written SVG.
- An unreachable DTU model hangs for minutes with no error; added to the runbook and HALp.

## Not yet verified

- **Anything on DTU models**: qwen36/qwen38 for skills and agents, mistral for RAG, the embed endpoint, logprobs passthrough for Exercise 4.
- **The 2c swarm end to end.** `--auto` does not reach child sessions; a scripted approval was (rightly) blocked. Needs one interactive run in the TUI, approving the specialists' shell commands, timed against the 23-minute slot.
- **Exercise 3 step 3** (the SVG plot) to completion: the run was cut off by a Zen 429.
- **HALp**: the 20-question evaluation in [halp-eval.md](halp-eval.md).
- **Zen rate limits for a room**: this laptop was rate-limited (429) after a day of tests. How the free tier limits 30 laptops on one network is unknown.
- Windows/WSL2, Linux, the Desktop app, and any OpenCode version other than 2.0.16.
- Load with 30 participants.
