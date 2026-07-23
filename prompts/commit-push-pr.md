# Commit, Push, Pull Request

Work in the current repository and follow `skills/commit-push-pr/SKILL.md` as the source of truth when it is available.

Inspect the repository and GitHub state, including authentication, the base branch, the current branch, existing open pull requests, local instructions, and the complete diff. Include only files related to the user's request; exclude `.DS_Store`, secrets, generated output, and temporary files.

If the current branch is protected or is the default branch, create a `codex/` branch. Group changes by common unit of work and prepare a separate commit for each coherent group when the change contains multiple independently understandable units. Keep dependent work in dependency order.

Before staging, committing, pushing, or creating the pull request, show the proposed work-unit groups and paths, excluded files, branch and base branch, commit messages, pull request title and complete body, draft state, and checks. Follow the repository's approval gate and wait for approval when the scope is ambiguous. Use Draft by default.

After approval, stage explicit paths, inspect each staged diff, create the commits, push with `git push -u origin HEAD`, and create the approved pull request. Do not merge, close, review, force-push, amend, rebase, or change labels or reviewers.

Report every commit hash, the pull request URL, base and head branches, draft state, included and excluded files, and verification results. Do not claim checks passed unless they were actually run.
