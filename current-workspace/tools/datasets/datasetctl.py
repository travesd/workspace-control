#!/usr/bin/env python3
"""Managed local detection dataset exports.

This tool is intentionally provider-neutral: Claude and Codex use the same
commands, catalog, manifests, and snapshot-shaped export artifacts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any

import duckdb
import psycopg
from psycopg.rows import dict_row
import pyarrow.parquet as pq


WORKSPACE_ROOT = Path(os.environ.get("WORKSPACE_ROOT", "/workspace"))
DATASET_ROOT = Path(os.environ.get("DATASET_ROOT", str(WORKSPACE_ROOT / "datasets" / "detection")))
CATALOG_PATH = DATASET_ROOT / "catalog.duckdb"
MANIFESTS_DIR = DATASET_ROOT / "manifests"
RUNS_DIR = MANIFESTS_DIR / "runs"
QUERIES_DIR = MANIFESTS_DIR / "queries"
PARQUET_DIR = DATASET_ROOT / "parquet"

RELATED_TABLES = [
    "dom_infos",
    "http_req_infos",
    "social_data_infos",
    "url_infos",
    "asn_infos",
    "cert_infos",
    "dns_infos",
    "whois_infos",
    "ip_whois_infos",
    "classification_results",
    "rule_results",
    "gatekeeper_submissions",
]

RELATED_FIELD_MAP = {
    "dom_infos": "domInfo",
    "http_req_infos": "httpReqInfo",
    "social_data_infos": "socialData",
    "url_infos": "urlInfo",
    "asn_infos": "asnInfo",
    "cert_infos": "certInfo",
    "dns_infos": "dnsInfo",
    "whois_infos": "whoisInfo",
    "ip_whois_infos": "ipWhoisInfo",
}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC).replace(microsecond=0)


def json_default(value: Any) -> str:
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    return str(value)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=json_default)


def pretty_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2, default=json_default)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip().lower()).strip("-")
    return slug[:80] or "export"


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        value = raw_value.strip().strip('"').strip("'")
        values[key] = value
    return values


def ensure_dirs() -> None:
    for path in [
        DATASET_ROOT,
        MANIFESTS_DIR,
        RUNS_DIR,
        QUERIES_DIR,
        PARQUET_DIR,
        PARQUET_DIR / "incident_versions",
        PARQUET_DIR / "incident_current",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def catalog() -> duckdb.DuckDBPyConnection:
    ensure_dirs()
    con = duckdb.connect(str(CATALOG_PATH))
    con.execute("SET timezone='UTC'")
    return con


def init_catalog() -> None:
    con = catalog()
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS export_runs (
            run_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            entity TEXT NOT NULL,
            source_env TEXT NOT NULL,
            query_sha256 TEXT NOT NULL,
            query_path TEXT,
            task_path TEXT,
            created_at TIMESTAMP NOT NULL,
            created_by TEXT,
            command TEXT,
            sql_text TEXT,
            row_count BIGINT NOT NULL,
            distinct_incident_count BIGINT NOT NULL,
            output_dir TEXT NOT NULL,
            snapshot_jsonl_path TEXT,
            notes TEXT
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS export_memberships (
            run_id TEXT NOT NULL,
            ordinal BIGINT NOT NULL,
            source_env TEXT NOT NULL,
            incident_id TEXT NOT NULL,
            row_hash TEXT,
            query_row_json TEXT NOT NULL,
            matched_at TIMESTAMP NOT NULL,
            PRIMARY KEY (run_id, ordinal)
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS incident_versions (
            source_env TEXT NOT NULL,
            incident_id TEXT NOT NULL,
            row_hash TEXT NOT NULL,
            source_created_at TIMESTAMP,
            source_updated_at TIMESTAMP,
            payload_json TEXT NOT NULL,
            first_seen_run_id TEXT NOT NULL,
            first_seen_at TIMESTAMP NOT NULL,
            PRIMARY KEY (source_env, incident_id, row_hash)
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS incident_current (
            source_env TEXT NOT NULL,
            incident_id TEXT NOT NULL,
            row_hash TEXT NOT NULL,
            source_created_at TIMESTAMP,
            source_updated_at TIMESTAMP,
            payload_json TEXT NOT NULL,
            last_seen_run_id TEXT NOT NULL,
            last_seen_at TIMESTAMP NOT NULL,
            PRIMARY KEY (source_env, incident_id)
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS incident_related_versions (
            source_env TEXT NOT NULL,
            table_name TEXT NOT NULL,
            source_pk TEXT NOT NULL,
            incident_id TEXT NOT NULL,
            row_hash TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            first_seen_run_id TEXT NOT NULL,
            first_seen_at TIMESTAMP NOT NULL,
            PRIMARY KEY (source_env, table_name, source_pk, row_hash)
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS snapshot_exports (
            local_snapshot_ref TEXT NOT NULL,
            run_id TEXT NOT NULL,
            source_env TEXT NOT NULL,
            incident_id TEXT NOT NULL,
            incident_row_hash TEXT NOT NULL,
            subject TEXT,
            type TEXT,
            client_id TEXT,
            snapshot_type TEXT NOT NULL,
            snapshot_source TEXT NOT NULL,
            snapshot_source_ref TEXT NOT NULL,
            snapshot_meta_json TEXT NOT NULL,
            data_hash TEXT NOT NULL,
            snapshot_json TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            PRIMARY KEY (run_id, local_snapshot_ref)
        )
        """
    )
    ensure_snapshot_exports_schema(con)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS file_manifest (
            file_path TEXT PRIMARY KEY,
            file_type TEXT NOT NULL,
            table_name TEXT,
            partition_values_json TEXT,
            row_count BIGINT,
            content_hash TEXT,
            run_id TEXT,
            created_at TIMESTAMP NOT NULL
        )
        """
    )
    con.close()
    write_dataset_readme()


def ensure_snapshot_exports_schema(con: duckdb.DuckDBPyConnection) -> None:
    rows = con.execute("PRAGMA table_info('snapshot_exports')").fetchall()
    pk_cols = [row[1] for row in rows if row[5]]
    if set(pk_cols) == {"run_id", "local_snapshot_ref"}:
        return
    if pk_cols == ["local_snapshot_ref"]:
        con.execute("ALTER TABLE snapshot_exports RENAME TO snapshot_exports_old")
        con.execute(
            """
            CREATE TABLE snapshot_exports (
                local_snapshot_ref TEXT NOT NULL,
                run_id TEXT NOT NULL,
                source_env TEXT NOT NULL,
                incident_id TEXT NOT NULL,
                incident_row_hash TEXT NOT NULL,
                subject TEXT,
                type TEXT,
                client_id TEXT,
                snapshot_type TEXT NOT NULL,
                snapshot_source TEXT NOT NULL,
                snapshot_source_ref TEXT NOT NULL,
                snapshot_meta_json TEXT NOT NULL,
                data_hash TEXT NOT NULL,
                snapshot_json TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                PRIMARY KEY (run_id, local_snapshot_ref)
            )
            """
        )
        con.execute(
            """
            INSERT OR IGNORE INTO snapshot_exports
            SELECT local_snapshot_ref, run_id, source_env, incident_id,
                   incident_row_hash, subject, type, client_id, snapshot_type,
                   snapshot_source, snapshot_source_ref, snapshot_meta_json,
                   data_hash, snapshot_json, created_at
            FROM snapshot_exports_old
            """
        )
        con.execute("DROP TABLE snapshot_exports_old")


def write_dataset_readme() -> None:
    readme = DATASET_ROOT / "README.md"
    if readme.exists():
        return
    readme.write_text(
        """# Detection Dataset Store

