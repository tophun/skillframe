---
name: commit-push-pr
description: Group the current related changes by common unit of work, create separate commits, push a branch, and open a GitHub pull request using the repository's PR conventions and approval gate. Use when the user asks to commit, push, and create a PR together or invokes `$commit-push-pr`. Do not merge, close, review, or modify labels/reviewers.
---

# Commit, Push, Pull Request

Turn the current related changes into grouped commits on one pushed branch and one pull request, while preserving the repository's PR approval gate.

## Workflow

### 1. Inspect repository and GitHub state

- Run `gh --version`, `gh auth status`, `git status --short`, and `git branch --show-current`.
- Run `git fetch origin` and identify the base branch in this order: `origin/HEAD`, `main`, `master`, `develop`.
- Inspect the base-to-head log and diff.
- Check for an existing open PR on the current branch. Do not create a duplicate.
- Read repository-local instructions, PR templates, and any local PR title/body conventions.

### 2. Select the change scope

- Include only files related to the user's request.
- Exclude unrelated work, editor metadata, `.DS_Store`, secrets, generated artifacts, and temporary files.
- If the current branch is `main` or another protected default branch, create a new branch with the `codex/` prefix.
- If the current branch already belongs to an open PR, stop and report that PR unless the user explicitly asks to update it.

### 3. Prepare commits by work unit

- Group the changes by common unit of work and choose one concise, repository-consistent commit message per group.
- Before creating a new commit, compare each work unit with recent commits on the current branch.
  - If it completes or directly follows the same feature, bug fix, refactor, test, or documentation change, prefer merging it into that commit.
  - For `HEAD`, use `git commit --amend` after showing the final message.
  - For an older unpushed local commit, use `git commit --fixup=<sha>` followed by `git rebase -i --autosquash <sha>^` after showing the target SHA, reason, and rewritten commit list for approval.
  - If the purpose differs, keep a separate commit.
  - Never rewrite a pushed/shared commit by default; create a follow-up commit unless the user explicitly requests history rewriting.
- Stage explicit paths for one work unit at a time and inspect each staged diff.
- Run focused checks relevant to the changed files.
- Create one commit per coherent work unit, in dependency order when needed.

### 4. Approval gate

Before staging, committing, pushing, or creating the PR when scope is ambiguous, show:

- selected files and excluded files;
- branch and base branch;
- commit messages for each work unit;
- PR title and complete body;
- draft or ready state;
- checks run and checks not run.

Proceed only after approval. Use Draft by default unless the user explicitly requests a ready PR.

### 5. Push and create the PR

- Commit the approved files by work unit.
- Push with `git push -u origin HEAD`.
- Create the PR with `gh pr create --title ... --body-file ... --base ... --draft` unless ready state was explicitly approved.
- Do not use `gh pr create --fill` when a repository template or PR body is available.

## Guardrails

- Never force-push or rewrite pushed/shared history. Amend or rebase only for an explicitly approved matching unpushed local commit.
- Do not merge, close, or delete branches in this skill.
- Never include changes that were not approved or that are unrelated to the request.
- Do not claim tests passed unless they were actually run.
- If `gh` is unavailable or unauthenticated, stop before committing or pushing and report the required setup.

## Report

Return the PR URL, base/head branches, draft state, every commit hash and message, included files grouped by work unit, excluded files, and verification results.
