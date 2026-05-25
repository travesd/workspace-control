# Draft Skill Promotion: Review And Prompt Iteration

Status: draft-only, not activated.

Created: 2026-05-25.

This draft preserves candidate skill/rubric changes from the workspace
knowledge promotion task without putting them in the hot path.

These files are intentionally under `docs/drafts/`. They are not consumed by
`renderctl`, `skillctl sync`, live `/workspace/agent-skills/`, Claude mirrors,
Codex mirrors, or Pi drafts.

## Source Evidence

- `/workspace/detection-platform-metal-work/done/20260515-fri/1.audit-pushed-incidents-20260506/SUMMARY.md`
- `/workspace/detection-platform-metal-work/done/20260515-fri/1.audit-pushed-incidents-20260506/corpus-edits/filter/seam-iteration-history.md`
- `/workspace/detection-platform-metal-work/busy/audit-pr64-before-after/notes.md`
- `/workspace/detection-platform-metal-work/busy/audit-pr64-before-after/iteration-log.md`
- `/workspace/datasets/curated-impersonation-70sample/MANIFEST.json`

## Candidate Changes

### Review Rubric Additions

Candidate target skills:

- `agent-skills/skills/validating-ground-truths/`
- `agent-skills/skills/autohunt-ground-truth-review/`

Draft rules:

- Judge the evaluator or classifier against its own configured rubric and
  output contract. Do not broaden a narrow impersonation or targeting question
  into generic maliciousness review.
- Treat designed handoffs as correct when the downstream path is part of the
  workflow contract. A non-portraying credential phish can be `suspicious`
  instead of a takedown-seam false negative.
- Use `monitor` for brand-confusable no-content domains. Content-bearing
  unrelated pages should resolve to `safe` or `suspicious`, not monitor.
- Do not use `rule_judgement`, `clientId`, or general knowledge as proof of
  protected-brand targeting.

Detailed rubric text to consider during promotion:

```markdown
### Mirror the Component's Own Decision Definition

When validating a classifier or evaluator, judge against that component's
actual prompt, rubric, and output contract. Do not replace a narrow component
question with a broader "is this malicious?" standard.

Example from PR #64: the autohunt impersonation seam asks whether the page
positively portrays itself as the protected brand. A credential-phishing page
on a brand-confusable hostname can be malicious without satisfying that seam's
positive-portrayal definition; a downgrade to `suspicious` can be the designed
handoff, not a false negative.

Use the broader system harm question only when the component under review is
itself responsible for that broader judgement.
```

```markdown
### Designed Handoffs Are Not Errors

Some workflows intentionally downgrade cases to another review path. In PR #64,
the autohunt impersonation seam validates positive brand portrayal only:
`impersonation -> takedown`, `association -> suspicious`, `none -> safe`.

Before marking an error, confirm whether the output was a terminal safe result
or a designed handoff to another workflow, queue, or human-review path.
```

### Candidate New Skill: `llm-prompt-iteration`

Draft trigger:

```yaml
name: llm-prompt-iteration
description: Iterate detection LLM workflow prompts with trace-backed prompt changes, variance-aware evaluation, prompt-cache updates, and task-local evidence ledgers.
```

Draft body:

```markdown
# LLM Prompt Iteration

Use this skill when changing or reviewing detection LLM workflow prompts,
judge/classifier rubrics, or evaluator prompt versions.

## Core Workflow

1. Read the current workflow YAML, prompt, output schema, and routing contract.
2. State the component's exact decision responsibility. Do not broaden it into
   a generic "is this bad?" question.
3. Collect trace evidence for failures before changing instructions. Use
   actual model reasoning, step traces, disagreement examples, or fixture
   failures.
4. Prefer concept-first framing over manifestation lists. Scope the question
   and inputs; do not teach the model a closed checklist of examples unless the
   component truly needs a list.
5. Add only trace-justified disambiguators. Avoid speculative prompt clauses.
6. Version the prompt file, bump the workflow signature or prompt cache key as
   the local convention requires, and record the change in a task-local ledger.
7. Validate on the relevant ground-truth fixture set. For borderline cases,
   compare multi-run means or majority decisions, not a single run.

## Design Checks

- Hardcoded lists, policy matrices, suffix tables, thresholds, and deterministic
  decision trees usually belong in code, not prompts.
- Keep LLMs for content understanding, multimodal reasoning, ambiguity, and
  novel-pattern detection.
- Asymmetric input visibility can be correct: give each stage the inputs that
  match its optimization target.
- Designed handoffs are valid outputs when the workflow contract routes them
  onward.
```

Draft reference sections:

- Evidence gate: component name, workflow, prompt version, output schema,
  exact responsibility, failing fixtures, traces, and routing consequence.
- Prompt change rules: concept-first framing, trace-justified disambiguators,
  no speculative clauses, no accidental single-signal dominance.
- Versioning: numbered prompt/workflow version, signature/cache-key update,
  task-local ledger with model/provider, temperature/max tokens, fixture set,
  run time, and result summary.
- Validation: fixture set first; repeated runs for small or borderline sets;
  preserve disagreement examples and unstable cases.

## Promotion Gate

Before promotion into `agent-skills/skills/` or a layered skill source:

1. Re-check source evidence and confirm the candidate text still matches the
   current workflow/rubric semantics.
2. Decide whether this should be a new skill or a reference section in an
   existing skill.
3. Apply the candidate changes to `agent-skills/skills/` and, if still needed,
   the layered source under `workspaces/detection-platform-metal/skills/`.
4. Run `SKILLCTL_CANONICAL_DIR=/workspace/workspace-control/agent-skills/skills /workspace/tools/skills/skillctl validate`.
5. Run `./tools/renderctl dry-run`.
6. Commit and push after approval.
7. Activate live only after separate explicit approval and rollback notes.
