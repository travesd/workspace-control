# ADR 0003: Activate Shared Skill Parameterization

Date: 2026-05-25
Status: accepted

## Context

The workspace-control repo had accumulated reviewed changes that made shared
skills more provider-neutral and easier to render from core, workspace, and
provider layers. The reviewed source was `/workspace/workspace-control` at
commit `b48f1d2`, with the main implementation commits:

- `e807a12 docs(workspace): parameterize core learning skills`
- `330d7a7 docs(workspace): split call-a-friend provider commands`
- `b48f1d2 docs(workspace): plan skill activation`

Pre-activation checks passed, and `tools/renderctl dry-run --mode live-check`
reported intentional live drift: the live workspace lacked two tool README
files and had older canonical/provider skill mirrors.

## Decision

Activate only the reviewed shared-skill and documentation slice into the live
workspace:

- sync `/workspace/workspace-control/agent-skills/skills/` to
  `/workspace/agent-skills/skills/`,
- regenerate `/workspace/.claude/skills/` and `/workspace/.agents/skills/`,
- copy the documentation-only tool README files into `/workspace/tools/`.

The activation explicitly excluded `AGENTS.md`, `CLAUDE.md`, Pi files,
provider runtime configuration, product repos, task lifecycle movement, and
active chat interruption.

A rollback snapshot was captured before writes:

```text
/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521/rollback/20260525T132202Z-before-skill-parameterization-activation/
```

## Consequences

Fresh Claude and Codex sessions now see the activated 17 shared skills and the
updated workspace tool documentation. Existing active chats keep their loaded
context until they are resumed, restarted, or ended.

The post-activation live drift check passed. The activation also exposed that
`skillctl sync` did not remove stale files from already-managed provider
mirrors. Future syncs must prune managed mirror directories before copying
canonical skill contents while still refusing to overwrite unmanaged mirrors.
