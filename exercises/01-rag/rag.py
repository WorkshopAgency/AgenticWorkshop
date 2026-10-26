"""RAG, one step at a time. Used by rag_notebook.py; every function prints what it did.

The documents are this workshop's own pages: README.md and each exercise's
README. The model has never seen them, so it can only answer from them if
we put the right pieces in front of it.

    cut()                    the pages, cut into pieces
    embed(pieces)            each piece turned into a list of numbers
    find(question, index)    the pieces closest to a question
    answer(question, hits)   ask the model, with or without pieces
    cited(answer, hits)      print every piece the answer cites, in full

Only the Python standard library is used. The models run at OpenRouter, with
the key in .openrouter-key in the workshop folder (Exercise 0), or in the
environment variable OPENROUTER_API_KEY.
"""
import json
import math
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

# the shared colours, by meaning (exercises/shared/look.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))
import look  # noqa: E402
import openrouter_key  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "outputs" / "01-rag"
# this exercise's own page is left out: it would hand over its answers
PAGES = [ROOT / "README.md"] + [p for p in sorted(ROOT.glob("exercises/*/README.md")) if p.parent.name != "01-rag"]

CHAT_URL = EMBED_URL = "https://openrouter.ai/api/v1"
CHAT_MODEL = "mistralai/mistral-nemo"   # Mistral Nemo 12B, a small model
EMBED_MODEL = "baai/bge-base-en-v1.5"   # 768 numbers per piece

RULES = """You answer questions using ONLY the numbered pieces given by the user.
- Use only facts stated in the pieces. Do not use outside knowledge.
- Cite the piece for every claim in square brackets, like [p12].
- If the pieces are not enough to answer, reply: not in the documents."""


# ---------------------------------------------------------------- talking to the models

def _key():
    return openrouter_key.read()


def _tls():
    """Python sometimes ships without the computer's certificates (python.org on a
    Mac, some uv builds); fall back to the system's own certificate file."""
    context = ssl.create_default_context()
    if not context.cert_store_stats()["x509_ca"]:
        for bundle in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"):
            if os.path.exists(bundle):
                context.load_verify_locations(bundle)
                break
    return context


