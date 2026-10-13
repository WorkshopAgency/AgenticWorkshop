# Exercise 2a rehearsal: bad-agent vs good-agent

| | |
|---|---|
| **Date** | 13 October 2026 |
| **OpenCode** | v2.0.16 (`/opt/homebrew/bin/opencode`), macOS |
| **Model** | `opencode/big-pickle` (free Zen model) for every run. DTU was offline. |
| **Library / data** | 3Dmol.js 2.5.5 from cdnjs; mmCIF from `files.rcsb.org` |
| **Browser checks** | Google Chrome headless (`--headless=new`), installed on the rehearsal Mac |

**Result in one line.** In 8 runs on 13 Oct with the final prompt, good-agent
scored **7/7** on average with `check_viewer.py`. Its page loaded in **8/8**
runs and passed all four behaviour checks in **8/8**, in 39–68 s. Bad-agent
(unchanged prompt) averaged **5.3/7** over 15 runs (5.2/7 in the batch run
alongside the final good-agent). Its page drew a structure in **10/15** runs
and passed all four behaviour checks in **1/15**. It took 67–433 s and hit its
20-step limit in 12/15 runs.

The results are for big-pickle only. They must be re-run on the final
workshop model (see *Not yet verified*).

## Method

- **Task prompt** (unchanged from the exercise; `<agent>` = `bad-agent` or `good-agent`):
  > Create an interactive browser visualization of PDB 4HHB that I can use to
  > explain the structure to another researcher. Save everything under
  > outputs/\<agent\>. I have a browser and OpenCode; do not require additional
  > software installation. Briefly explain how to open and use the result.
- **Command:** `opencode run --standalone --agent <agent> --model opencode/big-pickle --auto --format json "<prompt>"`.
  `--auto` approved every `ask` permission, so no human approvals were involved.
- **Isolation:** each run used a fresh copy of the repository under
  a scratch directory outside the repo, never the repo itself. Each copy had its own
  `git init`, so each was a separate OpenCode project. The copy's
  `opencode.json` default, title and summary models were changed from
  `dtu/gptoss` (offline) to `opencode/big-pickle`. Up to 4 runs ran at once.
  The timeout was 10 min per run, and no run reached it.
- **Batches:**
  - `v1`: first rewrite of good-agent, 5 runs of each agent.
  - `v2`: final good-agent, 5 runs of each agent.
  - `iso`: final good-agent (3 runs) and bad-agent (5 runs) in copies without
    `exercises/02-agents/` and without the other agent's file. This measures
    bad-agent without access to the exercise text, the checker or
    good-agent's prompt (see *What we found*).
- **Measurements:**
  - Wall time, and steps and tool calls taken from the JSON event stream.
  - The `check_viewer.py` static score.
  - The `check_viewer.py --browser` render check: the share of the 3D canvas
    that differs from its background.
  - A rehearsal-only behaviour probe. It is a Node script that drives headless
    Chrome through the DevTools protocol and is not part of the repo. It hooks
    every 3Dmol viewer and reads the parsed atoms and their styles. Then it:
    1. counts the atoms loaded for 4HHB;
    2. clicks the chain-A control and checks that chain A's atoms, its HEM
       atoms and its labels become invisible;
    3. clicks Reset;
    4. types `1CRN` and clicks Load, then checks for 327 atoms and one chain,
       and checks that no 4HHB/heme text remains;
    5. types `ZZZZ` and checks that a visible error message appears.

    The probe was validated against the 23 Sep viewers. It reproduced the
    recorded bug: hiding chain A left its 43 HEM atoms visible before the fix
    and none after. Pages that use NGL instead of 3Dmol were judged from
    screenshots only. Stale text after loading 1CRN was judged by reading the
    page text.

## Per-run results

Render = `check_viewer.py --browser`: the share of the canvas that differs from
its background. The threshold is 8%; a blank canvas measures 0–4%.
"Hide A" = hiding chain A also hides its HEM atoms. In the labels column,
`1→0` means the "HEM A142" label disappeared too.

