# skillframe

Personal Codex skills and Claude Code plugins for Korean git, code-review, and AI-DLC workflows.

This repo serves three things:

1. A **Codex skills pack** (install with `npx skills add`) — `skills/`
2. A **Codex plugin** (install with `codex plugin`) — `.agents/plugins/marketplace.json` + `plugins/skillframe-codex/`
3. A **Codex custom prompt pack** (install into `~/.codex/prompts/`) — `prompts/`
4. A **Claude Code plugin marketplace** (install with `/plugin`) — `.claude-plugin/marketplace.json` + `plugins/skillframe/`

## Claude Code plugin (marketplace)

Add this repo as a marketplace, then install the plugin:

```text
/plugin marketplace add tophun/skillframe
/plugin install skillframe@skillframe
```

The `skillframe` plugin exposes four skills and three commands:

| Skill | Use when |
| --- | --- |
| `skillframe:create-pull-request` | Create a new GitHub PR or repair an existing PR body/draft state with Korean title/body rules and an approval gate before `gh pr create/edit/ready`. Say "PR 만들어줘", `/pr`, or "PR 본문 고쳐줘". |
| `skillframe:code-review` | Review a GitHub PR through dedicated explore / reason / evaluate / write subagents (Haiku for search, Sonnet for review lanes and scoring, escalating either to Opus for concurrency / transaction / auth / lifecycle changes) and post **inline comments with code suggestions**; comment wording follows `humanize-korean` rules. Say "코드리뷰", `/code-review` with a PR link. |
| `skillframe:code-review-context` | Map the review perimeter from the diff and use codegraph selectively to trace affected callers, callees, and tests. |
| `skillframe:humanize-korean` | Rewrite AI-written Korean text to read naturally — detect and fix translationese / AI tells while preserving meaning. Say "AI 티 없애줘", "사람이 쓴 것처럼 윤문". |

The plugin also provides:

| Command | Use when |
| --- | --- |
| `/commit` | Group changes by common work unit and create separate Git commits. |
| `/commit-push-pr` | Commit, push, and open a Draft PR with the repository approval gate. |
| `/clean_gone` | Inspect and safely remove local branches marked `[gone]`. |

`create-pull-request` and `code-review` can use `humanize-korean` for PR/review wording; all ship in one plugin, so a single install covers everything.

## Codex plugin

The repository also includes a Codex-native plugin at
`plugins/skillframe-codex/`. It uses the required
`.codex-plugin/plugin.json` manifest and is exposed through the repo marketplace
at `.agents/plugins/marketplace.json`.

From the repository root, install it with:

```bash
codex plugin marketplace add .
codex plugin add skillframe-codex@personal
```

Check the marketplace and installed plugin:

```bash
codex plugin marketplace list
codex plugin list
```

Start a new Codex thread or session after installation. You can invoke the
plugin explicitly with `@skillframe-codex`, or ask Codex to use one of its
bundled skills:

| Skill | Use when |
| --- | --- |
| `ai-dlc` | Run an AI-Driven Development Lifecycle workflow with plan-first gates. |
| `create-pull-request` | Create a GitHub PR with Korean title/body conventions and an approval gate. |
| `code-review` | Review a GitHub PR and create a pending inline review draft without submitting it. |
| `code-review-context` | Build focused review context from the diff and affected callers, callees, and tests. |

For local plugin changes, update the plugin source, refresh or reinstall it
from the configured marketplace, and start a new thread so Codex loads the new
bundle. See the [Codex plugin README](plugins/skillframe-codex/README.md) for
the short install guide.

## Codex skills (`npx skills add`)

Install this skill pack with:

```bash
npx skills add tophun/skillframe
```

| Skill | Path | Use when |
| --- | --- | --- |
| `skillframe-create-pull-request` | `skills/create-pull-request` | Create a new GitHub PR with a Korean title/body and an approval gate before `gh pr create`. |
| `commit` | `skills/commit` | Group selected working-tree changes by common work unit and create separate Git commits. |
| `commit-push-pr` | `skills/commit-push-pr` | Commit, push, and open a Draft PR with repository conventions and approval. |
| `clean-gone` | `skills/clean-gone` | Safely clean local branches whose remote upstream is marked `[gone]`. |
| `ai-dlc` | `skills/ai-dlc` | Run AI-Driven Development Lifecycle workflows with plan-first gates and traceable artifacts. |

Invoke explicitly:

```text
Use $skillframe-create-pull-request
Use $ai-dlc
```

Shorthand for the PR workflow: `/pr`, `PR 만들어줘`.

## Codex custom commands

Codex discovers custom slash commands from the top-level Markdown files in
`~/.codex/prompts/`. Install this repository's prompts with:

```bash
mkdir -p ~/.codex/prompts
cp prompts/commit.md prompts/commit-push-pr.md prompts/clean_gone.md ~/.codex/prompts/
```

Then use them in Codex CLI or the IDE extension:

```text
/prompts:commit
/prompts:commit-push-pr
/prompts:clean_gone
```

The prompts are the slash-command entry points; the corresponding files under
`skills/` remain the reusable Codex skill definitions.

## Repository Layout

```text
.claude-plugin/
  marketplace.json                 # Claude Code marketplace listing
.agents/
  plugins/marketplace.json         # Codex repo marketplace listing
plugins/
  skillframe/                      # Claude Code plugin
    .claude-plugin/plugin.json
    commands/
      commit.md                    # -> /commit
      commit-push-pr.md            # -> /commit-push-pr
      clean_gone.md                # -> /clean_gone
    skills/
      create-pull-request/         # -> skillframe:create-pull-request
      code-review/                 # -> skillframe:code-review
      code-review-context/         # -> skillframe:code-review-context
      humanize-korean/             # -> skillframe:humanize-korean
    agents/                        # 5 humanize agents + 4 code-review agents
                                   #   (explorer/analyst/judge/writer)
  skillframe-codex/                # Codex plugin package
    .codex-plugin/plugin.json
    README.md
    skills/                        # bundled Codex skills
skills/                            # Codex skills pack (npx skills add)
  ai-dlc/
  clean-gone/
  commit/
  commit-push-pr/
  create-pull-request/
prompts/                          # Codex custom prompts for /prompts:* commands
  commit.md
  commit-push-pr.md
  clean_gone.md
```
