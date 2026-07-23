---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git log:*), Bash(git commit:*)
description: Group current changes by common work unit and create separate git commits
---

## Context

- Current git status: !`git status --short`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Task

Based on the current changes, group them by common work unit and create a separate Git commit for each coherent group.

1. Identify coherent work units and separate them from unrelated files, local metadata, secrets, and generated output.
2. Show the proposed work-unit groups, paths, and commit messages when the grouping is ambiguous.
3. Stage only the paths for one work unit at a time; do not use `git add -A` when unrelated files exist.
4. Use one concise, repository-consistent imperative or Conventional Commit message per work unit.
5. Before creating a new commit, compare each work unit with recent commits on the current branch. If it completes or directly follows the same purpose, prefer merging it into that commit: use `git commit --amend` for `HEAD`, or `git commit --fixup=<sha>` followed by `git rebase -i --autosquash <sha>^` for an older unpushed local commit.
6. If the purpose differs, create a separate commit even when files or branch names are related. Never rewrite a pushed/shared commit by default; create a follow-up commit unless the user explicitly requests it.
7. For an older commit, show the target SHA, reason, and rewritten commit list before rebasing. Inspect each staged diff and create one commit per work unit, in dependency order when needed.
8. Verify every commit hash and the final working-tree status.

Do not push or open a pull request. Do not rewrite pushed/shared history. Use amend or fixup/autosquash only for a matching unpushed local commit after showing the rewrite plan for approval. Do not reset or delete files. If the grouping, scope, or commit messages are ambiguous, ask before staging.
