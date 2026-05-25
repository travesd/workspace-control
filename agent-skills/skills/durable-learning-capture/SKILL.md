---
name: durable-learning-capture
description: "Route reusable learnings into the correct durable home: knowledge notes, instruction updates, shared skills, data manifests, or task summaries."
---

# Durable Learning Capture

Use this skill when the user says to remember something, a task produces a
reusable lesson, a review finds repeatable feedback, or an insights report
surfaces a durable pattern.

## Workflow

1. Identify the learning, its scope, and the local parameter map for durable
   homes.
2. Verify the source before writing. Use task evidence, code paths, command
   output, data manifests, decision records, or explicit user decisions.
3. Choose and record the durable home:
   - Task-only detail: task notes, resume packet, or closeout summary.
   - Reusable fact, method, gotcha, or principle: local knowledge note.
   - Repeatable multi-step procedure: shared skill or workflow reference.
   - Always-on safety or operating rule: local agent instruction contract.
   - Data-specific fact: data manifest, snapshot note, or evidence manifest.
   - Operating-model decision: decision record.
4. For knowledge notes, use the local note template and lint/index command when
   available.
5. If promoting migrated memory, require fresh evidence before changing automation, shared skills, or global rules.
6. If promoting to a shared skill, follow the local skill-maintainer workflow.
   Do not sync to live provider mirrors unless a separate activation task
   explicitly approves it.

## Guardrails

- Do not store secrets, env values, provider transcripts, or raw user prompts.
- Do not make provider-local memory the source of truth.
- Do not add broad global rules for one-off events; keep those in task notes until they repeat.
- Do not treat weak migration provenance as enough evidence for automation or global-rule promotion.
- If no local parameter map exists, write the learning to task context first
  and propose the durable target before editing global files.
