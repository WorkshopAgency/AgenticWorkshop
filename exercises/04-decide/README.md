# Exercise 04 — Typed decisions from token probabilities

| | |
|---|---|
| **Time** | 10 minutes |
| **Model** | `dtu/qwen36` (Qwen 3.6 35B-A3B); your data stays on the DTU server |
| **Needs** | Python 3.10+ (standard library only), a terminal in the workshop folder |
| **You'll learn** | How to get a yes/no, a choice or a score with a probability from a chat model, instead of parsing prose |
| **Done when** | You have run the three examples, compared a stated confidence with a token probability, and written one question of your own |
| **If stuck** | `/halp 04-decide` |

Agents often need small decisions: is this plot misleading, which tool comes
next, should a human look at this. Asking in prose and parsing the reply is
fragile. `decide.py` asks a **typed** question instead and reads the answer
from the model's token probabilities. This is a Jev-style "System One"
interface (state in, typed answers with probabilities out), built here on an
ordinary chat model so that it runs on the DTU models.

## How it works

For each question, the model sees the state, the question and the options
labelled with single letters, and the prompt ends with `Answer:`:

```
State:
A scatter plot from the Palmer penguins dataset ...

Question: Could this plot mislead a reader about the within-species relationship?

Options:
A) Yes
B) No

Reply with one letter only.
Answer:
```

The request asks for **one token** (`max_tokens=1`, `temperature=0`) plus
the 20 most likely first tokens with their log-probabilities
(`logprobs=true`, `top_logprobs=20`). The script adds up the probability of
each letter, including variants with a leading space (`"A"` and `" A"`), and
rescales them to sum to 1:

| Type | Result |
|---|---|
| `yesno` | P(yes) (yes and no are options A and B) |
| `choice` | a probability per option, and the most likely one |
| `score` | a probability per level, and the expected score |

It also prints how much of the top-20 probability fell on the option letters
at all. If that is low, the model wanted to say something else first; treat
the result with caution.

## The examples

All three describe the same Palmer penguins plot: bill length against bill
depth for the 342 penguins with both measurements. Pooled over all penguins,
the correlation is negative (r = -0.235). Within each species it is positive
(Adelie +0.39, Chinstrap +0.65, Gentoo +0.64): a Simpson's paradox. These
numbers were recomputed from the public `palmerpenguins` CSV.

| File | Plot | Intended verdict |
|---|---|---|
| `examples/1-pooled-no-colour.txt` | one colour, one regression line | misleading |
| `examples/2-pooled-with-claim.txt` | same, caption says "longer bills mean shallower bills" | misleading |
| `examples/3-by-species.txt` | coloured by species, a line and n per species | sound |

## Steps

### 1. Run the three examples (3 min)

```bash
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/1-pooled-no-colour.txt
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/2-pooled-with-claim.txt
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/3-by-species.txt
```

Compare P(yes), the chosen fix and the expected severity across the three.
For example 3 the right fix is `no_fix_needed`. A typed question can only
return one of its options, so a choice without a "none of these" option would
force an answer. Check how much probability that option gets.

### 2. Stated confidence versus token probability (2 min)

```bash
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/1-pooled-no-colour.txt --stated --swap
```

`--stated` also asks the question in prose ("give your confidence 0–100%")
and prints that next to the token probability of the same answer. `--swap`
asks again with the options in reverse order and reports how far the
probabilities moved.

### 3. Write your own question (3 min)

Copy `questions.json`, add a question and run it with `--questions`:

```json
{"id": "needs_legend", "type": "yesno", "text": "Does this plot need a legend?"}
```

```bash
mkdir -p outputs/04-decide
cp exercises/04-decide/questions.json outputs/04-decide/my-questions.json
python3 exercises/04-decide/decide.py --state exercises/04-decide/examples/3-by-species.txt --questions outputs/04-decide/my-questions.json
```

A `choice` question needs `options` (each with `label` and `description`);
a `score` question needs ordered `levels` (each with `value` and
`description`). Up to 10 options. Add `--json` for output a program can read.

### 4. Optional: your own plot

Describe a plot you made earlier in the workshop in a few sentences of plain
text and pass the text directly:

```bash
python3 exercises/04-decide/decide.py --state "A bar chart of ... The caption reads ..."
```

## Discussion (2 min)

- **Typed versus prose.** A probability over fixed options can be compared,
  thresholded and logged. A paragraph has to be parsed first.
- **A token probability is not calibrated truth.** It is how likely the model
  was to write that letter next. Compare it with the stated confidence, and
  with your own judgement.
- **Order sensitivity.** If reversing the options moves the answer, the
  decision depends on the prompt layout as well as the content.
- **Where it fits.** Routing (which agent or tool next), gating (stop or ask
  a human below a threshold) and triage (sort many items by risk) in agent
  pipelines. One short request per decision.

## If something goes wrong

- *"The model's reply contained no token probabilities"*: the model or gateway
  does not return logprobs. Run `scripts/check-setup.sh --module 04-decide`.
- *"None of the option letters ... were among the top tokens"*: the model
  started with something else, often a thinking token. The script asks Qwen
  to switch thinking off (`chat_template_kwargs`); this model or gateway did
  not honour it. Try another `DECIDE_MODEL`.
- *HTTP 400 naming an unknown parameter*: add `--keep-thinking` (sends only
  standard OpenAI parameters) and leave out `--guided`.
- `--guided` additionally sends vLLM's `structured_outputs` choice so that
  only option letters can be generated. Some gateways reject it.

## Verification status

**Verified** (against a local mock server that imitates the DTU endpoints,
13 October 2026): the request (one token, temperature 0, top-20 logprobs,
prompt ending with `Answer:`), summing leading-space token variants,
rescaling over the option letters, P(yes), the most likely choice, the
expected score, `--swap`, `--stated`, `--guided`, `--json`, and the error
messages for missing logprobs, missing option letters, a rejected parameter
and an unreachable server. The penguin numbers were checked against the
public dataset.

**Not yet verified** (needs the live DTU models):
- Whether the DTU gateway passes `logprobs` and `top_logprobs` through to
  vLLM and returns them.
- Whether Qwen 3.6 answers with a letter as its first token, and whether
  `chat_template_kwargs: {"enable_thinking": false}` is accepted and honoured.
- Whether `--guided` (`structured_outputs`) is accepted, and whether the
  returned logprobs are taken before or after that constraint.
- The model's actual verdicts on the three examples, and how large the
  `--swap` shift is.

## Settings

| Variable | Default | Meaning |
|---|---|---|
| `DTU_BASE` | `https://teaching.healthtech.dtu.dk/workshop` | Root of the model URLs |
| `DECIDE_MODEL` | `qwen36` | Model; requests go to `$DTU_BASE/$DECIDE_MODEL/chat/completions` |
| `DECIDE_URL` | derived from the above | Full base URL, for any other OpenAI-compatible server |
