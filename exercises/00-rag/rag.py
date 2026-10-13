#!/usr/bin/env python3
"""RAG, every stage visible.

A small retrieval-augmented generation (RAG) pipeline you can read in one go.
Each subcommand does one stage and prints what it did:

    chunk   split corpus/*.md and *.txt into overlapping pieces -> chunks.jsonl
    embed   turn every chunk into a vector with the embeddings endpoint -> index.json
    search  find the chunks most similar to a question (cosine or BM25)
    ask     build a prompt from the retrieved chunks and ask the chat model

Only the Python standard library is used. Settings come from flags or from
environment variables:

    DTU_BASE     root of the DTU model URLs (default: the workshop server)
    RAG_MODEL    chat model name (default: mistral)
    EMBED_MODEL  embedding model name (default: embed)
    RAG_URL      full base URL for the chat model (default: $DTU_BASE/$RAG_MODEL)
    EMBED_URL    full base URL for embeddings (default: $DTU_BASE/$EMBED_MODEL)

The client appends /chat/completions or /embeddings to the base URL.
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "outputs" / "00-rag"
CORPUS = HERE / "corpus"
SHIPPED_INDEX = HERE / "index.json"

DTU_BASE = os.environ.get("DTU_BASE", "https://teaching.healthtech.dtu.dk/workshop").rstrip("/")
RAG_MODEL = os.environ.get("RAG_MODEL", "mistral")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "embed")
RAG_URL = os.environ.get("RAG_URL", f"{DTU_BASE}/{RAG_MODEL}")
EMBED_URL = os.environ.get("EMBED_URL", f"{DTU_BASE}/{EMBED_MODEL}")

SYSTEM_RAG = """You answer questions using ONLY the evidence chunks given by the user.
Rules:
- Use only facts stated in the evidence. Do not use outside knowledge.
- Cite the chunk id for every claim in square brackets, like [c12].
- If chunks disagree with each other, say so and cite each of them.
- If the evidence is not enough to answer, reply: not in the documents."""


# ------------------------------------------------------------------- helpers

def shown(path):
    """A path relative to the workshop folder when possible, for shorter output."""
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def post_json(url, payload, timeout):
    """POST a JSON payload and return the decoded JSON reply."""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"{url} answered HTTP {err.code}: {body}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        raise RuntimeError(f"could not reach {url}: {err}") from None


# --------------------------------------------------------------------- chunk

def split_spans(text, size, overlap):
    """Return (start, end) character spans of overlapping chunks.

    A chunk is cut at a paragraph, sentence or word break near its end when
    possible, so that words are not split in half.
    """
    spans, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            earliest = start + size * 2 // 3
            for separator in ("\n\n", ". ", " "):
                cut = text.rfind(separator, earliest, end)
                if cut != -1:
                    end = cut + len(separator)
                    break
        spans.append((start, end))
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
        while start < end and not text[start - 1].isspace():
            start += 1  # move to the beginning of a word
    return spans


def cmd_chunk(args):
    """Split every corpus file into chunks and write chunks.jsonl."""
    if args.overlap >= args.size:
        sys.exit("--overlap must be smaller than --size")
    files = sorted(p for p in Path(args.corpus).iterdir() if p.suffix in (".md", ".txt"))
    if not files:
        sys.exit(f"No .md or .txt files found in {args.corpus}")
    chunks = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for start, end in split_spans(text, args.size, args.overlap):
            chunks.append({"id": f"c{len(chunks) + 1}", "source": path.name,
                           "start": start, "end": end, "text": text[start:end]})
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    print(f"Read {len(files)} file(s) from {shown(args.corpus)}")
    print(f"Cut them into {len(chunks)} chunks of at most {args.size} characters, "
          f"each overlapping the previous one by about {args.overlap} characters.")
    print(f"Wrote {shown(args.out)}\n\nFirst chunks:")
    for chunk in chunks[:3]:
        preview = " ".join(chunk["text"].split())[:120]
        print(f"  [{chunk['id']}] {chunk['source']} chars {chunk['start']}-{chunk['end']}: {preview}...")


def load_chunks(path):
    """Read chunks.jsonl, or stop with a hint if it does not exist yet."""
    if not Path(path).exists():
        sys.exit(f"{shown(path)} does not exist yet. Run: python3 {shown(__file__)} chunk")
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def fingerprint(chunks):
    """A short hash of the chunk ids and texts, to match an index to its chunks."""
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update((chunk["id"] + "\0" + chunk["text"] + "\0").encode("utf-8"))
    return digest.hexdigest()[:16]


# --------------------------------------------------------------------- embed

def normalise(vector):
    """Scale a vector to length 1, so that cosine similarity is a dot product."""
    length = math.sqrt(sum(x * x for x in vector)) or 1.0
    return [x / length for x in vector]


def embed_texts(texts, batch_size, timeout):
    """Send texts to the embeddings endpoint in batches; return unit vectors."""
    vectors = []
    for first in range(0, len(texts), batch_size):
        batch = texts[first:first + batch_size]
        reply = post_json(f"{EMBED_URL}/embeddings", {"model": EMBED_MODEL, "input": batch}, timeout)
        items = sorted(reply["data"], key=lambda item: item["index"])
        vectors.extend(normalise(item["embedding"]) for item in items)
    return vectors


def cmd_embed(args):
    """Embed every chunk and save the vectors to index.json."""
    chunks = load_chunks(args.chunks)
    print(f"Embedding {len(chunks)} chunks with model '{EMBED_MODEL}' at {EMBED_URL}/embeddings "
          f"in batches of {args.batch} ...")
    began = time.time()
    try:
        vectors = embed_texts([c["text"] for c in chunks], args.batch, timeout=120)
    except RuntimeError as err:
        sys.exit(f"Embedding failed: {err}\nYou can still search with --lexical (BM25).")
    index = {"embed_model": EMBED_MODEL, "fingerprint": fingerprint(chunks),
             "dims": len(vectors[0]), "ids": [c["id"] for c in chunks],
             "vectors": [[round(x, 6) for x in v] for v in vectors]}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(index), encoding="utf-8")
    print(f"Done in {time.time() - began:.1f} s: {len(vectors)} vectors with "
          f"{index['dims']} dimensions each, scaled to length 1.")
    print(f"Wrote {shown(args.out)}")


# -------------------------------------------------------------------- search

def tokenize(text):
    """Lower-case words and numbers."""
    return re.findall(r"\w+", text.lower())


def bm25_scores(query, chunks, k1=1.5, b=0.75):
    """Score each chunk with BM25, a classic keyword-matching formula."""
    docs = [tokenize(chunk["text"]) for chunk in chunks]
    average_length = sum(len(doc) for doc in docs) / len(docs)
    doc_freq = Counter(term for doc in docs for term in set(doc))
    scores = []
    for doc in docs:
        counts, score = Counter(doc), 0.0
        for term in set(tokenize(query)):
            if term in counts:
                idf = math.log(1 + (len(docs) - doc_freq[term] + 0.5) / (doc_freq[term] + 0.5))
                tf = counts[term]
                score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(doc) / average_length))
        scores.append(score)
    return scores


def load_index(chunks, index_path):
    """Return (index, None) if a matching index exists, else (None, reason)."""
    candidates = [Path(index_path)] if index_path else [OUT / "index.json", SHIPPED_INDEX]
    for path in candidates:
        if path.exists():
            index = json.loads(path.read_text(encoding="utf-8"))
            if index.get("fingerprint") != fingerprint(chunks):
                return None, (f"{shown(path)} was built from different chunks "
                              "(other corpus, --size or --overlap). Run 'embed' again.")
            return index, None
    return None, "no index.json found. Run 'embed' to build one."


def retrieve(query, chunks, k, lexical, index_path=None):
    """Return (method, [(score, chunk), ...]) for the top-k chunks."""
    if not lexical:
        index, reason = load_index(chunks, index_path)
        if index:
            try:
                query_vector = embed_texts([query], 1, timeout=20)[0]
                scores = [sum(a * b for a, b in zip(query_vector, v)) for v in index["vectors"]]
                ranked = sorted(zip(scores, chunks), key=lambda pair: -pair[0])
                return "cosine similarity of embeddings", ranked[:k]
            except RuntimeError as err:
                reason = f"the embeddings endpoint failed ({err})"
        print(f"NOTICE: falling back to BM25 keyword search because {reason}\n")
    ranked = sorted(zip(bm25_scores(query, chunks), chunks), key=lambda pair: -pair[0])
    return "BM25 keyword scores", ranked[:k]


def print_hits(method, hits):
    """Show each retrieved chunk with its id, source, score and full text."""
    print(f"Top {len(hits)} chunks by {method}:\n")
    for score, chunk in hits:
        print(f"[{chunk['id']}] {chunk['source']} chars {chunk['start']}-{chunk['end']}  score={score:.3f}")
        for line in chunk["text"].strip().splitlines():
            print(f"    {line}")
        print()


def cmd_search(args):
    """Retrieve and print the top-k chunks for a question."""
    chunks = load_chunks(args.chunks)
    method, hits = retrieve(args.question, chunks, args.k, args.lexical, args.index)
    print_hits(method, hits)


# ----------------------------------------------------------------------- ask

def build_messages(question, hits):
    """Assemble the chat messages. With no hits, send only the question."""
    if hits is None:
        return [{"role": "user", "content": question}]
    evidence = "\n\n".join(
        f"[{c['id']}] (source: {c['source']}, chars {c['start']}-{c['end']})\n{c['text'].strip()}"
        for _, c in hits)
    user = (f"Evidence:\n\n{evidence}\n\nQuestion: {question}\n\n"
            "Answer using only the evidence above and cite chunk ids like [c12].")
    return [{"role": "system", "content": SYSTEM_RAG}, {"role": "user", "content": user}]


def chat(messages, temperature):
    """Send messages to the chat model and return its text answer."""
    payload = {"model": RAG_MODEL, "messages": messages,
               "temperature": temperature, "max_tokens": 512}
    reply = post_json(f"{RAG_URL}/chat/completions", payload, timeout=180)
    return reply["choices"][0]["message"]["content"] or ""


def check_citations(answer, hits):
    """Print which chunk ids the answer cites, and flag ids it was never shown."""
    inside_brackets = " ".join(re.findall(r"\[([^\]]*)\]", answer))  # [c2], [c2, c4]
    cited = sorted(set(re.findall(r"\bc\d+\b", inside_brackets)), key=lambda c: int(c[1:]))
    given = {chunk["id"]: chunk for _, chunk in hits}
    if not cited:
        print("The answer cites no chunk ids.")
    for chunk_id in cited:
        if chunk_id in given:
            c = given[chunk_id]
            print(f"Cites [{chunk_id}] = {c['source']} chars {c['start']}-{c['end']}. Check it with:\n"
                  f"    grep -n \"<a short phrase from the chunk>\" {shown(CORPUS)}/{c['source']}")
        else:
            print(f"WARNING: cites [{chunk_id}], which was NOT in the evidence it was given.")


def cmd_ask(args):
    """Show the exact prompt, then the model's answer."""
    hits, method = None, "none (--no-rag)"
    if not args.no_rag:
        method, hits = retrieve(args.question, load_chunks(args.chunks), args.k, args.lexical, args.index)
    messages = build_messages(args.question, hits)
    print(f"Retrieval: {method}" + ("" if hits is None else f", k={len(hits)}"))
    print("=" * 30 + " EXACT PROMPT SENT " + "=" * 30)
    for message in messages:
        print(f"--- {message['role'].upper()} ---\n{message['content']}\n")
    print("=" * 79)
    print(f"Asking '{RAG_MODEL}' at {RAG_URL}/chat/completions ...\n")
    try:
        answer = chat(messages, args.temperature)
    except RuntimeError as err:
        sys.exit(f"The chat model did not answer: {err}")
    print(f"--- ANSWER ---\n{answer.strip()}\n")
    if hits is not None:
        check_citations(answer, hits)
    record = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "question": args.question,
              "model": RAG_MODEL, "retrieval": method,
              "chunk_ids": [c["id"] for _, c in hits or []], "answer": answer}
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "answers.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"\n(Logged to {shown(OUT / 'answers.jsonl')})")


