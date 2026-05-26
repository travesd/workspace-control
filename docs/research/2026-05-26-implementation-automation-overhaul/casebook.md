# Implementation Automation Casebook

Date: 2026-05-26

Status: initial sample from task artifacts; no raw transcript content

Purpose: identify recurring request and fulfillment shapes that should inform
the implementation automation kernel.

## Sampled Cases

| Case | Source | Request Class | Fulfillment Shape | Friction / Risk | Candidate Automation Gate |
|---|---|---|---|---|---|
| RBAC path-param matching | `/workspace/detection-platform-metal-work/done/20260525-mon/1.rbac-path-param-matching/SUMMARY.md` | focused product bug fix | PR merge with focused tests and Docker validation | low drift; ordinary scoped implementation | `source-read`, `scope`, `validation` gates enough; no agent loop needed |
| Filter-service subdomain whitelist | `/workspace/detection-platform-metal-work/done/20260525-mon/2.filter-service-subdomain-whitelist/SUMMARY.md` | focused product feature/fix | PR merge with focused and full package tests | needed merge-tree checks against updated `main` | add `pre-merge-base` and `conflict-scan` gate for PR follow-ups |
| Brand automation config foundation | `/workspace/detection-platform-metal-work/done/20260525-mon/4.brand-automation-config-foundation/SUMMARY.md` | scoped slice from broader feature | PR narrowed to event-history/API plumbing; broader implementation preserved elsewhere | scope control mattered more than implementation difficulty | require package-level non-goals and follow-up pointer for extracted scope |
| Social submission policy admin controls | `/workspace/detection-platform-metal-work/done/20260525-mon/5.social-submission-policy-admin-controls/SUMMARY.md` | multi-surface product feature | API/UI/RBAC/migration implementation with CI and conflict resolution after another PR | merge sequencing and migration ordering were load-bearing | add `dependency-pr` and `migration-order` gates |
| PR #99 first review | `/workspace/detection-platform-metal-work/done/20260525-mon/6.review-pr-99-monitoring-sync/SUMMARY.md` | deep PR review | code-trace + prod read-only evidence + review post | initial blocker was withdrawn after user reframed layered data-shape semantics | add `invariant-check` gate requiring explicit "is this asymmetry intended?" before blocker claims |
| PR #99 re-review | `/workspace/detection-platform-metal-work/done/20260526-tue/3.review-pr-99-monitoring-sync-cidb/SUMMARY.md` | review follow-up verification | verified each prior item against code and tests; ran containerized build/vet/test; approved | sqlite vs postgres behavior remained a soft residual risk | add `prior-findings-ledger` and `test-fidelity` gates |
| PR #101 review | `/workspace/detection-platform-metal-work/done/20260526-tue/2.review-pr-101-bot-http-social/SUMMARY.md` | high-risk PR review | independent human/agent review, call-a-friend cross-check, posted correction | cross-check caught a wording overclaim in NULL-vs-empty-string framing | add `cross-review` gate for large PRs and `correction-posted` evidence when review framing changes |
| Release notes audit | `/workspace/detection-platform-metal-work/done/20260525-mon/7.release-notes-audit/SUMMARY.md` | release/process investigation | compared release assets, tags, workflow, changelog script, and commit ranges | product/release learning did not belong in workspace-control knowledge | add `durable-home` gate to prevent over-promoting product facts |
| Workflow improvements go-live | `/workspace/detection-platform-metal-work/done/20260525-mon/8.workflow-improvements-go-live/SUMMARY.md` | operating-model activation | staged workspace-control changes, validation, rollback snapshots, activation | activation boundary and rollback evidence were the main risk controls | add `activation-boundary`, `rollback-snapshot`, and `live-check` gates |
| Knowledge source migration | `/workspace/detection-platform-metal-work/done/20260525-mon/9.workspace-knowledge-source-migration/SUMMARY.md` | operating-model/source-of-truth refactor | split workspace-control vs product-adjacent knowledge, activated docs/skills after validation | weak-provenance notes had to stay visible instead of becoming automation | add `provenance-strength` gate before knowledge drives automation |
| Knowledge follow-ups | `/workspace/detection-platform-metal-work/done/20260525-mon/10.workspace-knowledge-followups/SUMMARY.md` | cleanup and evidence hardening | re-verified/softened notes, kept pointer files due active references | cleanup had hidden dependency on active task references | add `active-reference-scan` gate before removing pointer files or aliases |
| Knowledge promotion | `/workspace/detection-platform-metal-work/done/20260525-mon/11.workspace-knowledge-promotion/SUMMARY.md` | skill/knowledge promotion decision | preserved candidate skill material as draft-only, not hot-path behavior | useful content was intentionally not activated | add `promotion-target` gate: draft, knowledge, skill, AGENTS, or no action |
| Threat-hunter submissions report | `/workspace/detection-platform-metal-work/done/20260526-tue/1.threat-hunter-submissions-report-7d/SUMMARY.md` | read-only DB report + static artifact | DB aggregate, static HTML report, local transient server, cleanup | source convention nuance mattered; data was point-in-time and not a durable dataset | add `data-retention` and `query-provenance` gates |
| Brand automation extraction | `/workspace/detection-agentic-workflows-work/busy/brand-automation-extraction/resume.md` | cross-repo extraction + guarded workflow implementation | standalone repo extraction, default-off writes, artifact validation, dry-run execution | credential hygiene and write boundary were critical | add `write-policy`, `artifact-validation`, and `credential-sanitization` gates |
| Evaluator audit conversion | `/workspace/detection-agentic-workflows-work/busy/convert-evaluator-audit-to-agentic-workflows/SUMMARY.md` | skill-to-deterministic-workflow port | package-based P0-P10 conversion with schemas, runbooks, parity evidence, oracle | package acceptance bars worked; remaining gap was categoriser-grounded score run | add `package-acceptance` and `parity-oracle` gates |
| Current session/status layer | `/workspace/detection-platform-metal-work/SESSIONS.md` | cross-task session recovery | generated index joins task resumes and live panes | one live pane still needs ID; recorded-but-not-live sessions remain normal | add `session-index-fresh` and `pane-id-known-or-waived` gates |

