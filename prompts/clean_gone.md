# Clean Gone Branches

Work in the current repository and follow `skills/clean-gone/SKILL.md` as the source of truth when it is available.

Refresh remote-tracking information with `git fetch --prune` when the repository and network are available. Inspect local branches and worktrees, and identify only local branches whose upstream is marked `[gone]`.

For every candidate, check whether it is the current branch, protected, attached to a worktree, or backed by uncommitted changes. Never delete the current branch, protected branches, or a dirty worktree. Show exact candidates and ask for confirmation before deleting any ambiguous, current, protected, or dirty item.

Remove a clean linked worktree before deleting its stale branch. Delete only confirmed `[gone]` branches. Never remove remote branches, tags, commits, or unrelated files.

Re-run the branch and worktree checks afterward and report what was removed and what was skipped.
