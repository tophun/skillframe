---
name: commit
description: Group the current working-tree changes by common unit of work and create a separate Git commit for each group after inspecting status, diff, branch, and recent history. Stage only files belonging to each work unit and use concise repository-consistent commit messages. Use when the user asks to commit changes, save the current work in Git, or invokes `$commit`; do not push, open a PR, amend, rebase, or delete files unless explicitly requested.
---

# Commit

Create a series of Git commits by grouping the changes the user has placed in scope into coherent, independently understandable units of work.

## Workflow

1. Inspect the repository:
   - `git status --short`
   - `git diff HEAD`
   - `git branch --show-current`
   - `git log --oneline -10`
2. Stop if there are no relevant changes.
3. Group changes by common unit of work, keeping each group independently understandable and reviewable. Separate unrelated edits, generated files, secrets, and local artifacts. Do not force all related files into one commit merely because they are part of the same broad task.
4. Read repository-local instructions and follow the repository's commit convention. Prefer one concise imperative or Conventional Commit message that describes the actual change.
5. Run a focused check when the change warrants it. Report checks that were not run and why.
6. For each work unit, stage explicit paths, inspect the staged diff, and create one commit with a concise message. Commit in dependency order when one work unit depends on another.
7. Verify each commit and then verify the final state with `git status --short` and `git log --oneline`.

## Guardrails

- Do not use `git add -A` or `git commit -am` when unrelated or untracked files may exist.
- Do not combine separate work units into one commit just to minimize the commit count.
- Do not include credentials, environment files, editor metadata, or generated output unless the user explicitly includes them.
- Do not push, create a branch, open a PR, amend, rebase, reset, or delete files in this skill.
- If the work-unit grouping, intended scope, or commit messages are ambiguous, show the proposed groups, files, and messages before staging.

## Report

Return each commit hash, message, work-unit grouping, committed paths, checks run, and any intentionally excluded files.
