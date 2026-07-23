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
5. Inspect each staged diff and create one commit per work unit, in dependency order when needed.
6. Verify every commit hash and the final working-tree status.

Do not push, open a pull request, amend, rebase, reset, or delete files. If the grouping, scope, or commit messages are ambiguous, ask before staging.