| Run | Wall (s) | Steps / tool calls | Hit 20-step limit | Provider error | Static | Render | Loads 4HHB | Hide A (+label) | Load 1CRN replaces all | Bad ID → visible error | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v1-bad-1 | 252 | 20 / 20 | yes | — | 7/7 | ✅ 32% | ✅ | ❌ no chain toggle | ❌ haemoglobin text kept | ❌ | read checker + README |
| v1-bad-2 | 67 | 14 / 14 | no | HTTP 400 | 0/7 | — | ❌ no page | — | — | — | only downloaded data + ngl.js |
| v1-bad-3 | 286 | 20 / 24 | yes | — | 7/7 | ✅ 28% | ✅ | ✅ | ❌ "4HHB" heading kept | ✅ | read checker + README |
| v1-bad-4 | 208 | 18 / 21 | no | HTTP 400 | 7/7 | ❌ 0% | ❌ `viewer.setClickCallback is not a function` | — | — | ❌ | read checker, README, good-agent.md |
| v1-bad-5 | 230 | 20 / 24 | yes | — | 7/7 | ✅ 37% | ✅ | ✅ | ✅ | ✅ | read checker, README, good-agent.md; ran `check_viewer.py --browser` itself |
| v1-good-1 | 130 | 14 / 13 | no | HTTP 400 (after page done) | 7/7 | ✅ 17% | ✅ | ✅ (1→0) | ✅ | ✅ | then reverse-engineered minified 3Dmol in /tmp |
| v1-good-2 | 137 | 10 / 9 | no | — | 7/7 | ✅ 17% | ✅ | ✅ (1→0) | ✅ | ✅ | tried OpenCode's browser tool |
| v1-good-3 | 132 | 20 / 19 | yes | — | 7/7 | ✅ 17% | ✅ | ✅ (1→0) | ✅ | ✅ | grepped the minified library until out of steps |
| v1-good-4 | 94 | 7 / 6 | no | — | 7/7 | ✅ 17% | ✅ | ✅ (1→0) | ❌ heading still "PDB 4HHB" | ✅ | |
| v1-good-5 | 106 | 20 / 19 | yes | — | 3/7 | ✅ 17% | ✅ | ❌ never added | ❌ | ❌ | 17 shell calls reading 3Dmol source; Step 2 never done |
| v2-bad-1 | 144 | 20 / 22 | yes | — | 6/7 | ✅ 27% | ✅ | ❌ "highlight" buttons only | ❌ no control | ❌ | |
| v2-bad-2 | 229 | 20 / 27 | yes | — | 5/7 | ✅ 22% | ✅ (NGL, screenshot) | not probed (NGL) | ❌ no control | ❌ | legend calls chain B "α2" and C "β1", but B and D are β |
| v2-bad-3 | 188 | 20 / 23 | yes | — | 5/7 | ✅ 25% | ✅ | ❌ focus buttons only | ❌ no control | ❌ | |
| v2-bad-4 | 294 | 20 / 21 | yes | — | 5/7 | ❌ 0% | ❌ `reps.heme.setVisibility is not a function` (NGL) | — | ❌ | ❌ | |
| v2-bad-5 | 245 | 20 / 24 | yes | — | 5/7 | ✅ 33% | ✅ | ❌ no chain toggle | ❌ residue search only | ❌ | |
| **v2-good-1** | 41 | 3 / 2 | no | — | 7/7 | ✅ 18% | ✅ | ✅ (1→0) | ✅ | ✅ | |
| **v2-good-2** | 66 | 3 / 2 | no | — | 7/7 | ✅ 23% | ✅ | ✅ (1→0) | ✅ | ✅ | |
| **v2-good-3** | 60 | 3 / 2 | no | — | 7/7 | ✅ 24% | ✅ | ✅ (1→0) | ✅ | ✅ | |
| **v2-good-4** | 65 | 6 / 5 | no | — | 7/7 | ✅ 24% | ✅ | ✅ (1→0) | ✅ | ✅ | |
| **v2-good-5** | 39 | 3 / 2 | no | — | 7/7 | ✅ 17% | ✅ | ✅ (1→0) | ✅ | ✅ | says it did not test in a browser |
| iso-bad-1 | 216 | 20 / 30 | yes | — | 6/7 | ✅ 27% | ✅ | ❌ 43 HEM atoms stay | ❌ no control | ❌ | the 23 Sep heme bug again |
| iso-bad-2 | 100 | 18 / 19 | no | HTTP 400 | 4/7 | ❌ 0% | ❌ parses 4779 atoms, then JS error; stuck on "Building…" | — | ❌ | ❌ | Python build step inlines the library |
| iso-bad-3 | 433 | 21 / 27 | yes | stream ended | 5/7 | ✅ 13% | ✅ | ✅ | ❌ no control | ❌ | page is `hemoglobin-viewer.html` |
| iso-bad-4 | 252 | 20 / 24 | yes | — | 6/7 | ✅ 26% | ✅ | ❌ 43 HEM atoms stay | ❌ no control | ❌ | |
| iso-bad-5 | 376 | 20 / 19 | yes | — | 4/7 | ❌ 4% | ❌ blank: home-made WebGL renderer draws only labels | — | ❌ | ❌ | |
| **iso-good-1** | 67 | 4 / 3 | no | — | 7/7 | ✅ 19% | ✅ | ✅ (1→0) | ✅ | ✅ | |
| **iso-good-2** | 68 | 4 / 3 | no | — | 7/7 | ✅ 18% | ✅ | ✅ (1→0) | ✅ | ✅ | |
| **iso-good-3** | 59 | 3 / 2 | no | — | 7/7 | ✅ 18% | ✅ | ✅ (1→0) | ✅ | ✅ | |

