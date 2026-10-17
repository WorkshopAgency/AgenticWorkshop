"""How the exercise scripts colour what they print, by meaning.

A script says what a piece of text is: a heading, a question, an answer, an
id, context to skim, or a warning. This file is the only place that decides
how each of those looks. The notebook panel, a terminal and Jupyter all show
the colours; NO_COLOR=1 turns them off.

    import look
    print(look.question("Question: Which model is the default?"))
    print(look.answer("Big Pickle"))
    print(look.table([["yes", "0.91"], ["no", "0.09"]], header=["option", "p"], highlight=0))

Only the Python standard library is used.
"""
import os

COLOUR = not os.environ.get("NO_COLOR")

# meaning -> terminal colour code (ANSI SGR)
STYLES = {
    "heading": "1",        # bold: section labels such as "ANSWER FROM ..."
    "question": "1;33",    # bold yellow: the question being asked
    "answer": "32",        # green: the model's answer, or the most likely option
    "ident": "36",         # cyan: ids, sources and labels you can look up
    "muted": "90",         # grey: context you may skim
    "warn": "31",          # red: something to check
}


def paint(style, text):
    """Text in the colour of a meaning from STYLES."""
    return f"\033[{STYLES[style]}m{text}\033[0m" if COLOUR else str(text)


def heading(text):
    return paint("heading", text)


def question(text):
    return paint("question", text)


def answer(text):
    return paint("answer", text)


def ident(text):
    return paint("ident", text)


def muted(text):
    return paint("muted", text)


def warn(text):
    return paint("warn", text)


def _numeric(cell):
    """True for a number such as 0.731 or 45%, which the table right-aligns."""
    try:
        float(str(cell).rstrip("%"))
        return True
    except ValueError:
        return False


def table(rows, header=None, highlight=None):
    """Rows as aligned columns: numbers right-aligned, the header in bold, and
    row number `highlight` (0-based) shown as the answer."""
    # every cell as text, so its printed length can be measured
    rows = [[str(cell) for cell in row] for row in rows]
    # the header counts too when the column widths are worked out
    every = rows + ([list(map(str, header))] if header else [])
    # each column as wide as its longest cell; a short row just has fewer columns
    widths = [max(len(row[i]) for row in every if i < len(row)) for i in range(max(map(len, every)))]

    def line(row):
        # pad each cell to its column width (numbers on the right, text on the
        # left), two spaces between columns, no spaces left at the end
        return "  ".join(cell.rjust(w) if _numeric(cell) else cell.ljust(w) for cell, w in zip(row, widths)).rstrip()

    # the header in bold, then the rows; the highlighted row in the answer colour
    out = [heading(line(list(map(str, header))))] if header else []
    out += [answer(line(row)) if i == highlight else line(row) for i, row in enumerate(rows)]
    return "\n".join(out)
