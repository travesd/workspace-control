# Detection Platform Metal Core Skill Parameter Map

This map supplies detection-platform-metal values for portable core skills.
It is a repo reference only until layered activation is explicitly approved.

## Instructions

- Always-loaded instruction contract:
  `/workspace/AGENTS.md`; repo source
  `/workspace/workspace-control/current-workspace/AGENTS.md`.
- Claude wrapper:
  `/workspace/CLAUDE.md`; repo source
  `/workspace/workspace-control/current-workspace/CLAUDE.md`.
- Workspace-control repo instructions:
  `/workspace/workspace-control/AGENTS.md`.
- Product repo instructions:
  `/workspace/detection-platform-metal/CLAUDE.md` and repo-local guidance
  under `/workspace/detection-platform-metal/`.

## Durable Homes

- Task records:
  `/workspace/detection-platform-metal-work/{busy,parked,later,done,archived,planned,investigations}/`.
- Task resume packet:
  task-local `resume.md`.
- Task notes and closeout:
  task-local `notes.md` and `SUMMARY.md`.
- Session index:
  `/workspace/detection-platform-metal-work/SESSIONS.md`.
- Knowledge notes:
  `/workspace/workspace-control/knowledge/`.
- Decision records:
  `/workspace/workspace-control/docs/decisions/`.
- Shared skills source in this repo:
  `/workspace/workspace-control/agent-skills/skills/`.
- Live canonical shared skills:
  `/workspace/agent-skills/skills/`.
- Provider skill mirrors:
  `/workspace/.claude/skills/` and `/workspace/.agents/skills/`.
- Data products and manifests:
  `/workspace/datasets/`.
- Platform backups:
  `/workspace/backups/`.

## Validation Commands

- Knowledge search/lint/index:
  `./tools/knowledgectl search <term>`,
  `./tools/knowledgectl lint`,
  `./tools/knowledgectl index`.
- Skill validation:
  `SKILLCTL_CANONICAL_DIR=/workspace/workspace-control/agent-skills/skills /workspace/tools/skills/skillctl validate`.
- Generated skill validation:
  `SKILLCTL_CANONICAL_DIR=<generated-root>/agent-skills/skills /workspace/tools/skills/skillctl validate`.
- Render checks:
  `./tools/renderctl dry-run`,
  `./tools/renderctl dry-run --mode live-check`.
- Session index:
  `/workspace/tools/agents/sessionctl index`.

## Activation Boundaries

- Draft operating-model changes in `/workspace/workspace-control`.
- Push only after explicit approval.
- Activate into `/workspace` only after separate explicit approval.
- Do not activate Pi unless the user starts the Pi migration path.
- Preserve rollback evidence under the task's rollback directory before live
  activation.
