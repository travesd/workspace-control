# Detection Platform Metal Skills

This directory holds draft render-input copies of detection-platform-metal
specific skills for `tools/renderctl dry-run --mode skills`.

The current live-compatible canonical source remains `agent-skills/skills/`
until explicit activation. Keep these draft copies synchronized with the
compatibility tree; do not treat them as live skill authority yet.

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
