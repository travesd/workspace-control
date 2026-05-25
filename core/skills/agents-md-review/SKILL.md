---
name: agents-md-review
description: Review always-loaded agent instructions and shared skills for stale factual claims, missing verification metadata, and instruction drift.
---

# Agent Instruction Review

Use this skill when a user flags agent guidance as wrong, before major
instruction rewrites, or during periodic workspace hygiene.

## Workflow

1. Identify the local instruction contract, provider wrappers, shared skills,
   knowledge-note homes, and decision-record paths from the local parameter map
   or workspace instructions.
2. Identify concrete factual claims in always-loaded instructions or shared
   skills that can drift.
3. Verify each claim against live files, tool output, authoritative docs, or
   dated task evidence.
4. Mark unverifiable claims as needing review instead of asserting them.
5. Propose edits that keep always-loaded instructions concise.
6. Move detailed rationale to the narrowest local knowledge home, reference
   docs, or decision records where appropriate.

## Guardrails

- Do not clutter always-loaded instructions with excessive metadata.
- Prefer source paths, verification dates, and re-check conditions for facts with known freshness risk.
- Do not change provider-specific files without checking whether the canonical
  source should change first.
- If no local parameter map exists, state the assumed instruction, knowledge,
  and decision-record locations before editing.
