# Pi Pilot Activation

The Pi pilot is currently draft-only. `.pi/agents/*.md` and `.pi/workflows/*.json` describe the desired coordination model but are not assumed to be runnable.

## Package Decision

No Pi package is installed or declared by default.

Candidates to review before activation:

- `pi-agents` for project-local agents and workflow graphs.
- `pi-subagents` for delegated agents, if inheritance can be configured explicitly.
- `ultimate-pi` only as a lifecycle-pattern reference.

## Required Activation Evidence

Before enabling any Pi package in `.pi/settings.json`, record:

- package name, version/source, and review notes,
- install command and whether it is project-local,
- generated install directories and ignore rules,
- workflow schema used by `.pi/workflows/*.json`,
- whether child agents inherit project context and shared skills,
- proof that a delegated Pi agent can read workspace rules and shared skills,
- proof that the package does not bypass no-push, Docker-only, or no-secret guardrails.

## Inheritance Requirements

If using a subagent package with explicit inheritance settings, delegated agents must append project context and inherit skills. Do not activate agents that run with a narrow prompt only unless the workflow also injects the relevant workspace guardrails.

## Runtime Artifacts

Keep package installs, caches, runs, sessions, and logs out of git unless a specific artifact is intentionally promoted after review.
