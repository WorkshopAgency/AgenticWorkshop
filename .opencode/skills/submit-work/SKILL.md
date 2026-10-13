---
name: submit-work
description: Share a skill, agent or MCP configuration to the workshop repository as a pull request. Use when the user wants to submit, publish or push their own work to the shared workshop repo, not for general git work in an unrelated project.
---

# Submit work to the workshop repository

Publish the user's own skill, agent or MCP configuration into
`_sectionday/exercises/04-share/submissions/<name>/` in the workshop repository, as a
pull request from their fork.

Publishing is public and hard to take back. A deleted commit stays in the
fork's history and in anyone's clone. Check before pushing, not after.

## Establish what is being shared

Identify the files the user actually wants to share, and where they are. A
skill is a folder with `SKILL.md`; an agent is one Markdown file; an MCP
contribution is the server block from `opencode.json` plus notes. Copy them
into `_sectionday/exercises/04-share/submissions/<name>/` — do not move them, so the
user's working setup keeps running.

Choose `<name>` with the user. Use their name or GitHub handle, lowercase
with hyphens, or their assigned `team-01` through `team-10` folder.
Never write into another person's submission folder, and never
modify files elsewhere in the repository.

## Check before publishing, and show the user

Run these and report the results before committing anything:

1. **What would be committed.** `git status --short` and `git diff --cached`.
   Read the actual file list. Do not rely on your own expectation of it.

2. **Nothing is silently ignored.** The repository's `.gitignore` excludes
   common folder names, so a submission in a folder called `build`, `dist`,
   `lib`, `var`, `target`, `venv`, `env`, `downloads`, `sdist`, `wheels` or
   `eggs` disappears without any error. Verify every intended file:

   ```bash
   git check-ignore -v _sectionday/exercises/04-share/submissions/<name>/*
   ```

   No output means nothing is ignored. Any output names a file that will not
   ship. Rename the folder rather than editing the shared `.gitignore`.

3. **No credentials.** Search the staged files for API keys, tokens,
   passwords and personal paths. The workshop keeps keys out of the
   repository. If anything looks like a secret, stop and tell the user.

4. **No large or generated files.** Databases, caches, `node_modules`,
   downloaded datasets and build products do not belong in a submission.
   State the total size. Anything over a few hundred KB needs a reason.

5. **It is self-contained.** A skill folder needs its `SKILL.md` and any
   file it references. Copying `SKILL.md` alone leaves a skill incomplete.

Report what each check found. Distinguish checks that passed, that failed,
and that you could not run.

## Publish

Students do not have write access to the workshop repository, so the work
goes through a fork. Offer ordinary Git and the GitHub website first; `gh`
is optional. Check whether this is a clone or ZIP, the current branch,
`git remote -v`, and staged changes. Do not include unrelated staged work.

### Ordinary Git + website

Ask the user to create a fork with GitHub's Fork button. In a fresh location,
clone that fork and enter it (substitute the actual fork owner):

```bash
git clone https://github.com/YOUR-USER/AgenticWorkshop.git
cd AgenticWorkshop
git switch -c submit-<name>
```

If already in an appropriate clone, do not clone again. If starting from a
ZIP, copy only the agreed submission files into the fork clone's submissions
folder. Keep all content edits limited to that folder. Run the checks above,
then, with approval:

```bash
git add _sectionday/exercises/04-share/submissions/<name>/
git diff --cached
git commit -m "Add <name> submission: <what it is>"
git push -u origin submit-<name>
```

Ask the user to open Compare & pull request on GitHub: their fork's branch
into peterwadsackett/AgenticWorkshop, base main. Until they create it, report
that the branch was pushed but the PR is pending; never invent a PR URL.

### Optional GitHub CLI

If the user prefers `gh` and it is authenticated, it can create the fork and
pull request instead. Verify the working directory and remote after cloning:

```bash
gh repo fork <workshop-repo> --clone --remote      # once
cd AgenticWorkshop                              # enter the new clone
git checkout -b submit-<name>
git add _sectionday/exercises/04-share/submissions/<name>
git commit -m "Add <name> submission: <what it is>"
git push -u origin submit-<name>
gh pr create --title "..." --body "..."
```

Ask before the push and before creating the pull request: those two steps are
the ones that publish. If `gh` is missing or not authenticated, use the
ordinary Git + website route above. Never install tools or change credentials
without the user's approval.

Commit only the submission folder. Never use `git push --force`,
`git reset --hard`, or any command that rewrites shared history. If the push
is rejected, report the error and let the user decide.

## Hand over

Give the user the pull request URL, list what was included, and state
anything you did not check. Do not claim the submission was accepted — it has
been proposed, and someone still has to merge it.
