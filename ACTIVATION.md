# Activation Boundary

`/workspace/workspace-control` is the reviewable source for proposed workspace operating-model changes. The live sandbox still runs from `/workspace` until a change is explicitly activated.

## Current Authority

| Area | Edit Here | Live Runtime | Activation Gate |
|---|---|---|---|
| Workspace rules | `AGENTS.md`, `current-workspace/AGENTS.md` | `/workspace/AGENTS.md` | Human review, then copy/sync intentionally. |
| Shared skills | `agent-skills/skills/` | `/workspace/agent-skills/skills/` plus provider mirrors | Approval, then sync to live canonical skills and run `skillctl validate && skillctl sync`. |
| Durable knowledge | `knowledge/` | This repo after agents are pointed at it | Sanitized notes only; no raw provider memory exports. |
| Helper scripts | `tools/` | Optional; live tools remain `/workspace/tools/` | Review, then copy or install deliberately. |
| Pi pilot | `.pi/`, `pi-pilot/` | Not active | Follow `pi-pilot/ACTIVATION.md`. |

## Activation Rules

- Do not push this repo to a remote until `SANITIZATION.md` is current and `tools/check-sensitive-content .` passes.
- Do not sync skill changes into live mirrors without explicit approval.
- Do not treat `.pi/workflows/*.json` as runnable until the package/schema has been selected and validated.
- Preserve live workspace guardrails: Docker-only product repo execution, no auto-push, local-stack validation, and read-only production access only when explicitly authorized.

## Suggested Sync Sequence

1. Run `tools/check-sensitive-content .`.
2. Run `tools/knowledgectl lint` and `tools/knowledgectl index` when knowledge notes changed.
3. Review `git diff --stat` and `git diff`.
4. Commit in `workspace-control`.
5. If activating skills, sync reviewed files into `/workspace/agent-skills/skills/`.
6. Run `/workspace/tools/skills/skillctl validate`.
7. Run `/workspace/tools/skills/skillctl sync`.
8. Record the activation in `docs/decisions/`.

See `MAINTENANCE.md` for the recurring upkeep workflow after activation.
