# Exercise 1 — RAG: give the model the documents

| | |
|---|---|
| **Model** | Mistral Nemo 12B for the answers and an embedding model for search, both at OpenRouter with the workshop key |
| **Needs** | Exercise 0: the notebook plugin and the workshop key in `.openrouter-key` |
| **You'll learn** | What retrieval-augmented generation (RAG) does at each step, and how to check a cited answer |
| **Done when** | You have run every cell, seen the closed-book and the open-book answer to the same question, and checked one citation |
| **If stuck** | `/halp 01-rag <what you tried>` |

## Why RAG

A language model only knows what it saw in training, plus whatever is in the
prompt. Ask it about something it never saw, and it still answers, fluently
and confidently, because producing plausible text is all it does.

Think of an exam. **Closed book**, the model answers from memory, even when
it never learned the subject. **Open book**, it may look things up first.
**Retrieval-augmented generation (RAG)** is the open book: before the model
answers, a search picks the parts of your documents that fit the question,
and the model gets those parts together with the question and an
instruction to answer only from them and to say where each claim came from.
Most "chat with your documents" tools work this way.

Here the documents are this workshop's own pages: the README and the
exercise pages. You know them, so you can judge the answers; the model has
never seen them.

```
 the workshop pages ──cut──► pieces ──embed──► numbers for each piece
                                                     │
 your question ─────────────────────────search──► the closest pieces
                                                     │
                     prompt = rules + pieces [p1] [p2] … + question
                                                     │
                                       model ──► answer with [p..] citations
                                                     │
                                         you ──► check the cited piece
```

## Before you start

You need the notebook plugin and the workshop key from
[Exercise 0](../00-plugins/README.md). Start a new chat in OpenCode and type:

```
/notebook exercises/01-rag/rag_notebook.py
```

The notebook opens next to the chat. Each cell shows its code (the input) in
grey and what it printed (the output) below it. Move with `↑` `↓`, run the
selected cell with `r`, and scroll a long output with `pgup` `pgdn`. Run the
cells from top to bottom: each one uses what the cells above made. The code
is short on purpose; the steps themselves are plain Python in
[`rag.py`](rag.py), one function each.

Run the first cell, **Connect to the models**. It should say that the
workshop key works. The first run starts a Python kernel and may take a
minute.

# Exercise 1a — Ask without the documents

## 1. Closed book

**Do:** run **1. Ask without the documents**. The question is "Which chat
model is the default in this workshop?"

**Look for:** the prompt is only the question. Does the model sound sure? Is
it right? You know the answer from the README.

**Why:** whatever it says comes from training alone. It cannot know this
workshop, and nothing stops it from answering anyway.

# Exercise 1b — Prepare the documents

## 2. Cut the documents into pieces

**Do:** run **2. Cut the pages into pieces**.

**Look for:** how many pieces, and three examples. Each has an id, like
`p11`, and the page and heading it came from.

**Why:** a model can only be given a few pieces at a time, and every piece
costs time and money. How you cut matters: too small, and an answer is split
across pieces; too large, and few fit in the prompt.

## 3. Turn each piece into numbers

**Do:** run **3. Turn the pieces into numbers**.

**Look for:** each piece is now a list of 768 numbers, an **embedding**. The
first few are printed.

**Why:** an embedding model places texts with similar meaning close
together. That is what lets the search in step 4 find a piece about "the
default model" even when it is worded differently from your question.

# Exercise 1c — Search, answer and check

## 4. Search, and read before you ask

**Do:** run **4. Find the pieces closest in meaning**, then **4b. Find the
pieces that share the most words**.

**Look for:** read the pieces **before** asking the model anything. Is the
answer in one of them? In which position? Do the two searches pick the same
pieces?

**Why:** search by meaning compares numbers; search by words counts shared
words, the way a search engine does. Either way, if the answer is not in the
retrieved pieces, no model can give it from them.

## 5. Open book

**Do:** run **5. Ask with the documents**.

**Look for:** the printed prompt: the rules, the pieces with their ids, then
your question. Does the answer cite a piece, like `[p17]`? Compare it with
step 1.

**Why:** same model, same question. The only difference is what it was given
to read.

## 6. Check the citation

**Do:** run **6. Show the cited pieces**.

**Look for:** is the answer really in the cited piece, in so many words?

**Why:** a citation turns "trust me" into something you can check in
seconds. A citation can also be wrong; checking is your job, not the model's.

# Exercise 1d — Find the limits

## 7. A question the documents cannot answer

**Do:** run **7. Ask something that is not in the documents**: "When is the
coffee break?"

**Look for:** there is no break in this workshop and the pages never mention
one. Does the model say "not in the documents", or invent a time?

**Why:** a good RAG answer admits when the documents are silent. Without the
rule to say so, many models fill the gap.

## 8. One piece or eight?

**Do:** run **8a. One piece**, then **8b. Eight pieces**. The question is
"How long is Exercise 3, and what are its parts?"

**Look for:** what does each answer contain? With eight pieces, does it add
anything that is not in them?

**Why:** the number of pieces is a trade-off: too few can miss half the
answer, too many add noise, cost and room for the model to embroider.

## Try your own question (optional)

Ask the agent in the chat to change a question in the notebook, for example:

> In exercises/01-rag/rag_notebook.py, change the question in the cell
> "1. Ask without the documents" to "What does /compact do?"

Approve the edit, then run cells 1, 4, 5 and 6 again (the numbers in their
titles). Or mark a cell with
`space`, go back to the chat with `ctrl+x ←`, and ask: "Is the cited text
really in the pieces of the cell I marked?"

## What to notice

- Without the documents, nothing stops the model from making an answer up,
  and a made-up answer sounds like a real one.
- With the documents, the answer can only be as good as the pieces you
  retrieved. Read those first.
- A citation is a claim. Checking it takes seconds.
- How many pieces to send is a trade-off.

**Discuss with your neighbour:**

1. Which of your own documents (protocols, lab notes, papers) would you want
   to search this way, and what would you be afraid it gets wrong?
2. Your colleague's RAG tool answers correctly but cites the wrong piece. Is
   that a problem?
3. Would you rather use a big model without your documents, or a small model
   with them?

# === Dive Deeper ===

# Exercise 1e — What the model reads: tokens and embeddings

In this exercise, Mistral Nemo wrote the answers and bge-base found the
pieces. Neither reads letters or words. Text is first cut into
**tokens**: short pieces of text from a fixed list, the model's vocabulary.
Each token is then turned into numbers. (Tokens are much smaller than the
pieces of up to 800 characters you cut the documents into in step 2.)

Each model has its own tokenizer, so the same text is cut in different ways:

| Model | Tokenizer | Vocabulary |
|---|---|---|
| Mistral Nemo (the answers) | BPE, built from bytes | 131,072 tokens |
| bge-base-en-v1.5 (the search) | WordPiece, lower case only | 30,522 tokens |
| GPT-4o, for comparison | BPE, built from bytes (`o200k_base`) | 200,019 tokens |

This part is for reading; running something is optional, at the end. Below,
colours separate the tokens, `␣` is a space that belongs to a token, and
`##` (bge only) means "continues the previous word".

<details>
<summary><b>What are the tokens?</b></summary>

**Everyday English costs the same everywhere.** "I love this workshop" is 4
tokens for all three models: common words are whole tokens in every
vocabulary.

**Biology does not.** "We quantified BRCA1 isoforms using RNA-seq." is 9, 15
or 12 tokens:

Mistral Nemo, 9 tokens

```math
{\color{RoyalBlue}\text{We}} \, {\color{OrangeRed}\text{␣quantified}} \, {\color{ForestGreen}\text{␣BRCA}} \, {\color{Orchid}\text{1}} \, {\color{RoyalBlue}\text{␣isoforms}} \, {\color{OrangeRed}\text{␣using}} \, {\color{ForestGreen}\text{␣RNA}} \, {\color{Orchid}\text{-seq}} \, {\color{RoyalBlue}\text{.}}
```

bge-base, 15 tokens

```math
{\color{RoyalBlue}\text{we}} \, {\color{OrangeRed}\text{quan}} \, {\color{ForestGreen}\#\#\text{ti}} \, {\color{Orchid}\#\#\text{fied}} \, {\color{RoyalBlue}\text{br}} \, {\color{OrangeRed}\#\#\text{ca}} \, {\color{ForestGreen}\#\#\text{1}} \, {\color{Orchid}\text{iso}} \, {\color{RoyalBlue}\#\#\text{forms}} \, {\color{OrangeRed}\text{using}} \, {\color{ForestGreen}\text{rna}} \, {\color{Orchid}\text{-}} \, {\color{RoyalBlue}\text{se}} \, {\color{OrangeRed}\#\#\text{q}} \, {\color{ForestGreen}\text{.}}
```

GPT-4o, 12 tokens

```math
{\color{RoyalBlue}\text{We}} \, {\color{OrangeRed}\text{␣quantified}} \, {\color{ForestGreen}\text{␣BR}} \, {\color{Orchid}\text{CA}} \, {\color{RoyalBlue}\text{1}} \, {\color{OrangeRed}\text{␣iso}} \, {\color{ForestGreen}\text{forms}} \, {\color{Orchid}\text{␣using}} \, {\color{RoyalBlue}\text{␣RNA}} \, {\color{OrangeRed}\text{-se}} \, {\color{ForestGreen}\text{q}} \, {\color{Orchid}\text{.}}
```

`BRCA1` is one gene and never one token. bge also lower-cases everything, so
for the search model `BRCA1` and `brca1` are the same text.

**Identifiers fall apart.** An Ensembl ID and an HGVS variant:

```
Mistral Nemo  29  BR │ CA │ 1 │ ␣is │ ␣E │ NS │ G │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │ 1 │ 2 │ 0 │ 4 │ 8 │ ; │ ␣variant │ ␣c │ . │ 6 │ 8 │ _ │ 6 │ 9 │ del │ .
GPT-4o        19  BR │ CA │ 1 │ ␣is │ ␣ENS │ G │ 000 │ 000 │ 120 │ 48 │ ; │ ␣variant │ ␣c │ . │ 68 │ _ │ 69 │ del │ .
```

Mistral Nemo reads every digit as its own token; GPT-4o groups up to three.
And `BRCA1` at the start of a line is `BR│CA│1` for Mistral, but `␣BRCA│1`
after a space: the same gene, different tokens.

</details>

<details>
<summary><b>From DNA to protein: tokens are not codons</b></summary>

The first 27 bases of the BRCA1 coding sequence are nine codons, which code
for the first nine amino acids of the protein:

```math
{\color{RoyalBlue}\text{ATG}} \, {\color{OrangeRed}\text{GAT}} \, {\color{ForestGreen}\text{TTA}} \, {\color{Orchid}\text{TCT}} \, {\color{RoyalBlue}\text{GCT}} \, {\color{OrangeRed}\text{CTT}} \, {\color{ForestGreen}\text{CGC}} \, {\color{Orchid}\text{GTT}} \, {\color{RoyalBlue}\text{GAA}}
```

```math
{\color{RoyalBlue}\text{M}} \, {\color{OrangeRed}\text{D}} \, {\color{ForestGreen}\text{L}} \, {\color{Orchid}\text{S}} \, {\color{RoyalBlue}\text{A}} \, {\color{OrangeRed}\text{L}} \, {\color{ForestGreen}\text{R}} \, {\color{Orchid}\text{V}} \, {\color{RoyalBlue}\text{E}}
```

Mistral Nemo cuts the same DNA into 15 tokens, and the protein into 5:

```math
{\color{RoyalBlue}\text{AT}} \, {\color{OrangeRed}\text{GG}} \, {\color{ForestGreen}\text{AT}} \, {\color{Orchid}\text{TT}} \, {\color{RoyalBlue}\text{AT}} \, {\color{OrangeRed}\text{CT}} \, {\color{ForestGreen}\text{G}} \, {\color{Orchid}\text{CT}} \, {\color{RoyalBlue}\text{CT}} \, {\color{OrangeRed}\text{TC}} \, {\color{ForestGreen}\text{GC}} \, {\color{Orchid}\text{G}} \, {\color{RoyalBlue}\text{TT}} \, {\color{OrangeRed}\text{G}} \, {\color{ForestGreen}\text{AA}}
```

```math
{\color{RoyalBlue}\text{MD}} \, {\color{OrangeRed}\text{LS}} \, {\color{ForestGreen}\text{AL}} \, {\color{Orchid}\text{R}} \, {\color{RoyalBlue}\text{VE}}
```

The start codon `ATG` is split over two tokens, and `MD`, `LS` and `AL` are
pairs of amino acids that happen to be common letter pairs. GPT-4o cuts both
almost the same way. bge cuts the DNA into other lower-case bits of one to
three letters (`at│##gga│##tt│##tat…`), no closer to codons. A text tokenizer is
compression learned from ordinary text: it does not know what a base, a
codon or an amino acid is.

Models trained on sequences choose their tokens differently. The protein
language model ESM-2 has a vocabulary of 33: the 20 amino acids, 5 letters
for rare or ambiguous residues, and markers such as start, end and mask.
Every amino acid is its own token, so every residue gets its own numbers,
and the embeddings it makes describe proteins, not sentences about them.

