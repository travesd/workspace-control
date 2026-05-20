# Core Recommendations Implementation Plan

Date: 2026-05-20

Status: proposed, not activated

Source investigation:

- `/workspace/detection-platform-metal-work/investigations/notes-and-incident-cache-20260520/synthesis.md`
- `/workspace/detection-platform-metal-work/investigations/notes-and-incident-cache-20260520/reviews/notes-review.md`
- `/workspace/detection-platform-metal-work/investigations/notes-and-incident-cache-20260520/reviews/incident-cache-review.md`
- `/workspace/detection-platform-metal-work/investigations/notes-and-incident-cache-20260520/reviews/karpathy-followup.md`

## Objective

Implement the investigation's core recommendations as staged, reviewable artifacts in `workspace-control` only. Promotion into the live `/workspace` runtime is a separate future decision and is not part of this implementation plan.

The target operating model is:

1. Markdown remains the canonical source for durable workspace knowledge.
2. Generated indexes and small helper tools make knowledge lookup reliable.
3. Shared skills make learning capture, research capture, task close-off, and incident dataset handling repeatable across Claude and Codex.
4. Local incident exports become a durable scope index plus expiring payload cache, not a second long-term incident archive.
5. Pi pilot mappings track the same provider-neutral workflows without becoming a separate source of truth.

## Non-Goals

- Do not activate changes into `/workspace/AGENTS.md`, `/workspace/agent-skills/`, or provider mirrors without approval.
- Do not modify live `/workspace/tools`, `/workspace/datasets`, `/workspace/backups`, `/workspace/AGENTS.md`, `/workspace/agent-skills`, provider mirrors, or product repos as part of this plan.
- Do not prune or delete dataset payloads in the first implementation slice.
- Do not introduce local Postgres for incident cache work unless later evidence shows DuckDB cannot handle the workflow.
- Do not vendor raw provider transcripts, provider-local memory exports, secrets, datasets, screenshots, backups, or runtime caches into this repo.
- Do not change detection-platform-metal product code as part of this plan.

## Guiding Constraints

- Respect `ACTIVATION.md`: this repo is reviewable source, not live runtime.
- Use provider-neutral skill instructions under `agent-skills/skills/`; provider-specific notes stay in provider metadata files only when necessary.
- Keep helper scripts dependency-light and host-safe. Existing repo tools use shell/perl; if Python is later used for workspace-control helpers, it must not execute product repo code or require host package installation.
- Treat generated indexes as discovery surfaces. The underlying Markdown notes and manifests remain authoritative.
- Preserve exact query scope and provenance for incident work even when payloads expire.

## Workstream A: Knowledge Lifecycle

### A1. Add Knowledge Contract Docs

Files:

- `knowledge/README.md`
- `knowledge/TEMPLATE.md`
- update `knowledge/INDEX.md` header once generated indexing exists

Implementation:

1. Document lookup order:
   - read live instructions,
   - run or read workspace status,
   - search generated knowledge index,
   - open only relevant notes,
   - open evidence paths for load-bearing claims.
2. Document promotion rules:
   - task-specific details stay in task notes or summaries,
   - reusable facts/gotchas become knowledge notes,
   - procedures become shared skills,
   - stable safety rules become `AGENTS.md`,
   - dataset-specific truths remain in dataset manifests.
3. Add a durable note template with required frontmatter:

   ```yaml
   ---
   title: Short human title
   type: feedback | project-fact | workflow | gotcha | decision-pointer
   tags: [workspace, detection]
   status: active | under-review | deprecated | superseded
   scope: workspace | repo | service | dataset | task
   verified: 2026-05-20
   source: /workspace/path/to/evidence.md
   re_verify_when: "Before automating, promoting to AGENTS.md, or after related tool changes"
   ---
   ```
4. Backfill existing seed notes with `type` and `scope`, or explicitly mark them as legacy seed notes that `knowledgectl lint` treats as warn-only until backfilled.

Acceptance criteria:

- A new agent can determine where to put a learning without reading the whole knowledge directory.
- Existing memory-migration notes are explicitly treated as seed notes that need stronger evidence before automation or global-rule promotion.
- Existing notes do not make the first strict lint run fail unexpectedly; either they are backfilled or legacy-handled by design.

Validation:

- Manual review of docs.
- `tools/check-sensitive-content .` passes.

### A2. Add `knowledgectl`

Files:

- `tools/knowledgectl`
- optionally `docs/reference/knowledgectl.md` if usage outgrows inline help

