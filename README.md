# Workspace Control

This repo version-controls the operating model for the `/workspace` detection-platform-metal sandbox.

It currently has two compatibility tracks:

- `current-workspace/` and `agent-skills/` preserve the current Claude/Codex workspace approach.
- `pi-pilot/` and `.pi/` hold an experimental Pi harness translation layer.

The next source layout is layered:

- `core/` for portable provider-neutral primitives,
- `workspaces/detection-platform-metal/` for the current workspace overlay,
- `providers/` for Claude, Codex, and Pi adapters,
- `current-workspace/` and `agent-skills/` as live-compatible activation
  sources until render/sync tooling can generate them from layered sources.

The source of truth should remain provider-neutral. Claude memory, Codex memory, and Pi configuration may mirror or consume this repo, but should not become separate canonical stores.

This repo is not activated into the live workspace automatically. See `ACTIVATION.md` for the current source-of-truth boundary and sync gates.

For ongoing upkeep after activation, see `MAINTENANCE.md`.

## What Belongs Here

- Workspace instructions and conventions.
- Shared Agent Skills.
- Core skills and workspace overlay skill source maps.
- Durable knowledge notes with provenance and re-verification rules.
- Workspace-control helper scripts in `tools/`.
- Process decisions and ADRs.
- Implementation plans for staged workspace-control changes.
- Task lifecycle state definitions and transition rules.
- Task resumability standards and note templates.
- Templates for task setup, session hygiene, close-off, and cross-agent review.
- Pi pilot agents, workflow drafts, and translation notes.

## What Does Not Belong Here

- Secrets or env files.
- Raw datasets, backups, screenshots, or task artifacts.
- Provider transcripts, provider-local memory exports, or local harness databases.
- Product repo code and worktrees.

## First Slice

This scaffold contains:

- live-compatible current workspace instructions for `/workspace/AGENTS.md` and
  `/workspace/CLAUDE.md`,
- current shared skills from `/workspace/agent-skills/skills/`,
- layered source-layout scaffolding under `core/`, `workspaces/`, and
  `providers/`,
- the 2026-05-20 workspace organization investigation outputs,
- normalized provider-neutral knowledge notes under `knowledge/`,
- a Pi pilot area with draft agents and workflow mapping.

Raw provider-local memory exports are intentionally not tracked. See `SANITIZATION.md`.

## Helper Scripts

- `tools/workspace-status` - short live orientation report for agents.
- `tools/workspace-artifact-inventory` - audit-grade inventory for cleanup/review work.
- `tools/knowledgectl` - lint, index, search, and stale-check provider-neutral knowledge notes.
- `tools/check-sensitive-content` - large-file and redacted secret-pattern check before commits or remotes.

## Current Plans

- `docs/plans/2026-05-20-core-recommendations-implementation.md` - staged implementation plan for knowledge lookup, shared workflow skills, incident cache semantics, and Pi workflow translation.
- `docs/plans/2026-05-21-workflow-improvements-go-live.md` - proposed live rollout and rollback plan for workflow improvements.
- `docs/plans/2026-05-21-task-lifecycle-update.md` - staged plan for task lifecycle states, parked-work handling, and future activation.
- `docs/reference/live-workspace-details.md` - on-demand details moved out of always-loaded workspace instructions.
- `docs/reviews/2026-05-21-thin-instructions-audit.md` - audit of always-loaded instruction size, links, and split recommendations.
- `docs/reviews/2026-05-21-workflow-improvements-final-review.md` - end-to-end review of final repo state against scoped improvements.
- `docs/reviews/2026-05-22-layered-repo-organization-review.md` - review of the layered source-layout scaffold and source-of-truth boundaries.
- `docs/specs/task-lifecycle.md` - proposed definitions for `busy`, `parked`, `later`, `done`, `archived`, and future archive destinations.
- `docs/specs/task-resumability.md` - task-first notes, resume packets, chat-dependency classification, and measurable resumability scoring.
- `docs/specs/repo-organization.md` - proposed layered source model for core, workspace overlays, provider adapters, and live compatibility outputs.
- `docs/plans/2026-05-22-layered-repo-organization.md` - staged plan for moving from the flat compatibility tree to the layered model.
- `MAINTENANCE.md` - ongoing repo upkeep, live sync, skill sync, knowledge sync, and Pi boundary rules.