## Patterns

### Automate As Checklists

- focused bug fixes with one repo and clear tests;
- task close-off with no data products;
- workspace status and session reconciliation;
- read-only report reproduction and cleanup.

### Automate As Deterministic Workflows

- PR re-review against prior findings;
- release audit;
- knowledge migration/promotion;
- cross-repo extraction;
- workflow/tool conversion with schemas and parity checks.

### Use Governed Agent Loops Sparingly

- large PR reviews where independent perspectives materially reduce risk;
- ambiguous research or review tasks where subtasks cannot be predicted
  upfront;
- complex LLM/evaluator workflows where iterative critique improves measurable
  output.

### Do Not Automate Yet

- product facts that need a product-doc home;
- provider credential handling beyond documented sanitation checks;
- live activation, push, PR, merge, and destructive cleanup.

## Candidate Gates To Add First

1. `workflow-classification`: kind, complexity, risk, thinking mode,
   automation mode.
2. `source-read`: code/docs/scripts read before claims or edits.
3. `validation-ledger`: commands and results captured as machine-readable
   evidence.
4. `durable-home`: task summary, knowledge note, skill draft, ADR, dataset
   manifest, or no action.
5. `approval-stop`: push, PR, live activation, destructive cleanup, production
   write, and external write actions.
6. `write-policy`: default-off, dry-run, or approved write.
7. `promotion-provenance`: weak memory/task provenance cannot become
   automation until re-verified.
8. `cross-review`: required for high-risk PR reviews and operating-model
   activation.

## Implication

The highest-return initial tool is not a general autonomous agent. It is a
small `workflowctl` that can classify work, check required gates, and surface
missing evidence before agents proceed.
