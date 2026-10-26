# Workshop administration

Operating notes for Peter and Dimitrios. For participant setup see the
[student README](README.md).

All paths below are `/home/local/workshop` on the compute nodes, not the
repository on a laptop.

## Before a workshop

- **The workshop key.** Exercises 1 and 5 call OpenRouter (Mistral Nemo,
  `bge-base` embeddings, Llama 3.1 8B) with one shared key. Give it a
  spending limit in OpenRouter, show it on a slide or the board at the start
  (Exercise 0c), never put it in the repository, and rotate it after
  the session. A whole room costs cents.
- **Qwenstorm, the default model.** The chat, the workshop agents and HALp
  use `dtu/qwen36`, which is Qwenstorm: copies of Qwen 3.6 on several GPU
  nodes behind one public URL (see [Qwenstorm](#qwenstorm)). Start it before
  the room arrives with `bash bin/llm start all`, and check the readiness
  summary of every node.
- **Free models.** People doing the course on their own have no DTU access
  and use OpenCode's free models instead; the workshop agents follow the
  model they select. In the room the free models are only for trying out:
  their allowance is counted per account and per network, so one room shares
  it, and once it is used up every free model refuses.
- **Plugins are cloned, not added.** Exercise 0 clones both plugins into
  `.opencode/plugins/`. On OpenCode 2.0.29 a plugin
  installed with `opencode plugin add github:…` loads but never redraws, so a
  sidebar that never changes means that install; HALp knows.
- **During a session**, one of us watches OpenRouter's usage page and the
  gateway logs. If Qwenstorm cannot be reached, people switch to a free model
  with `/models` until it is back.

### Still to check

1. **Exercises 1 and 5 with `RAG_DTU=1`.** Exercise 1 also needs an `embed`
   route, which Qwenstorm does not have, so leave Exercise 1 on the workshop
   key. Exercise 5 needs the token probabilities through the gateway.
2. **One run-through in the real interface.** The exercises were run with
   `opencode run`, which approves automatically. Still to see by hand:
   switching between Plan and Build, clicking through approvals one by one,
   and switching on `duckdb` with `/mcps` in Exercise 4.
3. **Windows (WSL2) and Linux.** Everything so far ran on a Mac: the install,
   `scripts/check-setup.sh`, the plugin install and the exercises.

## Qwenstorm

Qwenstorm is ten copies of Qwen 3.6, one GPU each, on three nodes:

| Node | GPUs | Copies | Ports |
|---|---|---|---|
| compute05 | 2 × H100 NVL | `qwen36-01`, `qwen36-02` | 28111–28112 |
| compute07 | 4 × RTX PRO 6000 Blackwell | `qwen36-03` … `qwen36-06` | 28113–28116 |
| compute08 | 4 × RTX PRO 6000 Blackwell | `qwen36-07` … `qwen36-10` | 28117–28120 |

- Each copy is its own vLLM server. It answers to `qwen36`, which is what
  students ask for, and to its own copy name, which the checks and logs use.
- Every node also runs its own **gateway** (port 28100) and its own public
  **endpoint** (port 28102). A gateway sends each request to the least busy
  live copy, its own node's copies first and the other nodes' copies after
  that. If a copy does not answer, the request moves to another one.
- Peter's HTTPS server balances `/workshop/qwen36` over the three endpoints
  and takes a node out of rotation while it does not answer, or answers 502
  or 503. No node needs another, so any one node can carry the room on its
  own, more slowly.

Everyone uses the same model name; nobody is assigned a copy. compute04 is
no longer part of the workshop.

## Connect

```bash
ssh -J dimkan@login.healthtech.dtu.dk dimkan@compute05
cd /home/local/workshop
```

compute07 and compute08 are reached from compute05 (`ssh compute07`). Run
everything on a compute node, not the login node.

## Start, stop and check

Any node can drive all three.

| Scope | Start | Stop | Status |
|---|---|---|---|
| One node | `bash bin/llm start compute07` | `bash bin/llm kill compute07` | `bash bin/llm status compute07` |
| Everything | `bash bin/llm start all` | `bash bin/llm kill all` | `bash bin/llm status all` |

**Before the workshop: `bash bin/llm start all`, then check the readiness
summary for every node.**

A start brings up the node's gateway, its copies and its endpoint, and leaves
anything already running alone. `kill` and `stop` are the same command. To
restart, stop, wait for success, then start.

On its own node, one copy or all of a node's copies:

```bash
bash bin/llm start qwen36-04    # one copy
bash bin/llm stop  qwen36-04
bash bin/llm start qwen36       # this node's copies and its endpoint
```

Restarting one node does not need a warning: the balancer and the other
nodes carry the room meanwhile. Stopping every node takes Qwenstorm away.

No tmux needed; closing SSH leaves everything running. Start it again after
a reboot. Use the setup only during the approved reservation, and do not
bypass the occupied-GPU checks. compute07 and compute08 are not in Slurm; the
launcher's `nvidia-smi` check still refuses occupied GPUs there.

Add `--dry-run` to preview. `bash bin/llm --help` for the rest.

## Model settings

`config/models.json` is the same file on every node. The `qwen36` profile:

| Setting | Value | Meaning |
|---|---:|---|
| `context` / `max_context` | 65536 | Running context per conversation |
| `max_output` | 4096 | Answer cap, applied by the gateway |
| `max_num_seqs` | 16 | Requests one copy runs at once |
| `max_inflight` | 16 | Requests a gateway sends to one copy at once |
| `gpu_memory_utilization` | 0.90 | Share of the GPU vLLM may use |
| `enforce_eager` | false | CUDA graphs on |

- **Context.** One OpenCode turn is about 9,000 tokens before any work: its
  instructions and tool definitions. 16384 was too small for the exercises.
  At 65536 a long chat reaches the limit and OpenCode compacts it and goes
  on. The checkpoint supports 262144.
- **CUDA graphs** make a copy about six times faster than eager mode
  (`enforce_eager: true`), for a fraction of a GB of GPU memory.
- **Students** may lower `limit.context` in their `opencode.json`; the
  supplied 65536 is already the maximum. The helper
  `.opencode/scripts/halp-context.py` carries the same limits: update its
  constants and the student table if the server limits change.

**Context** is the whole conversation plus the answer, in tokens, including
instructions and tool results. **Output** is the answer alone.

To change a setting, edit `config/models.json` on every node, then restart
one node at a time:

```bash
bash bin/llm stop qwen36-03      # each copy on this node
bash bin/llm start all --local
```

`bash bin/llm start qwen36-03 --context 32768` changes one launch only. A
running copy ignores a new start request. Changes to `max_inflight`,
`max_output` or the copies need a gateway restart on each node as well.

Qwen 3.8's weights are kept on compute05, and its profile is in
`config/models.json` with `enabled: false`. It needs both of compute05's GPUs,
so `qwen36-01` and `qwen36-02` stop first.

### Gateway request limits

Every student reaches a gateway without a key, so the whole room counts as a
single team, `workshop-shared`, and shares one set of limits per gateway:

| Limit | Where | Value |
|---|---|---:|
| Shared team requests per minute | `app/gateway.py`, `authorize()` | 2000 |
| Shared team concurrent requests | same line | all copies' `max_inflight` together |
| Requests in flight per copy | `config/models.json`, `max_inflight` | 16 |

Any of them returns a 429 with `Retry-After`: "Team request-per-minute
limit reached", "Team concurrent-request limit reached" or "Model busy; retry
with backoff". These are raised before the audit row is written, so **429s do
not appear in `logs/requests.jsonl`**. That file only shows requests that got
through, each with the copy that answered.

## Checks and troubleshooting

The launcher waits up to five minutes per node. A copy is **READY** once it
answers a short message itself and its node's gateway lists it as live; the
node's public route is then checked with a test message. The summary lists
each as READY or NOT READY with a reason. Re-running the start command
repeats the checks without reloading running copies.

From anywhere with access to the teaching URL:

```bash
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/qwen36/health
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/qwen36/models
```

`available: true` is the one to look for; `max_model_len` shows the running
context. On a node, its gateway shows every copy, live or not, and how many
requests each has in flight:

```bash
curl -s http://10.57.11.107:28100/workshop/health
bash bin/llm status all --local
tail -n 60 logs/direct-qwen36-04.log
```

Also `logs/direct-gateway.log` and `logs/direct-endpoint-qwen36.log` for the
connection services.

A node's gateway alone:

```bash
bash bin/llm stop gateway
bash bin/llm start gateway
```

That leaves the copies loaded; the balancer sends the room to the other
nodes meanwhile. Run the two commands separately rather than chained with
`&&`. `stop` waits for open requests to finish; afterwards, confirm with
`bash bin/llm status all --local` that the gateway shows a new PID.

## Files and ports

| Location | Purpose |
|---|---|
| `bin/llm.py` | Start, stop and status |
| `app/` | Connection handling and model requests |
| `app/nodes.py` | The nodes and their addresses |
| `config/models.json` | Model settings and the copies |
| `config/model-endpoints.json`, `config/reverse-proxy.json` | Public-connection settings |
| `config/access-policy.json` | Whether students need an API key |
| `models/`, `envs/`, `runtime/` | Models and installed software. Leave in place |
| `logs/`, `run/`, `cache/`, `tmp/` | Logs and working files. Do not clear while running |

vLLM 0.19.0 runs the copies. Ports on every node: 28100 gateway, 28102
endpoint, 28111–28120 copies.

## Endpoints

| Model ID | Public Base URL | HTTP upstream | Nodes |
|---|---|---|---|
| `qwen36` | `https://teaching.healthtech.dtu.dk/workshop/qwen36` | `balancer://workshop-qwen36` → `http://10.57.11.105:28102`, `.107:28102`, `.108:28102` | compute05, compute07, compute08 |

Use the public Base URL exactly as shown and **do not append `/v1`**.
OpenCode appends `/chat/completions`; health and listing use `/health` and
`/models`. Preserve that suffix when forwarding. TLS is handled by the HTTPS
proxy, so the upstreams are HTTP. The balancer in Peter's configuration:

```apache
<Proxy "balancer://workshop-qwen36">
    BalancerMember "http://10.57.11.105:28102" loadfactor=2 retry=10 connectiontimeout=3
    BalancerMember "http://10.57.11.107:28102" loadfactor=4 retry=10 connectiontimeout=3
    BalancerMember "http://10.57.11.108:28102" loadfactor=4 retry=10 connectiontimeout=3
    ProxySet lbmethod=bybusyness failonstatus=502,503
</Proxy>
```

Student API keys are disabled.

## Tests

On any node:

```bash
source bin/workshop-env.sh
PYTHONPATH=/home/local/workshop envs/manage/bin/python -m unittest discover -s tests -p 'test_*.py'
```
