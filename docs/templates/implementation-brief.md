# Implementation Brief

Status: draft | approved | blocked | superseded

## Scope Bucket

- Bucket: `trivial | standard | wide`
- Why:
- Ceremony adjustment:

## Goal

State the concrete behavior, artifact, or workflow change.

## Problem

Describe the operator or system problem this solves. For product-facing work,
include the affected user/workflow.

## Context And Source Read

- `path/to/source`
- `path/to/test`
- `path/to/doc`

## Non-Goals

- Scope that should not be changed in this implementation.

## Assumptions And Open Questions

- Assumption:
- Open question:

## Write Scope

- `path/or/module`

## Sealed Surfaces

- Tests, fixtures, schemas, data, prompts, or evals that workers must not
  modify without explicit coordinator approval.

## Implementation Packages

| Package | Owner | Write Scope | Acceptance |
|---|---|---|---|
| P0 | coordinator | `path/or/module` | observable result and validation command |

## Operator Summary

Keep this to one screen. Include only the goal, file-action summary,
validation commands, non-goals that matter, and open questions.

## Swarm Routing

- Decision: `none | review-only | parallel-read | parallel-implement`
- Coordinator:
- Shared context pack:
- Merge policy: `coordinator-applies`
- Conflict policy: `stop-and-report`
- Loop cap:

## Background Agent Lanes

| Lane | Role | Task | Mutable Surface | Sealed Surface | Preflight | Handoff |
|---|---|---|---|---|---|---|
| A | source-read | bounded question | none | repo/worktree | context pack read | response or artifact path |

## Stage Artifacts

- Brief:
- Context pack:
- Worker briefs:
- Worker handoffs:
- Review artifacts:

## Validation Plan

```text
command:
cwd:
expected:
fresh pass required before closeoff: yes
```

## Approval Stops

- [ ] push
- [ ] PR
- [ ] live activation
- [ ] destructive cleanup
- [ ] production write
- [ ] external write

## PRD Addendum

Use this section for product-facing or cross-cutting features.

- Target user/workflow:
- Requirements:
- UX/API/data contract:
- Rollout:
- Rollback:
- Acceptance criteria:
