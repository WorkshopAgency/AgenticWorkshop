# Exercise 4 — A decision model: typed answers with probabilities

| | |
|---|---|
| **Time** | 10 min |
| **Model** | `dtu/qwen36`; your data stays at DTU |
| **Needs** | `scripts/check-setup.sh --module 04-decide` passed. Python 3.10+, nothing to install. Nothing from other modules |
| **You'll learn** | How to get a yes/no, a choice or a score with a probability from a model, instead of a paragraph you have to interpret |
| **Done when** | You have run the three examples, compared a stated confidence with a token probability, and written one question of your own |
| **If stuck** | `/halp 04-decide <what you tried>` |

Agents make many small decisions: is this plot misleading, which tool next,
should a human look at this. Asking in prose and then reading the reply is
fragile. [`decide.py`](decide.py) asks a **typed** question instead and
reads the answer from the model's own probabilities.

## How it works

The model sees the description, the question and the options labelled A, B,
C…, and the prompt ends with `Answer:`. We ask for **one token** and for the
probabilities of the 20 most likely first tokens. The probabilities of the
option letters, rescaled to sum to 1, are the answer:

| Question type | You get |
|---|---|
| `yesno` | P(yes) |
| `choice` | a probability per option, and the most likely one |
| `score` | a probability per level, and the expected score |

The script also prints how much of the probability went to the option
letters at all. If that is low, the model wanted to say something else.

## 1. Run the three examples (3 min)

All three describe the same Palmer penguins plot of bill length against bill
depth. Pooled over all penguins the correlation is negative (−0.235); within
each species it is positive. Example 1 shows one colour and one line, example
2 adds a caption drawing the wrong conclusion, and example 3 colours by
species with one line each.

```bash
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/1-pooled-no-colour.txt
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/2-pooled-with-claim.txt
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/3-by-species.txt
```

Compare P(yes), the chosen fix and the expected severity. For example 3 the
right fix is `no_fix_needed`. A typed question can only return one of its
options; without a "none of these" option it would have to pick a fix.

## 2. Stated confidence versus probability (2 min)

```bash
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/1-pooled-no-colour.txt --stated --swap
```

`--stated` also asks for the answer in prose with a confidence from 0 to
100 %, and prints it next to the probability. `--swap` asks again with the
options in reverse order and shows how far the probabilities moved.

## 3. Write your own question (3 min)

```bash
mkdir -p outputs/04-decide
cp exercises/04-decide/questions.json outputs/04-decide/my-questions.json
```

Add a question to your copy, for example:

```json
{"id": "needs_legend", "type": "yesno", "text": "Does this plot need a legend?"}
```

```bash
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/3-by-species.txt --questions outputs/04-decide/my-questions.json
```

A `choice` question needs `options`, and a `score` question needs ordered
`levels`; see [`questions.json`](questions.json). If you did Exercise 3, you
can describe your own plot instead: `--state "A scatter plot of …"`.

**What to notice:** a probability over fixed options can be compared,
thresholded and logged; a paragraph has to be interpreted first. But a token
probability is not the probability of being right. It is how likely the
model was to write that letter, and if reversing the options moves it, the
answer depends on the layout of the prompt as well as on the plot. In an
agent pipeline this is useful for routing, for deciding when to stop and ask
a human, and for sorting many items by risk.

If the script says the reply contained no token probabilities, run
`scripts/check-setup.sh --module 04-decide` and tell an organiser.
`python3 exercises/04-decide/decide.py --help` lists the other options.

Next: [Exercise 5 — Safety](../05-safety/README.md).