Managed local store for reusable detection exports.

- Use `/workspace/tools/datasets/datasetctl`; do not write durable query dumps here by hand.
- Database access is read-only and goes through `/workspace/tools/db/dbctl`.
- Canonical incident payloads are deduplicated by `source_env + incident_id + row_hash`.
- Query results are stored as run memberships, so tasks retrieve by `run_id` rather than by scanning all local incidents.
- Snapshot JSONL artifacts are shaped for future `/api/v1/snapshots/import` use, but this tooling does not import snapshots or promote detection data.

Current API env discovery paths:

- `/workspace/classifiers.pipeline-prod-new.env`
- `/workspace/classifiers.pipeline-staging-new.env`

Those files are referenced by path only; dataset exports must not print secrets.
""",
        encoding="utf-8",
    )


def db_connect() -> psycopg.Connection:
    env_file = Path(os.environ.get("DB_ENV_FILE", str(WORKSPACE_ROOT / "db.env")))
    env_values = load_env_file(env_file)
    user = os.environ.get("PGUSER") or env_values.get("psql_username")
    password = os.environ.get("PGPASSWORD") or env_values.get("psql_password")
    dbname = os.environ.get("PGDATABASE") or env_values.get("DB_NAME") or "detection"
    host = os.environ.get("PGHOST") or "detection-db-tunnel"
    port = int(os.environ.get("PGPORT") or "25432")
    if not user or not password:
        raise SystemExit(f"Missing psql_username/psql_password in {env_file}")
    return psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        connect_timeout=15,
        sslmode="disable",
        row_factory=dict_row,
    )


def strip_sql(sql: str) -> str:
    sql = sql.strip()
    while sql.endswith(";"):
        sql = sql[:-1].rstrip()
    return sql


def read_query_rows(conn: psycopg.Connection, sql_path: Path, limit: int | None) -> tuple[str, list[dict[str, Any]]]:
    sql_text = strip_sql(sql_path.read_text(encoding="utf-8"))
    wrapped = f"SELECT * FROM ({sql_text}) AS datasetctl_query"
    if limit is not None:
        if limit < 1:
            raise SystemExit("--limit must be greater than zero")
        wrapped = f"{wrapped} LIMIT {int(limit)}"
    with conn.cursor() as cur:
        cur.execute(wrapped)
        rows = list(cur.fetchall())
    if rows and "incident_id" not in rows[0]:
        raise SystemExit("Export query must return an incident_id column")
    return sql_text, rows


def unique_incident_ids(rows: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    ids: list[str] = []
    for row in rows:
        incident_id = row.get("incident_id")
        if incident_id is None:
            raise SystemExit("Export query returned a row with null incident_id")
        key = str(incident_id)
        if key not in seen:
            seen.add(key)
            ids.append(key)
    return ids


def fetch_incidents(conn: psycopg.Connection, incident_ids: list[str]) -> dict[str, dict[str, Any]]:
    if not incident_ids:
        return {}
    found: dict[str, dict[str, Any]] = {}
    sql = """
        SELECT
            i.id::text AS incident_id,
            i.created_at AS source_created_at,
            i.updated_at AS source_updated_at,
            to_jsonb(i) AS payload
        FROM incidents i
        WHERE i.id::text = ANY(%s::text[])
    """
    for chunk in chunks(incident_ids, 1000):
        with conn.cursor() as cur:
            cur.execute(sql, (chunk,))
            for row in cur.fetchall():
                found[str(row["incident_id"])] = row
    missing = sorted(set(incident_ids) - set(found))
    if missing:
        raise SystemExit(f"{len(missing)} incident_id values were not found in incidents")
    return found


def table_has_incident_id(conn: psycopg.Connection, table_name: str) -> bool:
    sql = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
              AND column_name = 'incident_id'
        ) AS exists
    """
    with conn.cursor() as cur:
        cur.execute(sql, (table_name,))
        row = cur.fetchone()
    return bool(row and row["exists"])


