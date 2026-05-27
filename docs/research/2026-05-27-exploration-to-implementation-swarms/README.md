# Exploration-To-Implementation Gate And Background Swarms

Date: 2026-05-27

Status: research recommendation; workspace-control only; not activated live

## Problem

The current interaction pattern has a useful but risky shape:

1. the operator explores code conversationally;
2. the agent follows the exploration and accumulates useful local context;
3. at some point the conversation quietly turns into implementation;
4. edits begin before the goal, non-goals, write scope, validation, and approval
   stops are fully explicit.

The fix should not suppress exploratory code discussion. Exploratory
conversation is how the operator finds the actual problem. The missing control
is a promotion gate between exploration and implementation.

A second goal is to make implementation less blocking by using background agent
work. That is useful, but only if the work is decomposed into bounded,
non-conflicting lanes with a coordinator-owned integration step.

## Sources Reviewed

External:

- OpenAI Codex best practices:
  `https://developers.openai.com/codex/learn/best-practices`
- OpenAI Codex quickstart and cloud/background task guidance:
  `https://developers.openai.com/codex/quickstart`
- Claude Code common workflows, including plan-before-editing:
  `https://code.claude.com/docs/en/common-workflows`
- Claude Code parallel agents:
  `https://code.claude.com/docs/en/agents`
- Claude Code subagents:
  `https://code.claude.com/docs/en/sub-agents`

Local:

- `/workspace/reference_repos/Simon-sdlc-skill.md`
- `/workspace/workspace-control/docs/specs/implementation-automation-kernel.md`
- `/workspace/workspace-control/docs/specs/task-lifecycle.md`
- `/workspace/workspace-control/docs/specs/task-resumability.md`
- `/workspace/workspace-control/docs/reviews/2026-05-26-workflowctl-five-task-pilot.md`
- `/workspace/workspace-control/tools/workflowctl`
- Local explorer review from 2026-05-27.

## Useful Patterns

### Plan Before Difficult Work

OpenAI's Codex guidance recommends planning before complex, ambiguous, or hard
to describe tasks, including Plan mode, an interview step, or an execution-plan
template. Its suggested prompt shape is also directly relevant here: goal,
context, constraints, and done-when.

Local implication: after exploratory discussion, implementation should not begin
until those four fields exist in a task artifact.

### Plan Before Editing

Claude Code documents a plan-before-editing mode where the agent reads files and
proposes a plan before touching disk. This maps exactly to our needed boundary:
explore freely, then stop before edits and create an implementation contract.

Local implication: this should be a workflow gate, not a social reminder.

### Background Work Needs Isolation

OpenAI and Claude docs both support background or parallel coding tasks, but the
useful pattern is not "more agents everywhere." The useful pattern is:

- one coordinator owns the plan and final integration;
- each worker has a bounded mission;
- write scopes are disjoint or isolated by worktree;
- validation and review are separate lanes;
- the user or coordinator reviews diffs before push/PR/merge.

Local implication: background swarms should attach to `workflow.json` as a
contract. They should not bypass workspace approval stops.

### Stable Workflows Become Skills Or Automations

OpenAI guidance separates skills from automations: skills define repeatable
method, automations define schedule/background execution. This matters because
our first step should be a gate and brief template, not immediate full
automation.

Local implication: first implement the manual contract and pilot it, then only
promote stable parts into shared skills or automated dispatch.

### Stage Artifacts Beat Chat Memory

Simon's SDLC skill uses per-stage files as the handoff between explore, plan,
implementation, simplify, review, polish, and ship. The exact `.sdlc/`
directory and tmux driving pattern are repo/provider-specific, but the stage
artifact idea is strong: each phase leaves a durable, replayable record.

Local implication: use task artifacts, `workflow.json`, validation ledgers, and
implementation briefs as the durable handoff. Do not rely on chat history or
raw provider transcripts as the control surface.

### Scope Buckets Prevent Over-Exploration

