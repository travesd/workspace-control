---
name: validating-ground-truths
description: Review, create, or correct ground-truth expected outputs for detection LLM classifier tests, including domain and social incident judgement, safeDomain, and tag decisions.
---

# Validating Ground Truths

Use this skill when reviewing classifier expected files, auditing ground-truth labels, or deciding the correct judgement for a domain or social incident.

## Core Workflow

1. Locate the incident data, classifier rubric, and the relevant brand/social corpus before judging.
2. Treat corpus data as the authority for official domains, social accounts, and protected entities. Do not rely on general knowledge.
3. Extract the observable incident signals: subject, page content, redirects, enrichment data, classifier outputs, safeDomain, tags, and any corpus matches.
4. Decide the correct expected output: `judgement`, `safeDomain`, and tags.
5. Record the reasoning and any uncertainty. If the corpus is missing an apparently legitimate asset, flag it for human/corpus follow-up instead of silently marking it safe.

## Key Rules

- The brand/social corpus is the source of truth for legitimacy.
- `clientId` is downstream routing state, not evidence for the classifier expected output.
- Content-similarity results are signals, not verdicts; generic infrastructure pages can taint similarity matches.
- A valid typosquat is usually `monitor` even when the page is parked, empty, 404, or scrape-failed.
- Common-word brands can be safe only when the incident content clearly shows an unrelated business.
- Social account matches must be exact URL or alias matches on the same platform.

## Detailed Rubric

Read `references/ground-truth-rubric.md` when you need the full decision framework, examples, batch review structure, or common validation mistakes.
