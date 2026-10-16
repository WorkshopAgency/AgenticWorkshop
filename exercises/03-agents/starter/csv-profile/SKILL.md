---
name: csv-profile
description: Profile a CSV or CSV.GZ table before analysing it - rows, columns, inferred types, missing values including text markers such as NA, and counts per group. Use before computing statistics on a table you have not checked.
---

# csv-profile

Profile a table before anyone trusts numbers computed from it.

## Run

```bash
python3 .opencode/skills/csv-profile/profile.py <file.csv|file.csv.gz> [--group COLUMN] [--out outputs/<folder>/profile.md]
```

The script uses only the Python standard library. It prints the report and,
with `--out`, also writes it as Markdown.

## Report to the user

- Rows and columns, and the inferred type of each column.
- Missing values per column. Count empty cells **and** text markers
  (`NA`, `N/A`, `null`, `None`, `-`, `?`) separately, and say which markers
  were found. A numeric column that contains a marker will be read as text
  by many tools.
- Counts per group when a group column was given.
- Units and meanings only when a provenance file next to the data states
  them. Otherwise say they are unknown; do not guess.

## Rules

- Never modify the input file.
- If the file does not exist or cannot be parsed, say so and stop. Do not
  produce a profile of something else.
- Report what the script printed. Do not round away or omit missing-value
  counts.
