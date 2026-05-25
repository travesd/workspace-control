---
name: research-to-knowledge
description: Convert external research or public examples into concise workspace-specific learnings, proposed actions, and durable knowledge notes without storing raw research dumps.
---

# Research To Knowledge

Use this skill when external research, public repositories, papers, docs, or examples should be evaluated for workspace process improvements.

## Workflow

1. Record the source reviewed with URL or local path.
2. Extract only patterns that could change workspace behavior.
3. Translate each pattern into workspace-specific implications:
   - where it applies,
   - what action it suggests,
   - what evidence supports it,
   - what risks or incompatibilities exist.
4. Choose the durable home:
   - task note for one-off context,
   - `knowledge/*.md` for reusable learning,
   - shared skill for repeatable procedure,
   - ADR for operating-model decision,
   - spec/template when implementation needs a larger artifact.
5. For knowledge notes, use `knowledge/TEMPLATE.md` and run `tools/knowledgectl lint`.

## Output Shape

```markdown
## Source

- URL or path

## Useful Pattern

- Concise pattern, not a generic summary.

## Workspace Implication

- How it applies here.
- Where it should live.
- Evidence strength and caveats.

## Proposed Action

- Patch, note, skill, ADR, template, or no action.
```

## Guardrails

- Do not store full external articles, raw transcripts, secrets, or broad summaries with no workspace implication.
- Do not copy provider-specific skill formats into canonical shared skills without auditing them.
- Do not let external examples override workspace guardrails such as Docker-only product execution, no auto-push, and explicit live activation.
