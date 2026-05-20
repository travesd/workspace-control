---
name: durable-learning-capture
description: Route reusable workspace learnings into the correct durable home: knowledge notes, AGENTS.md, shared skills, dataset manifests, or task summaries.
---

# Durable Learning Capture

Use this skill when the user says to remember something, a task produces a reusable lesson, a review finds repeatable feedback, or an `/insights`-style report surfaces a durable pattern.

## Workflow

1. Identify the learning and its scope.
2. Verify the source before writing. Use task evidence, code paths, command output, dataset manifests, ADRs, or explicit user decisions.
3. Choose and record the durable home:
   - Task-only detail: task `notes.md` or `SUMMARY.md`.
   - Reusable fact, method, gotcha, or principle: `knowledge/*.md`.
   - Repeatable multi-step procedure: shared skill under `agent-skills/skills/`.
   - Always-on safety or workspace rule: `AGENTS.md`.
   - Dataset-specific fact: dataset `MANIFEST.json` or `SNAPSHOT.md`.
   - Operating-model decision: ADR under `docs/decisions/`.
4. For `knowledge/` notes, use `knowledge/TEMPLATE.md` and run `tools/knowledgectl lint`.
5. If promoting migrated memory, require fresh evidence before changing automation, shared skills, or global rules.
6. If promoting to a shared skill, follow `skill-maintainer` rules. Do not sync to live provider mirrors unless a separate activation task explicitly approves it.

## Guardrails

- Do not store secrets, env values, provider transcripts, or raw user prompts.
- Do not make provider-local memory the source of truth.
- Do not add broad global rules for one-off events; keep those in task notes until they repeat.
- Do not treat weak migration provenance as enough evidence for automation or global-rule promotion.
