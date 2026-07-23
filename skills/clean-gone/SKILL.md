---
name: clean-gone
description: Inspect and safely remove local Git branches whose upstream is marked `[gone]`, including linked worktrees when safe. Use when the user asks to clean stale or deleted remote branches, clean gone branches, or invokes `$clean-gone`. Never remove the current branch, protected branches, or worktrees with uncommitted changes without explicit confirmation.
---

# Clean Gone Branches

Remove local branches whose configured upstream no longer exists, while preserving active work and linked worktrees.

## Workflow

1. Refresh remote-tracking information with `git fetch --prune` when the repository and network are available.
2. Inspect `git branch -v` and `git worktree list`.
3. Collect only local branches whose upstream status is `[gone]`.
4. For each candidate, check:
   - whether it is the current branch;
   - whether it is `main`, `master`, `develop`, or another protected branch;
   - whether a linked worktree uses it;
   - whether that worktree has uncommitted changes.
5. Present the exact candidate branches and worktrees before deletion when any candidate is current, protected, dirty, or otherwise ambiguous.
6. Remove a clean linked worktree with `git worktree remove <path>` before deleting its branch. Never use `--force` on a dirty worktree without explicit confirmation.
7. Delete only confirmed stale branches with `git branch -D <branch>`; never delete a branch merely because it is old or unmerged.
8. Re-run `git branch -v` and `git worktree list` and report what was removed and what was skipped.

## Guardrails

- Never delete the current branch; switch to a safe branch first only when the user explicitly authorizes that operation.
- Never delete protected branches or branches without `[gone]` status.
- Do not discard uncommitted work in a worktree.
- Do not remove remote branches, tags, commits, or files outside the identified worktrees.
- If no branches are marked `[gone]`, report that no cleanup was needed.
