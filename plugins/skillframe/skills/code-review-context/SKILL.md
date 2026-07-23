---
name: code-review-context
description: Build focused architectural context for code reviews by starting from the diff, using codegraph init/index when useful, tracing affected callers and callees, and checking related tests and boundaries. Use for pull request reviews, commit reviews, refactors, shared API changes, cross-module changes, and security- or data-sensitive code. Continue with a manual fallback when codegraph is unavailable or incomplete.
---

# Code Review Context

Build enough repository context to judge a change correctly without loading the entire codebase into the review context.

## Core rule

Start with the diff. Expand the review scope only when the change crosses module boundaries, changes a shared contract, or touches security, data, concurrency, or other high-impact paths.

Treat codegraph as an impact-mapping aid, not as proof of complete runtime behavior.

## Workflow

### 1. Establish the review target

- Identify the repository root, base commit, head commit, and review type.
- Read the diff before exploring unrelated files.
- List changed files, changed symbols, public interfaces, configuration changes, migrations, and tests.
- Check repository-local instructions such as `AGENTS.md`, `CONTRIBUTING.md`, and review conventions.

### 2. Choose the required context depth

Use the smallest scope that can establish correctness:

- **Local change**: changed files, nearby helpers, direct tests, and direct callers.
- **Module-level change**: module boundary, public contract, callers, implementations, error paths, and related tests.
- **Cross-cutting or high-risk change**: end-to-end data/control flow, all relevant consumers, authorization and validation boundaries, persistence or external side effects, and failure recovery.

Do not build or query the full graph for a clearly isolated change unless the diff reveals an unexpected shared dependency.

### 3. Prepare and use codegraph conditionally

First discover the repository's codegraph integration and supported commands. Do not assume a particular CLI syntax. Inspect project documentation, existing scripts, package commands, or `codegraph --help` when available.

- Run `init` only when the repository has not been initialized for codegraph or its graph metadata is missing.
- Run `index` after a checkout, merge, or relevant code/configuration change when no matching index exists.
- Prefer incremental indexing and reuse an index tied to the current commit when supported.
- Record or verify the commit/version represented by the index before trusting results.
- Query only changed symbols and their relevant callers, callees, implementations, imports, consumers, and tests.
- Bound graph expansion: normally depth 2–3 and a small, relevant node set. Expand only when the initial results show another boundary.
- Exclude generated, vendored, and unrelated third-party code unless the diff touches them.

If codegraph is unavailable, fails, or does not model the language/runtime correctly, continue with repository search, language-server navigation, build metadata, and targeted file reads. Report the limitation when it affects confidence.

### 4. Validate the change against the context

For each changed behavior, check:

- Who calls the changed code, and what assumptions do those callers make?
- Which implementations, adapters, or serializers must remain compatible?
- Does the change alter validation, authorization, error handling, retries, transactions, caching, concurrency, or side effects?
- Do persistence schemas, API contracts, events, jobs, or configuration remain compatible?
- Are the relevant success, failure, boundary, and regression tests present and meaningful?
- Could dynamic dispatch, reflection, dependency injection, code generation, or runtime configuration create dependencies absent from the graph?

Review semantics and user impact, not only graph connectivity.

### 5. Report review context and findings

Keep the review focused. For every finding, provide:

1. Exact file and line or symbol.
2. Observable impact or failure mode.
3. Evidence from the diff, graph, callers, tests, or runtime contract.
4. The smallest practical fix or verification needed.

Also report briefly:

- Scope inspected and why it was sufficient.
- Codegraph status: reused, initialized, indexed, unavailable, stale, or incomplete.
- Important paths that were not statically discoverable.
- Tests run and tests not run when that affects confidence.

Do not turn the final review into an inventory of every file inspected.

## Efficiency guardrails

- Prefer targeted graph queries over full graph dumps.
- Prefer symbol and path summaries over copying source into context.
- Stop expanding a path once it reaches an unchanged, well-tested boundary.
- Reuse cached indexes; do not re-index repeatedly during one review unless the source changed.
- Keep tool output bounded and inspect more only when a finding depends on it.
- A graph result showing no edge is not evidence that no runtime dependency exists.

## Fallback decision

If the repository is small or the change is local, use diff plus direct navigation and skip codegraph. If the repository is large, the PR is cross-module, or a shared/high-risk path changed, initialize or refresh codegraph and use it to identify the review perimeter. If indexing is expensive or unavailable, make a bounded manual map and state the reduced confidence.
