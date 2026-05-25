---
name: db-readonly-investigation
description: Investigate the detection PostgreSQL database safely through the workspace DB utility container, preserving read-only access, query evidence, and output provenance.
---

# DB Read-Only Investigation

Use this skill for detection DB inspection, counts, samples, or export preparation.

## Workflow

1. Use the workspace utility container:

```bash
/workspace/tools/db/dbctl doctor prod
/workspace/tools/db/dbctl query "select current_database(), current_user;"
```

2. Keep queries read-only. Do not write to the DB, modify schema, or call production mutation APIs.
3. Save non-durable query notes under the active task or `/workspace/datasets/adhoc/`.
4. For durable incident exports, switch to `$detection-dataset-export` instead of writing ad-hoc dumps.
5. Stop the tunnel when finished unless the user is actively continuing DB work:

```bash
/workspace/tools/db/dbctl stop
```

## Evidence To Record

- target environment
- SQL file or exact query
- date/time window and timezone
- row counts and important breakdowns
- output path
- whether the operation was read-only

Do not print secrets from `/workspace/db.env` or any environment file.