def table_has_id(conn: psycopg.Connection, table_name: str) -> bool:
    sql = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
              AND column_name = 'id'
        ) AS exists
    """
    with conn.cursor() as cur:
        cur.execute(sql, (table_name,))
        row = cur.fetchone()
    return bool(row and row["exists"])


def fetch_related(conn: psycopg.Connection, incident_ids: list[str]) -> dict[str, list[dict[str, Any]]]:
    related: dict[str, list[dict[str, Any]]] = {}
    if not incident_ids:
        return related
    for table in RELATED_TABLES:
        if not table_has_incident_id(conn, table):
            continue
        pk_expr = "t.id::text" if table_has_id(conn, table) else "t.incident_id::text"
        sql = f"""
            SELECT
                t.incident_id::text AS incident_id,
                {pk_expr} AS source_pk,
                to_jsonb(t) AS payload
            FROM {table} t
            WHERE t.incident_id::text = ANY(%s::text[])
        """
        rows: list[dict[str, Any]] = []
        for chunk in chunks(incident_ids, 1000):
            with conn.cursor() as cur:
                cur.execute(sql, (chunk,))
                rows.extend(cur.fetchall())
        if rows:
            related[table] = rows
    return related


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[i : i + size] for i in range(0, len(values), size)]


def maybe_json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def extract_payload_value(payload: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in payload and payload[key] not in (None, ""):
            return payload[key]
    return None


def incident_created_date(row: dict[str, Any]) -> str:
    value = row.get("source_created_at")
    if isinstance(value, dt.datetime):
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    payload = maybe_json(row.get("payload_json") or row.get("payload") or {})
    if isinstance(payload, dict):
        created = extract_payload_value(payload, "created_at", "createdAt")
        if created:
            return str(created)[:10]
    return "unknown"


def upsert_export(
    con: duckdb.DuckDBPyConnection,
    *,
    run_id: str,
    source_env: str,
    rows: list[dict[str, Any]],
    incidents: dict[str, dict[str, Any]],
    related: dict[str, list[dict[str, Any]]],
    created_at: dt.datetime,
) -> dict[str, str]:
    incident_hashes: dict[str, str] = {}
    version_rows = []
    current_rows = []
    for incident_id, row in incidents.items():
        payload = maybe_json(row["payload"])
        payload_json = canonical_json(payload)
        row_hash = sha256_text(payload_json)
        incident_hashes[incident_id] = row_hash
        version_rows.append(
            (
                source_env,
                incident_id,
                row_hash,
                row.get("source_created_at"),
                row.get("source_updated_at"),
                payload_json,
                run_id,
                created_at,
            )
        )
        current_rows.append(
            (
                source_env,
                incident_id,
                row_hash,
                row.get("source_created_at"),
                row.get("source_updated_at"),
                payload_json,
                run_id,
                created_at,
            )
        )
    con.executemany(
        """
        INSERT OR IGNORE INTO incident_versions
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        version_rows,
    )
    con.executemany(
        """
        INSERT OR REPLACE INTO incident_current
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        current_rows,
    )

    membership_rows = []
    for ordinal, row in enumerate(rows, start=1):
        incident_id = str(row["incident_id"])
        membership_rows.append(
            (
                run_id,
                ordinal,
                source_env,
                incident_id,
                incident_hashes[incident_id],
                canonical_json(row),
                created_at,
            )
        )
    con.executemany(
        """
        INSERT OR REPLACE INTO export_memberships
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        membership_rows,
    )

    related_rows = []
    for table_name, table_rows in related.items():
        for index, row in enumerate(table_rows, start=1):
            payload = maybe_json(row["payload"])
            payload_json = canonical_json(payload)
            row_hash = sha256_text(payload_json)
            source_pk = str(row.get("source_pk") or f"{row['incident_id']}:{index}")
            related_rows.append(
                (
                    source_env,
                    table_name,
                    source_pk,
                    str(row["incident_id"]),
                    row_hash,
                    payload_json,
                    run_id,
                    created_at,
                )
            )
    if related_rows:
        con.executemany(
            """
            INSERT OR IGNORE INTO incident_related_versions
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            related_rows,
        )
    return incident_hashes


def related_for_incident(related: dict[str, list[dict[str, Any]]], incident_id: str) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for table, rows in related.items():
        selected = [maybe_json(row["payload"]) for row in rows if str(row["incident_id"]) == incident_id]
        if selected:
            result[table] = selected
    return result


def build_snapshot_record(
    *,
    run_id: str,
    source_env: str,
    query_sha: str,
    incident_id: str,
    incident_hash: str,
    incident_payload: dict[str, Any],
    related_payloads: dict[str, list[dict[str, Any]]],
    exported_at: dt.datetime,
) -> dict[str, Any]:
    subject = extract_payload_value(incident_payload, "subject", "domain", "url")
    incident_type = extract_payload_value(incident_payload, "type", "incident_type", "incidentType")
    client_id = extract_payload_value(incident_payload, "client_id", "clientId")
    source = extract_payload_value(incident_payload, "source")
    import_ready = incident_type in {"domain", "social"}

    data: dict[str, Any] = {
        "incidentId": incident_id,
        "source": source,
        "type": incident_type,
        "subject": subject,
        "incident": incident_payload,
        "related": related_payloads,
    }
    for table_name, field_name in RELATED_FIELD_MAP.items():
        rows = related_payloads.get(table_name)
        if not rows:
            continue
        if table_name in {"asn_infos", "dns_infos"}:
            data[field_name] = rows
        else:
            data[field_name] = rows[0]

    snapshot_source_ref = f"dataset:{source_env}:incident:{incident_id}:{incident_hash[:12]}"
    snapshot_meta = {
        "localDataset": "detection",
        "localRunId": run_id,
        "querySha256": query_sha,
        "sourceEnv": source_env,
        "sourceIncidentId": incident_id,
        "incidentRowHash": incident_hash,
        "exportedAt": exported_at.isoformat().replace("+00:00", "Z"),
        "snapshotImportReady": import_ready,
        "promotionPolicy": "manual-only",
        "detectionDataPromotion": "not-automatic",
    }
    if not import_ready:
        snapshot_meta["snapshotImportBlockedReason"] = "detection-core snapshot import currently accepts type=domain or type=social"
    return {
        "clientId": client_id,
        "subject": subject or incident_id,
        "type": incident_type or "unknown",
        "snapshotType": "incident",
        "snapshotSource": "local-dataset",
        "snapshotSourceRef": snapshot_source_ref,
        "snapshotMeta": snapshot_meta,
        "data": data,
        "parentSnapshotId": None,
    }


def write_snapshot_exports(
    con: duckdb.DuckDBPyConnection,
    *,
    run_id: str,
    source_env: str,
    query_sha: str,
    incidents: dict[str, dict[str, Any]],
    related: dict[str, list[dict[str, Any]]],
    incident_hashes: dict[str, str],
    output_path: Path,
    created_at: dt.datetime,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with output_path.open("w", encoding="utf-8") as out:
        for incident_id in sorted(incidents.keys()):
            incident_payload = maybe_json(incidents[incident_id]["payload"])
            rel = related_for_incident(related, incident_id)
            row_hash = incident_hashes[incident_id]
            snapshot = build_snapshot_record(
                run_id=run_id,
                source_env=source_env,
                query_sha=query_sha,
                incident_id=incident_id,
                incident_hash=row_hash,
                incident_payload=incident_payload,
                related_payloads=rel,
                exported_at=created_at,
            )
            snapshot_json = canonical_json(snapshot)
            out.write(snapshot_json + "\n")
            local_ref = snapshot["snapshotSourceRef"]
            meta_json = canonical_json(snapshot["snapshotMeta"])
            data_hash = sha256_text(canonical_json(snapshot["data"]))
            rows.append(
                (
                    local_ref,
                    run_id,
                    source_env,
                    incident_id,
                    row_hash,
                    snapshot.get("subject"),
                    snapshot.get("type"),
                    snapshot.get("clientId"),
                    snapshot["snapshotType"],
                    snapshot["snapshotSource"],
                    snapshot["snapshotSourceRef"],
                    meta_json,
                    data_hash,
                    snapshot_json,
                    created_at,
                )
            )
    con.executemany(
        """
        INSERT OR REPLACE INTO snapshot_exports
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    record_file(con, output_path, "snapshot-jsonl", "snapshot_exports", None, len(rows), run_id)


def record_file(
    con: duckdb.DuckDBPyConnection,
    path: Path,
    file_type: str,
    table_name: str | None,
    partition_values: dict[str, Any] | None,
    row_count: int | None,
    run_id: str | None,
) -> None:
    content_hash = None
    if path.exists() and path.is_file():
        content_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    con.execute(
        """
        INSERT OR REPLACE INTO file_manifest
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(path),
            file_type,
            table_name,
            canonical_json(partition_values) if partition_values else None,
            row_count,
            content_hash,
            run_id,
            utc_now(),
        ),
    )


def rewrite_incident_parquet(con: duckdb.DuckDBPyConnection, source_env: str, incident_ids: list[str], run_id: str) -> None:
    if not incident_ids:
        return
    placeholders = ",".join(["?"] * len(incident_ids))
    rows = con.execute(
        f"""
        SELECT source_env, incident_id, row_hash, source_created_at, source_updated_at, payload_json
        FROM incident_current
        WHERE source_env = ? AND incident_id IN ({placeholders})
        """,
        [source_env, *incident_ids],
    ).fetchall()
    dates = sorted({incident_created_date({"source_created_at": row[3], "payload_json": row[5]}) for row in rows})
    for created_date in dates:
        out_dir = PARQUET_DIR / "incident_current" / f"source_env={source_env}" / f"created_date={created_date}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "data.parquet"
        table = con.execute(
            """
            SELECT source_env, incident_id, row_hash, source_created_at, source_updated_at, payload_json
            FROM incident_current
            WHERE source_env = ?
              AND COALESCE(LEFT(CAST(source_created_at AS VARCHAR), 10), 'unknown') = ?
            ORDER BY incident_id
            """,
            [source_env, created_date],
        ).to_arrow_table()
        tmp_path = out_path.with_suffix(".tmp.parquet")
        pq.write_table(table, tmp_path)
        tmp_path.replace(out_path)
        record_file(
            con,
            out_path,
            "parquet",
            "incident_current",
            {"source_env": source_env, "created_date": created_date},
            table.num_rows,
            run_id,
        )


def write_run_manifest(
    *,
    run_id: str,
    name: str,
    source_env: str,
    sql_path: Path,
    query_sha: str,
    row_count: int,
    distinct_incident_count: int,
    output_dir: Path,
    snapshot_jsonl: Path,
    task_path: str | None,
    notes: str | None,
    created_at: dt.datetime,
) -> Path:
    manifest = {
        "runId": run_id,
        "name": name,
        "entity": "incidents",
        "sourceEnv": source_env,
        "createdAt": created_at.isoformat().replace("+00:00", "Z"),
        "querySha256": query_sha,
        "queryPath": str(sql_path),
        "taskPath": task_path,
        "rowCount": row_count,
        "distinctIncidentCount": distinct_incident_count,
        "outputDir": str(output_dir),
        "snapshotJsonlPath": str(snapshot_jsonl),
        "credentials": {
            "dbEnvFile": os.environ.get("DB_ENV_FILE", str(WORKSPACE_ROOT / "db.env")),
            "mode": "readonly-db-export",
            "apiEnvFilesReferenced": [
                os.environ.get("DATASETCTL_API_ENV_PROD", str(WORKSPACE_ROOT / "classifiers.pipeline-prod-new.env")),
                os.environ.get("DATASETCTL_API_ENV_STAGING", str(WORKSPACE_ROOT / "classifiers.pipeline-staging-new.env")),
            ],
        },
        "notes": notes,
        "guarantees": [
            "DB access is read-only.",
            "Incident payload storage is deduplicated by source_env + incident_id + row_hash.",
            "Task retrieval must use run_id membership.",
            "Snapshot JSONL is generated for future import only; no API import or detection_data promotion is performed.",
        ],
    }
    path = RUNS_DIR / f"{run_id}.json"
    path.write_text(pretty_json(manifest) + "\n", encoding="utf-8")
    return path


def cmd_init(_args: argparse.Namespace) -> None:
    init_catalog()
    print(f"dataset_root={DATASET_ROOT}")
    print(f"catalog={CATALOG_PATH}")


def cmd_export_incidents(args: argparse.Namespace) -> None:
    init_catalog()
    sql_path = Path(args.sql_file)
    if not sql_path.exists():
        raise SystemExit(f"SQL file not found: {sql_path}")
    source_env = args.env
    created_at = utc_now()
    name_slug = slugify(args.name)
    sql_text = strip_sql(sql_path.read_text(encoding="utf-8"))
    query_sha = sha256_text(sql_text)
    run_id = f"{created_at.strftime('%Y%m%dT%H%M%SZ')}-{name_slug}-{query_sha[:8]}"
    output_dir = RUNS_DIR / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    query_copy = QUERIES_DIR / f"{query_sha}.sql"
    if not query_copy.exists():
        query_copy.write_text(sql_text + "\n", encoding="utf-8")

    conn = db_connect()
    try:
        sql_text, query_rows = read_query_rows(conn, sql_path, args.limit)
        incident_ids = unique_incident_ids(query_rows)
        incidents = fetch_incidents(conn, incident_ids)
        related = fetch_related(conn, incident_ids) if not args.no_related else {}
    finally:
        conn.close()

    con = catalog()
    try:
        incident_hashes = upsert_export(
            con,
            run_id=run_id,
            source_env=source_env,
            rows=query_rows,
            incidents=incidents,
            related=related,
            created_at=created_at,
        )
        snapshot_jsonl = output_dir / "snapshot_import_requests.jsonl"
        write_snapshot_exports(
            con,
            run_id=run_id,
            source_env=source_env,
            query_sha=query_sha,
            incidents=incidents,
            related=related,
            incident_hashes=incident_hashes,
            output_path=snapshot_jsonl,
            created_at=created_at,
        )
        rewrite_incident_parquet(con, source_env, incident_ids, run_id)
        manifest_path = write_run_manifest(
            run_id=run_id,
            name=args.name,
            source_env=source_env,
            sql_path=sql_path,
            query_sha=query_sha,
            row_count=len(query_rows),
            distinct_incident_count=len(incident_ids),
            output_dir=output_dir,
            snapshot_jsonl=snapshot_jsonl,
            task_path=args.task_path,
            notes=args.notes,
            created_at=created_at,
        )
        con.execute(
            """
            INSERT INTO export_runs
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                args.name,
                "incidents",
                source_env,
                query_sha,
                str(sql_path),
                args.task_path,
                created_at,
                os.environ.get("USER") or os.environ.get("LOGNAME") or "agent",
                " ".join(shlex.quote(part) for part in sys.argv),
                sql_text,
                len(query_rows),
                len(incident_ids),
                str(output_dir),
                str(snapshot_jsonl),
                args.notes,
            ),
        )
        record_file(con, manifest_path, "manifest", "export_runs", None, 1, run_id)
    finally:
        con.close()

    print(f"run_id={run_id}")
    print(f"query_rows={len(query_rows)}")
    print(f"distinct_incidents={len(incident_ids)}")
    print(f"manifest={manifest_path}")
    print(f"snapshot_jsonl={snapshot_jsonl}")


