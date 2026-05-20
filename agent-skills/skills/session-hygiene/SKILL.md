---
name: session-hygiene
description: Keep Claude/Codex task sessions recoverable by aligning resume.md files, SESSIONS.md, tmux panes, transcripts, and next-step records.
---

# Session Hygiene

Use this skill when starting, pausing, handing off, or recovering an agent task, or when asked "where are we?" for active workspace sessions.

## Workflow

1. Read `/workspace/detection-platform-metal-work/ACTIVE.md`.
2. Run `/workspace/tools/agents/sessionctl index` or `reconcile` as appropriate.
3. Inspect the relevant task `resume.md`.
4. Ensure any session that owns or materially advances a `busy/<task>/` directory has a standard session row.
5. Record provider, role, session ID, resume command, tmux/window, status, transcript path, and notes.
6. Update the task's `Next Step` before pausing or handing off.

## Provider Notes

- Claude can be launched with a preassigned session ID via `sessionctl launch-claude`.
- Codex session IDs may need discovery through a tracking token via `sessionctl launch-codex` or `codex-id-for-token`.

## Guardrails

- Do not edit `SESSIONS.md` directly; regenerate it.
- Do not close, archive, or remove active task dirs or worktrees unless explicitly asked.
- Do not inspect provider transcripts for content unless recovery requires it.
