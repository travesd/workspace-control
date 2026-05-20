---
name: agents-md-review
description: Review AGENTS.md and shared skills for stale factual claims, missing verification metadata, and instruction drift.
---

# AGENTS.md Review

Use this skill when a user flags workspace guidance as wrong, before major instruction rewrites, or during periodic workspace hygiene.

## Workflow

1. Identify concrete factual claims in `AGENTS.md` or shared skills that can drift.
2. Verify each claim against live files, tool output, or authoritative docs.
3. Mark unverifiable claims as needing review instead of asserting them.
4. Propose edits that keep always-loaded instructions concise.
5. Move detailed rationale to `knowledge/` or ADRs where appropriate.

## Guardrails

- Do not clutter `AGENTS.md` with excessive metadata.
- Prefer source paths, verification dates, and re-check conditions for facts with known freshness risk.
- Do not change provider-specific files without checking whether the canonical source should change first.
