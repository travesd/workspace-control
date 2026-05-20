---
title: "feedback proposals not implementation"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_proposals_not_implementation.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: Proposals are not implementation tasks
description: When asked to plan/propose something, save the document — do NOT enter implementation mode or try to implement it
type: feedback
---

When the user asks to "plan a proposal" or "propose an alternative", they want a document to share with someone else — NOT an implementation plan to execute.

**Why:** The user works with a team and needs to present proposals for discussion. Entering plan mode (which gates implementation) is the wrong tool — it implies we're about to write code.

**How to apply:** Save proposals as work artifacts in `busy/<task>/`. Never enter plan mode for proposal/design work. Only enter plan mode when the user explicitly wants to implement something.