The SDLC skill starts by sizing work as trivial, standard, or wide, then caps
exploration and planning effort accordingly. This directly addresses the
operator habit we are trying to compensate for: exploratory conversation can
expand past the actual change.

Local implication: the implementation gate should record a scope bucket and
adjust ceremony. Trivial tasks can use a small brief and no swarm. Standard and
wide tasks need source-read evidence, package boundaries, and explicit swarm
routing.

### Human Plan And Worker Plan Are Different Artifacts

The SDLC skill applies a concise-output filter before showing the plan to the
user, while keeping detailed instructions in the worker-consumed plan file. This
is a useful distinction for our workflow: the operator should verify the outcome
and scope, not read every seam-map detail.

Local implication: implementation briefs should have a short operator summary
and a detailed worker contract. Context packs and swarm lane briefs should carry
the detail.

### Hard Worker Preflight

The SDLC skill has a blocking install/preflight step before handing work to a
background Codex session. In this workspace, host installs are prohibited for
product repos, so the exact command is not adoptable. The underlying gate is:
do not dispatch a background worker into an environment that cannot run the
required checks.

Local implication: before spawning implementation workers, verify the worktree,
container/local-stack path, validation commands, and sealed evaluator are
available. If the preflight fails, do not hand off to the swarm.

### Review Loop Caps

The SDLC skill loops only on blocker findings and caps polish attempts. This is
valuable for agent swarms because unlimited background iteration can consume
time while chasing nits.

Local implication: swarm contracts need stop conditions and loop caps. Review
findings should be severity-classified; only blockers trigger worker polish.

## Recommended Local Model

Introduce an explicit mode boundary:

```text
exploration -> implementation gate -> PRD/brief -> swarm routing -> execute -> verify
```

The practical version is:

1. explore conversationally and record sources;
2. size the scope as `trivial`, `standard`, or `wide`;
3. draft a short operator-facing brief;
4. expand that into worker lanes only when the scope justifies it;
5. run a blocking worker preflight;
6. dispatch background lanes;
7. integrate through the coordinator;
8. validate with fresh pass entries;
9. review, polish blockers only, then close off.

### Exploration Mode

Allowed:

- read code and docs;
- ask and answer architecture questions;
- compare options;
- inspect examples;
- identify likely write scopes;
- spawn read-only explorers for independent questions when authorized.

Not allowed:

- product edits;
- branch/worktree mutation unless explicitly preparing a task;
- validation claims without commands or artifacts;
- push, PR, merge, live activation, destructive cleanup.

### Implementation Gate

Trigger the gate when any of these are true:

- the operator says `implement`, `fix`, `build`, `proceed`, `ship`, `make the
  change`, or equivalent after exploratory discussion;
- the agent is about to edit product code;
- the likely change touches three or more files;
- the work crosses repo, service, UI/API, schema, data, LLM policy, or
  workspace-control boundaries;
- the task needs background agents.

The gate should produce either an implementation brief or a PRD.

Scope buckets:

| Bucket | Use When | Required Ceremony |
|---|---|---|
| `trivial` | one file, small diff, obvious existing pattern | short brief, no swarm unless review-only |
| `standard` | 2-5 files or one subsystem | brief, package plan, source-read evidence, swarm routing decision |
| `wide` | cross-subsystem, schema/API/UI, LLM/eval, workspace-control | brief or PRD addendum, context pack, explicit background lanes, review loop cap |

### Implementation Brief Versus PRD

Use an implementation brief for most engineering changes. It should fit in one
screen and include:

- goal;
- context/source-read evidence;
- non-goals;
- write scope;
- assumptions and open questions;
- implementation packages;
- validation plan;
- approval stops.

Use a PRD when the work changes operator-facing product behavior or spans a
larger feature. A PRD should add:

- target user/workflow;
- problem statement;
- requirements;
- acceptance criteria;
- UX/API/data contract;
- rollout and rollback notes.

### Swarm-First Routing

