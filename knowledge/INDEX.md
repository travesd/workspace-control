# Knowledge Index

This directory is the provider-neutral home for reusable workspace learnings.

## Status

Initial scaffold, 2026-05-20.

Current seed material:

- `imported/claude-memory/` - raw copied Claude workspace memory files. These are imported for migration, not yet normalized.
- `workspace-organization-efficiency-20260520.md` - summary of the organization review and first recommendations.

## Note Format

Normalized notes should be flat files under `knowledge/` with frontmatter:

```yaml
---
title: Short title
tags: [workspace, review]
status: active
verified: 2026-05-20
source: /path/to/source/artifact.md
re_verify_when: "Condition that should trigger review"
---
```

Use tags rather than early subdirectories until the corpus is large enough to need a deeper taxonomy.
