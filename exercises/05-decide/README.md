# Exercise 5 — A decision model: typed answers with probabilities

| | |
|---|---|
| **Model** | Llama 3.1 8B at OpenRouter, with the workshop key |
| **Needs** | The workshop key from Exercise 0, and `scripts/check-setup.sh --module 05-decide` passed. Python 3.10+, nothing to install |
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

This exercise runs in an ordinary terminal, from the workshop folder: you
call the model directly, so you can see exactly what you get back. The model
runs at OpenRouter with the workshop key from Exercise 0, so the descriptions
you send leave your laptop; they are made up for the exercise.

## 1. Run the three examples

**Do:**

```bash
python3 exercises/05-decide/decide.py --state exercises/05-decide/examples/1-pooled-no-colour.txt
python3 exercises/05-decide/decide.py --state exercises/05-decide/examples/2-pooled-with-claim.txt
python3 exercises/05-decide/decide.py --state exercises/05-decide/examples/3-by-species.txt
```

**Look for:** all three describe the same Palmer penguins plot of bill length
against bill depth. Pooled over all penguins the correlation is negative
(−0.235); within each species it is positive. Example 1 shows one colour and
one line, example 2 adds a caption drawing the wrong conclusion, and example
3 colours by species with one line each. Compare P(yes), the chosen fix and
the expected severity across the three. The script also prints how much of
the probability went to the option letters at all; if that is low, the model
wanted to say something else.

**Why:** for example 3 the right fix is `no_fix_needed`. A typed question can
only return one of its options; without a "none of these" option it would
have to pick a fix. Designing the options is part of designing the decision.

## 2. Stated confidence versus probability

**Do:**

```bash
python3 exercises/05-decide/decide.py --state exercises/05-decide/examples/1-pooled-no-colour.txt --stated --swap
```

**Look for:** `--stated` asks for the answer in prose with a confidence from 0
to 100 %, and prints it next to the probability. `--swap` asks again with the
options in reverse order and shows how far the probabilities moved.

**Why:** a confidence the model *writes* is just more generated text. A token
probability is measured, but it is still not the probability of being right:
it is how likely the model was to write that letter. If reversing the options
moves it, the answer depends on the layout of the prompt as well as on the
plot.

## 3. Write your own question

**Do:**

```bash
mkdir -p outputs/05-decide
cp exercises/05-decide/questions.json outputs/05-decide/my-questions.json
```

Add a question to your copy, for example:

```json
{"id": "needs_legend", "type": "yesno", "text": "Does this plot need a legend?"}
```

```bash
python3 exercises/05-decide/decide.py --state exercises/05-decide/examples/3-by-species.txt --questions outputs/05-decide/my-questions.json
```

**Look for:** a `choice` question needs `options`, and a `score` question needs
ordered `levels`; see [`questions.json`](questions.json). If you did
Exercise 4, describe your own plot instead: `--state "A scatter plot of …"`.

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

If the script says the reply contained no token probabilities, run
`scripts/check-setup.sh --module 05-decide` and tell an organiser.
`python3 exercises/05-decide/decide.py --help` lists the other options.

Next: [Exercise 6 — Safety](../06-safety/README.md).
