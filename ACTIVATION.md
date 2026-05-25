# Activation Boundary

`/workspace/workspace-control` is the reviewable source for proposed workspace operating-model changes. The live sandbox still runs from `/workspace` until a change is explicitly activated.

## Current Authority

| Area | Edit Here | Live Runtime | Activation Gate |
|---|---|---|---|
| Workspace-control repo rules | `AGENTS.md` | This repo only | Keep thin; do not copy to live `/workspace`. |
| Live workspace rules | `current-workspace/AGENTS.md` | `/workspace/AGENTS.md` | Human review, then copy/sync intentionally. |
| Shared skills | `agent-skills/skills/` | `/workspace/agent-skills/skills/` plus provider mirrors | Approval, then sync to live canonical skills and run `skillctl validate && skillctl sync`. |
| Durable knowledge | `knowledge/` | This repo after agents are pointed at it | Sanitized notes only; no raw provider memory exports. |
| Helper scripts | `tools/` | Optional; live tools remain `/workspace/tools/` | Review, then copy or install deliberately. |
| Layered source maps | `core/`, `workspaces/`, `providers/` | None until render/sync tooling is approved | Approve render/sync tooling and a clean dry-run diff before activation. |
| Pi pilot | `.pi/`, `pi-pilot/` | Not active | Follow `pi-pilot/ACTIVATION.md`. |

## Activation Rules

- Do not push this repo to a remote until `SANITIZATION.md` is current and `tools/check-sensitive-content .` passes.
- Do not sync skill changes into live mirrors without explicit approval.
- Do not treat `.pi/workflows/*.json` as runnable until the package/schema has been selected and validated.
- Do not activate layered `core/`, `workspaces/`, or `providers/` outputs until
  generated files diff cleanly against the current live-compatible sources.
- Preserve live workspace guardrails: Docker-only product repo execution, no auto-push, local-stack validation, and read-only production access only when explicitly authorized.

## Suggested Sync Sequence

1. Run `tools/check-sensitive-content .`.
2. Run `tools/renderctl dry-run`.
3. Run `tools/knowledgectl lint` and `tools/knowledgectl index` when knowledge notes changed.
4. Review `git diff --stat` and `git diff`.
5. Commit in `workspace-control`.
6. Run `git show --check --oneline HEAD` and, before pushing, `git diff --check origin/main..HEAD`.
7. Run `tools/renderctl dry-run --mode live-check` to identify the exact live
   delta. A nonzero result is expected when reviewed repo changes are not yet
   live.
8. If activating skills, sync reviewed files into `/workspace/agent-skills/skills/`.
9. Run `/workspace/tools/skills/skillctl validate`.
10. Run `/workspace/tools/skills/skillctl sync`.
11. Run `tools/renderctl dry-run --mode live-check` again to verify post-sync
    drift.
12. Record the activation in `docs/decisions/`.

See `MAINTENANCE.md` for the recurring upkeep workflow after activation.
