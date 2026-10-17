# /// script
# requires-python = ">=3.10"
# dependencies = ["tokenizers", "tiktoken"]
# ///
"""How three models cut text into tokens (Exercise 1, Dive Deeper).

    uv run exercises/01-rag/tokens.py
    uv run exercises/01-rag/tokens.py "TP53 R175H" ENSG00000141510

The first run downloads the three vocabularies, a few MB, without a key.
␣ is a space that belongs to the token, ## (bge) continues the previous
word, and a token that is only part of a character is shown as its bytes.
"""
import sys

import tiktoken
from tokenizers import Tokenizer

TEXTS = sys.argv[1:] or [
    "We quantified BRCA1 isoforms using RNA-seq.",
    "BRCA1 is ENSG00000012048; variant c.68_69del.",
    "ATGGATTTATCTGCTCTTCGCGTTGAA",
    "MDLSALRVE",
    "Hemoglobin has two α and two β chains 🧬",
]


def byte_alphabet():
    """Byte-level tokenizers write each byte as a printable letter; this undoes that."""
    keep = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256))
    letters, extra = keep[:], 0
    for b in range(256):
        if b not in keep:
            keep.append(b)
            letters.append(256 + extra)
            extra += 1
    return {chr(letter): b for b, letter in zip(keep, letters)}


BYTES = byte_alphabet()


def readable(piece: bytes) -> str:
    try:
        return piece.decode("utf-8").replace(" ", "␣")
    except UnicodeDecodeError:
        return piece.hex(" ").upper()


mistral = Tokenizer.from_pretrained("unsloth/Mistral-Nemo-Instruct-2407")
bge = Tokenizer.from_pretrained("BAAI/bge-base-en-v1.5")
gpt = tiktoken.get_encoding("o200k_base")

for text in TEXTS:
    rows = {
        "Mistral Nemo": [readable(bytes(BYTES[c] for c in t))
                         for t in mistral.encode(text, add_special_tokens=False).tokens],
        "bge-base": bge.encode(text, add_special_tokens=False).tokens,
        "GPT-4o": [readable(gpt.decode_single_token_bytes(i)) for i in gpt.encode(text)],
    }
    print(f"\n{text}   ({len(text.encode())} bytes in UTF-8)")
    for name, pieces in rows.items():
        print(f"  {name:13}{len(pieces):3}  " + " │ ".join(pieces))
