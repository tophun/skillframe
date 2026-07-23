# Commit

Work in the current repository and follow `skills/commit/SKILL.md` as the source of truth when it is available.

Inspect the current status, diff, branch, and recent history. Group the changes by common unit of work rather than making one commit for all files. Each group should be coherent, independently understandable, and reviewable.

For each work unit:

1. Identify the exact paths included and excluded.
2. Use a concise repository-consistent commit message.
3. Stage only that work unit's explicit paths.
4. Inspect the staged diff.
5. Create one commit for the work unit, in dependency order when needed.

Do not include unrelated edits, `.DS_Store`, secrets, generated output, or local metadata. Do not push, open a pull request, amend, rebase, reset, or delete files. If the work-unit grouping or commit messages are ambiguous, show the proposed groups and ask before staging.

Afterward, report every commit hash, message, work-unit grouping, committed paths, checks run, excluded files, and the final working-tree status.
