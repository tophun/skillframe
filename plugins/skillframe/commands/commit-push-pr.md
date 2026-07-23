---
allowed-tools: Bash(git switch:*), Bash(git checkout --branch:*), Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git log:*), Bash(git fetch:*), Bash(git commit:*), Bash(git push:*), Bash(gh --version:*), Bash(gh auth status:*), Bash(gh pr view:*), Bash(gh pr list:*), Bash(gh pr create:*)
description: Commit, push, and open a pull request
---

## Context

- Current git status: !`git status --short`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Task

Commit the current related changes, push a branch, and open one pull request.

1. Verify `gh` is installed and authenticated. Fetch `origin` and determine the base branch from `origin/HEAD`, `main`, `master`, or `develop`.
2. Inspect the diff and select only files related to the request. Exclude unrelated files, `.DS_Store`, secrets, generated output, and temporary files.
3. Check for an existing open PR on the current branch. Do not create a duplicate.
4. If on `main` or another protected default branch, create a new `codex/` branch.
5. Group the changes by common work unit and prepare one commit message per coherent group, plus a PR title/body using the repository's template and conventions.
6. Before staging, committing, pushing, or creating the PR, show the proposed work-unit groups and paths, excluded files, branch/base, commit messages, complete PR body, draft state, and checks. Follow the repository's PR approval gate.
7. After approval, stage explicit paths, inspect each staged diff, create one commit per work unit in dependency order, push with `git push -u origin HEAD`, and create a Draft PR with `gh pr create`. Use ready state only when explicitly requested.

Do not merge, close, review, force-push, amend, rebase, or change labels/reviewers. Do not claim checks passed unless they were actually run.
