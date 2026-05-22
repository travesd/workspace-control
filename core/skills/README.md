# Core Skills

This directory will hold portable shared skills after the split from the
current live-compatible `agent-skills/skills/` tree.

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

Do not move or duplicate skills here until a render/sync path can generate the
current `agent-skills/skills/` tree and validate it.

Several current `SKILL.md` files above still contain `/workspace` paths or
detection-platform-metal assumptions. Those need parameterization or a split
between portable core instructions and workspace-specific references before
they become true core skills.
