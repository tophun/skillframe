---
name: commit
description: Group the current working-tree changes by common unit of work and create Git commits after inspecting status, diff, branch, and recent history. When a work unit has the same purpose as an unpushed local commit, prefer amending or autosquashing into that commit; keep different purposes separate. Use when the user asks to commit changes, save the current work in Git, or invokes `$commit`; do not push, open a PR, or rewrite shared history.
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
5. Before creating a new commit, compare the work unit with recent commits on the current branch.
   - If it completes or directly follows the same feature, bug fix, refactor, test, or documentation change, prefer merging it into that commit.
   - If the matching commit is `HEAD`, stage the work unit and use `git commit --amend`.
   - If the matching commit is older but still local and unpushed, use `git commit --fixup=<sha>` followed by `git rebase -i --autosquash <sha>^`. Show the target SHA, reason, and rewritten commit list before executing it.
   - If the purpose differs, create a separate commit even when the files or branch are related.
   - If the matching commit is already pushed or shared, do not rewrite it; create a follow-up commit unless the user explicitly requests history rewriting.
6. Run a focused check when the change warrants it. Report checks that were not run and why.
7. For each work unit, stage explicit paths, inspect the staged diff, and create one commit with a concise message. Commit in dependency order when one work unit depends on another.
8. Verify each commit and then verify the final state with `git status --short` and `git log --oneline`.

## Guardrails

- Do not use `git add -A` or `git commit -am` when unrelated or untracked files may exist.
- Do not combine separate work units into one commit just to minimize the commit count.
- Do not include credentials, environment files, editor metadata, or generated output unless the user explicitly includes them.
- Do not push, create a branch, or open a PR in this skill.
- Do not amend or rebase pushed/shared history. Use amend or fixup/autosquash only for a matching unpushed local commit after the rewrite target and result are shown for approval.
- Do not reset or delete files.
- If the work-unit grouping, intended scope, or commit messages are ambiguous, show the proposed groups, files, and messages before staging.

## Report

Return each commit hash, message, work-unit grouping, committed paths, any rewritten commit SHA, checks run, and intentionally excluded files.
