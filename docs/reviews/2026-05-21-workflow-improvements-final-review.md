# Workflow Improvements Final Review

Date: 2026-05-21

Status: repo-ready, not activated live

## Scope

This review checks the final `workspace-control` state against the workspace
organization learnings, Karpathy thin-instructions follow-up, implementation
plans, and go-live/rollback requirements.

No live `/workspace` activation was performed by this review.

## Executive Assessment

The repo is ready for a reviewed activation task. The always-loaded instruction
surface is now thin, detailed procedures are linked, workflow improvements are
captured as provider-neutral skills/tools/docs, and every live rollout slice has
a rollback path.

Do not skip the activation task. Live promotion still needs a rollback snapshot,
skill sync, optional empty `parked/` creation, and a dry-run movement table
before any task directories move.

## Evidence Snapshot

Line counts:

| Surface | Lines | Assessment |
|---|---:|---|
| `AGENTS.md` | 24 | Thin repo contract. |
| `current-workspace/CLAUDE.md` | 7 | Thin provider-specific import. |
| `current-workspace/AGENTS.md` | 175 | Thin live activation candidate. |
| `docs/reference/live-workspace-details.md` | 270 | On-demand reference, acceptable. |
| `agent-skills/skills/classifier-corpus-coverage/SKILL.md` | 220 | Still long; defer split until next touch. |

Validation run:

```text
tools/knowledgectl lint
tools/knowledgectl index --check
tools/workspace-status --brief
tools/workspace-artifact-inventory
```

Observed:

- knowledge index is fresh,
- `workspace-status --brief` is 134 lines,
- latest task counts observed during review: `busy 28`, `parked 0`,
  `planned 3`, `later 1`, `done 10`,
  `archived 2`, `investigations 11`,
- knowledge lint has warnings but no errors; warnings are legacy seed-note
  metadata/provenance warnings.

## Planned Improvements Review

### Provider-Neutral Knowledge

Status: implemented in repo.

Evidence:

- `knowledge/README.md`
- `knowledge/TEMPLATE.md`
- `knowledge/INDEX.md`
- `knowledge/index.json`
- `tools/knowledgectl`

Assessment:

- The lookup flow matches the scoped learning: search generated index first,
  open only relevant notes, and verify linked evidence before relying on
  stale-prone claims.
- The warnings for 28 legacy seed notes are expected. They correctly prevent
  weak memory-migration notes from silently becoming stronger authority.

Remaining:

- Backfill `type` and `scope` on migrated seed notes over time.
- Re-verify high-impact legacy notes before promoting them into `AGENTS.md`,
  automation, or skills.

### Thin Instructions

Status: implemented in repo.

Evidence:

- `current-workspace/AGENTS.md`
- `docs/reference/live-workspace-details.md`
- `docs/reviews/2026-05-21-thin-instructions-audit.md`

Assessment:

- The always-loaded candidate now carries durable guardrails, path map, tool
  routing, lifecycle one-liners, and links.
- Long procedure details moved to the reference doc, tool READMEs, specs, and
  skills.
- This follows the Karpathy pattern: compact operating context, scoped
  procedures, and narrow references loaded only when needed.

Remaining:

- Keep the thin-instructions gate in the live activation task.
- Avoid re-expanding `AGENTS.md` when future procedures are added.

### Shared Skills And Templates

Status: implemented in repo, activation pending.

Evidence:

- `agent-skills/skills/durable-learning-capture/SKILL.md`
- `agent-skills/skills/session-hygiene/SKILL.md`
- `agent-skills/skills/task-closeoff/SKILL.md`
- `agent-skills/skills/workspace-status/SKILL.md`
- `agent-skills/skills/workspace-artifact-inventory/SKILL.md`
- `agent-skills/skills/research-to-knowledge/SKILL.md`
- `agent-skills/skills/agents-md-review/SKILL.md`
- `docs/templates/experiment-log.md`
- `docs/templates/subagent-brief.md`
- `docs/templates/task-lifecycle-block.md`

Assessment:

- The core workflow boundaries from the investigation are covered: learning
  capture, session hygiene, close-off, status, inventory, research capture,
  and instruction review.
- Skills are mostly concise and provider-neutral.

Remaining:

- Sync to live canonical skills only during approved activation.
- Later split `classifier-corpus-coverage` into a short skill plus references.

### Workspace Status And Artifact Inventory

Status: implemented in repo.

Evidence:

- `tools/workspace-status`
- `tools/workspace-artifact-inventory`

Assessment:

- `workspace-status --brief` stays under the 200-line target.
- Status includes knowledge health and lifecycle counts.
- Inventory separates audit-grade output from session-start orientation.
- Planned file-based specs are counted correctly.

Remaining:

- During activation, decide whether to call tools from repo path or add
  wrappers under `/workspace/tools/workspace-control/`.

### Task Lifecycle States

Status: implemented in repo, live movement pending.

Evidence:

- `docs/specs/task-lifecycle.md`
- `docs/templates/task-lifecycle-block.md`
- `current-workspace/AGENTS.md`
- `agent-skills/skills/task-closeoff/SKILL.md`
- `docs/plans/2026-05-21-task-lifecycle-update.md`

Assessment:

- `parked/` is clearly distinct from `later/` and `archived/`.
- The top-level archive concern is resolved by positive routing:
  current task lifecycle state uses `/workspace/detection-platform-metal-work/`.
- Lifecycle details live outside the always-loaded instruction file.

Remaining:

- Live activation must create `parked/`.
- A movement table is required before moving any task directories.
- `ACTIVE.md` and existing live task notes may still contain old wording until
  the activation/audit task updates them deliberately.

### Incident Scope Cache

Status: specified, not implemented live.

Evidence:

- `docs/specs/incident-scope-cache.md`
- `agent-skills/skills/detection-dataset-export/SKILL.md`

Assessment:

- The scoped recommendation is captured: use durable query/membership metadata
  and treat payloads as cache unless retained as fixtures/backups.
- The spec correctly avoids adding local Postgres now and avoids destructive
  pruning.

Remaining:

- Future `datasetctl` schema/CLI changes need a separate live implementation
  plan and dry-run migration.

### Pi Pilot Translation

Status: drafted, intentionally dark.

Evidence:

- `.pi/`
- `pi-pilot/`
- `pi-pilot/ACTIVATION.md`
- `pi-pilot/translation-map.md`

Assessment:

- Pi remains a translation/pilot surface, not a live coordinator.
- The go-live plan keeps Pi disabled until a package/schema/runtime is selected
  and validated.

Remaining:

- Separate Pi decision before any runnable harness activation.

### Go-Live And Revert

Status: implemented as plan, not executed.

Evidence:

- `docs/plans/2026-05-21-workflow-improvements-go-live.md`

Assessment:

- Rollout is slice-based and reversible:
  read-only helpers, skills, thin instructions, lifecycle directory, then task
  movement only after approval.
- Rollback covers instructions, skills/provider mirrors, task moves, and
  workspace-control source commits.

Remaining:

- Create the live activation task and rollback snapshot before touching live
  files.

## Risks

- Legacy knowledge notes still carry weak migration provenance. This is visible
  and non-blocking, but high-impact notes need re-verification before promotion.
- The live workspace has not been activated yet. Agents in current sessions
  still follow live `/workspace/AGENTS.md`, not the staged thin candidate.
- The large `classifier-corpus-coverage` skill could still impose context cost
  when invoked. It is on-demand and not part of the first activation slice, so
  this is not a blocker.
- Live task movement is inherently risky around dirty worktrees and active
  sessions. The movement table and explicit approval gate are mandatory.

## Ready Criteria

The repo-side work is ready when these pass:

```bash
git status --short
git diff --check
tools/check-sensitive-content /workspace/workspace-control
tools/knowledgectl lint
tools/knowledgectl index --check
bash -n tools/workspace-status tools/workspace-artifact-inventory tools/knowledgectl tools/check-sensitive-content
```

Live activation is ready only after:

1. the activation task exists,
2. rollback snapshot is captured,
3. `skillctl validate` passes before and after skill sync,
4. thin `AGENTS.md` is reviewed,
5. no task directories move without an approved movement table.

## Final Recommendation

Proceed to a live activation task when desired, but activate in the conservative
order from the go-live plan. The first live slice should stop after the dry-run
task movement table; actual task moves should be a separate approval.
