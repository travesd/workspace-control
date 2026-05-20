# Pi Project Drafts

This `.pi/` directory is a draft project-local Pi configuration area. It is not an activated Pi harness.

It is intentionally minimal:

- `agents/` contains role prompts that mirror the Claude/Codex review pattern.
- `workflows/` contains example workflow JSON that can be adapted after a Pi package/schema is selected.
- `skills/` is reserved for Pi-specific skill mirrors if we decide not to load `agent-skills/skills/` directly.

No Pi package is installed or declared by default. Do not install or vendor third-party Pi packages here without review, pinning, and an ADR.

Before activation, follow `../pi-pilot/ACTIVATION.md`.
