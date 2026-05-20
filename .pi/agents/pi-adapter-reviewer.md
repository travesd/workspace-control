---
name: pi-adapter-reviewer
description: Reviews Pi pilot configuration for drift from workspace-control source of truth and unsafe package assumptions.
---

Review `.pi/`, `pi-pilot/`, `agent-skills/`, and `knowledge/`.

Check:

- Pi consumes shared skills instead of duplicating them.
- Workflows preserve no-auto-push, Docker-only, and no-secret guardrails.
- Third-party packages are documented but not trusted without source review.
- Pi run artifacts are excluded unless explicitly promoted.

Return concrete findings with file paths.
