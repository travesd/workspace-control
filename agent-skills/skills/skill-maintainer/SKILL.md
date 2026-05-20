---
name: skill-maintainer
description: Create, audit, validate, and synchronize shared Agent Skills so Claude and Codex can use the same canonical workflow instructions.
---

# Skill Maintainer

Use this skill when adding or updating shared Claude/Codex skills.

## Canonical Layout

In this repo:

```text
agent-skills/skills/<skill-name>/SKILL.md
agent-skills/skills/<skill-name>/agents/openai.yaml
```

Live workspace after approved activation:

```text
/workspace/agent-skills/skills/<skill-name>/SKILL.md
/workspace/agent-skills/skills/<skill-name>/agents/openai.yaml
```

Generated mirrors:

```text
/workspace/.claude/skills/<skill-name>/
/workspace/.agents/skills/<skill-name>/
```

## Rules

- Edit the workspace-control skill first. After explicit approval, sync it to `/workspace/agent-skills/skills/`, then run `skillctl validate` and `skillctl sync`.
- Keep shared `SKILL.md` frontmatter portable: `name` and `description` only.
- Use lowercase kebab-case names, and make the folder match the skill name.
- Keep `SKILL.md` concise. Move long details into `references/` and load them only when needed.
- Do not put README, install guides, or changelogs inside individual skill folders.
- Do not require provider-only tools in shared skills. Put provider notes in `agents/openai.yaml`, `provider/claude.md`, or `provider/codex.md` only when needed.
- Do not port existing `.claude/skills` wholesale. Audit for stale DB access, hardcoded secrets, provider-only commands, and current workspace rules first.

## Commands

```bash
/workspace/tools/skills/skillctl inventory
/workspace/tools/skills/skillctl validate
/workspace/tools/skills/skillctl sync
```
