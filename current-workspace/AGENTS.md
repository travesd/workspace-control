# AGENTS.md — Detection Platform Metal Sandbox

This is the canonical workspace-level instruction file for Claude and Codex/OpenAI agents. `/workspace/CLAUDE.md` imports this file and stays thin, with Claude-specific routing or setup only where needed. Keep behavior rules provider-neutral unless a tool truly differs.

## Scope

This workspace is for **detection-platform-metal** only (Docker Swarm + Redis Streams, default branch `main`).

The old **detection-platform** (GKE) has been archived to `/workspace/archive/` for PR migration reference — there are open PRs there that will be ported into metal over time. Do not start new work in the archive. Reference it only when porting a specific PR.

## Execution Model

**Agents run on the host. Repo code runs in Docker containers.**

- Never invoke `python3`, `go`, `npm`, `pytest`, `go test`, etc. against repo code on the host.
- Always go through the repo's Docker tooling: `docker compose`, `docker stack`, per-service Dockerfiles under `infrastructure/docker/`.
- Tests: `cd services/<service> && make test-unit` only works if the Makefile targets `docker run`/`docker compose`. Check before running — if a target assumes host-installed Go/Python, translate it into a container invocation.
- Release testing is **local stack only** (`infrastructure/docker/deploy.sh` + Swarm). No staging, no production, no kubectl, no gcloud.

## Primary Working Directories

| Path | Role |
|------|------|
| `/workspace/detection-platform-metal` | Read-only reference, always on `main`. Never branch work here. |
| `/workspace/detection-platform-metal.worktrees/<branch>/` | Active branch work (one worktree per branch). |
| `/workspace/detection-platform-metal-work/` | Work artifacts: `ACTIVE.md`, `planned/`, `busy/`, `later/`, `done/`, `archived/`, `investigations/`. |
| `/workspace/datasets/` | Clean central local dataset store for new durable exports. Use `datasets/adhoc/` for temporary data-shaped outputs. See `datasets/INDEX.md` and `datasets/MANAGEMENT.md`. |
| `/workspace/backups/` | Point-in-time platform state snapshots (configuration + curated detection data + classifier-worker state) intended for restore. Append-only after capture. Distinct from `datasets/` (data products for reuse in tasks/evals) and `archive/` (truly historical, pre-central-store). See `backups/README.md` and §"Platform State Backups". |
| `/workspace/agent-skills/` | Canonical shared Agent Skills for Claude and Codex. Sync generated mirrors with `/workspace/tools/skills/skillctl`. |
| `/workspace/data/` | Empty compatibility/scratch path. Dataset/export outputs should go to `/workspace/datasets/adhoc/` or a named dataset. |
| `/workspace/testing-data/` | Curated eval datasets (classifier/LLM ground truth). |
| `/workspace/archive/` | Historical repos, completed task archives, and old pre-central-store data. Use only when intentionally requested or needed for provenance. |

Worktree directory names mirror the branch (slashes → dashes): `feat/foo` → `feat-foo`.

## Critical Rules

### 1. Verify Before Asserting
Never assert facts about code, data, or system state without verifying first. If you haven't read the actual source, run the actual container, or queried the actual data, say "I haven't verified this" and go check. Show evidence (file:line, command output) when making claims.

### 2. Minimal, Surgical Changes Only
Deliver exactly what was asked. Do not rewrite adjacent code, refactor surrounding modules, upgrade dependencies, or add "improvements" beyond scope. If broader changes seem warranted, describe them and ask first.

### 3. Docker-Only Execution
- Repo code runs in containers. Period.
- If a `make` target or script runs Python/Go on the host, either (a) run the container-equivalent, or (b) flag it and ask — don't shim by installing host deps.
- For ad-hoc scripts (eval runs, one-off queries), use `docker run --rm -v $(pwd):/work -w /work <image> <cmd>` rather than setting up a local venv.
- `pivoter.env` and `docker-swarm.env` at `/workspace/` are mount/source targets for local-stack containers, not for direct shell execution.

## Local Multi-Worktree Stacks

Use the workspace gateway tool when running more than one local
`detection-platform-metal` stack at the same time:

```bash
/workspace/tools/gateway/gatewayctl stack up <name> <worktree-path> 127.0.0.N \
  --tag latest --no-build
/workspace/tools/gateway/gatewayctl url <name>
/workspace/tools/gateway/gatewayctl doctor
/workspace/tools/gateway/gatewayctl stack down <name>
```

