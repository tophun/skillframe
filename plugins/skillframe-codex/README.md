# skillframe-codex

Codex plugin that bundles the reusable skills in this repository.

## Install from this repository

From the repository root, add the repo marketplace and install the plugin:

```bash
codex plugin marketplace add .
codex plugin add skillframe-codex@personal
```

Verify the configured marketplace and installed plugin:

```bash
codex plugin marketplace list
codex plugin list
```

Start a new Codex thread or session after installation so the bundled skills are
available. You can invoke the plugin explicitly with `@skillframe-codex`, or
ask Codex to use one of its bundled skills for the task.

## Bundled skills

- `ai-dlc`: Run AI-Driven Development Lifecycle workflows with plan-first gates.
- `create-pull-request`: Create a GitHub PR with Korean title/body conventions and an approval gate.
- `code-review`: Review a GitHub PR and create a pending inline review draft without submitting it.
- `code-review-context`: Build focused architectural context from the diff and affected callers, callees, and tests.

The Codex code-review skills are separate Codex implementations. They do not modify or
replace the Claude Code plugin under `plugins/skillframe/`.

The standalone skill definitions remain available under the repository's root
`skills/` directory for `npx skills add` workflows.
