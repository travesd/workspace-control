# Core Skills

This directory holds draft render-input copies of portable shared skill
concepts for `tools/renderctl dry-run --mode skills`.

The current live-compatible canonical source remains `agent-skills/skills/`
until explicit activation. Keep these draft copies synchronized with the
compatibility tree; do not treat them as live skill authority yet.

Core skill concepts:

- `agents-md-review`
- `call-a-friend`
- `durable-learning-capture`
- `research-to-knowledge`
- `session-hygiene`
- `skill-maintainer`
- `task-closeoff`
- `workspace-artifact-inventory`
- `workspace-status`

Several current `SKILL.md` files above still contain `/workspace` paths or
detection-platform-metal assumptions. Those need parameterization or a split
between portable core instructions and workspace-specific references before
they become true core skills.

Parameterization started with the near-portable review and knowledge skills:
`agents-md-review`, `durable-learning-capture`, and
`research-to-knowledge`. Portable skills should use a local parameter map for
paths, commands, and activation boundaries instead of embedding workspace
values directly.

Template:
`core/templates/skill-parameter-map.md`

Detection-platform-metal map:
`workspaces/detection-platform-metal/specs/core-skill-parameter-map.md`

Portability audit:
`docs/reviews/2026-05-25-core-skill-portability-audit.md`