- Tool docs: `/workspace/tools/gateway/README.md`
- State: `/workspace/.agent-gateway/`
- Gateway listener: `127.0.0.1:18000`
- Instance binds: use `127.0.0.2`, `127.0.0.3`, etc.; reserve `127.0.0.1` for the gateway.
- The tool generates Compose overrides outside the repo, binds published ports to the chosen loopback IP, and removes the host bind from `filter-service` so it does not collide with the editor/code-server host `:8080` listener.
- Start targets default to `detection-ui-frontend` and dependencies. Add `--all` only when every Compose service is required.
- Use `--extra-override <file>` for task-specific fixtures or startup overrides.
- VS Code Remote/manual port forwarding works when forwarding port `18000` and browsing `http://<name>.localhost:18000/`.
- code-server path proxy URLs such as `/proxy/<port>/...` do not select host-based routes by themselves. Prefer VS Code Remote for this workflow, or use direct loopback URLs from the host.

### 3a. Detection DB Access
Use the workspace DB utility container, not host-installed clients and not the devcontainer:

```bash
/workspace/tools/db/dbctl auth prod      # refresh Cloudflare Access when needed
/workspace/tools/db/dbctl start prod     # start cloudflared tunnel container
/workspace/tools/db/dbctl psql           # interactive psql in postgres client container
/workspace/tools/db/dbctl query "select current_database(), current_user;"
```

- Credentials live in `/workspace/db.env` with owner-only permissions. Do not print secrets.
- Cloudflare Access browser tokens live in the `detection-db-cloudflared` Docker volume.
- The tunnel and client containers share the private `detection-db-access` Docker network; the DB port is not published on the host.
- The PostgreSQL client container mounts `/workspace`, so exports can write directly to `datasets/` or task directories without devcontainer path limitations. Use `/workspace/datasets/adhoc/` for temporary data-shaped outputs.
- Agent DB use must be read-only unless the user explicitly asks for a mutating operation and the credential permits it.
- For reusable detection incident exports, use `/workspace/tools/datasets/datasetctl` instead of standalone CSV/JSONL dumps. `datasetctl` reads from the DB, stores canonical incident payloads once, records exact query membership by `run_id`, and writes snapshot-shaped JSONL for future API import. It does not write to the DB, import snapshots, or promote `detection_data`.
- If a repo-level skill (e.g. `connect-detection-db`) teaches a host `cloudflared` + `psql` pattern, ignore those commands in this workspace and use `dbctl` (or the `db-readonly-investigation` skill). See §8d for the full upstream-skill resolution rule.

### 4. No Staging / Production
- No kubectl, no gcloud, no GAR, no BigQuery, no ArgoCD. The tooling may still be installed but it is out of scope.
- Staging API endpoints (`api-dev.detection.phishsonar.com`) and production (`api.detection.phishsonar.com`) are off-limits for validation. Use the local stack.
- Exception: read-only detection database access through `/workspace/tools/db/dbctl` is allowed when the user explicitly asks for DB investigation/export work. Record the query, target env, credential path, and output location.
- If something requires staging/prod access, stop and ask — there is probably a local-stack alternative or the feature is out of scope.

### 5. State Your Plan for Non-Trivial Work
For investigations, multi-step fixes, or anything touching 3+ files: state your plan in 2-3 bullets before executing. Include what you'll check, what you'll change, expected outcome. Do not silently switch approaches mid-task.

### 6. Checkpoint Commits for Large Features
For features touching 5+ files: commit and run the container-based test suite after each logical unit. Do not build everything before testing.

### 7. No Auto-Push
You can `git push` and `gh pr create` — but **always ask first**. A user approving one push does not approve all future pushes. Metal PR base is `main`.

Before creating a PR/MR, asking the user to merge, or handing work to another
agent, ensure the PR/MR title uses the repo commit format
`<type>(<scope>): <description>`. Squash merges use the PR/MR title as the
main-branch commit subject, so malformed titles break release changelog
classification. Prefer an explicit `gh pr create --title ...`; do not rely on
`--fill` unless the source commit headline already follows the required format.

### 8. Cross-Agent Compatibility
Write plans, notes, and instructions so either Claude or Codex can resume the work:

