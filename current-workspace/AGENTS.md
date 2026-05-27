# AGENTS.md — Detection Platform Metal Sandbox

This is the thin, provider-neutral operating contract for agents in
`/workspace`. `/workspace/CLAUDE.md` imports this file and should stay
Claude-specific only.

Detailed procedures live in tool READMEs, shared skills, and workspace-control
reference docs. Load them only when the task needs them.

## Scope

This workspace serves the Detection Platform ecosystem. In-scope repos:

- **detection-platform-metal** — the platform itself (Docker Swarm + Redis
  Streams, default branch `main`).
- **detection-agentic-workflows** — agent-facing operator surface for the
  platform (Pi CLI + deterministic JSON-envelope tools, default branch
  `main`).
- **workspace-control** — reviewable source for workspace operating-model
  changes, shared instructions, shared skills, and activation plans (default
  branch `main`).

Each repo follows the parallel-suffix convention: a read-only `<repo-name>`
checkout, a `<repo-name>.worktrees/` tree for branch worktrees, and a
`<repo-name>-work/` tree for task state. Cross-repo task lineage (a task in
one `-work/` tree continuing or extending a task in another) is recorded in
`LINEAGE.md` under the successor task, with a forward-pointer note appended
to the origin task's `resume.md`.

The old GKE-era `detection-platform` repo is legacy migration provenance under
`/workspace/archive/`.

## Non-Negotiable Rules

- Verify before asserting. Read source, run the actual container/tool, or query
  the actual data before making factual claims.
- Repo code runs in Docker containers. Do not run product `python3`, `go`,
  `npm`, `pytest`, `go test`, or similar directly on the host.
- Validate product work against the local stack only. Do not use staging or
  production APIs for validation.
- Do not use `kubectl`, `gcloud`, GAR, BigQuery, or ArgoCD for validation. If
  staging or production seems required, stop and ask.
- Production DB access is read-only and only through `/workspace/tools/db/dbctl`
  when explicitly needed for DB investigation/export work.
- Use git worktrees for branch work. Never branch in
  `/workspace/detection-platform-metal`.
- Make minimal, scoped changes. Do not refactor, upgrade, or rewrite adjacent
  code unless the task requires it.
- Workspace operating-model changes must be drafted in
  `/workspace/workspace-control` first, reviewed and validated, committed and
  pushed after approval, then activated into `/workspace` only with explicit
  approval and rollback notes. Emergency live fixes must be backported before
  task closeoff.
- Do not push, create PRs, merge, remove worktrees, or run destructive cleanup
  without explicit approval where workspace rules require it. One approval does
  not authorize later pushes or PR actions.
- Keep task artifacts with the task. Put reusable data products in
  `/workspace/datasets/`, not inside `busy/<task>/`.
- Never delete useful task context. Move it to the right lifecycle state.
- Keep shared instructions provider-neutral. Use "the agent" unless a rule is
  truly Claude-specific or OpenAI/Codex-specific.

## Primary Paths

| Path | Role |
|---|---|
| `/workspace/detection-platform-metal` | Read-only reference checkout on `main`. |
| `/workspace/detection-platform-metal.worktrees/<branch>/` | Active branch worktrees for the metal repo. |
| `/workspace/detection-platform-metal-work/` | Task state for metal work: `busy/`, `parked/`, `later/`, `done/`, `archived/`, `planned/`, `investigations/`. |
| `/workspace/detection-platform-metal-work/knowledge/` | Workspace/product-adjacent knowledge for detection-platform-metal agents. |
| `/workspace/detection-agentic-workflows` | Read-only reference checkout on `main` for the agentic-workflows repo. |
| `/workspace/detection-agentic-workflows.worktrees/<branch>/` | Active branch worktrees for the agentic-workflows repo. |
| `/workspace/detection-agentic-workflows-work/` | Task state for agentic-workflows work: same lifecycle dirs (`busy/`, `parked/`, …) as metal-work. |
| `/workspace/workspace-control` | Reviewable source checkout on `main` for workspace operating-model changes. |
| `/workspace/workspace-control.worktrees/<branch>/` | Active branch worktrees for non-trivial workspace-control branch work. |
| `/workspace/workspace-control-work/` | Task state for workspace-control operating-model work: same lifecycle dirs as the other task roots. |
| `/workspace/datasets/` | Durable reusable data products and manifests. |
| `/workspace/backups/` | Point-in-time platform state backups for restore planning. |
| `/workspace/agent-skills/` | Canonical shared Claude/Codex skills. |
| `/workspace/workspace-control/` | Reviewable source for workspace operating-model changes. |
| `/workspace/testing-data/` | Curated classifier/LLM eval datasets and ground truths. |
| `/workspace/data/` | Compatibility/scratch path; reusable outputs belong in `/workspace/datasets/`. |
| `/workspace/archive/` | Legacy migration provenance only. |