Commands:

- `tools/knowledgectl lint`
- `tools/knowledgectl index`
- `tools/knowledgectl index --check`
- `tools/knowledgectl search <query>`
- `tools/knowledgectl stale`

Implementation details:

1. `lint`
   - Scan `knowledge/*.md`, excluding `INDEX.md`, `README.md`, and `TEMPLATE.md`.
   - Require the frontmatter fields from A1.
   - Validate enum values for `type`, `status`, and `scope`.
   - Require `source` to be a path, URL, or explicit migration/source note.
   - Flag source paths pointing at ignored/secrets/provider-transcript areas.
   - Warn, not fail, when `source` is weak migration provenance.
   - Support an explicit transitional mode for legacy seed notes until A1 backfill is complete.
2. `index`
   - Generate `knowledge/INDEX.md` from note metadata.
   - Generate `knowledge/index.json` for machine lookup.
   - Sort deterministically by `type`, then title.
   - Preserve a small hand-written intro block only if the tool owns the generated section markers.
3. `index --check`
   - Regenerate into a temp file and fail if committed index output is stale.
4. `search`
   - Start with `rg` over title/tags/body and the generated JSON.
   - Defer SQLite FTS until note volume or lookup friction justifies it.
5. `stale`
   - List notes with non-active status.
   - List notes with weak migration provenance.
   - Optionally warn on old `verified` dates, but do not pretend to understand arbitrary `re_verify_when` text automatically.

Acceptance criteria:

- `tools/knowledgectl lint` exits non-zero for malformed required frontmatter.
- Existing seeded notes are either compliant or reported as explicit warn-only legacy records.
- `tools/knowledgectl index --check` can be used in pre-commit/review.
- `tools/knowledgectl search git identity` finds the existing git identity note.
- `tools/knowledgectl stale` surfaces migration-provenance notes without blocking normal use.

Validation:

- Run all `knowledgectl` commands against this repo.
- Run `tools/check-sensitive-content .`.

### A3. Wire Knowledge Health Into Status

Files:

- `tools/workspace-status`
- possibly `tools/workspace-artifact-inventory`

Implementation:

1. Add a compact "Knowledge Health" section:
   - note count,
   - under-review/deprecated/superseded count,
   - weak-provenance count,
   - stale index warning,
   - pointer to `knowledge/INDEX.md`.
2. Keep `workspace-status --brief` under the intended short orientation size.
3. Put heavier details only in `workspace-artifact-inventory` or `knowledgectl stale`.

Acceptance criteria:

- `tools/workspace-status --brief` remains concise.
- The status output identifies whether the knowledge index is stale without printing note bodies.

Validation:

- `tools/workspace-status --brief`
- `tools/workspace-status --full`
- `tools/workspace-artifact-inventory`

## Workstream B: Skills And Templates

### B1. Tighten `durable-learning-capture`

Files:

- `agent-skills/skills/durable-learning-capture/SKILL.md`

Implementation:

1. Require agents to start from task evidence, code paths, command output, dataset manifests, or approved user decision records.
2. Require the routing decision to be written explicitly:
   - task-only,
   - knowledge note,
   - shared skill,
   - `AGENTS.md`,
   - dataset/backup manifest,
   - ADR.
3. Add a `promotion_verified` rule:
   - weak memory-migration notes can be used for lookup,
   - but need fresh evidence before becoming automation, skills, or global rules.
4. Reference `knowledge/TEMPLATE.md` and `tools/knowledgectl lint`.

Acceptance criteria:

- The skill tells agents exactly when not to globalize a learning.
- The skill is portable across Claude and Codex.

Validation:

- Review frontmatter: only `name` and `description`.
- Do not run live `skillctl` as part of this plan.
- Future activation validation, if separately approved, would include `/workspace/tools/skills/skillctl validate`.

### B2. Add `research-to-knowledge`

Files:

- `agent-skills/skills/research-to-knowledge/SKILL.md`
- optional `agent-skills/skills/research-to-knowledge/references/template.md`
- `.pi/workflows/research-to-knowledge.json`

Implementation:

1. Create a shared skill for external research capture.
2. Required output shape:
   - source reviewed,
   - useful pattern,
   - workspace-specific implication,
   - proposed action,
   - evidence strength,
   - where it should live.
