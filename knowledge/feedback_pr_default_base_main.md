---
title: "PRs target main in detection-platform-metal"
description: "In phishfort/detection-platform-metal the default base for PRs is `main`. Pass `--base main` explicitly to avoid legacy defaults leaking in from gh config or past sessions."
type: feedback
tags: [feedback, memory-migration]
status: active
scope: repo
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

When opening a PR in `phishfort/detection-platform-metal`, target `main`. Pass `--base main` explicitly to `gh pr create`.

**Why:** The old detection-platform repo used `develop` as its working branch (develop → staging → main promote workflow). Metal has no staging/promote layer — `main` is the integration branch. Old muscle memory or leftover gh config from detection-platform can cause PRs to open against the wrong base.

**How to apply:**
- Always `--base main` for detection-platform-metal PRs
- The old "don't open against main" guidance from detection-platform does NOT apply here — it's the correct target now
- If you're porting a detection-platform PR into metal, the source branch's base was `develop`; the new metal PR's base is `main`
