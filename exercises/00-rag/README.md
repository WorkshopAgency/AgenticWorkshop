# Exercise 0 — RAG: give the model the documents

| | |
|---|---|
| **Time** | 15 min |
| **Model** | `dtu/mistral` (Mistral Nemo 12B) for the answers, and an embedding model at DTU for search |
| **Needs** | `scripts/check-setup.sh` passed. Python 3.10+, nothing to install. Nothing from other modules |
| **You'll learn** | What retrieval-augmented generation (RAG) does at each step, and how to check a cited answer |
| **Done when** | You have a cited answer, found the cited text with `grep`, and compared k=1 with k=8 |
| **If stuck** | `/halp 00-rag <what you tried>` |

## Why RAG

A language model only knows what it saw in training, plus whatever is in the
prompt. Ask it about something it never saw, and it will still answer,
fluently and confidently, because producing plausible text is all it does.

**Retrieval-augmented generation (RAG)** gives the model the relevant part of
your own documents together with the question, and asks it to answer from
those and say where the answer came from. It is how most "chat with your
documents" tools work, and the same idea sits inside agents that search
before they answer.

The documents here are the guides for **nf-core/rnaseq 3.27.0**, released in
September 2026, so the model has not seen them. Together they are about
55,000 tokens, more than three times what Mistral's context window holds in
this workshop. You cannot paste them all in; you have to choose which parts
to send. We use a small model on purpose: the difference between answering
with and without the documents is easy to see.

```
 corpus/*.md ──chunk──► ~380 pieces ──embed──► index
                                                 │
 your question ──────────────search──────► the k best pieces
                                                 │
            prompt = rules + pieces [c1] [c2] ... + question
                                                 │
                              Mistral ──► answer with [c..] citations
                                                 │
                                  you ──► grep the cited text
```

## Before you start

This exercise runs in an ordinary terminal, not in OpenCode: you call the
model directly, so you can see every step that an agent would normally hide.
Run all commands from the workshop folder.

Everything goes through one script, [`rag.py`](rag.py). It prints what each
step did. Open it: it is plain Python, one function per step. The questions
are in [`questions.md`](questions.md); try them before you read the answers.

**Or as a notebook, inside OpenCode (optional).** The same steps are cells in
[`rag_notebook.py`](rag_notebook.py), which you run one by one in a notebook
panel next to the chat. Install the plugin from a terminal in the workshop
folder, then quit OpenCode (`ctrl+c`) and start it again:

```bash
git clone -q --depth 1 --branch v0.1.1 https://github.com/dskanakoglou/opencode-notebook .opencode/plugins/opencode-notebook
```

In a chat, type `/notebook exercises/00-rag/rag_notebook.py`. Select a cell
with `↑` `↓` and run it with `r`; the selected cell shows its whole output.
Follow the steps below for what to look for. You can also mark a cell with
`space` and ask the agent about it: "Is the cited text really in the pieces
of the cell I marked?"

## 1. Ask without the documents (2 min)

**Do:**

```bash
python3 exercises/00-rag/rag.py ask "When strandedness is set to auto, how does nf-core/rnaseq decide, and with which default thresholds?" --no-rag
```

**Look for:** the script prints the exact prompt (only your question), then
the answer. Does the model sound sure? Does it name numbers? Keep the answer;
you will compare it with step 4.

**Why:** this is the baseline. Whatever it says here comes from training
alone, and the model cannot know this release.

## 2. Cut the documents into pieces (2 min)

**Do:**

```bash
python3 exercises/00-rag/rag.py chunk
```

**Look for:** open `outputs/00-rag/chunks.jsonl`. Each line is one piece of at
most 800 characters, with an id (`c1`, `c2`, …), the file it came from, and
where in that file.

**Why:** a model can only be given a few pieces, so the documents are cut
into pieces small enough to send. Neighbouring pieces overlap, so a sentence
cut at a boundary is still whole in one of them. How you cut matters: too
small and an answer is split across pieces, too large and few fit in the
prompt.

