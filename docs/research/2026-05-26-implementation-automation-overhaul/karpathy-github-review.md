# Karpathy GitHub Review

Date: 2026-05-26

Status: external research supplement; no live activation

## Source

Reviewed:

- GitHub profile API: `https://api.github.com/users/karpathy`
- Repo list API: `https://api.github.com/users/karpathy/repos?per_page=100&sort=updated`
- `https://github.com/karpathy/autoresearch`
- `https://github.com/karpathy/nanochat`
- `https://github.com/karpathy/llm-council`
- `https://github.com/karpathy/reader3`
- `https://github.com/karpathy/rendergit`
- `https://github.com/karpathy/gitstats`
- `https://github.com/karpathy/micrograd`
- `https://github.com/karpathy/nanoGPT`
- `https://github.com/karpathy/llm.c`
- `https://github.com/karpathy/llama2.c`
- `https://github.com/karpathy/minbpe`

The profile had 63 public repos at review time. The highest-signal recent repos
for our workflow-control work are `autoresearch`, `nanochat`, `llm-council`,
`rendergit`, and the minimal reference implementation family
(`micrograd`, `nanoGPT`, `llm.c`, `llama2.c`, `minbpe`).

## Useful Pattern

### 1. Agent Autonomy Works When The World Is Tiny

`autoresearch` makes an agent autonomous by shrinking the world:

- one mutable file: `train.py`;
- one sealed evaluator/harness: `prepare.py`;
- one human-editable program: `program.md`;
- one fixed run budget: 5 minutes;
- one main metric: validation bits per byte;
- one ledger: `results.tsv` with keep/discard/crash;
- one branch lineage per run.

This is the cleanest concrete example found for implementation automation. It
does not ask the model to be broadly trustworthy. It creates a small game where
trustworthiness is replaced by measurement and reversible search.

Workspace implication:

- `workflowctl` should optimize for "tiny worlds": explicit write scope, sealed
  validation, fixed budget, and a results ledger.
- For implementation tasks, the default artifact should identify the mutable
  surface and the sealed evaluator surface.
- For LLM/rubric/classifier work, an autonomous loop is acceptable only after
  the metric and keep/discard rule are fixed.

### 2. Program Files Are The New Research Org Code

`autoresearch` treats `program.md` as the editable instruction layer for the
agent organization. The code under experiment changes, but the human mainly
programs the agent through the Markdown program.

Workspace implication:

- Our shared skills, runbooks, `workflow.json`, and implementation packages are
  not documentation-only. They are executable organization code for agents.
- We should version and review workflow-control prompts/programs with the same
  seriousness as product code.
- A future `workflowctl` should support a `program.md` or `workflow.md` surface
  per task when autonomous iteration is authorized.

### 3. Keep/Discard Needs A Metric And A Complexity Budget

`autoresearch` tells the agent to keep changes that improve the metric and to
prefer simplification when metrics tie. `llm.c`, `llama2.c`, and `nanochat`
apply the same taste at repo scale: root/default paths stay simple and
hackable; complex or platform-specific work lives in `dev/`, forks, or optional
paths.

Workspace implication:

- Add a complexity budget to implementation packages: a change can pass tests
  and still be rejected if it adds too much operational complexity.
- `workflowctl validate` should eventually support a human-readable
  "complexity delta" note alongside test results.
- For workspace-control itself, default behavior should remain a small
  reference implementation; richer adapters belong under provider/workspace
  overlays.

### 4. One Dial Beats A Hundred Knobs

`nanochat` emphasizes a single complexity dial (`--depth`) that determines the
rest of the model configuration. This is a design principle, not just an LLM
training trick.

Workspace implication:

- Implementation automation should expose a few profiles instead of many knobs:
  `checklist`, `deterministic-workflow`, `agent-loop`; `clear`, `complicated`,
  `complex`, `chaotic`; low/medium/high risk.
- Avoid a sprawling workflow schema where agents must fill dozens of weakly
  meaningful fields before doing work.

### 5. Leaderboards Make Progress Concrete

`nanochat` converts open-ended model improvement into "time to GPT-2" and
leaderboard rows with date, commit, metric, and contributor. `autoresearch`
turns overnight tinkering into logged experiments.

Workspace implication:

- Our automation metrics should be visible, not just preserved:
  - time from request to first useful action;
  - percent of tasks with validation ledgers;
  - repeated correction categories;
  - closeoff completeness;
  - tasks that still require raw chat to resume.
- `workspace-status` should eventually show a tiny automation-health summary;
  the full leaderboard belongs in `workspace-artifact-inventory` or an
  investigation artifact.

### 6. Multi-Model Review Is Useful, But It Needs Structure

`llm-council` uses first opinions, blind peer review, and a chairman synthesis.
This mirrors our recent high-value PR review pattern: independent pass,
cross-review, synthesis, and correction when the review framing overclaims.

Workspace implication:

- Keep `call-a-friend`, but make it a typed gate in the kernel:
  `cross-review.required=true` for high-risk PR reviews, operating-model
  activation, and LLM evaluator changes.
- Prefer "independent pass -> anonymized/identity-minimized critique ->
  synthesis" over unstructured parallel opinions.
- Preserve disagreement examples, not just the final answer.

### 7. Flattened Context Is A Tool Primitive

`rendergit` exists because clicking through repo trees is poor ergonomics for
both humans and LLMs. It offers a human view and an LLM-oriented flat view.
`reader3` does the same for EPUB chapters: make bounded chunks easy to pass to
LLMs.

Workspace implication:

- Add a future `workflowctl context-pack` command that renders a bounded task or
  worktree slice into a reviewable bundle for humans/agents.
- The bundle must respect local secret and size filters, and should include
  source paths plus selected files, not the entire workspace.
- This could reduce the repeated source-scout tax without relying on raw chat.

### 8. Minimal Reference Implementations Are Better Than Frameworks

Across `micrograd`, `minbpe`, `nanoGPT`, `llm.c`, and `llama2.c`, the repeated
pattern is a readable reference implementation with tests and a clear extension
boundary. Even when performance matters, complexity is admitted only when it is
broadly useful and localized.

Workspace implication:

- The implementation automation kernel should start as a small reference
  workflow plus `workflowctl`, not as a generic orchestration platform.
- Provider adapters should be forks/ports in spirit: linked and validated, but
  not allowed to pollute the root control loop with provider-specific branches.

## Proposed Actions

### Patch The Kernel Spec

Add these concepts to `docs/specs/implementation-automation-kernel.md`:

- mutable surface;
- sealed evaluator surface;
- budget;
- metric;
- keep/discard rule;
- complexity delta;
- optional context-pack.

### Patch The Templates

Extend `docs/templates/workflow.json` with:

- `experiment.budget`;
- `experiment.metric`;
- `experiment.keep_rule`;
- `surfaces.mutable`;
- `surfaces.sealed_evaluator`;
- `complexity_delta`.

### Patch The Plan

Add a Karpathy-informed `workflowctl` slice:

- `workflowctl context-pack`;
- `workflowctl experiment init`;
- `workflowctl experiment record`;
- no autonomous loop until metrics and approval gates are explicit.

## Caveats

- `autoresearch` uses destructive git reset as part of its keep/discard loop.
  Do not copy that directly into this workspace. If adopted, it must happen only
  inside an isolated worktree/branch with explicit authorization and with task
  artifacts preserved.
- Karpathy's repos are intentionally hackable and sometimes explicitly
  unsupported. That is a good research pattern, not a direct production
  operating model.
- GPU training benchmarks do not map to detection-platform validation. The
  transferable idea is fixed-budget, metric-led iteration, not the specific
  metric.