- Use `AGENTS.md` as the provider-neutral source of truth; keep `CLAUDE.md` aligned for Claude Code.
- Prefer explicit file paths, commands, branch names, PR/issue links, and validation evidence over chat-only context.
- For non-trivial active tasks, keep `busy/<task>/resume.md` current with Claude/Codex session IDs, resume commands, transcript paths, tmux window names, worktree/branch/PR context, and the next action. Use `/workspace/tools/agents/sessionctl` where possible.
- Agent resume commands must start from `/workspace`, even when the task's code lives in a worktree. Pass the worktree path as context to the resumed chat instead of making it the launch cwd.
- Say "the agent" for shared rules. Use "Claude" or "Codex" only when a tool or behavior is provider-specific.
- If a workflow depends on a Claude-only or OpenAI-only capability, name that dependency and provide the closest fallback.
- Claude sessions can be launched with a preassigned `--session-id`; prefer that for new Claude work. Codex sessions do not currently expose a documented preassigned-ID flag in this workspace, so use a unique tracking token and then record the discovered local transcript/session ID.

### 8a. Agent Session Tracking
Task-local `resume.md` files are the canonical recovery records for active
agent work. `/workspace/detection-platform-metal-work/SESSIONS.md` is a
generated global lookup for convenience; do not hand-edit it.

- Use `/workspace/tools/agents/sessionctl launch-claude` or `launch-codex` for new non-trivial agent windows when practical.
- If an agent was started outside `sessionctl`, record it in the owning task with `/workspace/tools/agents/sessionctl record` as soon as the session ID is known.
- Regenerate the central lookup with `/workspace/tools/agents/sessionctl index` after session records change.
- Use `/workspace/tools/agents/sessionctl reconcile` when recovering from crashes or when `busy/` has tasks without `resume.md`; it creates missing resume files, normalizes old ones, and regenerates `SESSIONS.md`.
- If `SESSIONS.md` lists live agent panes needing IDs, either record the ID from the provider UI/transcript or restart that work through `sessionctl` before it becomes critical.
- Before pausing, handing off, or closing a task, update the task's `resume.md` status/next step and regenerate `SESSIONS.md`.

### 8b. LLM Provider Support
LLM workflow changes must preserve multi-provider operation:

- Treat `packages/py-llm-engine` as the canonical provider abstraction. It resolves Gemini/Google, OpenAI, and Anthropic model prefixes through litellm-compatible model IDs.
- Do not hard-code a single provider in prompts, YAML workflow configs, metrics, dashboards, or UI copy unless the workflow is intentionally provider-specific.
- OpenAI examples should use `openai/...` or `gpt-*` with `OPENAI_API_KEY`; Anthropic examples should use `anthropic/...` or `claude-*` with `ANTHROPIC_API_KEY`; Gemini examples should use `gemini/...` or `google/...` with `GEMINI_API_KEY`/`GOOGLE_API_KEY`.
- When adding model override env vars, avoid provider-named vars unless the override truly only applies to that provider. Prefer neutral names such as `*_LLM_MODEL` for new work.
- Provider comparisons for LLM quality work must record model ID, provider, temperature/max tokens, fixture set, and disagreement examples.

### 8c. Shared Agent Skills
Use Agent Skills for reusable workflows that should be available to both Claude and Codex:

- Canonical shared skills live in `/workspace/agent-skills/skills/<skill-name>/`.
- Provider mirrors live in `/workspace/.claude/skills/` and `/workspace/.agents/skills/`; treat mirrored shared skills as generated copies.
- Edit the canonical skill first, then run:
  ```bash
  /workspace/tools/skills/skillctl validate
  /workspace/tools/skills/skillctl sync
  ```
- Shared `SKILL.md` files must use portable frontmatter: `name` and `description`. Do not require Claude-only tools, Codex-only metadata, dynamic context commands, MCP server names, or hardcoded credentials in canonical instructions.
- Provider-specific metadata may live beside the canonical skill, such as `agents/openai.yaml`, `provider/claude.md`, or `provider/codex.md`, but the shared workflow must remain usable without it.
- Existing provider-specific skills under `.claude/skills` or repo-local skill folders are not automatically portable. Audit and port them intentionally; do not copy them wholesale.

### 8d. Repo-Level Skills vs Workspace Tooling
Upstream `<repo>/.claude/skills/` skills are written for developer laptops with host-installed `cloudflared`, `psql`, and provider CLIs. **Do not modify them to fit this workspace** — the repo serves multiple audiences (laptops, CI, this sandbox). Adaptation is purely workspace-side.

**Precedence rule:** when both a repo-level skill and a workspace-shared skill cover the same job, prefer the workspace skill in this workspace.

