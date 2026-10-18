# Exercise 5 — A decision model: typed answers with probabilities

| | |
|---|---|
| **Model** | Llama 3.1 8B at OpenRouter, with the workshop key |
| **Needs** | Exercise 0: the notebook plugin and the workshop key. `scripts/check-setup.sh --module 05-decide` passed |
| **You'll learn** | How to get a yes/no, a choice or a score with a probability from a model, instead of a paragraph you have to interpret |
| **Done when** | You have run the three examples, compared a stated confidence with a token probability, and written one question of your own |
| **If stuck** | `/halp 05-decide <what you tried>` |

## Why a decision model

Agents make many small decisions: is this plot misleading, which tool next,
should a human look at this. Asking in prose and then reading the reply is
fragile: "probably not, although…" is hard for a program to act on, and hard
to compare across a hundred cases.

A **decision model** answers a *typed* question (yes/no, one of a few
choices, a score) and gives a probability with it. Some models are built for
this. Here we get the same kind of answer from an ordinary chat model,
[`decide.py`](decide.py), by reading the model's own probabilities instead of
its words.

How it works: the model sees a description, the question and the options
labelled A, B, C…, and the prompt ends with `Answer:`. We ask for **one
token** and for the probabilities of the 20 most likely first tokens. The
probabilities of the option letters, rescaled to sum to 1, are the answer:

| Question type | You get |
|---|---|
| `yesno` | P(yes) |
| `choice` | a probability per option, and the most likely one |
| `score` | a probability per level, and the expected score |

## Before you start

You need the notebook plugin and the workshop key from
[Exercise 0](../00-plugins/README.md). Start a new chat in OpenCode and type:

```
/notebook exercises/05-decide/decide_notebook.py
```

Run the first cell, **Connect to the model**. It should say that the workshop
key works. The model runs at OpenRouter, so the descriptions you send leave
your laptop; they are made up for the exercise. Each step below is one or
more cells; the code is short, and the steps themselves are plain Python in
[`decide.py`](decide.py).

# Exercise 5a — Run the three examples

**Do:** run the three **5a** cells: **Example 1: one colour, one line**,
**Example 2: …** and **Example 3: …**.

**Look for:** all three describe the same Palmer penguins plot of bill length
against bill depth. Pooled over all penguins the correlation is negative
(−0.235); within each species it is positive. Example 1 shows one colour and
one line, example 2 adds a caption drawing the wrong conclusion, and example
3 colours by species with one line each. Compare P(yes), the chosen fix and
the expected severity across the three. Each table also says how much of
the probability went to the option letters at all; if that is low, the model
wanted to say something else.

**Why:** for example 3 the right fix is `no_fix_needed`. A typed question can
only return one of its options; without a "none of these" option it would
have to pick a fix. Designing the options is part of designing the decision.

# Exercise 5b — Stated confidence versus probability

**Do:** run **5b · Stated confidence, and the options reversed**.

**Look for:** the model answers in prose with a confidence from 0 to 100 %,
printed next to the token probability ("stated in prose"). Then it is asked
again with the options in reverse order, and the table says how far the
probabilities moved.

**Why:** a confidence the model *writes* is just more generated text. A token
probability is measured, but it is still not the probability of being right:
it is how likely the model was to write that letter. If reversing the options
moves it, the answer depends on the layout of the prompt as well as on the
plot.

# Exercise 5c — Write your own question

**Do:** run **5c · Your own question**. It asks one question of its own:

```python
{"id": "needs_legend", "type": "yesno", "text": "Does this plot need a legend?"}
```

Change the text, or add a question to the list, and run the cell again. You
can ask the agent in the chat to make the edit for you.

**Look for:** a `choice` question needs `options`, and a `score` question needs
ordered `levels`; see [`questions.json`](questions.json). If you did
Exercise 4, describe your own plot instead: put its description, in quotes,
in place of the file name.

**Why:** the question decides what you can learn. A yes/no is easy to act on;
a score shows how sure the model is spread across levels.

## What to notice

- A probability over fixed options can be compared, thresholded and logged;
  a paragraph has to be interpreted first.
- A token probability is not the chance of being right, and option order can
  move it.
- In an agent pipeline this fits routing (which tool or agent next), gating
  (stop and ask a human below a threshold) and triage (sort many items by
  risk).

**Discuss with your neighbour:**

1. Which decision in your own analysis would you hand to a typed question,
   and which never?
2. At what probability would you let a pipeline continue without a human?
3. How would you check whether the probabilities can be trusted on your data?

If a cell says the reply contained no token probabilities, run
`scripts/check-setup.sh --module 05-decide` and tell an organiser.

# === Dive Deeper ===

# Exercise 5d — Can a token probability be trusted?

**Do:** run **5d · All three examples, options reversed**. It asks every
question about all three descriptions twice: with the options in their usual
order, and reversed.

**Look for:** for which questions does the top answer change when only the
order of the options changes ("TOP ANSWER CHANGED")? How far do the
probabilities move?

**Why:** models prefer some option positions or letters regardless of what
the options say ([Zheng et al., 2023](https://arxiv.org/abs/2309.03882);
[Pezeshkpour and Hruschka, 2023](https://arxiv.org/abs/2308.11483)). Asking
in several orders and averaging is a simple defence; Zheng et al. also
propose a correction, PriDe.

A probability is **calibrated** when, of all answers given with 0.8, about
80 % turn out right. Modern neural networks are often over-confident
([Guo et al., 2017](https://arxiv.org/abs/1706.04599)). Large language models
can be well calibrated on multiple-choice and true/false questions *in the
right format* ([Kadavath et al., 2022](https://arxiv.org/abs/2207.05221)),
which is the format `decide.py` uses. Training a model to follow instructions
can weaken that: the GPT-4 report measured calibration from the probabilities
of the letters A–D, as `decide.py` does, and found the pre-trained model well
calibrated and the final model much less so
([OpenAI, 2023](https://arxiv.org/abs/2303.08774), Figure 8).

To find out on your own decisions: label 20 cases yourself, run them, and
count how many of the answers given with more than 0.8 were right.

Previous: [Exercise 4 — MCP](../04-mcp/README.md) · Next: [Exercise 6 — Safety](../06-safety/README.md).
