# AGENTS.md — Detection Platform Metal Sandbox

This is the thin, provider-neutral operating contract for agents in
`/workspace`. `/workspace/CLAUDE.md` imports this file and should stay
Claude-specific only.

Detailed procedures live in tool READMEs, shared skills, and workspace-control
reference docs. Load them only when the task needs them.

## Scope

This workspace is for **detection-platform-metal** only: Docker Swarm + Redis
Streams, default branch `main`.

The old GKE-era `detection-platform` repo is legacy migration provenance under
`/workspace/archive/`. Current metal task state belongs under
`/workspace/detection-platform-metal-work/`.

## Non-Negotiable Rules

- Verify before asserting. Read source, run the actual container/tool, or query
  the actual data before making factual claims.
- Repo code runs in Docker containers. Do not run product `python3`, `go`,
  `npm`, `pytest`, `go test`, or similar directly on the host.
- Validate product work against the local stack only. Do not use staging or
  production APIs for validation.
- Production DB access is read-only and only through `/workspace/tools/db/dbctl`
  when explicitly needed for DB investigation/export work.
- Use git worktrees for branch work. Never branch in
  `/workspace/detection-platform-metal`.
- Make minimal, scoped changes. Do not refactor, upgrade, or rewrite adjacent
  code unless the task requires it.
- Do not push, create PRs, merge, remove worktrees, or run destructive cleanup
  without explicit approval where workspace rules require it.
- Keep task artifacts with the task. Put reusable data products in
  `/workspace/datasets/`, not inside `busy/<task>/`.
- Never delete useful task context. Move it to the right lifecycle state.
- Keep shared instructions provider-neutral. Use "the agent" unless a rule is
  truly Claude-specific or OpenAI/Codex-specific.

## Primary Paths

| Path | Role |
|---|---|
| `/workspace/detection-platform-metal` | Read-only reference checkout on `main`. |
| `/workspace/detection-platform-metal.worktrees/<branch>/` | Active branch worktrees. |
| `/workspace/detection-platform-metal-work/` | Task state: `busy/`, `parked/`, `later/`, `done/`, `archived/`, `planned/`, `investigations/`. |
| `/workspace/datasets/` | Durable reusable data products and manifests. |
| `/workspace/backups/` | Point-in-time platform state backups for restore planning. |
| `/workspace/agent-skills/` | Canonical shared Claude/Codex skills. |
| `/workspace/workspace-control/` | Reviewable source for workspace operating-model changes. |
| `/workspace/archive/` | Legacy migration provenance only. |

Worktree directory names mirror branch names with slashes replaced by dashes.
Example: `feat/foo` -> `feat-foo`.

## Tool Routing

| Need | Use | Details |
|---|---|---|
| Workspace orientation | `/workspace/workspace-control/tools/workspace-status --brief` | `workspace-status` skill |
| Multi-worktree local stack | `/workspace/tools/gateway/gatewayctl` | `/workspace/tools/gateway/README.md` |
| Detection DB investigation | `/workspace/tools/db/dbctl` | `db-readonly-investigation` skill |
| Reusable incident export | `/workspace/tools/datasets/datasetctl` | `detection-dataset-export` skill |
| Cloudflare Access observability | `/workspace/tools/access/accessctl` | `cloudflare-access-observability` skill |
| Agent session records | `/workspace/tools/agents/sessionctl` | `/workspace/tools/agents/README.md` |
| Shared skill validation/sync | `/workspace/tools/skills/skillctl` | `skill-maintainer` skill |

If a repo-local skill or README teaches host `cloudflared`, host `psql`, or
provider-local CLI patterns, prefer the workspace skill/tooling in this table.

## Task Lifecycle

The lifecycle root is `/workspace/detection-platform-metal-work/`.

- `planned/`: scoped work that has not started.
- `busy/`: active now, near-term PR/review/CI action, or protected critical
  work.
- `parked/`: valuable paused work with a concrete restart, extraction, or
  decision condition.
- `later/`: lightweight backlog or reminder with no preserved active state.
- `done/`: completed and summarized work.
- `archived/`: reference-only closed/superseded context after useful material
  is summarized or extracted.
- `investigations/`: standalone research not yet tied to branch/task lifecycle.

At session start, read:

1. `/workspace/detection-platform-metal-work/ACTIVE.md`
2. `/workspace/detection-platform-metal-work/SESSIONS.md`
3. relevant task `resume.md`

For non-trivial active tasks, keep `resume.md` current with task path,
branch/worktree/PR, session IDs, transcript paths when known, status, and next
action. Regenerate the session index after session record changes:

```bash
/workspace/tools/agents/sessionctl index
```

Detailed lifecycle definitions:
`/workspace/workspace-control/docs/specs/task-lifecycle.md`

## Worktrees And Product Validation

Create branch work from the read-only reference checkout:

```bash
git -C /workspace/detection-platform-metal worktree add \
  /workspace/detection-platform-metal.worktrees/<branch-name> -b <branch-name>
```

Run service tests/builds through containers or repo Make targets that themselves
use Docker. If a target assumes host-installed dependencies, translate it to a
container invocation or stop and ask.

Before opening a PR or asking for merge, ensure the PR title uses:

```text
<type>(<scope>): <description>
```

## Data And Artifacts

- Task artifacts stay with the task directory as it moves through lifecycle
  states.
- Durable datasets, exports, eval results, and corpus snapshots go under
  `/workspace/datasets/` with a manifest.
- Use `/workspace/datasets/adhoc/` for temporary data-shaped outputs.
- Screenshots go under the task's `screenshots/` directory, not workspace root.
- Platform state backups go under `/workspace/backups/` and are append-only
  after capture.

Detailed dataset/cache semantics:

- `/workspace/datasets/INDEX.md`
- `/workspace/datasets/MANAGEMENT.md`
- `/workspace/workspace-control/docs/specs/incident-scope-cache.md`

## Skills And Knowledge

- Shared skills live in `/workspace/agent-skills/skills/`; provider mirrors are
  generated copies under `/workspace/.claude/skills/` and
  `/workspace/.agents/skills/`.
- Edit canonical shared skills first, then run `skillctl validate` and
  `skillctl sync` only after approval.
- Durable provider-neutral learnings live in
  `/workspace/workspace-control/knowledge/`.
- Do not load the whole knowledge tree at session start. Search the generated
  index or use `knowledgectl search`, then open only relevant notes.

## Review And Handoff

- For investigations, multi-step fixes, or changes touching three or more
  files, state a short plan before executing.
- For non-trivial work, include a review checkpoint focused on scope, drift,
  validation, operator impact, and missing tests.
- For LLM workflow quality changes, preserve multi-provider operation and
  record model ID, provider, temperature/max tokens, fixture set, run time, and
  disagreement examples.
- Before pausing, handing off, or closing a task, update `resume.md` and run
  `sessionctl index`.

## Detailed References

- Live workspace details:
  `/workspace/workspace-control/docs/reference/live-workspace-details.md`
- Activation and rollback plan:
  `/workspace/workspace-control/docs/plans/2026-05-21-workflow-improvements-go-live.md`
- Task lifecycle spec:
  `/workspace/workspace-control/docs/specs/task-lifecycle.md`
- Thin-instructions audit:
  `/workspace/workspace-control/docs/reviews/2026-05-21-thin-instructions-audit.md`
- Repo architecture and service-level rules:
  `/workspace/detection-platform-metal/CLAUDE.md`
