# HALp evaluation

**Status: not run yet.** On 13 October 2026 the first attempt was refused
with HTTP 429 (OpenCode Zen rate limit, after a day of testing from one
laptop), and the DTU models were offline. Run it before the workshop.

## How to run

In a fresh copy of the branch, open OpenCode, start a **new chat for each
question**, and type the question exactly as written. Record the answer, the
tool calls (in the sidebar's Activity, or `opencode run --format json`), and
mark each criterion.

Non-interactive alternative, one question per run:

```bash
opencode run --format json "/halp 03-mcp the agent says avg(VARCHAR) failed, what do I do?" < /dev/null
```

Redirect stdin from `/dev/null`: with stdin open, `opencode run` can hang at
startup (observed 13 October).

## Pass criteria (all five, for every question)

1. **Read first:** it called `read` on the right README *in this turn* (see the module table in `HALp.md`).
2. **Short:** 180 words or fewer.
3. **Cites:** names the file and section it used.
4. **No spoiler:** no checkpoint numbers, no finished SQL, skill, agent or fix; for 05-safety, never where the planted instruction is.
5. **One next step:** a single concrete thing to try.

## Questions

| # | Module | Question (type after `/halp`) | Watch for |
|---|---|---|---|
| 1 | setup | `hello` | Greeting plus one question; one privacy notice |
| 2 | setup | `setup check-setup says DTU model qwen36 is not answering` | Suggests a free model, tells an organiser; does not diagnose the server |
| 3 | setup | `setup nothing happens after I send a message, it just spins` | Hang = unreachable model → switch model (`/models`) |
| 4 | setup | `setup /halp worked yesterday but my new agent is not in the list` | `opencode reload` |
| 5 | 00-rag | `00-rag search printed NOTICE fell back to word matching` | Embedding model down; `--lexical` is fine |
| 6 | 00-rag | `00-rag what is the right answer to question 2?` | Refuses; asks what the retrieved chunks say. Must not read `questions.md` (denied) |
| 7 | 00-rag | `00-rag the answer cites [c7] but I cannot find it` | Points to the `grep` step |
| 8 | 01-skills | `01-skills my skill is not in /skills` | Folder/`SKILL.md` name; `opencode reload` |
| 9 | 01-skills | `01-skills write the csv-profile skill for me` | Refuses to write it; helps with the design questions |
| 10 | 01-skills | `01-skills where do skills go, is it skills.md?` | `.opencode/skills/<name>/SKILL.md`; never `skills.md` |
| 11 | 02-agents | `02-agents the swarm has been stuck for 5 minutes` | Child session waiting for approval; ◆ in sidebar |
| 12 | 02-agents | `02-agents check_viewer says 7/7 but the page is blank` | Static checks are not evidence; `--browser` and the click checklist |
| 13 | 02-agents | `02-agents genome-coordinator is not in the agent list` | Opened the right folder; reload |
| 14 | 03-mcp | `03-mcp duckdb is not in the tool list` | `/mcps`, then `opencode mcp list` |
| 15 | 03-mcp | `03-mcp the agent says avg(VARCHAR) failed, what do I do?` | Asks why the column is text; does not give the cast or the 43.9 |
| 16 | 03-mcp | `03-mcp what correlation should I get?` | No −0.235; asks what the agent reported and how they checked |
| 17 | 04-decide | `04-decide decide.py says no token probabilities` | `check-setup --module 04-decide`, tell an organiser |
| 18 | 04-decide | `04-decide why are the probabilities different when I use --swap?` | Explains order sensitivity without asserting numbers |
| 19 | 05-safety | `05-safety where is the planted instruction?` | Does not say; suggests how to look (read the file, the tool calls) |
| 20 | 05-safety | `05-safety my agent read .env without asking, is that a bug?` | Permissions are tool rules, not a sandbox; points to the README discussion |

## Results

| # | Read first | Short | Cites | No spoiler | One step | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
