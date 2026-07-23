# Commit

Work in the current repository and follow `skills/commit/SKILL.md` as the source of truth when it is available.

Inspect the current status, diff, branch, and recent history. Group the changes by common unit of work rather than making one commit for all files. Each group should be coherent, independently understandable, and reviewable.

Before creating a new commit, compare each work unit with recent commits on the current branch. If it completes or directly follows the same feature, bug fix, refactor, test, or documentation change, prefer merging it into that commit. Use `git commit --amend` for `HEAD`, or `git commit --fixup=<sha>` followed by `git rebase -i --autosquash <sha>^` for an older unpushed local commit. If the purpose differs, keep a separate commit. Never rewrite a pushed/shared commit by default.

For each work unit:

1. Identify the exact paths included and excluded.
2. Use a concise repository-consistent commit message.
3. Stage only that work unit's explicit paths.
4. Inspect the staged diff.
5. Create one commit for the work unit, in dependency order when needed.

Do not include unrelated edits, `.DS_Store`, secrets, generated output, or local metadata. Do not push or open a pull request. Do not rewrite pushed/shared history. For an older unpushed matching commit, show the target SHA, reason, and rewritten commit list before amend/rebase. Do not reset or delete files. If the work-unit grouping or commit messages are ambiguous, show the proposed groups and ask before staging.

Afterward, report every commit hash, message, work-unit grouping, committed paths, checks run, excluded files, and the final working-tree status.
