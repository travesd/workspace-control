# Implementation Automation Overhaul Research

Date: 2026-05-26

Status: research synthesis; no live activation

## Question

How should `workspace-control` evolve from a resumability and instruction
system into an implementation automation control plane for Claude, Codex, Pi,
and future agent harnesses?

This pass reviewed current workspace evidence, prior history reviews, and
external sources on thinking modes, problem solving, systems design, and AI
agent architecture. It intentionally translates sources into local implications
instead of preserving raw research.

## Local Evidence

The 2026-05-20 workspace organization review already found strong agreement
between Claude and Codex:

- durable learning capture was split between task notes, provider-local memory,
  and summaries;
- session hygiene and task close-off depended too much on human discipline;
- agents repeatedly paid a session-start scout tax;
- stale high-precedence claims could misdirect implementation work.

Source paths:

- `docs/research/2026-05-20-workspace-organization/recommendations.md`
- `docs/research/2026-05-20-workspace-organization/reviews/cross-review.md`
- `docs/specs/task-resumability.md`

The 2026-05-25 go-live closed the first layer: thin live instructions, shared
skills, generated status, knowledge indexing, lifecycle states, and
repo-first activation are live-aligned. That made work recoverable.

Source path:

- `/workspace/detection-platform-metal-work/done/20260525-mon/8.workflow-improvements-go-live/SUMMARY.md`

The current 2026-05-26 live status shows the next bottleneck:

- `workspace-status --brief` reports 12 busy task dirs, 13 recorded sessions,
  10 recorded-but-not-live sessions, one live pane needing an ID, and 27 stale
  workspace-control knowledge candidates.
- `detection-agentic-workflows` now contains JSON-envelope style operator
  workflows and artifact validation. The brand automation extraction task has
  already proven the value of plan/draft/review/write-plan/execute-dry-run
  pipelines with saved handoff artifacts.

Source paths:

- `/workspace/detection-platform-metal-work/SESSIONS.md`
- `/workspace/detection-agentic-workflows-work/busy/brand-automation-extraction/resume.md`
- `/workspace/detection-agentic-workflows-work/busy/convert-evaluator-audit-to-agentic-workflows/resume.md`

Follow-up external review:

- `karpathy-github-review.md` reviews Andrej Karpathy's GitHub projects and
  maps `autoresearch`, `nanochat`, `llm-council`, and the minimal reference
  implementation repos into concrete changes for this kernel.

Follow-up chat-history review:

- `chat-history-patterns.md` aggregates local Claude and Codex history signals
  without preserving raw transcripts. It confirms that implementation,
  verification, review, resumability, environment preflight, approval stops,
  and durable-learning routing should be first-class workflow states.

Conclusion: the workspace no longer mainly needs more instructions. It needs a
typed control loop that turns task requests into classified work, selected
thinking modes, owned artifacts, validation gates, and close-off extraction.

## External Patterns Mapped Locally

| Source | Useful Pattern | Workspace Implication |
|---|---|---|
| Kahneman dual-process model, Nobel biography | Judgement can be fast/intuitive or slower/rule-governed; deliberate reasoning can correct intuitive errors. | Encode a mode router. Routine tasks can use checklist automation, but risky implementation and ambiguous investigation need explicit slow-path gates. |
| Klein recognition-primed decision model | Experts often generate a plausible option from experience, then act without comparing many options. | Preserve fast expert paths for recurring workspace tasks, but require evidence and simulation/validation before acting when blast radius is non-trivial. |
| Design Council Double Diamond | Discover/define before develop/deliver; test small and reject what fails. | Split task automation into problem framing and implementation phases. Do not let agents implement from a vague user prompt without a typed problem frame. |
| Cynefin complexity framing | Clear, complicated, complex, and chaotic situations need different approaches. | Route clear tasks to deterministic checklists, complicated tasks to expert/planned implementation, complex tasks to experiments and evaluators, and chaotic tasks to stabilization only. |
| Donella Meadows leverage points | Rules, information flows, goals, and self-organization are higher leverage than changing individual events. | Prioritize tooling and contracts that change future agent behavior over adding reminders to `AGENTS.md`. |
| NASA systems engineering | System design, product realization, and crosscutting technical management are separate but connected concerns. | Add explicit phase gates for requirements, design, realization, verification, and lifecycle management in task automation. |
| SEI software architecture | Architecture is design decisions about structure and behavior; early analysis of qualities reduces downstream rework. | Implementation plans should state quality attributes and fitness checks before editing code, especially for shared services and agent workflows. |
| Google SRE toil framing | Manual, repetitive, automatable, tactical work with no enduring value scales poorly. | Identify repeated agent chores and turn them into `workflowctl` commands or deterministic workflow tools; keep novel judgment with humans/agents. |
| NIST AI RMF | AI risk management uses govern/map/measure/manage and must consider lifecycle, context, real-world drift, and human-AI interaction. | Agent automation needs governance metadata, mapped risk, measurement artifacts, and managed approvals for write-side or high-impact steps. |
| Anthropic agent architecture guidance | Start simple; distinguish predefined workflows from autonomous agents; use evaluator-optimizer, routing, parallelization, and ground-truth feedback when appropriate. | Prefer deterministic workflows and structured tools first; only use open-ended agent loops when fixed workflows cannot predict the steps. |
| OpenAI agent guidance | Agents manage workflow execution, use tools, operate within guardrails, and should hand control back on failure. | Define agentic implementation as a controlled workflow owner with tool access, guardrails, stop conditions, and explicit human handoff points. |
| OpenAI Agents SDK docs | Server-owned orchestration is appropriate when application code owns tools, state, approvals, and observability. | `workspace-control` should specify orchestration/state/approval contracts; provider adapters can execute them without becoming the source of truth. |

