#!/usr/bin/env python3
"""Split all-results.csv into agent-sized batches for ground truth review.

Usage:
    python3 run-review.py --input all-results.csv --output-dir review-batches --batch-size 100

Creates:
    review-batches/
        batch-001.csv   (100 rows)
        batch-002.csv   (100 rows)
        ...
        manifest.json   (batch metadata)
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

csv.field_size_limit(sys.maxsize)


def main():
    parser = argparse.ArgumentParser(description="Split results CSV into review batches")
    parser.add_argument("--input", required=True, help="Input CSV file (all-results.csv)")
    parser.add_argument("--output-dir", required=True, help="Output directory for batches")
    parser.add_argument("--batch-size", type=int, default=100, help="Rows per batch (default: 100)")
    parser.add_argument("--only-with-judgement", action="store_true",
                        help="Only include rows that have an AI judgement")
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    # Read input
    with open(args.input) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    if args.only_with_judgement:
        original = len(rows)
        rows = [r for r in rows if r.get("ai_judgement", "").strip()
                and r["ai_judgement"].strip() not in ("N/A", "")]
        print(f"Filtered to {len(rows)} rows with AI judgement (from {original})")

    # Sort by safe_domain for locality
    rows.sort(key=lambda r: (r.get("safe_domain", ""), r.get("subject", "")))

    # Split into batches
    batches = []
    for i in range(0, len(rows), args.batch_size):
        batch_rows = rows[i:i + args.batch_size]
        batch_num = len(batches) + 1
        batch_name = f"batch-{batch_num:03d}"
        batch_file = output / f"{batch_name}.csv"

        with open(batch_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(batch_rows)

        # Collect brand distribution for this batch
        brands = {}
        for r in batch_rows:
            sd = r.get("safe_domain", "unknown")
            brands[sd] = brands.get(sd, 0) + 1

        batches.append({
            "batch_id": batch_name,
            "file": batch_file.name,
            "rows": len(batch_rows),
            "brands": brands,
        })

    # Write manifest
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_file": str(args.input),
        "total_rows": len(rows),
        "batch_size": args.batch_size,
        "total_batches": len(batches),
        "batches": batches,
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"Created {len(batches)} batches in {output}/")
    print(f"  Total rows: {len(rows)}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