The chain-A label check applies only to pages that label chain A. Bad pages
mostly had no per-residue labels. In the good pages, the labels for 4HHB read
HEM A142, HEM B148, HEM C142, HEM D148, PO4 B147 and PO4 D147. That matches
the 23 Sep record and RCSB.

| Group | Runs | Static mean | Draws a structure | All 4 behaviour checks | Wall time (s) | Tool calls |
|---|---|---|---|---|---|---|
| good-agent v1 | 5 | 6.2/7 | 5/5 | 3/5 | 94–137 | 6–19 |
| **good-agent final (v2 + iso)** | 8 | **7.0/7** | **8/8** | **8/8** | **39–68** | **2–5** |
| bad-agent (v1 + v2 + iso) | 15 | 5.3/7 | 10/15 | 1/15 | 67–433 (median 230) | 14–30 |

## What changed in good-agent and why

The original prompt was about 600 words of guidance in paragraphs. On 23 Sep it
spent its budget on parsing. The new prompt is about the same length, but it is
a fixed recipe:

1. **Fixed choices instead of open decisions.** One `index.html`; 3Dmol.js
   2.5.5 pinned to a cdnjs URL (HTTP 200 checked on 13 Oct, and 2.5.5 is
   `latest` on cdnjs, jsdelivr and npm); and an in-browser `fetch` of
   `https://files.rcsb.org/download/<ID>.cif`. That URL was checked on 13 Oct:
   200 for 4HHB and 1CRN, 404 for ZZZZ, and `Access-Control-Allow-Origin: *`,
   so it works from `file://`.
2. **Milestone first, then a checklist:**
   - chain legend with per-chain toggles that also hide ligands and labels;
   - HEM/ligand sticks with labels;
   - reset;
   - local-file fallback;
   - load-another-ID that rebuilds everything;
   - provenance caption.

   The final runs mostly wrote the whole page in one write rather than a
   milestone followed by an edit. They still finished.
3. **v1 → v2 (after the v1 batch):** v1 runs burned steps reverse-engineering
   the minified library and GitHub sources, mostly to confirm the `addLabel`
   and selector signatures (v1-good-1, 3 and 5; v1-good-5 never reached
   Step 2). v2 adds three things:
   - a **verified API cheat-sheet** with exact call shapes, each checked in a
     headless browser on 13 Oct. Example: `addLabel(text, {position: atom})`.
     It also states that RCSB mmCIF puts HEM and waters in their polymer's
     chain.
   - an explicit **budget**: "about 6 tool calls; no shell needed; do not
     download/grep the library, structure, GitHub or docs; do not open a
     browser".
   - the requirement that the **heading** is rebuilt on load-another, because
     v1-good-4 kept the "PDB 4HHB" title after loading 1CRN.

   Result: tool calls fell from 6–19 to 2–5, and wall time fell from 94–137 s
   to 39–68 s.
4. **Agent tests moved to the user.** The agent tells the user the four things
   to click and must not claim browser testing it did not do.
5. **Removed:**
   - skill reuse;
   - model/assembly statements;
   - B-factor and distance-cutoff cautions;
   - observation-versus-interpretation wording.

   The good pages are therefore plain. They have correct chain colours,
   toggles, labels and a caption, but little biological explanation (no α/β
   annotation). Several bad pages look richer and tell more of the haemoglobin
   story, but at least one mislabels chains (v2-bad-2). That contrast is worth showing.
6. **Unchanged:** permissions (`edit`/`shell` ask, `subagent` deny) and
   `steps: 20`. The final good-agent used at most 6 steps, so 20 leaves ample
   headroom. Bad-agent used all 20 in 12/15 runs and ended with "Maximum steps
   reached". Raising the limit would make it slower, and these runs give no
   evidence that it would make the page better.

`bad-agent.md` changed only by the added `model:` line. Its prompt is
untouched.

## What we found beyond the scores