def cmd_runs_list(_args: argparse.Namespace) -> None:
    init_catalog()
    con = catalog()
    try:
        rows = con.execute(
            """
            SELECT run_id, source_env, name, created_at, row_count, distinct_incident_count
            FROM export_runs
            ORDER BY created_at DESC
            LIMIT 50
            """
        ).fetchall()
    finally:
        con.close()
    for row in rows:
        print("\t".join(str(value) for value in row))


def cmd_runs_show(args: argparse.Namespace) -> None:
    init_catalog()
    con = catalog()
    try:
        row = con.execute(
            """
            SELECT run_id, name, entity, source_env, query_sha256, query_path, task_path,
                   created_at, row_count, distinct_incident_count, output_dir,
                   snapshot_jsonl_path, notes
            FROM export_runs
            WHERE run_id = ?
            """,
            [args.run_id],
        ).fetchone()
    finally:
        con.close()
    if not row:
        raise SystemExit(f"Run not found: {args.run_id}")
    keys = [
        "runId",
        "name",
        "entity",
        "sourceEnv",
        "querySha256",
        "queryPath",
        "taskPath",
        "createdAt",
        "rowCount",
        "distinctIncidentCount",
        "outputDir",
        "snapshotJsonlPath",
        "notes",
    ]
    print(pretty_json(dict(zip(keys, row))))


