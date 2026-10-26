#!/usr/bin/env python3
"""Typed decisions from a chat model's token probabilities.

You give a STATE (a description of something) and a list of typed QUESTIONS.
For each question the model sees the options labelled A, B, C, ... and the
prompt ends with "Answer:". We ask for exactly one token and read the
probabilities the model gave to the letters A, B, C, ... (logprobs). Those
probabilities, renormalised over the option letters, are the decision:

    yesno   -> P(yes)
    choice  -> a probability for each option, and the most likely one
    score   -> a probability for each level, and the expected score

Only the Python standard library is used. The model is Llama 3.1 8B at
OpenRouter, with the workshop key in .openrouter-key in the workshop folder
(Exercise 0) or in OPENROUTER_API_KEY. With DECIDE_DTU=1, Qwenstorm (Qwen 3.6
at DTU) is used instead, when it is up. DECIDE_MODEL overrides the model.

The client appends /chat/completions to the base URL.
"""
import argparse
import json
import math
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

# the shared colours, by meaning (exercises/shared/look.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))
import look  # noqa: E402
import openrouter_key  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
USE_DTU = os.environ.get("DECIDE_DTU") == "1"
if USE_DTU:
    DECIDE_MODEL = os.environ.get("DECIDE_MODEL", "qwen36")
    DECIDE_URL = f"https://teaching.healthtech.dtu.dk/workshop/{DECIDE_MODEL}"
else:
    DECIDE_MODEL = os.environ.get("DECIDE_MODEL", "meta-llama/llama-3.1-8b-instruct")
    DECIDE_URL = "https://openrouter.ai/api/v1"
LETTERS = "ABCDEFGHIJ"

SYSTEM = ("You are a careful reviewer. Read the state, then answer the question "
          "with the letter of exactly one option.")
NO_LOGPROBS = ("The model's reply contained no token probabilities (logprobs), so a "
               "typed decision cannot be computed.\nThis model or gateway may not "
               "support logprobs. Run the setup check: scripts/check-setup.sh --module 05-decide")


# ---------------------------------------------------------------- HTTP helper

def workshop_key():
    return openrouter_key.read()


def tls():
    """Python sometimes ships without the computer's certificates; use the system's own file."""
    context = ssl.create_default_context()
    if not context.cert_store_stats()["x509_ca"]:
        for bundle in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"):
            if os.path.exists(bundle):
                context.load_verify_locations(bundle)
                break
    return context


def post_json(url, payload, timeout=120):
    """POST a JSON payload and return the decoded JSON reply."""
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if not USE_DTU:
        problem = openrouter_key.problem()
        if problem:
            sys.exit(problem)
        headers["Authorization"] = f"Bearer {workshop_key()}"
        # only providers that return token probabilities
        payload = {**payload, "provider": {"require_parameters": True}}
        payload.pop("chat_template_kwargs", None)
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=tls()) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", "replace")[:300]
        hint = ""
        if err.code == 400:
            hint = ("\nIf the error names an unknown parameter, try --keep-thinking "
                    "(drops chat_template_kwargs) and leave out --guided.")
        sys.exit(f"{url} answered HTTP {err.code}: {body}{hint}")
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        sys.exit(f"Could not reach {url}: {err}")


def status():
    """Say which model decides, and whether the key works."""
    where = "DTU" if USE_DTU else "OpenRouter"
    print(f"Decisions: {DECIDE_MODEL} at {where}.")
    if USE_DTU:
        return
    problem = openrouter_key.problem()
    if problem:
        print(look.warn(problem))
        return
    request = urllib.request.Request("https://openrouter.ai/api/v1/key",
                                     headers={"Authorization": f"Bearer {workshop_key()}"})
    try:
        with urllib.request.urlopen(request, timeout=30, context=tls()) as response:
            json.loads(response.read())
        print("The workshop key works.")
    except urllib.error.HTTPError as err:
        print(look.warn(f"The key was refused (HTTP {err.code}). Check .openrouter-key."))
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        print(look.warn(f"Could not reach OpenRouter: {err}. Check the network."))


# ------------------------------------------------------------------ questions

def load_state(value):
    """--state may be a file path or the text itself."""
    path = Path(value)
    return path.read_text(encoding="utf-8").strip() if path.is_file() else value


