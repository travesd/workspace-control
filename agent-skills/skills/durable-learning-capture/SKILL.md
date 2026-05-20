---
name: durable-learning-capture
description: Route reusable workspace learnings into the correct durable home: knowledge notes, AGENTS.md, shared skills, dataset manifests, or task summaries.
---

# Durable Learning Capture

Use this skill when the user says to remember something, a task produces a reusable lesson, a review finds repeatable feedback, or an `/insights`-style report surfaces a durable pattern.

## Workflow

1. Identify the learning and its scope.
2. Verify the source before writing. Cite the task, file, command output, or report path.
3. Choose the durable home:
   - Always-on safety or workspace rule: `AGENTS.md`.
   - Repeatable multi-step procedure: shared skill under `agent-skills/skills/`.
   - Reusable fact, method, gotcha, or principle: `knowledge/*.md`.
   - Dataset-specific fact: dataset `MANIFEST.json` or `SNAPSHOT.md`.
   - Task-specific detail: task `notes.md` or `SUMMARY.md`.
4. For `knowledge/` notes, use frontmatter with `title`, `tags`, `status`, `verified`, `source`, and `re_verify_when`.
5. If promoting to a shared skill, follow `skill-maintainer` rules before syncing to provider mirrors.

## Guardrails

- Do not store secrets, env values, provider transcripts, or raw user prompts.
- Do not make provider-local memory the source of truth.
- Do not add broad global rules for one-off events; keep those in task notes until they repeat.