</details>

<details>
<summary><b>Below the tokens: UTF-8 bytes</b></summary>

A computer stores text as bytes. UTF-8 uses one byte for an English letter or
a digit, two for a Greek letter such as `α` (`CE B1`), and four for an emoji
such as 🧬 (`F0 9F A7 AC`).

Mistral Nemo and GPT-4o build their tokens from bytes, so they can cut any
text, even a character they have never seen: at worst a token is a single
byte. bge builds its tokens from characters, and a character it does not
know becomes `[UNK]`, "unknown":

```
Hemoglobin has two α and two β chains 🧬
Mistral Nemo  13  H │ em │ oglobin │ ␣has │ ␣two │ ␣α │ ␣and │ ␣two │ ␣β │ ␣chains │ 20 F0 9F │ A7 │ AC
bge-base      12  hem │ ##og │ ##lo │ ##bin │ has │ two │ α │ and │ two │ β │ chains │ [UNK]
```

`α` and `β` are common enough to be whole tokens. 🧬 is not: Mistral cuts it
into tokens that are bytes, none of them a character on its own (`20` is the
space before it), and bge does not see it at all. What the search model
cannot see, it cannot find.

</details>

<details>
<summary><b>Why does it matter?</b></summary>

**Limits and cost are counted in tokens.** The context window, the price and
the speed all depend on the number of tokens. IDs, numbers and sequences
fill the window much faster than prose: 27 bases are 15 tokens, while the 20
letters of "I love this workshop" are 4.

**Odd tokens, odd mistakes.** A model that reads
`0│0│0│0│0│0│1│2│0│4│8` can drop or repeat a digit when it copies an ID.
Check every identifier an agent writes against the source.

**Search and answers use different tokenizers.** In step 4, bge cut your
question its own way, in lower case, before searching. Mistral then read the
documents it found cut a different way.

</details>

<details>
<summary><b>From tokens to numbers: embeddings</b></summary>

**Inside a model, each token becomes a list of numbers.** The model's first
layer looks up each token in a big table, where every row holds a few hundred
to a few thousand numbers learned in training. The layers after that mix in
the other tokens, so the same token ends up with different numbers in
different sentences.

**An embedding model turns a whole text into one list of numbers.** bge turns
any text into 768 numbers; the first five for "BRCA1 mutations raise the risk
of breast cancer." are `-0.038, 0.004, -0.062, -0.002, 0.043`. Texts with
similar wording and topic get similar lists. That is what step 3 made for
every piece of the documents, and what step 4 compared your question
with. Here bge compares four sentences with that one (1 means the
same direction, 0 unrelated):

| Similarity | Sentence |
|---|---|
| 0.886 | BRCA1 mutations **do not** raise the risk of breast cancer. |
| 0.874 | Women with harmful BRCA1 variants are more likely to develop breast tumours. |
| 0.720 | We quantified BRCA1 isoforms using RNA-seq. |
| 0.353 | The coffee break is at ten in the main hall. |

**The sentence that says the opposite comes first.** Embeddings measure what
a text is about, not whether it agrees: similar is not the same as true.
That is why step 6 has you check the citation.

</details>

<details>
<summary><b>The whole path, from your text to the next token</b></summary>

```
your text
   ↓  tokenizer: cut into tokens            BR │ CA │ 1
token numbers                               35846, 9467, 1049
   ↓  look-up table: each token to a list of numbers
   ↓  layers: every token looks at the others (attention)
numbers that depend on the whole text
   ↓  a score for every token in the vocabulary
probabilities for the next token
   ↓  pick one, add it to the text, repeat
the answer, one token at a time
```

An embedding model like bge stops halfway and returns one list of numbers
per text. A chat model like Mistral goes all the way down. The last step,
the probabilities for the next token, is what the decision model in
[Exercise 5](../05-decide/README.md) reads instead of the model's written
answer.

</details>

**Try it yourself (optional).** See how the three tokenizers cut your own
gene names, sample IDs or sequences:

```bash
uv run exercises/01-rag/tokens.py "TP53 R175H" ENSG00000141510
```

Without text it prints the examples above. The first run downloads the three
vocabularies, a few MB; no key is needed.

**Discuss with your neighbour:** which of your own identifiers would a model
most likely copy wrongly, and how would you check?

Next: [Exercise 2 — Skills](../02-skills/README.md).