def options_for(question):
    """Return the question's options as a list of {label, text, value}."""
    kind = question["type"]
    if kind == "yesno":
        return [{"label": "yes", "text": "Yes", "value": None},
                {"label": "no", "text": "No", "value": None}]
    if kind == "choice":
        return [{"label": o["label"], "text": o.get("description", o["label"]), "value": None}
                for o in question["options"]]
    if kind == "score":
        return [{"label": str(level["value"]), "text": f"{level['value']}: {level['description']}",
                 "value": float(level["value"])} for level in question["levels"]]
    sys.exit(f"Question {question.get('id')}: unknown type '{kind}' (use yesno, choice or score)")


def check_questions(questions):
    """Stop early with a clear message if a question is malformed."""
    for question in questions:
        for key in ("id", "type", "text"):
            if key not in question:
                sys.exit(f"A question in the questions file has no '{key}': {question}")
        count = len(options_for(question))
        if not 2 <= count <= len(LETTERS):
            sys.exit(f"Question {question['id']} has {count} options; use 2 to {len(LETTERS)}.")


def option_lines(options):
    """Format options as 'A) ...' lines."""
    return "\n".join(f"{LETTERS[i]}) {o['text']}" for i, o in enumerate(options))


def build_messages(state, question, options, stated=False):
    """The prompt: state, question, lettered options, ending with 'Answer:'."""
    body = f"State:\n{state}\n\nQuestion: {question['text']}\n\nOptions:\n{option_lines(options)}\n\n"
    if stated:
        body += ("Give the letter of your answer and your confidence from 0 to 100% "
                 "that it is correct, in this format:\nAnswer: <letter>\nConfidence: <number>%")
    else:
        body += "Reply with one letter only.\nAnswer:"
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": body}]


# -------------------------------------------------------------- probabilities

def letter_probabilities(top_logprobs, letters):
    """Sum token probabilities per option letter.

    Tokenizers often have several tokens for one letter, e.g. "A" and " A"
    (with a leading space). We strip spaces and add their probabilities.
    Returns ({letter: probability}, coverage), where coverage is how much of
    the top-token probability fell on option letters at all.
    """
    raw = {letter: 0.0 for letter in letters}
    for item in top_logprobs:
        token = item["token"].strip().rstrip(").:")
        if token in raw:
            raw[token] += math.exp(item["logprob"])
    coverage = sum(raw.values())
    if coverage == 0:
        return None, 0.0
    return {letter: p / coverage for letter, p in raw.items()}, coverage


def request_distribution(messages, letters, args):
    """One constrained completion: max_tokens=1, temperature=0, top-20 logprobs."""
    payload = {"model": DECIDE_MODEL, "messages": messages, "max_tokens": 1,
               "temperature": 0, "logprobs": True, "top_logprobs": 20}
    if not args.keep_thinking:
        payload["chat_template_kwargs"] = {"enable_thinking": False}
    if args.guided:
        payload["structured_outputs"] = {"choice": list(letters)}
    reply = post_json(f"{DECIDE_URL}/chat/completions", payload)
    logprobs = (reply.get("choices") or [{}])[0].get("logprobs") or {}
    content = logprobs.get("content") or []
    if not content or not content[0].get("top_logprobs"):
        sys.exit(NO_LOGPROBS)
    top = content[0]["top_logprobs"]
    probs, coverage = letter_probabilities(top, letters)
    if probs is None:
        seen = ", ".join(repr(t["token"]) for t in top[:5])
        sys.exit(f"None of the option letters {', '.join(letters)} were among the top tokens "
                 f"(the most likely were {seen}). The model did not answer with a letter.\n"
                 "If that is a thinking token such as '<think>', this model or gateway "
                 "ignored the request to switch thinking off; try another DECIDE_MODEL.")
    return probs, coverage


def decide(state, question, args, reverse=False):
    """Ask one question; return {label: probability} and the letter coverage."""
    options = options_for(question)
    if reverse:
        options = options[::-1]
    letters = LETTERS[:len(options)]
    probs, coverage = request_distribution(build_messages(state, question, options), letters, args)
    distribution = {o["label"]: probs[letters[i]] for i, o in enumerate(options)}
    return distribution, coverage


def summarise(question, distribution):
    """Turn a distribution into the typed answer for this question type."""
    answer = max(distribution, key=distribution.get)
    result = {"id": question["id"], "type": question["type"], "question": question["text"],
              "distribution": distribution, "answer": answer}
    if question["type"] == "yesno":
        result["p_yes"] = distribution["yes"]
    if question["type"] == "score":
        result["expected"] = sum(float(label) * p for label, p in distribution.items())
    return result


