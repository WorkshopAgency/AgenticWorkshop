# Corpus requirements for Exercise 00 (RAG)

The real corpus has **not been chosen yet**. `corpus/` currently holds a
**PLACEHOLDER** corpus: two invented "Glimmerfen Moss Station" handbooks,
used only to test `rag.py`. Replace them before the workshop.

## What the real corpus must provide

- [ ] **Openly licensed.** Redistribution in a public repository is allowed
      (for example CC BY, CC0 or public domain). Record the licence below.
- [ ] **Longer than about 16k tokens** (roughly 60,000+ characters), so it
      does not fit in Mistral Nemo's 16,384-token context. Retrieval must be
      necessary, not optional.
- [ ] **Facts the models cannot know.** Recent, local or niche material, so
      the `--no-rag` answer is wrong or invented rather than recalled.
- [ ] **One version conflict.** Two passages that give different values for
      the same fact (for example an old and a revised protocol), so `k=1`
      and `k=8` can give different answers.
- [ ] **One unanswerable question.** A natural question whose answer is not
      in the corpus, so the correct reply is "not in the documents".
- [ ] **Plain text.** `.md` or `.txt` files in `corpus/`. Convert PDFs or
      HTML first and check the text by eye.
- [ ] **No personal or confidential data.** Participants may also send the
      text to external models.

## Record for each file

| File | Source (URL or citation) | Licence | Version / date of the text | Date retrieved |
|---|---|---|---|---|
| `corpus/...` | | | | |

## When the real corpus is added

1. Delete the two `PLACEHOLDER-*.md` files from `corpus/`.
2. Fill in the table above and the answer key in `questions.md`.
3. Run `python3 exercises/00-rag/rag.py chunk` with the default settings, then
   `python3 exercises/00-rag/rag.py embed --out exercises/00-rag/index.json`
   to build the shipped index. `search` only uses an index whose recorded
   fingerprint matches the participant's `chunks.jsonl`. Participants who
   chunk with the default settings get identical chunks, so the shipped index
   matches them.
4. Record the chunk ids for each answer in `questions.md`. The ids depend on
   `--size` and `--overlap`.
