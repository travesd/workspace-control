---
title: "feedback log investigation incrementally"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_log_investigation_incrementally.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: Log investigations incrementally, not at the end
description: For deep investigations/reviews, update notes.md and a dedicated investigation doc AS you read files — don't let findings live only in conversation context
type: feedback
originSessionId: a9d4383d-0f97-4c25-927b-d1cb1f8fb877
---
When doing a deep investigation or design review that spans many files, log findings to disk incrementally as you read, not just at the end.

**Why:** User called this out on the llm-judge-domain-workflows task (2026-04-10) after I was about to dispatch a big Explore agent and return only a final synthesis. Deep investigations risk having findings evaporate if context compresses, and the user can't see progress or correct the direction early. Notes on disk survive; context doesn't.

**How to apply:**
- Create a dedicated `busy/<task>/investigation-*.md` (or `findings.md`) at the start of any multi-file review
- Update `notes.md` with a running log entry per significant action (file read, surprise found, decision made) — one-liner is fine
- After each chunk of reading, append detailed extracts (file paths, line numbers, verbatim snippets) to the investigation doc
- Prefer direct Read + incremental logging over delegating a big batch to an Explore agent whose internal work doesn't get logged in real time
- Delegation is still fine for enumeration of the long tail — but log the returned findings to the investigation doc immediately
- This applies to design reviews, architecture audits, bug root-causing that spans >3 files, and similar deep dives
