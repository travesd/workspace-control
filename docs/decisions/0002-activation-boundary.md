# ADR 0002: Keep Workspace-Control Staged Until Explicit Activation

Date: 2026-05-20
Status: accepted

## Context

The first workspace-control snapshot copied live workspace rules, skills, tools, knowledge candidates, and Pi pilot files into a local repo. A deep review found that agents could confuse the repo copy with the live runtime source of truth, especially for shared skills and Pi workflows.

## Decision

Treat `/workspace/workspace-control` as the reviewable source for proposed workspace operating-model changes. The live runtime remains `/workspace` until a change is explicitly activated.

Activation requires:

- sanitization checks,
- human approval,
- a recorded sync path,
- validation through live workspace tooling when skills or tools are activated.

Pi files remain draft-only until a package/schema decision is recorded.

## Consequences

- The repo can evolve safely without silently changing active agent behavior.
- Activation becomes explicit and auditable.
- There is less risk of split-brain skill or Pi configuration during the transition.
