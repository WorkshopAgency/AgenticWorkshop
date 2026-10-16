# Exercise 1 — RAG: give the model the documents

| | |
|---|---|
| **Time** | 15 min |
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

## 1. Closed book (2 min)

**Do:** run **1. Ask without the documents**. The question is "Which chat
model is the default in this workshop?"

**Look for:** the prompt is only the question. Does the model sound sure? Is
it right? You know the answer from the README.

**Why:** whatever it says comes from training alone. It cannot know this
workshop, and nothing stops it from answering anyway.

## 2. Cut the documents into pieces (2 min)

**Do:** run **2. Cut the pages into pieces**.

**Look for:** how many pieces, and three examples. Each has an id, like
`p11`, and the page and heading it came from.

**Why:** a model can only be given a few pieces at a time, and every piece
costs time and money. How you cut matters: too small, and an answer is split
across pieces; too large, and few fit in the prompt.

## 3. Turn each piece into numbers (1 min)

**Do:** run **3. Turn the pieces into numbers**.

**Look for:** each piece is now a list of 768 numbers, an **embedding**. The
first few are printed.

**Why:** an embedding model places texts with similar meaning close
together. That is what lets the search in step 4 find a piece about "the
default model" even when it is worded differently from your question.

## 4. Search, and read before you ask (3 min)

**Do:** run **4. Find the pieces closest in meaning**, then **4b. Find the
pieces that share the most words**.

**Look for:** read the pieces **before** asking the model anything. Is the
answer in one of them? In which position? Do the two searches pick the same
pieces?

**Why:** search by meaning compares numbers; search by words counts shared
words, the way a search engine does. Either way, if the answer is not in the
retrieved pieces, no model can give it from them.

## 5. Open book (2 min)

**Do:** run **5. Ask with the documents**.

**Look for:** the printed prompt: the rules, the pieces with their ids, then
your question. Does the answer cite a piece, like `[p17]`? Compare it with
step 1.

**Why:** same model, same question. The only difference is what it was given
to read.

## 6. Check the citation (1 min)

**Do:** run **6. Show the cited pieces**.

**Look for:** is the answer really in the cited piece, in so many words?

**Why:** a citation turns "trust me" into something you can check in
seconds. A citation can also be wrong; checking is your job, not the model's.

## 7. A question the documents cannot answer (2 min)

**Do:** run **7. Ask something that is not in the documents**: "When is the
coffee break?"

**Look for:** there is no break in this workshop and the pages never mention
one. Does the model say "not in the documents", or invent a time?

**Why:** a good RAG answer admits when the documents are silent. Without the
rule to say so, many models fill the gap.

## 8. One piece or eight? (2 min)

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

Next: [Exercise 2 — Skills](../02-skills/README.md).
