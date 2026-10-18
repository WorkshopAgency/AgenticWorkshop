# %% [markdown] Exercise 5 — A decision model, step by step
# Select a cell with the arrow keys and press r to run it, or enter to run it
# and move to the next one. Each cell prints the description it sends, then
# one table per question: the options, their probabilities, and the most likely
# option in green.

# %% Connect to the model
import sys
sys.path.insert(0, "exercises/05-decide")
import decide

decide.status()

# %% [markdown]
# Three descriptions of the same Palmer penguins plot: bill length against bill
# depth. Pooled over all penguins the correlation is negative; within each
# species it is positive. For each description the model answers three typed
# questions: could the plot mislead (yes or no), the best fix (one of five),
# and how severe the problem is (a score from 1 to 5).

# %% 5a · Example 1: one colour, one line
results1 = decide.run("exercises/05-decide/examples/1-pooled-no-colour.txt")

# %% 5a · Example 2: the same plot, with a caption that draws the wrong conclusion
results2 = decide.run("exercises/05-decide/examples/2-pooled-with-claim.txt")

# %% 5a · Example 3: coloured by species, one line each
results3 = decide.run("exercises/05-decide/examples/3-by-species.txt")

# %% [markdown]
# Example 1 again, asked two more ways. First the model answers in prose and
# writes its own confidence, shown next to the token probability. Then the
# options are asked in reverse order, to see how far the probabilities move.

# %% 5b · Stated confidence, and the options reversed
results5b = decide.run("exercises/05-decide/examples/1-pooled-no-colour.txt", stated=True, swap=True)

# %% [markdown]
# Your own question. A yes/no question needs an id, a type and a text. A choice
# question also needs options, and a score question ordered levels: see
# exercises/05-decide/questions.json. Change the question, or ask the agent to,
# and run the cell again. To ask about your own plot, put its description in
# place of the file name, in quotes.

# %% 5c · Your own question
my_questions = [
    {"id": "needs_legend", "type": "yesno", "text": "Does this plot need a legend?"},
]
mine = decide.run("exercises/05-decide/examples/3-by-species.txt", questions=my_questions)

# %% [markdown]
# Dive deeper: every question about all three descriptions, asked twice, with
# the options in their usual order and reversed. Look for "TOP ANSWER CHANGED".

# %% 5d · All three examples, options reversed
results5d = [decide.run(f"exercises/05-decide/examples/{name}", swap=True)
             for name in ("1-pooled-no-colour.txt", "2-pooled-with-claim.txt", "3-by-species.txt")]