Every non-trivial implementation should pass through a swarm router, but the
router may choose "no swarm" for clear one-file fixes. This avoids adding agent
overhead where it would slow the task down.

Recommended default lanes:

| Task Shape | Background Agents |
|---|---|
| Clear one-file fix | none, or one review/test agent after patch |
| Normal implementation | one source-read explorer and one validation/review agent |
| Cross-cutting implementation | separate implementation workers by disjoint write scope, plus validation/review |
| UI/API/schema work | frontend worker, backend worker, contract/test worker |
| LLM/eval work | evaluator/fixtures worker, implementation worker, disagreement-review worker |
| Workspace-control change | source/spec reviewer and render/activation-check reviewer |

For coding workers, prefer separate worktrees or disjoint write sets. The
coordinator should integrate. Workers should not push, open PRs, merge, or
activate live workspace files.

Worker handoff artifacts should be written under the task directory, not a
provider-specific hidden directory. Suggested names:

```text
implementation-brief.md
artifacts/swarm/<lane-id>-brief.md
artifacts/swarm/<lane-id>-handoff.md
artifacts/review/<iteration>.md
```

## Proposed Contract

Add this shape to `workflow.json` in a later implementation slice:

```json
{
  "implementation_gate": {
    "decision": "continue-exploration | promote-to-implementation | stop",
    "exploration_sources": [],
    "source_read": [],
    "problem_statement": "",
    "goal": "",
    "non_goals": [],
    "implementation_home": "",
    "brief_path": "",
    "prd_path": "",
    "write_scope": [],
    "sealed_surfaces": [],
    "validation_plan": [],
    "open_questions": [],
    "approval_stops": []
  },
  "swarm": {
    "enabled": false,
    "router_decision": "none | review-only | parallel-read | parallel-implement",
    "coordinator": "primary-agent",
    "shared_context_pack": "",
    "merge_policy": "coordinator-applies",
    "conflict_policy": "stop-and-report",
    "agents": [
      {
        "id": "",
        "role": "source-read | implementation | validation | review",
        "task": "",
        "mutable_surface": [],
        "sealed_surface": [],
        "worktree": "",
        "budget": "",
        "stop_conditions": [],
        "handoff_artifact": ""
      }
    ],
    "forbidden_actions": [
      "push",
      "pr",
      "merge",
      "live-activation",
      "production-write",
      "destructive-cleanup"
    ]
  },
  "stage_artifacts": {
    "brief": "",
    "worker_briefs": [],
    "worker_handoffs": [],
    "reviews": [],
    "polish": [],
    "ship": ""
  }
}
```

## Risks

- Background agents multiply conflicts unless write scopes are explicit.
- Background agents can make the main conversation less aware of details unless
  every lane returns a structured handoff artifact.
- "Always use swarms" can waste time on trivial tasks. The safer rule is:
  always route through the swarm decision; only spawn workers when the router
  shows positive value.
- PRD ceremony can slow small work. Keep the brief lightweight and reserve full
  PRDs for larger product changes.
- Provider-specific background features differ. Keep the canonical contract
  provider-neutral and export provider-specific runbooks later.
- Simon's SDLC skill auto-pushes, auto-creates PRs, and auto-admin-merges to
  staging. That is not adoptable here because workspace rules require explicit
  approval for push/PR/merge/live activation, and product validation must stay
  local/container-based.
- Simon's SDLC skill runs host package installs. That is not adoptable for
  product repos in this workspace; use container/local-stack validation gates
  instead.

## Recommendation

Proceed with a small workspace-control implementation:

1. add an implementation brief template;
2. add PRD fields to the brief template rather than creating a heavy PRD
   process first;
3. extend the workflow spec with `implementation_gate` and `swarm`;
4. add `workflowctl gate check` and `workflowctl swarm check` before adding any
   executor;
5. include scope buckets, stage artifacts, worker preflight, and loop caps;
6. pilot on one real implementation task and one exploratory conversation.