Established mappings:

| Repo skill (laptop pattern) | Workspace skill | Wrapper |
|---|---|---|
| `connect-detection-db` | `db-readonly-investigation` | `/workspace/tools/db/dbctl` |
| Dashboard / Loki / Prometheus / API health checks | `cloudflare-access-observability` | `/workspace/tools/access/accessctl` |
| Ad-hoc DB dump scripts inside skills | `detection-dataset-export` | `/workspace/tools/datasets/datasetctl` |

For repo skills that bake host tooling into Python/shell subprocess calls rather than just SKILL.md text (e.g. `audit-pushed-incidents`, `audit-enrichment-data`, `dom-info-quality`, `analyse-metrics`, `generate-enrichment-report`), the trivial wrappers above are not enough. Options, in preference order:

1. **Workspace shadow skill** — same-name canonical skill at `/workspace/agent-skills/skills/<name>/` that re-implements the workflow with workspace tooling. Visible only to agents running in this workspace; laptop checkouts of the repo are unaffected.
2. **Workspace skill-runner container** — a `/workspace/tools/skill-runner/` image carrying the host tools the upstream skill expects (`cloudflared`, `psql`, `python3`, `claude`), attached to the relevant tunnel networks and mounting `/workspace`. The upstream skill runs unmodified inside; outputs land on the shared mount. Build only when needed; don't speculate.
3. **Skip the skill in this workspace** until (1) or (2) lands.

Do not add workspace notes, env-var indirection, host-shim paths, or any other adaptation hooks to the repo skill itself, even if the change is nominally portable. Workspace runtime concerns belong in workspace-side artifacts.

### 9. Review Checkpoints
For non-trivial work, build critique into the task:

- After the plan and source-read phase, run a second-agent critique when tool policy and user request permit it; otherwise run a fresh self-review pass focused on scope, missing files, risky assumptions, and validation strategy.
- Before opening a PR, run a review pass focused on regressions, tests, data migrations, operator impact, and instruction/doc drift.
- For LLM workflows, compare at least two provider/model families when the change affects judgement quality or prompt semantics. Record fixtures, model IDs, run time, and disagreement examples.
- Record review findings in `busy/<task>/notes.md` or `review.md`, including which findings were accepted, rejected, or deferred.

## Workspace Organisation — MANDATORY

### Worktree Rules
- Always use a git worktree for branch work:
  ```bash
  git -C /workspace/detection-platform-metal worktree add \
    /workspace/detection-platform-metal.worktrees/<branch-name> -b <branch-name>
  ```
- Name the worktree directory exactly after the branch (slashes → dashes)
- When the PR merges, remove the worktree:
  ```bash
  git -C /workspace/detection-platform-metal worktree remove <path>
  git -C /workspace/detection-platform-metal worktree prune
  ```

### Work Artifacts Layout
```
detection-platform-metal-work/
  ACTIVE.md                  ← current critical/in-flight task inventory
  SESSIONS.md                ← generated global active/inactive agent-session lookup
  .sessions/index.json       ← generated machine-readable session lookup
  planned/                   ← specs not yet started (<date>.<task>.md)
  busy/<task-name>/          ← active: plan.md, notes.md, resume.md, screenshots/
  later/<task-name>/         ← deferred but likely useful; not active, not superseded
  archived/                  ← paused, superseded, or closed-unmerged work; never delete useful context
  done/
    INDEX.md                 ← master table of all completed tasks
    YYYYMMDD-dow/            ← day directory
      DAY.md                 ← day narrative + task table
      N.<task-name>/         ← N = sequence within the day
        SUMMARY.md           ← what shipped, learnings
        plan.md              ← preserved from busy/
        notes.md             ← preserved from busy/
  investigations/            ← standalone, not tied to a branch
```

### Data Products vs Task Artifacts
**Task artifacts** (plan.md, notes.md, screenshots, logs) stay with the task → `busy/` → `later/` or `done/`.
**Data products** (datasets, exports, submissions, eval results, corpus snapshots) go to `/workspace/datasets/`.

Rule: if data will be referenced by future tasks, has value beyond this task's lifecycle, or is built incrementally across tasks, it belongs in `datasets/`, not nested in `busy/<task>/`.

Historical exports from before the central-store reset live in `/workspace/archive/datasets/`. Do not load or reference that archive by default; consult it only when a task explicitly needs old data or provenance.

### Dataset Management and Traceability
Avoid duplicate storage without losing query provenance:

