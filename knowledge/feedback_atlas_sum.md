---
title: "feedback atlas sum"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_atlas_sum.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: atlas.sum is auto-regenerated — don't flag it
description: atlas.sum is regenerated during Docker image build; stale atlas.sum in git doesn't break migrations
type: feedback
---

**Never flag atlas.sum as a blocker or action item when adding migrations.**

The atlas-migrate-hook Dockerfile runs `atlas migrate hash --dir file:///migrations` which regenerates atlas.sum from the actual .sql files during every image build. No CI step validates it, the application doesn't check it, and `atlas migrate apply` at deployment uses the regenerated version inside the container.

**Why:** Investigation on 2026-04-07 confirmed: atlas.sum is hygiene only, not a migration blocker. The Docker build always fixes it. Flagging it creates false urgency and annoys the user.

**How to apply:** When adding migration .sql files, just create the .sql file. Don't touch atlas.sum, don't mention it needs updating, don't add caveats about CI handling it. It's a non-issue.
