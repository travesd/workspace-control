# Translation Map: Current Workspace To Pi Pilot

## Current Source Of Truth

| Current Artifact | Purpose | Pi Pilot Mapping |
|---|---|---|
| `/workspace/AGENTS.md` | Always-loaded workspace rules | Root `AGENTS.md`; Pi must preserve these guardrails |
| `/workspace/agent-skills/skills/` | Shared reusable workflows | `agent-skills/skills/`; optionally exposed through `.pi/skills/` or Pi settings |
| `/workspace/detection-platform-metal-work/*` | Task lifecycle and artifacts | Pi workflows should write plans/reviews back to task dirs, not only Pi run dirs |
| Claude-local workspace memory store | Claude-local learnings | Migrated into provider-neutral `knowledge/` |
| `/workspace/tools/agents/sessionctl` | Session tracking | Future `session-hygiene` workflow/tool wrapper |
| `/workspace/workspace-control/tools/workspace-status` | Live orientation report | Pi prompt/skill entry point for session start |
| `/workspace/workspace-control/tools/workspace-artifact-inventory` | Audit-grade inventory | Pi workflow evidence source |

## Proposed Pi Agents

| Agent | Role |
|---|---|
| `workspace-scout` | Read current state and produce a short orientation report |
| `workspace-reviewer` | Review a proposed process or scaffold against workspace rules |
| `workspace-synthesizer` | Merge provider or subagent findings into final recommendations |
| `knowledge-curator` | Normalize learnings into provider-neutral knowledge notes |
| `session-steward` | Inspect and repair recoverability metadata |
| `task-closer` | Build safe task close-off plans |
| `pi-adapter-reviewer` | Review Pi configuration for drift and package risk |

## Proposed Pi Workflows

| Workflow | Shape |
|---|---|
| workspace cross-review | fork scout/reviewer branches, join, synthesize |
| task close-off | sequence status, close-off checklist, inventory, summary |
| durable learning capture | classify learning, write knowledge note, propose skill/AGENTS updates |

## Open Questions

- Whether Pi should consume `agent-skills/skills/` directly or through generated `.pi/skills/` mirrors.
- Whether Pi run artifacts should remain local-only or selected outputs should be promoted to task dirs.
- Whether the `ultimate-pi` package is useful as inspiration only, or should be installed after source review.