- Detection incident exports that may be reused across tasks must use the managed store at `/workspace/datasets/detection/` via `/workspace/tools/datasets/datasetctl`.
- Treat query result sets as memberships, not storage units. Tasks must retrieve incidents by `run_id` so they only operate on rows selected by their query, even when some incident payloads were already present locally.
- Durable incident payloads are deduplicated by `source_env + incident_id + row_hash`. If an upstream incident changes, the new row hash is a new version; unchanged payloads are not duplicated.
- Snapshot-shaped exports are for future `/api/v1/snapshots/import` use only. Do not auto-import snapshots and never auto-promote `detection_data` from snapshot exports.
- When an export is meant to match a UI/reporting number, read the code that computes that metric and record the exact predicates. For example, Daily Submissions "new takedowns" is not "all submitted"; it is `gatekeeper_submissions.outcome = 'pushed_new'` plus `LOWER(judgement) = 'bad'`, with any source/date/scope filters applied separately.
- Every durable dataset directory must contain a manifest (`MANIFEST.json` or `SNAPSHOT.md`) with source system, exact query/filter, time window, row counts, schema/version notes, generating task, command/script path, and parent dataset IDs if derived.
- Prefer content-addressed or run-addressed layout for large exports: keep immutable raw exports once, then store derived slices as manifests plus references to parent files, row IDs, hashes, or query predicates. Do not copy multi-GB raw data just to create a filtered view.
- If a task needs a subset, write a small derived artifact plus a pointer to the canonical parent. When feasible, use Parquet partitioning, DuckDB views, symlinks, or manifest references rather than another full JSONL/CSV copy.
- Keep task-local analysis scripts in the task directory, but write reusable outputs under `/workspace/datasets/<domain>/<dataset-id>/`.
- `datasets/INDEX.md` is a human index, not the manifest. Update it for discoverability, but keep machine-readable provenance next to the data.
- For production exports, record whether the workspace no-prod rule was explicitly waived, the credential path used, and whether the operation was read-only or mutating.

### Platform State Backups

`/workspace/backups/` holds point-in-time captures of detection-platform state intended for disaster-recovery restore. Each backup is a tree of JSON dumps mirroring the API surfaces required to reconstitute the platform. Distinct from `datasets/` (data products for reuse in tasks/evals) and `archive/` (truly historical, pre-central-store).

- Naming: `<platform>/<env>-<YYYY-MM-DD>/` (e.g. `detection-platform/prod-2026-05-11/`).
- Required `MANIFEST.json`: source environment, endpoint URLs, exact API filters/queries, time window + extraction timestamp (UTC), row counts per section, credential path used (not the secret value), explicit production-access waiver record, read-only flag.
- Required `README.md`: restore notes (which sections map to which endpoints; ordering; gotchas).
- Detection-platform layout convention:
  - `migrate-shape/` — mirrors the GET phase of `infrastructure/docker/migrate.sh` (clients+assets, referenced enrichment_snapshots, detection_data target_types, rules, feeder settings, gatekeeper limits, TR publishing configs).
  - `clustering-api/` — `/api/clustering/*` and `/api/hash-list/*` dumps from classifier-worker via the detection-ui proxies (covers building/labeled/graduated clusters and runs).
  - `classifier-extras/` — classifier-adjacent config that `migrate.sh` deliberately does not cover: `/api/v1/classifier` (registry), `/api/v2/llm/configs` (LLM workflow / evaluator routing), `/api/v1/enrichment-exclusions`, and per-client `/api/v1/corpus/config/<clientId>`. These often look empty in prod but the empty state is itself meaningful (vs. unset).
- Treat directories as append-only after capture. Re-runs land in a new dated directory.
- Backup scripts start task-local under `busy/<task>/`; promote to `/workspace/tools/<name>/` only when recurring or shared.
- Cross-check expectation: detection-core `detection_data` with `target_type=ssdeep_cluster` row count must equal classifier-worker `/api/clustering/clusters?status=graduated` filtered to `promoted=true`. Record the result in `MANIFEST.json`.
- Restore path is operator-driven (e.g. replay via `migrate.sh` with a stub source serving the dumped JSON; clustering API has no bulk import — restore semantics for that need to be designed before relying on the backup for clustering recovery).

### Screenshots
- During tasks → `busy/<task>/screenshots/` — **never** in `/workspace/` root or `investigations/` root
- Investigation screenshots → `investigations/<topic>/screenshots/`
- Playwright MCP: save directly to the task's screenshots dir, not the default `.playwright-mcp/`

