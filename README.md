# skillframe

Personal Codex skills for Korean git workflows and AI-DLC based development.

## Install

Install this skill pack with:

```bash
npx skills add tophun/skillframe
```

Generic form:

```bash
npx skills add <owner/repo>
```

After installation, restart or refresh your Codex session if the new skills do not appear immediately.

## Skills

| Skill | Path | Use when |
| --- | --- | --- |
| `skillframe-commit` | `skills/commit` | Group current git changes into reviewer-friendly commits and write Korean Conventional Commit messages. |
| `skillframe-create-pull-request` | `skills/create-pull-request` | Create a new GitHub PR with a Korean title/body and an approval gate before `gh pr create`. |
| `ai-dlc` | `skills/ai-dlc` | Run AI-Driven Development Lifecycle workflows with plan-first gates and traceable artifacts. |

## Usage

Invoke a skill explicitly in Codex:

```text
Use $skillframe-commit
Use $skillframe-create-pull-request
Use $ai-dlc
```

Common shorthand requests are also supported for the skillframe git workflows:

```text
/commit
/pr
PR 만들어줘
```

## Repository Layout

```text
skills/
  ai-dlc/
  commit/
  create-pull-request/
```
