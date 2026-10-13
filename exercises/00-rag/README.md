# Exercise 00 — RAG, every stage visible

| | |
|---|---|
| **Time** | 15 minutes |
| **Model** | `dtu/mistral` (Mistral Nemo 12B) for answers, `dtu/embed` for embeddings (planned) |
| **Needs** | Python 3.10+ (standard library only), a terminal in the workshop folder |
| **You'll learn** | What retrieval-augmented generation (RAG) actually does at each stage, and how to check a cited answer yourself |
| **Done when** | You have a cited answer, have found the cited text in the corpus with `grep`, and have compared k=1 with k=8 |
| **If stuck** | `/halp 00-rag` |

> **Corpus status:** `corpus/` currently contains a **PLACEHOLDER** corpus (two
> invented handbooks) used for testing. The real corpus will replace it; see
> `CORPUS.md`. Question numbers below refer to the answer key in `questions.md`.

The model is deliberately a small one (12B parameters), so the difference
between answering with and without documents is easy to see.

## The pipeline

```
 corpus/*.md ──chunk──► chunks.jsonl ──embed──► index.json
                                                    │
 your question ──embed (or BM25 keywords)──► retrieve top-k chunks
                                                    │
                        augment prompt: rules + [c2] [c4] ... + question
                                                    │
                                    generate (mistral) ──► answer
                                                    │
                          cite [c4] ──► verify: grep the cited text in corpus/
```

Everything runs through one script, `rag.py`, which prints what each stage
did. Open it: it is about 350 lines of plain Python, one function per step.

## Where files go

| File | Where | Why |
|---|---|---|
| `chunks.jsonl`, `index.json` you build | `outputs/00-rag/` | Your own work; `outputs/` is ignored by git |
| `answers.jsonl` (log of every `ask`) | `outputs/00-rag/` | So you can compare answers later |
| Prebuilt `index.json` (to be shipped) | `exercises/00-rag/` | Used only if you have not built your own |

`search` uses `outputs/00-rag/index.json` if it exists, otherwise the shipped
`exercises/00-rag/index.json`. An index is used only if it was built from the
same chunks you have now (the script checks a fingerprint). If you re-chunk
with other settings, run `embed` again.

If the embeddings endpoint is unreachable, or there is no matching index,
`search` and `ask` switch to **BM25 keyword search** and print a `NOTICE:`
line saying so. You can also ask for BM25 directly with `--lexical`.

## Steps

Run every command from the workshop folder.

### 1. Ask without documents (2 min)

```bash
python3 exercises/00-rag/rag.py ask "<question 1 from questions.md>" --no-rag
```

The script prints the exact prompt (here, only your question), then the
answer. The corpus contains facts the model cannot know. Is the answer
confident? Is it right?

### 2. Chunk the corpus (2 min)

```bash
python3 exercises/00-rag/rag.py chunk
```

Open `outputs/00-rag/chunks.jsonl`. Each line is one chunk: an `id` (`c1`,
`c2`, ...), the `source` file, the character span `start`–`end` in that file,
and the `text`. Neighbouring chunks overlap by about 150 characters so that a
sentence cut at a boundary still appears whole in one of them.

### 3. Retrieve, and read before you ask (3 min)

```bash
python3 exercises/00-rag/rag.py search "<question 1>" -k 3
```

Read the three chunks **before** asking the model anything. Does the answer
appear in them? If not, no model can give it from these chunks. Try
`--lexical` and compare the ranking.

### 4. Ask with documents, then verify the citation (3 min)

```bash
python3 exercises/00-rag/rag.py ask "<question 1>" -k 3
```

Read the printed prompt: the rules, the chunks with their ids, then the
question. The model is told to answer only from the evidence, cite ids like
`[c12]`, and say "not in the documents" when the evidence is not enough.

After the answer, the script lists each cited chunk and its file. It warns if
the answer cites an id that was not in the prompt. Then check it yourself:

```bash
grep -n "a short phrase from the cited chunk" exercises/00-rag/corpus/<file>
```

Use a short phrase: lines in the files may wrap mid-sentence.

### 5. Split the room: k=1 versus k=8 (4 min)

Half the room runs `-k 1`, the other half `-k 8`, on the **conflict** and
the **unanswerable** questions from `questions.md`:

```bash
python3 exercises/00-rag/rag.py ask "<conflict question>" -k 1
python3 exercises/00-rag/rag.py ask "<unanswerable question>" -k 8
```

Compare with your neighbour. Which chunks did each half retrieve? Did k=1
see both versions of the conflicting fact? Did k=8 bring in text that let
the model guess an answer to the unanswerable question?

Example from the placeholder corpus, default chunking, BM25: for question P2
("How long are moss cores dried before weighing?"), k=1 retrieves only the
2019 rule (`[c2]`, 36 hours); k=3 also retrieves the 2024 rule (`[c4]`, 48 hours).

### 6. Optional: agentic RAG with a skill

`skill/corpus-search/SKILL.md` tells an OpenCode agent to run `rag.py search`
itself, quote chunk ids and say when the evidence is insufficient. Install it
with one command:

```bash
mkdir -p .opencode/skills && cp -r exercises/00-rag/skill/corpus-search .opencode/skills/
```

Exit and reopen OpenCode so it finds the skill, then ask one of the questions
in a chat. Approve the `python3 ... search` command when asked. Unlike `ask`,
the agent decides what to search for and can search again with different
words.

## What to notice

- Without documents, nothing stops the model from inventing an answer.
- Retrieval quality limits answer quality: check the chunks first.
- A citation is a claim. Checking it with `grep` takes seconds.
- k is a trade-off. Too few chunks can miss half of a conflict; too many add
  noise and use up the context window.

## Verification status

**Verified** (against a local mock server that imitates the DTU endpoints,
13 October 2026): chunking (`.md` and `.txt`; every chunk equals its file
span), batched embedding with vectors scaled to length 1, cosine and BM25
search, the BM25 fallback with a `NOTICE:` when embedding fails or the index
is missing or stale, the exact prompt printed matching the prompt sent,
`--no-rag` sending only the question, and the warning for a cited id that was
not in the prompt. The BM25 retrievals quoted in step 5 were run on the
placeholder corpus.

**Not yet verified** (needs the live DTU models):
- Mistral's actual answers, with or without documents. The "confident wrong
  answer" in step 1 is the expected behaviour, not an observed one.
- The `embed` endpoint (`https://teaching.healthtech.dtu.dk/workshop/embed/embeddings`),
  which does not exist yet, its model name and vector size, and timing.
- Whether the DTU gateway passes `/embeddings` requests through.
- The `corpus-search` skill in a live OpenCode session (whether the agent
  picks it up, runs the search and cites ids as instructed).

## Settings

| Variable | Default | Meaning |
|---|---|---|
| `DTU_BASE` | `https://teaching.healthtech.dtu.dk/workshop` | Root of the model URLs |
| `RAG_MODEL` | `mistral` | Chat model; requests go to `$DTU_BASE/$RAG_MODEL/chat/completions` |
| `EMBED_MODEL` | `embed` | Embedding model; requests go to `$DTU_BASE/$EMBED_MODEL/embeddings` |
| `RAG_URL`, `EMBED_URL` | derived from the above | Full base URL, for any other OpenAI-compatible server |

`python3 exercises/00-rag/rag.py <command> --help` lists every flag.
`scripts/check-setup.sh --module 00-rag` checks whether the embedding model answers.
