# %% [markdown] Exercise 1 — RAG, step by step
# Select a cell with the arrow keys and press r to run it. Go from top to
# bottom: each cell uses what the cells above it made. The grey lines are the
# code (the input); below them is what it printed (the output).

# %% Connect to the models
import sys
sys.path.insert(0, "exercises/01-rag")
import rag

rag.status()

# %% [markdown] Step 1 · Closed book
# First, the model on its own. It has never seen this workshop's pages, so it
# can only answer from what it learned in training. Watch how sure it sounds.

# %% 1. Ask without the documents
question = "Which chat model is the default in this workshop?"
closed = rag.answer(question)

# %% [markdown] Step 2 · Cut the documents into pieces
# The documents are this workshop's pages. A model can only be given a few
# pieces at a time, so we cut the pages at headings and paragraphs.

# %% 2. Cut the pages into pieces
pieces = rag.cut()

# %% [markdown] Step 3 · Turn each piece into numbers
# An embedding model turns each piece into a long list of numbers that
# captures its meaning. Pieces about similar things get similar numbers.

# %% 3. Turn the pieces into numbers
index = rag.embed(pieces)

# %% [markdown] Step 4 · Search
# The question is turned into numbers too, and the closest pieces win. Read
# them before you ask the model anything: is the answer in there? Then the
# same search by shared words, the way a search engine does it.

# %% 4. Find the pieces closest in meaning
hits = rag.find(question, index, k=3)

# %% 4b. Find the pieces that share the most words
word_hits = rag.find(question, index, k=3, words=True)

# %% [markdown] Step 5 · Open book
# Now the same question, with the pieces and strict rules: answer only from
# the pieces, and cite them. Compare with step 1.

# %% 5. Ask with the documents
reply = rag.answer(question, hits)

# %% [markdown] Step 6 · Check the citation
# A citation is a claim. Here are the cited pieces in full: is the answer
# really in them?

# %% 6. Show the cited pieces
rag.cited(reply, hits)

# %% [markdown] Step 7 · A question the documents cannot answer
# There is no coffee break in this workshop, and the pages never mention one.
# Does the model say so, or invent a time?

# %% 7. Ask something that is not in the documents
q7 = "When is the coffee break?"
reply7 = rag.answer(q7, rag.find(q7, index, k=3))

# %% [markdown] Step 8 · One piece or eight?
# How many pieces you send is a trade-off: too few can miss half the answer,
# too many add noise and cost. Run both and compare.

# %% 8a. One piece
q8 = "How long is Exercise 3, and what are its parts?"
reply8a = rag.answer(q8, rag.find(q8, index, k=1))

# %% 8b. Eight pieces
reply8b = rag.answer(q8, rag.find(q8, index, k=8))
