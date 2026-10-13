#!/usr/bin/env bash
# Check that this laptop is ready for the workshop, or for one module.
#
#   scripts/check-setup.sh                      shared setup (run this first)
#   scripts/check-setup.sh --module 03-mcp      also that module's own needs
#
# Modules: 00-rag 01-skills 02-agents 03-mcp 04-decide 05-safety
# Works on macOS, Linux and Windows WSL2. Only reads; changes nothing.

PIN="2.0.16"   # OpenCode version the material was rehearsed on
DTU="https://teaching.healthtech.dtu.dk/workshop"
ZEN="https://opencode.ai/zen/v1"

fails=0
ok()   { printf '  \033[32m✅\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m❌\033[0m %s\n' "$1"; [ -n "$2" ] && printf '     → %s\n' "$2"; fails=$((fails+1)); }
warn() { printf '  \033[33m⚠️ \033[0m %s\n' "$1"; [ -n "$2" ] && printf '     → %s\n' "$2"; }
have() { command -v "$1" >/dev/null 2>&1; }
# run a command with a time limit (macOS has no `timeout`)
limit() { local s=$1; shift; perl -e 'alarm shift; exec @ARGV' "$s" "$@"; }
http() { curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$@"; }

dtu_model() {   # $1 = model id
  if [ "$(http "$DTU/$1/health")" = "200" ]; then ok "DTU model $1 answers"
  else warn "DTU model $1 is not answering" "use a free OpenCode model instead and tell an organiser"; fi
}

shared() {
  echo "Shared setup"
  if [ -f opencode.json ] && [ -d .opencode/agents ]; then ok "in the workshop folder"
  else bad "not in the workshop folder" "cd into the folder that contains opencode.json"; fi

  if have opencode; then
    v=$(opencode --version 2>/dev/null | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ "$v" = "$PIN" ]; then ok "OpenCode $v"
    else warn "OpenCode $v (the workshop was tested on $PIN)" "opencode upgrade $PIN"; fi
  else bad "OpenCode is not installed" "see the README, Install section"; fi

  if have python3 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
    ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
  else bad "Python 3.10 or newer is missing" "install python3 (WSL: sudo apt install python3)"; fi

  if [ "$(http "$ZEN/models")" = "200" ]; then ok "free OpenCode models reachable"
  else bad "cannot reach opencode.ai" "check the network / Wi-Fi"; fi
  dtu_model qwen36
}

module() {
  echo "Module $1"
  case "$1" in
    00-rag)
      dtu_model mistral
      if [ "$(http "$DTU/embed/health")" = "200" ]; then ok "embedding model answers"
      else warn "embedding model is not answering" "rag.py falls back to word matching (--lexical)"; fi
      ;;
    01-skills)
      ok "nothing extra needed"
      ;;
    02-agents)
      models=$(curl -s --max-time 15 "$ZEN/models")
      for f in .opencode/agents/genome-*.md; do
        m=$(sed -n 's/^model: *opencode\///p' "$f")
        [ -z "$m" ] && continue
        case "$models" in *"\"$m\""*) ok "$(basename "$f" .md) model $m is live" ;;
          *) bad "$(basename "$f" .md) model $m is not offered any more" "tell an organiser" ;; esac
      done
      ;;
    03-mcp)
      if have uv; then ok "uv $(uv --version | cut -d' ' -f2)"
      else bad "uv is missing" "curl -LsSf https://astral.sh/uv/install.sh | sh"; fi
      if [ -f exercises/03-mcp/data/workshop.duckdb ]; then ok "database built"
      else warn "database not built yet" "step 1 of the exercise builds it"; fi
      if have opencode && limit 30 opencode mcp list 2>/dev/null | grep -i duckdb | grep -qi connected; then
        ok "duckdb MCP server connected"
      else warn "duckdb MCP server not connected yet" "type /mcps in OpenCode and switch on duckdb"; fi
      ;;
    04-decide)
      body='{"model":"qwen36","messages":[{"role":"user","content":"Answer A or B. Answer:"}],"max_tokens":1,"temperature":0,"logprobs":true,"top_logprobs":5}'
      out=$(curl -s --max-time 30 -H 'content-type: application/json' -d "$body" "$DTU/qwen36/chat/completions")
      if printf '%s' "$out" | python3 -c 'import sys,json; c=json.load(sys.stdin)["choices"][0]; sys.exit(0 if c["logprobs"]["content"][0]["top_logprobs"] else 1)' 2>/dev/null
      then ok "qwen36 returns token probabilities"
      else bad "qwen36 returned no token probabilities" "tell an organiser: decide.py needs logprobs"; fi
      ;;
    05-safety)
      if [ -f .opencode/agents/safe-analyst.md ]; then ok "safe-analyst agent present"
      else bad "safe-analyst agent missing" "update your copy: git pull, or download the ZIP again"; fi
      ;;
    *) bad "unknown module '$1'" "choose one of: 00-rag 01-skills 02-agents 03-mcp 04-decide 05-safety" ;;
  esac
}

shared
if [ "$1" = "--module" ] && [ -n "$2" ]; then echo; module "$2"; fi
echo
if [ "$fails" -eq 0 ]; then echo "Ready. (⚠️ lines are worth reading but do not block you.)"
else echo "$fails problem(s) above. Fix the ❌ lines, or ask: /halp setup"; exit 1; fi
