---
name: detection-dataset-export
description: Export detection incident scopes with exact query membership, deduplicated incident versions, and snapshot-shaped materialization while preserving cache-vs-durable provenance.
---

# Detection Dataset Export

Use this skill when creating reusable detection incident scopes, snapshot-shaped exports, or query-membership manifests.

In workspace-control, treat the incident cache model as proposed design guidance until the live `datasetctl` implementation supports explicit retention flags.

## Workflow

1. Write the SQL query in a task or `datasets/adhoc/` directory.
2. Ensure the result includes `incident_id`. Include any columns needed to explain the membership, such as source, type, judgement, outcome, or submitted timestamp.
3. Export through the managed store:

```bash
/workspace/tools/datasets/datasetctl export incidents \
  --env prod \
  --name <short-dataset-name> \
  --sql-file <query.sql> \
  --task-path <task-or-adhoc-path>
```

4. Record the returned `run_id`. Treat that `run_id` as the query result set and the durable scope reference.
5. Materialize only the run you need:

```bash
/workspace/tools/datasets/datasetctl materialize incidents \
  --run-id <run_id> \
  --format ids \
  --output <path>

/workspace/tools/datasets/datasetctl materialize incidents \
  --run-id <run_id> \
  --format snapshot-jsonl \
  --output <path>
```

## Rules

- Do not create standalone CSV/JSONL/Parquet dumps for durable incident exports.
- Do not infer that "already stored" means "selected by this query"; always retrieve by `run_id`.
- Canonical incident versions are deduplicated by source environment, incident ID, and row hash. A changed upstream incident is a new version.
- Snapshot-shaped JSONL is import-ready data only. Do not call import APIs, write to the DB, or promote `detection_data`.
- If the export is meant to match a UI/reporting number, first read the code that computes that metric and record the exact predicates.
- Keep temporary analysis outputs in `/workspace/datasets/adhoc/`; keep reusable data in the managed dataset store.
- For task investigations, prefer durable scope metadata over long-lived local payload copies.
- Preserve full payloads as durable fixtures only when the payload itself is the reusable data product and a manifest explains why.
- Platform recovery snapshots belong under `/workspace/backups/`, not `datasetctl`.
- Do not mention proposed retention/tag flags as available live commands until `datasetctl` implements them.
