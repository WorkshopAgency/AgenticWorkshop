---
name: corpus-search
description: Search the Exercise 00 document corpus (exercises/01-rag/corpus) and answer only from the retrieved chunks, quoting chunk ids. Use when the user asks a question that the workshop corpus should answer. Do not use it for general knowledge questions.
---

# Search the workshop corpus before answering

Answer questions about the documents in `exercises/01-rag/corpus/` only from
text retrieved by the search tool, never from memory.

## Steps

1. If `outputs/01-rag/chunks.jsonl` does not exist, run
   `python3 exercises/01-rag/rag.py chunk` first.
2. Search with the user's question, or a shorter keyword version of it:

   ```bash
   python3 exercises/01-rag/rag.py search "<question>" -k 5
   ```

   Add `--lexical` to use keyword (BM25) search. If the output starts with
   `NOTICE: falling back to BM25`, the embedding search was unavailable; say
   so in your answer.
3. Read the retrieved chunk texts. If they do not answer the question, search
   once or twice more with different wording (synonyms, the key noun alone).
4. Answer using only what the chunks say. Cite the chunk id for every claim in
   square brackets, like `[c12]`, and name the source file.
5. If chunks disagree (for example an older and a newer version), give both
   values with both chunk ids and say which source is newer if the text says so.
6. If the retrieved text does not contain the answer, say "not in the
   documents" and list what you searched for. Do not fill the gap from memory.

## Do not

- Do not edit or delete files in `exercises/01-rag/corpus/`.
- Do not cite a chunk id that did not appear in the search output.
- Do not run `rag.py ask`; you are the model that answers here.
