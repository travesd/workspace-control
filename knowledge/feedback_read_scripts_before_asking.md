---
title: "Read canonical scripts and code before asking scope questions"
description: "When a task could plausibly be defined by an existing script or code path, find and read it before asking the user clarifying questions."
type: feedback
tags: [feedback, memory-migration]
status: active
scope: workspace
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

When the user asks for a broad task ("backup all production X", "restore everything", "sync env Y → Z"), assume a canonical script or code path already defines what "all X" means. Grep for `migrate*.sh`, `backup*.sh`, `sync*.sh`, `restore*.sh`, `*export*`, `*restore*` in the repo and read it BEFORE asking the user clarifying questions about scope, table lists, or sequencing.

**Why**: The user has corrected this twice in one session — first by saying "you havent even looked at the code have you?" when I asked about time-window scoping for snapshots without checking the schema, then by pointing me at `migrate.sh` after I asked tier/scope questions without finding it. The canonical script answered most of those questions (`migrate.sh` defines critical detection data as: clients+assets, enrichment_snapshots, detection_data including ssdeep_hash + ssdeep_cluster target_types, rules, feeder settings, gatekeeper limits, TR publishing configs).

**How to apply**:
- Before asking AskUserQuestion about "what counts as X" or "which tables", spend up to a minute on `find . -name 'migrate*'` / `grep -ri 'backup\|sync\|restore' --include='*.sh' --include='*.md' --include='*.py'` / reading top-level `tools/`, `scripts/`, `infrastructure/` directories.
- If a script defines the scope, mirror its structure when proposing the backup/export, instead of inventing your own tier model.
- Ask clarifying questions only for things the code genuinely can't answer (auth/credentials, output location, scope expansions beyond what the script covers, motivation).
- This applies to any domain-specific operation: deployment, migration, export, audit, sync, restore.
