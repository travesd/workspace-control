# Workspace Control

This repo version-controls the operating model for the `/workspace` detection-platform-metal sandbox.

It has two tracks:

- `current-workspace/` and `agent-skills/` preserve the current Claude/Codex workspace approach.
- `pi-pilot/` and `.pi/` hold an experimental Pi harness translation layer.

The source of truth should remain provider-neutral. Claude memory, Codex memory, and Pi configuration may mirror or consume this repo, but should not become separate canonical stores.

## What Belongs Here

- Workspace instructions and conventions.
- Shared Agent Skills.
- Durable knowledge notes with provenance and re-verification rules.
- Process decisions and ADRs.
- Templates for task setup, session hygiene, close-off, and cross-agent review.
- Pi pilot agents, workflow drafts, and translation notes.

## What Does Not Belong Here

- Secrets or env files.
- Raw datasets, backups, screenshots, or task artifacts.
- Provider transcripts or local harness databases.
- Product repo code and worktrees.

## First Slice

This initial scaffold imports:

- current workspace instructions from `/workspace/AGENTS.md` and `/workspace/CLAUDE.md`,
- current shared skills from `/workspace/agent-skills/skills/`,
- the 2026-05-20 workspace organization investigation outputs,
- a raw copy of Claude workspace memory under `knowledge/imported/claude-memory/`,
- a Pi pilot area with draft agents and workflow mapping.

Future work should migrate imported memory into normalized `knowledge/*.md` notes before deleting or deprecating the imported copy.
