#!/usr/bin/env bash
# Check that this laptop is ready for the workshop, or for one module.
#
#   scripts/check-setup.sh                      shared setup (run this first)
#   scripts/check-setup.sh --module 04-mcp      also that module's own needs
#
# Modules: 00-plugins 01-rag 02-skills 03-agents 04-mcp 05-decide 06-safety
# Works on macOS, Linux and Windows WSL2. Only reads; changes nothing.

MIN="2.0.29"   # oldest OpenCode the workshop plugins were tested with
ZEN="https://opencode.ai/zen/v1"

fails=0
ok()   { printf '  \033[32m✅\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m❌\033[0m %s\n' "$1"; [ -n "$2" ] && printf '     → %s\n' "$2"; fails=$((fails+1)); }
warn() { printf '  \033[33m⚠️ \033[0m %s\n' "$1"; [ -n "$2" ] && printf '     → %s\n' "$2"; }
have() { command -v "$1" >/dev/null 2>&1; }
# run a command with a time limit (macOS has no `timeout`)
limit() { local s=$1; shift; perl -e 'alarm shift; exec @ARGV' "$s" "$@"; }
http() { curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$@"; }

plugin() {      # $1 = folder in .opencode/plugins
  if [ -f ".opencode/plugins/$1/tui.tsx" ]; then ok "plugin $1 installed"
  else bad "plugin $1 is not installed" "Exercise 0, step 2"; fi
}
key() {         # the workshop key, tested with Exercise 1's own code
  if [ ! -s .openrouter-key ] && [ -z "$OPENROUTER_API_KEY" ]; then
    bad "no workshop key" "Exercise 0, step 3: put it in .openrouter-key"
  elif limit 40 python3 exercises/01-rag/rag.py 2>&1 | grep -q "key works"; then ok "the workshop key works"
  else bad "the workshop key was refused or OpenRouter is unreachable" "check .openrouter-key, then tell an organiser"; fi
}

shared() {
  echo "Shared setup"
  if [ -f opencode.json ] && [ -d .opencode/agents ]; then ok "in the workshop folder"
  else bad "not in the workshop folder" "cd into the folder that contains opencode.json"; fi

  if have opencode; then
    v=$(opencode --version 2>/dev/null | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    latest=$(curl -s --max-time 10 https://registry.npmjs.org/@opencode%2fcli/latest \
             | python3 -c 'import sys,json; print(json.load(sys.stdin)["version"])' 2>/dev/null)
    older() { [ "$1" != "$2" ] && [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -1)" = "$1" ]; }
    if older "$v" "$MIN"; then bad "OpenCode $v is too old" "opencode upgrade"
    elif [ -n "$latest" ] && older "$v" "$latest"; then warn "OpenCode $v; $latest is out" "opencode upgrade"
    else ok "OpenCode $v"; fi
  else bad "OpenCode is not installed" "README, Quick start step 1"; fi

  if have python3 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
    ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
  else bad "Python 3.10 or newer is missing" "README, Quick start step 1: uv python install 3.12 --default"; fi

  if have uv; then ok "uv $(uv --version | cut -d' ' -f2)"
  else bad "uv is missing" "README, Quick start step 1"; fi

  if have git; then ok "git $(git --version | cut -d' ' -f3)"
  else warn "git is missing" "README, Quick start step 1; without it, use the ZIP downloads"; fi

  if [ "$(http "$ZEN/models")" = "200" ]; then ok "free OpenCode models reachable"
  else bad "cannot reach opencode.ai" "check the network / Wi-Fi"; fi
}

module() {
  echo "Module $1"
  case "$1" in
    00-plugins)
      if have git; then ok "git $(git --version | cut -d' ' -f3)"
      else warn "git is missing" "download the plugin ZIPs instead, as the README says"; fi
      if have uv; then ok "uv $(uv --version | cut -d' ' -f2), which starts the notebook's Python"
      else bad "uv is missing" "curl -LsSf https://astral.sh/uv/install.sh | sh"; fi
      plugin opencode-sidebar-plus
      plugin opencode-notebook
      key
      ;;
    01-rag)
      plugin opencode-notebook
      if have uv; then ok "uv, which starts the notebook's Python"
      else bad "uv is missing" "curl -LsSf https://astral.sh/uv/install.sh | sh"; fi
      key
      ;;
    02-skills)
      ok "nothing extra needed for 2a-2f"
      if [ -f .opencode/plugins/opencode-notebook/tui.tsx ]; then ok "notebook plugin, for the optional extra"
      else warn "the optional extra needs the notebook plugin" "Exercise 0, step 2"; fi
      ;;
    03-agents)
      models=$(curl -s --max-time 15 "$ZEN/models")
      for f in .opencode/agents/genome-*.md; do
        m=$(sed -n 's/^model: *opencode\///p' "$f")
        [ -z "$m" ] && continue
        case "$models" in *"\"$m\""*) ok "$(basename "$f" .md) model $m is live" ;;
          *) bad "$(basename "$f" .md) model $m is not offered any more" "tell an organiser" ;; esac
      done
      ;;
    04-mcp)
      if have uv; then ok "uv $(uv --version | cut -d' ' -f2)"
      else bad "uv is missing" "curl -LsSf https://astral.sh/uv/install.sh | sh"; fi
      if [ -f exercises/04-mcp/data/workshop.duckdb ]; then ok "database built"
      else warn "database not built yet" "step 1 of the exercise builds it"; fi
      if have opencode && limit 30 opencode mcp list 2>/dev/null | grep -i duckdb | grep -qi connected; then
        ok "duckdb MCP server connected"
      else warn "duckdb MCP server not connected yet" "type /mcps in OpenCode and switch on duckdb"; fi
      ;;
    05-decide)
      key
      if limit 90 python3 exercises/05-decide/decide.py --state "A bar chart of three values." --json >/dev/null 2>&1
      then ok "the decision model returns token probabilities"
      else bad "decide.py got no token probabilities" "run it once to see the message, then tell an organiser"; fi
      ;;
    06-safety)
      if [ -f .opencode/agents/safe-analyst.md ]; then ok "safe-analyst agent present"
      else bad "safe-analyst agent missing" "update your copy: git pull, or download the ZIP again"; fi
      ;;
    *) bad "unknown module '$1'" "choose one of: 00-plugins 01-rag 02-skills 03-agents 04-mcp 05-decide 06-safety" ;;
  esac
}

shared
if [ "$1" = "--module" ] && [ -n "$2" ]; then echo; module "$2"; fi
echo
if [ "$fails" -eq 0 ]; then echo "Ready. (⚠️ lines are worth reading but do not block you.)"
else echo "$fails problem(s) above. Fix the ❌ lines, or ask: /halp setup"; exit 1; fi
