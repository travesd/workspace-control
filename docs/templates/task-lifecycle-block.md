# Task Lifecycle Block

Use this block in `resume.md` when a task is not plainly active, or when moving
between `busy/`, `parked/`, `later/`, and `archived/`.

```markdown
## Lifecycle

- State: parked
- Substate: prototype-baseline | deferred-pr | extraction-needed | blocked-external | paused-critical
- State reason: Why this task is in the current state.
- Restart when: The condition that moves this back to `busy/`, or `n/a`.
- Extract before archive: Reusable work, learnings, patches, data, or decisions to harvest before final archive.
- Branch/worktree status: Branch, PR, worktree, and cleanliness state.
- Artifact policy: What must be preserved, moved to `/workspace/datasets/`, or summarized.
- Review after: Optional date, event, or decision trigger.
```

State-specific notes:

- For `parked/`, `Restart when` or `Extract before archive` must be concrete.
- For `later/`, keep the block short; use `State reason` and links only when
  there is no active branch or artifact state.
- For `archived/`, prefer `SUMMARY.md`; include the replacement path or reason
  no restart is expected.