## Thinking Modes To Encode

### 1. Recognition Mode

Use for recurring tasks with known playbooks: status checks, session hygiene,
task close-off, DB read-only investigations, dataset export, and browser
review. The automation should choose the relevant skill, run the current live
tool, and preserve evidence.

Failure mode to guard against: treating a superficially familiar task as
identical to the previous one. Require a short scope/risk check before writes.

### 2. Deliberate Engineering Mode

Use for normal implementation. The agent must read the relevant source, define
the target behavior, create a plan, make scoped edits, and validate through the
containerized local stack.

Failure mode to guard against: code-first action without source reading, or
declaring success from inference rather than command output.

### 3. Divergent-Convergent Design Mode

Use when the request is vague, cross-cutting, or design-heavy. First widen:
collect evidence, user goals, constraints, alternatives, and risks. Then narrow:
choose one plan and acceptance gates.

Failure mode to guard against: overfitting to the user's first example or to a
single convenient discriminator.

### 4. Experimental Complex-Systems Mode

Use for LLM prompt/workflow quality, classifier policy, corpus generation,
review rubrics, and emergent behavior. The control loop should produce
experiment logs, model/provider/config metadata, fixture sets, disagreement
examples, and measurable criteria.

Failure mode to guard against: turning observed examples into hard-coded rules
before the failure mode is understood.

### 5. Systems-Leverage Mode

Use for workspace-control changes. Ask which intervention changes the system:
rules, information flows, task state shape, tool affordances, feedback loops,
or source-of-truth boundaries.

Failure mode to guard against: adding another reminder where the right answer
is a generated artifact, a typed contract, or an execution gate.

### 6. Governed Agent Mode

Use only when a task needs autonomous multi-step control. It requires a sandbox,
approved tool surface, stop conditions, trace artifacts, validation gates, and
human checkpoints for destructive, production, or external write actions.

Failure mode to guard against: building a free-form agent when a deterministic
workflow would be cheaper, safer, and easier to debug.

## Proposed Direction

The next workspace-control leap should be an Implementation Automation Kernel:

```text
request
  -> intake contract
  -> mode router
  -> task/worktree/session preflight
  -> executable plan with acceptance gates
  -> scoped implementation packages
  -> validation and review evidence
  -> close-off and durable learning extraction
```

This should live in `workspace-control` as source-of-truth specs, templates,
and a small helper tool first. Live activation remains separate.

The kernel should not replace agent judgement. It should reduce avoidable
judgement by making the recurring decisions explicit:

- what kind of work is this?
- which thinking mode applies?
- what artifacts must exist before edits?
- what validates completion?
- what must be preserved or extracted?
- where does the learning go?

## Sources

- Daniel Kahneman Nobel biography:
  `https://www.nobelprize.org/prizes/economic-sciences/2002/kahneman/biographical/`
- Gary Klein Recognition-Primed Decision model:
  `https://www.gary-klein.com/rpd`
- Design Council Double Diamond:
  `https://www.designcouncil.org.uk/resources/the-double-diamond/`
- Harvard Business Publishing overview of Cynefin:
  `https://www.harvardbusiness.org/insight/navigating-complexity-a-new-map-for-a-new-territory/`
- Donella Meadows, "Leverage Points: Places to Intervene in a System":
  `https://groups.nceas.ucsb.edu/sustainability-science/2010%20weekly-sessions/session-112013-11.22.2010-managing-for-sustainability-speaker-pamela-matson/supplemental-readings-from-the-reader/Meadows.%201999%20Leverage_Points.pdf/view.html`
- NASA Systems Engineering Handbook:
  `https://www.nasa.gov/reference/systems-engineering-handbook/`
- CMU SEI Software Architecture:
  `https://www.sei.cmu.edu/software-architecture/`
- Google SRE, "Eliminating Toil":
  `https://sre.google/sre-book/eliminating-toil/`
- NIST AI RMF 1.0:
  `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf`
- Anthropic, "Building effective agents":
  `https://www.anthropic.com/engineering/building-effective-agents`
- OpenAI, "A practical guide to building agents":
  `https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf`
- OpenAI Agents SDK docs:
  `https://developers.openai.com/api/docs/guides/agents`
