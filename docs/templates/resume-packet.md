# Resume Packet Template

Paste this block into `resume.md` for any non-trivial task.

```markdown
## Resume Packet

- Task path:
- Lifecycle state:
- Goal:
- Current state:
- Exact next action:
- Branch/worktree/PR:
- Sessions/transcripts:
- Validation done:
- Validation still needed:
- Implementation gate:
  - Decision: continue-exploration | promote-to-implementation | stop
  - Scope bucket: trivial | standard | wide
  - Brief:
  - Source-read evidence:
  - Write scope:
  - Swarm routing: none | review-only | parallel-read | parallel-implement
- Important decisions:
- Constraints and guardrails:
- Artifacts and evidence:
- Open questions:
- Chat dependency: optional | useful-for-history | required
- Chat dependency reason:
```

Use `optional` when the task can be resumed from artifacts alone. Use
`useful-for-history` when chat may help explain background but is not required.
Use `required` only when a named chat or transcript is still needed to avoid
losing critical state.

## Resumability Score

```markdown
## Resumability Score

- Score: __/10
- Missing points:
- Chat dependency:
- Fresh-agent recovery estimate:
- Durable extraction: none | done | pending: <target>
```

Score against
`/workspace/workspace-control/docs/specs/task-resumability.md`.
