# Core Layer

This directory is reserved for provider-neutral, workspace-neutral operating
primitives.

Core content should be reusable outside the detection-platform-metal workspace.
It may describe agent collaboration, task notes, resumability, durable learning,
or review conventions, but it should not depend on `/workspace` paths,
detection services, Cloudflare Access, production DB details, or provider-local
memory.

Current status: scaffolding only. Canonical files still live in existing
compatibility locations such as `agent-skills/skills/`, `docs/specs/`, and
`current-workspace/`.

Before moving files here, follow
`docs/specs/repo-organization.md`.

