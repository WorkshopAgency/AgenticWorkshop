"""Create a new, empty run folder for an agent team and print its path.

    python3 exercises/03-agents/new_run.py              outputs/genome-team/run-...
    python3 exercises/03-agents/new_run.py penguin-team outputs/penguin-team/run-...

The time and the four letters come from here, not from the model: models
guess both badly, and a reused folder mixes two runs.
"""
import re
import secrets
import string
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
team = sys.argv[1] if len(sys.argv) > 1 else "genome-team"
if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", team):
    raise SystemExit("Use a short lowercase team name, such as penguin-team.")
letters = "".join(secrets.choice(string.ascii_lowercase) for _ in range(4))
run = ROOT / "outputs" / team / f"run-{time.strftime('%Y%m%d-%H%M')}-{letters}"
run.mkdir(parents=True)
print(run.relative_to(ROOT))
