# Detection Platform Metal Skills

This directory will hold detection-platform-metal-specific skills after the
skill tree is split.

Candidate workspace overlay skills:

- `autohunt-ground-truth-review`
- `classifier-corpus-coverage`
- `cloudflare-access-observability`
- `daily-submissions-metrics`
- `db-readonly-investigation`
- `detection-dataset-export`
- `detection-ui-browser-review`
- `validating-ground-truths`

These depend on local workspace tools, detection data, product semantics, or
operator access patterns. Keep them out of the portable core layer unless they
are split into a generic core skill plus a workspace reference.

Current canonical source remains `agent-skills/skills/`.
