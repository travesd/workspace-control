---
title: "virtiofs ENFILE — historical (superseded 2026-04-24)"
description: "Historical pointer — /workspace was virtiofs with an fd-limit ENFILE issue until 2026-04-24, now ext4 block-device. No active rule."
tags: [feedback, memory-migration]
status: active
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

**SUPERSEDED 2026-04-24**: `/workspace` is now a native ext4 block-device mount (`/dev/vdc`). The virtiofs fd-pressure ENFILE issue is resolved at the root.

This file is retained only as historical context. Earlier commits and instructions may reference path workarounds because of this. Do not apply the old workarounds; they are no longer needed. Worktrees, Go caches, and bind mounts behave normally on the current ext4 setup.
