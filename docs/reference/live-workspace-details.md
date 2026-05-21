# Live Workspace Details

Status: reference material, load only when needed

This reference holds operational detail that should not be always-loaded in
`/workspace/AGENTS.md`.

## Local Multi-Worktree Stacks

Use the workspace gateway when running more than one local
`detection-platform-metal` stack:

```bash
/workspace/tools/gateway/gatewayctl stack up <name> <worktree-path> 127.0.0.N --tag latest --no-build
/workspace/tools/gateway/gatewayctl url <name>
/workspace/tools/gateway/gatewayctl doctor
/workspace/tools/gateway/gatewayctl stack down <name>
```

Key points:

- Tool docs: `/workspace/tools/gateway/README.md`
- State: `/workspace/.agent-gateway/`
- Gateway listener: `127.0.0.1:18000`
- Use instance binds such as `127.0.0.2`, `127.0.0.3`; reserve
  `127.0.0.1` for the gateway.
- Start targets default to `detection-ui-frontend` and dependencies. Add
  `--all` only when every Compose service is required.
- Use a unique stack name and loopback IP per worktree. Check current
  allocations with `gatewayctl status` or `gatewayctl stack list`.
- Use `--no-build` only after confirming the required tagged local images
  exist. If a stack fails on a missing `localhost:5000/*:<tag>` image or no
  local registry is listening, treat that as an image/registry blocker.
- Prefer direct loopback URLs or VS Code Remote port forwarding over
  code-server path proxy URLs when host-based routing matters.

## Local Classifier And LLM Environment

Local classifier, brand-corpus, and LLM validation may need AI provider
credentials. In this workspace the local env file is:

```text
/workspace/classifiers.env
```

Do not print values from this file. Check only variable names or presence, and
pass it to Docker or Compose as an env file. Do not conclude credentials are
missing just because the current agent process environment lacks provider keys.

## Detection DB Access

Use the workspace DB utility container, not host-installed clients:

```bash
/workspace/tools/db/dbctl auth prod
/workspace/tools/db/dbctl start prod
/workspace/tools/db/dbctl psql
/workspace/tools/db/dbctl query "select current_database(), current_user;"
```

Key points:

- Credentials live in `/workspace/db.env`; do not print secrets.
- Cloudflare Access browser tokens live in the `detection-db-cloudflared`
  Docker volume.
- DB access is read-only unless the user explicitly asks for a mutating
  operation and the credential permits it.
- For reusable detection incident exports, use
  `/workspace/tools/datasets/datasetctl` instead of ad-hoc CSV/JSONL dumps.

## No Staging Or Production Validation

Validation uses the local stack. The following are out of scope for routine
validation:

- kubectl,
- gcloud,
- GAR,
- BigQuery,
- ArgoCD,
- staging API endpoints,
- production API endpoints.

Exception: read-only detection database access through `dbctl` is allowed when
the task explicitly asks for DB investigation/export work. Record the query,
target environment, credential path, and output location.

If a task appears to require staging or production validation, stop and ask.
There is usually a local-stack alternative, or the work is outside this
sandbox's validation scope.

## Docker Execution And Env Files

Agents run on the host; repo code runs in Docker containers.

Use repo Docker tooling:

- `docker compose`,
- `docker stack`,
- per-service Dockerfiles under `infrastructure/docker/`,
- repo Make targets only when they invoke Docker themselves.

For ad-hoc repo scripts, use a container with the workspace mounted, for
example:

```bash
docker run --rm -v /workspace:/workspace -w "$PWD" <image> <cmd>
```

Workspace env files are inputs to local-stack containers and workspace tools,
not general shell setup files. Treat these as env-file or mount targets unless a
tool documents otherwise:

- `/workspace/docker-swarm.env`,
- `/workspace/pivoter.env`,
- `/workspace/classifiers.env`.

Do not print secret values from env files.

## Agent Session Tracking

Task-local `resume.md` files are the canonical recovery records for active
agent work. `/workspace/detection-platform-metal-work/SESSIONS.md` is a
generated convenience index; do not hand-edit it.

Use:

```bash
/workspace/tools/agents/sessionctl launch-claude
/workspace/tools/agents/sessionctl launch-codex
/workspace/tools/agents/sessionctl record
/workspace/tools/agents/sessionctl index
/workspace/tools/agents/sessionctl reconcile
```

Agent resume commands should start from `/workspace`; pass the worktree path as
context instead of making it the launch cwd.

