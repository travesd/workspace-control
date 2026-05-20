# Pi Workflow Mapping

The Pi pilot maps workspace-control workflows into project-local Pi agents and workflow JSON. These files are draft specifications, not runnable activation state.

## Source Of Truth

- Shared skills: `agent-skills/skills/`
- Pi settings: `.pi/settings.json`
- Pi agents: `.pi/agents/*.md`
- Pi workflows: `.pi/workflows/*.json`
- Knowledge: `knowledge/`

Pi should consume these files after activation. It should not create a separate canonical memory layer.

## Workflows

| File | Purpose |
|---|---|
| `.pi/workflows/workspace-cross-review.json` | Parallel scout/reviewer review followed by synthesis. |
| `.pi/workflows/durable-learning-capture.json` | Curate, review, and synthesize a reusable learning. |
| `.pi/workflows/session-hygiene.json` | Inspect session drift and review safe remediation. |
| `.pi/workflows/task-closeoff.json` | Build and review a safe task close-off plan. |
| `.pi/workflows/pi-adapter-review.json` | Review Pi config for drift and unsafe assumptions. |
| `.pi/workflows/research-to-knowledge.json` | Convert external research into workspace-specific learnings or no-action decisions. |

## Package Position

Do not install Pi packages by default. Current package candidates are:

- `pi-agents` for project-local agents and workflow graphs.
- `pi-subagents` for conversational and background delegation.
- `ultimate-pi` as a lifecycle-pattern reference.

Before installing any package, review its source, record an ADR, and update `ACTIVATION.md`.
