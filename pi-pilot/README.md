# Pi Pilot

This directory tracks the possible Pi harness approach beside the current Claude/Codex workflow.

Pi is currently treated as an experimental adapter layer. It should read from:

- root `AGENTS.md`,
- `knowledge/`,
- `agent-skills/`,
- `.pi/agents/` and `.pi/workflows/` drafts.

It should not become the canonical store for workspace rules or durable learnings.

## Useful Pi Capabilities To Evaluate

- Project-local skills via `.pi/skills/` and `.agents/skills/`.
- Project-local agents via `.pi/agents/*.md`.
- Workflow graphs with `spawn`, `sequence`, `fork`, `join`, and `loop`.
- Persisted flows for auditability.
- Harness-style plan/evaluate/review artifacts.

## Guardrails

- Review Pi packages before installing them.
- Do not let Pi workflows bypass Docker-only execution rules for product repos.
- Do not allow Pi to auto-push or auto-merge.
- Keep `.pi/harness/runs/` out of git unless a specific run artifact is intentionally promoted.