# ---------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    chunks_default = str(OUT / "chunks.jsonl")

    p = sub.add_parser("chunk", help="split the corpus into overlapping chunks")
    p.add_argument("--size", type=int, default=800, help="max characters per chunk")
    p.add_argument("--overlap", type=int, default=150, help="characters shared with the previous chunk")
    p.add_argument("--corpus", default=str(CORPUS))
    p.add_argument("--out", default=chunks_default)
    p.set_defaults(func=cmd_chunk)

    p = sub.add_parser("embed", help="embed every chunk into index.json")
    p.add_argument("--chunks", default=chunks_default)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--out", default=str(OUT / "index.json"))
    p.set_defaults(func=cmd_embed)

    for name, func in (("search", cmd_search), ("ask", cmd_ask)):
        p = sub.add_parser(name, help=f"{name} the corpus")
        p.add_argument("question")
        p.add_argument("--lexical", action="store_true", help="use BM25 keyword search")
        p.add_argument("--chunks", default=chunks_default)
        p.add_argument("--index", help="index.json to use (default: outputs/00-rag, then shipped)")
        if name == "search":
            p.add_argument("-k", type=int, default=3, help="number of chunks to retrieve")
        else:
            group = p.add_mutually_exclusive_group()
            group.add_argument("-k", type=int, default=3, help="number of chunks to retrieve")
            group.add_argument("--no-rag", action="store_true", help="send only the question")
            p.add_argument("--temperature", type=float, default=0.0)
        p.set_defaults(func=func)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