3. Explicitly prohibit storing full external articles, raw transcripts, secrets, or generic summaries with no workspace implication.
4. Use Karpathy follow-up as the first example:
   - compact Markdown operating context,
   - narrow editable surfaces,
   - fixed metrics,
   - experiment logs,
   - safety caveats.

Acceptance criteria:

- External research produces concise project-contextual notes, not generic research dumps.
- The skill can be used by both Claude and Codex.

Validation:

- Run `tools/check-sensitive-content .`.
- Review the skill for provider-specific tooling assumptions.

### B3. Add Experiment Log Template

Files:

- `docs/templates/experiment-log.md`
- optional `docs/templates/experiment-log.tsv.header`
- update relevant skills:
  - `agent-skills/skills/task-closeoff/SKILL.md`
  - LLM/evaluator-related skills when touched later

Template fields:

- run id,
- task path,
- branch/commit or config hash,
- editable files,
- read-only harness files,
- command,
- metric,
- fixture/data scope,
- result,
- keep/discard/defer decision,
- follow-up note or linked artifact.

Acceptance criteria:

- LLM/evaluator and cache experiments have a standard low-friction log format.
- The template supports both Markdown summaries and TSV/JSONL machine logs.

Validation:

- Use the template in one future test task before making it mandatory.

### B4. Update Task/Subagent Brief Template

Files:

- `docs/templates/subagent-brief.md`
- update `.pi/agents/*` or `.pi/workflows/*` only where the same concept exists

Required sections:

- objective,
- context paths,
- editable paths,
- read-only paths,
- output path,
- validation,
- forbidden actions,
- review questions.

Acceptance criteria:

- Future delegated work has explicit ownership and validation boundaries.
- Briefs can be used with Claude, Codex, or Pi-style agents.

Validation:

- Use in the next multi-agent investigation before promoting to a global rule.

## Workstream C: Incident Scope Cache Specification

### C1. Add Design Spec

Files:

- `docs/specs/incident-scope-cache.md`
- update `current-workspace/tools/README.md` with a pointer

Spec content:

1. Terminology:
   - scope index,
   - projection index,
   - payload cache,
   - materialization,
   - durable fixture,
   - backup.
2. Retention classes:
   - `ephemeral`,
   - `task-cache`,
   - `reusable-scope`,
   - `durable-fixture`,
   - `backup` as out-of-scope for `datasetctl`.
3. Proposed DuckDB schema extensions:
   - `schema_migrations`,
   - `tags`,
   - `run_tags`,
   - `incident_tags`,
   - `run_retention`,
   - `incident_projection`,
   - `payload_cache_entries`,
   - `cache_eviction_log`.
4. CLI additions:
   - `datasetctl cache status`,
   - `datasetctl runs tag`,
   - `datasetctl runs retention`,
   - `datasetctl export incidents --retention-class ... --tag namespace:key=value`,
   - future `datasetctl cache prune --dry-run`.
5. Compatibility policy:
   - no deletion in first slice,
   - existing exports marked legacy-retained,
   - snapshot JSONL generation remains compatible until callers are migrated,
   - new materialization behavior introduced behind explicit flags.

Acceptance criteria:

- A developer can implement the schema and CLI changes without rereading the whole investigation.
- The spec explains why local Postgres is deferred.
- The spec states what metadata is never pruned: run, query, membership, hashes, counts, manifests.
- The spec is clearly marked as proposed and not active live `datasetctl` behavior.

Validation:

- Review against current `/workspace/tools/datasets/datasetctl.py` as read-only reference.
- Review against `/workspace/datasets/MANAGEMENT.md` as read-only reference.

### C2. Update Dataset Export Skill

Files:

- `agent-skills/skills/detection-dataset-export/SKILL.md`

Implementation:

1. Preserve current guarantees:
   - read-only DB access,
   - `run_id` is the query result set,
   - no API import,
   - no `detection_data` promotion.
2. Add decision guidance:
   - use scope-cache mode for task investigations,
   - use durable-fixture mode only when payloads must persist,
   - use `/workspace/backups` for platform recovery snapshots,
   - use `/workspace/datasets/adhoc` for temporary materializations.
3. Add expected future flags but mark them as pending until live `datasetctl` supports them.

Acceptance criteria:

- The skill reflects the new cache model without claiming unsupported commands are active.
- Agents remain unable to confuse "incident is stored locally" with "incident was selected by this query."

Validation:

- Review skill text for command/support accuracy.
- Do not run live `skillctl` as part of this plan.
- Future activation validation, if separately approved, would include `skillctl validate && skillctl sync`.

