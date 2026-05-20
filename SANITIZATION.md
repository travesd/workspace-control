# Sanitization Report

Date: 2026-05-20

## Decision

This repo keeps provider-neutral workspace operating-model material only. Raw provider-local memory exports, provider transcripts, credential files, env files, datasets, backups, and task artifacts are not tracked.

## Actions Taken

- Removed the tracked raw Claude memory import under `knowledge/imported/`.
- Rebuilt `knowledge/*.md` as normalized notes with:
  - `title`
  - `description`
  - `tags`
  - `status`
  - `verified`
  - sanitized `source`
  - `re_verify_when`
- Removed `originSessionId` and provider-local source paths from normalized knowledge notes.
- Sanitized the git-identity note to keep the operational rule without personal account/email details or raw user quotes.
- Replaced provider-local transcript and usage-report paths in research docs with provider-neutral descriptions.
- Hardened `tools/check-sensitive-content` to redact findings and fail on high-confidence secret assignments.

## Retained

- Aggregate counts and process findings from the 2026-05-20 workspace organization investigation where they are useful for planning and do not expose credential values.
- Generic provider-local path conventions inside copied tooling snapshots where the path is part of the tool implementation and does not include credential values.
- `.pi/` draft workflow and agent files, marked as inactive until activation.

## Required Before Remote Push

Run:

```bash
tools/check-sensitive-content .
git status --short
```

Do not create a remote or push if either command reports unreviewed findings.
