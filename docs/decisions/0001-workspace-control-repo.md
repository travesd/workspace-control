# ADR 0001: Create A Workspace Control Repo

Date: 2026-05-20
Status: accepted

## Context

The workspace has strong conventions in `/workspace/AGENTS.md`, shared skills under `/workspace/agent-skills/`, task artifacts under `/workspace/detection-platform-metal-work/`, and provider-local memory under Claude/Codex home directories.

The 2026-05-20 organization review found that reusable learnings, session recovery metadata, and human indexes drift across long-running multi-agent work.

## Decision

Create `/workspace/workspace-control` as a separate local git repo for the workspace operating model.

It will version-control:

- current workspace instructions,
- shared skills,
- provider-neutral knowledge notes,
- process decisions,
- templates and future helper scripts,
- a Pi harness pilot track.

It will not vendor product repo code, raw datasets, backups, env files, credentials, provider transcripts, or large task artifacts.

## Consequences

- The workspace gets a reviewable history for process and harness changes.
- Claude, Codex, and Pi can consume the same canonical files.
- This repo introduces another artifact that must be kept current, so close-off and durable-learning workflows should update it deliberately.