Claude sessions can be launched with a preassigned `--session-id`. Codex
sessions do not currently expose a documented preassigned-ID flag in this
workspace, so use a unique tracking token and record the discovered transcript
or session ID.

## Browser MCP And Agent Browser Review

Use the workspace wrapper for browser MCP sessions:

```bash
/workspace/tools/browser-mcp/browser-mcp detection-ui
```

Key points:

- Tool docs: `/workspace/tools/browser-mcp/README.md`
- Shared skill: `detection-ui-browser-review`
- Config seed files: `/workspace/.mcp.json` and
  `/workspace/workspace-control/current-workspace/config/`
- Set `AGENT_BROWSER_OUTPUT_DIR` before launching the agent client when
  screenshots or saved browser artifacts are required.
- Keep browser artifacts under `busy/<task>/screenshots/` or
  `investigations/<topic>/screenshots/`.
- Browser MCP review is exploratory. Keep Docker-backed unit, frontend, and
  Playwright e2e tests as regression validation for code changes.

If an already-running agent reports `Transport closed`, the existing stdio MCP
transport cannot be repaired from inside that chat. Check and clean stale
Playwright MCP runtimes, then restart or resume the agent client from
`/workspace`:

```bash
/workspace/tools/browser-mcp/browser-mcp doctor
/workspace/tools/browser-mcp/browser-mcp cleanup --dry-run
/workspace/tools/browser-mcp/browser-mcp cleanup
```

The cleanup command targets Playwright MCP containers/processes only. It does
not stop the local gateway, detection-ui stacks, DB tunnels, or application
containers.

## Shared Agent Skills

Canonical shared skills live in:

```text
/workspace/agent-skills/skills/<skill-name>/
```

Generated provider mirrors live in:

```text
/workspace/.claude/skills/
/workspace/.agents/skills/
```

Rules:

- Edit the canonical skill first.
- Shared `SKILL.md` frontmatter must use only `name` and `description`.
- Provider-specific notes may live beside the canonical skill, for example
  `agents/openai.yaml`, `provider/claude.md`, or `provider/codex.md`.
- Existing provider-specific skills are not automatically portable; audit and
  port them intentionally.

Validation/sync:

```bash
/workspace/tools/skills/skillctl validate
/workspace/tools/skills/skillctl sync
```

## Repo-Level Skills Vs Workspace Tooling

Upstream `<repo>/.claude/skills/` skills are written for developer laptops.
When both a repo-level skill and workspace-shared skill cover the same job,
prefer the workspace skill in this sandbox.

Established mappings:

| Repo skill or laptop pattern | Workspace skill | Wrapper |
|---|---|---|
| `connect-detection-db` | `db-readonly-investigation` | `/workspace/tools/db/dbctl` |
| Dashboard, Loki, Prometheus, API health checks | `cloudflare-access-observability` | `/workspace/tools/access/accessctl` |
| Ad-hoc DB dump scripts inside skills | `detection-dataset-export` | `/workspace/tools/datasets/datasetctl` |

For repo skills that bake host tooling into Python/shell subprocess calls,
choose one of:

1. a workspace shadow skill,
2. a workspace skill-runner container,
3. skip the skill in this workspace until an adaptation exists.

Do not add workspace-specific adaptation hooks to the product repo skill
itself.

## LLM Provider Support

LLM workflow changes must preserve multi-provider operation.

- Treat `packages/py-llm-engine` as the canonical provider abstraction.
- Use litellm-compatible model IDs: OpenAI as `openai/...` or `gpt-*`,
  Anthropic as `anthropic/...` or `claude-*`, Gemini as `gemini/...` or
  `google/...`.
