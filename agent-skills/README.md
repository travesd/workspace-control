# Shared Agent Skills

This directory is the workspace-control copy of shared skills. While this repo is being prepared, edit proposed canonical skill content here first. The live workspace still consumes `/workspace/agent-skills/skills/` until an activation/sync step is explicitly approved.

These skills are intended to be portable between Claude and Codex. Pi can also consume Agent Skills from project paths, but the Pi pilot should not silently diverge from these canonical skills.

## Added By Workspace Organization Review

- `durable-learning-capture`
- `session-hygiene`
- `task-closeoff`
- `workspace-status`
- `workspace-artifact-inventory`
- `agents-md-review`

Before changing skills:

1. Edit skill content here.
2. Review the change in this repo.
3. After approval, sync to `/workspace/agent-skills/skills/`.
4. Run `/workspace/tools/skills/skillctl validate` and `/workspace/tools/skills/skillctl sync` from the live workspace.
