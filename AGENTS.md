# AGENTS.md - Workspace Control Repo

This repo is for workspace operating-model documentation and harness configuration. It is not the detection-platform-metal product repo.

## Rules

- Do not copy secrets, env files, credentials, provider transcripts, raw datasets, backups, or product worktrees into this repo.
- Keep canonical shared knowledge provider-neutral. Claude, Codex, and Pi may consume or mirror these files, but provider-local memory is not authoritative.
- For workspace operating-model changes, edit and review this repo first,
  commit and push after approval, then activate into live `/workspace` only
  with explicit approval and rollback notes.
- Use `MAINTENANCE.md` for recurring upkeep, live-sync, skill-sync, and knowledge-sync workflow.
- When changing shared skills, edit `agent-skills/skills/` here first, then sync to the live workspace mirrors through the workspace skill tooling after explicit approval.
- Pi configuration under `.pi/` is draft-only unless `pi-pilot/ACTIVATION.md` says otherwise. It must preserve the same guardrails as `/workspace/AGENTS.md`: Docker-only repo execution, no auto-push, local-stack validation, and read-only production access only when explicitly authorized.
- Use ADRs in `docs/decisions/` for durable process decisions.
- Use `docs/specs/task-resumability.md` for task note, handoff, and recovery
  standards; keep only pointers in always-loaded workspace instructions.
- Keep `knowledge/` limited to workspace operating-model and agent workflow
  learnings. Product, release, incident, or task-specific facts belong in their
  task summary, product docs, dataset manifests, or the product repo unless
  they change how agents operate the workspace.

## Validation

Before committing:

```bash
git status --short
tools/check-sensitive-content .
```

The sensitivity checker redacts values and exits non-zero for high-confidence findings. Do not commit real secret values.