def materialized_rows(con: duckdb.DuckDBPyConnection, run_id: str) -> list[dict[str, Any]]:
    rows = con.execute(
        """
        SELECT
            m.ordinal,
            m.incident_id,
            m.row_hash,
            m.query_row_json,
            v.payload_json,
            s.snapshot_json
        FROM export_memberships m
        JOIN incident_versions v
          ON v.source_env = m.source_env
         AND v.incident_id = m.incident_id
         AND v.row_hash = m.row_hash
        LEFT JOIN snapshot_exports s
          ON s.run_id = m.run_id
         AND s.incident_id = m.incident_id
         AND s.incident_row_hash = m.row_hash
        WHERE m.run_id = ?
        ORDER BY m.ordinal
        """,
        [run_id],
    ).fetchall()
    return [
        {
            "ordinal": row[0],
            "incident_id": row[1],
            "row_hash": row[2],
            "query_row": json.loads(row[3]),
            "incident": json.loads(row[4]),
            "snapshot": json.loads(row[5]) if row[5] else None,
        }
        for row in rows
    ]


def cmd_materialize_incidents(args: argparse.Namespace) -> None:
    init_catalog()
    con = catalog()
    try:
        rows = materialized_rows(con, args.run_id)
    finally:
        con.close()
    if not rows:
        raise SystemExit(f"No incident memberships found for run: {args.run_id}")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as out:
        for row in rows:
            if args.format == "ids":
                out.write(str(row["incident_id"]) + "\n")
            elif args.format == "incident-jsonl":
                out.write(canonical_json(row) + "\n")
            elif args.format == "snapshot-jsonl":
                if row["snapshot"] is None:
                    raise SystemExit(f"Run {args.run_id} has no snapshot export for {row['incident_id']}")
                out.write(canonical_json(row["snapshot"]) + "\n")
            else:
                raise SystemExit(f"Unknown format: {args.format}")
    print(f"rows={len(rows)}")
    print(f"output={output}")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Managed local detection dataset exports")
    sub = p.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize dataset store")
    init.set_defaults(func=cmd_init)

    export = sub.add_parser("export", help="run read-only exports")
    export_sub = export.add_subparsers(dest="entity", required=True)
    export_incidents = export_sub.add_parser("incidents", help="export incidents by query membership")
    export_incidents.add_argument("--env", default=os.environ.get("DB_ENV", "prod"), choices=["prod", "production", "staging", "stage"])
    export_incidents.add_argument("--name", required=True)
    export_incidents.add_argument("--sql-file", required=True)
    export_incidents.add_argument("--task-path")
    export_incidents.add_argument("--notes")
    export_incidents.add_argument("--limit", type=int)
    export_incidents.add_argument("--no-related", action="store_true", help="only export incidents table payloads")
    export_incidents.set_defaults(func=cmd_export_incidents)

    runs = sub.add_parser("runs", help="inspect export runs")
    runs_sub = runs.add_subparsers(dest="runs_command", required=True)
    runs_list = runs_sub.add_parser("list", help="list recent runs")
    runs_list.set_defaults(func=cmd_runs_list)
    runs_show = runs_sub.add_parser("show", help="show one run")
    runs_show.add_argument("run_id")
    runs_show.set_defaults(func=cmd_runs_show)

    materialize = sub.add_parser("materialize", help="materialize exact run memberships")
    materialize_sub = materialize.add_subparsers(dest="materialize_entity", required=True)
    materialize_incidents = materialize_sub.add_parser("incidents")
    materialize_incidents.add_argument("--run-id", required=True)
    materialize_incidents.add_argument("--format", choices=["ids", "incident-jsonl", "snapshot-jsonl"], default="incident-jsonl")
    materialize_incidents.add_argument("--output", required=True)
    materialize_incidents.set_defaults(func=cmd_materialize_incidents)

    return p


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