### Task Close-Off (after PR merge)
1. Verify merge: `gh pr view <N> --json state`
2. Write `SUMMARY.md`: what shipped, learnings, skill suggestions
3. Save reusable learnings to memory if applicable
4. **Harvest data products**: if `busy/<task>/` contains exports/datasets, move them to `/workspace/datasets/` and leave a pointer in `notes.md`
5. Move to done: `mv busy/<task>/ done/YYYYMMDD-dow/N.<task>/` — **never `rm -rf`** the busy dir
6. Update `done/YYYYMMDD-dow/DAY.md` and `done/INDEX.md`
7. Remove worktree + prune

At session start, read `ACTIVE.md`, then `SESSIONS.md`, then each relevant task's `resume.md`, and scan `busy/` for stale tasks whose PRs already merged.

### Task Archiving
Before moving anything out of `busy/`, read `/workspace/detection-platform-metal-work/ACTIVE.md`.

- Keep these critical in-flight tasks unless the user explicitly says otherwise: LLM rethink/domain LLM v2, LLM detection UI, and clustering proposal.
- Move merged/completed tasks to `done/YYYYMMDD-dow/N.<task>/` with `SUMMARY.md` or a clear pointer to the preserved plan/notes.
- Move deferred-but-promising tasks to `later/<task>/` when they are not active
  now, not merged, and not superseded. Update the task `resume.md` first with
  the reason for deferral, preserved branch/worktree/PR context, artifact paths,
  and the condition that should bring the task back into `busy/`. Regenerate
  `SESSIONS.md` afterward with `/workspace/tools/agents/sessionctl index`.
- Move paused, superseded, or closed-unmerged tasks to `archived/YYYYMMDD-<reason>/<task>/`; never `rm -rf` task context.
- Remove a worktree only after `git status --short` is clean and the branch/PR state is verified. Branches can remain even when the local worktree is removed.

## PR Migration: detection-platform → detection-platform-metal

When porting an open PR from the archived detection-platform repo into metal:

1. **Find the source**:
   - Branch: `/workspace/archive/detection-platform.worktrees/<branch>/`
   - Plan/notes: `/workspace/archive/detection-platform-work/{busy,done/*}/<task>/`
2. **Create the metal worktree** on a matching branch name from `/workspace/detection-platform-metal`
3. **Port service-code changes only**. Skip:
   - `infrastructure/helm-charts/` (no Helm in metal)
   - `argocd/`, `terraform/` (no ArgoCD, different terraform)
   - GAR image tags / CI workflows that push to GAR
4. **Validate via the local stack** — `infrastructure/docker/deploy.sh` brings up the Swarm stack. Do not test against staging.
5. **Record in the new task's `plan.md`** with a header:
   ```
   **Migrated from**: detection-platform <branch> / PR #<N>
   **Source archive**: /workspace/archive/detection-platform-work/{busy,done/<date>}/<orig-task>/
   ```
6. Once all PRs are migrated, the compat symlinks (`/workspace/detection-platform*` → archive) can be deleted.

## Archive Pointers

- `/workspace/archive/README.md` — full index
- `/workspace/archive/tooling-notes/CLAUDE-gke.md` — the pre-migration CLAUDE.md (GKE/staging/ArgoCD/GAR workflows)
- `/workspace/archive/tooling-notes/MEMORY-gke.md` — the pre-migration memory index
- `/workspace/archive/tooling-notes/memory-gke/` — archived individual memory files

## Backward-Compat Symlinks

These exist so committed code in active metal worktrees (e.g. fixture JSONLs referencing old paths) keeps resolving during the migration period:

- `/workspace/detection-platform{,.worktrees,-work}` → `archive/…`
- `/workspace/claude-sandbox-sa-{staging,production}.json` → `archive/loose-files/credentials/…`
- `/workspace/classifiers*.env`, `detection-core.env`, `submit-tr.env` → `archive/loose-files/envs/…`

Don't write new code that depends on these symlinks. Use archive paths explicitly, or lift the value into `docker-swarm.env` / metal config. Symlinks get removed once all PR migrations are complete.

## Repo-Level Instructions

`/workspace/detection-platform-metal/CLAUDE.md` covers repo-internal architecture, test commands, and coverage thresholds. Defer to it for codebase-specific guidance. This file covers sandbox/environment conventions.