Worktree directory names mirror branch names with slashes replaced by dashes.
Example: `feat/foo` -> `feat-foo`. The same applies for any in-scope repo:
`<repo-name>.worktrees/<branch-with-dashes>/`.

## Tool Routing

| Need | Use | Details |
|---|---|---|
| Workspace orientation | `/workspace/workspace-control/tools/workspace-status --brief` | `workspace-status` skill |
| Central task discovery index | `/workspace/workspace-control/tools/task-index render` | `/workspace/workspace-control/docs/reference/task-index.md` |
| Implementation gate, validation ledger, context pack, or swarm routing | `/workspace/workspace-control/tools/workflowctl` | `/workspace/workspace-control/docs/reference/workflowctl.md` |
| Multi-worktree local stack | `/workspace/tools/gateway/gatewayctl` | `/workspace/tools/gateway/README.md` |
| Local classifier/LLM env | `/workspace/classifiers.env` | Pass as an env file; do not print values |
| Detection DB investigation | `/workspace/tools/db/dbctl` | `db-readonly-investigation` skill |
| Reusable incident export | `/workspace/tools/datasets/datasetctl` | `detection-dataset-export` skill |
| Cloudflare Access observability | `/workspace/tools/access/accessctl` | `cloudflare-access-observability` skill |
| Detection UI browser review | `/workspace/tools/browser-mcp/browser-mcp` | `detection-ui-browser-review` skill |
| Agent session records | `/workspace/tools/agents/sessionctl` | `/workspace/tools/agents/README.md` |
| Shared skill validation/sync | `/workspace/tools/skills/skillctl` | `skill-maintainer` skill |
| Run agentic workflows / Pi | `docker compose run --rm agentic pnpm <tool> …` from the agentic-workflows repo or its worktree | `/workspace/detection-agentic-workflows/README.md` |

If a repo-local skill or README teaches host `cloudflared`, host `psql`, or
provider-local CLI patterns, prefer the workspace skill/tooling in this table.
`gatewayctl` supports concurrent local stacks through unique stack names and
loopback IPs; missing local images or a stopped local registry are image
blockers, not evidence that multi-instance stacks are unsupported.

## Task Lifecycle

Each in-scope repo has its own lifecycle root (`<repo-name>-work/`). Currently
populated:

- `/workspace/detection-platform-metal-work/`
- `/workspace/detection-agentic-workflows-work/`
- `/workspace/workspace-control-work/`

Use the owning repo's task root. Cross-repo initiatives use a coordinator task
plus repo-specific child tasks, linked through `LINEAGE.md` and
`workflow.json.related_tasks`. Discovery can be centralized through generated
indexes, but task ownership stays in the repo task root.

Within each root the standard lifecycle dirs apply:

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

At session start, read the relevant repo's task-root files:

1. `<repo-name>-work/ACTIVE.md`
2. `<repo-name>-work/SESSIONS.md`
3. relevant task `resume.md`

When a task in one repo's `-work/` tree continues or extends a task in
another's, record the relationship in `LINEAGE.md` under the successor task
and append a forward-pointer paragraph to the origin task's `resume.md`.

