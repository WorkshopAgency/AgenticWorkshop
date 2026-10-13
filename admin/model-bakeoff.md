# Model bake-off for the genome-team swarm

Picks models for the five-agent swarm (`genome-coordinator` plus auditor, analyst,
visualizer and reviewer). The swarm agent files are **not** changed. The
recommended assignment is at the end. **It was applied to the agent files on
13 October 2026** (dkb-2026 branch).

- **Date:** 13 October 2026, 10:30–11:23 CEST
- **OpenCode:** v2.0.16 (`/opt/homebrew/bin/opencode`), using the background service
- **Script:** `admin/model-bakeoff.py` (standard library only; one command; prints the table)
- **Raw data** (not in the repo): `results.jsonl`, one event stream per run, and the
  scratch copies, under the organiser's `--workdir`

## Models checked

| Source | Free chat models found |
|---|---|
| Live list, `https://opencode.ai/zen/v1/models` | big-pickle, ling-3.1-flash-free, **cat-jam-free** (new since the earlier list), mimo-v2.6-flash-free, nemotron-3.5-lightning-free, step-5-preview-free, longcat-2.5-preview-free, space-bunny-free |
| Excluded from the live list | muse-spark-1.2/1.3-contributor-free (contributor tier: trains on inputs); jev-1.13-free (not a chat model) |
| `opencode models` (local catalogue) | It also lists exo-free, ling-3.0-flash-fin-free and nemotron-3-ultra-free, which are **not** in the live list. ling-3.0-flash-fin-free (the analyst's current model) returned `400 Upstream request failed: Model is unavailable.` |
| DTU (`dtu/qwen36`, `qwen38`, `mistral`, `gptoss`) | Not run (offline). Each base URL timed out after 10 s with no HTTP response. |

In v2.0.16, `opencode models opencode` fails with "Unexpected positional argument".
Use plain `opencode models`.

## Method

- Every run used `opencode run --auto --format json --model <m> "<task>"` in a
  **fresh copy of the repo** (git-initialised, without `.git` history, `slides/`
  or `outputs/`). Each run had a 6-minute timeout. At most one run per model was
  in flight, and all eight models ran in parallel.
- The scratch `opencode.json` points the default, title and summary models at
  `opencode/big-pickle` instead of `dtu/gptoss` (see the findings).
- The script computes ground truth from the CSV before any run:

| Task | Prompt (abridged) | Pass criterion |
|---|---|---|
| T1 read and inspect | "How many rows and which organism groups are in `<file>`? Give counts per group." | 25,965 rows, plus each of the 8 group counts on that group's line |
| T2 compute | For `Complete Genome` assemblies only: n and median genome size in Mb per group, to 2 dp, computed by running code | All 8 n values exact and all 8 medians within 0.011 Mb or 0.5 % (e.g. bacteria 6745 / 3.88; fungi 69 / 23.03; vertebrate_mammalian 3 / 3060.04) |
| T3 write a file | Write `bakeoff_out/group_summary.csv` with exactly `group,n_assemblies,median_genes_per_mb,median_gc_percent` | The file is in the project, the header is exact, 8 rows, n exact, medians within 0.011 or 0.2 % |

- Per run, the script records: pass/fail, completed (no error event, no timeout,
  non-empty answer), wall time, tool calls, and failed or invalid tool calls
  (`tool_use` events with `status: error`). It also classifies API errors
  (403/404/429/unavailable/timeout).

## Results: 3 tasks × 3 repetitions per model (72 runs)

| Model | T1 | T2 | T3 | Overall | Median s (range) | Failed tool calls | API errors |
|---|---|---|---|---|---|---|---|
| opencode/big-pickle | 3/3 | 3/3 | 3/3 | **9/9** | 16 (13–323) | 0 / 46 | none |
| opencode/cat-jam-free | 3/3 | 3/3 | 3/3 | **9/9** | 8 (5–133) | 1 / 50 | none |
| opencode/space-bunny-free | 3/3 | 3/3 | 3/3 | **9/9** | 33 (8–91) | 0 / 99 | none |
| opencode/longcat-2.5-preview-free | 3/3 | 3/3 | 3/3 | **9/9** | 62 (40–111) | 0 / 60 | none |
| opencode/step-5-preview-free | 3/3 | 3/3 | 3/3 | **9/9** | 84 (25–269) | 0 / 68 | none |
| opencode/mimo-v2.6-flash-free | 3/3 | 3/3 | 3/3 | **9/9** | 97 (37–138) | 0 / 59 | none |
| opencode/ling-3.1-flash-free | 3/3 | 3/3 | 3/3 | **9/9** | 170 (95–303) | 1 / 59 | none |
| opencode/nemotron-3.5-lightning-free | 3/3 | 3/3 | **1/3** | 7/9 | 60 (27–84) | 3 / 98 | none |
| dtu/qwen36, qwen38, mistral, gptoss | – | – | – | not run (offline) | – | – | – |

All 72 runs completed with a non-empty answer. None timed out, and none returned
a 403, 404 or 429.

Failure details:

- **nemotron-3.5-lightning-free, T3 ×2:** The numbers were correct, but the CSV
  went to the wrong place. The model built an absolute path for `bakeoff_out/`
  in a parent directory of the project instead of in the project. `--auto`
  allowed this write outside the project. In the swarm, `external_directory` is
  denied, so this behaviour would show up as a blocked write.
- **Failed tool calls:** cat-jam-free called a non-existent tool `bash` once
  ("No tool named "bash" is currently available"). This is the broken-tool-name
  failure from the rehearsal. ling-3.1 once and nemotron 3 times used `read` on
  the `.gz` file ("Cannot read binary file"). Every failed call was followed by
  a successful retry.
- **Environment trap seen in most runs:** macOS `zcat` cannot open `.gz` files
  (it looks for `.Z`). Every model recovered with `gunzip -c` or Python, at the
  cost of one or two extra steps.
- **Speed:** Runs were slow at times. One big-pickle T1 took 323 s against a
  median of 16 s, and step-5 took 269 s on one T2. These runs were in parallel
  with other users of the free tier, so the times show variability, not
  capacity.

## End-to-end swarm run (two runs)

The recommended assignment was written into the **scratch copy's** agent files.
The command was:
`opencode run --auto --format json --agent genome-coordinator --model opencode/big-pickle "Run the genome-size team task with all four specialist subagents. Save the actual outputs in a new folder under outputs/genome-team/. Report failed or untested steps."`

**Result: the swarm did not complete. It was blocked at step 1 because `--auto`
does not reach subagent sessions.**

- **Coordinator (big-pickle):** It ran normally for about 45 s. It made 12 tool
  calls (`shell`, `read`) without errors and read the PROVENANCE file, the
  README and all five agent files. It created
  `outputs/genome-team/run-2026-10-13-genome-size/` and checked the input
  (25,965 rows, 9 columns). It then delegated with the **`subagent`** tool
  (input key `agent`, not `task`/`subagent_type`). The parent session had no
  pending permission requests at any time.
- **No 403 error.** "Free tier can only be used from within OpenCode" did not
  appear in this run or in any of the 72 task runs.
- **Child session:** `genome-auditor` started with its configured model,
  `step-5-preview-free`, as the session API shows. Its first `shell` call
  (`pwd`, `ls -la`, then `ls -la exercises/03-mcp/data/byo/`) raised **2
  permission requests** (`action: shell`). These stayed pending, unanswered,
  from 11:10:18 to 11:22:49 (12.5 min). Nothing changed during that time: no
  transport timeout fired, and the coordinator received no error. I interrupted
  the parent session at 11:22:49, which also marked the child as `interrupted`.
  Total wall time was 838 s.
- **Files produced:** none. The run directory exists but is empty. The analyst,
  visualizer and reviewer were never reached, so their models are untested in
  the swarm. They are tested only by the single-agent tasks above.
- **Not done:** I did not script answers to the pending approvals. Having the
  harness click "Allow" for child agents was blocked as unsafe in this session,
  so a full headless swarm run still needs an organiser decision (see "Not yet
  verified").
- **Second run, 11:25** (the script itself, `--swarm-only --blocked-after 60`):
  same result. The coordinator delegated to `genome-auditor` about 60 s in. The
  auditor's first `shell` request (`ls -la …/exercises/03-mcp/data/byo/`) was
  still pending after 60 s, so the script stopped the run as blocked. Wall time
  was 151 s, with no 403 and no output files.

What this means for the workshop: a student running the swarm interactively
must approve each specialist's shell and edit requests, as the coordinator
prompt already expects ("A paused child may need the student's approval").
Under `opencode run --auto`, the swarm stalls with no error message.

## Other findings relevant to the workshop

1. **An offline DTU model hangs; it does not fail.** `opencode run --model dtu/gptoss`
   produced no error event for 455 s. Its only events were three `step_start`
   events, the second about 6 min in, consistent with silent retrying. It ended
   only when I interrupted it. A role on an offline DTU model will therefore
   stall the swarm without an error message.
2. **The repo `opencode.json` sets the title and summary agents to `dtu/gptoss`.**
   In one probe with that config, the session title arrived about 5 min after
   the run finished. This is consistent with the title call waiting on DTU, but
   I did not confirm the cause. Compaction (the `summary` agent) would depend on
   DTU in the same way. I did not test that.
3. **`opencode run` takes the project directory from `$PWD`, not from the process
   working directory.** In a first smoke test launched from Python with
   `cwd=` only, one run wrote `bakeoff_out/` into the real repo. I deleted it.
   The script now sets `PWD` and aborts if a session reports a different
   directory. This matters for any organiser script that drives `opencode run`.
4. In v2.0.16, `GET /api/session?parentID=…` ignores the filter. The script
   filters on the `parentID` field itself.

## Recommended assignment

The swarm agent files were not edited. Apply the assignment by changing the
`model:` line in each file.

### All-Zen (recommended)

| Role | Model | Why |
|---|---|---|
| coordinator | `opencode/big-pickle` | 9/9, 0/46 failed tool calls, fastest median among the established models (16 s). In the swarm it made 12 tool calls cleanly and delegated correctly, with no 403. |
| auditor | `opencode/step-5-preview-free` | 9/9, 0/68 failed tool calls. It runs first, so if it misbehaves the problem shows early. |
| analyst | `opencode/mimo-v2.6-flash-free` | 9/9, 0/59 failed tool calls. It computed T2 and T3 correctly every time. |
| visualizer | `opencode/space-bunny-free` | 9/9, 0/99 failed tool calls, fast (33 s median). It wrote the T3 file correctly 3/3. |
| reviewer | `opencode/longcat-2.5-preview-free` | 9/9, 0/60 failed tool calls. It comes from a different family than the analyst (Meituan LongCat vs Xiaomi MiMo, inferred from the names). |

Five different models spread the free-tier load across five upstreams. No
contributor model is used.

Not chosen:

- **nemotron-3.5-lightning:** it wrote the T3 file outside the project 2 of 3
  times.
- **ling-3.1-flash:** correct, but the slowest (170 s median, up to 303 s).
- **cat-jam-free:** the fastest, but it made the broken-tool-name error once and
  its provider is undisclosed. It is the first spare for any role.

### Alternative with one DTU role (untested: DTU was offline)

Same as above, but with **auditor = `dtu/qwen38`**. It has the largest DTU
context window (32k) and the auditor's job is the lightest. Because the auditor
runs first, a DTU outage shows up before any other work. Finding 1 still
applies, though: an offline DTU model **hangs instead of failing**. Organisers
should check DTU with `curl -m 10 https://teaching.healthtech.dtu.dk/workshop/qwen38/models`
before the session and fall back to the all-Zen assignment if it does not
respond.

### Caveats on this choice

- Families come from the model names. big-pickle, space-bunny and cat-jam are
  undisclosed models, so their family and data-retention policy are **not
  verified**.
- Three of the five are `preview` models. ling-3.0 disappeared between the
  rehearsal and today, and others may follow. Re-run the script the day before.

## Not yet verified

- **The full swarm, end to end.** The analyst, visualizer and reviewer never ran
  in the swarm, and no `report.md`, `plots.html`, `review.md` or `agent-run.md`
  was produced. This needs either an interactive TUI run where someone approves
  the child requests, or an organiser decision to let a harness approve them in
  a scratch copy.
- **Whether child approval prompts appear to a student in the TUI or `mini`
  interface.**
- **DTU models** (`qwen36`, `qwen38`, `mistral`, `gptoss`): offline, not run.
- **Behaviour with 30 concurrent users.** This test had at most 8 concurrent
  runs, one per model, plus other unrelated sessions on the same machine. It saw
  no 429s, but that says nothing about 30 students × 5 agents on one IP or
  account.
- **Plot quality.** No task checks the visualizer's HTML/SVG. T3 only shows that
  it writes a correct file at a given path.
- **Whether the `dtu/gptoss` title/summary setting slows or breaks long
  sessions when DTU is down.**

## Re-running

```bash
python3 admin/model-bakeoff.py                 # 8 Zen models x 3 tasks x 3 reps, then the swarm
python3 admin/model-bakeoff.py --no-swarm      # table only (about 25 min)
python3 admin/model-bakeoff.py --swarm-only --analyst opencode/cat-jam-free   # try another assignment
python3 admin/model-bakeoff.py --models opencode/big-pickle dtu/qwen38 --reps 1
```

The script skips any DTU model whose base URL does not answer within 10 s
("not run (offline)"). It also skips Zen models missing from the live list and
contributor/jev models. The swarm is stopped and reported as blocked once
subagent approvals have been pending for `--blocked-after` seconds (default 300).
The script never answers approvals itself. Scratch copies and logs go to
`$TMPDIR/opencode-bakeoff-<timestamp>/` unless `--workdir` is given. The workdir
must be outside the repo.
