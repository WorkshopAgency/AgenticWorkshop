#!/usr/bin/env python3
"""Model bake-off for the genome-team swarm (Exercise 3, OpenCode v2).

Runs three known-answer tool tasks on the NCBI reference-genome CSV against
each candidate model, scores them against ground truth computed here, and
prints a table. Optionally runs one end-to-end swarm with a chosen assignment.

Every run happens in a fresh scratch copy of the repo, never in the repo
itself. The scratch copy's opencode.json is patched so that the default,
title and summary models point at a Zen model rather than dtu/gptoss
(an offline DTU backend makes OpenCode retry silently instead of failing).

Usage (from anywhere; standard library only):

    python3 admin/model-bakeoff.py                     # all tasks, all models, 3 reps
    python3 admin/model-bakeoff.py --reps 1 --models opencode/big-pickle
    python3 admin/model-bakeoff.py --swarm-only        # just the end-to-end swarm
    python3 admin/model-bakeoff.py --no-swarm          # skip the swarm

Results (JSONL per run, event streams, scratch copies) go under --workdir,
default $TMPDIR/opencode-bakeoff-<timestamp>.
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import csv
import datetime as dt
import gzip
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA_REL = "exercises/03-mcp/data/byo/ncbi_reference_genomes.csv.gz"
ZEN_MODELS_URL = "https://opencode.ai/zen/v1/models"

ZEN_CANDIDATES = [
    "opencode/big-pickle",
    "opencode/ling-3.1-flash-free",
    "opencode/mimo-v2.6-flash-free",
    "opencode/nemotron-3.5-lightning-free",
    "opencode/step-5-preview-free",
    "opencode/longcat-2.5-preview-free",
    "opencode/space-bunny-free",
    "opencode/cat-jam-free",
]
DTU_CANDIDATES = ["dtu/qwen36", "dtu/qwen38", "dtu/mistral", "dtu/gptoss"]

# Recommended all-Zen assignment (see admin/model-bakeoff.md for the evidence).
DEFAULT_SWARM = {
    "coordinator": "opencode/big-pickle",
    "auditor": "opencode/step-5-preview-free",
    "analyst": "opencode/mimo-v2.6-flash-free",
    "visualizer": "opencode/space-bunny-free",
    "reviewer": "opencode/longcat-2.5-preview-free",
}
SWARM_PROMPT = (
    "Run the genome-size team task with all four specialist subagents. Save the "
    "actual outputs in a new folder under outputs/genome-team/. Report failed or "
    "untested steps."
)

T3_PATH = "bakeoff_out/group_summary.csv"
T3_COLUMNS = ["group", "n_assemblies", "median_genes_per_mb", "median_gc_percent"]

TASKS = {
    "T1": (
        f"How many rows and which organism groups are in {DATA_REL}? "
        "Give counts per group."
    ),
    "T2": (
        f"Using {DATA_REL}, take only assemblies whose assembly_level is exactly "
        "'Complete Genome'. For each organism group (column `group`), report the "
        "number of such assemblies and their median genome size in Mb "
        "(genome_size is in base pairs; 1 Mb = 1,000,000 bp), to 2 decimals. "
        "Compute this by running code on the file; do not estimate. Answer with "
        "one line or table row per group."
    ),
    "T3": (
        f"Using all rows of {DATA_REL}, write a CSV file to {T3_PATH} (create the "
        "folder if needed) with exactly these columns in this order: "
        + ",".join(T3_COLUMNS)
        + ". One row per organism group (column `group`). n_assemblies is the row "
        "count; median_genes_per_mb is the median over assemblies of "
        "total_gene_count / (genome_size / 1,000,000), computed per assembly; "
        "median_gc_percent is the median of gc_percent. Round medians to 2 "
        "decimals. Compute by running code; then reply with the file path."
    ),
}

ERROR_PATTERNS = [
    ("403", re.compile(r"\b403\b|free tier can only be used", re.I)),
    ("404", re.compile(r"\b404\b|not found", re.I)),
    ("429", re.compile(r"\b429\b|rate limit|too many requests", re.I)),
    ("unavailable", re.compile(r"unavailable|\b400\b|\b50[0-9]\b|overloaded", re.I)),
    ("timeout", re.compile(r"timeout|timed out", re.I)),
    ("aborted", re.compile(r"abort|interrupt", re.I)),
]

_print_lock = threading.Lock()


def log(msg: str) -> None:
    with _print_lock:
        print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# --------------------------------------------------------------------------
# Ground truth
# --------------------------------------------------------------------------

def ground_truth(path: Path) -> dict:
    with gzip.open(path, "rt", newline="") as fh:
        rows = list(csv.DictReader(fh))
    groups = collections.Counter(r["group"] for r in rows)
    complete = collections.defaultdict(list)
    dens = collections.defaultdict(list)
    gc = collections.defaultdict(list)
    for r in rows:
        try:
            size = float(r["genome_size"])
        except ValueError:
            continue
        if size <= 0:
            continue
        if r["assembly_level"] == "Complete Genome":
            complete[r["group"]].append(size / 1e6)
        try:
            dens[r["group"]].append(float(r["total_gene_count"]) / (size / 1e6))
        except ValueError:
            pass
        try:
            gc[r["group"]].append(float(r["gc_percent"]))
        except ValueError:
            pass
    return {
        "rows": len(rows),
        "groups": dict(groups),
        "complete": {g: (len(v), statistics.median(v)) for g, v in complete.items()},
        "density": {g: statistics.median(v) for g, v in dens.items()},
        "gc": {g: statistics.median(v) for g, v in gc.items()},
    }


# --------------------------------------------------------------------------
# Answer checking
# --------------------------------------------------------------------------

_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _numbers(line: str) -> list[float]:
    line = re.sub(r"(?<=\d)[,   ](?=\d{3}(?!\d))", "", line)
    return [float(x) for x in _NUM.findall(line)]


def _norm(s: str) -> str:
    return s.lower().replace("_", " ").replace("`", "").replace("*", "")


def _close(a: float, b: float, abs_tol: float, rel_tol: float) -> bool:
    return abs(a - b) <= max(abs_tol, rel_tol * abs(b))


def _group_lines(text: str, group: str) -> list[str]:
    g = _norm(group)
    pat = re.compile(r"(?<![a-z])" + re.escape(g) + r"(?![a-z])")
    return [ln for ln in _norm(text).splitlines() if pat.search(ln)]


def check_lines(text: str, expected: dict, tols: list[tuple[float, float]]) -> tuple[bool, list[str]]:
    """expected: group -> tuple of values; each value must appear on one line naming the group."""
    problems = []
    for group, values in expected.items():
        ok = False
        for ln in _group_lines(text, group):
            nums = _numbers(ln)
            if all(any(_close(n, v, *tols[i]) for n in nums) for i, v in enumerate(values)):
                ok = True
                break
        if not ok:
            problems.append(f"{group}: expected {values}")
    return not problems, problems


def check_t1(text: str, truth: dict, workdir: Path) -> tuple[bool, str]:
    ok_total = any(_close(n, truth["rows"], 0, 0) for n in _numbers(text))
    ok, probs = check_lines(text, {g: (n,) for g, n in truth["groups"].items()}, [(0, 0)])
    if not ok_total:
        probs.insert(0, f"total {truth['rows']} not found")
    return ok and ok_total, "; ".join(probs)


def check_t2(text: str, truth: dict, workdir: Path) -> tuple[bool, str]:
    exp = {g: (n, round(m, 2)) for g, (n, m) in truth["complete"].items()}
    ok, probs = check_lines(text, exp, [(0, 0), (0.011, 0.005)])
    return ok, "; ".join(probs)


def check_t3(text: str, truth: dict, workdir: Path) -> tuple[bool, str]:
    f = workdir / T3_PATH
    if not f.exists():
        return False, f"{T3_PATH} missing"
    try:
        with f.open(newline="") as fh:
            rows = list(csv.reader(fh))
    except Exception as exc:  # noqa: BLE001
        return False, f"unreadable: {exc}"
    if not rows or [c.strip() for c in rows[0]] != T3_COLUMNS:
        return False, f"header {rows[0] if rows else None}"
    body = {r[0].strip(): r for r in rows[1:] if r and r[0].strip()}
    probs = []
    if set(body) != set(truth["groups"]):
        probs.append(f"groups {sorted(body)}")
    for g, n in truth["groups"].items():
        r = body.get(g)
        if not r or len(r) < 4:
            probs.append(f"{g}: missing")
            continue
        try:
            n_ok = int(float(r[1])) == n
            d_ok = _close(float(r[2]), truth["density"][g], 0.011, 0.002)
            gc_ok = _close(float(r[3]), truth["gc"][g], 0.011, 0.002)
        except ValueError:
            probs.append(f"{g}: non-numeric {r}")
            continue
        if not (n_ok and d_ok and gc_ok):
            probs.append(f"{g}: got {r[1:4]}")
    return not probs, "; ".join(probs)


CHECKS = {"T1": check_t1, "T2": check_t2, "T3": check_t3}


# --------------------------------------------------------------------------
# Scratch copies and OpenCode runs
# --------------------------------------------------------------------------

def make_base(workdir: Path, config_model: str) -> Path:
    base = workdir / "base"
    if base.exists():
        return base
    shutil.copytree(
        REPO, base,
        ignore=shutil.ignore_patterns(".git", "slides", "outputs", "admin", "bakeoff_out"),
    )
    cfg_path = base / "opencode.json"
    cfg = json.loads(cfg_path.read_text())
    pid, mid = config_model.split("/", 1)
    ref = {"providerID": pid, "model": mid}
    cfg["model"] = ref
    cfg.setdefault("agents", {})
    for a in ("title", "summary"):
        cfg["agents"].setdefault(a, {})["model"] = dict(ref)
    cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")
    return base


def fresh_copy(base: Path, dest: Path) -> Path:
    shutil.copytree(base, dest)
    env = {**os.environ, "GIT_AUTHOR_NAME": "bakeoff", "GIT_AUTHOR_EMAIL": "bakeoff@localhost",
           "GIT_COMMITTER_NAME": "bakeoff", "GIT_COMMITTER_EMAIL": "bakeoff@localhost"}
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"], ["git", "commit", "-qm", "base"]):
        subprocess.run(cmd, cwd=dest, check=True, env=env, stdout=subprocess.DEVNULL)
    return dest


def oc_api(method: str, path: str, *params: str, cwd: Path | None = None) -> dict | None:
    cmd = ["opencode", "api", method, path]
    for p in params:
        cmd += ["--param", p]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           stdin=subprocess.DEVNULL, cwd=cwd,
                           env={**os.environ, "PWD": str(cwd)} if cwd else None)
        return json.loads(r.stdout)
    except Exception:  # noqa: BLE001
        return None


def classify(msg: str) -> str:
    for name, pat in ERROR_PATTERNS:
        if pat.search(msg):
            return name
    return "other"


def parse_events(lines: list[str]) -> dict:
    out = {"session": None, "text": "", "tool_calls": 0, "tool_errors": 0,
           "tool_error_detail": [], "errors": [], "steps": 0, "tools": collections.Counter(),
           "subagent_calls": []}
    last_text = ""
    for ln in lines:
        try:
            e = json.loads(ln)
        except json.JSONDecodeError:
            continue
        out["session"] = out["session"] or e.get("sessionID")
        t = e.get("type")
        part = e.get("part") or {}
        if t == "step_start":
            out["steps"] += 1
        elif t == "text":
            last_text = part.get("text") or ""
            out["text"] += last_text + "\n"
        elif t == "tool_use":
            out["tool_calls"] += 1
            name = part.get("tool") or "?"
            out["tools"][name] += 1
            st = part.get("state") or {}
            if st.get("status") == "error" or name in ("invalid", "?"):
                out["tool_errors"] += 1
                out["tool_error_detail"].append(f"{name}: {str(st.get('error') or st.get('output'))[:160]}")
            if name in ("task", "subagent", "agent"):
                inp = st.get("input") or {}
                out["subagent_calls"].append({
                    "tool": name,
                    "agent": inp.get("subagent_type") or inp.get("agent") or inp.get("name"),
                    "status": st.get("status"),
                    "output": str(st.get("output") or st.get("error") or "")[:400],
                })
        elif t == "error":
            err = e.get("error") or {}
            msg = f"{err.get('type')}: {err.get('message')} (status {err.get('status')})"
            out["errors"].append(msg)
    out["final_text"] = last_text
    return out


def run_opencode(cwd: Path, model: str, prompt: str, timeout: int, events_file: Path,
                 agent: str | None = None, on_tick=None) -> dict:
    cmd = ["opencode", "run", "--auto", "--format", "json", "--model", model]
    if agent:
        cmd += ["--agent", agent]
    cmd.append(prompt)
    t0 = time.monotonic()
    lines: list[str] = []
    timed_out = False
    with events_file.open("w") as ef:
        # The opencode client takes the project directory from $PWD, not from the
        # process cwd; without this every run would land in the caller's directory.
        env = {**os.environ, "PWD": str(cwd)}
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)

        def reader():
            for ln in proc.stdout:
                lines.append(ln)
                ef.write(ln)
                ef.flush()

        th = threading.Thread(target=reader, daemon=True)
        th.start()
        deadline = time.monotonic() + timeout
        stopped = False
        while True:
            try:
                proc.wait(timeout=min(30, max(1, deadline - time.monotonic())))
                break
            except subprocess.TimeoutExpired:
                if on_tick and on_tick(parse_events(lines)["session"], time.monotonic() - t0):
                    stopped = True
                elif time.monotonic() < deadline:
                    continue
            timed_out = not stopped
            ev = parse_events(lines)
            if ev["session"]:
                oc_api("POST", f"/api/session/{ev['session']}/interrupt")
            try:
                proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                proc.kill()
            break
        th.join(timeout=10)
        stderr = proc.stderr.read() if proc.stderr else ""
    res = parse_events(lines)
    res["wall_s"] = round(time.monotonic() - t0, 1)
    res["ran_in"] = None
    if res["session"]:
        info = oc_api("GET", f"/api/session/{res['session']}") or {}
        res["ran_in"] = ((info.get("data") or {}).get("location") or {}).get("directory")
        if res["ran_in"] and Path(res["ran_in"]).resolve() != Path(cwd).resolve():
            raise SystemExit(f"session {res['session']} ran in {res['ran_in']}, not {cwd}; aborting")
    res["timed_out"] = timed_out
    res["stopped"] = stopped
    res["returncode"] = proc.returncode
    res["stderr"] = stderr[-2000:]
    if timed_out:
        res["errors"].append(f"timeout after {timeout}s")
    return res


def one_task_run(base: Path, workdir: Path, model: str, task: str, rep: int,
                 truth: dict, timeout: int) -> dict:
    tag = f"{model.replace('/', '_')}__{task}__r{rep}"
    dest = fresh_copy(base, workdir / "runs" / tag)
    res = run_opencode(dest, model, TASKS[task], timeout, workdir / "events" / f"{tag}.jsonl")
    completed = (not res["timed_out"] and not res["errors"]
                 and bool(res["final_text"].strip()))
    passed, why = CHECKS[task](res["text"], truth, dest)
    if task == "T3":  # the file is what counts; the reply only needs to exist
        passed = passed and not res["timed_out"]
    else:
        passed = passed and completed
    rec = {
        "model": model, "task": task, "rep": rep, "completed": completed, "passed": passed,
        "check": why, "wall_s": res["wall_s"], "steps": res["steps"],
        "tool_calls": res["tool_calls"], "tool_errors": res["tool_errors"],
        "tool_error_detail": res["tool_error_detail"][:5], "errors": res["errors"],
        "error_kinds": sorted({classify(e) for e in res["errors"]}),
        "empty_answer": not res["final_text"].strip(), "session": res["session"],
        "stderr": res["stderr"][-300:],
    }
    log(f"{model:40s} {task} r{rep}: {'PASS' if passed else 'fail'} "
        f"{res['wall_s']:6.1f}s tools={res['tool_calls']} toolerr={res['tool_errors']} "
        f"err={rec['error_kinds'] or '-'} {why[:80]}")
    return rec


# --------------------------------------------------------------------------
# Pre-flight
# --------------------------------------------------------------------------

def live_zen_models() -> list[str]:
    try:  # curl, because python.org builds on macOS often lack CA certificates
        r = subprocess.run(["curl", "-sS", "-m", "20", ZEN_MODELS_URL],
                           capture_output=True, text=True, check=True)
        data = json.loads(r.stdout)
        return [m["id"] for m in data.get("data", data)]
    except Exception as exc:  # noqa: BLE001
        log(f"could not fetch {ZEN_MODELS_URL}: {exc}")
        return []


def local_models() -> list[str]:
    r = subprocess.run(["opencode", "models"], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL, cwd=REPO, timeout=120,
                       env={**os.environ, "PWD": str(REPO)})
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def dtu_reachable(model: str) -> bool:
    cfg = json.loads((REPO / "opencode.json").read_text())
    mid = model.split("/", 1)[1]
    url = cfg["providers"]["dtu"]["models"][mid]["settings"]["baseURL"].rstrip("/") + "/models"
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-m", "10", "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    code = r.stdout.strip()
    return code.isdigit() and 0 < int(code) < 500


# --------------------------------------------------------------------------
# Swarm
# --------------------------------------------------------------------------

def set_agent_model(path: Path, model: str) -> None:
    txt = path.read_text()
    new, n = re.subn(r"(?m)^model:.*$", f"model: {model}", txt, count=1)
    if n != 1:
        raise SystemExit(f"no model: line in {path}")
    path.write_text(new)


def child_sessions(parent: str) -> list[dict]:
    # The server ignores the parentID query filter in v2.0.16, so filter here.
    d = oc_api("GET", "/api/session", f"parentID={parent}", "limit=200") or {}
    return [s for s in d.get("data", []) if s.get("parentID") == parent]


def run_swarm(base: Path, workdir: Path, assign: dict, timeout: int, blocked_after: int) -> dict:
    dest = fresh_copy(base, workdir / "runs" / "swarm")
    for role, model in assign.items():
        set_agent_model(dest / ".opencode" / "agents" / f"genome-{role}.md", model)
    subprocess.run(["git", "commit", "-qam", "assign"], cwd=dest, stdout=subprocess.DEVNULL,
                   env={**os.environ, "GIT_AUTHOR_NAME": "b", "GIT_AUTHOR_EMAIL": "b@l",
                        "GIT_COMMITTER_NAME": "b", "GIT_COMMITTER_EMAIL": "b@l"})
    log(f"swarm: starting in {dest} with {assign}")
    timeline: list[dict] = []
    last = {"line": "", "pending_since": None}

    def tick(sid, elapsed):
        # Poll child sessions so a child blocked on an approval prompt is visible.
        # In v2.0.16 `run --auto` does not reach subagent sessions: their "ask"
        # permissions stay pending and nobody can answer them in a headless run.
        # Returns True (stop the run) once approvals have been pending for
        # `blocked_after` seconds. The harness never answers approvals itself.
        if not sid:
            return False
        snap = {"t": round(elapsed), "children": []}
        for s in child_sessions(sid):
            perms = oc_api("GET", f"/api/session/{s.get('id')}/permission") or {}
            snap["children"].append({
                "id": s.get("id"), "agent": s.get("agent"),
                "model": (s.get("model") or {}).get("id"), "outcome": s.get("outcome"),
                "pending_permissions": perms.get("data", []) or [],
            })
        timeline.append(snap)
        line = ", ".join(
            f"{c['agent']}[{c['model']}]:{c['outcome'] or 'running'}"
            + (f" PENDING-APPROVAL×{len(c['pending_permissions'])}" if c["pending_permissions"] else "")
            for c in snap["children"]) or "none"
        if line != last["line"]:
            log(f"swarm t={snap['t']}s children: {line}")
            last["line"] = line
        if any(c["pending_permissions"] for c in snap["children"]):
            last["pending_since"] = last["pending_since"] or elapsed
            if elapsed - last["pending_since"] >= blocked_after:
                log(f"swarm: child approvals pending for {blocked_after}s; stopping (blocked)")
                return True
        else:
            last["pending_since"] = None
        return False

    res = run_opencode(dest, assign["coordinator"], SWARM_PROMPT, timeout,
                       workdir / "events" / "swarm.jsonl", agent="genome-coordinator",
                       on_tick=tick)
    (workdir / "swarm-timeline.json").write_text(json.dumps(timeline, indent=2))
    if res["session"] and (res["stopped"] or res["timed_out"]):
        for s in child_sessions(res["session"]):  # interrupting the parent leaves children running
            if not s.get("outcome"):
                oc_api("POST", f"/api/session/{s.get('id')}/interrupt")
    blocked =[{"agent": c["agent"], "model": c["model"],
                "pending": [{"action": p.get("action"), "resources": p.get("resources")}
                            for p in c["pending_permissions"]]}
               for c in (timeline[-1]["children"] if timeline else []) if c["pending_permissions"]]
    out_root = dest / "outputs" / "genome-team"
    files = sorted(str(p.relative_to(dest)) for p in out_root.rglob("*") if p.is_file()) \
        if out_root.exists() else []
    kids = []
    if res["session"]:
        for s in child_sessions(res["session"]):
            sid = s.get("id")
            perms = oc_api("GET", f"/api/session/{sid}/permission") or {}
            kids.append({
                "id": sid, "agent": s.get("agent"),
                "model": (s.get("model") or {}).get("id"),
                "outcome": s.get("outcome"), "title": s.get("title"),
                "tokens_out": (s.get("tokens") or {}).get("output"),
                "pending_permissions": len(perms.get("data", []) or []),
            })
    all_text = "\n".join(res["errors"]) + "\n" + res["text"] + "\n" + \
        "\n".join(c["output"] for c in res["subagent_calls"])
    summary = {
        "assignment": assign, "wall_s": res["wall_s"], "timed_out": res["timed_out"],
        "errors": res["errors"], "tool_calls": res["tool_calls"],
        "tool_errors": res["tool_errors"], "tool_error_detail": res["tool_error_detail"],
        "subagent_calls": res["subagent_calls"], "child_sessions": kids,
        "stopped_by_harness": res["stopped"], "blocked_on_approvals": blocked,
        "files": files, "saw_403": bool(re.search(r"\b403\b|free tier can only", all_text)),
        "session": res["session"], "final_text": res["final_text"][-3000:],
        "scratch_dir": str(dest),
    }
    (workdir / "swarm-summary.json").write_text(json.dumps(summary, indent=2))
    return summary


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def table(records: list[dict], skipped: dict[str, str], models: list[str], tasks: list[str]) -> str:
    by = collections.defaultdict(list)
    for r in records:
        by[(r["model"], r["task"])].append(r)
    hdr = "| Model | " + " | ".join(f"{t} pass" for t in tasks) + \
          " | Overall | Median s | Tool errors | API errors |"
    out = [hdr, "|" + "---|" * (len(tasks) + 5)]
    for m in models:
        if m in skipped:
            out.append(f"| {m} | " + " | ".join("–" for _ in tasks) + f" | {skipped[m]} | – | – | – |")
            continue
        rs = [r for r in records if r["model"] == m]
        if not rs:
            continue
        cells = []
        for t in tasks:
            x = by[(m, t)]
            cells.append(f"{sum(r['passed'] for r in x)}/{len(x)}" if x else "–")
        npass = sum(r["passed"] for r in rs)
        med = statistics.median(r["wall_s"] for r in rs)
        te = sum(r["tool_errors"] for r in rs)
        tc = sum(r["tool_calls"] for r in rs)
        kinds = collections.Counter(k for r in rs for k in r["error_kinds"])
        ek = ", ".join(f"{k}×{v}" for k, v in sorted(kinds.items())) or "none"
        out.append(f"| {m} | " + " | ".join(cells) +
                   f" | {npass}/{len(rs)} | {med:.0f} | {te}/{tc} | {ek} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="*", help="models to test (default: Zen free list + DTU)")
    ap.add_argument("--tasks", nargs="*", default=list(TASKS), choices=list(TASKS))
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=360, help="seconds per task run")
    ap.add_argument("--jobs", type=int, default=8, help="models tested in parallel (runs per model are serial)")
    ap.add_argument("--workdir", type=Path)
    ap.add_argument("--config-model", default="opencode/big-pickle",
                    help="model written into the scratch opencode.json as default/title/summary")
    ap.add_argument("--no-swarm", action="store_true")
    ap.add_argument("--swarm-only", action="store_true")
    ap.add_argument("--swarm-timeout", type=int, default=2400)
    ap.add_argument("--blocked-after", type=int, default=300,
                    help="stop the swarm once subagent approvals have been pending this long (s)")
    for role in DEFAULT_SWARM:
        ap.add_argument(f"--{role}", default=DEFAULT_SWARM[role], help=f"swarm model for {role}")
    a = ap.parse_args()

    workdir = a.workdir or Path(tempfile.gettempdir()) / f"opencode-bakeoff-{dt.datetime.now():%Y%m%d-%H%M%S}"
    workdir = workdir.resolve()
    if REPO in workdir.parents or workdir == REPO:
        raise SystemExit("--workdir must be outside the repo")
    (workdir / "runs").mkdir(parents=True, exist_ok=True)
    (workdir / "events").mkdir(exist_ok=True)
    log(f"workdir: {workdir}")
    ver = subprocess.run(["opencode", "--version"], capture_output=True, text=True).stdout.strip()
    log(f"opencode: {ver}")

    live = live_zen_models()
    local = local_models()
    meta = {"date": dt.datetime.now().isoformat(timespec="seconds"), "opencode": ver,
            "zen_live": live, "opencode_models": local}
    (workdir / "meta.json").write_text(json.dumps(meta, indent=2))
    log("Zen live free: " + ", ".join(m for m in live if m.endswith("-free") or m == "big-pickle"))
    log("opencode models (opencode/, dtu/): " +
        ", ".join(m for m in local if m.startswith(("opencode/", "dtu/"))))

    truth = ground_truth(REPO / DATA_REL)
    (workdir / "truth.json").write_text(json.dumps(truth, indent=2))
    base = make_base(workdir, a.config_model)

    models = a.models or (ZEN_CANDIDATES + DTU_CANDIDATES)
    skipped: dict[str, str] = {}
    for m in models:
        mid = m.split("/", 1)[1]
        if "contributor" in mid or mid.startswith("jev-"):
            skipped[m] = "excluded (contributor / not chat)"
        elif m.startswith("opencode/") and live and mid not in live:
            skipped[m] = "not run (not in live Zen list)"
        elif m.startswith("dtu/") and not dtu_reachable(m):
            skipped[m] = "not run (offline)"
    for m, why in skipped.items():
        log(f"{m}: {why}")

    records: list[dict] = []
    if not a.swarm_only:
        todo = [m for m in models if m not in skipped]

        def per_model(m: str) -> list[dict]:
            recs = []
            for rep in range(1, a.reps + 1):
                for t in a.tasks:
                    recs.append(one_task_run(base, workdir, m, t, rep, truth, a.timeout))
                    with (workdir / "results.jsonl").open("a") as fh:
                        fh.write(json.dumps(recs[-1]) + "\n")
            return recs

        with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
            for recs in ex.map(per_model, todo):
                records.extend(recs)
        print()
        print(table(records, skipped, models, a.tasks))
        print()

    if not a.no_swarm:
        assign = {r: getattr(a, r) for r in DEFAULT_SWARM}
        s = run_swarm(base, workdir, assign, a.swarm_timeout, a.blocked_after)
        print("Swarm:", json.dumps({k: s[k] for k in
              ("wall_s", "timed_out", "stopped_by_harness", "blocked_on_approvals", "errors",
               "saw_403", "tool_errors", "files", "child_sessions")}, indent=2))
    log(f"details: {workdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
