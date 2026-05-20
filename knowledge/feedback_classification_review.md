---
title: "Classification review learnings"
description: "Procedural rules for /review-classification — what to check, what to exclude, push conventions"
tags: [feedback, memory-migration]
status: active
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

Don't assume AI-flagged incidents should all be pushed. On first test, 47% of "AI-flagged but not submitted" cases were correctly held back by the LLM gatekeeper — legitimate businesses with coincidental brand names (Polish budgeting app "PlanB", delivery app "Keeta", hiking gear "Tether").

**Why:** The LLM gatekeeper is intentionally conservative. Brand-name collisions are real and common. The skill should surface evidence for the user to decide, not recommend overriding the LLM.

**How to apply:**
- When reviewing submit candidates, always check if the page content actually targets the protected brand vs just sharing a name.
- Exclude Cloudflare 403/challenge pages from takedown evidence — no content to support a takedown.
- Detection-only clients reject gatekeeper pushes — check client eligibility first.
- Source tag for classification review pushes: `api-autohunt-cc`.
- Push reasoning should describe the infringement evidence (credential form, wallet connect, investment scam), not pipeline metadata.
- Brand keyword min 4 chars — 3-char keywords like `1in`, `usd` cause too many false matches.
- Always verify safe_subjects are actual client domains before pushing.
- Always dedup incidents — BQ returns duplicates when processed through multiple autohunt strategies.
- **Two-step push for TR-enabled clients**: after gatekeeper push (`/api/v1/incidents/gatekeeper`), call TR publish (`/api/v1/admin/tr-publishing/retry/{id}`). Direct API push bypasses the rule engine so TR doesn't fire automatically. Query `/api/v1/admin/tr-publishing` for current TR client list and filter config (`judgementFilter`, `gatekeeperOutcomeFilter`) — don't rely on a memorised client roster.
