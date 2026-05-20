# Skill Tooling

Source: `/workspace/tools/skills/skillctl`

`skillctl` manages shared Agent Skills in this workspace.

## Expected Layout

```text
/workspace/agent-skills/skills/<skill-name>/SKILL.md
/workspace/.claude/skills/<skill-name>/
/workspace/.agents/skills/<skill-name>/
```

The canonical source is `/workspace/agent-skills/skills/`. Provider mirrors are generated.

## Common Commands

```bash
/workspace/tools/skills/skillctl inventory
/workspace/tools/skills/skillctl validate
/workspace/tools/skills/skillctl sync
```

## Rules

- Keep shared `SKILL.md` frontmatter portable: `name` and `description`.
- Do not require provider-only tools in canonical skills.
- Put provider-specific metadata beside the canonical skill, such as `agents/openai.yaml` or provider notes.
- Validate before syncing mirrors.