## Workstream D: Future Live Dataset Tool Notes

This section is not an implementation workstream for this plan. It records future live-rollout notes so the staged `workspace-control` spec can be evaluated against the eventual tool changes. No files under `/workspace/tools`, `/workspace/datasets`, or any live runtime path are modified by this plan.

### D1. Future Non-Destructive Schema Migration

Future live files, not touched by this plan:

- `/workspace/tools/datasets/datasetctl.py`
- `/workspace/tools/datasets/README.md`
- `/workspace/datasets/MANAGEMENT.md`

Implementation:

1. Add a `schema_migrations` table and migration runner.
2. Add tag/retention/projection/cache tables from C1.
3. Backfill existing runs:
   - retention class `legacy-retained`,
   - tags from `name`, `task_path`, `source_env`, `query_path`,
   - projection rows from existing incident current/version payloads where possible.
4. Do not delete or move payloads.

Future acceptance criteria:

- Existing `runs list`, `runs show`, and `materialize incidents` behavior remains unchanged.
- Re-running `datasetctl init` is idempotent.

Future validation:

- Run against the existing catalog with a backup copy or dry-run migration first.
- Compare run counts, membership counts, and snapshot export counts before/after.

### D2. Future Cache Status And Tags

Future live files, not touched by this plan:

- `/workspace/tools/datasets/datasetctl.py`
- `/workspace/tools/datasets/README.md`

Implementation:

1. Add `datasetctl cache status`:
   - catalog size,
   - snapshot JSONL bytes,
   - Parquet bytes,
   - payload cache rows by retention class,
   - untagged run count,
   - legacy-retained count.
2. Add `datasetctl runs tag <run_id> namespace:key=value`.
3. Add `datasetctl runs retention <run_id> --class ... --expires-at ... --pin`.

Future acceptance criteria:

- Operators can see storage pressure before any prune command exists.
- Tags and retention can be applied to old runs without re-export.

Future validation:

- Run `cache status` on current catalog.
- Tag one non-critical test/smoke run and show it round-trips in `runs show`.

### D3. Future Export Flags

Future live files, not touched by this plan:

- `/workspace/tools/datasets/datasetctl.py`
- `/workspace/tools/datasets/README.md`
- `/workspace/datasets/MANAGEMENT.md`

Implementation:

1. Add `--retention-class`, defaulting to:
   - `task-cache` when `--task-path` is supplied,
   - `reusable-scope` otherwise.
2. Add repeated `--tag namespace:key=value`.
3. Populate `incident_projection` during export from fetched payload and query row.
4. Keep snapshot JSONL generation by default during compatibility period.
5. Add a future-compatible `--write-snapshot-jsonl/--no-write-snapshot-jsonl` flag, but do not flip the default until callers are reviewed.

Future acceptance criteria:

- New exports carry structured tags/retention/projection.
- Existing callers are not broken.

Future validation:

- Use a small read-only test query.
- Verify run manifest, catalog rows, projection rows, and materialized output.

### D4. Future Dry-Run Prune Only

Future live files, not touched by this plan:

- `/workspace/tools/datasets/datasetctl.py`

Implementation:

1. Add `datasetctl cache prune --dry-run`.
2. Refuse non-dry-run deletion initially.
3. Report candidate bytes/rows by retention class and task state.
4. Refuse to select runs linked to `busy/` tasks unless explicitly overridden in a future implementation.

Future acceptance criteria:

- The workspace can estimate savings without risk.
- No files are deleted.

Future validation:

- Run dry-run on current catalog and record output in a task note.

## Workstream E: Pi Pilot Translation

Files:

- `.pi/workflows/durable-learning-capture.json`
- `.pi/workflows/task-closeoff.json`
- `.pi/workflows/session-hygiene.json`
- `.pi/workflows/research-to-knowledge.json`
- `pi-pilot/translation-map.md`
- `pi-pilot/WORKFLOWS.md`

Implementation:

1. Translate new/updated shared skills into Pi workflow drafts.
2. Keep Pi workflows descriptive until the package/schema is selected and validated.
3. Map canonical workspace concepts:
   - knowledge note,
   - generated index,
   - task summary,
   - run membership,
   - incident payload cache,
   - activation gate.
4. Record unsupported features as explicit gaps instead of approximating silently.

Acceptance criteria:

- Pi pilot expresses the same workflow semantics as shared skills.
- Pi pilot does not claim runtime activation.

Validation:

