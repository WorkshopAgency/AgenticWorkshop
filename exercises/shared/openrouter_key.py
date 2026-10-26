"""The workshop key (Exercise 0c): read it, and say plainly what is wrong with it."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FILE = ROOT / ".openrouter-key"
PLACEHOLDERS = ("YOUR-KEY", "PASTE-THE-KEY-HERE")


def read():
    """The key from OPENROUTER_API_KEY or .openrouter-key, or "" when there is none."""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key and FILE.exists():
        key = FILE.read_text().strip()
    return key


def problem():
    """What is wrong with the key, as one thing to do, or None. Never shows the key."""
    # A file named after the key means the key and the file name were swapped.
    if any(ROOT.glob("sk-or-v1-*")):
        return ("A file in the workshop folder is named after your key: the key and the file "
                "name were swapped. Fix it, without showing the key, with: "
                "echo sk-or-v1-* > .openrouter-key && rm sk-or-v1-*")
    key = read()
    if not key:
        return "No workshop key yet: see Exercise 0c."
    if key in PLACEHOLDERS:
        return (f".openrouter-key still holds {key}. Run: echo YOUR-KEY > .openrouter-key, "
                "with your key in place of YOUR-KEY.")
    if not key.startswith("sk-or-"):
        return "That is not an OpenRouter key: they start with sk-or-v1-. Check .openrouter-key (Exercise 0c)."
    return None
