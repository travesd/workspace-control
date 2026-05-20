---
name: autohunt-ground-truth-review
description: Review autohunt AI evaluator result batches and produce structured ground-truth judgements, error categories, confidence, and concise reasoning per incident.
---

# Autohunt Ground Truth Review

Use this skill when validating autohunt evaluator output from CSV batches or merging agent review results into a ground-truth dataset.

## Input

The expected CSV columns are:

- `incident_id`
- `safe_domain`
- `subject`
- `ai_judgement`
- `rule_judgement`
- `reasoning`
- `page_title`
- `inner_text`

## Review Workflow

1. Split large CSVs into batches when needed.
2. For each row, decide whether the subject targets the protected brand represented by `safe_domain`.
3. Assign one ground-truth judgement: `safe`, `monitor`, `suspicious`, `takedown`, or `misrouted`.
4. Assign one error type: `correct`, `false_positive`, `false_negative`, `wrong_severity`, or `misrouted`.
5. Assign one category tag and write one or two sentences of reasoning.
6. Produce JSON review files and merge them into a CSV/summary only after reviewing all batches.

## Helper Scripts

Run helper scripts in a container from the directory containing the input/output files:

```bash
docker run --rm -v /workspace:/workspace -w "$PWD" python:3.12-slim \
  python /workspace/agent-skills/skills/autohunt-ground-truth-review/scripts/run-review.py \
  --input all-results.csv \
  --output-dir review-batches \
  --batch-size 100

docker run --rm -v /workspace:/workspace -w "$PWD" python:3.12-slim \
  python /workspace/agent-skills/skills/autohunt-ground-truth-review/scripts/merge-reviews.py \
  --input-dir review-batches \
  --output ground-truths.csv
```

Write durable review outputs under `/workspace/datasets/adhoc/` or a named dataset directory, not `/workspace/data`.

## Detailed Rubric

Read `references/autohunt-review-rubric.md` when you need judgement definitions, category tags, examples, or the exact JSON output schema.
