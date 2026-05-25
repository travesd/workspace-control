#!/usr/bin/env python3
"""Merge agent review outputs into a single ground truth CSV and summary.

Usage:
    python3 merge-reviews.py --input-dir review-batches --output ground-truths.csv

Expects review-batches/batch-NNN.review.json files (agent output).
Produces:
    ground-truths.csv          — full dataset with ground truth columns added
    ground-truths-summary.json — aggregate accuracy metrics
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

csv.field_size_limit(sys.maxsize)


def main():
    parser = argparse.ArgumentParser(description="Merge agent review outputs")
    parser.add_argument("--input-dir", required=True, help="Directory with batch-NNN.review.json files")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    review_files = sorted(input_dir.glob("batch-*.review.json"))

    if not review_files:
        print(f"No review files found in {input_dir}/")
        print(f"Expected files like: batch-001.review.json")
        sys.exit(1)

    print(f"Found {len(review_files)} review files")

    # Merge all results
    all_results = []
    batch_summaries = []
    for rf in review_files:
        data = json.loads(rf.read_text())
        batch_id = data.get("batch_id", rf.stem)
        results = data.get("results", [])
        all_results.extend(results)
        if "summary" in data:
            batch_summaries.append({"batch_id": batch_id, **data["summary"]})
        print(f"  {rf.name}: {len(results)} results")

    print(f"\nTotal results: {len(all_results)}")

    # Write merged CSV
    fieldnames = [
        "incident_id", "safe_domain", "subject",
        "ai_judgement", "ground_truth", "agrees",
        "confidence", "error_type", "category", "reasoning",
    ]
    output_path = Path(args.output)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in all_results:
            writer.writerow(r)

    print(f"Wrote {len(all_results)} rows to {output_path}")

    # Compute aggregate summary
    agrees = sum(1 for r in all_results if r.get("agrees"))
    disagrees = len(all_results) - agrees
    accuracy = agrees / len(all_results) if all_results else 0

    gt_dist = defaultdict(int)
    ai_dist = defaultdict(int)
    error_dist = defaultdict(int)
    category_dist = defaultdict(int)
    confidence_dist = defaultdict(int)

    # Per-brand accuracy
    brand_stats = defaultdict(lambda: {"total": 0, "agrees": 0, "disagrees": 0})

    for r in all_results:
        gt_dist[r.get("ground_truth", "unknown")] += 1
        ai_dist[r.get("ai_judgement", "unknown")] += 1
        error_dist[r.get("error_type", "unknown")] += 1
        category_dist[r.get("category", "unknown")] += 1
        confidence_dist[r.get("confidence", "unknown")] += 1

        sd = r.get("safe_domain", "unknown")
        brand_stats[sd]["total"] += 1
        if r.get("agrees"):
            brand_stats[sd]["agrees"] += 1
        else:
            brand_stats[sd]["disagrees"] += 1

    # Sort brands by disagree count
    worst_brands = sorted(
        brand_stats.items(),
        key=lambda x: x[1]["disagrees"],
        reverse=True,
    )[:20]

    summary = {
        "merged_at": datetime.now(timezone.utc).isoformat(),
        "total": len(all_results),
        "agrees": agrees,
        "disagrees": disagrees,
        "accuracy": round(accuracy, 4),
        "ground_truth_distribution": dict(gt_dist),
        "ai_judgement_distribution": dict(ai_dist),
        "error_type_distribution": dict(error_dist),
        "category_distribution": dict(category_dist),
        "confidence_distribution": dict(confidence_dist),
        "worst_brands": [
            {"brand": b, **s} for b, s in worst_brands if s["disagrees"] > 0
        ],
        "batch_summaries": batch_summaries,
    }

    summary_path = output_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"Summary: {summary_path}")

    # Print key metrics
    print(f"\n=== Aggregate Metrics ===")
    print(f"  Accuracy: {accuracy:.1%} ({agrees}/{len(all_results)})")
    print(f"  Ground truth: {dict(gt_dist)}")
    print(f"  Error types: {dict(error_dist)}")
    print(f"\n  Worst brands (by disagreement count):")
    for b, s in worst_brands[:10]:
        if s["disagrees"] > 0:
            acc = s["agrees"] / s["total"] if s["total"] else 0
            print(f"    {b:<30} {s['disagrees']:>3} disagree / {s['total']:>3} total ({acc:.0%} acc)")


if __name__ == "__main__":
    main()
