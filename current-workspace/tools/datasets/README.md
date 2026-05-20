# Detection Dataset Utility

`datasetctl` is the shared Claude/Codex command surface for reusable detection
exports. It runs in Docker and writes to `/workspace/datasets/detection`.

## Guarantees

- DB access is read-only and goes through `/workspace/tools/db/dbctl`.
- Durable incident payloads are deduplicated by
  `source_env + incident_id + row_hash`.
- Query results are stored as run memberships. Tasks must retrieve by `run_id`,
  so they only operate on incidents selected by their query.
- Snapshot JSONL is generated for future `/api/v1/snapshots/import` use.
- `datasetctl` does not import snapshots and never promotes `detection_data`.
- The wrapper serializes access with `/workspace/.agent-datasets/catalog.lock`
  because DuckDB allows only one writer process at a time.

## Commands

```bash
/workspace/tools/datasets/datasetctl init
```

Export incidents from a SQL query. The query must return an `incident_id`
column. Other selected columns are preserved in the run membership row.

```bash
/workspace/tools/datasets/datasetctl export incidents \
  --env prod \
  --name llm-rethink-seed \
  --sql-file /workspace/datasets/adhoc/llm-rethink-query.sql \
  --task-path /workspace/detection-platform-metal-work/busy/llm-rethink-domain-llm-v2
```

Inspect and re-materialize an exact run:

```bash
/workspace/tools/datasets/datasetctl runs list
/workspace/tools/datasets/datasetctl runs show <run_id>

/workspace/tools/datasets/datasetctl materialize incidents \
  --run-id <run_id> \
  --format snapshot-jsonl \
  --output /workspace/datasets/adhoc/<task>/snapshots.jsonl
```

## Snapshot Export Shape

Each export writes:

```text
/workspace/datasets/detection/manifests/runs/<run_id>/snapshot_import_requests.jsonl
```

Each line is shaped like detection-core `ImportSnapshotRequest`:

```json
{
  "clientId": "...",
  "subject": "...",
  "type": "domain",
  "snapshotType": "incident",
  "snapshotSource": "local-dataset",
  "snapshotSourceRef": "dataset:prod:incident:<incident_id>:<row_hash_prefix>",
  "snapshotMeta": {
    "localDataset": "detection",
    "localRunId": "<run_id>",
    "querySha256": "...",
    "sourceEnv": "prod",
    "sourceIncidentId": "...",
    "incidentRowHash": "...",
    "promotionPolicy": "manual-only",
    "detectionDataPromotion": "not-automatic"
  },
  "data": {}
}
```

The future import path must use the API, not DB writes. API credentials are
expected to come from the existing `*-new.env` files when import tooling is
added later.

Records whose source incident type is not `domain` or `social` are preserved
with their original type and marked `snapshotMeta.snapshotImportReady = false`;
the tool does not coerce them into an importable type.
