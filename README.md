# Workspace Control

This repo version-controls the operating model for the `/workspace` detection-platform-metal sandbox.

It has two tracks:

- `current-workspace/` and `agent-skills/` preserve the current Claude/Codex workspace approach.
- `pi-pilot/` and `.pi/` hold an experimental Pi harness translation layer.

The source of truth should remain provider-neutral. Claude memory, Codex memory, and Pi configuration may mirror or consume this repo, but should not become separate canonical stores.

This repo is not activated into the live workspace automatically. See `ACTIVATION.md` for the current source-of-truth boundary and sync gates.

## What Belongs Here

- Workspace instructions and conventions.
- Shared Agent Skills.
- Durable knowledge notes with provenance and re-verification rules.
- Workspace-control helper scripts in `tools/`.
- Process decisions and ADRs.
- Implementation plans for staged workspace-control changes.
- Task lifecycle state definitions and transition rules.
- Templates for task setup, session hygiene, close-off, and cross-agent review.
- Pi pilot agents, workflow drafts, and translation notes.

## What Does Not Belong Here

- Secrets or env files.
- Raw datasets, backups, screenshots, or task artifacts.
- Provider transcripts, provider-local memory exports, or local harness databases.
- Product repo code and worktrees.

## First Slice

This scaffold contains:

- current workspace instructions from `/workspace/AGENTS.md` and `/workspace/CLAUDE.md`,
- current shared skills from `/workspace/agent-skills/skills/`,
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
- `docs/plans/2026-05-21-task-lifecycle-update.md` - staged plan for task lifecycle states, parked-work handling, and future activation.
- `docs/specs/task-lifecycle.md` - proposed definitions for `busy`, `parked`, `later`, `done`, `archived`, and future archive destinations.
