# Workshop administration

Operating notes for Peter and Dimitrios. For participant setup see the
[student README](README.md).

All paths below are `/home/local/workshop` on the compute nodes, not the
repository on a laptop.

## Conference edition (dkb-2026): what must be true before the day

30 participants working individually, no break. Everything below is
**not yet verified**. Tick it off with the date and who checked it.

| # | Requirement | Why | Check |
|---|---|---|---|
| 1 | `qwen36`, `qwen38`, `mistral`, `gptoss` answer (on 13 Oct all four returned 503, later no connection) | Every module | `scripts/check-setup.sh` from a laptop outside DTU |
| 2 | A new **`embed`** route serving an embedding model (e.g. Qwen3-Embedding-0.6B) at `…/workshop/embed/embeddings` | Exercise 0 (RAG). Without it `rag.py` falls back to word matching | `scripts/check-setup.sh --module 00-rag` |
| 3 | The gateway forwards **`logprobs` and `top_logprobs`** for `qwen36` and returns them (check `app/request_compat.py` does not strip them) | Exercise 4 has no fallback without it | `scripts/check-setup.sh --module 04-decide` |
| 4 | The gateway forwards **`/embeddings`**, not only `/chat/completions` | Requirement 2 | as 2 |
| 5 | Load test: 30 simultaneous sessions per block profile (qwen36 for skills and MCP; mistral and embed for RAG; 30 swarms mostly on free models; qwen36 one-token requests for Exercise 4), recording p50/p95 latency and 429/5xx | On 25 Sep the room broke the gateway in 15 minutes | `admin/loadtest.sh` (to be written), results in this file |
| 6a | Decide the `agents.title` / `agents.summary` model in `opencode.json` (currently `dtu/gptoss`). On 13 Oct an offline DTU model produced **no error for 455 s**, it just hung, and one session title arrived ~5 min late. If DTU is down, compaction (the summary agent) may hang too (not tested) | Background tasks should not depend on one endpoint | Rehearsal with DTU deliberately unreachable |
| 6b | **Free-model rate limit (high risk).** OpenCode publishes no limits. User reports: one counter shared by *all* free models, about 200 requests per long rolling window, a ~15–20 requests/minute burst cap, and lockouts of 8–27 h; keyed on IP plus device or account (an `ipRateLimiter` exists in their server code). 30 laptops behind one NAT may share one budget, and a swarm uses many requests. Paid balance reportedly does *not* lift it (open issue [#33318](https://github.com/anomalyco/opencode/issues/33318)). This laptop was locked out on 13 Oct | 2c and every free-model fallback | Email help@anoma.ly about a 30-seat event on one network; or fund a Console workspace with members and cheap paid models; test 2–3 laptops on the venue network |
| 6 | Limits changed only from measured load, and **no gateway restart during the session** | A restart on 25 Sep left the room with no DTU models for 1–2 min | Runbook below |

**Day-of runbook.** One organiser watches the gateway log and `/health` during
the session; the other teaches. If DTU models fail, announce the free-model
fallback (`/models` → a free OpenCode model) rather than restarting. An
unreachable DTU model **hangs without an error**, so tell the room: no output
for a minute means switch model. Exercise 0
continues with `rag.py --lexical`; Exercise 4 has no fallback and moves to
discussion.

## Connect

```bash
ssh -J dimkan@login.healthtech.dtu.dk dimkan@compute04
cd /home/local/workshop
```

compute05 works the same way. Run everything on a compute node, not the login
node.

## Start, stop and check

Either node can drive both.

| Scope | Start | Stop | Status |
|---|---|---|---|
| compute04 models | `bash bin/llm start compute04` | `bash bin/llm kill compute04` | `bash bin/llm status compute04` |
| compute05 model | `bash bin/llm start compute05` | `bash bin/llm kill compute05` | `bash bin/llm status compute05` |
| Everything | `bash bin/llm start all` | `bash bin/llm kill all` | `bash bin/llm status all` |

**Before the workshop: `bash bin/llm start all`, then check the readiness
summary for both nodes.**

A start also brings up any missing connection services and leaves
already-running models alone. `kill` and `stop` are the same command. To
restart, stop, wait for success, then start.

> The **gateway** is the shared connection service and runs on compute04.
> Stopping compute04 disconnects every model, Qwen 3.8 included. Starting
> compute05 brings the gateway up if needed, but does not start compute04's
> other models.

No tmux needed; closing SSH leaves the models running. Start them again after
a reboot. Use the setup only during the approved reservation, and do not
bypass the occupied-GPU checks.

Single models run on their own node:

```bash
bash bin/llm start mistral      # compute04
bash bin/llm stop  mistral
bash bin/llm start qwen38       # compute05
bash bin/llm stop  qwen38
```

Add `--dry-run` to preview. `bash bin/llm --help` for the rest.

## Model settings

| Model ID | Node | GPUs | Configured context | Launcher ceiling | Checkpoint maximum | Output cap |
|---|---|---|---:|---:|---:|---:|
| `qwen36` | compute04 | 0, 1 | 16384 | 65536 | 262144 | 4096 |
| `qwen38` | compute05 | 0, 1 | 32768 | 65536 | 262144 | 8192 |
| `mistral` | compute04 | 2 | 16384 | 32768 | 131072 | 4096 |
| `gptoss` | compute04 | 3 | 16384 | 32768 | 131072 | 8192 |

The checkpoint maximum is what the model supports, not what the current GPU
allocation fits. The launcher ceiling is what it will accept without testing.

**25 September live check:** Qwen 3.6 is currently running with 32768 context
(its persistent default above remains 16384); Qwen 3.8 has 32768, Mistral and
GPT-OSS have 16384. All four passed public chat, streaming and tool round trips.
Students may set client context/output up to these running limits and the
output caps above without separate approval. Defaults in the download remain
unchanged. The helper `.opencode/scripts/halp-context.py` carries this dated
snapshot: update its constants and the student table if server limits change.

**Context** is the whole conversation plus the answer, in tokens, including
instructions and tool results. **Output** is the answer alone.

Change a model's context by stopping it first:

```bash
bash bin/llm stop mistral
bash bin/llm start mistral --context 32768
```

- That changes one launch. For a persistent default, edit `context` in the
  node's `config/models.json`, then stop and start.
- A running model ignores a new start request. Revert with
  `bash bin/llm stop mistral` then `bash bin/llm start mistral --context 16384`.
- Student `limit.context` defaults stay at 16384, 32768 for Qwen 3.8, with
  output 4096. Students restart OpenCode after a config change.
- Output caps live in compute04's `app/gateway.py`, separate from server
  context. Changing them needs tests and a gateway restart.

### Raising the context limits

1. Confirm GPU visibility and the reservation. Keep the GPU assignments and
   occupied-GPU checks.
2. Test one model at a time against its checkpoint maximum, using a temporary
   profile and keeping the working configuration for recovery. Do not bypass
   vLLM's length and memory validation, change quantization, or add context
   extension.
3. Check the running `max_model_len`, a normal response, a long input,
   streaming, and a tool-call round trip. Then concurrent requests,
   cancellation and busy responses.
4. The gateway and model endpoints cap request bodies at 2 MiB. If that blocks
   valid input, raise the application caps to 8 MiB and have Peter match the
   HTTPS-proxy limit. Keep answer caps as they are.
5. Once a target passes, persist `context` and `max_context` in that node's
   `config/models.json`, synchronise Qwen 3.8's profile on both nodes, and
   check the public endpoint after the restart. If it fails, restore the
   previous profile.
6. Update the student defaults only if you intend students to use more.
   Budgets above 32768 need organiser approval.

### Gateway request limits

**Raised 25 September 2026, during the workshop,** after the room hit
`Provider request failed with HTTP 429` retries. Every student reaches the
gateway without a key, so the whole room counts as a single team,
`workshop-shared`, and shares one set of limits.

| Limit | Where | Before | Now |
|---|---|---:|---:|
| Shared team requests per minute | `app/gateway.py`, `authorize()`, `workshop-shared` | 60 | 600 |
| Shared team concurrent requests | same line | 4 | 40 |
| In-flight requests per model | `config/models.json`, `max_inflight`, all four models | 4 | 12 |

Any of the three returns a 429 with `Retry-After`: "Team request-per-minute
limit reached", "Team concurrent-request limit reached" or "Model busy; retry
with backoff". These are raised before the audit row is written, so **429s do
not appear in `logs/requests.jsonl`**. That file only shows requests that got
through.

The new values have not been load-tested. After the restart the health check
reported all four models active and requests returned 200. If Qwen 3.6 or
Qwen 3.8 slows down badly, lower that model's `max_inflight` to 8. The
previous files are kept next to the originals on compute04 as
`app/gateway.py.bak-<timestamp>` and `config/models.json.bak-<timestamp>`.
Either change needs a gateway restart; see the warning under
[Checks and troubleshooting](#checks-and-troubleshooting).

## Checks and troubleshooting

The launcher waits up to five minutes per node, checks gateway and model
health, then sends a test message through each public URL. A model is
**READY** only once it returns text. Models are checked independently, and the
summary lists each as READY or NOT READY with a reason. Check both nodes.

Re-running the start command repeats the checks without reloading running
models.

**Isolation warning (checked 23 September 2026):** the shared gateway's
`/health` and `/models` handlers probe every configured backend, including
compute05. A compute04-only start's normal readiness checks can therefore
contact compute05. Do not use those checks when compute05 must be completely
untouched. Test a selected compute04 model with a direct chat request instead;
do not stop the shared gateway while compute05 is in use.

From anywhere with access to the teaching URL:

```bash
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/mistral/health
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/mistral/models
```

Swap `mistral` for another model ID. `available: true` is the one to look for;
`max_model_len` shows the running context size.

On the node:

```bash
bash bin/llm status all
tail -n 60 logs/direct-mistral.log
```

Also `direct-qwen36.log`, `direct-qwen38.log`, `direct-gptoss.log`, and
`logs/direct-gateway.log` on compute04 for connection-service errors.

Gateway only, on compute04:

```bash
bash bin/llm stop gateway
bash bin/llm start gateway
```

That leaves the models loaded, but disconnects every model while the gateway
is down. Warn the room first, and run the two commands separately rather than
chained with `&&`.

**Observed on 25 September 2026:** `stop` waits for open requests to finish.
It waited on a 179-second Qwen 3.8 request, and the replacement gateway did not
start after that stop. The room had no DTU models for about 1–2 minutes, until
`bash bin/llm start gateway` was run on its own. After a stop, confirm with
`bash bin/llm status all` that the gateway shows a new PID, and check
`/health`.

### Model switching and effort compatibility (25 September 2026)

- Mistral Nemo rejects reasoning metadata from earlier GPT-OSS/Qwen turns
  (`ThinkChunk`). On compute04, `app/request_compat.py` now removes assistant
  `reasoning`, `reasoning_content` and `reasoning_text` fields for Mistral only.
  Visible answers, tool calls and tool results are preserved. Regression tests
  are in `tests/test_reasoning_history.py`; all 92 server tests passed.
- Qwen 3.8's template rejects `high`. Although it advertises `xhigh` as its
  default, the running API also rejects an explicit `reasoning_effort: xhigh`.
  The student configuration therefore lists only tested explicit `low` and
  `medium` variants. Leaving effort unset uses the server default.
- Mistral uses an empty variants list, preventing OpenCode's generic
  low/medium/high fallback. Updating the JSON requires `opencode reload` and
  reselecting the model in existing sessions.
- Only the shared gateway was restarted for this fix, not the GPU engines.
  Switched-model Mistral history was tested through public HTTPS in both normal
  and streaming modes. Successful requests do not guarantee answer quality:
  Mistral remains less reliable at following complex workshop instructions.

## Files and ports

| Location | Purpose |
|---|---|
| `bin/llm.py` | Start, stop and status |
| `app/` | Connection handling and model requests |
| `config/models.json` | Model settings and server addresses |
| `config/model-endpoints.json`, `config/reverse-proxy.json` | Public-connection settings |
| `config/access-policy.json` | Whether students need an API key |
| `models/`, `envs/`, `runtime/` | Models and installed software. Leave in place |
| `logs/`, `run/`, `cache/`, `tmp/` | Logs and working files. Do not clear while running |

vLLM 0.19.0 runs the models. Peter's HTTPS server forwards each public model
URL to its HTTP address.

## Endpoints

| Model ID | Public Base URL | HTTP upstream | Node |
|---|---|---|---|
| `qwen36` | `https://teaching.healthtech.dtu.dk/workshop/qwen36` | `http://10.57.11.104:28102` | compute04 |
| `qwen38` | `https://teaching.healthtech.dtu.dk/workshop/qwen38` | `http://10.57.11.105:28101` | compute05 |
| `mistral` | `https://teaching.healthtech.dtu.dk/workshop/mistral` | `http://10.57.11.104:28103` | compute04 |
| `gptoss` | `https://teaching.healthtech.dtu.dk/workshop/gptoss` | `http://10.57.11.104:28104` | compute04 |

Use the public Base URLs exactly as shown and **do not append `/v1`**.
OpenCode appends `/chat/completions`; health and listing use `/health` and
`/models`. Preserve that suffix when forwarding. TLS is handled by the HTTPS
proxy, so the upstreams are HTTP.

The gateway is on compute04 port 28100 and must reach Qwen 3.8's service on
compute05 port 28201.

Student API keys are disabled.

## Tests

On compute04:

```bash
source bin/workshop-env.sh
PYTHONPATH=/home/local/workshop envs/manage/bin/python -m unittest discover -s tests -p 'test_*.py'
```