## 3. Search, and read before you ask (3 min)

**Do:**

```bash
python3 exercises/00-rag/rag.py search "When strandedness is set to auto, which default thresholds are used?" -k 3
```

Then the same search with `--lexical` added.

**Look for:** read the three pieces **before** asking the model anything. Is
the answer, two thresholds, in one of them? In which position? Does
`--lexical` give a different order?

**Why:** search uses **embeddings**: each piece, and your question, becomes a
list of numbers that captures its meaning, and pieces close in meaning to
the question come first. `--lexical` instead counts matching words, like a
search engine. If the answer is not in the retrieved pieces, no model can
give it from them.

## 4. Ask with the documents, then check the citation (3 min)

**Do:**

```bash
python3 exercises/00-rag/rag.py ask "When strandedness is set to auto, how does nf-core/rnaseq decide, and with which default thresholds?" -k 3
```

Then check one citation yourself:

```bash
grep -n "stranded_threshold" exercises/00-rag/corpus/usage.md
```

**Look for:** the printed prompt: the rules, the pieces with their ids, then
your question. Does the answer cite a piece, like `[c12]`? Is the cited text
really there in the file? Compare it with your answer from step 1.

**Why:** the model is told to answer only from the pieces, to cite them, and
to say so when they are not enough. A citation turns "trust me" into
something you can check in seconds.

## 5. One piece or eight? (5 min)

**Do:** half the room uses `-k 1`, the other half `-k 8`. Ask questions 4 and
5 from `questions.md`:

```bash
python3 exercises/00-rag/rag.py ask "Which Salmon version does release 3.27.0 use, and what changed in quantification?" -k 1
python3 exercises/00-rag/rag.py ask "What is the minimum sequencing depth per sample that nf-core/rnaseq recommends?" -k 8
```

**Look for:** compare with your neighbour. Did one piece contain the Salmon
versions at all, or did the model answer anyway? Question 5 has no answer in
the documents: did eight pieces give the model enough loosely related text to
invent one?

**Why:** k, the number of pieces, is a trade-off. Too few can miss the answer
or half of it; too many add noise and use up the context window.

## Optional: let an agent search

**Do:** [`skill/corpus-search/SKILL.md`](skill/corpus-search/SKILL.md) tells
an OpenCode agent to run the search itself and cite the pieces. Install it:

```bash
mkdir -p .opencode/skills && cp -r exercises/00-rag/skill/corpus-search .opencode/skills/
```

Run `opencode reload`, start a new chat in OpenCode and ask one of the
questions.

**Why:** with `ask`, you decided what to search for. An agent decides itself,
and can search again with other words when the first results are poor. That
is more powerful, and harder to check.

If the embedding model is not available, `rag.py` says so and searches by
matching words instead. Everything above still works.

## What to notice

- Without the documents, nothing stops the model from making an answer up,
  and a made-up answer sounds like a real one.
- With the documents, the answer can only be as good as the pieces you
  retrieved. Read those first.
- A citation is a claim. Checking it with `grep` takes seconds.
- k is a trade-off: too few pieces miss things, too many add noise.

**Discuss with your neighbour:**

1. Which of your own documents (protocols, lab notes, papers) would you want
   to search this way, and what would you be afraid it gets wrong?
2. Your colleague's RAG tool answers correctly but cites the wrong piece. Is
   that a problem?
3. Would you rather use a big model without your documents, or a small model
   with them?

The documents are © the nf-core/rnaseq team, MIT licence
([`corpus/LICENSE-nf-core-rnaseq`](corpus/LICENSE-nf-core-rnaseq)), from
[nf-core/rnaseq 3.27.0](https://github.com/nf-core/rnaseq/tree/3.27.0).

Next: [Exercise 1 — Skills](../01-skills/README.md).
