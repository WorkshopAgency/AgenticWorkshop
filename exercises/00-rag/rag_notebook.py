# %% [markdown]
# # Exercise 0 — RAG as a notebook
#
# The same five steps as the README, one cell each, with the same `rag.py`.
# Open it with `/notebook exercises/00-rag/rag_notebook.py`; select a cell
# with the arrow keys and run it with `r`. Read the README's **Look for** and
# **Why** for each step as you go.

# %% Setup
import os
import subprocess
import sys

# The DTU models down? Remove the # below, then restart the kernel with k.
# os.environ["RAG_OPENCODE"] = "opencode/glm-5.3-flash-free"

sys.path.insert(0, "exercises/00-rag")
import rag

QUESTION = ("When strandedness is set to auto, how does nf-core/rnaseq decide, "
            "and with which default thresholds?")


def step(*args):
    """Run one rag.py command, exactly as in the terminal."""
    sys.argv = ["rag.py", *args]
    try:
        rag.main()
    except SystemExit as stop:
        if stop.code not in (0, None):
            print(stop.code)


print("Answers from:", rag.RAG_OPENCODE or f"{rag.RAG_MODEL} at {rag.RAG_URL}")

# %% 1. Ask without the documents
step("ask", QUESTION, "--no-rag")

# %% 2. Cut the documents into pieces
step("chunk")

# %% 3. Search, and read before you ask
step("search", "When strandedness is set to auto, which default thresholds are used?", "-k", "3")

# %% 3b. The same search by matching words
step("search", "When strandedness is set to auto, which default thresholds are used?", "-k", "3", "--lexical")

# %% 4. Ask with the documents
step("ask", QUESTION, "-k", "3")

# %% 4b. Check the citation yourself
print(subprocess.run(["grep", "-n", "stranded_threshold", "exercises/00-rag/corpus/usage.md"],
                     capture_output=True, text=True).stdout)

# %% 5a. One piece
step("ask", "Which Salmon version does release 3.27.0 use, and what changed in quantification?", "-k", "1")

# %% 5b. Eight pieces
step("ask", "What is the minimum sequencing depth per sample that nf-core/rnaseq recommends?", "-k", "8")
