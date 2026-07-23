---
allowed-tools: Bash(git fetch:*), Bash(git branch:*), Bash(git worktree:*), Bash(git status:*)
description: Clean local branches whose remote upstream was deleted
---

## Task

Inspect and safely remove local branches marked `[gone]` because their remote upstream was deleted.

1. Run `git fetch --prune` when the repository and network are available.
2. Run `git branch -v` and `git worktree list`.
3. Identify only local branches with `[gone]` status.
4. For every candidate, check whether it is current, protected, attached to a worktree, or backed by uncommitted changes.
5. Show the exact branches and worktrees that would be removed when any candidate is current, protected, dirty, or ambiguous, and ask for confirmation.
6. Remove a clean linked worktree with `git worktree remove <path>` before deleting its branch. Do not use `--force` on dirty worktrees without explicit confirmation.
7. Delete only confirmed stale branches with `git branch -D <branch>`.
8. Re-run `git branch -v` and `git worktree list`, then report removed and skipped items.

Never delete the current or protected branch, discard uncommitted work, remove remote branches, or delete branches without `[gone]` status. If there are no `[gone]` branches, report that no cleanup was needed.
