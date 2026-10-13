# Exercise 0 — RAG: give the model the documents

| | |
|---|---|
| **Time** | 15 min |
| **Model** | `dtu/mistral` (Mistral Nemo 12B) for the answers, and an embedding model at DTU for search |
| **Needs** | `scripts/check-setup.sh` passed. Python 3.10+, nothing to install. Nothing from other modules |
| **You'll learn** | What retrieval-augmented generation (RAG) does at each step, and how to check a cited answer |
| **Done when** | You have a cited answer, found the cited text with `grep`, and compared k=1 with k=8 |
| **If stuck** | `/halp 00-rag <what you tried>` |

A language model only knows what it saw in training, plus whatever you put in
the prompt. RAG puts the relevant part of your documents in the prompt.

The documents here are the guides for **nf-core/rnaseq 3.27.0**, released in
September 2026, so the model has not seen them. Together they are about
55,000 tokens, more than three times what Mistral's context window holds in
this workshop. You cannot paste them in, so you have to choose which parts
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

Everything runs through one script, [`rag.py`](rag.py). It prints what each
step did. Open it: it is plain Python, one function per step. The questions
are in [`questions.md`](questions.md); try them before you read the answers.

## 1. Ask without the documents (2 min)

```bash
python3 exercises/00-rag/rag.py ask "When strandedness is set to auto, how does nf-core/rnaseq decide, and with which default thresholds?" --no-rag
```

The script prints the exact prompt, which is only your question, then the
answer. Does the model sound sure? Is it right?

## 2. Cut the documents into pieces (2 min)

```bash
python3 exercises/00-rag/rag.py chunk
```

Open `outputs/00-rag/chunks.jsonl`. Each line is one piece of at most 800
characters, with an id (`c1`, `c2`, …), the file it came from and where in
that file. Neighbouring pieces overlap, so a sentence cut at a boundary is
still whole in one of them.

## 3. Search, and read before you ask (3 min)

```bash
python3 exercises/00-rag/rag.py search "When strandedness is set to auto, which default thresholds are used?" -k 3
```

Read the three pieces **before** asking the model anything. Is the answer in
them? If not, no model can give it from these. Add `--lexical` to search by
matching words instead of meaning, and compare the order.

## 4. Ask with the documents, then check the citation (3 min)

```bash
python3 exercises/00-rag/rag.py ask "When strandedness is set to auto, how does nf-core/rnaseq decide, and with which default thresholds?" -k 3
```

Read the prompt it prints: the rules, the pieces with their ids, then your
question. The model is told to answer only from the pieces, cite them like
`[c12]`, and say so when they are not enough. Then check one citation
yourself:

```bash
grep -n "stranded_threshold" exercises/00-rag/corpus/usage.md
```

## 5. One piece or eight? (5 min)

Half the room uses `-k 1`, the other half `-k 8`. Ask questions 4 and 5 from
`questions.md`:

```bash
python3 exercises/00-rag/rag.py ask "Which Salmon version does release 3.27.0 use, and what changed in quantification?" -k 1
python3 exercises/00-rag/rag.py ask "What is the minimum sequencing depth per sample that nf-core/rnaseq recommends?" -k 8
```

Compare with your neighbour. Did one piece contain the Salmon versions at
all, or did the model answer anyway? Did eight pieces give the model enough
loosely related text to invent an answer to a question the documents do not
answer?

## Optional: let an agent search

[`skill/corpus-search/SKILL.md`](skill/corpus-search/SKILL.md) tells an
OpenCode agent to run the search itself and cite the pieces. Install it:

```bash
mkdir -p .opencode/skills && cp -r exercises/00-rag/skill/corpus-search .opencode/skills/
```

Run `opencode reload`, start a new chat and ask one of the questions. Unlike
`ask`, the agent decides what to search for, and can search again with other
words.

**What to notice:** without the documents nothing stops the model from making
an answer up. With them, the answer can only be as good as the pieces you
retrieved, so read those first. A citation is a claim; checking it with
`grep` takes seconds. And k is a trade-off: too few pieces can miss half of
the story, too many add noise.

If the embedding model is not available, `rag.py` says so and searches by
matching words instead. Everything above still works.

The documents are © the nf-core/rnaseq team, MIT licence
([`corpus/LICENSE-nf-core-rnaseq`](corpus/LICENSE-nf-core-rnaseq)), from
[nf-core/rnaseq 3.27.0](https://github.com/nf-core/rnaseq/tree/3.27.0).

Next: [Exercise 1 — Skills](../01-skills/README.md).
