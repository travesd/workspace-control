---
title: "feedback virtiofs enfile workaround"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_virtiofs_enfile_workaround.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: virtiofs ENFILE — historical (superseded 2026-04-24)
description: Historical pointer — /workspace was virtiofs with an fd-limit ENFILE issue until 2026-04-24, now ext4 block-device. No active rule.
type: feedback
originSessionId: b822048f-5ea0-4685-be40-ed454892fc03
---
**SUPERSEDED 2026-04-24**: `/workspace` is now a native ext4 block-device mount (`/dev/vdc`). The virtiofs fd-pressure ENFILE issue is resolved at the root.

This file is retained only as historical context — earlier commits and CLAUDE.md language reference ext4 symlinks / `/home/user/...` paths because of this. Don't apply any of the old workarounds; they're no longer needed. Worktrees, Go caches, and bind mounts behave normally on the current ext4 setup.
