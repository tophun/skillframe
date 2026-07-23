# skillframe

Personal Codex skills and Claude Code plugins for Korean git, code-review, and AI-DLC workflows.

This repo serves two things:

1. A **Codex skills pack** (install with `npx skills add`) — `skills/`
2. A **Claude Code plugin marketplace** (install with `/plugin`) — `.claude-plugin/marketplace.json` + `plugins/`

## Claude Code plugins (marketplace)

Add this repo as a marketplace, then install the plugins:

```text
/plugin marketplace add tophun/skillframe
/plugin install humanize-korean@skillframe
/plugin install code-review@skillframe
```

| Plugin | Contains | Use when |
| --- | --- | --- |
| `humanize-korean` | skill `humanize-korean` · 6 agents | Rewrite AI-written Korean text to read naturally — detect and fix translationese / AI tells while preserving meaning. Say "AI 티 없애줘", "사람이 쓴 것처럼 윤문". |
| `code-review` | skill `code-review` | Review a GitHub PR with multi-agent analysis and post **inline comments with code suggestions**; comment text is polished via `humanize-korean`. Say "코드리뷰", `/code-review`, or `$code-review` with a PR link. |

Each plugin is focused and installed independently (official-marketplace style). `code-review` uses `humanize-korean`, so install both.

## Codex skills (`npx skills add`)

Install this skill pack with:

```bash
npx skills add tophun/skillframe
```

| Skill | Path | Use when |
| --- | --- | --- |
| `skillframe-create-pull-request` | `skills/create-pull-request` | Create a new GitHub PR with a Korean title/body and an approval gate before `gh pr create`. |
| `ai-dlc` | `skills/ai-dlc` | Run AI-Driven Development Lifecycle workflows with plan-first gates and traceable artifacts. |

Invoke explicitly:

```text
Use $skillframe-create-pull-request
Use $ai-dlc
```

Shorthand for the PR workflow: `/pr`, `PR 만들어줘`.

## Repository Layout

```text
.claude-plugin/
  marketplace.json                 # Claude Code marketplace listing
plugins/
  humanize-korean/                 # standalone humanize plugin
    .claude-plugin/plugin.json
    skills/humanize-korean/
    agents/                        # humanize-monolith + 5 agents
  code-review/          # code-review plugin (uses humanize-korean)
    .claude-plugin/plugin.json
    skills/code-review/
skills/                           # Codex skills pack (npx skills add)
  ai-dlc/
  create-pull-request/
```