- **The static score can be gamed, and the bad agent gamed it.** In batch v1,
  4/5 bad-agent runs read `exercises/02-agents/README.md` and `check_viewer.py`,
  and 2/5 also read `good-agent.md`. All four scored 7/7. One of them
  (v1-bad-4) crashed on a nonexistent method and showed an empty canvas. In
  batch v2, 0/5 read those files. The behaviour depends on what the agent
  happens to explore. When the files were absent (`iso`), bad-agent averaged
  5.0/7 with 0/5 full passes. Static scores are a conversation starter. The
  browser and click checks are the evidence.
- **The 23 Sep failure modes came back with the vague prompt:**
  - nonexistent library methods: v1-bad-4 (3Dmol), v2-bad-4 (NGL);
  - hiding a chain leaves its heme visible: iso-bad-1, iso-bad-4;
  - stale identity after loading another structure: v1-bad-1, v1-bad-3.

  New failure modes were a home-made WebGL renderer that draws nothing
  (iso-bad-5), an unrequested Python build step (iso-bad-2, 3, 5) and wrong α/β
  chain labels (v2-bad-2).
- **Frontmatter `model:` was not applied by `opencode run`.** Test: in a copy
  whose project default was `opencode/nemotron-3.5-lightning-free`, run
  `opencode run --agent bad-agent` and `--agent good-agent` without `--model`.
  `opencode debug agents` reported both agents' model as `big-pickle`, yet the
  exported sessions show the project default `nemotron-3.5-lightning-free` was
  used. All trials above passed `--model` explicitly, so the comparison itself
  is fair. Whether the TUI/Desktop agent selector applies the frontmatter
  model was not tested.
- **Provider flakiness:** 4/28 runs ended with a big-pickle `HTTP 400`, and 1
  with "stream ended without finish_reason". One of them (v1-good-1) failed
  after its page was finished.
- **`check_viewer.py --browser` had to be fixed during the rehearsal.** A
  colour count over the whole screenshot flagged a blank page with colourful
  buttons as rendered (iso-bad-5), and it missed a page hidden behind a fading
  "Loading…" overlay (v2-bad-5, under headless virtual time). The final
  version disables CSS transitions in a temporary copy of the page and
  measures only inside the largest `<canvas>`. Measured values:

  | Page | Canvas that differs from background |
  |---|---|
  | Good pages | 17–24% |
  | Bad pages that rendered | 13–37% |
  | Empty or crashed pages | 0–4% |
  | Negative control (bad ID) | 0% |

  The threshold is 8%.

## Limitations

- One model (big-pickle), one machine (macOS, Chrome) and one day. The runs
  shared the machine and the provider with other workshop rehearsals running
  at the same time, so wall times include that contention.
- `--auto` approvals. In the workshop, participants approve each edit and shell
  command. Bad-agent made 14–30 tool calls, mostly shell; good-agent made 2–5,
  mostly edits/reads. Time spent approving was not measured.
- The behaviour probe uses heuristics to find controls by label or button
  text, and it only reads atoms from 3Dmol. NGL pages and "focus" buttons were
  judged from screenshots and page text. The local-file input was not
  exercised in any run.
- "Stale text" after loading 1CRN was judged by reading the text. For example,
  a generic "Heme & other ligands: 0 groups" heading was not counted as stale.
- `check_viewer.py` static checks are regex heuristics. A page can pass a check
  without the feature working, and an unusual working page can fail one. The
  checker says so in its output.

## Not yet verified

- **The final model.** Both agents' frontmatter says `model: opencode/big-pickle`
  because DTU was offline. Switch it to `dtu/qwen36` or the swarm bake-off
  winner, then re-run at least 3 runs per agent. A small-context model
  (16k–32k) may not fit the good page in one write.
- Whether the **TUI/Desktop agent selector** uses the frontmatter `model:`.
  `opencode run` did not.
- **Interactive timing**, with human approvals, against the 10-minute slot.
- **Windows/WSL2:** Edge/Chrome opening `file://` pages that fetch from RCSB,
  and `check_viewer.py --browser`, which looks for Chrome at the macOS path,
  `google-chrome`/`chromium` on PATH, or `C:\Program Files\...\chrome.exe`.
  From WSL2, `--chrome` is needed and `file://` paths may not resolve. Firefox
  and Safari were not tested.
- The prompt variant `outputs/02-agents/<agent>`, which matches the restructured
  README's "outputs go under `outputs/02-agents/`". All runs used
  `outputs/<agent>`.
- The offline local-file fallback and loading a structure without a ligand
  from a local file.

---

The proposed 2a text was applied to `exercises/02-agents/README.md` on 13 October 2026.