For non-trivial active tasks, keep `resume.md` current with task path,
branch/worktree/PR, session IDs, transcript paths when known, status, and next
action. Regenerate the session index after session record changes:

```bash
/workspace/tools/agents/sessionctl index
```

Detailed lifecycle definitions:
`/workspace/workspace-control/docs/specs/task-lifecycle.md`

Task-first resumability standard:
`/workspace/workspace-control/docs/specs/task-resumability.md`

## Worktrees And Product Validation

Create branch work from the read-only reference checkout:

```bash
git -C /workspace/detection-platform-metal worktree add \
  /workspace/detection-platform-metal.worktrees/<branch-name> -b <branch-name>
```

Run service tests/builds through containers or repo Make targets that themselves
use Docker. If a target assumes host-installed dependencies, translate it to a
container invocation or stop and ask.

Use repo Docker tooling (`docker compose`, `docker stack`, and Dockerfiles under
`infrastructure/docker/`). For ad-hoc repo scripts, run inside a container with
the workspace mounted rather than creating host virtualenvs or installing host
dependencies.

Treat workspace env files such as `/workspace/docker-swarm.env`,
`/workspace/pivoter.env`, and `/workspace/classifiers.env` as container
env-file or mount inputs. Do not print them or source them directly into the
agent shell unless a tool specifically documents that pattern.

For features touching five or more files, checkpoint after each logical unit
with the relevant container-based validation.

Before opening a PR or asking for merge, ensure the PR title uses:

```text
<type>(<scope>): <description>
```

Prefer an explicit `gh pr create --title ...`; do not rely on `--fill` unless
the source commit headline already matches the required format.

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
- Workspace-control operating-model learnings live in
  `/workspace/workspace-control/knowledge/`.
- Detection-platform-metal workspace/product-adjacent learnings live in
  `/workspace/detection-platform-metal-work/knowledge/`.
- Do not load either knowledge tree at session start. Search the generated
  indexes or use `/workspace/workspace-control/tools/knowledgectl search
  <term>`; set `KNOWLEDGE_DIR=/workspace/detection-platform-metal-work/knowledge`
  for the workspace-level tree.

## Review And Handoff

- For investigations, multi-step fixes, or changes touching three or more
  files, state a short plan before executing.
- When exploratory code discussion turns into non-trivial implementation,
  create or update an implementation brief and pass the `workflowctl` gate
  before edits. Record a swarm routing decision before background agents;
  `none` is valid, and the coordinator owns integration and validation.
- For non-trivial work, include a review checkpoint focused on scope, drift,
  validation, operator impact, and missing tests.
- For LLM workflow quality changes, preserve multi-provider operation and
  record model ID, provider, temperature/max tokens, fixture set, run time, and
  disagreement examples.
- Write plans and notes so either Claude or Codex can resume: prefer explicit
  paths, commands, branch names, PR/issue links, and validation evidence over
  chat-only context.
- If a workflow depends on a provider-specific capability, name the dependency
  and the closest fallback.
- Before pausing, handing off, or closing a task, update `resume.md` and run
  `sessionctl index`.

## Detailed References

- Live workspace details:
  `/workspace/workspace-control/docs/reference/live-workspace-details.md`
- Activation and rollback plan:
  `/workspace/workspace-control/docs/plans/2026-05-21-workflow-improvements-go-live.md`
- Workspace-control maintenance:
  `/workspace/workspace-control/MAINTENANCE.md`
- Task lifecycle spec:
  `/workspace/workspace-control/docs/specs/task-lifecycle.md`
- Task resumability spec:
  `/workspace/workspace-control/docs/specs/task-resumability.md`
- Multi-repo task organization:
  `/workspace/workspace-control/docs/specs/multi-repo-task-organization.md`
- Thin-instructions audit:
  `/workspace/workspace-control/docs/reviews/2026-05-21-thin-instructions-audit.md`
- Repo architecture and service-level rules:
  `/workspace/detection-platform-metal/CLAUDE.md`
