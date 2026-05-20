---
title: Workspace organization and efficiency review
tags: [workspace, organization, skills, knowledge, pi]
status: active
verified: 2026-05-20
source: /workspace/detection-platform-metal-work/investigations/workspace-organization-efficiency-20260520/recommendations.md
re_verify_when: "After workspace-control repo first implementation slice or Pi pilot changes"
---

# Workspace Organization And Efficiency Review

The 2026-05-20 review found that the workspace has strong rules and tooling, but reusable learnings, session metadata, and human indexes drift under long-running multi-agent work.

Priority order:

1. Provider-neutral `knowledge/` plus `durable-learning-capture`.
2. `session-hygiene`.
3. `task-closeoff`.
4. `workspace-status` and `workspace-artifact-inventory`.
5. Manifest-derived dataset and backup indexes.
6. Lightweight claim verification for factual guidance in `AGENTS.md` and shared skills.

The Pi harness should be treated as an adapter/experiment that reads this provider-neutral source of truth, not as the canonical memory system.
