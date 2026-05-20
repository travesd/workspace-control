# AGENTS.md - Workspace Control Repo

This repo is for workspace operating-model documentation and harness configuration. It is not the detection-platform-metal product repo.

## Rules

- Do not copy secrets, env files, credentials, provider transcripts, raw datasets, backups, or product worktrees into this repo.
- Keep canonical shared knowledge provider-neutral. Claude, Codex, and Pi may consume or mirror these files, but provider-local memory is not authoritative.
- When changing shared skills, edit canonical skill files here first, then sync to the workspace mirrors through the workspace skill tooling after explicit approval.
- Pi configuration under `.pi/` is experimental. It must preserve the same guardrails as `/workspace/AGENTS.md`: Docker-only repo execution, no auto-push, local-stack validation, and read-only production access only when explicitly authorized.
- Use ADRs in `docs/decisions/` for durable process decisions.
- Keep `knowledge/` notes short, sourced, tagged, and dated. Include when to re-verify facts that can drift.

## Validation

Before committing:

```bash
git status --short
find . -type f -size +1M -print
rg -n "(BEGIN .*PRIVATE|api[_-]?key|secret|token|password|credential)" .
```

False positives are expected for documentation that discusses secrets. Do not commit real secret values.