- Use the matching provider key names when examples require keys:
  `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, or
  `GOOGLE_API_KEY`.
- Avoid provider-named override env vars unless the override is intentionally
  provider-specific. Prefer neutral names such as `*_LLM_MODEL`.
- Provider comparisons should record model ID, provider, temperature/max
  tokens, fixture set, run time, and disagreement examples.

## Dataset Management And Traceability

Detection incident exports that may be reused across tasks should use the
managed store at `/workspace/datasets/detection/` through `datasetctl`.

Traceability rules:

- Treat query result sets as memberships, not storage units.
- Retrieve incidents by `run_id` so tasks operate only on rows selected by the
  original query.
- Durable incident payloads are deduplicated by
  `source_env + incident_id + row_hash`.
- Snapshot-shaped exports are for future `/api/v1/snapshots/import` use only;
  do not auto-import snapshots or auto-promote `detection_data`.
- When an export must match a UI/reporting number, read the implementation and
  record exact predicates.
- Every durable dataset directory needs a manifest with source system, query or
  filters, time window, row counts, schema notes, generating task, command or
  script path, and parent dataset IDs if derived.
- Prefer manifests, references, symlinks, DuckDB views, or Parquet partitions
  over copying large raw files for filtered views.

Historical exports from before the central-store reset live in
`/workspace/archive/datasets/`. Use `/workspace/datasets/` for current data
products.

## Platform State Backups

`/workspace/backups/` holds point-in-time captures of detection-platform state
intended for disaster-recovery restore. It is distinct from datasets and
archive provenance.

Naming:

```text
<platform>/<env>-<YYYY-MM-DD>/
```

Required:

- `MANIFEST.json` with source environment, endpoint URLs, filters/queries,
  extraction timestamp, row counts, credential path, production-access waiver
  record, and read-only flag.
- `README.md` with restore notes, endpoint mapping, ordering, and gotchas.

Detection-platform backup layout convention:

- `migrate-shape/`: mirrors the GET phase of
  `infrastructure/docker/migrate.sh`.
- `clustering-api/`: `/api/clustering/*` and `/api/hash-list/*` dumps.
- `classifier-extras/`: classifier registry, LLM configs, exclusions, and
  corpus config.

Treat backup directories as append-only after capture. Re-runs land in a new
dated directory.

Backup scripts start under the active task. Promote them to `/workspace/tools/`
only when recurring or shared.

Cross-check expectation: detection-core `detection_data` rows with
`target_type=ssdeep_cluster` should match classifier-worker
`/api/clustering/clusters?status=graduated` filtered to `promoted=true`. Record
the result in `MANIFEST.json`.

Restore is operator-driven. Clustering APIs do not currently have a bulk import
path, so restore semantics for clustering need to be designed before relying on
the backup for clustering recovery.

## Task Close-Off

After PR merge or accepted completion:

1. Verify merge state, for example `gh pr view <N> --json state`.
2. Write `SUMMARY.md` with what shipped, learnings, and skill suggestions.
3. Capture reusable learnings or state "none".
4. Move reusable data products to `/workspace/datasets/` and leave pointers.
5. Move task context to the right lifecycle state.
6. Update `done/YYYYMMDD-dow/DAY.md` and `done/INDEX.md` when using `done/`.
7. Remove worktree only after status is clean and branch/PR state is verified.

Before moving anything out of `busy/`, read
`/workspace/detection-platform-metal-work/ACTIVE.md`.
At session start, also scan `busy/` for stale tasks whose PRs already merged.

Keep these critical in-flight threads unless explicitly told otherwise:

- LLM rethink / domain LLM v2,
- LLM detection UI,
- clustering proposal.

## PR Migration From GKE Archive To Metal

When porting an open PR from archived `detection-platform` into metal:

1. Find source branch under
   `/workspace/archive/detection-platform.worktrees/<branch>/`.
2. Find source plan/notes under
   `/workspace/archive/detection-platform-work/{busy,done/*}/<task>/`.
3. Create the metal worktree from `/workspace/detection-platform-metal`.
4. Port service-code changes only.
5. Skip Helm, ArgoCD, Terraform, GAR image tags, and CI workflows that push to
   GAR.
6. Validate through the local stack only.
7. Record the migration source in the new task `plan.md`.

Suggested plan header:

```markdown
**Migrated from**: detection-platform <branch> / PR #<N>
**Source archive**: /workspace/archive/detection-platform-work/{busy,done/<date>}/<orig-task>/
```

## Archive Pointers

- `/workspace/archive/README.md`: full archive index.
- `/workspace/archive/tooling-notes/CLAUDE-gke.md`: pre-migration GKE
  workspace instructions.
- `/workspace/archive/tooling-notes/MEMORY-gke.md`: pre-migration memory
  index.
- `/workspace/archive/tooling-notes/memory-gke/`: archived individual memory
  files.

## Backward-Compatibility Symlinks

Compatibility symlinks exist so committed code in active metal worktrees keeps
resolving during migration:

- `/workspace/detection-platform{,.worktrees,-work}` -> archive paths.
- `/workspace/claude-sandbox-sa-{staging,production}.json` -> archived loose
  credentials.
- `/workspace/classifiers*.env`, `detection-core.env`, `submit-tr.env` ->
  archived loose envs.

Do not write new code that depends on these symlinks. Use explicit archive
paths or lift values into `docker-swarm.env` / metal config.