def _post(url, payload):
    headers = {"Content-Type": "application/json"}
    problem = openrouter_key.problem()
    if problem:
        raise SystemExit(problem)
    headers["Authorization"] = f"Bearer {_key()}"
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=120, context=_tls()) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as err:
        raise SystemExit(f"{url} answered HTTP {err.code}: {err.read().decode()[:300]}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        raise SystemExit(f"Could not reach {url}: {err}") from None


def status():
    """Say which models answer, and whether the key works."""
    print(f"Answers: {CHAT_MODEL}. Search: {EMBED_MODEL}. Both at OpenRouter.")
    problem = openrouter_key.problem()
    if problem:
        print(problem)
        return
    request = urllib.request.Request("https://openrouter.ai/api/v1/key",
                                     headers={"Authorization": f"Bearer {_key()}"})
    try:
        with urllib.request.urlopen(request, timeout=30, context=_tls()) as response:
            json.loads(response.read())
        print("The workshop key works.")
    except urllib.error.HTTPError as err:
        print(f"The key was refused (HTTP {err.code}). Check .openrouter-key.")
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        print(f"Could not reach OpenRouter: {err}. Check the network.")


def _chat(messages):
    reply = _post(f"{CHAT_URL}/chat/completions",
                  {"model": CHAT_MODEL, "messages": messages, "temperature": 0.2, "max_tokens": 400})
    return reply["choices"][0]["message"]["content"] or ""


def _embed(texts):
    vectors = []
    for start in range(0, len(texts), 64):
        reply = _post(f"{EMBED_URL}/embeddings", {"model": EMBED_MODEL, "input": texts[start:start + 64]})
        for item in sorted(reply["data"], key=lambda d: d["index"]):
            norm = math.sqrt(sum(x * x for x in item["embedding"])) or 1.0
            vectors.append([x / norm for x in item["embedding"]])
    return vectors


# ---------------------------------------------------------------- the steps

def cut(size=800):
    """Cut the workshop pages into pieces of at most `size` characters, at headings and paragraphs."""
    pieces = []
    for page in PAGES:
        name = page.relative_to(ROOT).as_posix()
        heading, buffer = "", ""
        for block in re.split(r"\n\s*\n", page.read_text(encoding="utf-8")):
            block = block.strip()
            if not block:
                continue
            if block.startswith("#"):
                _flush(pieces, name, heading, buffer)
                heading, buffer = block.splitlines()[0].lstrip("# ").strip(), ""
                block = "\n".join(block.splitlines()[1:]).strip()
                if not block:
                    continue
            if buffer and len(buffer) + len(block) > size:
                _flush(pieces, name, heading, buffer)
                buffer = ""
            buffer = f"{buffer}\n\n{block}".strip()
        _flush(pieces, name, heading, buffer)
    for number, piece in enumerate(pieces, 1):
        piece["id"] = f"p{number}"
    print(f"{len(PAGES)} pages cut into {len(pieces)} pieces. Three of them:\n")
    for piece in pieces[10:13]:
        print(f"{look.ident('[' + piece['id'] + ']')} {piece['source']}")
        print(look.muted(f"    {piece['text'][:160].replace(chr(10), ' ')} …") + "\n")
    return pieces


def _flush(pieces, name, heading, text):
    if text.strip():
        pieces.append({"source": f"{name} › {heading}" if heading else name, "text": text.strip()[:1200]})


def embed(pieces):
    """Turn every piece into a list of numbers that captures its meaning."""
    OUT.mkdir(parents=True, exist_ok=True)
    cache = OUT / "index.json"
    texts = [p["text"] for p in pieces]
    if cache.exists():
        saved = json.loads(cache.read_text())
        if saved.get("texts") == texts and saved.get("model") == EMBED_MODEL:
            print(f"{len(texts)} pieces, already turned into numbers (saved in {cache.relative_to(ROOT)}).")
            return {"pieces": pieces, "vectors": saved["vectors"]}
    vectors = _embed(texts)
    cache.write_text(json.dumps({"model": EMBED_MODEL, "texts": texts, "vectors": vectors}))
    print(f"{len(vectors)} pieces, each now a list of {len(vectors[0])} numbers.")
    print(f"Piece {pieces[0]['id']} starts: {[round(x, 3) for x in vectors[0][:5]]} …")
    return {"pieces": pieces, "vectors": vectors}


def find(question, index, k=3, words=False):
    """The k pieces closest to the question: by meaning (embeddings), or with words=True by shared words."""
    pieces = index["pieces"]
    if words:
        scores = _word_scores(question, pieces)
        how = "shared words (BM25)"
    else:
        q = _embed([question])[0]
        scores = [sum(a * b for a, b in zip(q, v)) for v in index["vectors"]]
        how = "meaning (cosine similarity of embeddings)"
    ranked = sorted(zip(scores, pieces), key=lambda pair: -pair[0])[:k]
    print(f"The {k} pieces closest to the question, by {how}:\n")
    for rank, (score, piece) in enumerate(ranked, 1):
        print(f"{rank}. {look.ident('[' + piece['id'] + ']')} score {score:.3f}  {piece['source']}")
        print(look.muted(f"   {piece['text'][:140].replace(chr(10), ' ')} …") + "\n")
    return [piece for _, piece in ranked]


def _word_scores(question, pieces, k1=1.5, b=0.75):
    tokens = lambda text: re.findall(r"[a-z0-9]+", text.lower())
    docs = [tokens(p["text"]) for p in pieces]
    average = sum(map(len, docs)) / len(docs)
    df = Counter(word for doc in docs for word in set(doc))
    scores = []
    for doc in docs:
        tf = Counter(doc)
        score = 0.0
        for word in set(tokens(question)):
            if word in tf:
                idf = math.log(1 + (len(docs) - df[word] + 0.5) / (df[word] + 0.5))
                score += idf * tf[word] * (k1 + 1) / (tf[word] + k1 * (1 - b + b * len(doc) / average))
        scores.append(score)
    return scores


def answer(question, hits=None):
    """Ask the model. Without hits it answers from memory; with hits only from those pieces."""
    if hits is None:
        messages = [{"role": "user", "content": question}]
    else:
        evidence = "\n\n".join(f"[{p['id']}] ({p['source']})\n{p['text']}" for p in hits)
        messages = [{"role": "system", "content": RULES},
                    {"role": "user", "content": f"Pieces:\n\n{evidence}\n\nQuestion: {question}"}]
    print(look.heading("PROMPT SENT TO THE MODEL"))
    if hits is None:
        print(look.muted("--- user ---"))
    else:  # the same text as in messages, coloured by part
        print(look.muted(f"--- system ---\n{RULES}\n\n--- user ---\nPieces:\n"))
        for p in hits:
            print(look.ident(f"[{p['id']}] ({p['source']})"))
            print(look.muted(p["text"]) + "\n")
    print(look.question(question if hits is None else f"Question: {question}") + "\n")
    text = _chat(messages).strip()
    print(look.heading(f"ANSWER FROM {CHAT_MODEL}"))
    print(look.answer(text))
    if hits is not None:
        given = {p["id"] for p in hits}
        cited = sorted(set(re.findall(r"\bp\d+\b", " ".join(re.findall(r"\[([^\]]*)\]", text)))))
        print("\nCited: " + (look.ident(", ".join(cited)) if cited else look.warn("nothing")))
        for piece_id in cited:
            if piece_id not in given:
                print(look.warn(f"WARNING: {piece_id} was not among the pieces it was given."))
    return text


def cited(text, hits):
    """Print, in full, every piece the answer cites, so you can check the claim yourself."""
    ids = sorted(set(re.findall(r"\bp\d+\b", " ".join(re.findall(r"\[([^\]]*)\]", text)))))
    if not ids:
        print(look.warn("The answer cites no piece."))
    for piece in hits:
        if piece["id"] in ids:
            print(f"{look.ident('[' + piece['id'] + ']')} {piece['source']}\n{piece['text']}\n")


if __name__ == "__main__":
    status()  # scripts/check-setup.sh runs this