- Review against `pi-pilot/ACTIVATION.md`.
- Run `tools/check-sensitive-content .`.

## Workstream F: Future Activation Notes

Activation is separate from this implementation plan. This section is a future checklist only; do not run it while implementing the staged `workspace-control` artifacts.

Steps:

1. Run `tools/check-sensitive-content .`.
2. Run all available helper validations:
   - `tools/knowledgectl lint`,
   - `tools/knowledgectl index --check`,
   - `tools/workspace-status --brief`,
   - `tools/workspace-artifact-inventory`.
3. Review `git diff --stat` and `git diff` in `workspace-control`.
4. Commit `workspace-control`.
5. Stop. A future human-approved activation task must decide whether to sync anything into the live workspace.
6. If a future activation is approved, record that decision in a new ADR before changing live paths.

Acceptance criteria:

- Staged repo changes are reviewable without affecting live runtime.
- Any future live activation has an auditable decision record before live paths change.

## Sequencing

Recommended order:

1. A1 and A2: knowledge docs and `knowledgectl`.
2. B1: tighten durable learning capture against the new knowledge contract.
3. A3: add knowledge health to status after `knowledgectl` exists.
4. B2, B3, B4: research capture and experiment/subagent templates.
5. C1 and C2: incident cache spec and skill wording.
6. E: Pi pilot translation updates.
7. D1-D4: keep as future live-rollout notes only.
8. F: keep as future activation notes only.

## Milestones

### Milestone 1: Knowledge Lookup Is Mechanical

Deliverables:

- `knowledge/README.md`
- `knowledge/TEMPLATE.md`
- `tools/knowledgectl`
- generated `knowledge/INDEX.md`
- generated `knowledge/index.json`

Done when:

- malformed notes fail lint,
- index freshness can be checked,
- an agent can search for an existing learning without reading all notes.

### Milestone 2: Learning Capture Is Enforced At Workflow Boundaries

Deliverables:

- updated `durable-learning-capture`,
- updated `task-closeoff`,
- `research-to-knowledge`,
- experiment/subagent templates.

Done when:

- close-off includes candidate durable learnings or explicit "none",
- external research gets workspace-specific implications,
- delegated task briefs define editable/read-only/output/validation paths.

### Milestone 3: Incident Cache Semantics Are Specified And Reflected In Skills

Deliverables:

- `docs/specs/incident-scope-cache.md`,
- updated `detection-dataset-export`,
- updated Pi workflow drafts.

Done when:

- agents know when to create task cache vs durable fixture,
- the local Postgres question is documented as deferred,
- no unsupported `datasetctl` commands are presented as active.

### Milestone 4: Future Live Cache Tooling Is Specified

Deliverables:

- proposed non-destructive `datasetctl` schema migration design,
- proposed tag/retention/projection behavior,
- proposed `cache status` behavior,
- proposed dry-run-only prune behavior.

Done when:

- workspace-control docs explain the future live rollout clearly,
- no staged skill or doc claims unsupported live commands are available,
- no live dataset files or tools have been changed.

## Risks And Mitigations

| Risk | Mitigation |
|---|---|
| Manual indexes keep drifting | Generate `knowledge/INDEX.md` and use `index --check`. |
| Migrated memory notes become over-trusted | Mark weak provenance and require promotion verification before automation/global rules. |
| Tooling grows too heavy | Start with shell/perl and `rg`; defer SQLite FTS. |
| Agents treat staged repo changes as live | Repeat activation boundary in docs and skills; do not sync without approval. |
| Dataset cache loses reproducibility | Never prune run/query/membership/hash/count/manifests. |
| Payload pruning deletes active-task evidence | First release has status and dry-run only; future prune refuses `busy/` tasks by default. |
| Local Postgres becomes a false source of truth | Defer it; use DuckDB scope/projection/cache layers. |
| Pi pilot drifts from shared skills | Treat Pi workflows as translations and keep canonical semantics in shared skills. |
| Staged implementation accidentally touches live runtime | Keep live rollout notes non-executable in this plan; stop before any sync or `/workspace/tools` change. |

## Initial Task Breakdown

Suggested task names if splitting into active work:

1. `workspace-control-knowledge-tooling`
2. `workspace-control-learning-skills`
3. `workspace-control-incident-cache-spec`
4. `workspace-control-pi-workflow-sync`

All listed tasks are `workspace-control` tasks only. Any future live `datasetctl` or live workspace activation work must be proposed and approved as a separate task.
