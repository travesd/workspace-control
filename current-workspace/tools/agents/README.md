# Agent Session Tracking

`sessionctl` records Claude and Codex resume metadata in task-local
`resume.md` files. It is workspace tooling; run it from the host with
`/workspace` as the canonical working directory.

## Quick Start

Create a resume file for an active task:

```bash
/workspace/tools/agents/sessionctl init review-pr-34-tlsh-minhash \
  --worktree /workspace/detection-platform-metal.worktrees/add-minhash-tlsh-hashing \
  --branch add-minhash-tlsh-hashing \
  --pr https://github.com/phishfort/detection-platform-metal/pull/34
```

Record a known resumed session:

```bash
/workspace/tools/agents/sessionctl record review-pr-34-tlsh-minhash \
  --provider Claude \
  --role "PR #34 review" \
  --session-id 8f22a9ae-7a6a-401b-873c-8bd7f2f91fbc \
  --resume-command "cd /workspace && claude-yolo --resume 8f22a9ae-7a6a-401b-873c-8bd7f2f91fbc" \
  --tmux "0:1:claude-pr34"
```

Detect currently resumed Claude/Codex sessions without touching their panes:

```bash
/workspace/tools/agents/sessionctl detect
```

Generate the central lookup:

```bash
/workspace/tools/agents/sessionctl index
```

Recover and normalize task metadata after a crash:

```bash
/workspace/tools/agents/sessionctl reconcile
```

## New Sessions

Claude can be launched with a known session ID:

```bash
/workspace/tools/agents/sessionctl launch-claude review-pr-34-tlsh-minhash claude-pr34 \
  --role "PR #34 review"
```

Codex does not expose a documented "start with this session ID" flag in the
installed CLI. For new Codex work, `launch-codex` starts the session with a
unique tracking token in the initial prompt, waits for the local JSONL
transcript to contain that token, then records the discovered session ID.

```bash
/workspace/tools/agents/sessionctl launch-codex local-brand-snapshot-harvest codex-corpus \
  --role "Corpus validation"
```

Both launch commands create tmux windows with `/workspace` as the working
directory and write or update `busy/<task>/resume.md`.

## Central Lookup

`/workspace/detection-platform-metal-work/SESSIONS.md` is generated from
task-local `resume.md` files plus live tmux/process state. It is an index, not
the source of truth.

Generated outputs:

- `/workspace/detection-platform-metal-work/SESSIONS.md` — human lookup
- `/workspace/detection-platform-metal-work/.sessions/index.json` — machine-readable lookup

Use `sessionctl reconcile` when task dirs are missing `resume.md` files or when
older resume notes need to be normalized into the standard table shape.

## Recovery

After a crash:

1. Read `/workspace/detection-platform-metal-work/ACTIVE.md`.
2. Run `/workspace/tools/agents/sessionctl reconcile`.
3. Read `/workspace/detection-platform-metal-work/SESSIONS.md`.
4. Open each active task's `resume.md`.
5. Recreate tmux windows from the recorded `Resume Command` values.
6. Treat rows marked `pending-id` or `stale` as advisory only; verify against
   transcripts and task notes before resuming.
