# Answer key (TEMPLATE)

Fill this in once the real corpus is chosen (see `CORPUS.md`). Chunk ids
assume the default `chunk` settings (`--size 800 --overlap 150`). If you
re-chunk with other settings, the ids change.

Types:
- **answerable**: the answer is stated in one place.
- **conflict**: two passages disagree, so a good answer names both and cites both.
- **unanswerable**: the answer is not in the corpus; the correct reply is "not in the documents".

## Real corpus

| # | Question | Expected answer | Source chunk(s) | Type |
|---|---|---|---|---|
| 1 | | | | answerable |
| 2 | | | | answerable |
| 3 | | | | conflict |
| 4 | | | | unanswerable |

## PLACEHOLDER corpus (for testing `rag.py` only)

These rows match the invented Glimmerfen files in `corpus/`. Chunk ids were
read from `chunks.jsonl` after running `chunk` with the default settings.

| # | Question | Expected answer | Source chunk(s) | Type |
|---|---|---|---|---|
| P1 | How deep is each moss core? | 14 centimetres | c2 (2019), c4 (2024) | answerable |
| P2 | How long are moss cores dried before weighing? | 48 hours since the 2024 edition; the 2019 edition said 36 hours | c2 (2019: 36 h), c4 (2024: 48 h) | conflict |
| P3 | What is the minimum group size on the bog? | 3 people since 2024; 2 people in 2019 | c3 (2019), c5 (2024) | conflict |
| P4 | Who funds the Glimmerfen Moss Station? | not in the documents | none | unanswerable |
