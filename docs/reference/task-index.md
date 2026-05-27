# task-index Reference

Status: repo helper; not activated live

`tools/task-index` renders a central discovery index from repo-owned task
roots. It does not change task ownership and does not move task artifacts.

## Command

```text
tools/task-index render [--root <workspace>] [--out <dir>]
```

Without `--out`, the command prints Markdown to stdout. With `--out`, it
writes:

```text
<out>/TASKS.md
<out>/.task-index/index.json
```

The intended live activation targets are:

```text
/workspace/TASKS.md
/workspace/.task-index/index.json
```

## Inputs

The renderer scans:

- `/workspace/detection-platform-metal-work/`
- `/workspace/detection-agentic-workflows-work/`
- `/workspace/workspace-control-work/`

It reads task-local `workflow.json`, `resume.md`, and `SUMMARY.md` when
present. `planned/` Markdown notes are included as backlog entries. Missing
roots are represented explicitly in the index.

## Boundary

The generated index is for discovery only. The owning task root remains the
authoritative source for lifecycle, validation, and closeoff.
