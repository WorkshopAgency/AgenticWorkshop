# %% [markdown] Exercise 1 — RAG, step by step
# Select a cell with the arrow keys and press r to run it. Go from top to
# bottom: each cell uses what the cells above it made. The grey lines are the
# code (the input); below them is what it printed (the output).

# %% Connect to the models
import sys
sys.path.insert(0, "exercises/01-rag")
import rag

rag.status()

# %% [markdown]
# First, the model on its own. It has never seen this workshop's pages, so it
# can only answer from what it learned in training. Watch how sure it sounds.

# %% 1a · Ask the model on its own
question = "Which chat model is the default in this workshop?"
closed = rag.answer(question)

# %% [markdown]
# The documents are this workshop's pages. A model can only be given a few
# pieces at a time, so we cut the pages at headings and paragraphs.

# %% 1b · Cut the pages into pieces
pieces = rag.cut()

# %% [markdown]
# An embedding model turns each piece into a long list of numbers that
# captures its meaning. Pieces about similar things get similar numbers.

# %% 1c · Turn the pieces into numbers
index = rag.embed(pieces)

# %% [markdown]
# The question is turned into numbers too, and the closest pieces win. Read
# them before you ask the model anything: is the answer in there? Then the
# same search by shared words, the way a search engine does it.

# %% 1d · Find the pieces closest in meaning
hits = rag.find(question, index, k=3)

# %% 1d · Find the pieces that share the most words
word_hits = rag.find(question, index, k=3, words=True)

# %% [markdown]
# Now the same question, with the pieces and strict rules: answer only from
# the pieces, and cite them. Compare with the answer in 1a.

# %% 1e · Ask with the documents
reply = rag.answer(question, hits)

# %% [markdown]
# A citation is a claim. Here are the cited pieces in full: is the answer
# really in them?

# %% 1f · Show the cited pieces
rag.cited(reply, hits)

# %% [markdown]
# There is no coffee break in this workshop, and the pages never mention one.
# Does the model say so, invent a time, or answer a different question? If it
# answers something else, read the pieces it was given: one may contain an
# instruction, and a small model can follow it instead of your question.

# %% 1g · Ask something that is not in the documents
q7 = "When is the coffee break?"
reply7 = rag.answer(q7, rag.find(q7, index, k=3))

# %% [markdown]
# How many pieces you send is a trade-off: too few can miss half the answer,
# too many add noise and cost. Run both and compare.

# %% 1h · Send one piece
q8 = "What are the three lessons of this workshop?"
reply8a = rag.answer(q8, rag.find(q8, index, k=1))

# %% 1h · Send eight pieces
reply8b = rag.answer(q8, rag.find(q8, index, k=8))
