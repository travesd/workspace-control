# Workspace-Level Instruction Drift Audit

Date: 2026-05-21

Source compared:

- Pre-go-live workspace contract:
  `/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521/rollback/live-files/AGENTS.md`
- Current live/source contract:
  `/workspace/AGENTS.md`
  and `current-workspace/AGENTS.md`
- Detail target:
  `docs/reference/live-workspace-details.md`

## Summary

The thin `AGENTS.md` migration correctly moved many long procedures into
reference docs and shared skills, but it also removed several compact
workspace-level guardrails. Those should remain always discoverable because
agents need them before knowing which skill or reference to load.

## Restored To Always-Loaded Workspace Contract

- Local classifier/LLM credentials live at `/workspace/classifiers.env`; pass as
  an env file and do not print values.
- `gatewayctl` supports concurrent local stacks through unique stack names and
  loopback IPs; missing local images or a stopped registry are image blockers.
- `/workspace/testing-data/` is the curated classifier/LLM eval data location.
- `/workspace/data/` is compatibility/scratch only; reusable outputs belong in
  `/workspace/datasets/`.
- Validation must not use `kubectl`, `gcloud`, GAR, BigQuery, or ArgoCD.
- One approval to push or create a PR does not authorize future push/PR actions.
- Repo execution uses Docker tooling; ad-hoc repo scripts should run in
  containers, not host virtualenvs.
- Workspace env files are container env-file or mount inputs unless a tool
  documents otherwise.
- Features touching five or more files should checkpoint after each logical
  unit with container validation.
- PR titles should be set explicitly when needed; do not rely on `--fill` if
  the source commit title is not already compliant.
- Cross-agent handoff notes should use explicit paths, commands, branches, PRs,
  and validation evidence.
- Provider-specific workflow dependencies should name the closest fallback.
- Browser review now has an always-discoverable tool-routing row for the shared
  browser MCP wrapper and `detection-ui-browser-review` skill.

## Restored To Reference Detail

- Docker execution examples and env-file semantics.
- Staging/production validation stop-and-ask rule.
- LLM provider support details: `packages/py-llm-engine`,
  litellm-compatible model IDs, provider key names, neutral model override env
  names, and comparison metadata.
- Platform backup details: task-local scripts first, ssdeep cluster cross-check,
  and operator-driven restore limitations.
- Task close-off exact merge-state check and stale-merged busy-task scan.
- Task lifecycle spec status now matches live activation; the definitions are
  active, while physical task movement remains intentional and user-approved.
- Browser MCP wrapper recovery semantics: `doctor`, `cleanup --dry-run`, and
  `cleanup` target stale Playwright MCP runtimes only and cannot reconnect an
  already-closed agent stdio transport.

## Browser MCP / Agent Wrapper Follow-Up

After the tmux/browser sidetrack, live workspace tooling had newer browser MCP
recovery support than the `workspace-control` seed:

- `/workspace/tools/browser-mcp/browser-mcp` had `doctor` and `cleanup`.
- `/workspace/tools/browser-mcp/README.md` documented `Transport closed`
  recovery and cleanup scope.
- `/workspace/agent-skills/skills/detection-ui-browser-review/SKILL.md`
  included matching recovery guidance.

The source repo now mirrors those live changes in
`current-workspace/tools/browser-mcp/` and
`agent-skills/skills/detection-ui-browser-review/`. The sanitized Codex config
seed remains under `current-workspace/config/`; the user's global
`/home/user/.codex/config.toml` was not modified.

## Preserved Elsewhere

- DB access, dataset export, Cloudflare Access observability, browser review,
  task close-off, skill maintenance, and session hygiene procedures are covered
  by shared skills.
- PR migration, archive pointers, backward-compatibility symlinks, dataset
  traceability, and platform backup layout are in
  `docs/reference/live-workspace-details.md`.
- Task lifecycle definitions are in `docs/specs/task-lifecycle.md`.

## Not Restored To AGENTS.md

The full old procedural text was intentionally not restored to keep
`AGENTS.md` thin. Detailed command sequences and long edge-case rationale stay
in references or skills unless they are required before skill selection.
