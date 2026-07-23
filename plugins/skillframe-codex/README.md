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

The standalone skill definitions remain available under the repository's root
`skills/` directory for `npx skills add` workflows.
