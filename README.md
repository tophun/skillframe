# skillframe

Personal Codex skills and Claude Code plugins for Korean git, code-review, and AI-DLC workflows.

This repo serves two things:

1. A **Codex skills pack** (install with `npx skills add`) — `skills/`
2. A **Claude Code plugin marketplace** (install with `/plugin`) — `.claude-plugin/marketplace.json` + `plugins/`

## Claude Code plugins (marketplace)

Add this repo as a marketplace, then install the plugin:

```text
/plugin marketplace add tophun/skillframe
/plugin install skillframe-code-review@skillframe
```

| Plugin | Bundles | Use when |
| --- | --- | --- |
| `skillframe-code-review` | skills: `skillframe-code-review`, `humanize-korean` · agents: `humanize-monolith` +5 | Review a GitHub PR with multi-agent analysis and post **inline comments with code suggestions**; comment text is polished by the bundled `humanize-korean`. Say "코드리뷰", `/code-review`, or `$skillframe-code-review` with a PR link. |

The plugin is self-contained: the `humanize-korean` skill and its execution agents are bundled, so no separate install is required.

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
  marketplace.json           # Claude Code marketplace listing
plugins/
  skillframe-code-review/    # code-review plugin
    .claude-plugin/plugin.json
    skills/
      skillframe-code-review/
      humanize-korean/        # bundled dependency
    agents/                   # humanize-monolith + 5 humanize agents
skills/                      # Codex skills pack (npx skills add)
  ai-dlc/
  create-pull-request/
```