def ask_stated(state, question, args):
    """Ask the same question in prose, with a stated confidence."""
    options = options_for(question)
    payload = {"model": DECIDE_MODEL, "temperature": 0, "max_tokens": 200,
               "messages": build_messages(state, question, options, stated=True)}
    if not args.keep_thinking:
        payload["chat_template_kwargs"] = {"enable_thinking": False}
    text = post_json(f"{DECIDE_URL}/chat/completions", payload)["choices"][0]["message"]["content"] or ""
    letter = re.search(r"Answer:\s*\(?([A-J])\b", text)
    confidence = re.search(r"Confidence:\s*(\d+(?:\.\d+)?)", text)
    index = LETTERS.index(letter.group(1)) if letter else None
    return {"text": text.strip(),
            "answer": options[index]["label"] if index is not None and index < len(options) else None,
            "confidence": float(confidence.group(1)) / 100 if confidence else None}


# --------------------------------------------------------------------- output

def print_result(result):
    """Readable table for one question: the most likely option in green."""
    print(f"{look.ident('[' + result['id'] + ']')} {result['type']}: {look.question(result['question'])}")
    labels = list(result["distribution"])
    rows = [[label, f"{p:.3f}", "#" * round(p * 30)] for label, p in result["distribution"].items()]
    table = look.table(rows, header=["option", "probability", ""], highlight=labels.index(result["answer"]))
    print("\n".join("    " + line for line in table.split("\n")))
    if "p_yes" in result:
        print(f"    P(yes) = {look.answer(format(result['p_yes'], '.3f'))}")
    if "expected" in result:
        print(f"    expected score = {look.answer(format(result['expected'], '.2f'))}")
    held = f"option letters held {result['coverage']:.1%} of the top-20 token probability"
    print("    " + (look.muted(held) if result["coverage"] > 0.5 else look.warn(held + ": low, treat with caution")))
    if "swapped" in result:
        swapped = result["swapped"]
        line = (f"reversed option order: most likely = {swapped['answer']}, "
                f"largest shift in any option = {swapped['shift']:.3f}")
        print("    " + (line if swapped["answer"] == result["answer"] else look.warn(line + "  (TOP ANSWER CHANGED)")))
    if "stated" in result:
        stated = result["stated"]
        token_p = result["distribution"].get(stated["answer"])
        print(f"    stated in prose: answer = {stated['answer']}, confidence = "
              f"{'?' if stated['confidence'] is None else format(stated['confidence'], '.0%')}"
              f"  | token probability of that answer = "
              f"{'?' if token_p is None else format(token_p, '.3f')}")
    print()


def run(state, questions=None, stated=False, swap=False, guided=False, keep_thinking=False, show=True):
    """Ask every question about the state; print a table per question and return the results.

    state: the text, or a file that holds it. questions: a list of questions, or a
    questions file (default: questions.json next to this script).
    """
    args = argparse.Namespace(guided=guided, keep_thinking=keep_thinking)
    state = load_state(str(state))
    if questions is None:
        questions = HERE / "questions.json"
    if isinstance(questions, (str, Path)):
        questions = json.loads(Path(questions).read_text(encoding="utf-8"))["questions"]
    check_questions(questions)
    if show:
        print(look.heading("STATE") + "\n" + look.muted(state) + "\n")
    results = []
    for question in questions:
        distribution, coverage = decide(state, question, args)
        result = summarise(question, distribution)
        result["coverage"] = coverage
        if swap:
            reversed_dist, _ = decide(state, question, args, reverse=True)
            shift = max(abs(reversed_dist[label] - p) for label, p in distribution.items())
            result["swapped"] = {"distribution": reversed_dist, "shift": shift,
                                 "answer": max(reversed_dist, key=reversed_dist.get)}
        if stated:
            result["stated"] = ask_stated(state, question, args)
        results.append(result)
        if show:
            print_result(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--state", required=True, help="a file with the state, or the text itself")
    parser.add_argument("--questions", default=str(HERE / "questions.json"))
    parser.add_argument("--stated", action="store_true", help="also ask in prose for a stated confidence")
    parser.add_argument("--swap", action="store_true", help="re-run with the option order reversed")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser.add_argument("--guided", action="store_true",
                        help="also send vLLM structured_outputs choice (some gateways reject it)")
    parser.add_argument("--keep-thinking", action="store_true",
                        help="do not send chat_template_kwargs to switch thinking off")
    args = parser.parse_args()

    if not args.json:
        print(f"Model '{DECIDE_MODEL}' at {DECIDE_URL}/chat/completions\n")
    results = run(args.state, args.questions, stated=args.stated, swap=args.swap,
                  guided=args.guided, keep_thinking=args.keep_thinking, show=not args.json)
    if args.json:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
